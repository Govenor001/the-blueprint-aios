---
name: operator
description: Turn an approved request into a bounded draft or controlled action while stopping for owner approval before consequences.
metadata:
  wing: command
  department: Command
  function: Operations
  replaces: Repeating operational work without a visible approval boundary.
  the-human: Approves consequential actions and owns the final decision.
  ladder:
    manual: Owner performs each operational step.
    assisted: Agent prepares a draft and waits for approval.
    autonomous: A bounded routine runs only after the owner approves the schedule.
  trigger: Run when the owner requests an operational draft or approved action.
  outputs: [Draft, approval request, execution record]
  kpis: [Drafts returned, approvals recorded, actions with evidence]
  tools: [claude]
  requires-context: [context/about-business.md, context/faq.md]
  model: smart
  autonomy: assisted
  scaffolding-phase: 2
---

## What this does

Operator prepares work and makes the approval boundary visible.

## Execution

1. Read the request, business context, and FAQ.
2. Draft the requested work.
3. Stop before sending, publishing, spending, deleting, or changing external data.
4. Record the owner approval and the result if the owner proceeds.

## Rules

Never claim an action happened before a verified result exists.
