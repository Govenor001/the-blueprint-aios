# Day 4 — The Intelligence Wing

*Floor 2 (Wiring) meets Floor 3 (Workshops). Today your AIOS starts watching your market around the clock and hands you a ranked morning brief — replacing $100+/mo monitoring tools with $0. ~30 minutes.*

**By the end of Day 4:** a working intelligence engine pulling your niche's news from free sources, scored by AI, delivered as a morning brief in your voice.

---

## Why this wing is the sleeper hit

Most people never build market monitoring because the tools are expensive. Yours costs nothing: free public feeds (Google News, Reddit, Hacker News) plus Groq (free) to score and tag what matters. You wake up already knowing what happened in your world overnight — and so does your content.

## Step 1 — Give your AIOS its Groq key

The intelligence engine uses Groq (free) to score news so you don't spend Claude tokens on it.

> My Groq API key is gsk_... . Save it to my settings.

## Step 2 — Set your niche

The engine needs to know what to watch. Tell it plainly:

> Set up my Intelligence Wing. My niche keywords are: [5–8 terms your customers and competitors care about]. Watch Google News, Reddit, and Hacker News for these.

Examples: a realtor might use "mortgage rates, first-time buyers, [their city] housing, FHA loans"; a fitness coach "hypertrophy, protein timing, home gym, [their method]." Use *your* world.

## Step 3 — Run the engine

> Run the intelligence engine and show me what it found.

It fetches recent items from the free feeds, uses Groq to score each for relevance and tag it, and keeps the strongest signals. First run should surface real, current items about your niche.

## Step 4 — Install the morning brief

```
cp -r skill-vault/brief .claude/skills/
```

Then:

> Use the brief skill to give me this morning's brief.

You get a ranked, plain-language brief — each item a headline plus your AIOS's take, in your voice. This is what will land on your phone every morning once we go 24/7.

## Step 5 — Connect it to your content

Here's the compounding part: tell your Content Wing to use the brief.

> When you write my content, pull from today's intelligence brief so it's timely.

Now your content isn't generic — it reacts to what's actually happening in your market, today.

---

## Adapt-to-you note

The feeds are universal; your *keywords* make them yours. A B2B SaaS founder and a wedding photographer run the identical engine on completely different terms and get completely different briefs. Tune the keywords over a few days until the brief is consistently relevant — that tuning is the whole skill.

## Done when

Your engine returns real, current, on-topic signals for your niche, and the brief reads like something you'd actually want in your inbox each morning.

## Proof of build

Post your first morning brief about *your* industry. Seeing everyone's different-niche briefs side by side is one of the best threads in the challenge.

## Tomorrow

Day 5 — leads and your inbox: your AIOS qualifies prospects, drafts outreach, and plugs into your entire Google Workspace.
