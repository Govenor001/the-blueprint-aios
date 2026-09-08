import json

from scripts.model_for import model_for


def test_model_for_reads_skill_tier_and_route(tmp_path, monkeypatch):
    (tmp_path / "config").mkdir()
    (tmp_path / "dashboard" / "static").mkdir(parents=True)
    (tmp_path / "config" / "models.yaml").write_text(
        "route: bedrock\ntiers:\n  bedrock:\n    fast: fast-id\n    smart: smart-id\n    deep: deep-id\n",
        encoding="utf-8",
    )
    (tmp_path / "dashboard" / "static" / "map.json").write_text(
        json.dumps({"wings": [{"departments": [{"functions": [{"agents": [{"name": "inbox", "model": "fast"}]}]}]}]}),
        encoding="utf-8",
    )
    assert model_for(tmp_path, skill="inbox") == "fast-id"


def test_model_for_allows_server_route_override(tmp_path, monkeypatch):
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "models.yaml").write_text(
        "route: claude-subscription\ntiers:\n  claude-subscription:\n    smart: subscription-id\n  bedrock:\n    smart: bedrock-id\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("AIOS_MODEL_ROUTE", "bedrock")
    assert model_for(tmp_path, tier="smart") == "bedrock-id"
