# Day 7 — Autopilot + Inspection

*The finish line. Today your AIOS starts working on a schedule — while you sleep — and you run the inspection, get your score, and graduate. ~35 minutes.*

**By the end of Day 7:** your AIOS works overnight on its own, you have your inspection score, and you're a certified Agent Architect.

---

## Why cadence is last

We saved automation for the end on purpose: **never put a job on a timer until it works when you run it by hand.** You've spent a week proving each wing works on demand. Now — and only now — we let them run without you.

## Step 1 — Schedule your morning brief

You'll use `cron`, the scheduler already on your Mac/Linux machine. One honest note first: a schedule only fires while this machine is awake — that's fine this week (pick a time your laptop is open; going 24/7 is the post-challenge module). And unattended jobs are the right place for an **API key** (`ANTHROPIC_API_KEY` in your `.env`) rather than your Pro login — Anthropic's consumer terms cover you at the keyboard, not scripts running alone, and a daily brief costs a few dollars a month on the API.

Run `crontab -e` and add (adjust the path to your kit folder):

```
SHELL=/bin/bash
0 7 * * * cd /path/to/the-blueprint-aios && set -a && . ./.env && set +a && python3 scripts/engine.py --quiet && claude -p "Run the brief skill on context/signals.json. Output plain text only." | python3 scripts/bridge.py --send-stdin
```

Tomorrow at 7am, a brief about your market lands on your phone with no action from you. (The `SHELL=/bin/bash` line matters — it's the #1 cron gotcha in `references/known-failures.md`.)

## Step 2 — Schedule your content

> Schedule my content to be drafted every morning and dropped into my Telegram (or scheduled via Blotato if I connected it).

Now your content is created daily on its own — you review and publish (free route) or it posts automatically (Blotato route).

## Step 3 — Schedule anything else that's ready

Whatever wings you've made solid — lead follow-up, a weekly newsletter — put them on their cadence too. The rule holds: only schedule what already works by hand.

## Step 4 — Confirm it fired on its own

Don't take it on faith. Set a test schedule two minutes out (`crontab -e`, change `0 7` to the coming minute), watch it fire, then set the real time. Seeing your AIOS do something while you did nothing is the proof that Floor 4 is real.

## Step 5 — Run the inspection

> Run /inspect.

Your AIOS scores itself out of 100 against The Blueprint's four floors — Foundation, Wiring, Workshops, Autopilot — and shows you exactly where you're strong and what to improve. This is your baseline. Re-run it weekly and watch the number climb; that climbing score is how you'll keep leveling up after the challenge.

## Step 6 — Graduate

Post your **inspection score** plus a **phone screenshot** in the community, then come to the **live graduation call** — certificates, the best builds of the cohort, and open Q&A (including "how would this work in my business?" — bring that one if you have a team). You'll get your **Agent Architect certificate** with your name, your AIOS's name, and your score — ready for LinkedIn.

---

## What you have now

Stop and take this in. In seven days you built an AI Operating System that:
- writes your content in your voice,
- watches your market overnight and briefs you,
- qualifies your leads and drafts your outreach,
- triages your inbox and plans your day,
- runs on a schedule while your laptop's open — with a clear path to full 24/7,
- and answers you by text or voice from your phone.

The only thing you pay for is Claude. Everything else is free. And it's *yours* — built on your business, your voice, your priorities.

## Adapt-to-you note

Your schedules match your life — maybe your brief comes at 6am before the gym, maybe content drafts at 9pm when you plan the next day. Set the cadence around how *you* work.

## Proof of build

Your `/inspect` scoreboard + a phone screenshot. Then claim your certificate.

## After the challenge

- **`/expand`** — your weekly ritual. Every Friday, find one more thing to automate and ship it. Your AIOS grows forever.
- **The "Sell This for $1,500" bonus** — set up this exact system for a client. One client pays for the challenge many times over.
- **The 30-day roadmap** — one new automation a week for the next month.

You're not done. You're operational. Welcome, Architect.
