# Day 4 — The Content Wing, Part 2: Newsletter + Video

*Two more Workshops today: a newsletter that lands in the inbox, and a video engine that turns your content into scroll-stopping clips. ~35 minutes.*

**By the end of Day 4:** a send-ready newsletter proven to hit your own inbox, and two ready-to-use video presets configured to your brand.

---

## Part A — The Newsletter

### Why Resend, and why domain verification matters

Most newsletters die in spam because the sender's domain isn't verified. Resend (free) plus proper DNS records is what gets you into the Primary inbox. We do the boring-but-critical part first.

### Step 1 — Finish your Resend domain

In your Day 2 homework you created your Resend account and added your domain (if you skipped it, do it now — section 6 of the services guide — and let DNS verify while you build the video half). Check it now:
- In Resend → **Domains**, it should say **Verified**. If it still says pending, confirm the SPF and DKIM DNS records are in at your registrar and give it time.
- Verified means your mail is authenticated. This one step is the difference between inbox and spam.

### Step 2 — Install and configure the newsletter skill

```
cp -r skill-vault/newsletter .claude/skills/
```

Tell your AIOS your sending details:

> Set my newsletter sender to "Your Name <newsletter@yourdomain.com>" and my Resend API key is re_... . Save these to my settings.

### Step 3 — Draft and test-send

> Use the newsletter skill to turn my best content this week into a newsletter, then send a test to my own email address.

Check your inbox. Confirm it:
- Landed in **Primary** (not Promotions/Spam).
- Looks right (subject, layout, your voice, working unsubscribe).

If it hit spam, your domain verification isn't complete — fix that before sending to anyone real.

---

## Part B — The Video Engine

### Why video-as-code

Your AIOS can generate videos on command using Remotion and the two presets in this kit — no video editor, no timeline. When your content changes, it re-renders in one command.

### Step 4 — Set up the presets

The two presets live in `video-presets/` — a ready-to-run project:
- **Pulse** — news/insight clips (animated charts, kinetic headlines)
- **Breakdown** — listicle/steps clips (numbered, with a progress bar)

Install once and open the live preview:

```
cd video-presets
npm install
npm run studio
```

Then point them at your brand — ask your AIOS:

> Read video-presets/README.md. Add my brand to the BRANDS palette in ArchitectKit.jsx with my colors: [your hex codes].

### Step 5 — Render your first video

> Write Pulse props for this week's top insight from my signals, then render it.

Or render straight from the terminal: `npm run render:pulse`. You get a vertical MP4 in `video-presets/out/`. Preview it. Change the data, re-render — that's the whole loop.

---

## Adapt-to-you note

Your newsletter is *your* list and *your* voice — could be a weekly market update for real-estate clients, a coaching tip series, a product drop announcement. The video presets take *your* colors and *your* numbers. Same engines, your brand.

## Done when

A test newsletter is confirmed in your own Primary inbox, and you've rendered one video in your brand colors.

## Proof of build

Post a screenshot of your test newsletter **in your own inbox (Primary tab)** — the deliverability proof. Bonus: drop your first rendered video.

## Tomorrow

Day 5 — leads and your inbox: your AIOS qualifies prospects, drafts outreach, and plugs into your entire Google Workspace.
