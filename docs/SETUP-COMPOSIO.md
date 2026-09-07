# Connect Composio

This is the Day 5 connector step. The student supplies a Composio API key locally; the key is never written to the repository.

1. Install the Python dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

2. Set `COMPOSIO_API_KEY` in the local environment, or let the helper prompt for it:

   ```powershell
   python scripts/create_composio_session.py
   ```

3. Copy the printed `composio` object into `.claude/settings.json` under `mcpServers`.

4. Restart Claude Code and verify the connector from the dashboard's Connections panel.

The helper uses Composio's current Python package and requests an MCP-backed session. Never commit `.claude/settings.json`, `.mcp.json`, or any API key.
