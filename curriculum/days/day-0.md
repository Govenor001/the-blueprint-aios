# Day 0 — Prepare the Site

*The platform is already built. Today you connect its home server, Claude access, Telegram, and the private environment file that the rest of the challenge will use. ~25 minutes.*

**By the end of Day 0 you'll have:** the AIOS installed on your server, Claude authenticated for headless work, the dashboard loading, and a safe home for your keys.

---

## Step 1 — Claude + Claude Code (the one that matters)

Follow section 1 of [00-SERVICES-AND-SETUP.md](../00-SERVICES-AND-SETUP.md): subscribe to Claude Pro ($20/mo — the one real cost), rent the server, run the installer, and confirm the Mission Control dashboard loads. **Don't move on until it does.**

**A word on cost, because it's the question everyone asks.** Your subscription includes your usage. You are not billed per message, per agent, or per hour — it's the same $20 whether your AIOS runs once today or fifty times. There is a fair-use ceiling (Claude tracks usage in rolling windows), and if you ever hit it, Claude tells you and it resets. What you must **not** do is set up an Anthropic **API key**. That's the pay-per-word route, it has no ceiling, and it's how people accidentally spend $300 in a weekend. Nothing in this build needs one.

**The server is the normal route.** It has no browser, so the normal sign-in won't work. Run:

```bash
claude setup-token
```

It prints a link. Open that link on a browser, approve it, and paste the code back into the server. That's a long-lived token tied to your subscription — the same flat monthly cost — and it's what lets your AIOS keep working on schedule after you close the dashboard.

## Step 2 — A safe home for your keys

The installer creates the server-side `.env` file with restricted permissions. Add connections from the dashboard as each day calls for them; never put secrets in a loose file or in the repository. (A password manager for backups is even better.)

## What about all the other services?

They come later, on purpose: Groq on Day 3, Resend as Day 2 homework, Composio on Day 5, and Telegram on Day 6. The full setup guide for each lives in [00-SERVICES-AND-SETUP.md](../00-SERVICES-AND-SETUP.md) — you'll be pointed at the right section on the right day.

---

## Adapt-to-you note

Some services map to *your* business, not ours. When a guide says "your niche," "your domain," "your social accounts" — use yours. The *mechanism* is identical; the *content* is yours.

## Done when

The dashboard loads, the health check is green, and the server reports the map and activity log as ready.

## Proof of build

Post in the community: a screenshot of **Mission Control showing the green health check**, and a one-line "Day 0 done — platform ready." Read a few others' while you're there.

## Dashboard checkpoint

Open the map, choose the agent you will use first, read its safety boundary, and promote it from manual to assisted only after you understand its output.

## Tomorrow

Day 1 — you run one command, name your AIOS, and it learns your business well enough to tell *you* what to focus on this week.
