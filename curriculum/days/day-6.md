# Day 6 — Move In: The Command Wing

*Floor 4 (Autopilot) begins. Today your AIOS stops living on your laptop and moves onto a 24/7 cloud server — and into your pocket, where you text and voice-note it from anywhere. This is the day it becomes real. ~50 minutes.*

**By the end of Day 6:** your AIOS runs on a free always-on server, and you can message it from your phone — laptop closed — and get a real answer back.

---

## Why this is the day everyone remembers

Up to now, your AIOS only works when your laptop is open. Today that changes. There's a specific moment — you send the first message from your phone and the reply comes back — where it clicks that you actually built this. Screenshot that moment.

## Step 1 — Connect to your server

You created an Oracle Always-Free Ubuntu server on Day 0. Connect to it (from your terminal, using the SSH key you saved):

```
ssh -i /path/to/your-key ubuntu@YOUR_SERVER_IP
```

If it connects, you're in. (First-time SSH quirks and the exact command are in the day's video — this is the one step worth watching over reading.)

## Step 2 — Put your AIOS on the server

Copy your AIOS folder up to the server and install what it needs. Your AIOS can walk you through this — ask it:

> Walk me through deploying my AIOS to my Oracle server at [IP]. I want it running 24/7.

The deploy sets up Python, your keys (as environment variables — never hard-coded), and the services that keep running after you disconnect.

## Step 3 — Create your Telegram bot connection

You made a bot with @BotFather on Day 0 (you have its token). Now connect it:

> My Telegram bot token is [token] and my chat ID is [id]. Set up the Telegram bridge so I can message my AIOS from my phone.

To find your chat ID if you didn't save it: message your bot once, then your AIOS can fetch it, or use @userinfobot.

## Step 4 — The moment: text it from your phone

Open Telegram on your **phone**. Message your bot: *"Are you working?"*

The reply comes back — from a server, not your laptop. **Close your laptop lid. Message it again. It still answers.** That's an operating system now, not an app you open.

## Step 5 — Turn on voice notes

Send your bot a **voice message** from your phone. It transcribes what you said (using Groq's free Whisper) and acts on it. If you set up ElevenLabs, it can reply in a real voice too. Now you can talk to your AIOS while you drive.

---

## Adapt-to-you note

This is identical for everyone — it's infrastructure, not content. Whatever your business, the payoff is the same: your AIOS, doing your work, reachable from your pocket, running while you sleep. The server is free, the bot is free, the transcription is free.

## Done when

You send a message from your phone with your laptop closed and get a real answer — text and voice.

## Proof of build

Post a screenshot of a **real conversation with your AIOS on your phone.** This is the one everyone remembers posting. Film the moment if you can.

## Tomorrow

Day 7 — the finish line. Schedules that run while you sleep, your inspection score, and your certification.
