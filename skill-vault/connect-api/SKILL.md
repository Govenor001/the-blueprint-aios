---
name: connect-api
description: Connect a service through its OpenAPI description with a strict operation whitelist.

metadata:
  wing: comms
  department: Connections
  function: OpenAPI Bridge
  replaces: Writing a new custom integration for every service.
  the-human: The owner chooses the service, key, and small set of permitted operations.
  ladder:
    manual: Inspect the spec and approve a whitelist.
    assisted: Register the bridge and run one read-only operation.
    autonomous: Run approved read-only operations on a schedule.
  trigger: The owner asks to connect a service with an OpenAPI specification.
  outputs:
    - Cached specification
    - Whitelisted MCP registration
    - Read-only verification result
  kpis:
    - Operations whitelisted
    - Read-only checks passed
  tools: [claude, webhook]
  requires-context: [connections.md]
  model: smart
  autonomy: assisted
  scaffolding-phase: 2
---

## What this does
Turns a service's OpenAPI description into a small, reviewable MCP connection.

## Inputs it reads
- The service documentation or api.apis.guru directory
- connections.md

## Execution
1. Find the official specification, then use the public directory only as a fallback.
2. Show the owner the available operations and select no more than twenty.
3. Ask for the API key and store it only in the local environment file.
4. Register mcp-openapi-proxy with the specification URL, auth settings, and TOOL_WHITELIST.
5. Cache the specification in vault/specs/ and run one read-only operation.
6. Report the source, timestamp, operation, and result.

## Rules
- Never register a service without a whitelist.
- Never call a write operation during setup.
- If auth or the spec is uncertain, say UNAVAILABLE and stop.
