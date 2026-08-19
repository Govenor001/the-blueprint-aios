# Day 5 — The Growth + Comms Wings

*Two wings today. Growth: your AIOS works your leads. Comms: it plugs into your entire Google Workspace in a few clicks. This is the day beginners historically quit on the connection step — so we made it three clicks instead of an afternoon. ~40 minutes.*

**By the end of Day 5:** your AIOS qualifies leads and drafts outreach, and it can read your Gmail, plan your day from your calendar, and reach your Drive/Sheets/Docs — all through one connection.

---

## Part A — The Growth Wing

### Step 1 — Install the growth skills

```
cp -r skill-vault/qualify skill-vault/outreach skill-vault/followup .claude/skills/
```

### Step 2 — Qualify a real lead list

Drop a list of prospects (a CSV or a paste — names, companies, whatever you have). No list yet? Use the practice set at `sample-data/leads.csv` — twelve fictional leads built for exactly this. Then:

> Use qualify to score these leads and tell me who to contact first and why.

It ranks them by fit (do they match your ideal customer?) and signal (is there a reason to reach out now?), so you work the best ones first.

### Step 3 — Draft outreach

> Use outreach to draft a personalized first message for my top 5 leads.

One tailored opener per lead, in your voice — review, tweak, send. Never a mass-merge; every message has a real, specific hook.

---

## Part B — The Comms Wing (your Google Workspace)

### Why Composio

Connecting an AI to Gmail the old way means a Google Cloud project, a consent screen, and OAuth plumbing — exactly where beginners give up. Composio does all of that for you. One connection covers Gmail, Calendar, Drive, Sheets, and Docs, and it stays connected.

### Step 4 — Connect your Google Workspace (the three-click part)

1. Sign in at **composio.dev** and open **dashboard.composio.dev**.
2. Copy your **API key** (Settings → Project Settings → API Keys — starts with `ak_`).
3. In **Toolkits**, connect **Gmail** and **Google Calendar**: click Connect → sign in with Google → approve → **land on the "connected" page.** (If it says "initializing," you didn't finish the consent — do it again to the success screen.)
4. Optionally connect **Drive, Sheets, Docs** the same way.

Now wire Claude Code to it — the exact walkthrough is **`references/composio-setup.md`** (copy `.mcp.json.example` to `.mcp.json`, paste your MCP server URL, restart Claude Code). Two minutes, and the proof is asking:

> List the subject lines of my 5 most recent emails.

### Step 5 — Install and run the Comms skills

```
cp -r skill-vault/inbox skill-vault/plan-day .claude/skills/
```

Then, the two moments that make this real:

> Triage my inbox.

It reads your recent mail and sorts it into *needs you now* / *can wait* / *ignore*, drafting replies for the urgent ones — so you make decisions instead of reading everything.

> Plan my day.

It reads your calendar and priorities and builds a realistic plan around them.

### Step 6 (optional) — Log leads to a Sheet

If you connected Google Sheets, close the loop between the wings:

> When I qualify leads, log them to my Google Sheet [link].

Now Growth and Comms work together — leads scored and recorded automatically.

---

## Adapt-to-you note

Your leads, your inbox, your calendar. A consultant uses this to triage client email and prep meetings; a store owner uses it to handle supplier mail and log wholesale leads. The wings are the same; the data is yours. Email and calendar are a *supporting* part of your AIOS here — the headline is that your whole system now reaches your real work.

## Done when

Your AIOS scores a real lead list, drafts real outreach, and successfully triages your actual inbox and plans your actual day.

## Proof of build

Post either the outreach campaign it drafted (redact names) **or** your AIOS's plan for your day. This is also the day it's worth learning to *sell*: the same Google-Workspace setup is something businesses pay consultants $1,500+ to build — see the "Sell This" bonus.

## Tomorrow

Day 6 — the big one. Your AIOS lands in your pocket: you'll text it (and talk to it) from your phone.
