# Wiring Claude Code to Composio (the Comms Wing connection)

Composio holds your Google sign-in; Claude Code reaches it over MCP.
Ten minutes, once.

## 1 — Connect your Google apps in Composio
1. Sign up / sign in at composio.dev and open the dashboard (redirects to app.composio.dev).
2. Go to **Settings** → **API Keys** and copy your API key (starts with `ak_`). Save this.
3. In the main dashboard, find **Connected Accounts** or **Integrations**.
4. Connect **Gmail** and **Google Calendar**: click Connect, complete the
   Google sign-in, approve all permissions, and **land on the "connected" page**. If it
   says "initializing", you didn't finish — redo it to the success screen.
5. Optional: Drive, Sheets, Docs the same way.

## 2 — Create an MCP session

Composio uses sessions to create MCP endpoints. The repo includes a helper script:

```bash
# Install Composio if you don't have it
pip install composio-core

# Run the session creation script
python3 scripts/create_composio_session.py
```

When prompted, paste your API key from Step 1. The script outputs JSON configuration with your MCP URL and headers.

## 3 — Configure Claude Code

1. Open (or create) `.claude/settings.json` in your project root.
2. Add the JSON from Step 2 under `"mcpServers"`:

```json
{
  "mcpServers": {
    "composio": {
      "type": "http",
      "url": "YOUR_SESSION_URL_FROM_SCRIPT",
      "headers": {
        "Authorization": "Bearer YOUR_TOKEN_FROM_SCRIPT"
      }
    }
  }
}
```

3. **Important:** If your `settings.json` already has other content, just add the `"mcpServers"` section without overwriting existing settings.
4. Save the file.

## 4 — Restart and approve

1. Quit Claude Code completely and reopen it in this project folder.
2. When it starts, it will ask to approve the new Composio MCP server. Approve it.

## 5 — Prove it works

Ask your AIOS:
> List the subject lines of my 5 most recent emails.

If you see actual subjects from your inbox, you're connected.

## Troubleshooting

**"composio-core not found"**: Run `pip install composio-core`

**"Invalid API key"**: Double-check you copied the full key from Settings → API Keys in Composio dashboard

**"No emails returned"**: Make sure Gmail is shown as "Connected" (not "Initializing") in your Composio dashboard

**Claude Code doesn't prompt for MCP approval**: Make sure you fully quit and reopened Claude Code after editing settings.json

## Honest notes
- **Cost:** free tier (2026-08-15 pricing) is 100,000 tool calls/month,
  20,000 of them through Composio's shared Google app. A personal setup
  uses a fraction of that. Some premium tools bill separately from
  2026-09-01.
- **Privacy:** you're giving a third party OAuth access to your Google
  account. Connect only the apps you'll use; revoke any time at
  myaccount.google.com → Security → Third-party access.
