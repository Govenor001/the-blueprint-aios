#!/usr/bin/env python3
"""Collect panel cards without making the dashboard call external APIs."""

from __future__ import annotations

import argparse
import json
import re
import os
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


def _env_name(value: str) -> str:
    return re.sub(r"[^A-Z0-9]+", "_", value.upper()).strip("_")


def _read_connection(source: dict[str, Any]) -> tuple[str, Any, str | None]:
    """Read one explicitly configured read-only endpoint.

    Connectors are deliberately endpoint-driven: the student supplies the
    endpoint produced by Composio or an OpenAPI bridge in .env. The collector
    never guesses an API, follows redirects, or sends a write request.
    """
    connection = str(source.get("connection", "connection"))
    operation = str(source.get("operation", "read"))
    endpoint_env = str(source.get("endpoint_env") or f"AIOS_{_env_name(connection)}_{_env_name(operation)}_URL")
    endpoint = os.environ.get(endpoint_env)
    if not endpoint:
        return "unavailable", None, "connection not configured"
    if not endpoint.startswith("https://") and not endpoint.startswith("http://127.0.0.1") and not endpoint.startswith("http://localhost"):
        return "error", None, "endpoint must use HTTPS or local HTTP"
    token_env = source.get("token_env")
    token = os.environ.get(str(token_env)) if token_env else None
    if token_env and not token:
        return "unavailable", None, "credential not configured"
    headers = {"Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(endpoint, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            raw = response.read(256 * 1024)
        try:
            value: Any = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            value = raw.decode("utf-8", errors="replace")
        field = source.get("field") or source.get("value_path")
        if field and isinstance(value, dict):
            for part in str(field).split("."):
                if not isinstance(value, dict) or part not in value:
                    return "error", None, f"response field not found: {field}"
                value = value[part]
        return "available", value, None
    except urllib.error.HTTPError as exc:
        return "error", None, f"HTTP {exc.code}"
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return "error", None, str(exc.reason if isinstance(exc, urllib.error.URLError) else exc)[:240]


def _card_id(panel: str, card: dict[str, Any]) -> str:
    value = card.get("id") or f"{panel}-{card.get('title', 'card')}"
    return re.sub(r"[^a-z0-9-]+", "-", str(value).lower()).strip("-")


def collect(root: Path) -> int:
    root = Path(root).resolve()
    panels = root / "config" / "panels"
    metric_dir = root / "var" / "metrics"
    metric_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for path in sorted(panels.glob("*.yaml")):
        payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        for card in payload.get("cards", []):
            card_id = _card_id(path.stem, card)
            now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
            source = card.get("source", {})
            row: dict[str, Any] = {"retrieved_at": now, "card_id": card_id, "source": source, "status": "unavailable"}
            if isinstance(source, dict) and "local" in source:
                local = root / str(source["local"])
                row["source_label"] = f"local: {source['local']}"
                row["status"] = "available" if local.exists() else "unavailable"
                row["value"] = len(list(local.glob("*"))) if local.exists() else None
            elif isinstance(source, dict) and source.get("connection"):
                operation = source.get("operation", "read")
                row["source_label"] = f"{source['connection']}: {operation}"
                status, value, error = _read_connection(source)
                row["status"] = status
                row["value"] = value
                if error:
                    row["error"] = error
            else:
                row["source_label"] = "UNAVAILABLE"
                row["error"] = "connection not configured"
            with (metric_dir / f"{card_id}.jsonl").open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            count += 1
    return count


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    print(collect(args.root))
