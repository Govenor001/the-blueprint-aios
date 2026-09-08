from scripts.local_model import classify, embed


def test_local_model_is_optional(monkeypatch):
    monkeypatch.delenv("AIOS_LOCAL_MODEL_URL", raising=False)
    assert embed(["hello"]) is None
    assert classify("hello", ["greeting"]) is None
