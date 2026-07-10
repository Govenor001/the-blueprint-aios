# Day 0 — Prepare the Site

*Before we build, we gather materials. A builder doesn't start pouring concrete before the tools are on-site. Day 0 gets every account and tool ready so Days 1–7 never stall. Budget 45–60 minutes. You won't build anything today — you're clearing the runway.*

**By the end of Day 0 you'll have:** every account created, every key saved, and Claude Code replying in your terminal.

---

## Step 1 — Read the parts list

Open `curriculum/00-SERVICES-AND-SETUP.md`. That's your complete list of services with a setup guide for each. Keep it open beside you today. The honest cost summary: **you pay for Claude (~$20/mo); a cloud server is free on Oracle; everything else is free.**

## Step 2 — Create a place to keep your keys

You'll collect ~8 API keys today. Losing them mid-build is the #1 momentum-killer. Use a password manager, or make one file called `my-keys.txt` in a safe place and label each key clearly:

```
CLAUDE:        (Pro subscription — no key if using Pro)
GROQ:          gsk_...
COMPOSIO:      ak_...
TELEGRAM_BOT:  ...
TELEGRAM_CHAT: ...
RESEND:        re_...
ELEVENLABS:    ...
GITHUB_TOKEN:  ...
SERVER_IP:     ...
```

## Step 3 — Work down the Day-0 checklist

Do these in this order (full steps for each are in the services guide):

1. **⭐ Claude + Claude Code** — subscribe to Claude Pro, install Claude Code, run `claude`, confirm it replies. *This is the one that matters most — don't move on until it works.*
2. **⭐ Cloud server** — create your Oracle Always-Free Ubuntu instance, save the SSH key, note the IP.
3. **⭐ Groq** — sign up, create an API key, save it.
4. **Composio** — sign up, save the API key; if you have 5 minutes, connect Gmail now.
5. **Telegram** — install it, create your bot via @BotFather, save the token.
6. **Resend** — sign up, save the key, add your domain (verification can finish overnight).
7. **GitHub + Git + Node.js** — accounts and installs.
8. **ElevenLabs** — optional, save the key if you want spoken replies.
9. **Social publishing** — decide: Blotato (paid) or the free "AIOS drafts to my Telegram, I tap post" route.

## Step 4 — Install the three tools on your computer

You need these three installed locally (the server pieces come Day 6):
- **Claude Code** (from Step 1)
- **Git** — git-scm.com
- **Node.js** (LTS) — nodejs.org

Quick test in your terminal — all three should print a version:
```
claude --version
git --version
node --version
```

---

## Adapt-to-you note

Some services map to *your* business, not ours. When the guide says "your niche," "your domain," "your social accounts" — use yours. You're building this for your world, not copying ours. The *mechanism* is identical; the *content* is yours.

## Done when

Every box on the Day-0 checklist (bottom of the services guide) is ticked, and `claude` replies in your terminal.

## Proof of build

Post in the community: a screenshot of **Claude Code replying in your terminal**, and a one-line "Day 0 done — tools ready." That's your first check-in. Read a few others' while you're there.

## Tomorrow

Day 1 — you clone your AIOS, run one command, name it, and it learns your business well enough to tell *you* what to focus on this week.
