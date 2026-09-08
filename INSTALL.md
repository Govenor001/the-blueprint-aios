# Install — a finished platform on your server

Students do not build the platform. The installer creates the dashboard, map,
agent library, vault, bridge, schedules, diagrams, and safety controls. The
seven-day challenge is for connecting services, adding business context, and
verifying the result.

## 1. Prepare the server

Use a fresh Ubuntu 24.04 VPS. Set a strong dashboard password and, if you have
a domain pointed at the server, set `AIOS_DOMAIN` so Caddy provisions HTTPS.

```bash
export DASHBOARD_PASSWORD='choose-a-long-password'
export AIOS_DOMAIN='aios.example.com'       # optional
curl -fsSL https://raw.githubusercontent.com/Govenor001/the-blueprint-aios/main/deploy/install.sh -o /tmp/aios-install.sh
sudo -E bash /tmp/aios-install.sh
```

Without a domain, the dashboard stays private on `127.0.0.1:8787`; use an SSH
tunnel. Schedules are installed but remain disabled until the owner approves
them on Day 7.

## 2. Authenticate Claude

On the server, run:

```bash
sudo -u aios claude setup-token
sudo -u aios claude -p 'say ok'
```

Approve the link on your phone and paste the code back. Do not create an
`ANTHROPIC_API_KEY`; this platform uses Claude subscription authentication or
the configured Bedrock route.

## 3. Open Mission Control

The dashboard is already populated with the full map and panels. Start with
[Day 0](curriculum/days/day-0.md), then follow [Days 1–7](curriculum/README.md).
You only add your context, connect your accounts, choose approval boundaries,
and verify each result.

## If something is not connected

Mission Control says `UNAVAILABLE` or `needs setup` rather than inventing a
number. Follow the relevant setup page, run the check again, and inspect the
activity feed. Credentials belong in `/opt/aios/.env`, never in Git or the
dashboard.
