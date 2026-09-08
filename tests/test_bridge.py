import json

from scripts import bridge


def test_send_splits_long_messages(monkeypatch):
    calls = []
    monkeypatch.setattr(bridge, "tg", lambda method, params=None, timeout=70: calls.append((method, params)) or {})
    bridge.send("123", "x" * 8000)
    assert len(calls) == 3
    assert all(call[0] == "sendMessage" for call in calls)
    assert all(len(call[1]["text"]) <= 3900 for call in calls)


def test_speak_falls_back_to_text_without_voice_credentials(monkeypatch):
    monkeypatch.delenv("ELEVEN_API_KEY", raising=False)
    monkeypatch.delenv("ELEVENLABS_API_KEY", raising=False)
    monkeypatch.delenv("ELEVEN_VOICE_ID", raising=False)
    assert bridge.speak("hello") is None


def test_send_voice_fails_closed_without_audio():
    assert bridge.send_voice("123", b"") is False


def test_transcribe_uses_groq_response(monkeypatch):
    bridge.GROQ_KEY = "test-key"

    class Response:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def read(self):
            return json.dumps({"text": "hello from voice"}).encode()

    monkeypatch.setattr(bridge.urllib.request, "urlopen", lambda request, timeout=60: Response())
    assert bridge.transcribe(b"audio") == "hello from voice"
