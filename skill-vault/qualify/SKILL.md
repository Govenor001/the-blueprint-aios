---
name: qualify
description: Score a lead list and tell the user who to call first and why. Use when someone says "qualify these leads", "who should I contact", "score my list", or hands over a CSV of prospects. Ranks by fit + intent so the user works the best leads first.
scaffolding-phase: 1
---

## What this does
The Growth Wing's first workshop. Takes a lead list and scores each lead on fit (do they match the ICP?) and signal (is there a reason to reach out now?), then ranks them so the user spends their limited hours on the highest-probability conversations.

## Inputs it reads
- The lead list (CSV/paste: name, company, role, plus whatever's there — site, LinkedIn, notes)
- `context/about-business.md` — the ICP and offer, so "good fit" means something specific

## Execution
1. **Define fit from the ICP.** Pull the ideal-customer profile from context. Fit = how closely each lead matches (industry, size, role, stage).
2. **Read for signal.** From whatever's in the row (recent hire, funding, a pain the offer solves, engagement), score intent/timing.
3. **Score + rank.** Combine into a single 0–100 with a one-line "why" per lead. Group into A (call today), B (this week), C (nurture).
4. **Deliver a ranked table** + a one-paragraph "start here" summary: the top 5 and the single sharpest reason to open each.

## Rules
- **Fit AND signal.** A perfect-fit lead with no reason-to-call-now isn't an A.
- **Every score gets a one-line reason** — no black-box numbers.
- **Never invent facts** about a lead. Score on what's in the row; flag what's missing.
- Hand-off ready for `outreach` — the A-list becomes its input.
