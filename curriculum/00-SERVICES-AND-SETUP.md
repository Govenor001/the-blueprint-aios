# Services & Setup Guides — everything you'll sign up for

This is your complete parts list. By the end of the challenge your AI Operating System runs on these — the same stack that runs a real production system. **Almost all of it is free.** We'll tell you the exact cost of everything, honestly, up front.

Set these up during **Day 0** so nothing stalls you once the build starts. Each guide is step-by-step. Do them in order; the ⭐ ones are needed from Day 1, the rest you'll wire on the day they're introduced.

---

## What you actually pay for (the whole truth)

| Service | What it's for | Cost | Required? |
|---|---|---|---|
| **Claude (Claude Code)** ⭐ | The brain — writes, reasons, runs everything | ~$20/mo (Claude Pro) | **Yes** — the one real cost |
| **Cloud server** ⭐ | Runs your AIOS 24/7 | **$0** on Oracle Always-Free (taught default) | Yes, but free |
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

**Cost:** A **Claude Pro** subscription (~$20/mo) covers it for personal use. Heavy/business use can instead use an **API key** (pay-as-you-go).

**Setup:**
1. Go to **claude.com** and create an account.
2. Subscribe to **Claude Pro** (Settings → Billing).
3. Install Claude Code: on Mac/Linux open Terminal; on Windows install via the instructions at **claude.com/code**. (We give exact commands in Day 0.)
4. Run `claude` in your terminal and log in with your Claude account when prompted.
5. Test: type `claude` and ask "are you working?" — you should get a reply.

> **Cheaper/heavier option:** an Anthropic **API key** (console.anthropic.com → API Keys) instead of Pro. Pay only for what you use. We'll show both paths.

---

# ⭐ 2. Cloud server — where your AIOS lives 24/7

**What it is:** A small always-on computer in the cloud so your AIOS keeps working when your laptop is closed.

**Cost:** **$0** if you use **Oracle Cloud Always-Free** (our taught default — it's genuinely free forever). AWS free tier also works for the first 12 months.

**Setup (Oracle Always-Free):**
1. Go to **oracle.com/cloud/free**, create an account (a card is required for identity verification but you won't be charged on Always-Free).
2. In the console: **Create a VM instance** → choose an **Always Free eligible** shape (Ampere/ARM, 1–4 cores).
3. Choose **Ubuntu** as the image.
4. Download the **SSH key pair** it generates (keep the private key safe — it's how you log in).
5. Note the instance's **public IP address**.
6. Test the connection (Day 6 walks this in full): `ssh -i your-key ubuntu@YOUR_IP`.

> Prefer AWS? Create a free-tier **EC2 Ubuntu** instance instead — same idea, same steps later. Oracle is our default only because it's free with no 12-month clock.

---

# ⭐ 3. Groq — fast, free AI

**What it is:** Groq runs open models extremely fast and free. Your AIOS uses it for the high-volume jobs where you don't need to spend Claude tokens — scoring news, quick drafts — and for **transcribing your voice notes** (Whisper).

**Cost:** Free tier (very generous).

**Setup:**
1. Go to **console.groq.com** and sign up.
2. Open **API Keys** → **Create API Key** → copy it (starts with `gsk_`).
3. Save it somewhere safe — you'll paste it into your AIOS's settings on Day 4.

---

# 4. Composio — one connection for your whole Google Workspace

**What it is:** Composio handles the hard part of connecting your AIOS to Gmail, Calendar, Drive, Sheets, Docs, GitHub, and Notion. It manages the sign-in and keeps it connected so your AIOS never has to re-authenticate. This is what powers your Comms Wing.

**Cost:** Free tier — 20,000 actions/month, far more than a personal setup uses.

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

**Cost:** Free tier (enough for personal use).

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

**Cost:** $0. Nothing to set up — you just tell your AIOS your niche keywords on Day 4.

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

# 12. Skool — your community (automation is free)

**What it is:** If you run (or start) a Skool community, your AIOS can post, engage, and manage members in it. The automation runs on your **own login**, so there's no extra cost beyond whatever Skool plan you already have.

**Setup:** Covered on its own day — your AIOS uses your logged-in session, no separate API signup.

---

## Day-0 checklist (do all of these before Day 1)

- [ ] ⭐ Claude account + Claude Pro + Claude Code installed and replying
- [ ] ⭐ Cloud server account created (Oracle Always-Free), SSH key saved, IP noted
- [ ] ⭐ Groq API key saved
- [ ] Composio account + API key saved (connect Gmail now if you can)
- [ ] Telegram installed + bot created + token saved
- [ ] Resend account + API key + domain added (verification can finish later)
- [ ] GitHub account + Git installed + token saved
- [ ] Node.js installed
- [ ] ElevenLabs key saved (optional)
- [ ] Decided on social publishing: Blotato (paid) or the free Telegram-draft route
- [ ] A folder on your computer to keep all these keys safe (a password manager is ideal)

Once these boxes are checked, Day 1 flies. See `days/day-0.md` for the walkthrough.
