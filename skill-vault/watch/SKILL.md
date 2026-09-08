---
name: watch
description: name: watch

metadata:
  wing: intelligence
  department: Intelligence
  function: Monitoring
  replaces: Checking competitors and market signals manually and inconsistently.
  the-human: The owner decides which movement merits a response.
  ladder:
    manual: Run it manually and review every step.
    assisted: Prepare the work and wait for the owner's review.
    autonomous: Run on schedule after the owner has approved the pattern.
  trigger: Run when the user asks for this job or its schedule fires.
  outputs:
    - A structured monitoring result
  kpis:
    - Completed outputs per run
    - Items flagged for owner review
  tools: [claude]
  requires-context: [context/watchlist.md]
  model: smart
  autonomy: assisted
  scaffolding-phase: 1
---


## What this does
The Intelligence Wing's second workshop. Maintains a small watchlist (competitors, keywords, brands) and checks free sources for movement: new content, launches, pricing changes, funding, hiring signals. Reports only what changed — silence when nothing did.

## Inputs it reads
- `context/watchlist.md` — one line per target: name, why watched, last-known state (create it on first run by asking for 3–5 targets)
- Free sources: Google News RSS per target, their public site/blog, Reddit mentions

## Execution
1. **Load the watchlist.** If empty, interview: "Name 3–5 competitors or topics you'd pay to have watched. For each: why?"
2. **Sweep.** For each target, pull the last 7 days from free feeds. Compare against last-known state.
3. **Filter hard.** Only genuine movement counts: launched, changed pricing, raised, hired notably, shipped content that's working. No "they posted on LinkedIn again."
4. **Report.** Per mover: what changed, why it matters *to this business*, and one suggested response ("your move"). Update last-known state in the watchlist.

## Rules
- **Silence is a valid report.** "No meaningful movement" beats manufactured news.
- **Always end a mover with "your move:"** — intel without a suggested action is trivia.
- **Update the watchlist file every run** so state compounds.
- If a required context file is missing, say so and stop.
