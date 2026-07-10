---
name: brief
description: Your morning brief. Use when someone says "brief me", "what's the news", "morning brief", or on a schedule. Pulls overnight news in the user's niche, ranks it, and delivers the top items with a short take in their voice.
scaffolding-phase: 1
---

## What this does
The Intelligence Wing's daily output. Fetches fresh news for the user's niche, keeps what matters, and hands back a ranked brief — each item a headline plus one or two sentences of *our take*, in the user's voice. Runs on demand, or on a 7am schedule once you reach Autopilot.

## Inputs it reads
- `context/about-business.md` and `context/priorities.md` — so it knows the niche and what to weight
- `references/voice.md` — so the take sounds like the user
- A news source (free): Google News RSS for the niche keywords, and/or a signals file if the Intelligence Wing is wired

## Execution
1. **Fetch.** Pull the latest items for the niche keywords from the free news feed (last 24h). If a signals file exists, use it; if it's empty, fall back to the live feed — never run dry.
2. **Rank.** Score each item for relevance to the business and this quarter's priorities. Drop off-topic noise (stocks, gadgets, unrelated). Keep the top 10.
3. **Write the take.** For each kept item: the headline, then 1–2 sentences of what it means *for this business* — in the user's voice. No fluff, every line actionable or informative.
4. **Deliver.** Plain text, numbered, opening line "Here's this morning's brief." No attachments.

## Rules
- **Never run dry** — always have a fallback source.
- **Our take, never a borrowed name.** First person plural.
- **Relevance over volume** — 6 sharp items beat 10 padded ones.
- Phase 1: run it by hand, read the output, correct the ranking, *then* schedule it.
