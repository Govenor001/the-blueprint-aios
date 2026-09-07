#!/usr/bin/env python3
"""Create a Composio MCP session without exposing credentials in the repository."""

from __future__ import annotations

import json
import os
import sys

try:
    from composio import Composio
except ImportError:
    print("ERROR: composio package is not installed.")
    print("Run: pip install -r requirements.txt")
    raise SystemExit(1)

api_key = os.getenv("COMPOSIO_API_KEY")
if not api_key:
    api_key = input("Enter your Composio API key: ").strip()
if not api_key:
    print("ERROR: No API key provided")
    raise SystemExit(1)

try:
    composio = Composio(api_key=api_key)
    session = composio.create(user_id="claude_code_user", mcp=True)
    mcp = getattr(session, "mcp", None)
    if mcp is None or not getattr(mcp, "url", None):
        raise RuntimeError("Composio did not return an MCP session URL")
    server = {"type": "http", "url": mcp.url}
    headers = getattr(mcp, "headers", None)
    if headers:
        server["headers"] = dict(headers)
    print("\nSession created. Add this object under mcpServers in .claude/settings.json:")
    print(json.dumps({"composio": server}, indent=2))
except Exception as exc:
    print(f"ERROR: {exc}")
    raise SystemExit(1)
