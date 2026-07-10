# The Blueprint — the four floors of an AIOS

You don't build a house by starting with the roof. You pour a foundation, run the wiring, build the workshops, then wire it to run on its own. An AI Operating System is the same. Four floors, built in order.

Most people fail because they start at the top — they try to build a fully autonomous agent before the thing even knows what their business does. The Blueprint stops that.

---

## Floor 1 — Foundation (it knows your business)

The Foundation is everything your AIOS knows about you without being told: who you are, what you sell, who you serve, how you sound, what matters this quarter, what you've already decided.

**Done when:** a brand-new Claude session, with no extra prompting, can answer *"what does this business do, who runs it, and what are they focused on right now?"* — in your voice.

**You build it with:** `/blueprint` (the Day-1 interview) fills your `context/` files and your operating manual. You add to it every time you make a decision worth remembering.

Foundation is non-negotiable and it's first. An AIOS without it is a stranger with opinions.

---

## Floor 2 — Wiring (it reaches your stuff)

Wiring connects your AIOS to live data — your calendar, your inbox, your leads, your niche's news. Not a paste of yesterday's numbers. Live.

**Done when:** you ask *"what's on my plate today?"* and it pulls real, current data with zero copy-paste.

**You build it with:** free APIs and small scripts. A Google News feed for your niche. The Gmail and Calendar APIs. A leads file. Each connection gets one row in `connections.md` and, if it took research to wire, a saved guide in `references/` so you never research it twice.

Wiring is what turns a clever writer into an operating system.

---

## Floor 3 — Workshops (it does the work)

A Workshop is a skill: a saved, repeatable job your AIOS runs on command. "Write this week's content." "Give me the morning brief." "Draft outreach to these leads." Each is a small assembly line that ships a real artifact.

**Done when:** a short phrase triggers a multi-step job and something usable comes out the other end.

**You build it with:** `/expand` (the weekly ritual that turns one manual task into one new skill) and the Skill Vault (ten pre-built workshops you customize).

Rule: **one workshop, one job.** A workshop that tries to do everything does nothing well.

---

## Floor 4 — Autopilot (it runs without being asked)

Autopilot is cadence — the schedules and triggers that make your AIOS work while you don't. The 7am brief. The daily content drop. The follow-up that goes out on time. And the phone line: you text it, it answers.

**Done when:** your laptop is closed, a brief lands in your pocket, and you can message your AIOS and get a real answer back.

**You build it with:** a free cloud server, a scheduler (cron), and a Telegram bot. This is the floor that makes it an *operating system* instead of an app you open.

**Build Autopilot last.** Never automate a job that doesn't already work when you run it by hand. If a workshop is flaky on demand, putting it on a timer just breaks it on schedule.

---

## The dependency order

```
Foundation ──▶ Wiring ──▶ Workshops ──▶ Autopilot
   (first)     (parallel with Workshops)    (last)
```

Foundation is first and mandatory. Wiring and Workshops can grow side by side. Autopilot is always last — it only automates what already works.
