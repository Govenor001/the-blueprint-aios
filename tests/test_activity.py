import json

from scripts.activity import log, redact


def test_redacts_secrets_and_emails(tmp_path, monkeypatch):
    monkeypatch.setenv("AIOS_ROOT", str(tmp_path))
    message = "ak_secret sent to owner@example.com"
    assert "[redacted]" in redact(message)
    log("test", detail=message)
    row = json.loads((tmp_path / "var" / "activity.jsonl").read_text().splitlines()[0])
    assert "ak_secret" not in row["detail"]
    assert "owner@example.com" not in row["detail"]

def test_rotates_large_activity_file(tmp_path, monkeypatch):
    monkeypatch.setenv("AIOS_ROOT", str(tmp_path))
    path = tmp_path / "var" / "activity.jsonl"
    path.parent.mkdir(parents=True)
    path.write_text("x" * (10 * 1024 * 1024 + 1), encoding="utf-8")
    log("rotate")
    assert (tmp_path / "var" / "activity.jsonl.1").exists()
