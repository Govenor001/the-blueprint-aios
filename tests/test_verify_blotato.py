import json

from scripts.verify_blotato import verify_blotato


def test_verify_blotato_missing_key_is_explicit(tmp_path, monkeypatch):
    monkeypatch.delenv("BLOTATO_API_KEY", raising=False)
    result = verify_blotato(tmp_path)
    assert result["status"] == "unavailable"
    assert result["accounts"] == []


def test_verify_blotato_keeps_only_account_names(tmp_path, monkeypatch):
    monkeypatch.setenv("BLOTATO_API_KEY", "secret")

    class Response:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def read(self):
            return json.dumps({"jsonrpc": "2.0", "id": 1, "result": {"content": [{"type": "text", "text": json.dumps({"accounts": [{"id": "secret-id", "platform": "instagram", "username": "owner"}]})}]}}).encode()

    monkeypatch.setattr("scripts.verify_blotato.urllib.request.urlopen", lambda request, timeout: Response())
    result = verify_blotato(tmp_path)
    assert result["status"] == "available"
    assert result["accounts"] == [{"platform": "instagram", "name": "owner"}]
    assert "secret-id" not in json.dumps(result)
