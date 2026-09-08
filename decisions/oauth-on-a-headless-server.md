# OAuth on a headless server

## Decision

Keep the browser step on the owner's device and keep the resulting credential on the
server. Do not ask students to run a browser on the server or paste OAuth secrets into a
chat message.

## Claude authentication

For a Claude subscription, run `claude setup-token` as the `aios` user. The CLI prints a
first-party approval link; the owner opens that link in a browser, approves it, and pastes
the returned code into the server session. Claude Code owns the resulting credential. AIOS
does not write it to `.env` and rejects `ANTHROPIC_API_KEY`.

For the owner’s Bedrock route, set the AWS region and Bedrock model route in the systemd
environment. The live Jarvis box was verified with `CLAUDE_CODE_USE_BEDROCK=1`,
`AWS_REGION=us-east-1`, and the pinned Sonnet inference profile; a bounded
`claude -p` invocation returned successfully through Bedrock.

## Google and other connectors

Use the connector’s official browser consent flow on the owner’s device, then store only
the resulting server-side environment values or MCP session configuration. The connection
skill must perform one read-only verification and record the source, timestamp, and result.
Writes, sends, publishes, spending, and deletes remain approval-gated.

## Failure behavior

If consent is incomplete, the dashboard says `needs_setup` or `UNAVAILABLE`. It does not
guess that a connection exists and does not expose credential values in the dashboard or
activity log.
