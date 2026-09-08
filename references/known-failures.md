# Known failures — the tell and the fix

These are the failures that actually happen when you build this kit, catalogued from running the production system it's modeled on. `/rescue` reads this. Each entry: the tell (how you know it's this one) and the fix.

---

## Scheduled jobs never run — "it worked when I ran it by hand"
**Tell:** a cron job produces no output and no error; running the exact command manually works fine. The cron log shows nothing, or `source: not found`.
**Cause:** cron runs `/bin/sh` (dash), not bash. A line using `source .env` dies before your script starts.
**Fix:** add `SHELL=/bin/bash` as the first line of your crontab (`crontab -e`), or replace `source` with `. ` (dot). Safe to apply.

---

## API returns 401 — "unauthorized"
**Tell:** every call to one service fails with HTTP 401, even calls that used to work.
**Cause:** the API key is wrong, revoked, or expired.
**Fix:** this needs you — get a fresh key from the service dashboard and update it. If the service is optional, switch to the free fallback: transcription → Groq Whisper, LLM → your Claude token or Bedrock, news → Google News RSS.

---

## API returns 402 — "out of credit / balance exhausted"
**Tell:** HTTP 402, message about topping up billing. The code is fine; the account is empty.
**Cause:** a paid API ran out of credit.
**Fix:** either top up (your call — it's billing), or move to the free alternative. This kit is built so every paid service has a free substitute. Also add a back-off so you're not hammering a dead API every few seconds.

---

## API returns 403 — "not available for this account"
**Tell:** HTTP 403 that mentions access or availability, not auth. The credential is valid (other calls work), the specific resource isn't enabled.
**Cause:** the model/feature isn't granted on your account (common with cloud LLM providers).
**Fix:** enable it in the provider console, or repoint to a model that *is* enabled. List what's available first, then pick from that list — don't guess model IDs.

---

## Posts/actions blocked by a bot wall — 403 HTML, "request blocked"
**Tell:** reads succeed, writes fail with an HTML 403 (CloudFront / Cloudflare), regardless of headers.
**Cause:** the platform doesn't allow automated writes — that block *is* their policy, and working around it usually violates their terms and risks your account.
**Fix:** use the platform's official API or its official Zapier/integration route if one exists. If there isn't one, this task's ceiling is **draft-and-notify**: your AIOS prepares the post and drops it in your Telegram, you publish with one tap. That's the honest version of "automated."

---

## Newsletter/broadcast won't send — 403 on create
**Tell:** the send call 403s with a permissions message even though the key authenticates.
**Cause:** the provider's free plan blocks API-created broadcasts.
**Fix:** move to a provider whose free tier allows API sends (e.g. Resend Broadcasts), and verify your sending domain (SPF/DKIM) so mail lands in the inbox, not spam.

---

## Public tunnel URL stopped working
**Tell:** webhooks 502/timeout; the URL that worked yesterday is dead. No new inbound lines in the log.
**Cause:** a throwaway tunnel URL rotated (they change on restart).
**Fix:** pull the new URL from the tunnel log, update wherever it's referenced. For production, use a named tunnel on a domain you own so it never rotates.

---

## Nothing to work with — "no signals / empty queue"
**Tell:** a content or intel job runs but produces nothing; the input file is empty.
**Cause:** the upstream data source is down or returned nothing, and there's no fallback.
**Fix:** add a fallback source so the job never runs dry (free news RSS is the reliable floor), and an alert so you know when the primary went quiet.

---

## Telegram bridge is silent — messages get no reply
**Tell:** you text the bot, nothing comes back; the bridge terminal shows nothing (or isn't running).
**Cause:** in order of likelihood: the bridge process isn't running; `.env` wasn't loaded into that terminal (`set -a && . ./.env && set +a`); `TELEGRAM_CHAT_ID` is a different id than the phone you're texting from; two bridge processes are fighting over updates (Telegram hands each update to only one).
**Fix:** run `python3 scripts/bridge.py --check` and read what it says. Kill duplicates (`pkill -f bridge.py`), reload the env, restart. If the bridge replies "your chat id is …", put that exact number in `.env`.

---

## Cloud "free tier" instance can't be created — "out of capacity"
**Tell:** the provider accepts your signup but every attempt to launch a free instance fails with a capacity error.
**Cause:** free-tier capacity in popular regions is chronically oversubscribed; this is normal, not something you misconfigured.
**Fix:** don't burn a day fighting it. A ~$5/mo VPS (Hetzner, DigitalOcean, etc.) launches in five minutes and is the boring, reliable choice. Free tiers also reclaim idle instances — read the provider's policy before trusting one with your AIOS.
