---
name: followup
description: name: followup

metadata:
  wing: growth
  department: Sales
  function: Sequencing
  replaces: Losing good leads because nobody remembers the next useful follow-up.
  the-human: The owner chooses whether a message is appropriate and approves every send.
  ladder:
    manual: Run it manually and review every step.
    assisted: Prepare the work and wait for the owner's review.
    autonomous: Run on schedule after the owner has approved the pattern.
  trigger: Run when the user asks for this job or its schedule fires.
  outputs:
    - A structured sequencing result
  kpis:
    - Completed outputs per run
    - Items flagged for owner review
  tools: [claude]
  requires-context: [context/followups.md, references/voice.md]
  model: smart
  autonomy: assisted
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
- If a required context file is missing, say so and stop.
