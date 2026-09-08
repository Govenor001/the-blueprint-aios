# Student acceptance checklist

Run this at the end of each day. The point is to verify the platform and configure the student's own systems, not to write platform code.

## Day 0 — access

- [ ] Claude subscription or approved Bedrock route is authenticated.
- [ ] The server-side dashboard password is set.
- [ ] No API-key override is present.
- [ ] The dashboard starts only with authentication.

## Day 1 — foundation

- [ ] The onboarding interview has completed the required context files.
- [ ] The AIOS can describe the owner's business without being re-told.
- [ ] Missing context is reported instead of guessed.

## Day 2 — content

- [ ] A content-week draft was produced.
- [ ] The owner reviewed the voice and CTA.
- [ ] Nothing was published automatically.

## Day 3 — intelligence

- [ ] A watchlist exists.
- [ ] A brief contains sources and retrieval times.
- [ ] Unavailable sources say UNAVAILABLE.

## Day 4 — operator safety

- [ ] A newsletter or inbox draft exists.
- [ ] The owner can identify exactly what would be sent.
- [ ] No send or publish occurred without approval.

## Day 5 — connections

- [ ] At least one connector passed a read-only test.
- [ ] The key exists only in the local environment file.
- [ ] The dashboard reports missing connections clearly.

## Day 6 — command

- [ ] Telegram is locked to the owner's chat ID.
- [ ] A text request returns a response.
- [ ] Voice is tested only if a transcription key is configured.

## Day 7 — proof

- [ ] python scripts/student_check.py passes.
- [ ] The dashboard map loads with Basic auth.
- [ ] The activity feed contains a real run.
- [ ] A metric file exists and records source, timestamp, and status.
- [ ] The owner has explicitly approved any schedules to enable.

A failure is a setup item to fix, not a reason to rebuild the platform.
