---
name: outreach
description: Draft personalized first-touch messages from a lead list. Use when someone says "write outreach", "draft cold emails", "message these leads", or after /qualify. One tailored opener per lead, in the user's voice, ready to review and send.
scaffolding-phase: 1
---

## What this does
The Growth Wing's second workshop. Turns a (qualified) lead list into personalized first-touch drafts — email or DM — each one specific to the lead, in the user's voice, with a soft, single ask. Drafts only; the user approves before anything sends.

## Inputs it reads
- The lead list (ideally the A-list from `qualify`)
- `context/about-business.md` — the offer and the outcome it delivers
- `references/voice.md` — so it sounds like the user, not a template

## Execution
1. **Find the hook per lead.** One specific, true thing about them (their role, a recent move, a pain the offer solves). Generic openers get deleted.
2. **Write the message.** Short. One personalized line → one line of relevance (the outcome, not the features) → one soft ask (a question or a low-friction next step). No pitch-slap.
3. **Match the voice.** Register from `voice.md`. Never fake the user's voice on something that sends externally without a visible draft.
4. **Deliver as a review list** — lead, channel, draft, and the hook it's built on. Flag any lead too thin to personalize (send to nurture instead).

## Rules
- **One specific hook per lead** or it goes to nurture — no mass-merge.
- **One ask.** Two asks is zero replies.
- **Outcome, not features.** Lead with what changes for them.
- **Draft, never auto-send.** Phase 1 is manual review, always.
