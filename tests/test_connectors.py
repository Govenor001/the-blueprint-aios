import json
import os
from pathlib import Path

from scripts.connector import ConnectorResult, load_connector, write_mcp_config


def test_missing_connector_is_explicitly_unavailable():
    result = load_connector("gmail", {}).read("unread_count")
    assert isinstance(result, ConnectorResult)
    assert result.status == "unavailable"
    assert result.value is None


def test_mcp_config_preserves_multiple_headers_and_private_mode(tmp_path: Path):
    path = tmp_path / ".mcp.json"
    write_mcp_config("https://example.test/mcp", {"Authorization": "${TOKEN}", "X-Tenant": "${TENANT}"}, path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["mcpServers"]["aios-connector"]["headers"]["X-Tenant"] == "${TENANT}"
    if os.name != "nt":
        assert path.stat().st_mode & 0o777 == 0o600
