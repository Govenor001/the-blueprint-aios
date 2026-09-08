# The AIOS Agent Spec

Every agent in the vault carries a structured spec in its YAML frontmatter.

**One source of truth.** The dashboard, the map, and the docs all read the same
file Claude executes. There is no separate data file to drift out of sync — if an
agent changes, the map changes.

## The frontmatter contract

Claude Code only permits a fixed set of top-level frontmatter keys
(`name`, `description`, `argument-hint`, `compatibility`, `license`, `metadata`,
`disable-model-invocation`, `user-invocable`). **Everything in our spec therefore
nests under `metadata:`** — that key exists for exactly this, and anything placed
at the top level throws a validation warning.

```yaml
---
# --- identity (Claude reads these) ---
name: qualify
description: >
  One paragraph. What it does + the trigger phrases a user would actually say.
  This is what Claude matches on, so write it for recall, not for marketing.

metadata:
  # --- placement on the map ---
  wing: growth              # intelligence | content | growth | comms | command |
                            # back-office | build
  department: Sales         # the org-chart column it renders under
  function: Qualification   # the sub-group within that column

  # --- the pitch (renders on the agent's card) ---
  replaces: >
    The specific unglamorous pain this kills. Name the failure, not the feature.
  the-human: >
    What the owner still owns after this agent runs. Directing, not doing.

  # --- the autonomy ladder ---
  ladder:
    manual:     What this looks like when a person does it by hand today.
    assisted:   The agent drafts, a human approves before anything leaves.
    autonomous: It runs end to end and only escalates real judgment calls.

  # --- the mechanics ---
  trigger: What starts it — an instruction, a schedule, or an inbound event.
  outputs:                  # the artifacts it hands back
    - Ranked lead table
    - "Start here" summary
  kpis:                     # how you know it worked
    - Leads scored per run
    - A-list conversion rate
  tools: [claude, sheets]   # keys from tool-registry.md
  requires-context:         # context files it must read to be any good
    - context/about-business.md

  # --- cost ---
  model: smart              # fast | smart | deep  (a tier, never a product name)

  # --- rollout ---
  autonomy: assisted        # where THIS build sits on the ladder today
  scaffolding-phase: 1      # which day of the challenge installs it
---
```

## Choosing `model`

The owner pays for every run, so this field is real money, not a preference.

| Value | Use it for |
|---|---|
| `fast` | High volume, low judgment. Triage, sorting, extraction, tagging. |
| `smart` | The default. Nearly every agent belongs here. |
| `deep` | Genuinely hard reasoning where a wrong answer costs the owner something. Strategy, the morning brief, anything that weighs trade-offs. |

If you cannot say why an agent needs `deep`, it does not need `deep`.

**Why a tier and not a model name.** `config/models.yaml` maps these three words to real
models, once, for whichever route the box is on — a Claude subscription, Bedrock, or the
advanced cheap-model module. Writing `sonnet` in a skill file hardcodes one route into one
agent, so a route switch silently leaves that agent behind. **The validator rejects a
product name here.**

Agents are Tier 2 by definition: they run inside Claude Code. Tier 0 work (metrics, charts)
is plain Python and Tier 1 work (document search) is a local model called from our own
scripts — neither is a skill, so neither uses this field.

## Rules

- **`replaces` names a failure, not a feature.** "Mail-merge blasts that read like
  mail-merge blasts" beats "improves personalization."
- **`the-human` is non-negotiable.** Every agent states what stays yours. An agent
  with nothing left for the human is either lying or dangerous.
- **All three ladder rungs get written**, even for agents shipped at `assisted`.
  The ladder is the teaching device — it shows the owner where they are and what's
  next.
- **`autonomy` is honest.** If it drafts and waits for approval, it is `assisted`.
  Do not label an approval-gated agent `autonomous` to make the map look better.
- **`kpis` must be measurable from the agent's own output.** No vanity metrics.
- **`requires-context` is enforced.** If the context file is missing, the agent
  says so and stops rather than inventing a business it knows nothing about.
- **An agent never invents a number.** If a metric it wants was not collected, it
  names the missing connection and stops. A plausible fake figure is worse than a
  blank, because the owner will act on it.

## Why frontmatter and not a data file

Altari's map ships a 188 KB `data.ts` with 120 role descriptions and no execution
layer — the descriptions and the agents are separate things, so the map is a
brochure. Putting the spec in frontmatter means the thing that renders on the
dashboard *is* the thing that runs. A generated map cannot lie about what the
system does.

## The body

Frontmatter is the spec. The body is the build. Keep the existing shape:

```markdown
## What this does
One paragraph of plain-English purpose.

## Inputs it reads
The files, lists, and context it pulls from.

## Execution
Numbered steps. This is the part Claude follows.

## Rules
The guardrails. What it must never do.
```
