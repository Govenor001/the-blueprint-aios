---
name: connect-blotato
description: Connect Blotato for social publishing after the owner confirms the paid-plan and trial-ending warning.

metadata:
  wing: comms
  department: Connections
  function: Social Publishing
  replaces: Copying social content into multiple platforms by hand.
  the-human: The owner confirms billing, selects accounts, and approves every post before publishing.
  ladder:
    manual: Show the commands and let the owner run the read-only account check.
    assisted: Register the connection and prepare drafts for approval.
    autonomous: Schedule only after the owner has reviewed repeated successful runs.
  trigger: The owner asks to connect Blotato or publish through Blotato.
  outputs:
    - Connection status and connected account names
    - Approval-ready publishing plan
  kpis:
    - Accounts discovered
    - Drafts awaiting approval
  tools: [claude, blotato]
  requires-context: [connections.md]
  model: smart
  autonomy: assisted
  scaffolding-phase: 2
---

## What this does
Connects the official Blotato MCP server while keeping the API key in the local environment.

## Inputs it reads
- connections.md
- The owner's confirmation that creating a key ends the free trial and may start billing

## Execution
1. Warn plainly that generating a Blotato API key requires a paid plan and may end the free trial.
2. Wait for the owner to confirm before asking for a key.
3. Store the key only as BLOTATO_API_KEY in the local environment file, quoted.
4. Register the official MCP endpoint and test with a read-only account listing.
5. Report account names and leave publishing in draft mode.

## Rules
- Never create a key before confirmation.
- Never put a key in markdown, JSON, activity logs, or chat.
- Never publish without explicit approval.
- If the connection cannot be verified, say UNAVAILABLE.
