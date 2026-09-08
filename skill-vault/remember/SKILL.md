---
name: remember
description: Save an approved durable fact to the local business context.

metadata:
  wing: intelligence
  department: Knowledge
  function: Context Maintenance
  replaces: Re-answering the same durable preference because it was never saved in a reliable place.
  the-human: The owner decides what is durable enough to remember.
  ladder:
    manual: Run it manually and review every step.
    assisted: Prepare the work and wait for the owner's review.
    autonomous: Run on schedule after the owner has approved the pattern.
  trigger: Run when the user asks for this job or its schedule fires.
  outputs:
    - A structured context maintenance result
  kpis:
    - Completed outputs per run
    - Items flagged for owner review
  tools: [claude]
  requires-context: []
  model: smart
  autonomy: assisted
  scaffolding-phase: 1
---


## What this does
The Foundation's memory workshop. When a fact worth keeping shows up — a preference, a decision, a person, a recurring detail — this saves it as a small memory file and indexes it, so the AIOS knows it in every future session instead of re-asking. This is what makes it feel like it actually knows the user over time.

## Where memory lives
- `memory/` — one file per fact, short and specific
- `memory/INDEX.md` — one line per memory (title + one-line hook), loaded at the start of each session

## Execution
1. **Decide if it's worth saving.** Durable and reusable → save. One-off or already in the repo/context files → don't. If unsure, ask "want me to remember this?"
2. **Write one file, one fact.** Give it a short kebab-case name and a one-line description. Body: the fact, plus *why it matters* and *how to apply it* if it's guidance.
3. **Index it.** Add a one-line pointer to `memory/INDEX.md`.
4. **Check for duplicates first** — update the existing file rather than creating a second one on the same topic. Delete memories that turn out wrong.

## Rules
- **One fact per file.** Small and specific beats one giant notes file.
- **Never store secrets** — no passwords, API keys, or tokens in memory. Those live in env vars.
- **Don't save what's already known** — the repo, context files, and chat history already hold plenty. Save what's *not* obvious.
- **Index every save** or it won't load next session.
