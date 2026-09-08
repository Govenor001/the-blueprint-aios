---
name: onboard
description: Interview the owner to fill every context file required by the installed skills.

metadata:
  wing: command
  department: Foundation
  function: Context Onboarding
  replaces: Guessing what the business needs instead of collecting the owner's actual context.
  the-human: The owner supplies and approves the facts that become the AIOS foundation.
  ladder:
    manual: Complete the interview one question at a time.
    assisted: Suggest missing context files and draft answers for approval.
    autonomous: Re-check context freshness on a schedule.
  trigger: Start a new AIOS or ask to fill missing business context.
  outputs:
    - Completed context files
    - Missing-context checklist
  kpis:
    - Required context files completed
    - Questions answered
  tools: [claude]
  requires-context: []
  model: smart
  autonomy: assisted
  scaffolding-phase: 1
---

## What this does
Drives a one-question-at-a-time setup interview from the installed skills' requires-context fields.

## Inputs it reads
- Every installed skill's metadata.requires-context list
- Existing context files

## Execution
1. Read the skill map and collect unique required context paths.
2. Show progress as files completed out of total.
3. Ask one question at a time for each missing file.
4. Write only owner-approved answers, then report what remains.

## Rules
- Never invent business facts.
- Skip existing non-empty files.
- Stop and ask when the owner is unsure.
