#!/usr/bin/env python3
"""
Creates a Composio MCP session for Claude Code integration.
Run this once to get your MCP URL and headers.
"""
import os
import sys

try:
    from composio import Composio
except ImportError:
    print("ERROR: composio package not installed.")
    print("Run: pip install composio-core")
    sys.exit(1)

# Get API key from environment or prompt
api_key = os.getenv('COMPOSIO_API_KEY')
if not api_key:
    api_key = input("Enter your Composio API key: ").strip()
    if not api_key:
        print("ERROR: No API key provided")
        sys.exit(1)

# Create session
try:
    composio = Composio(api_key=api_key)
    session = composio.create(user_id="claude_code_user")
    
    print("\n✓ Session created successfully!")
    print("\nAdd this to your .claude/settings.json under 'mcpServers':")
    print("\n{")
    print('  "composio": {')
    print('    "type": "http",')
    print(f'    "url": "{session.mcp.url}",')
    if hasattr(session.mcp, 'headers') and session.mcp.headers:
        print('    "headers": {')
        for key, val in session.mcp.headers.items():
            print(f'      "{key}": "{val}"')
        print('    }')
    print('  }')
    print("}")
    
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)
