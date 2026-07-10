---
name: newsletter
description: Turn today's brief or topics into a send-ready newsletter. Use when someone says "write the newsletter", "newsletter draft", or on a schedule after the morning brief. Drafts in the user's voice with their branding, ready for a free email provider.
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
