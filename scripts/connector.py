#!/usr/bin/env python3
"""Small, read-only connector boundary used by collectors and setup helpers."""

from __future__ import annotations

import json
import os
import re
import stat
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping


@dataclass(frozen=True)
class ConnectorResult:
    value: Any
    source: str
    collected_at: str
    status: str
    error: str | None = None


def _stamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _slug(value: str) -> str:
    return re.sub(r"[^A-Z0-9]+", "_", value.upper()).strip("_")


class ReadOnlyHttpConnector:
    def __init__(self, name: str, endpoint: str | None, token: str | None = None):
        self.name = name
        self.endpoint = endpoint
        self.token = token

    def read(self, operation: str = "read", field: str | None = None) -> ConnectorResult:
        source = f"{self.name}: {operation}"
        if not self.endpoint:
            return ConnectorResult(None, source, _stamp(), "unavailable", "connection not configured")
        if not (self.endpoint.startswith("https://") or self.endpoint.startswith("http://127.0.0.1") or self.endpoint.startswith("http://localhost")):
            return ConnectorResult(None, source, _stamp(), "error", "endpoint must use HTTPS or local HTTP")
        headers = {"Accept": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        try:
            with urllib.request.urlopen(urllib.request.Request(self.endpoint, headers=headers, method="GET"), timeout=10) as response:
                raw = response.read(256 * 1024)
            try:
                value: Any = json.loads(raw.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                value = raw.decode("utf-8", errors="replace")
            if field:
                for part in field.split("."):
                    if not isinstance(value, dict) or part not in value:
                        return ConnectorResult(None, source, _stamp(), "error", f"response field not found: {field}")
                    value = value[part]
            return ConnectorResult(value, source, _stamp(), "available")
        except urllib.error.HTTPError as exc:
            return ConnectorResult(None, source, _stamp(), "error", f"HTTP {exc.code}")
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            detail = exc.reason if isinstance(exc, urllib.error.URLError) else exc
            return ConnectorResult(None, source, _stamp(), "error", str(detail)[:240])


def load_connector(name: str, environ: Mapping[str, str] | None = None) -> ReadOnlyHttpConnector:
    env = environ if environ is not None else os.environ
    prefix = f"AIOS_{_slug(name)}"
    endpoint = env.get(f"{prefix}_BASE_URL") or env.get(f"{prefix}_URL")
    token_name = env.get(f"{prefix}_TOKEN_ENV")
    token = env.get(token_name) if token_name else env.get(f"{prefix}_API_KEY")
    return ReadOnlyHttpConnector(name, endpoint, token)


def write_mcp_config(url: str, headers: Mapping[str, str], path: Path) -> None:
    """Write an untracked MCP config with caller-provided variable placeholders."""
    if not url.startswith(("https://", "http://127.0.0.1", "http://localhost")):
        raise ValueError("MCP URL must use HTTPS or local HTTP")
    payload = {"mcpServers": {"aios-connector": {"url": url, "headers": dict(headers)}}}
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    path.chmod(stat.S_IRUSR | stat.S_IWUSR)
