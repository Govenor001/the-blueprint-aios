---
name: plan-day
description: Turn the owner's priorities into a practical daily plan.

metadata:
  wing: comms
  department: Back Office
  function: Calendar Management
  replaces: Filling the day with tasks without protecting time for the priorities that matter.
  the-human: The owner chooses what to accept, move, or decline.
  ladder:
    manual: Run it manually and review every step.
    assisted: Prepare the work and wait for the owner's review.
    autonomous: Run on schedule after the owner has approved the pattern.
  trigger: Run when the user asks for this job or its schedule fires.
  outputs:
    - A structured calendar management result
  kpis:
    - Completed outputs per run
    - Items flagged for owner review
  tools: [claude, calendar]
  requires-context: [context/priorities.md]
  model: smart
  autonomy: assisted
  scaffolding-phase: 1
---


## What this does
The Comms Wing's planning workshop. Pulls the calendar and task list, weighs them against this quarter's priorities, and hands back a realistic day — not a wish list. It answers "if I only get one real thing done today, what should it be, and when?"

## Inputs it reads
- Calendar (via the wired Calendar connection) — today's events + open blocks
- Task source (a `tasks.md`, or a wired tool) — what's outstanding
- `context/priorities.md` — the 90-day priorities everything gets weighed against

## Execution
1. **Map the fixed points.** Meetings and commitments already on the calendar; find the real open blocks between them.
2. **Rank the open work** by tie to priorities × urgency. Pick the one or two things that actually move a 90-day priority.
3. **Place them in real blocks** — match effort to available time, protect one deep-work block, don't over-schedule (leave slack).
4. **Deliver a plan:** the timeline for the day, the one "if nothing else, do this" item, and anything worth declining or moving.

## Rules
- **Realistic, not aspirational** — a plan with 12 hours of work in an 8-hour day is useless.
- **Tie the top item to a stated priority** — "why this matters today."
- **Protect one deep block** — the plan should defend focus, not just fill time.
- **Name what to skip.** Saying no is half of planning.
- If a required context file is missing, say so and stop.
