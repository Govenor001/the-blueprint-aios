---
name: rescue
description: Self-repair. Use when something in the AIOS breaks — a skill errors, a cron job didn't run, an API returns 401/403/402, a post didn't go out, the newsletter didn't send. Reads the error, checks the known-failures database, fixes what it safely can, and tells the user exactly what to paste for help if it can't.
---

## What this does

When something breaks, the user runs `/rescue` instead of staring at a stack trace. It diagnoses the failure, matches it against `references/known-failures.md`, applies a safe fix if there is one, and — if it can't fix it — writes a clean, copy-paste-ready help request the user can drop into the community. Almost nobody ships automated tech support *inside* the product. This is why students don't quit on Day 2.

## Step 1 — Gather the evidence
Ask what broke, or read it if they pasted it. Then look for the real signal:
- The error text, exit code, or HTTP status
- The relevant log (`cron.log`, a service log, the skill's own output)
- Whether the thing ran at all (check the schedule / last-run timestamp) vs. ran and failed

Don't guess from the symptom. A "no posts went out" can be a dead API key, a scheduler that never fired, or a content step that produced nothing — three different fixes.

## Step 2 — Match against known failures
Read `references/known-failures.md` and match by signal. It catalogs the failures that actually happen when you build this kit — dead keys, cron shell mismatches, WAF blocks, plan limits, out-of-credit APIs, tunnel rotation. Each entry has the tell and the fix.

## Step 3 — Fix or escalate
- **Known + safe to fix** (restart a service, repoint a model, add a missing env var, switch to a free fallback): apply it, then verify it actually worked — re-run the thing and read the output. Never claim fixed without evidence.
- **Known but needs the user** (a billing top-up, an OAuth login, a new API key): tell them exactly what to do, in one or two steps.
- **Unknown:** write a help request with the error, what they were doing, what they've tried, and the relevant log lines — ready to paste. A good bug report gets answered; a vague one doesn't.

## Step 4 — Log it
Append a one-line entry to `decisions/log.md`: what broke, what fixed it. Next time it's a known failure.

## Rules
- **Diagnose before you touch anything.** Read the actual error, not the symptom.
- **Safe fixes only, autonomously.** Restarts, repoints, fallbacks, missing env vars — yes. Deleting data, rotating live credentials, changing billing — never without asking.
- **Verify every fix** by re-running and reading the output. Evidence, not assertion.
- **When you escalate, make it copy-paste ready.** The user shouldn't have to write the bug report.
