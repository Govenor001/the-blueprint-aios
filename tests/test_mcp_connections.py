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


def test_configured_servers_reads_private_env_file_names_only(tmp_path, monkeypatch):
    monkeypatch.delenv("BLOTATO_API_KEY", raising=False)
    (tmp_path / ".env").write_text("BLOTATO_API_KEY=private-value\n", encoding="utf-8")
    configure_blotato(tmp_path)
    row = configured_servers(tmp_path)[0]
    assert row["status"] == "connected"
    assert "private-value" not in json.dumps(row)
