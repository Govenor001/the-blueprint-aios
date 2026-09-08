#!/usr/bin/env python3
"""Safely manage AIOS MCP registrations without writing credential values to JSON."""

from __future__ import annotations

import argparse
import json
import os
import re
import stat
from pathlib import Path
from typing import Any


PLACEHOLDER = re.compile(r"\$\{([A-Z][A-Z0-9_]*)\}")


def _settings_path(root: Path) -> Path:
    return Path(root).resolve() / ".claude" / "settings.json"


def _load(root: Path) -> dict[str, Any]:
    path = _settings_path(root)
    if not path.exists():
        return {"mcpServers": {}}
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("Claude settings must be a JSON object")
    servers = payload.setdefault("mcpServers", {})
    if not isinstance(servers, dict):
        raise ValueError("Claude mcpServers must be an object")
    return payload


def _write(root: Path, payload: dict[str, Any]) -> None:
    path = _settings_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    try:
        path.chmod(stat.S_IRUSR | stat.S_IWUSR)
    except OSError:
        pass


def _upsert(root: Path, name: str, server: dict[str, Any]) -> None:
    payload = _load(root)
    payload["mcpServers"][name] = server
    _write(root, payload)


def configure_blotato(root: Path) -> None:
    """Register Blotato with an env placeholder, never the actual API key."""
    _upsert(root, "blotato", {
        "type": "http",
        "url": "https://mcp.blotato.com/mcp",
        "headers": {"blotato-api-key": "${BLOTATO_API_KEY}"},
        "timeout": 600000,
        "tier": "A",
    })


def configure_openapi(
    root: Path,
    name: str,
    spec_url: str,
    base_url: str,
    api_key_var: str,
    whitelist: list[str],
    auth_type: str = "bearer",
) -> None:
    """Register the generic bridge with an explicit operation whitelist."""
    if not whitelist or len(whitelist) > 20:
        raise ValueError("an OpenAPI MCP registration needs 1-20 whitelisted operations")
    _upsert(root, name, {
        "command": "uvx",
        "args": ["mcp-openapi-proxy"],
        "env": {
            "OPENAPI_SPEC_URL": spec_url,
            "OPENAPI_BASE_URL": base_url,
            "API_KEY": f"${{{api_key_var}}}",
            "API_AUTH_TYPE": auth_type,
            "TOOL_WHITELIST": ",".join(whitelist),
        },
        "tier": "C",
    })


def _values(value: Any) -> list[str]:
    if isinstance(value, str):
        return PLACEHOLDER.findall(value)
    if isinstance(value, dict):
        return [name for item in value.values() for name in _values(item)]
    if isinstance(value, list):
        return [name for item in value for name in _values(item)]
    return []


def configured_servers(root: Path) -> list[dict[str, Any]]:
    """Report MCP readiness using names and counts only; never return values."""
    payload = _load(root)
    result = []
    for name, server in payload.get("mcpServers", {}).items():
        variables = sorted(set(_values(server)))
        missing = [variable for variable in variables if not os.environ.get(variable)]
        result.append({
            "name": name,
            "tier": server.get("tier", "unknown"),
            "status": "needs_setup" if missing else "connected",
            "missing": missing,
            "tools": len(server.get("tool_whitelist", [])) if isinstance(server.get("tool_whitelist"), list) else None,
        })
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("blotato")
    openapi = sub.add_parser("openapi")
    openapi.add_argument("name")
    openapi.add_argument("--spec-url", required=True)
    openapi.add_argument("--base-url", required=True)
    openapi.add_argument("--api-key-var", required=True)
    openapi.add_argument("--whitelist", nargs="+", required=True)
    openapi.add_argument("--auth-type", default="bearer")
    sub.add_parser("check")
    args = parser.parse_args(argv)
    if args.command == "blotato":
        configure_blotato(args.root)
    elif args.command == "openapi":
        configure_openapi(args.root, args.name, args.spec_url, args.base_url, args.api_key_var, args.whitelist, args.auth_type)
    else:
        print(json.dumps(configured_servers(args.root), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
