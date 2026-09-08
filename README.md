# The Blueprint — Build Your Own AI Operating System

A complete platform that turns Claude Code into a personal **AI Operating System (AIOS)** — a named AI staff member that writes your content, monitors your market, works your leads, handles your inbox, and takes orders from your phone. **The interface, map, bridge, vault, schedules, and safety controls are already built; students connect their own services and context on their server.**

This is the kit you build in **The 7-Day Agent Architect Challenge**. It's the same architecture that runs our own companies — packaged so you can run yours on it.

> **Building this, rather than following it?** Start at
> **[IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md)** — the build specification. Eight
> builds, 49 tasks, each with a DO and a CHECK. Read **BUILD 0** before writing any code,
> and read the "Start here" section before that. This README describes the product; the
> plan describes how to construct it.

---

## The one test that matters

> **While your laptop is closed, your AIOS observes one real event and produces an output faster and better than you would have — and it reaches you on your phone.**

Every part of this kit rolls up to that. If a floor, a wing, or a skill doesn't move you toward it, it doesn't ship. Because it lives on your own server, the lid is closed from Day 0 — that test is the product, not a graduation step you reach later.

---

## The two frameworks

You learn to *think* like an architect (**The Architect's Loop**) and to *build* like one (**The Blueprint**). The loop is how you decide what to automate; the blueprint is what you actually construct.

### The Architect's Loop — how you think
**Survey → Design → Construct.**
- **Survey** — walk your week, find the drudgery and the bottleneck.
- **Design** — decide the fate of the task: *Kill it, Automate it, or Assign it* (to a person). Pick the lowest autonomy level that works. Tie it to a number.
- **Construct** — build in small, tested blocks. Roll it out on **Scaffolding**: manual → drafted → supervised → hands-off. Take the supports off one at a time.

Full detail: [references/the-architects-loop.md](references/the-architects-loop.md)

### The Blueprint — what you build
Four floors, built in order. You can't put up walls before the foundation.

| Floor | Name | It's done when… |
|---|---|---|
| 1 | **Foundation** | A fresh Claude session can answer "what does this business do and who runs it?" without being told |
| 2 | **Wiring** | "What's on my plate today?" pulls live data — no copy-paste |
| 3 | **Workshops** | A short phrase triggers a multi-step job that ships a real artifact |
| 4 | **Autopilot** | Laptop closed. A brief lands on your phone. You text it and it answers |

Full detail: [references/the-blueprint-framework.md](references/the-blueprint-framework.md)

---

## The operating map

Your AIOS is one second brain with seven operating wings. Each wing is a visible part of the map and contains departments, functions, and named agents.

| Wing | What it does for you |
|---|---|
| **Content Wing** | Writes posts, carousels, newsletter drafts, and video scripts in your voice |
| **Intelligence Wing** | Monitors your niche 24/7 and hands you a ranked morning brief |
| **Growth Wing** | Qualifies leads, drafts outreach, runs your follow-up |
| **Comms Wing** | Triage, drafts, and daily plan for your email and calendar |
| **Command Wing** | Your phone HQ — text or voice-note your AIOS from anywhere |
| **Back-office Wing** | Finance, records, and internal administration |
| **Build Wing** | Platform health, delivery, and expansion |

---

## The skills

The kit ships four core skills plus a **Skill Vault** of ten more you unlock as you build.

| Skill | When you run it |
|---|---|
| `/blueprint` | Day 1. Interviews you, names your AIOS, fills its brain. |
| `/inspect` | Day 7, then weekly. Scores your AIOS out of 100 against The Blueprint. Watch it climb. |
| `/expand` | Weekly ritual. Finds one thing worth automating, scopes it, ships it. |
| `/rescue` | Any time something breaks. Reads the error, checks known failures, fixes it or tells you exactly what to paste for help. |

See [.claude/skills/](.claude/skills/) for the four core skills and [skill-vault/](skill-vault/) for the ten bonus skills.

---

## Quick start

1. **Install the platform** on an Ubuntu 24.04 server with `deploy/install.sh`.
2. **Authenticate Claude headlessly** with `claude setup-token`, then connect Telegram and your chosen services.
3. **Follow the seven-day challenge.** Add your business context, keys, sources, and approval choices; do not rebuild the platform.
4. **Day 7:** run `/inspect`, test a timer, and confirm the student acceptance checklist.
5. **Weekly:** run `/expand`. Add one approved automation to the existing map.

Full day-by-day path: **The 7-Day Agent Architect Challenge** (see `curriculum/`).

---

## License

MIT — build on it, ship it, and sell what you build with it. See `LICENSE`.
