---
name: newsletter
description: name: newsletter

metadata:
  wing: content
  department: Marketing
  function: Distribution
  replaces: Turning useful ideas into a newsletter by rebuilding the same structure from scratch every time.
  the-human: The owner chooses the subject and approves the final send.
  ladder:
    manual: Run it manually and review every step.
    assisted: Prepare the work and wait for the owner's review.
    autonomous: Run on schedule after the owner has approved the pattern.
  trigger: Run when the user asks for this job or its schedule fires.
  outputs:
    - A structured distribution result
  kpis:
    - Completed outputs per run
    - Items flagged for owner review
  tools: [claude]
  requires-context: [context/about-business.md, references/voice.md]
  model: smart
  autonomy: assisted
  scaffolding-phase: 1
---


## What this does
The Content Wing's second workshop. Takes the freshest input available (the morning brief, a topic list, or this week's content) and turns it into a complete newsletter: subject line, preview text, branded body, CTA — in the user's voice.

## Inputs it reads
- Today's brief output or `pending` topics, if present — else ask for 3 topics
- `context/about-business.md` + `references/voice.md`
- `references/newsletter-template.md` if the user has saved one (branding, layout, footer)

## Execution
1. **Pick the spine.** One lead story, 3–5 short items, one CTA. A newsletter is a ranked brief with a personality, not a data dump.
2. **Write it.** Subject line (under 55 chars, curiosity or concrete payoff — no clickbait), preview text, lead paragraph in the user's voice, short items with "our take" per item, single CTA at the end.
3. **Assemble the HTML** from the saved template if present; otherwise clean minimal HTML (600px column, system fonts, one accent color from the brand).
4. **Deliver as a draft** with a note on how to send via the wired free provider (e.g. Resend Broadcasts). Never send without approval at Phase 1.

## Rules
- **One CTA.** More than one is none.
- **Subject line gets three options**, user picks.
- **Escape template variables properly** — unsubscribe tags must survive into the final HTML.
- **Deliverability basics:** send from a verified domain (SPF/DKIM), plain honest subject, no spam-trigger formatting.
- If a required context file is missing, say so and stop.
