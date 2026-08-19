# Wiring Claude Code to Composio (the Comms Wing connection)

Composio holds your Google sign-in; Claude Code reaches it over MCP.
Ten minutes, once.

## 1 — Connect your Google apps in Composio
1. Sign up / sign in at composio.dev and open the dashboard.
2. Connect **Gmail** and **Google Calendar**: click Connect, complete the
   Google sign-in, approve, and **land on the "connected" page**. If it
   says "initializing", you didn't finish — redo it to the success screen.
3. Optional: Drive, Sheets, Docs the same way.

## 2 — Get your MCP server URL
Composio's current docs recommend its native agent plugin for Claude Code
unless you explicitly want MCP. For the MCP route, use **Composio Connect**
or create a Composio session with MCP enabled, scoped to the apps and tools
you connected, then copy the hosted MCP endpoint URL and any required
headers. The current path is documented at docs.composio.dev/docs/sessions-via-mcp.

## 3 — Point Claude Code at it
1. Copy `.mcp.json.example` (repo root) to `.mcp.json`.
2. Replace the placeholder with your URL. If Composio gives you headers,
   add them using the current Claude Code MCP configuration format.
3. If the URL or headers contain a key or secret, add `.mcp.json` to
   `.gitignore` before anything else.
4. Restart Claude Code in this folder and approve the new MCP server
   when it asks.

## 4 — Prove it works
Ask your AIOS:

> List the subject lines of my 5 most recent emails.

Real subjects come back — you're wired. Add a `composio` row per app in
`connections.md`.

## Honest notes
- **Cost:** free tier (2026-08-15 pricing) is 100,000 tool calls/month,
  20,000 of them through Composio's shared Google app. A personal setup
  uses a fraction of that. Some premium tools bill separately from
  2026-09-01.
- **Privacy:** you're giving a third party OAuth access to your Google
  account. Connect only the apps you'll use; revoke any time at
  myaccount.google.com → Security → Third-party access.
