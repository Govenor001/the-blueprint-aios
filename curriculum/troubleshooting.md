# Stuck? Start here — the top snags, day by day

Each entry: how it looks, what it is, what to do. If yours isn't here,
run `/rescue` in Claude Code — it reads the error and either fixes it
or writes your help post for you.

## Day 0
- **`claude: command not found`** — Claude Code isn't installed or your terminal needs reopening after install. Redo section 1 of the services guide, open a *new* terminal, retry.
- **BotFather never sends a token** — the bot's username must end in `bot` (e.g. `maya_aios_bot`). Try `/newbot` again.
- **"Where do I paste the token?"** — into the `.env` file in the kit folder, on the `TELEGRAM_BOT_TOKEN=` line, no quotes, no spaces.

## Day 1
- **The answers feel generic afterwards** — your Q2 voice samples were typed, not pasted, or too short. Paste two real sent emails/posts into `blueprint-intake.md` and re-run `/blueprint`.
- **No business data to give it?** — run the whole challenge as the demo business: `sample-data/demo-business.md`.

## Day 2
- **Posts don't sound like you** — add one more raw sample to `references/voice.md` and say "match this register, not a house style." Two rounds usually locks it.
- **It writes about the wrong niche** — your Q1 answer was vague. Re-run `/blueprint` and name the customer precisely.

## Day 3
- **`GROQ_API_KEY` errors** — you created the key but didn't load it: `set -a && . ./.env && set +a` in the same terminal you run the engine from.
- **Engine returns junk/off-topic items** — keywords too broad ("AI", "business"). Use 5–8 phrases your *customers* would search. Tuning this over a few days is the skill.
- **Reddit shows as a source error** — normal; Reddit rate-limits scripts. The other two sources carry the brief.

## Day 4
- **Newsletter lands in spam** — domain isn't verified yet. Resend → Domains must say **Verified**; if pending, confirm the SPF and DKIM records at your registrar and give it a few hours.
- **`npm install` fails in video-presets** — check `node --version` is 18+. Corporate/VPN networks sometimes block the headless-browser download; retry off VPN.
- **Render is slow** — the first render downloads a browser; later renders are much faster.

## Day 5
- **Composio stuck at "initializing"** — you didn't finish the Google consent to the success screen. Reconnect and click through to "connected".
- **Claude Code can't see Composio** — `.mcp.json` missing or still has the placeholder URL; follow `references/composio-setup.md` step 3, then *restart Claude Code in this folder*.
- **No leads to qualify** — use `sample-data/leads.csv`.

## Day 6
- **Bridge silent** — see "Telegram bridge is silent" in `references/known-failures.md` (short version: `--check`, reload `.env`, kill duplicates).
- **Voice notes answer with a complaint about Groq** — put your Day-3 `GROQ_API_KEY` in `.env` and restart the bridge.

## Day 7
- **Cron job never fires** — the classic. `SHELL=/bin/bash` must be the first crontab line, and the cron line must `cd` into the kit folder. See the first entry in `references/known-failures.md`.
- **Cron fires but nothing reaches Telegram** — `TELEGRAM_CHAT_ID` isn't in `.env`, or the env-load isn't in the cron line. Copy the Day 7 line exactly and only change the path and time.
- **Laptop was asleep at 7am** — schedules run while the machine is awake this week. Pick a time it's open, or take the post-challenge Go-24/7 module.
