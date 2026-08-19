# Services & Setup Guides — everything you'll sign up for

This is your complete parts list. By the end of the challenge your AI Operating System runs on these — the same stack that runs a real production system. **Almost all of it is free.** We'll tell you the exact cost of everything, honestly, up front.

Only the ⭐ items are needed before Day 1. Everything else gets set up on the day it's used — each daily lesson tells you when, and the step-by-step guide for it lives on this page.

---

## What you actually pay for (the whole truth)

| Service | What it's for | Cost | Required? |
|---|---|---|---|
| **Claude (Claude Code)** ⭐ | The brain — writes, reasons, runs everything | $20/mo (Claude Pro) for hands-on use; optional API pay-as-you-go (~$3–15/mo typical) for scheduled jobs | **Yes** — the one real cost |
| **Cloud server** | Runs your AIOS 24/7 *after* the challenge | $0–$6/mo | **No** — the challenge runs from your laptop; the server is the post-challenge graduation |
| **Social scheduler (Blotato)** | Auto-posts across your social channels | ~$29/mo | Optional — free alternatives given |

**Everything else on this page is free.** If you only ever pay for Claude, your AIOS still does the vast majority of what ours does.

---

## The free stack (all of it)

| Service | What it's for | Cost |
|---|---|---|
| Groq | Fast AI for scoring/drafting + voice transcription | Free tier |
| Composio | Connects Gmail, Calendar, Drive, Sheets, Docs, GitHub, Notion in one place | Free tier (20k actions/mo) |
| Telegram | Text/voice your AIOS from your phone | Free |
| Resend | Sends your newsletter so it lands in the inbox | Free tier (3k emails/mo) |
| ElevenLabs | Gives your AIOS a voice (optional) | Free tier |
| Remotion | Renders your videos | Free / open source |
| Google News + Reddit + Hacker News | Your market-intelligence feeds | Free, no signup |
| GitHub | Stores your code + free public hosting for your video files | Free |
| Skool | Your community (automation runs on your own login) | Free (the automation part) |

---

# ⭐ 1. Claude Code — the brain

**What it is:** Claude Code is Anthropic's AI that runs in your terminal. It's the engine of your whole AIOS — it writes your content, reasons about your business, and drives every other tool. This is the one thing worth paying for.

**Cost:** A **Claude Pro** subscription ($20/mo) covers everything you do hands-on in this challenge. **Two honest caveats:** Pro has weekly usage limits, and Anthropic's consumer terms cover *you* using Claude — not unattended scripts running while you sleep. For anything you put on a schedule (Day 7), the right tool is an **API key** (console.anthropic.com, pay-as-you-go — a daily brief and content draft typically runs a few dollars a month). We show both paths.

**Setup:**
1. Go to **claude.com** and create an account.
2. Subscribe to **Claude Pro** (Settings → Billing).
3. Install Claude Code: on Mac/Linux open Terminal; on Windows install via the instructions at **claude.com/code**. (We give exact commands in Day 0.)
4. Run `claude` in your terminal and log in with your Claude account when prompted.
5. Test: type `claude` and ask "are you working?" — you should get a reply.

> **Cheaper/heavier option:** an Anthropic **API key** (console.anthropic.com → API Keys) instead of Pro. Pay only for what you use. We'll show both paths.

---

# 2. Cloud server — optional, for after the challenge

**What it is:** A small always-on computer in the cloud, so your AIOS can keep working with your laptop closed.

**Do you need it this week? No.** Day 6 runs the phone bridge from your laptop. Moving to a server is the graduation step after the challenge, and we walk it properly then.

**Honest options when you're ready:**
- **A cheap paid VPS (~$4–6/mo)** — Hetzner, DigitalOcean, or similar. Boring, reliable, five-minute setup. This is what we actually recommend.
- **Oracle Cloud Always-Free** — genuinely $0, but with real catches: free ARM capacity is frequently unavailable ("out of capacity" errors are common), the free allotment has shrunk over time, and **Oracle's official policy reclaims idle free instances** (under ~20% utilization over 7 days) — which a light automation box often is. If free-with-caveats suits you, it works; go in with eyes open.
- **AWS free tier** — free for 12 months, then billed.

---

# 3. Groq — fast, free AI (set up on Day 3)

**What it is:** Groq runs open models extremely fast and free. Your AIOS uses it for the high-volume jobs where you don't need to spend Claude tokens — scoring news, quick drafts — and for **transcribing your voice notes** (Whisper).

**Cost:** Free tier (very generous).

**Setup:**
1. Go to **console.groq.com** and sign up.
2. Open **API Keys** → **Create API Key** → copy it (starts with `gsk_`).
3. Save it into your `.env` file — Day 3 uses it.

---

# 4. Composio — one connection for your whole Google Workspace

**What it is:** Composio handles the hard part of connecting your AIOS to Gmail, Calendar, Drive, Sheets, Docs, GitHub, and Notion. It manages the sign-in and keeps it connected so your AIOS never has to re-authenticate. This is what powers your Comms Wing.

**Cost:** Free tier — 100,000 tool calls/month on the pricing introduced 2026-08-15 (20,000 of them via Composio's shared Google app; some premium tools bill separately from 2026-09-01). Far more than a personal setup uses.

**Setup:**
1. Go to **composio.dev** and sign up (Google sign-in is quickest).
2. Open the dashboard at **dashboard.composio.dev**.
3. **Settings → Project Settings → API Keys** → copy your key (starts with `ak_`). Save it.
4. In **Toolkits/Apps**, find each app you want (start with **Gmail** and **Google Calendar**), click **Connect**, and complete the Google sign-in **all the way to the "connected" screen** (this is the step people miss — if it says "initializing," you didn't finish).
5. You can add **Drive, Sheets, Docs, GitHub, Notion** the same way.

> **Day-5 tip:** finish the consent to a success page for each. Half-finished connections show as "initializing" and won't work.

---

# 5. Telegram — your AIOS in your pocket

**What it is:** A free messaging app. You'll create a **bot** so you can text (and voice-note) your AIOS from anywhere.

**Cost:** Free.

**Setup:**
1. Install **Telegram** on your phone and/or desktop.
2. In Telegram, search for **@BotFather** (the official bot-maker).
3. Send `/newbot`, follow the prompts (name it, e.g. "My AIOS"), and BotFather gives you a **bot token** — copy it.
4. Get your **chat ID**: message your new bot once, then we'll pull the ID with a one-line command on Day 6 (or search **@userinfobot** and it tells you your ID).
5. Save the bot token + chat ID for Day 6.

---

# 6. Resend — inbox-landing newsletter

**What it is:** Resend sends email that actually reaches the inbox. It replaces expensive newsletter tools. You'll use it to send your newsletter to your list.

**Cost:** Free tier — 3,000 emails/month, 100/day.

**Setup:**
1. Go to **resend.com** and sign up.
2. **API Keys → Create** → copy the key (starts with `re_`). Save it.
3. **Domains → Add Domain** → enter a domain you own (e.g. yourbrand.com).
4. Resend shows you **DNS records** (SPF, DKIM) — add them at your domain registrar (GoDaddy, Namecheap, Cloudflare, etc.). This is what makes your mail land in the inbox, not spam.
5. Wait for the domain to show **Verified** (usually minutes, sometimes a few hours).

> No domain yet? You can send from Resend's shared domain to test, but get your own domain for real sending — it's ~$10/yr and essential for deliverability.

---

# 7. ElevenLabs — give your AIOS a voice (optional)

**What it is:** Turns your AIOS's replies into natural speech, so voice notes come back as a real voice.

**Cost:** Free tier is **non-commercial use only** (~10 minutes of speech/month). Using the voice in your business needs the $6/mo Starter plan. Skip this entirely if you don't want spoken replies — text costs nothing.

**Setup:**
1. Go to **elevenlabs.io** and sign up.
2. **Profile → API Key** → copy it. Save it.
3. Pick or create a **voice** in the Voices library and copy its **Voice ID**.
4. Save the key + voice ID for Day 6. (Skip this entirely if you don't want spoken replies — text still works.)

---

# 8. GitHub — code storage + free video hosting

**What it is:** GitHub stores your AIOS code, and its **Releases** feature doubles as free public hosting for your rendered video files (so your social scheduler can grab them).

**Cost:** Free.

**Setup:**
1. Go to **github.com** and create an account.
2. Install **Git** on your machine (git-scm.com).
3. Create a **Personal Access Token** (Settings → Developer settings → Tokens) — you'll use it for command-line pushes. Save it.
4. That's it for now — you'll create your AIOS repo during the build.

---

# 9. Remotion — your video engine

**What it is:** Remotion renders videos from code. Your AIOS uses it (with the two presets included in this kit) to make scroll-stopping vertical videos for your content.

**Cost:** Free / open source.

**Setup:**
1. Install **Node.js** (nodejs.org, LTS version) — this also gives you `npm`.
2. Remotion installs itself into your project with one command on Day 2 (`npm install`); no account needed.
3. The two ready-made presets ship in this kit under `video-presets/`.

---

# 10. Intelligence feeds — Google News, Reddit, Hacker News

**What it is:** Free, public sources your Intelligence Wing reads to monitor your market. **No signup, no keys.** Your AIOS pulls them directly.

**Cost:** $0. Nothing to set up — you just tell your AIOS your niche keywords on Day 3.

---

# 11. Social scheduler (Blotato) — optional paid

**What it is:** Blotato posts your content across multiple social platforms on a schedule from one place. It's the one convenience tool that's paid.

**Cost:** ~$29/mo.

**Free alternatives (we teach these too):**
- Post directly via each platform's own free API (more setup, $0).
- Use a free scheduler's free tier for a couple of channels.
- Have your AIOS **draft everything and drop it in your Telegram** for you to post with one tap — $0, fully manual publish, fully automated creation.

**Blotato setup (if you choose it):**
1. Sign up at **blotato.com**, connect your social accounts.
2. **Settings → API** → copy your API key. Save it for Day 2.

---

# 12. Skool — why we DON'T automate it

Skool has no public API, and its Terms of Service prohibit automated access to accounts — including your own. Automating your login risks the community you're building, so we don't, and you shouldn't. If you need Skool automation, use Skool's official Zapier integration; otherwise, let your AIOS **draft** Skool posts and comments and post them yourself in one tap.

---

## Day-0 checklist (only two things are required before Day 1)

- [ ] ⭐ Claude account + Claude Pro + Claude Code installed and replying
- [ ] ⭐ Telegram installed + bot created via @BotFather + token saved into `.env`
- [ ] Git + Node.js installed (`git --version`, `node --version` both answer)
- [ ] Copied `.env.example` to `.env` (your one safe home for keys — never a loose text file, never committed)

Everything else on this page gets set up **on the day it's used** — the lesson tells you when. Optional head start if you have 10 spare minutes: create your Groq key (Day 3) and your Resend account (Day 4).

Once these boxes are checked, Day 1 flies. See `days/day-0.md` for the walkthrough.
