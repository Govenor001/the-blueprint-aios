---
name: expand
description: The weekly ritual — find one automation worth building, scope it, ship it. Use when someone says "let's expand", "what should I automate next", "add a room", or as a Friday habit. One run = one shipped skill.
---

## What this does

Walks the user through The Architect's Loop once a week to surface and ship **one** new workshop. One run, one artifact. It also drills the Loop into their head — after four or five runs they start spotting automations mid-week without prompting, because the questions have become instinct. That's the real payoff. The kit doesn't need this on a timer; it needs the user running it every Friday.

Not `/inspect` (that's "is it built right?"). This is "what leverage am I missing?" Run `/inspect` first if the structure is messy.

## First run: Day 14, after the user has wired at least one connection and run `/inspect` once. Earlier, the output is trivial.

## Phase 1 — Survey (find the candidate)
Ask, conversationally, in order:
1. Walk me through your week — what did you do 3+ times?
2. Anything that felt manual, boring, or copy-paste?
3. Anything where you thought "a sharp intern could do this"?
4. If 500 customers showed up tomorrow, what breaks first?
5. What would bring you those 500?
Surface 1–3 candidates ranked by leverage. Then: **"Pick one to scope."**

## Phase 2 — Design (scope one)
- **Fate first — Kill / Automate / Assign.** Ask "what if you just stopped doing this?" If nothing breaks → Kill it, log the win, stop. Cheerfully. That's a success. If it needs human judgment → Assign to a person, log it, stop.
- **If automating: map it** — trigger, sources, transform, branch, destination. If they can't name all five: "if you can't explain it to a person, you can't explain it to an AI — sketch it and come back."
- **Autonomy level** — default to the lowest that works (L1 suggested → L4 hands-off). Push back hard on L4 on a first build.
- **The number** — which lever (more customers / more per customer / less cost) and which metric. No number, no build.
Write the scoped spec to `decisions/log.md` as a dated entry.

## Phase 3 — Construct (ship it)
Ask "how do you want to ship this?" Default to the most boring option that works:
1. **Saved prompt** — a template they run by hand. Zero infrastructure.
2. **Deterministic skill** — a SKILL.md that runs a script, no AI step. Best for clear-rule transforms.
3. **AI-assisted skill** — a SKILL.md with one AI call (draft / classify / summarize).
4. **Sub-agent** — last resort, only if it genuinely needs reasoning + tools.

Scaffold the chosen artifact. Stamp every new skill with a scaffolding header:
```markdown
---
scaffolding-phase: 1   # Phase 1 — manual. Run it by hand first.
---
```
This locks them into manual rollout on the first build; the phase only advances by an explicit edit, so they can't silently skip straight to hands-off.

## Output every run
1. One dated `decisions/log.md` entry with the scoped spec.
2. One scaffolded artifact (prompt, skill, or agent).
3. A one-screen close: what was scoped, what shipped, and the Phase-1 reminder.

## Rules
1. **One run = one artifact.** No parallel scoping.
2. **Survey always runs first**, even if they arrive with a pre-formed idea.
3. **Kill-first** — if the answer is Kill, exit happy; that's a win.
4. **Lowest autonomy that works.** Earn L4.
5. **The number is mandatory.** No metric, skill stops.
6. **Scaffolding Phase 1 ships into every artifact.**
