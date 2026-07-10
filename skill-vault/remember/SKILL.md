---
name: remember
description: Save a fact to the AIOS's long-term memory so it stops asking twice. Use when someone says "remember that…", "make a note", "don't forget", or when a durable fact surfaces mid-conversation. One fact per file, indexed so it loads next session.
scaffolding-phase: 1
---

## What this does
The Foundation's memory workshop. When a fact worth keeping shows up — a preference, a decision, a person, a recurring detail — this saves it as a small memory file and indexes it, so the AIOS knows it in every future session instead of re-asking. This is what makes it feel like it actually knows the user over time.

## Where memory lives
- `memory/` — one file per fact, short and specific
- `memory/INDEX.md` — one line per memory (title + one-line hook), loaded at the start of each session

## Execution
1. **Decide if it's worth saving.** Durable and reusable → save. One-off or already in the repo/context files → don't. If unsure, ask "want me to remember this?"
2. **Write one file, one fact.** Give it a short kebab-case name and a one-line description. Body: the fact, plus *why it matters* and *how to apply it* if it's guidance.
3. **Index it.** Add a one-line pointer to `memory/INDEX.md`.
4. **Check for duplicates first** — update the existing file rather than creating a second one on the same topic. Delete memories that turn out wrong.

## Rules
- **One fact per file.** Small and specific beats one giant notes file.
- **Never store secrets** — no passwords, API keys, or tokens in memory. Those live in env vars.
- **Don't save what's already known** — the repo, context files, and chat history already hold plenty. Save what's *not* obvious.
- **Index every save** or it won't load next session.
