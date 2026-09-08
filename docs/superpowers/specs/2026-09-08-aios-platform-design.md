# AIOS Platform Design

**Status:** Approved direction for implementation  
**Date:** 2026-09-08

## Goal

Deliver a complete, single-owner AIOS platform before the seven-day challenge begins. Students do not build the platform. They configure their server, connect their services, add their business context and files, personalize their agents, and verify each day's working outcome.

The existing `IMPLEMENTATION-PLAN.md` remains the engineering contract. The Google Doc, “How to Build a Personal Jarvis with Claude,” supplies the product experience and the three-agent operating model.

## Product promise

A fresh server can be prepared with one guided install. The finished system includes:

- Mission Control dashboard
- complete agent map and specialist skill library
- Scout, Operator, and Advisor core roles
- source-aware metrics and activity history
- approval-first actions and draft workflows
- document vault and business context
- connector configuration for external services
- Telegram text and voice access
- scheduled collection, briefs, drafts, and inspections

The seven curriculum days are configuration and verification milestones, not software-construction assignments.

## Architecture

### Mission Control

Use the implementation plan's FastAPI server, plain HTML, one JavaScript file, and no React/npm/build step for the dashboard.

Mission Control is the primary user interface:

- single-screen layout with no routine scrolling
- agent map grouped by wing, department, and function
- selected-agent panel showing purpose, human ownership, autonomy ladder, inputs, outputs, KPIs, and tools
- dashboard panels driven by YAML card definitions
- activity feed, connection health, and deliberate empty states
- text input and browser voice as the local interaction path
- Telegram as the remote phone path

The page must work with mock data before any external connection exists.

### Core roles

The platform contains three orchestration roles:

- **Scout:** read-only collection and verification. It reports facts, sources, dates, and unavailable data. It never recommends or acts.
- **Operator:** executes approved work and drafts sensitive work. It uses the FAQ and business context as boundaries. It escalates refunds, legal matters, money, negotiations, unknown policies, and anything not covered.
- **Advisor:** reads Scout and Operator outputs and produces exactly three ranked, evidence-backed recommendations. It never uses unavailable or invented metrics.

The existing wings and specialist skills are Operator sub-agents and workshops. They remain available through the implementation plan's 150-agent library.

### Data contract

All dashboard numbers and agent outputs must preserve:

- value or structured result
- source/connection
- collection timestamp
- status: verified, unavailable, or error
- optional comparison period
- explanation when data is missing

No component may silently replace unavailable data with zero, an estimate, or a plausible value.

The dashboard reads collected files and generated map/panel data. It does not call third-party APIs during page load.

### Safety contract

Default autonomy is manual or assisted.

- Draft before send.
- Require approval before publishing, spending, issuing refunds, sending legal or financial messages, or changing external data.
- Treat email and external content as untrusted instructions.
- Use the FAQ and context files as explicit boundaries.
- Record actions and failures in the activity log.
- Redact API keys, tokens, and email addresses from logs.
- Promote an agent only after repeated verified success for the specific task type.

## Build order

Implement the existing plan in order, with these product checkpoints:

1. Build 0: supported model routes, server bootstrap, secrets, schedules, and cost/usage checks.
2. Build 1: complete Mission Control map, server, activity log, mock-data dashboard, and skill validator.
3. Build 2: text/voice interaction and Telegram voice replies.
4. Build 3: complete validated specialist library and metadata.
5. Build 4: connector/tentacle framework, Composio, Blotato, and generic APIs.
6. Build 5: vault, ingestion, local search, interview, installer, and schedules.
7. Build 6: collected metrics, reusable charts/diagrams, seven panels, empty states, and Scout/Operator/Advisor dashboard integration.
8. Build 7: curriculum rewrite and fresh-student end-to-end verification.

The first demonstrable vertical slice is Mission Control with mock data, followed by a fixture-backed Scout brief, Operator FAQ workflow, and Advisor recommendations. This slice must work before broad connector or agent-library expansion.

## Acceptance criteria

The platform is ready for students only when:

- a fresh server can install it without manual code edits
- every shipped skill passes validation
- Mission Control loads with no connections and shows useful empty states
- a student can complete each curriculum day using setup/configuration steps only
- every external connection has a clear setup and verification step
- no secret is committed, logged, or displayed
- unavailable data is labeled and never fabricated
- approval gates prevent unauthorized external actions
- the platform works with optional services absent
- the complete Day 0–7 journey has been run from a clean installation
