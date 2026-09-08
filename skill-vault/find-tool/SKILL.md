---
name: find-tool
description: Find a small shortlist of MCP tools for a requested capability without overwhelming the owner.

metadata:
  wing: comms
  department: Connections
  function: Tool Discovery
  replaces: Searching thousands of integrations and still not knowing which one is safe.
  the-human: The owner chooses which connection to test and approve.
  ladder:
    manual: Review a shortlist and compare sources.
    assisted: Prepare a read-only setup plan.
    autonomous: Refresh the shortlist when a connected tool changes.
  trigger: The owner asks what tool can connect a service or capability.
  outputs:
    - At most five ranked connection options
    - Source, tier, and setup warning for each
  kpis:
    - Shortlists delivered
    - Options tested read-only
  tools: [claude, github]
  requires-context: [references/mcp-shortlist.md]
  model: fast
  autonomy: assisted
  scaffolding-phase: 2
---

## What this does
Searches the curated shortlist first, then the public MCP registry only when needed.

## Inputs it reads
- references/mcp-shortlist.md
- The public MCP registry when the shortlist has no match

## Execution
1. Understand the capability and the service the owner wants.
2. Search the shortlist and rank the closest official or maintained options.
3. If nothing matches, search the registry and keep at most five results.
4. For each result, show source, connection tier, permissions, and first read-only test.
5. Wait for the owner to choose before connecting anything.

## Rules
- Never show thousands of results.
- Never recommend an unverified write-capable connection as safe.
- If no trustworthy option is found, say UNAVAILABLE.
