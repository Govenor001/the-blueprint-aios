---
name: inbox
description: Triage the owner's inbox and prepare safe next actions.

metadata:
  wing: comms
  department: Back Office
  function: Email Triage
  replaces: Reading every inbox message to find the few that truly need the owner.
  the-human: The owner decides what is important and approves replies.
  ladder:
    manual: Run it manually and review every step.
    assisted: Prepare the work and wait for the owner's review.
    autonomous: Run on schedule after the owner has approved the pattern.
  trigger: Run when the user asks for this job or its schedule fires.
  outputs:
    - A structured email triage result
  kpis:
    - Completed outputs per run
    - Items flagged for owner review
  tools: [claude, gmail]
  requires-context: [context/about-me.md, context/about-business.md, references/voice.md]
  model: smart
  autonomy: assisted
  scaffolding-phase: 1
---


## What this does
The Comms Wing's core workshop. Reads recent inbox threads and sorts them into what actually needs the user, then drafts replies for the ones that do — so the user makes decisions instead of reading every message.

## Inputs it reads
- Gmail (via the wired Gmail connection) — recent unread/important threads
- `context/about-me.md` + `context/about-business.md` — so it knows what matters and who's who
- `references/voice.md` — for reply drafts

## Execution
1. **Pull recent threads.** Last day or since last run.
2. **Triage into three buckets:** Reply-now (needs the user, time-sensitive or important) · Reply-later (matters, not urgent) · Ignore/archive (newsletters, noise, FYI).
3. **Draft the Reply-now set** in the user's voice — concise, answers the actual question, one clear next step. Never send; stage as drafts.
4. **Deliver** a one-screen triage: the three buckets with counts, the Reply-now drafts ready to approve, and a one-line "here's what actually needs you today."

## Rules
- **Read-only on the mailbox until trusted** — draft, don't send; never delete on the user's behalf at Phase 1.
- **Sign as the assistant, or as the user only with a visible draft** — never impersonate silently on an external reply.
- **Bias toward the Ignore bucket** — the value is protecting the user's attention, not surfacing everything.
- **Handle nothing you're unsure about** — flag it for the user rather than guess on something important.
- If a required context file is missing, say so and stop.
