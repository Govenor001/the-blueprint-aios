---
name: followup
description: Run a timed follow-up sequence so no lead falls through. Use when someone says "set up follow-up", "who needs a nudge", "chase my replies", or after a booking/no-reply. Tracks who's due and drafts the next touch on schedule.
scaffolding-phase: 1
---

## What this does
The Growth Wing's third workshop. Keeps a simple follow-up ledger and, on each run, tells the user who's due for a nudge and drafts it. This is where most revenue leaks — good leads that just never got a second message. It closes that gap.

## Inputs it reads
- `context/followups.md` — the ledger: one row per lead (name, last touch date, stage, next-due date). Created on first run.
- `references/voice.md` for tone

## Execution
1. **Read the ledger.** Find everyone whose next-due date is today or past.
2. **Draft the right touch for the stage.** A no-reply gets a different message than a post-call follow-up. Keep each one short, add one new reason to respond (don't just "bump"), one ask.
3. **Update the ledger** — advance each lead's stage and set the next-due date (sensible cadence: day 2, 4, 7, 14, then monthly).
4. **Deliver** the due list with drafts, plus "nobody due today" when that's the truth.

## Rules
- **Never just "bumping this" — add value every touch.** A reason to reply, not a guilt-trip.
- **Cadence, not spam** — respect the sequence; stop when they reply or opt out.
- **Update the ledger every run** so it's the single source of truth.
- Drafts only at Phase 1. Advance to auto-send only once the user trusts the drafts.
