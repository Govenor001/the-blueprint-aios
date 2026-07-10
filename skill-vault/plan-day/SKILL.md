---
name: plan-day
description: Build the user's day around their priorities. Use when someone says "plan my day", "what's on today", "help me prioritize", or on a morning schedule. Reads calendar + tasks + priorities and produces a realistic plan.
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
