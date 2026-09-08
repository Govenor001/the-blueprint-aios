# Day 6 — The Command Wing: Your AIOS in Your Pocket

*Floor 4 begins. Today you text your AIOS from your phone — from the couch, the car, the school run — and it answers. The bridge is already running as a service on the server; today you connect and verify it. ~30 minutes.*

**By the end of Day 6:** you send a message from your phone and your AIOS answers — text and voice.

---

## Why connection-first

The magic of Day 6 is the conversation, not another build. The bridge is already installed on the server. You connect Telegram, confirm the owner gate, send a text and a voice note, and verify that the response and activity record behave correctly.

## Step 1 — Create and connect Telegram

In Telegram, open **@BotFather**, send `/newbot`, and copy the bot token. In Mission Control, open Connections and add the token. Message the new bot once so the server can identify your chat.

## Step 2 — Run the pre-flight check

Open the dashboard health check and confirm the Telegram bridge is connected. It verifies the bot token with Telegram and confirms that the server can reach the AI engine.

It verifies your bot token with Telegram, confirms the `claude` CLI is installed, and tells you whether voice notes are on (they are if your Day-3 `GROQ_API_KEY` is in `.env`). Fix anything it flags — it tells you exactly what.

## Step 3 — Lock the bridge to you

Message your bot from your **phone**. The server records your **chat id**; add that ID in Mission Control and refresh the bridge. From this moment the bridge answers *only you* — anyone else who finds your bot gets silence.

## Step 4 — The moment

Message your bot: *"Are you working?"*

Watch the activity panel update, and the reply land on your phone. Then ask it something real — *"what should I focus on tomorrow?"* — and it answers from everything it learned this week. **Screenshot that exchange.** This is the one everyone remembers posting.

## Step 5 — Voice notes

Send your bot a **voice message**. It transcribes what you said (Groq's free Whisper) and answers it. Now you can talk to your AIOS while you drive.

## Verify the server handoff

The server is already the home of this bridge. If you use a Claude subscription, complete the headless `claude setup-token` step from Day 0. If you use Bedrock, verify the AWS model route and billing settings. The challenge does not ask students to build or host the bridge; it asks them to connect, personalize, and verify it.

---

## Adapt-to-you note

This is identical for everyone — it's infrastructure, not content. Whatever your business, the payoff is the same: your AIOS, doing your work, answering in your pocket.

## Done when

You send a message from your phone and get a real answer back — text and voice — and the bridge is locked to your chat id.

## Proof of build

Post a screenshot of a **real conversation with your AIOS on your phone.** Film the moment if you can.

## Tomorrow

Day 7 — the finish line. Schedules that run without being asked, your inspection score, and your certification.
