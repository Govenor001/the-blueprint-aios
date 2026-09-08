---
name: qualify
description: Score a lead list and tell the user who to call first and why. Use when someone says "qualify these leads", "who should I contact", "score my list", or hands over a CSV of prospects. Ranks by fit + intent so the user works the best leads first.

metadata:
  wing: growth
  department: Sales
  function: Qualification

  replaces: >
    Working a lead list top to bottom because nothing tells you which name is worth
    the call — so the best prospect in the file gets reached on a Thursday, cold,
    three weeks late.
  the-human: >
    You own who is actually worth your hours and what the offer is worth to them.
    The agent ranks the list; you decide which conversations you want.

  ladder:
    manual: >
      You skim the list, recognise two names, call those, and never get to row 40.
    assisted: >
      The agent scores and ranks every lead with a reason per score, you read the
      table and pick who to open.
    autonomous: >
      It scores on arrival, re-scores as new signals land, drops the A-list into
      outreach, and only pings you when a lead's score jumps.

  trigger: >
    User hands over a lead list (CSV or paste), or a new list lands in the leads folder.
  outputs:
    - Ranked table with a 0-100 score and one-line reason per lead
    - A/B/C grouping (call today / this week / nurture)
    - '"Start here" summary naming the top 5 and the sharpest hook for each'
  kpis:
    - Leads scored per run
    - Share of A-list that replies
    - Rows flagged for missing data
  tools: [claude, sheets]
  requires-context:
    - context/about-business.md

  model: smart

  autonomy: assisted
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
- **No context, no scoring.** If `context/about-business.md` is missing, say so and stop — a fit score against an unknown ICP is a made-up number.
- Hand-off ready for `outreach` — the A-list becomes its input.
