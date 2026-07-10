---
name: inspect
description: Score this AIOS against The Blueprint's four floors. Use when someone asks "inspect my setup", "score my AIOS", "is my AIOS actually working", or "find my gaps". Read-only. Produces a 0-100 scoreboard, the top-3 gaps ranked by leverage, and one recommended next move. Run Day 7, then weekly.
---

## What this does

Runs a **building inspection** on the current Claude Code project. Reads — never writes — the operating manual, memory, skills, connections, decisions, and schedules. Scores each of the four floors out of 25 (100 total), names the strengths, and ranks the top 3 gaps by leverage. First run is your baseline; re-run weekly to watch the number climb. That climbing number is the hook.

Scope is structural: *"is it built right?"* — not *"what could it do?"* (that's `/expand`).

## Step 1 — Walk the building
Look for intent, not exact filenames. Use Glob and Read.
- **Foundation:** `CLAUDE.md`, `context/`, `references/voice.md`, memory files, `decisions/log.md`
- **Wiring:** `.mcp.json` / `settings.json` MCP servers, `scripts/*` hitting APIs, `.env` keys with a matching `references/{tool}.md`, `connections.md`
- **Workshops:** `.claude/skills/*/SKILL.md` (count + which are user-built)
- **Autopilot:** cron entries, `.claude/settings.json` hooks, skills named `daily-*`/`weekly-*`/`morning-*`, a deployed server, a phone bridge

## Step 2 — Score each floor (25 each)

**Foundation (25)** — operating manual is substantive (5) · identity + voice captured (5) · persistent memory with real entries (5) · reference docs exist (5) · decisions logged (5)

**Wiring (25)** — count reachable data domains across Revenue, Customers, Calendar, Comms, Tasks, Notes, News; ~4 pts each up to 15 · a saved API guide per wired tool (5) · at least one connection can *write*, not just read (5)

**Workshops (25)** — 4+ skills installed (10) · at least one you built yourself, beyond the four core skills (10) · a sub-agent or multi-step job defined (5)

**Autopilot (25)** — at least one scheduled trigger (10) · recent activity in the last 30 days (10) · deployed off your laptop / reachable by phone (5)

## Step 3 — Rank the top 3 gaps by leverage
Leverage = points lost × impact. Weight heavily: 0 data domains wired (×4), thin/missing Foundation (×3), ≤2 domains wired (×3), 0 user-built skills (×2), no schedule (×2), everything read-only (×2). Sort, take the top 3, give each a concrete one-line next step.

## Step 4 — Print the report
```
# AIOS Inspection — {date}
Score: {total}/100  ({stage})

Foundation   {bar} {n}/25  {label}
Wiring       {bar} {n}/25  {label}
Workshops    {bar} {n}/25  {label}
Autopilot    {bar} {n}/25  {label}

Stages: 0-39 Blueprint · 40-69 Framed · 70-89 Wired · 90-100 Live
(bar = one block per 5 pts; label = Strong ≥20 / Solid 15-19 / Thin 8-14 / Missing <8)

Strengths
- {1-3 bullets}

Top 3 gaps (by leverage)
1. {gap} → {next step}
2. {gap} → {next step}
3. {gap} → {next step}

Next: {single highest-leverage move}
```
Then offer: *"Save this to `inspections/{date}.md` so you can track your score over time?"* — the only thing this skill may write.

## Rules
- **Read-only** except the optional saved report.
- **Be honest, not generous.** Most real setups land 40–70. A 95 is a genuine flex.
- **Fast** — under 60 seconds. Read targeted files; count skill folders by frontmatter, don't read each in full.
- **Don't recommend skills that don't exist.** Point at what's actually installed or in the Vault.
