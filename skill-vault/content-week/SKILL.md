---
name: content-week
description: name: content-week

metadata:
  wing: content
  department: Marketing
  function: Creation
  replaces: Starting every week with a blank page and inconsistent posts.
  the-human: The owner approves the drafts and chooses what gets published.
  ladder:
    manual: Run it manually and review every step.
    assisted: Prepare the work and wait for the owner's review.
    autonomous: Run on schedule after the owner has approved the pattern.
  trigger: Run when the user asks for this job or its schedule fires.
  outputs:
    - A structured creation result
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
The Content Wing's core workshop. From the user's brand, niche, and voice, it drafts a week of content — short posts, hooks, and carousel outlines — ready to review and schedule. One prompt in, a week out.

## Inputs it reads
- `context/about-business.md` — offer, ICP, angle
- `references/voice.md` — the register to match
- The morning brief or a topic list, if there's a fresh one — so content ties to what's actually happening

## Execution
1. **Pick the angles.** Choose 5–7 topics: mix evergreen (the offer, the ICP's pain) with timely (from the brief). One idea per post — don't cram.
2. **Draft each post.** In the user's voice, platform-appropriate length, a real hook on line one, one clear takeaway, a soft CTA. No hashtag salad, no "AI slop" phrasing.
3. **Add carousel outlines** for the 2–3 strongest ideas: title slide + 4–6 point slides, each slide one thought.
4. **Deliver as a review list** — numbered, easy to approve or edit. Never auto-publish on the first build.

## Rules
- **One idea per post.** Depth over breadth.
- **Match the voice sample** — don't invent a house style.
- **Show, don't send** — this drafts; the user approves. Advance past Phase 1 only when you trust it.
- Optional: hand the strongest script to a video tool (e.g. an avatar generator) if the user has one wired — but that's a bonus, not a dependency.
- If a required context file is missing, say so and stop.
