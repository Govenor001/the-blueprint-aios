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
**Cause:** the platform's bot protection blocks non-browser writes.
**Fix:** route the write through a real headless browser (Playwright) using your session cookies, after the page's challenge completes. Reads can stay on the fast path.

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
