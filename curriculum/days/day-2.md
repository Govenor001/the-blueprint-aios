# Day 2 — The Content Wing, Part 1

*Floor 3 begins: your first Workshop. Today your AIOS writes a week of your content, in your voice, in the time it takes to make coffee. ~25 minutes.*

**By the end of Day 2:** a week of social posts and carousel outlines, written in your voice, ready to review — and you'll understand exactly how the skill did it, so it's never magic.

---

## Why content first

It's the fastest "holy, it actually works" moment, and it's the wing most people join for. It also teaches you what a **skill** is — the building block of every Workshop — using an example that pays off immediately.

## Step 1 — Understand what a skill is (2 minutes)

Open `skill-vault/content-week/SKILL.md` and read it. Notice the shape: a description of *when* to use it, the inputs it reads (your business, your voice), the steps it follows, and the rules it obeys. That's all a skill is — a repeatable job written in plain language. You'll build your own later; today you use a ready one.

## Step 2 — Install the Content Wing skill

Copy the `content-week` skill from the Vault into your active skills:

```
cp -r skill-vault/content-week .claude/skills/
```

Ask your AIOS to confirm it sees it:

> Do you have the content-week skill available? List your skills.

## Step 3 — Generate your week

Run it:

> Use content-week to write my content for the week.

It reads your business and voice (from Day 1) and drafts 5–7 posts plus a couple of carousel outlines — about *your* niche, for *your* audience.

## Step 4 — Tune the voice

Read the drafts. Do they sound like you? If the tone's off:
- Add another real writing sample to `references/voice.md`.
- Tell it directly: "make these punchier / warmer / less formal — here's an example of my actual voice: [paste]."
- Re-run. This is the loop — a few rounds and it locks onto your voice.

## Step 5 — Decide how you'll publish

Two paths (you chose one on Day 0):
- **Free route:** have your AIOS drop the finished posts into a file or your Telegram (wired Day 6), and you post them with a tap. Zero cost, you stay in control.
- **Blotato route (paid):** connect Blotato so your AIOS schedules them automatically. We wire this on Day 7's autopilot.

For today, just get great drafts. Publishing comes later.

---

## Adapt-to-you note

Our content is about AI automation across four brands. Yours is about *your* thing — real estate, coaching, e-commerce, a local service. The skill doesn't care; it writes from *your* Foundation. If your business is visual (say, interior design), lean on the carousel outlines; if it's B2B, lean on the text posts. Tell the skill your preference and it adjusts.

## Done when

You have a week of posts in your voice that you'd actually be happy to publish, and you can explain (from Step 1) roughly how the skill produced them.

## Proof of build

Post one AI-generated post next to something you wrote by hand. Ask the community: can they tell which is which? When they can't, you've nailed the voice.

## Tomorrow

Day 3 — a send-ready newsletter that lands in the inbox, plus your video engine.
