# Day 0 — Prepare the Site

*Before we build, we gather materials — but only the materials we need tomorrow. Two required signups, two installs, ~25 minutes. Every other account in the services guide gets created on the day it's used, when you can see why you're signing up.*

**By the end of Day 0 you'll have:** Claude Code replying in your terminal, a Telegram bot waiting for Day 6, and a safe home for your keys.

---

## Step 1 — Claude + Claude Code (the one that matters)

Follow section 1 of [00-SERVICES-AND-SETUP.md](../00-SERVICES-AND-SETUP.md): subscribe to Claude Pro ($20/mo — the one real cost), install Claude Code, run `claude` in your terminal, confirm it replies. **Don't move on until it does.**

## Step 2 — Telegram bot (2 minutes now saves fumbling on Day 6)

Install Telegram on your phone. Message **@BotFather**, send `/newbot`, follow the prompts (the username must end in `bot`), and copy the **bot token** it gives you.

## Step 3 — A safe home for your keys

In the kit folder, copy `.env.example` to a file called `.env` and paste your bot token into `TELEGRAM_BOT_TOKEN=`. That file is your key vault for the whole build — it's already git-ignored, and every script in the kit reads from it. (A password manager for backups is even better. A loose `keys.txt` on your desktop is not.)

## Step 4 — Git + Node.js

Install **Git** (git-scm.com) and **Node.js LTS** (nodejs.org). Quick test — all three print a version:

```
claude --version
git --version
node --version
```

## What about all the other services?

They come later, on purpose: Groq on Day 3 (2 minutes), Resend as Day 2 homework, Composio on Day 5, and the rest only if you want them. The full setup guide for each lives in [00-SERVICES-AND-SETUP.md](../00-SERVICES-AND-SETUP.md) — you'll be pointed at the right section on the right day.

---

## Adapt-to-you note

Some services map to *your* business, not ours. When a guide says "your niche," "your domain," "your social accounts" — use yours. The *mechanism* is identical; the *content* is yours.

## Done when

`claude` replies in your terminal, your `.env` exists with the bot token in it, and Git + Node answer with versions.

## Proof of build

Post in the community: a screenshot of **Claude Code replying in your terminal**, and a one-line "Day 0 done — tools ready." Read a few others' while you're there.

## Tomorrow

Day 1 — you run one command, name your AIOS, and it learns your business well enough to tell *you* what to focus on this week.
