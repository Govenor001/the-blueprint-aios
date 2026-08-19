#!/usr/bin/env python3
"""The Command Wing bridge — talk to your AIOS from Telegram.

Runs on your laptop (Day 6). Text your bot -> it runs `claude -p` in this
repo -> the answer comes back to your phone. Voice notes are transcribed
via Groq Whisper (free) if GROQ_API_KEY is set. Stdlib only.

Usage:
  python3 scripts/bridge.py --check       # verify setup, then exit
  python3 scripts/bridge.py               # run the bridge (Ctrl+C to stop)
  echo "hello" | python3 scripts/bridge.py --send-stdin   # one-shot push

Safety: replies only to TELEGRAM_CHAT_ID once it's set. Claude runs with
its DEFAULT permissions — it can read your AIOS files and answer, but it
will not take privileged actions unattended.
"""
import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request
import uuid

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
        run = subprocess.run(["claude", "-p", prompt], cwd=ROOT,
                             capture_output=True, text=True, timeout=300)
        return run.stdout.strip() or run.stderr.strip() or "(no reply)"
    except subprocess.TimeoutExpired:
        return "That took over 5 minutes — try a smaller question."
    except FileNotFoundError:
        return "`claude` isn't installed on the machine running the bridge."


def transcribe(audio_bytes):
    if not GROQ_KEY:
        return None
    boundary = uuid.uuid4().hex
    parts = [
        ('--%s\r\nContent-Disposition: form-data; name="model"\r\n\r\n'
         'whisper-large-v3-turbo\r\n' % boundary).encode(),
        ('--%s\r\nContent-Disposition: form-data; name="file"; '
         'filename="voice.oga"\r\nContent-Type: audio/ogg\r\n\r\n'
         % boundary).encode() + audio_bytes + b"\r\n",
        ("--%s--\r\n" % boundary).encode(),
    ]
    req = urllib.request.Request(
        "https://api.groq.com/openai/v1/audio/transcriptions",
        data=b"".join(parts),
        headers={"Authorization": "Bearer " + GROQ_KEY,
                 "Content-Type":
                     "multipart/form-data; boundary=" + boundary})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read()).get("text", "").strip()


def voice_to_text(file_id):
    path = tg("getFile", {"file_id": file_id})["file_path"]
    url = "https://api.telegram.org/file/bot%s/%s" % (TOKEN, path)
    audio = urllib.request.urlopen(url, timeout=60).read()
    return transcribe(audio)


def check():
    problems = []
    if not TOKEN:
        problems.append("TELEGRAM_BOT_TOKEN is not set "
                        "(run: set -a && . ./.env && set +a)")
    else:
        try:
            me = tg("getMe", timeout=15)
            print("+ Bot token valid: @%s" % me.get("username"))
        except Exception as exc:
            problems.append("Bot token rejected by Telegram: %s" % exc)
    if CHAT_ID:
        print("+ TELEGRAM_CHAT_ID set (%s) — bridge is locked to you" % CHAT_ID)
    else:
        print("! TELEGRAM_CHAT_ID not set — first message will tell you "
              "your id; set it before leaving the bridge running")
    try:
        v = subprocess.run(["claude", "--version"], capture_output=True,
                           text=True, timeout=30)
        print("+ claude CLI found: %s" % v.stdout.strip())
    except Exception:
        problems.append("`claude` CLI not found on PATH")
    print("+ Voice notes: %s" % ("ON (Groq key set)" if GROQ_KEY
                                 else "off (no GROQ_API_KEY — text only)"))
    if problems:
        print("\nFIX THESE FIRST:")
        for p in problems:
            print("  x " + p)
        sys.exit(1)
    print("\nAll good. Run:  python3 scripts/bridge.py")


def run_bridge():
    if not TOKEN:
        sys.exit("TELEGRAM_BOT_TOKEN not set. Run --check first.")
    print("Bridge running. Message your bot from your phone. Ctrl+C stops.")
    offset = 0
    while True:
        try:
            updates = tg("getUpdates", {"offset": offset, "timeout": 60})
        except KeyboardInterrupt:
            raise
        except Exception as exc:
            print("(poll error, retrying: %s)" % exc)
            continue
        for u in updates:
            offset = u["update_id"] + 1
            msg = u.get("message") or {}
            chat = str(msg.get("chat", {}).get("id", ""))
            if not chat:
                continue
            if CHAT_ID and chat != CHAT_ID:
                continue  # someone else found your bot — ignore silently
            if not CHAT_ID:
                send(chat, "Your chat id is %s — put TELEGRAM_CHAT_ID=%s "
                     "in your .env and restart the bridge."
                     % (chat, chat))
                continue
            text = msg.get("text")
            if not text and msg.get("voice"):
                text = voice_to_text(msg["voice"]["file_id"])
                if text is None:
                    send(chat, "Voice notes need GROQ_API_KEY set. "
                         "Text works right now.")
                    continue
                send(chat, "Heard: %s" % text)
            if not text:
                continue
            print("-> " + text[:80])
            send(chat, ask_claude(text))


def main():
    if "--check" in sys.argv:
        check()
    elif "--send-stdin" in sys.argv:
        if not (TOKEN and CHAT_ID):
            sys.exit("--send-stdin needs TELEGRAM_BOT_TOKEN and "
                     "TELEGRAM_CHAT_ID set.")
        send(CHAT_ID, sys.stdin.read().strip())
    else:
        try:
            run_bridge()
        except KeyboardInterrupt:
            print("\nBridge stopped.")


if __name__ == "__main__":
    main()
