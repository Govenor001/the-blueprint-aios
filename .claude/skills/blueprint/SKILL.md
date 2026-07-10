---
name: blueprint
description: Day-1 setup for a new AIOS. Use when someone says "set me up", "onboard me", "let's get started", "name my assistant", or has just cloned The Blueprint kit. Runs a 7-question interview, names the AIOS, and scaffolds the Foundation file set at the end. Idempotent — re-run any time after editing blueprint-intake.md.
---

## What this does

One combined wizard. Interviews the user (7 questions, hard cap), lets them **name their AIOS and give it a personality**, then writes the Foundation file set in a single batch. This is Floor 1 of The Blueprint.

**The wow moment:** at the end, tell them to ask *"[Name], what should I focus on this week?"* — and answer it using only the files you just wrote, in their voice. That one exchange is what makes it feel real.

## Execution

### Step 1 — Read the intake
Read `blueprint-intake.md`. If the answers are filled, skip to Step 3. If some are filled, ask which to keep. If it's a fresh clone, run Step 2.

### Step 2 — The interview (7 questions, hard cap)
Ask one at a time. Write each answer into `blueprint-intake.md` as you go so they can resume if interrupted.

1. **Who are you, what do you sell, who do you sell it to?** (identity, offer, ICP)
2. **Paste 1–2 things you've written recently — don't edit them.** This is the only hard rule: voice samples must be *pasted from real writing*, never typed fresh in the chat. If they start typing prose, stop them: *"Paste it raw from a real email or post — if you write it here while we talk, it's already shaped by our conversation. This is the one rule I can't bend."*
3. **Your 2–3 biggest priorities for the next 90 days?** Push back on "grow the business" — make them name a number, a deadline, or a deliverable.
4. **Where does revenue land and where is it tracked?** (Stripe, Skool, a spreadsheet…)
5. **Where do you talk to customers and your team day to day?** (Gmail/Outlook, Slack, DMs, phone)
6. **Where do your notes, docs, and recordings live?** (Drive, Notion, Dropbox, a messy desktop folder)
7. **What one task eats your week, and where do you track work?** (capture the top pain + the task tool)

Then, before scaffolding: **"What do you want to name your AIOS, and what's its personality — dry and efficient, warm and chatty, or something else?"** Capture both.

### Step 3 — Scaffold the Foundation
Write (or update, backing up originals to `archives/`) these files:
1. `context/about-me.md` — from Q1 + Q7
2. `context/about-business.md` — from Q1 + Q4
3. `context/priorities.md` — from Q3, numbered
4. `references/voice.md` — the Q2 samples verbatim, with a one-line header
5. `connections.md` — one row per system named in Q4–Q7, each `not yet wired`
6. `CLAUDE.md` — fill every `{{...}}`, including the AIOS name and personality

### Step 4 — The closing screen (three lines)
```
✓ Foundation poured. [Name] knows who you are, what you sell, what matters this quarter, and how you sound.

Today:  ask [Name] — "what should I focus on this week?"
Tomorrow: wire one tool from connections.md (Floor 2).
Day 7:  run /inspect to see your score.
```

When they ask the closing prompt, answer in their voice, in three bullets, each tied to a Q3 priority, ending with: *"If I had to pick one thing for Monday, it'd be [X] because [reason]. Want me to draft it? And — where could I take part of this off your hands?"*

## Rules
1. **7 questions, no Q8 in conversation.**
2. **Voice must be pasted, never typed fresh.** Refuse otherwise.
3. **One-shot scaffold** — write Step 3 in one batch, no per-file confirmation.
4. **Idempotent** — re-running with an edited intake refreshes files and backs up originals.
5. **Name + personality are mandatory** — they create ownership. Don't skip.
6. **No API keys on Day 1.** Wiring is Floor 2, tomorrow.
