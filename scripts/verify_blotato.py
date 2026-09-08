#!/usr/bin/env python3
"""Verify Blotato with one read-only MCP account listing."""

from __future__ import annotations

import argparse
import json
import os
import stat
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ENDPOINT = "https://mcp.blotato.com/mcp"


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _api_key(root: Path) -> str:
    if os.environ.get("BLOTATO_API_KEY"):
        return os.environ["BLOTATO_API_KEY"]
    for path in (Path(root).resolve() / ".env", Path(root).resolve().parent / ".env"):
        try:
            for line in path.read_text(encoding="utf-8").splitlines():
                key, separator, value = line.partition("=")
                if separator and key.strip() == "BLOTATO_API_KEY":
                    return value.strip().strip("'\"")
        except OSError:
            continue
    return ""


def _json_response(body: str) -> dict[str, Any]:
    for line in body.splitlines():
        line = line[5:].strip() if line.startswith("data:") else line.strip()
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict) and ("result" in payload or "error" in payload):
            return payload
    raise ValueError("Blotato returned no JSON-RPC response")


def verify_blotato(root: Path) -> dict[str, Any]:
    root = Path(root).resolve()
    stamp = _now()
    key = _api_key(root)
    if not key:
        result = {"status": "unavailable", "source": "Blotato MCP", "retrieved_at": stamp, "accounts": [], "error": "BLOTATO_API_KEY is not configured"}
    else:
        request = urllib.request.Request(
            ENDPOINT,
            data=json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "blotato_list_accounts", "arguments": {}}}).encode(),
            headers={"blotato-api-key": key, "Content-Type": "application/json", "Accept": "application/json, text/event-stream"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                payload = _json_response(response.read().decode("utf-8", errors="replace"))
            if "error" in payload:
                raise RuntimeError(str(payload["error"].get("message", "MCP request failed")))
            content = payload.get("result", {}).get("content", [])
            text = "".join(item.get("text", "") for item in content if item.get("type") == "text")
            data = json.loads(text)
            raw_accounts = data.get("accounts", data) if isinstance(data, dict) else data
            accounts = []
            for account in raw_accounts if isinstance(raw_accounts, list) else []:
                if isinstance(account, dict):
                    accounts.append({"platform": str(account.get("platform", "unknown")), "name": str(account.get("username") or account.get("fullname") or "unnamed")})
            result = {"status": "available", "source": "Blotato MCP", "retrieved_at": stamp, "accounts": accounts}
        except (OSError, ValueError, RuntimeError, urllib.error.URLError) as exc:
            result = {"status": "error", "source": "Blotato MCP", "retrieved_at": stamp, "accounts": [], "error": str(exc)[:240]}
    output = root / "var" / "connections" / "blotato.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    try:
        output.chmod(stat.S_IRUSR | stat.S_IWUSR)
    except OSError:
        pass
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    print(json.dumps(verify_blotato(args.root), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
