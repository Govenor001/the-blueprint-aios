#!/usr/bin/env python3
"""Telegram bridge for the owner-facing AIOS command wing."""

import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

from activity import log
from model_for import model_for

ROOT = Path(__file__).resolve().parents[1]
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")
GROQ_KEY = os.environ.get("GROQ_API_KEY", "")


def tg(method, params=None, timeout=70):
    url = "https://api.telegram.org/bot%s/%s" % (TOKEN, method)
    data = urllib.parse.urlencode(params or {}).encode()
    req = urllib.request.Request(url, data=data)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        out = json.loads(resp.read())
    if not out.get("ok"):
        raise RuntimeError("Telegram %s failed: %s" % (method, out))
    return out["result"]


def send(chat_id, text):
    text = text or "(empty reply)"
    for i in range(0, len(text), 3900):
        tg("sendMessage", {"chat_id": chat_id, "text": text[i:i + 3900]})


def ask_claude(prompt):
    try:
        resolved_model = model_for(ROOT, tier="smart")
        log("skill_started", detail=f"telegram model={resolved_model}")
        run = subprocess.run(["claude", "--model", resolved_model, "-p", prompt], cwd=ROOT, capture_output=True, text=True, timeout=300)
        output = run.stdout.strip() or run.stderr.strip() or "(no reply)"
        log("skill_finished", detail=output[-1000:], status="ok" if run.returncode == 0 else "error")
        return output
    except subprocess.TimeoutExpired:
        log("skill_error", detail="telegram request timed out", status="error")
        return "That took over 5 minutes — try a smaller question."
    except FileNotFoundError:
        log("skill_error", detail="claude CLI is not installed", status="error")
        return "`claude` isn't installed on the machine running the bridge."
    except Exception as exc:
        log("skill_error", detail=str(exc), status="error")
        return "The AIOS could not answer that request."


def transcribe(audio_bytes):
    if not GROQ_KEY:
        return None
    boundary = uuid.uuid4().hex
    parts = [
        ('--%s\r\nContent-Disposition: form-data; name="model"\r\n\r\nwhisper-large-v3-turbo\r\n' % boundary).encode(),
        ('--%s\r\nContent-Disposition: form-data; name="file"; filename="voice.oga"\r\nContent-Type: audio/ogg\r\n\r\n' % boundary).encode() + audio_bytes + b"\r\n",
        ("--%s--\r\n" % boundary).encode(),
    ]
    req = urllib.request.Request("https://api.groq.com/openai/v1/audio/transcriptions", data=b"".join(parts), headers={"Authorization": "Bearer " + GROQ_KEY, "Content-Type": "multipart/form-data; boundary=" + boundary})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read()).get("text", "").strip()


def voice_to_text(file_id):
    path = tg("getFile", {"file_id": file_id})["file_path"]
    url = "https://api.telegram.org/file/bot%s/%s" % (TOKEN, path)
    return transcribe(urllib.request.urlopen(url, timeout=60).read())


def check():
    problems = []
    if not TOKEN:
        problems.append("TELEGRAM_BOT_TOKEN is not set")
    else:
        try:
            me = tg("getMe", timeout=15)
            print("+ Bot token valid: @%s" % me.get("username"))
        except Exception as exc:
            problems.append("Bot token rejected by Telegram: %s" % exc)
    if CHAT_ID:
        print("+ TELEGRAM_CHAT_ID set — bridge is locked to you")
    else:
        print("! TELEGRAM_CHAT_ID not set — first message will tell you your id")
    try:
        v = subprocess.run(["claude", "--version"], capture_output=True, text=True, timeout=30)
        print("+ claude CLI found: %s" % v.stdout.strip())
    except Exception:
        problems.append("claude CLI not found on PATH")
    print("+ Voice notes: %s" % ("ON" if GROQ_KEY else "off"))
    if problems:
        print("\nFIX THESE FIRST:")
        for problem in problems:
            print("  x " + problem)
        return 1
    print("\nAll good.")
    return 0


def run_bridge():
    if not TOKEN:
        raise SystemExit("TELEGRAM_BOT_TOKEN not set. Run --check first.")
    offset = 0
    (ROOT / "var").mkdir(exist_ok=True)
    (ROOT / "var" / "bridge.pid").write_text(str(os.getpid()), encoding="utf-8")
    try:
        while True:
            updates = tg("getUpdates", {"offset": offset, "timeout": 60})
            for update in updates:
                offset = update["update_id"] + 1
                msg = update.get("message") or {}
                chat = str(msg.get("chat", {}).get("id", ""))
                if not chat or (CHAT_ID and chat != CHAT_ID):
                    continue
                text = msg.get("text")
                log("message_received", detail=text or "voice message")
                if not CHAT_ID:
                    send(chat, "Your chat id is %s — put TELEGRAM_CHAT_ID=%s in .env and restart the bridge." % (chat, chat))
                    continue
                if not text and msg.get("voice"):
                    text = voice_to_text(msg["voice"]["file_id"])
                    if text is None:
                        send(chat, "Voice notes need GROQ_API_KEY set. Text works right now.")
                        continue
                    send(chat, "Heard: %s" % text)
                if text:
                    send(chat, ask_claude(text))
    finally:
        try:
            (ROOT / "var" / "bridge.pid").unlink()
        except FileNotFoundError:
            pass


def main():
    if "--check" in sys.argv:
        raise SystemExit(check())
    if "--send-stdin" in sys.argv:
        if not (TOKEN and CHAT_ID):
            raise SystemExit("--send-stdin needs TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID set.")
        send(CHAT_ID, sys.stdin.read().strip())
        return
    try:
        run_bridge()
    except KeyboardInterrupt:
        print("\nBridge stopped.")


if __name__ == "__main__":
    main()
