# Install — the one-paste setup

You don't set this up by hand. You paste one instruction into Claude Code and it installs itself, then walks you into Day 1. That's the whole point of an AI Operating System — it can build itself.

## Step 1 — Get the kit onto your machine
Clone this repo into a folder, or download it as a zip and unzip it.

## Step 2 — Open the folder in Claude Code
```
cd the-blueprint-aios
claude
```

## Step 3 — Paste this, exactly:

> Read `INSTALL.md`, then set me up. Confirm the four core skills in `.claude/skills/` are present, read `references/the-blueprint-framework.md` and `references/the-architects-loop.md` so you understand the system, then run the `/blueprint` skill to onboard me. Interview me, help me name you, and pour my Foundation. When you're done, tell me the one prompt to ask you next.

That's it. Claude Code reads its own instructions, verifies the kit, learns the frameworks, and runs your Day-1 onboarding. No config files to edit, no keys to paste yet — wiring starts on Day 3.

## What "installed" looks like
When setup finishes you'll have:
- A named AIOS with a personality you chose
- Your `context/` files filled with who you are, what you sell, this quarter's priorities, and your voice
- A filled `CLAUDE.md` operating manual
- The one wow prompt to ask it next: *"[Name], what should I focus on this week?"*

## If anything goes wrong
Run `/rescue`. It reads the error, checks the known-failures list, and either fixes it or hands you a ready-to-paste help request for the community. You are never stuck alone on this.

---
*The rest of the build — wiring live data, the five wings, phone access — is the 7-day challenge. See `curriculum/README.md`.*
