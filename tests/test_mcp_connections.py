import json

from scripts.mcp_connections import configure_blotato, configured_servers


def test_configure_blotato_uses_environment_placeholder_and_never_key(tmp_path, monkeypatch):
    monkeypatch.setenv("BLOTATO_API_KEY", "secret-value")

    configure_blotato(tmp_path)

    settings = json.loads((tmp_path / ".claude" / "settings.json").read_text(encoding="utf-8"))
    blotato = settings["mcpServers"]["blotato"]
    assert blotato["url"] == "https://mcp.blotato.com/mcp"
    assert blotato["headers"]["blotato-api-key"] == "${BLOTATO_API_KEY}"
    assert "secret-value" not in json.dumps(settings)
    assert configured_servers(tmp_path)[0]["status"] == "connected"
