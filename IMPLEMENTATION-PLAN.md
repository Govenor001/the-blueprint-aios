# AIOS — Build Plan

**Who this is for:** a junior dev, or a cheap AI model doing one task at a time.

**How to use it:** do the tasks in order. Each task has **DO** and **CHECK**.
If CHECK fails, fix it before moving on. Never skip a CHECK.
If a task asks you to decide something, stop and ask. Everything is already decided.

There are seven builds, numbered 0 to 6.

| Build | What it is | Plain words |
|---|---|---|
| 0 | The Brain | Three tiers: free Python, a free local model, and Claude on a flat monthly plan. Never the per-token API. Do this first. |
| 1 | The Mind | A web page showing every agent. Click one, see what it does. |
| 2 | The Voice | You talk to it. It talks back. |
| 3 | The Agents | Get to 150 agents. Download the ones that exist, write the rest. |
| 4 | The Tentacles | Paste any API key. It can now use that service. |
| 5 | The Vault | Their keys and company documents, locked on their own server. |
| 6 | The Panels | Every section shows their real numbers, as charts and diagrams. Ask for one in plain English and get it, on the dashboard or on your phone. |

Builds 1, 2, 4, 5 are the machine. Build 3 is the content. Build 6 is the face.

**Build 3 is the longest. Build 6 is the one that sells it.** Build 1 proves the system
exists; Build 6 is the only part that shows the owner their own business. Do not treat it
as polish to do at the end, and do not let it balloon either. It has exactly one pattern,
stated in **"The rule that makes this possible"** at the top of Build 6.

---

# Start here. Do these four things before anything else.

The builds run in order, 0 to 6, but four items are out of order on purpose because they
gate everything else or they take calendar time you do not have spare.

**1. Read Build 0 all the way through before you write a line of code.** It is the auth,
cost and tier model that every other build assumes. Skip it and you will build 150 agents
that silently run on the wrong model, and you will not find out from an error message.

**2. Build the validator, Task 1.2, before converting a single agent.** It is one file and
maybe an hour. Build 3 converts about 140 files against it. Converting them first and
checking later means re-opening 140 files. **This is the highest-leverage hour in the plan.**

**3. Start the week-long usage measurement in Task 0.3 on day one.** It takes seven days of
wall-clock time that cannot be compressed: one server, the cheapest plan you intend to
recommend, the default schedule switched on, recording real usage. Every day you delay is a
day the plan recommendation stays a guess. **The subscription usage limits colliding with
scheduled agents is the single most likely cause of refunds in week two** — see Task 0.3.

**4. Prototype the headless OAuth question in Task 4.5 early.** It is the one genuine unknown
left in this plan. If it does not work, Build 4 loses a tier and that is a scope decision for
the owner, not something to discover on the day it is needed.

**Two standing rules for the whole job.** Never skip a CHECK — they exist because each one
has already caught a real failure. And nothing ships that has never been run once by a human
who read the output: a missing agent costs a feature, a confidently wrong agent costs the
customer.

---

# What you are building

Read this whole section before you write a line of code. If you build the tasks without
understanding the finished thing, you will build five parts that do not add up.

## In one paragraph

A business owner rents a five-dollar-a-month server. One command installs their AIOS on
it. They open a web address and see a map of about 150 agents grouped by department,
like an org chart of staff they now have. They spend seven days telling it about their
business and switching agents on. After that it runs on its own. They talk to it from
Telegram, by typing or by voice, and it answers in voice. It reads their email, their
calendar, their documents, and any other software they paste a key for. Everything they
own stays on their server. We never hold their keys or their files.

## What they see on screen

One page. This is the product's face and it is what goes on the sales page, so it has
to look deliberate.

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  YOUR AIOS          151 agents · 118 assisted · 33 autonomous      ● ● ●     │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  INTELLIGENCE   CONTENT       GROWTH      COMMS    BACK OFFICE   BUILD   ··· │
│  ┌────────────┐   ┌────────────┐   ┌────────────┐   ┌──────────┐ ┌─────────┐ │
│  │ Intelligence│   │ Marketing  │   │ Sales      │   │Back Office│ │ Finance │ │
│  │            │   │            │   │            │   │          │ │         │ │
│  │ ◐ watch    │   │ ◐ newsletter│   │ ◐ qualify ◀│   │ ◐ inbox  │ │ ○ invoice│ │
│  │ ● brief    │   │ ◐ content-wk│   │ ◐ outreach │   │ ● plan-day│ │ ○ expenses│
│  │ ○ digest   │   │ ● socials  │   │ ◐ followup │   │ ◐ triage │ │         │ │
│  └────────────┘   └────────────┘   └────────────┘   └──────────┘ └─────────┘ │
│                                                                              │
│  ○ manual   ◐ assisted   ● autonomous                                        │
├──────────────────────────────────────────────────────────────────────────────┤
│  qualify                                                        [ Run now ]  │
│                                                                              │
│  REPLACES   Working a lead list top to bottom because nothing tells you       │
│             which name is worth the call.                                    │
│  STILL YOURS You decide which conversations you want. It only ranks them.     │
│                                                                              │
│  WHERE IT IS    ○ manual  ▶ ◐ assisted ◀  ○ autonomous                      │
│                 Scores and ranks every lead with a reason. You pick who to    │
│                 open. Next rung: it drops the A-list straight into outreach.  │
│                                                                              │
│  HANDS BACK  Ranked table · A/B/C grouping · "Start here" top five           │
│  USES        [Claude] [Sheets]                                               │
├──────────────────────────────────────────────────────────────────────────────┤
│  CONNECTIONS                                                                 │
│  Gmail        Composio    ✓ connected      last read 6:04am                  │
│  Calendar     Composio    ✓ connected      last read 6:04am                  │
│  Blotato      own MCP     ✓ 3 accounts     last post yesterday 4:10pm        │
│  ManyChat     bridge      ⚠ key missing    set MANYCHAT_API_KEY              │
├──────────────────────────────────────────────────────────────────────────────┤
│  ACTIVITY                                                                    │
│  6:04am  brief      finished   3 sources, 1 thing needs you                  │
│  6:00am  inbox      finished   14 mail, 2 urgent, 2 drafts waiting           │
│  yesterday 4:10pm  socials    finished   posted to 3 accounts                │
└──────────────────────────────────────────────────────────────────────────────┘
```

Four things on that page and nothing else: **the map**, **the panel for whichever agent
you clicked**, **the connections**, **the activity feed**.

**Click a department name instead of an agent, and the middle band becomes that
department's numbers.** Same page, same frame, the panel swaps. This is what Build 6
builds and it is where the product stops looking like a file browser.

```
├──────────────────────────────────────────────────────────────────────────────┤
│  CONTENT                                            collected 14 minutes ago │
│                                                                              │
│  ┌─ Skool members ──────┐  ┌─ Engagement, 30 days ─────────────────────────┐ │
│  │                      │  │        ╭─╮                              ╭╮   │ │
│  │       1,284          │  │   ╭─╮ ╭╯ ╰╮        ╭──╮            ╭─╮ ╭╯╰╮  │ │
│  │       ▲ 37 this week │  │ ╭─╯ ╰─╯   ╰────╮ ╭─╯  ╰──╮   ╭─────╯ ╰─╯  ╰  │ │
│  │                      │  │─╯               ╰─╯       ╰───╯               │ │
│  │  from Skool          │  │ Aug 8                                  Sep 7  │ │
│  └──────────────────────┘  └───────────────────────────────────────────────┘ │
│                                                                              │
│  ┌─ Posts this week ────┐  ┌─ Views by platform, 30 days ──────────────────┐ │
│  │ Instagram  ████████ 8│  │  ── Instagram   42.1k    ▲ 18%               │ │
│  │ TikTok     █████   5 │  │  ── TikTok      31.6k    ▲  4%               │ │
│  │ LinkedIn   ███     3 │  │  ── LinkedIn     3.2k    ▼  9%               │ │
│  │  from Blotato        │  │  from Blotato                                 │ │
│  └──────────────────────┘  └───────────────────────────────────────────────┘ │
│                                                                              │
│  ┌─ Waiting for you ────────────────────────────────────────────────────────┐│
│  │ thursday-newsletter.md    newsletter    2 hours ago      [ Review ]      ││
│  │ launch-week-hooks.md      content-week  yesterday        [ Review ]      ││
│  └──────────────────────────────────────────────────────────────────────────┘│
├──────────────────────────────────────────────────────────────────────────────┤
│  ASK JARVIS   how are my Instagram views looking?                    [ ▶ ]   │
└──────────────────────────────────────────────────────────────────────────────┘
```

Ask the question in that bottom bar and the answer comes back as a chart plus two
sentences. Ask the same question from Telegram and the same chart arrives as a photo.

The map is generated from the agents' own files. Nobody types it by hand. That matters:
it means the page can never claim the system does something it does not do.

## A Monday morning, once it is finished

This is the story the product has to actually deliver. Every task in this plan exists to
make one line of it true.

- **6:00am.** Nobody is awake. The server runs the inbox agent. Fourteen emails come in,
  two need a human, it writes two draft replies and sends neither.
- **6:04am.** The brief agent reads the overnight sources and writes one page.
- **7:30am.** The owner picks up their phone and holds the microphone button in Telegram.
  "What do I need to know today." Eight seconds later their phone speaks the answer back
  in a voice.
- **7:32am.** They type "send the second draft." It sends that one and only that one.
- **9:00am.** They paste a lead list into Telegram. The qualify agent ranks it and names
  the top five with a reason for each.
- **11:00am.** They open the dashboard on a laptop, click an agent they have never used,
  read what it does, and press Run.
- **4:00pm.** They say "post this week's content." It posts to three social accounts and
  the activity feed shows all three.
- **Any time.** They drag four PDFs about their business into a folder. Next run, the
  agents know what is in them.

If a task in this plan does not serve one of those lines, it is not needed.

## What lives on their server

```
/opt/aios/
  .env          their API keys. chmod 600. the only place keys exist.
  app/          our code, the 150 agents, the dashboard
  vault/
    documents/  the company files they upload
    context/    what the agents actually read about their business
  var/          the activity log
```

Two processes run all the time: the Telegram bridge and the dashboard. A handful of
timers run agents on a schedule. That is the whole machine.

## What it is not. Do not build these.

A junior dev with initiative is the risk here, so this fence is part of the spec.

- **Not multi-user.** One owner, one server. No accounts, no sign-up, no teams.
- **Not hosted by us.** We never run their server or hold their keys. If a task tempts
  you toward a central service, you have misread it.
- **No mobile app.** Telegram is the phone app.
- **No agent builder UI.** Agents are markdown files. The dashboard reads them and never
  writes them.
- **No React, no npm, no build step** for the dashboard. One HTML file, one JS file.
  **This survives the charts.** We do not add a JavaScript charting library. Charts are
  SVG generated in Python, which is why the same chart can go to Telegram. See Task 6.2.
- **No database.** Files on disk. The activity log is a text file. This is deliberate:
  a non-technical owner has to be able to look at their own data. **This survives the
  metrics too.** Metric history is append-only JSONL, one file per card, which a person
  can open and read. If you ever feel you need SQLite, you have made a card too clever.
- **Nothing sends without asking.** No agent sends an email, posts, or deletes anything
  without showing the owner what it is about to do first.
- **No per-token API billing, anywhere, ever.** Not as a fallback, not as a default, not
  "just for testing". A customer box that sets `ANTHROPIC_API_KEY` is a bug, and the
  installer refuses to run when it finds one. See Build 0.
- **No local model in Tier 2.** Tier 1 is a local model doing narrow, checkable work.
  Running the *agents* on a self-hosted model needs an unsupported translation proxy and
  costs more in hardware than the subscription it replaces. Task 0.6 has the arithmetic.
  If you are tempted, read it, then don't.
- **No GPU, and nothing that needs one.** The target is a ~$5 box. Every choice in this
  plan is sized for 1 GB of RAM and no accelerator.

## Done means

A stranger rents a server, runs one command, spends seven days on the challenge, and
ends up with something that runs their morning without them. They can talk to it. They
can see everything it did. They can plug in their own tools. All of it is theirs, on
hardware they pay for, and they could delete us tomorrow and keep it.

---

## Before you start

```bash
cd /tmp/bp-check
git checkout -b build/aios
```

Read `references/agent-spec.md`. Then read `skill-vault/qualify/SKILL.md`.
Those two files are the pattern. Everything else copies them.

**Two mistakes everyone makes. Do not make them.**

1. In a skill's frontmatter, custom fields go **under `metadata:`**. Claude Code only
   allows these at the top level: `name`, `description`, `argument-hint`,
   `compatibility`, `license`, `metadata`, `disable-model-invocation`,
   `user-invocable`. Anything else there breaks the skill.
2. A YAML list item must **never start with a double quote**.
   Wrong: `- "Start here" summary`
   Right: `- '"Start here" summary'`

## "Agent" and "skill" are not the same thing. Read this.

Claude Code has two different mechanisms and they are easy to confuse.

| | **Skill** | **Subagent** |
|---|---|---|
| Lives in | `skill-vault/<name>/SKILL.md` | `.claude/agents/<name>.md` |
| Frontmatter | `name`, `description`, `metadata` | `name`, `description`, `tools`, `model` |
| Body is | a **procedure**. Numbered steps to follow. | a **persona**. "You are a senior sales engineer…" |
| Runs in | the current conversation | its own separate context window |
| Good for | a repeatable job with a defined output | a long open-ended job whose middle you do not want to read |

**What we ship: skills. Every single one.** There are no subagents in this product.

**What we call them to the customer: agents.** "151 agents" is the product language. It
is the right word for a business owner. Nobody buys a skill.

So inside this plan and inside the code, the word is **skill**. On the dashboard, the
sales page, and in anything the customer reads, the word is **agent**. One file, two
names, depending on who is looking.

**Why skills and not subagents.** The dashboard is generated from skill frontmatter, so
one mechanism means one source of truth. A skill also keeps its work in the owner's
conversation, which is what you want when the owner is watching from Telegram and needs
to approve a draft. A subagent hides its work and reports a summary.

**The one place to revisit this later:** long research jobs like market analysis, which
generate a lot of noise the owner does not want in their chat. Those are the honest case
for subagents. Do not build it in v1. Get 150 skills working first.

---

# BUILD 0 — The brain: how it connects, and what it costs

Do this first. Every other build assumes it works, and it is the one place where a wrong
choice costs the customer real money every month.

## The three tiers

**Not every job in this system needs a large language model, and the ones that don't are
where the money is saved.** Sort every piece of work into one of three tiers before you
write it. Getting a job into a lower tier is the highest-leverage optimisation in the whole
product, and it is free.

| Tier | Runs on | Cost | What belongs here |
|---|---|---|---|
| **0 — no model** | Plain Python, stdlib | **Zero** | Metric collection, chart rendering, the map, the activity log, schedules. |
| **1 — local model** | A small model on the customer's own box, called over HTTP from our scripts | **Zero after install** | Embedding and searching their uploaded documents. Optionally: tagging, extraction, log redaction. |
| **2 — judgment** | Claude Code | The subscription | All 150 agents. Anything that writes, decides, weighs a trade-off, or speaks to the customer. |

**The rule: push work down a tier whenever the lower tier can do it honestly.** A follower
count does not need a language model. Neither does a bar chart. Semantic search over a
folder of PDFs does not need Claude.

**And the rule that limits it: never push work down a tier to save money when the lower
tier will get it wrong.** A cheaper model that invents a revenue figure costs more than
Claude ever will. See the ceiling in Task 0.6.

### Tier 2 is Claude Code, and it is not the API

**Claude Code is not a model slot in this product. It is the whole engine.** The skills,
the tentacles, the MCP connections, the file access — all of it belongs to Claude Code.
That is why there is no GPT option and we do not advertise one.

**And it is not the API either.** Per-token API billing is the wrong instrument for a
system that runs a business all day, and it is the single easiest way to hand a customer a
bill that ends the subscription. **A Claude subscription includes usage.** Same Claude
Code, same everything, flat monthly cost, no per-token charge.

| Route | Who uses it | What they pay |
|---|---|---|
| **Claude subscription** (Pro or Max) | **Every customer.** This is the route the curriculum teaches. | Flat monthly. Usage included. |
| **Amazon Bedrock** | The owner, for testing on the existing AWS box | Per token, on the AWS bill |
| Cheap hosted open model | An **advanced library module**, not the curriculum. Task 0.6. | ~$3/mo, prepaid cap |
| Anthropic API key | **Nobody.** Do not put this in the curriculum. | Per token, uncapped |

**Why the API is the wrong instrument, with the arithmetic.** One agent run accumulates
roughly 50k input tokens across its turns, because Claude Code re-sends context on every
turn, and produces a few thousand output tokens. At twenty runs a day:

| Route | Per run | Per month |
|---|---|---|
| Claude API, Sonnet rates | ~$0.20 | **~$120** |
| **Claude subscription** | included | **$20 flat** |
| Cheap hosted open model | ~$0.005 | ~$3, prepaid |

The per-run figures are estimates; the point they make is not. **The subscription is six
times cheaper than the API for the same work, and it cannot surprise anyone.** That is the
whole reason the product is viable at $97.

### Task 0.1 — The customer route: subscription on a headless server

The problem: a Claude subscription signs in through a browser, and a VPS has no browser.
There is a built-in answer.

**DO:** On the server, as the `aios` user:

```bash
claude setup-token
```

Confirmed present in the CLI: *"Set up a long-lived authentication token (requires Claude
subscription)."* It prints a URL, the customer opens it on their laptop, approves, and
pastes the code back. The result is a long-lived token on the server, so the timers and
the Telegram bridge keep working unattended.

Rules:

- **Never `--bare` for this.** That flag forces auth to `ANTHROPIC_API_KEY` or
  `apiKeyHelper` and never reads the subscription credentials. It will silently push the
  customer onto per-token billing, which is the exact outcome we are avoiding.
- Do not write the token anywhere our code reads. Claude Code owns it.
- Day 0 of the curriculum has to say **which plan to buy before they start.** A customer
  who reaches Day 6 and discovers they need a subscription is a refund.

**CHECK:** Close the SSH session, wait for a timer to fire, and confirm an agent ran with
nobody logged in. Then `claude -p "say ok"` as the `aios` user returns `ok`.

### Task 0.2 — The owner route: Bedrock on the existing AWS box

The owner already has Claude through Bedrock and does not want a second subscription just
to test. Supported directly.

**DO:** In the Bedrock console, open the Model catalog, pick an Anthropic model, and submit
the use case form — **access is granted immediately on submission**, once per AWS account.
Then run `claude`, choose **3rd-party platform**, then **Amazon Bedrock**, and let the
wizard do the rest. If already signed in, run `/setup-bedrock`. The wizard detects AWS
profiles, asks for the region, checks which models the account can actually invoke, and
writes the result to `~/.claude/settings.json`.

Scripted equivalent, for the installer:

```bash
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1
export ANTHROPIC_DEFAULT_SONNET_MODEL='us.anthropic.claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'
```

IAM needs `bedrock:InvokeModel`, `bedrock:InvokeModelWithResponseStream`,
`bedrock:ListInferenceProfiles` and `bedrock:GetInferenceProfile`.

**Two Bedrock traps that will waste the owner's afternoon:**

1. **Pin the models.** Unpinned, the primary model resolves to Claude Code's built-in
   default, which is an **Opus** model on current versions. Opus costs several times Sonnet
   per token. An unpinned Bedrock box quietly bills at the Opus rate for everything.
2. **`WebSearch` does not exist on Bedrock.** Any skill that searches the web — `watch`
   most obviously — will behave differently on the owner's test box than on a customer's
   subscription. **Test anything web-facing on a real subscription before shipping it**, or
   you will debug a skill that was never broken.

**CHECK:** `/status` inside Claude Code shows `Amazon Bedrock` and the expected region.
`/status` also shows the resolved model, and it is the Sonnet ID you pinned, not Opus.

### Task 0.3 — The thing that decides whether this product survives contact

This is the most important paragraph in the plan and it is easy to skip.

**Subscription plans have usage limits: a rolling five-hour window and a weekly window.**
And per Anthropic's own cost documentation, **a scheduled task sends the full context every
time it fires, even when the session is idle.** Our entire product is scheduled agents
running unattended all day. Those two facts collide.

Get this wrong and a customer on the cheapest plan hits "You've hit your weekly limit" on
day three, their AIOS goes silent, and they refund. So:

- **The metric collector is plain Python, not Claude.** Task 6.1 calls the APIs directly
  with `urllib`. Pulling a follower count does not need a language model. **This is the
  single biggest saving in the system** — the dashboard refreshes all day for zero tokens.
- **Timers run few things, rarely.** The morning brief and the inbox triage are worth a
  scheduled run. Most of the 150 agents are worth running when asked. Default a new agent
  to on-demand and make the customer opt it into a schedule.
- **Set `model:` honestly per skill.** `fast` for triage and extraction, `smart` for the
  rest, `deep` only where a wrong answer costs real money. This is the per-skill dial from
  the agent spec and it is the difference between a plan that lasts a week and one that
  lasts five hours.
- **Vault search runs on Tier 1, not on Claude.** Searching the customer's own documents is
  the single largest avoidable token cost in the system, and Task 0.5 makes it free.
- **Say the required plan out loud, with the reason.** Recommend the plan that comfortably
  carries the default schedule, and tell customers that adding more scheduled agents uses
  more of the allowance. Usage credits exist as the escape hatch for heavy users.
- **Sessions are short and single-purpose.** The bridge shells out per request rather than
  holding one long conversation, which is already how `bridge.py` works. Keep it that way:
  long-lived context is re-sent on every turn and gets expensive fast.

**DO:** Before Sept 14, run one server for a full week on the cheapest plan you intend to
recommend, with the default schedule switched on. **Record the actual usage.** Publish the
recommendation from that measurement, not from a guess.

**CHECK:** After seven days the box has not hit a weekly limit, and you can state the
recommended plan with a number behind it.

### Task 0.4 — Per-skill model choice, named by tier and not by product

Every agent declares how much brain it needs. **Name the rung, not the model**, so that
changing route later is one file and not 150.

**DO:** Add `model:` to the skill spec. Allowed values `fast`, `smart`, `deep`. Optional;
missing means `smart`, because that is the right answer for nearly every agent.

| Value | Use it for |
|---|---|
| `fast` | High volume, low judgment. Triage, sorting, extraction, tagging. |
| `smart` | The default. Nearly every agent. |
| `deep` | Genuinely hard reasoning where a wrong answer costs the owner money. |

Then create **`config/models.yaml`**, the only place a tier becomes a real model:

```yaml
# The active route. One of: claude-subscription | bedrock | openrouter
route: claude-subscription

tiers:
  claude-subscription:
    fast:  haiku
    smart: sonnet
    deep:  opus
  bedrock:
    fast:  us.anthropic.claude-haiku-4-5-20251001-v1:0
    smart: us.anthropic.claude-sonnet-4-6
    deep:  us.anthropic.claude-sonnet-4-6   # deliberately not Opus. See Task 0.2 trap 1.
  openrouter:                                # advanced module only. See Task 0.6.
    fast:  qwen/qwen3.7-flash
    smart: qwen/qwen3.6-35b-a3b
    deep:  qwen/qwen3-max-thinking
```

**The trap that will cost you an hour: Claude Code does not read `metadata.model`.** It is
not on Claude Code's frontmatter allowlist — it is *our* field. Nothing happens
automatically. **Whatever launches a skill must look the tier up in `config/models.yaml`
and pass it as `claude --model <id>`.** That means the dashboard's `/api/run`, the systemd
timers, and `bridge.py` all read this file. Write one helper, `scripts/model_for.py`, and
call it from all three. If you skip this, every agent silently runs on the default model
and the `fast`/`deep` labels on the dashboard are decoration.

**CHECK:** `inbox` resolves to a Haiku model and `brief` to an Opus one — prove it by
logging the resolved `--model` value to the activity log on every run, not by reading the
yaml. Change `route:` to `bedrock`, run one agent, and confirm the logged model ID changed
with no skill file edited.

### Task 0.5 — Tier 1: the free local model on the customer's own box

**This tier exists for one job that Claude should never be paid to do: searching the
customer's own documents.** They upload their business into `vault/`. Every time an agent
needs "what does my onboarding doc say about refunds", the wrong answer is to feed 40 pages
to Claude. The right answer is a local embedding model, which is free, private, and fast.

**Tier 1 does not go through Claude Code.** Claude Code cannot point at a local model
without an unsupported translation proxy (Task 0.6 explains why that is a bad trade). So
Tier 1 is our own Python calling a local HTTP endpoint. This keeps it entirely outside the
Claude Code auth story, which is what makes it simple.

**DO:** Write `scripts/local_model.py` exposing exactly two functions:

```python
embed(texts: list[str]) -> list[list[float]]   # for vault search
classify(text: str, labels: list[str]) -> str  # optional, Tier 1b below
```

**Tier 1a — embeddings. Build this. It fits the baseline box.** A sentence-embedding model
is around 130 MB and runs on CPU in a couple of hundred megabytes of RAM, so it works on
the same ~$5 VPS everything else runs on. This powers vault search in Build 5.

**Tier 1b — a small generative model. Optional, and gated.** A 4B model quantised is around
3 GB, which does **not** fit the baseline 1 GB box. Only offer it if the customer has 4 GB+,
and check before installing:

```bash
awk '/MemTotal/ {exit ($2 < 3800000)}' /proc/meminfo || echo "skip the local model"
```

If it is available, use it for log redaction and tagging. Never for anything the customer
reads as an answer.

**Everything in Tier 1 degrades gracefully or it does not ship.** If no local model is
installed, `embed()` returns `None` and vault search falls back to keyword matching;
`classify()` returns `None` and redaction falls back to the regex rules that already exist.
**A missing local model must never break a page, fail an install, or block an agent.** It is
an optimisation, not a dependency.

**CHECK:** Uninstall the local model entirely and confirm the dashboard loads, vault search
still returns results, and the activity log is still redacted. Then install it and confirm
vault search gets better while the token spend for a search stays at zero.

### Task 0.6 — The cheap hosted route, and why it is a library module and not the curriculum

The owner will be asked this by customers, so the plan needs a real answer rather than a
shrug. **Open models are 40 to 60 times cheaper per token than Claude.** At the prices
checked while writing this, `qwen3.6-35b-a3b` is $0.05 per million input and $0.70 per
million output, which puts the same twenty-runs-a-day workload near **$3 a month**. Prepaid
credits mean the balance *is* the spending cap, so the runaway-bill risk that rules out the
Anthropic API does not apply here.

That is a real option and the plan records it. **It is not the default, for three reasons,
and a junior dev must not promote it to one.**

1. **There is no Anthropic-format endpoint, so it needs a proxy.** OpenRouter serves
   OpenAI-format `/api/v1/chat/completions` only. Claude Code speaks Anthropic format, so a
   translation layer (LiteLLM, claude-code-router) has to sit between them. That is another
   service on the box that a non-technical customer cannot debug.
2. **It is explicitly unsupported.** Anthropic's own gateway documentation states that it
   *"doesn't support routing Claude Code to non-Claude models through any gateway."* It
   works until a Claude Code release changes something, and then it is the owner's support
   inbox, during a cohort.
3. **Agentic reliability, which is the real reason.** Cheap models write acceptable prose.
   Where they fall down is exactly what this product is: many-turn tool calling, following a
   sixty-line procedure without drifting, and the exact-string matching the Edit tool needs.
   And the failure mode is the worst one available to us — the agent spec's hard rule is
   that **an agent never invents a number**, and weaker models break that rule most, and
   plausibly, in a chart the owner then acts on. A missing agent costs a feature. A
   confidently wrong revenue figure costs the customer.

**Can it be free? For a demo, yes. For this product, no — and the reason is requests, not
tokens.** OpenRouter's free model variants are capped at 20 requests per minute and **50
requests per day** until you have bought $10 of credit ever, which lifts it to 1,000 per
day. A single agentic run is not one request; it is one request per turn, so ten to thirty.
**Fifty requests a day is two or three agent runs — a demo, not a business.** The 1,000/day
tier is genuinely workable, but you paid to get there, so it is not free either, and which
models carry a `:free` variant changes without notice. **Do not build the product on it.**

**DO:** Write this up as a module for the $49/mo library, not as a curriculum day. Title it
for what it delivers — cutting the running cost from $20 to about $3 — and label it
advanced. Ship it with: the proxy install, `config/models.yaml` switched to `route:
openrouter`, a required prepaid cap, and an honest list of what degrades. **Test it on the
owner's box first and name the agents that stop working.**

**Do not put this in Days 0-7 and do not mention it on the sales page.** What justifies $97
is a non-technical owner getting a working system in seven days. A translation proxy plus a
model that silently mangles tool calls produces refunds faster than any missing feature.

**CHECK:** The module exists, the owner has personally run the whole vault on it, and the
"what degrades" list is written from that run rather than from this paragraph.

---

# BUILD 1 — The Mind

A web page. It shows every agent grouped by department. You click an agent and a panel
shows what it does. This is also what we screenshot for the sales page.

**Stack: FastAPI + one HTML file + one JS file. No React. No npm. No build step.**
That is not a preference. A build step is the number one way this breaks on someone
else's machine.

### Task 1.1 — The tool list

**DO:** Create `references/tool-registry.md` with exactly this table.

```markdown
| key | Display name | Brand hex |
|---|---|---|
| claude | Claude | #D97757 |
| gmail | Gmail | #EA4335 |
| calendar | Google Calendar | #4285F4 |
| sheets | Google Sheets | #34A853 |
| drive | Google Drive | #FBBC04 |
| docs | Google Docs | #4285F4 |
| telegram | Telegram | #26A5E4 |
| groq | Groq | #F55036 |
| elevenlabs | ElevenLabs | #000000 |
| remotion | Remotion | #0B84F3 |
| composio | Composio | #6366F1 |
| socialclaw | SocialClaw | #111111 |
| blotato | Blotato | #1F6FEB |
| manychat | ManyChat | #2C7BE5 |
| github | GitHub | #181717 |
| webhook | Custom API | #888888 |
```

**CHECK:** The file exists and has 16 rows plus the header.

### Task 1.2 — The checker

**DO:** Create `scripts/validate_skills.py`. It looks at every
`skill-vault/*/SKILL.md` and prints PASS or FAIL for each.

It must FAIL a skill if any of this is true:

- The frontmatter is not valid YAML.
- There is a top-level key that is not in the allowed list (see "Two mistakes" above).
- `metadata` is missing any of: `wing`, `department`, `function`, `replaces`,
  `the-human`, `ladder`, `trigger`, `outputs`, `kpis`, `tools`, `autonomy`,
  `scaffolding-phase`.
- `metadata.ladder` does not have exactly three keys: `manual`, `assisted`, `autonomous`.
- `metadata.autonomy` is not one of: `manual`, `assisted`, `autonomous`.
- `metadata.wing` is not one of: `intelligence`, `content`, `growth`, `comms`,
  `command`, `back-office`, `build`.
- `metadata.model` is present and is not one of: `fast`, `smart`, `deep`.
  It is optional. Missing means `smart`, and the map fills that in rather than
  failing, because that is the right answer for nearly every agent anyway.
  **Reject a real model name here.** `sonnet`, `opus`, or `qwen/qwen3.6-35b-a3b` in a
  skill file is an error, not a synonym — tiers are resolved once in
  `config/models.yaml` (Task 0.4), and a hardcoded model name is how a route switch
  silently stops working for one agent.
- `outputs`, `kpis`, or `tools` is empty.
- A tool in `metadata.tools` is not a `key` in `references/tool-registry.md`.

Print one line per problem, like `qualify: metadata.kpis: is empty`.
Exit 0 if everything passed. Exit 1 if anything failed.

**CHECK:**
```bash
python3 scripts/validate_skills.py
```
`qualify` says PASS. The other 9 say FAIL. `echo $?` prints `1`. That is correct
right now, because only `qualify` has been converted.

### Task 1.3 — Turn the skills into map data

**DO:** Create `scripts/build_map.py`.

It runs the Task 1.2 checks first. If anything fails, it prints the failures and
exits without writing. Then it reads all the frontmatter and writes one file:
`dashboard/static/map.json`, shaped like this:

```json
{
  "generated": "2026-09-14T10:00:00Z",
  "counts": { "total": 10, "manual": 0, "assisted": 8, "autonomous": 2 },
  "tools": { "claude": { "name": "Claude", "hex": "#D97757" } },
  "wings": [
    { "wing": "growth",
      "departments": [
        { "department": "Sales",
          "functions": [
            { "function": "Qualification",
              "agents": [
                { "name": "qualify",
                  "description": "...",
                  "replaces": "...",
                  "the-human": "...",
                  "ladder": { "manual": "...", "assisted": "...", "autonomous": "..." },
                  "trigger": "...",
                  "outputs": ["..."],
                  "kpis": ["..."],
                  "tools": ["claude", "sheets"],
                  "autonomy": "assisted",
                  "model": "smart",
                  "phase": 1 }
              ] } ] } ] }
  ]
}
```

Order: wings in the order listed in Task 1.2. Departments A-Z. Functions A-Z.
Agents by `phase`, then by name.

Add this line to `.gitignore`:
```
dashboard/static/map.json
```
It is generated. It never gets committed.

**CHECK:**
```bash
python3 scripts/build_map.py
python3 -c "import json;print(json.load(open('dashboard/static/map.json'))['counts'])"
```
The total matches the number of skills that passed.

### Task 1.4 — The web server

**DO:** Create `dashboard/requirements.txt`:
```
fastapi==0.115.*
uvicorn[standard]==0.32.*
pyyaml==6.*
```

Create `dashboard/server.py`. Five routes, nothing else:

| Route | Returns |
|---|---|
| `GET /` | the file `dashboard/static/index.html` |
| `GET /api/map` | the contents of `dashboard/static/map.json` |
| `GET /api/activity?limit=50` | last 50 lines of `var/activity.jsonl`, newest first |
| `GET /api/health` | `{"bridge": true/false, "claude": true/false, "disk_free_mb": 0}` |
| `POST /api/run` | body `{"skill":"brief"}` → starts that skill, returns `{"run_id":"..."}` |

Rules, all of them mandatory:

- Every route needs HTTP Basic auth. Username is `owner`. Password comes from the
  environment variable `DASHBOARD_PASSWORD`.
- If `DASHBOARD_PASSWORD` is not set, the server refuses to start and prints
  `DASHBOARD_PASSWORD is not set. Refusing to start.` **Never ship a default password.**
- `POST /api/run` only accepts a skill name that exists in `map.json`. Anything else
  returns 400. Never put the incoming name into a shell command string.

**CHECK:**
```bash
cd /tmp/bp-check
DASHBOARD_PASSWORD=test python3 -m uvicorn dashboard.server:app --port 8000 &
curl -su owner:test localhost:8000/api/map | head -c 100     # JSON appears
curl -s localhost:8000/api/map                                # 401 Unauthorized
curl -su owner:test -X POST localhost:8000/api/run \
     -H 'Content-Type: application/json' -d '{"skill":"../../etc/passwd"}'   # 400
```
All three behave as written. Then `unset DASHBOARD_PASSWORD` and start it again — it
must refuse.

### Task 1.5 — The activity log

**DO:** Create `scripts/activity.py` with one function:

```python
def log(event, skill=None, detail=None, status="ok"):
    """Append one line of JSON to var/activity.jsonl."""
```

Each line: `{"ts": "<iso8601>", "event": ..., "skill": ..., "detail": ..., "status": ...}`

Rules:

- Append only. Never rewrite the file.
- Cut `detail` to 200 characters.
- **Before writing, remove secrets from `detail`.** Replace anything matching
  `sk-...`, `ak_...`, `xi-api...`, or an email address with `[redacted]`.
  This log shows on a web page that people will screenshot.
- When the file passes 10 MB, rename it to `activity.jsonl.1` and start a new one.

Then call `log()` from `scripts/bridge.py` in four places: message received, skill
started, skill finished, error caught.

**CHECK:** Run a skill. Then `tail -1 var/activity.jsonl` is one valid JSON object
with a real timestamp. Now pass the string `sk-ant-test123` in as `detail` and confirm
the file says `[redacted]`.

### Task 1.6 — The page itself

**DO:** Create `dashboard/static/index.html` and `dashboard/static/app.js`.
Plain HTML. CSS inside a `<style>` tag. One JS file using `fetch`. Nothing installed.

**Build the layout drawn in "What they see on screen" at the top of this plan.** That
mockup shows five bands. You build four of them here. The `CONNECTIONS` band is added
later in Task 4.6, so leave a gap for it.

Four sections, top to bottom:

1. **Header.** The words `YOUR AIOS`. Then the counts from `map.json`, like
   `10 agents · 8 assisted · 2 autonomous`. Then coloured dots from `/api/health`.
2. **The map.** One column per wing. Inside each column, a card per department.
   Inside each card, the agent names. Next to each name, a dot showing autonomy:
   hollow for `manual`, half-filled for `assisted`, filled for `autonomous`.

   **Build this plain version now and keep it forever.** Task 6.2b replaces it with a
   generated archify diagram that looks far better, but this hand-built list stays as the
   fallback for a server with no Node and for the moment before the first diagram is
   generated. The map is the one thing on this page that is never allowed to be missing.
3. **The panel.** Clicking an agent opens it. Show `replaces`, `the-human`, the three
   ladder rungs with the current one highlighted, `trigger`, `outputs`, `kpis`, and the
   tool names as coloured chips using the hex from the registry. Put a **Run** button
   at the bottom that POSTs to `/api/run`.
4. **The feed.** The last 50 lines from `/api/activity`. Refresh every 10 seconds.

Rules:

- Dark background, near-black. One accent colour. This gets screenshotted for the
  sales page, so it has to look deliberate.
- Must read cleanly at 1200 pixels wide.
- If `/api/map` returns an error, show the text
  `Map not built yet — run: python3 scripts/build_map.py`.
  Never show a blank page.

**CHECK:** Open it in a browser. Click three different agents and confirm the panel
changes correctly each time. Press Run and watch the event appear in the feed within
10 seconds. Open the browser console: zero errors.

---

# BUILD 2 — The Voice

Right now `scripts/bridge.py` already turns your voice notes into text. It uses Groq
Whisper. Look at `voice_to_text()` on line 81. That half works.

What is missing: it always replies with typing. We want it to reply with a voice note.

### Task 2.1 — Make it speak

**DO:** Edit `scripts/bridge.py`. Add two functions.

```python
def speak(text):
    """Turn text into mp3 bytes using ElevenLabs. Return None if it can't."""
```
- Reads `ELEVEN_API_KEY` and `ELEVEN_VOICE_ID` from the environment.
- POST to `https://api.elevenlabs.io/v1/text-to-speech/<ELEVEN_VOICE_ID>?output_format=mp3_44100_128`
- Headers: `xi-api-key: <ELEVEN_API_KEY>` and `Content-Type: application/json`
- Body: `{"text": text, "model_id": "eleven_turbo_v2_5"}`
- Return the raw response bytes. On any error, return `None`. Never raise.

```python
def send_voice(chat_id, mp3_bytes):
    """Send audio to Telegram as a voice note."""
```
- Telegram needs OGG/Opus. Convert first, in a temp directory:
  `ffmpeg -y -i in.mp3 -c:a libopus -b:a 32k out.ogg`
- Then POST multipart to `https://api.telegram.org/bot<TOKEN>/sendVoice`
  with fields `chat_id` and a file field named `voice`.
- **Important:** the existing `tg()` function on line 31 cannot do this. It only
  sends url-encoded form data, not files. Write the multipart body yourself, the same
  way `transcribe()` does it on line 62.

### Task 2.2 — Wire it up

**DO:** In `run_bridge()`, the reply currently happens on line 157:
`send(chat, ask_claude(text))`. Replace that with this logic:

```
reply = ask_claude(text)
send(chat, reply)                       # always send the text too
if the message was a voice note and ELEVEN_API_KEY is set:
    mp3 = speak(first 800 characters of reply)
    if mp3 is not None:
        send_voice(chat, mp3)
```

Rules:

- Voice in, voice out. Text in, text out. **Never** send audio in reply to typing.
- Cut the spoken version at 800 characters, ending on a full stop, then add
  ` "Full answer above."` ElevenLabs charges per character.
- Always send the text as well, so nothing is lost if the audio fails.
- If `ELEVEN_API_KEY` is not set, everything still works with text. No crash.

**CHECK:** Four tests on a real phone.

1. Type a message. You get text. No audio.
2. Send a voice note. You get text **and** a voice note. In Telegram it must show a
   waveform with a play button. If it shows a grey file attachment instead, your ffmpeg
   step failed and you sent mp3. Run `ffmpeg -version` to confirm ffmpeg exists.
3. `unset ELEVEN_API_KEY`, restart, send a voice note. You get text. Nothing crashes.
4. Send a voice note that gets a long answer. The audio stops cleanly mid-answer and
   says the full answer is above.

### Task 2.3 — Write it down

**DO:** Add `ffmpeg` to the requirements list in `curriculum/days/day-6.md`, and add
`ELEVEN_API_KEY` and `ELEVEN_VOICE_ID` to `curriculum/00-SERVICES-AND-SETUP.md`.

**CHECK:** Someone can follow Day 6 from scratch and get voice working without asking
you anything.

---

# BUILD 3 — The Agents

Target: 150 agents.

## Start here: the owner has supplied a zip of about 150 skills

**A zip of roughly 150 business skills, already selected from GitHub, is attached to this
plan.** Use it. Do not go back to GitHub to re-pick candidates — that selection work is
done, and it was the slow, judgement-heavy part.

**We ship complete.** The launch product contains the full library. The subscription then
adds more over time in the Skool community. That is a stronger offer than shipping 30 and
promising the rest, and it is now the plan.

**What the zip does not remove.** Every file still has to pass the same gate, because the
dashboard is generated from frontmatter and a file that does not carry our spec is
invisible to the product. For each one:

1. Does it have `metadata:` with our fields — `wing`, `department`, `function`, `replaces`,
   `the-human`, `ladder`, `trigger`, `outputs`, `kpis`, `tools`? Almost certainly not,
   because no GitHub file knows about our spec. That has to be written.
2. Is the body a **procedure** or a **persona**? If it opens "You are a…", it is a
   subagent prompt and needs the rewrite in Task 3.3. Check with
   `grep -rl "You are a" <unzipped>/`.
3. Does it claim a KPI it cannot count, or reference a tool we do not have?
4. **What is its licence?** This is the one that can hurt us commercially.

**The licence check is not optional and it is not paranoia.** We are selling this. Files
gathered from GitHub carry whatever licence their repo had, and some of the largest and
most attractive agent collections have **no licence at all**, which means all rights
reserved and no permission to redistribute — `contains-studio/agents` with 12,410 stars is
exactly this. A zip flattens that information away.

**DO, before writing a single line of conversion code:**

1. Unzip to `imports/staged/` and **do not copy anything into `skill-vault/` yet.**
2. For every file, establish which repo it came from and what that repo's licence is.
   Record it in `imports/ATTRIBUTION.md`: file, source repo, licence, commit if known.
3. **Any file whose origin cannot be established does not ship.** Keep it as research —
   read it, learn what the job is, write our own version from scratch. The job title is a
   fact and facts are free. The wording is someone else's property.
4. MIT and Apache-2.0 files ship with their notices travelling alongside, in
   `imports/licenses/`.

**CHECK:** `imports/ATTRIBUTION.md` has a row for every file in `skill-vault/` that came
from the zip, each naming a real licence. No file in `skill-vault/` has unknown provenance.

## What this means for Sept 14

**Decided: we ship all 150 on day one.** The library is complete at launch and the
subscription adds to it from there. The zip is what makes that possible, because it removes
the selection work.

But be clear about what is left, because it is still the biggest job in the plan:
**150 files have to be converted, and each one has to be run once by a human who reads the
output.** Converting is much faster than authoring from nothing — call it 20 to 30 minutes
each done properly. Across 150 that is still one to two weeks of focused work for one
person, and **the running-and-reading is the bottleneck, not the writing.**

So the plan splits by risk, not by wing:

| Priority | Which agents | Why first |
|---|---|---|
| **Must be tested before launch** | Anything that touches the outside world — sends, posts, replies, pays, deletes | An untested agent that mishandles a real customer's inbox costs more trust than a missing agent ever would |
| **Must be tested before launch** | Everything on a default schedule | It runs unattended, so nobody is watching when it goes wrong |
| Tested as the cohort uses them | Read-only and draft-only agents | The worst case is a bad draft the owner discards |

**The hard rule stands: nothing ships that has never been run.** Every one of the 150 gets
executed once. What varies is how hard we probe it, not whether we ran it.

**And nothing ships as `autonomous` on day one.** The whole library launches at `manual` or
`assisted`, and customers promote agents up the ladder themselves as they learn to trust
them. That is the curriculum's teaching device anyway, and it converts the testing gap into
a feature instead of a risk.

**One thing not to do, however tempting.** If a file cannot be made to work in time, cut it
from the ship list — **do not leave it in the vault as a greyed-out "coming soon" box.** The
map is generated from skills that exist so that it can never claim a capability the system
lacks. A customer who clicks five placeholders and finds nothing stops trusting the ones
that work. Roadmap on the sales page; the dashboard shows what runs.

**What must be true on Sept 14 is that the machine works, not that the library is full.**
Builds 1, 2, 4, 5 and one panel of 6 are the launch. A customer with 30 working agents and
a dashboard that shows their real numbers is delighted. A customer with 150 agents and no
dashboard has a folder of markdown files.

## Read this before you start. It changes the plan.

I searched GitHub for agents we could take instead of writing. Here is what is
actually there.

**The good news.** Two large collections are MIT licensed, which means we are allowed
to use them commercially as long as we keep the licence notice.

| Repo | Stars | Licence |
|---|---|---|
| `wshobson/agents` | 39,474 | MIT |
| `VoltAgent/awesome-claude-code-subagents` | 24,911 | MIT |

**Use these two as the fallback when the zip leaves a gap**, and as the source for the
Build wing. Almost everything in them is for *programmers* — backend architects, Kubernetes
operators, test writers — which is why they are the right place to stock the Build wing and
the wrong place to look for business agents.

**Why the Build wing is worth including rather than scope creep:** a business owner who can
ask their AIOS to fix their own landing page, wire up a form, or debug the thing their
contractor left broken is a customer who does not churn. It is also the cheapest wing to
stock, because these files were written for Claude Code already. **Convert it last** — it is
the easiest, so it is the wrong place to spend the first week.

**There is no repo on GitHub with 137 tested business agents ready to use.** I searched for
it specifically and it does not exist, which is why the owner's zip is a curated selection
rather than a download, and why this product can be sold at all. It also means: **expect the
zip's files to need the same three fixes listed below**, because they came from the same kind
of source.

## Now the part that changes your estimate. Do not skip it.

**Those 55 files are not skills. They are subagent persona prompts.** See the skills
versus subagents table in "Before you start". Here is what one actually looks like:

```yaml
---
name: sales-engineer
description: "Use this agent when you need to conduct technical pre-sales..."
tools: Read, Write, Edit, Glob, Grep, WebFetch, WebSearch
model: sonnet
---

You are a senior sales engineer with expertise in technical sales...
```

Compare that to `skill-vault/qualify/SKILL.md`, which is a numbered procedure with
declared inputs and outputs. **They are not the same kind of document.** Converting one
into the other is a rewrite, not a reformat.

So the honest arithmetic is. **This table is the only agent count in this plan. Every
other number anywhere else is downstream of it.**

| Where the 150 come from | Count | How hard |
|---|---|---|
| Already finished in `skill-vault/` | 10 | done |
| **From the owner's zip**, licence-checked then converted | about 130 | medium — a real rewrite each, but no selection work |
| **Gaps the zip leaves**, written from nothing (Task 3.4) | about 10 | slow |
| **Total on the map** | **150** | |

**The zip changed which job is hard.** Before, the hard part was deciding what 150 agents
should even be — searching, judging, discarding. That is done. What remains is 140
conversions, which is mechanical enough to move fast on but still has to happen file by
file, because **a file without our frontmatter is invisible to the dashboard.**

The Build wing's agents come from the same zip if it contains them, and from the two MIT
dev repos if it does not. Those are the easiest conversions in the set, because they were
written for Claude Code already.

**The Build wing is inside the 150, not on top of it.** About 45 of the 150 are coding
agents. If you read it as "150 business agents plus 45 coding agents" you have invented
about two months of work nobody asked for.

**What the zip really saves you** is the thinking: what each job is called, what a good one
covers, what the steps roughly are, what to measure. That is worth real time. What it does
not save you is writing the skill. Budget for that. **If you look at 150 files and tell
yourself the library is done, you will be about a month behind and not know why.** The zip
is the raw material. The vault is the product.

**Three specific things wrong with the imported files** that you must fix on every one:

1. **They are personas, not procedures.** "You are a senior sales engineer" tells Claude
   who to be, not what to do. Our skills say what to do, in order.
2. **They invent metrics.** Lines like `Demo success rate > 80% achieved` appear
   throughout. That is a target nobody measured, in a file that cannot measure it. Our
   spec bans this: a KPI has to be countable from the agent's own output.
3. **They reference things we do not have.** Several say "query context manager for
   requirements." There is no context manager in our system. Left in, the agent will
   describe a step it cannot take. Replace those with our real `context/` files.
4. **Their `model:` is a product name at the top level.** Look at the example above:
   `model: sonnet`, unnested. Ours is a tier, nested under `metadata:`. Translate it —
   `haiku` becomes `fast`, `sonnet` becomes `smart`, `opus` becomes `deep` — and delete the
   top-level key. The validator rejects both the wrong place and the wrong value, so this
   one will stop you rather than slip through. Same for a top-level `tools:` written as a
   comma-separated string; ours is a list of registry keys under `metadata:`.

**A repo you must not touch.** `contains-studio/agents` has 12,410 stars and excellent
marketing agents. It has **no licence file**. No licence means all rights reserved.
We cannot use it in a paid product. Read it for ideas, copy nothing.

**A useful find.** `wshobson/agents` contains a `social-publishing` skill that posts to
13 platforms through one API key using a service called SocialClaw. That is the
auto-posting feature, already built, MIT licensed. Use it in Build 4.

### Task 3.1 — Convert the 9 skills we already have

The nine: `brief`, `content-week`, `followup`, `inbox`, `newsletter`, `outreach`,
`plan-day`, `remember`, `watch`.

**DO, one skill at a time:**

1. Open the skill's `SKILL.md` and read it.
2. **Do not change the body.** Leave `## What this does`, `## Inputs it reads`,
   `## Execution`, `## Rules` exactly as they are. They already work.
3. Add a `metadata:` block, copying the shape from `skill-vault/qualify/SKILL.md`.
   Fill it in from what you just read:
   - `trigger` — what starts it
   - `outputs` — the things it hands back, from `## Execution`
   - `requires-context` — the `context/*.md` files named in `## Inputs it reads`
   - `tools` — only the ones it really uses, keys from the tool registry
4. Write `replaces` and `the-human` yourself.
   `replaces` names a **problem**, not a feature. Write the annoying thing that
   happens today without this agent.
   `the-human` says what the owner still decides after the agent runs.
5. Write all three ladder rungs, even though we ship most as `assisted`.
6. Set `autonomy` honestly. If it writes a draft and waits for a human, it is
   `assisted`. Do not write `autonomous` to make the map look better.
7. Add one line to `## Rules`: if a file listed in `requires-context` is missing, say
   so and stop.

**Use this table. Do not invent your own categories.**

| skill | wing | department | function |
|---|---|---|---|
| watch | intelligence | Intelligence | Monitoring |
| brief | intelligence | Intelligence | Synthesis |
| remember | intelligence | Knowledge | Context Maintenance |
| newsletter | content | Marketing | Distribution |
| content-week | content | Marketing | Creation |
| qualify | growth | Sales | Qualification |
| outreach | growth | Sales | Outreach Writing |
| followup | growth | Sales | Sequencing |
| inbox | comms | Back Office | Email Triage |
| plan-day | comms | Back Office | Calendar Management |

**CHECK after every single skill:**
```bash
python3 scripts/validate_skills.py
```
Convert one, check, commit. Then the next. If you convert all nine and then run the
checker, you will spend the afternoon untangling nine problems at once.

**When all nine are done:** the checker exits 0 and all 10 say PASS.

### Task 3.2 — Top up from the two MIT repos, only where the zip left a gap

**The zip is the primary source.** Do the zip first (see the top of Build 3): stage it,
record provenance, and sort it by wing. Only then read this task, and only for the wings
the zip left thin. If the zip covers a wing, skip that wing here — two imports of the same
job is 30 wasted conversions, not 30 more agents.

**DO:** Create `scripts/import_agents.py` and a folder `imports/`.

The script clones the two MIT repos into `imports/raw/` (shallow, `--depth 1`), then
copies **only** the business-relevant files into `imports/staged/`, keeping a record of
where each came from. Before copying a file, check whether a staged zip file already does
that job; if it does, do not copy.

Take these paths and no others.

From `VoltAgent/awesome-claude-code-subagents`:
```
categories/08-business-product/*.md
categories/10-research-analysis/*.md
categories/07-specialized-domains/{email-deliverability-engineer,healthcare-admin,m365-admin,seo-specialist,x-api-integration,payment-integration,risk-manager}.md
```

From `wshobson/agents`:
```
plugins/business-analytics/**
plugins/content-marketing/**
plugins/customer-sales-automation/**
plugins/hr-legal-compliance/**
plugins/payment-processing/**
plugins/seo-analysis-monitoring/**
plugins/seo-content-creation/**
plugins/social-publishing/**
plugins/startup-business-analyst/**
plugins/brand-landingpage/**
```

Skip every `README.md`.

**Licence handling. This is not optional.** Create `imports/ATTRIBUTION.md`. For each
imported file write one row: the file, the repo it came from, the licence (MIT), and
the commit hash of the clone. Copy both repos' `LICENSE` files into
`imports/licenses/`. MIT requires the notice to travel with the code. If we ship
without it we are infringing.

Add to `.gitignore`:
```
imports/raw/
```
Keep `imports/staged/` and `imports/ATTRIBUTION.md` in git. Do not commit the clones.

**CHECK:** `ls imports/staged | wc -l` returns at least 150 — the zip plus whatever this
task topped up. `imports/ATTRIBUTION.md` has one row per staged file, no blanks, including
every file that came from the zip.

### Task 3.3 — Turn an imported persona into a working skill

This is the repeating job. Roughly 55 times. **Treat the staged file as research notes,
not as a draft to edit.** Open it, read it, then write a new file.

**DO, for one file at a time:**

1. Read the staged file. Write down, in your own words, the one job it does and the one
   artifact it should hand back. If you cannot name the artifact, this file is not a job,
   it is a job title. Skip it and note why.
2. Create `skill-vault/<name>/SKILL.md` from scratch, using
   `skill-vault/qualify/SKILL.md` as the template.
3. Fill in the frontmatter. All of it is ours. `replaces`, `the-human` and the three
   ladder rungs **do not exist in the source files**, so you are writing them fresh
   every time.
4. Write the body as our four sections: `## What this does`, `## Inputs it reads`,
   `## Execution`, `## Rules`.
   - **`## Execution` is the real work.** Turn the persona's bullet lists into numbered
     steps that produce the artifact from step 1. If the source file has no steps, only
     adjectives, you are writing the steps yourself.
   - Write for a business owner, not a developer. Cut the jargon.
   - **Delete every invented metric.** Replace with KPIs countable from this skill's own
     output.
   - **Delete every reference to a system we do not have**, such as a "context manager".
     Point it at the real `context/` files instead.
5. Add `source:` under `metadata:` naming the origin repo, so attribution survives.
6. **Run it.** Give it real input and read the output. Ask one question: would a business
   owner have paid for this? If no, fix it or delete the skill. **A skill that has never
   run does not ship.**
7. `python3 scripts/validate_skills.py` must exit 0.
8. Commit, one skill per commit.

**CHECK:** For every skill in `skill-vault/`, you can name the day you ran it and what
came out. If you cannot, it is not done.

**CHECK, and this one catches the common failure:** open any three converted skills and
confirm none of them contain the phrase "You are a" in the body. If they do, you edited
a persona instead of writing a procedure, and the skill will ramble instead of producing
the artifact.

### Task 3.4 — Write the missing business skills

**DO:** Use the job list in `ai-workforce-blueprint.pdf` as the menu of jobs a business
actually needs. For each job that is not already covered, write a new skill the same
way as Task 3.3, steps 2 through 7.

**Write the text yourself.** Do not copy sentences from the PDF, and do not copy from
`contains-studio/agents`. The list of jobs is a fact and facts are free. The wording is
someone else's property.

**This task is now gap-filling, not bulk authoring.** The zip covers most of the list, so
work from the difference rather than from zero:

1. List every job in the PDF.
2. List every skill the zip actually delivered, after the licence check in Task 3.0.
3. **Write only what is in the first list and not the second.** Expect this to be a short
   list, and expect it to be the awkward jobs nobody on GitHub bothered with — which are
   often the ones closest to what our specific customer does.
4. Cover any wing the zip left thin. **A wing with two agents in it looks broken on the
   map**, so an under-filled wing is a higher priority than another agent in an already
   deep one.

**The hard rule: never ship an agent you have not run.** If a job cannot be made to work in
time, cut it from the ship list rather than shipping it untested. One agent that confidently
mishandles a real customer's inbox costs more trust than a missing capability.

**CHECK:** Every job in the PDF is either covered by a working skill or explicitly recorded
as out of scope with a reason. No wing has fewer than five agents. The dashboard renders
every one without a gap or a blank card.

### Task 3.5 — The Build wing, last

**DO:** Get to about 45 coding agents, the same way as Task 3.3. **Take them from the
owner's zip first** — sort the staged files by wing and count how many coding agents the zip
already gave you. Only top up from the two MIT repos (`wshobson/agents`,
`VoltAgent/awesome-claude-code-subagents`) if the zip left you short, and only under the
same licence gate. This is the easiest work in Build 3, which is exactly why it goes last.

Pick for **what a business owner would ask for**, not for what impresses an engineer.
Fixing a landing page, editing copy on their own site, wiring a form to a spreadsheet,
reading an error message, reviewing what a contractor delivered. **Skip the Kubernetes
operators, the service-mesh agents, and anything that assumes a CI pipeline.** Our
customer does not have one and never will.

The conversion is lighter here than for business skills, because these files were written
for Claude Code in the first place, so their tools and assumptions are already right. The
persona-to-procedure rewrite from Task 3.3 still applies in full. **It is lighter, not
skippable.**

One extra rule for this wing: **every Build-wing skill shows the owner the change before
it makes it.** These agents touch working websites. `autonomy: assisted` is the ceiling
here and no Build-wing skill ships as `autonomous`.

**CHECK:** `python3 scripts/build_map.py` shows 150 or more across seven wings.
`grep -rl "kubernetes\|service mesh\|helm" skill-vault/` prints nothing. No skill with
`wing: build` has `autonomy: autonomous`.

---

# BUILD 4 — The Tentacles

The 150 agents are what it comes with. The tentacles are what makes it theirs.
The owner pastes an API key for something they already pay for, and their AIOS can now
use it. A CRM. A posting tool. A chat tool. Anything with an API.

## Read this first. It saves you weeks.

Everything below was checked live on 7 September 2026. Two important things came out of
that.

**One.** Every tentacle is an MCP server. There is no second mechanism. Do not build a
custom connector framework. Claude Code already has one, and it already reads keys from
the environment so keys never touch a config file.

**Two.** There are exactly five kinds of tentacle. Build tiers A and C first. Those are
the only two where "paste a key" genuinely works end to end, and between them they cover
both services the owner asked for by name.

| Tier | How it connects | Covers | What the owner does |
|---|---|---|---|
| A | Official remote MCP server, API key in a header | Blotato | Pastes a key. Done. |
| B | Official remote MCP server, OAuth login | HubSpot, GoHighLevel | Browser login. See the warning in Task 4.5. |
| C | Generic bridge that reads the service's OpenAPI spec | ManyChat, Pipedrive, most software | Pastes a key. |
| D | Pick from the public MCP registry | the long tail, about 9,100 servers | Picks from a shortlist. |
| E | Composio | apps with no MCP server and no public spec | Login through Composio. |

### How Claude Code stores keys. Learn this before you write anything.

Official docs: https://code.claude.com/docs/en/mcp

A server over HTTP looks like this:

```json
{
  "mcpServers": {
    "blotato": {
      "type": "http",
      "url": "https://mcp.blotato.com/mcp",
      "headers": { "blotato-api-key": "${BLOTATO_API_KEY}" },
      "timeout": 600000
    }
  }
}
```

A server that runs as a local program looks like this:

```json
{
  "mcpServers": {
    "manychat": {
      "command": "uvx",
      "args": ["mcp-openapi-proxy"],
      "env": { "API_KEY": "${MANYCHAT_API_KEY}" }
    }
  }
}
```

**`${VAR}` works.** Claude Code substitutes environment variables in `command`, `args`,
`env`, `url`, and `headers`. `${VAR:-default}` works too. So the key lives in
`/opt/aios/.env` and the config only ever holds the variable name. That is the whole
security story, and it is already built.

**One trap.** If a variable is not set, Claude Code passes the literal text `${VAR}`
through and only prints a warning. It does not stop. The owner then gets a confusing
401. **So before running anything, check that every variable named in the config
actually exists.** Make that a startup check.

**Do not hand-edit the JSON.** Use the CLI. It validates for you:

```bash
claude mcp add-json <name> '<json>' -s user   # best for scripts
claude mcp add <name> <url> -t http -H "Key: value" -s user
claude mcp list
claude mcp get <name>
claude mcp remove <name>
```

### Task 4.1 — Tier A: Blotato, the one the owner asked for

Blotato has an official MCP server. This is a one-line install.

**DO:** Create `skill-vault/connect-blotato/SKILL.md`. It walks the owner through:

1. **Warn them first, before anything else.** Blotato's API needs a paid plan, and
   **generating an API key immediately ends their free trial and starts billing.** The
   skill must say this in plain words and wait for a yes. Do not skip this. A surprise
   charge on day five of a seven-day challenge is a refund.
2. Get the key. Write it to `/opt/aios/.env` as `BLOTATO_API_KEY`.
   **Wrap it in quotes.** Blotato keys often end in an `=` character, and an unquoted
   `=` gets mangled by shells and `.env` parsers. Their own docs say this is the number
   one cause of 401s.
3. Register the server:
   ```bash
   claude mcp add blotato --url https://mcp.blotato.com/mcp \
     --header "blotato-api-key: ${BLOTATO_API_KEY}"
   ```
4. Test with a read-only call: list the owner's connected social accounts.
5. Report which accounts it found, by name.

Reference docs, all confirmed live:
- Getting started: https://help.blotato.com/api/start.md
- Claude Code page with the exact command: https://help.blotato.com/api/claude-code.md
- MCP tools list: https://help.blotato.com/api/mcp/tools.md

Facts you will need. Do not guess these.

| Thing | Value |
|---|---|
| REST base URL | `https://backend.blotato.com/v2` |
| Auth header | `blotato-api-key` — **not** `Authorization: Bearer` |
| Wrong host that models keep inventing | `api.blotato.com` does not exist |
| Rate limit | 30 requests per minute |
| Publish endpoint | `POST /v2/posts` |

If you ever call the REST API directly instead of the MCP server, note that
`scheduledTime` and `useNextFreeSlot` sit at the **top level**, as siblings of `post`,
not inside it. That is a common mistake.

**CHECK:** With only the skill, connect Blotato and list the connected accounts. Then
confirm `grep BLOTATO /opt/aios/app/.claude/settings.json` shows `${BLOTATO_API_KEY}`
and never the key itself.

### Task 4.2 — Tier C: the generic bridge, one tool for every other service

Most software publishes an OpenAPI file describing its whole API. There is a maintained
open-source bridge that reads that file and turns it into MCP tools with no code. That
means one tool covers hundreds of services.

Use `matthewhand/mcp-openapi-proxy`. MIT licensed, Python, actively maintained.
https://github.com/matthewhand/mcp-openapi-proxy

**DO:** Create `skill-vault/connect-api/SKILL.md`. When the owner says "connect my
ManyChat" or "connect my Pipedrive", it:

1. Finds the service's OpenAPI file. Try, in order: the service's own docs, then the
   free directory at https://api.apis.guru/v2/list.json which holds about 2,500 specs.
2. Asks for the API key. Writes it to `.env`. Never anywhere else.
3. Registers the bridge with `claude mcp add-json`, setting these environment
   variables: `OPENAPI_SPEC_URL`, `API_KEY`, `API_AUTH_TYPE` if the service does not use
   Bearer, and `TOOL_WHITELIST`.
4. **Sets `TOOL_WHITELIST`. This is mandatory, not optional.** See the warning below.
5. Makes one read-only call and reports the result.
6. Saves a copy of the spec file into `vault/specs/` so the tentacle keeps working if
   the service moves the URL.

**The warning about tool counts.** A big service turns into a huge number of tools.
HubSpot is 245. Pipedrive is over 150. Loading 245 tools into Claude ruins its ability
to think, and it will get slower and dumber, not more capable. **Never register a
service without a whitelist of the ten or twenty operations the owner actually needs.**
If you skip this, the whole system degrades and it will look like a Claude problem
rather than your bug.

For ManyChat specifically, these are confirmed live:

| Thing | Value |
|---|---|
| OpenAPI spec | `https://api.manychat.com/swagger/compileJson?type=Page_API` |
| Base URL | `https://api.manychat.com` — the spec leaves this blank, so you must set it |
| Auth | `Authorization: Bearer <key>` |
| Endpoint count | 34, all under `/fb/`, which covers Instagram too despite the name |
| Useful ones | `GET /fb/subscriber/getInfo`, `POST /fb/subscriber/addTagByName`, `POST /fb/sending/sendContent`, `GET /fb/page/getTags` |
| No official MCP server | correct. Community ones exist but are abandoned. Do not use them. |
| Spec URL is undocumented | it works today but could move. That is why you cache it. |

**CHECK:** Connect ManyChat using only the skill. Ask "how many subscribers have the
tag X" in plain English and get a real number. Then run `claude mcp get manychat` and
confirm the tool count is under 25 because the whitelist worked.

### Task 4.3 — Tier D: let them browse the registry

There is an official public registry of MCP servers with a free JSON API. About 9,100
servers. `GET https://registry.modelcontextprotocol.io/v0/servers`

**DO:** Create `skill-vault/find-tool/SKILL.md`. The owner describes what they want to
connect. The skill queries the registry, and shows **at most five** options with what
each one does.

**Do not show them 9,100 results.** Keep a curated shortlist of about 50 servers you
have personally tested in `references/mcp-shortlist.md`, and search that first. Only
fall back to the full registry if nothing matches.

**A correction, in case you read it somewhere else.** The GitHub repo
`modelcontextprotocol/servers` is **no longer a directory of servers.** It now holds
only seven reference examples. Its own README points at the registry. Do not build a
browse feature on that repo.

**CHECK:** Ask for something specific like "I want to connect Notion" and get a small
list with the official one first.

### Task 4.4 — Tier E: Composio, for the big-name apps

This already works. Day 5 sets it up and `scripts/create_composio_session.py` creates
the connection.

Two corrections to what we previously wrote in the curriculum:

- Composio covers **over 1,500 apps**, not 100. Fix that number wherever it appears.
- The free tier is 100,000 tool calls a month, 50,000 trigger events, and unlimited
  connected accounts if you bring your own OAuth app. Usage **pauses** at the cap, so
  there is no surprise bill. Say that in the curriculum, it removes a real objection.

**DO:** Confirm Gmail still connects. Update the app-count and free-tier numbers in
`curriculum/days/day-5.md`, `references/composio-setup.md`, and
`curriculum/00-SERVICES-AND-SETUP.md`.

**CHECK:** Follow `references/composio-setup.md` on a clean machine, connect Gmail using
only what is written there, then ask for your five most recent email subject lines and
get real subjects back.

### Task 4.5 — Prototype the OAuth problem before you build anything else

**Do this task early. Out of order if you like. It is the one thing that could break
the design.**

Tier B services, HubSpot and GoHighLevel, use OAuth. OAuth opens a browser. Our AIOS
runs on a headless server with no browser and no screen. `claude mcp login <name>
--no-browser` prints a link the owner can open on their laptop, but the reply from the
login has to get back to a port on the server.

**DO:** On a real VPS with no desktop, try to connect HubSpot end to end. Write down
exactly what happens in `decisions/oauth-on-a-headless-server.md`. Then pick one:

- It works with `--no-browser` plus an SSH tunnel → document the steps and ship it.
- It does not work → Tier B services connect through Composio instead, which handles
  the login on its own servers. Say so plainly and move on.

**Do not guess.** Do not write curriculum for Tier B until this file exists with a real
answer in it.

Two notes for when you get there:

- HubSpot through Composio currently shows the owner an **"unverified app" warning**
  during login, because Composio's shared HubSpot app is still waiting on approval. To a
  non-technical business owner that looks like a scam. Fix: we register our own HubSpot
  OAuth app and ship its ID, which we should do anyway.
- GoHighLevel's own MCP server is worth copying as a design. It exposes only **four**
  tools — list locations, search operations, describe operation, execute operation — and
  those four front over 550 operations. That is how you avoid the tool-count problem in
  Task 4.2. If our generic bridge grows past a handful of services, switch it to this
  shape: one `search_operations` tool and one `execute_operation` tool per service,
  instead of hundreds of individual tools.

### Task 4.6 — Show the tentacles on the dashboard

**DO:** Add a `Connections` panel. One row per tentacle, gathered from `claude mcp list`
plus Composio's connected accounts. Each row shows the name, the tier, whether its
environment variable is actually set, how many tools it exposes, and the result of the
last test call.

**CHECK:** Every tentacle you set up appears. Remove a key from `.env`, restart, and the
row turns into a warning that names the missing variable. It must not disappear
silently, and it must not just say "error".

### Task 4.7 — Keys without keys, if you have time

`headersHelper` in the MCP config points at a program that prints auth headers instead
of putting them in the config at all. That lets the vault hand out short-lived tokens.

```json
"my-api": {
  "type": "http",
  "url": "${API_BASE_URL}/mcp",
  "headersHelper": "/opt/aios/bin/get-auth-headers.sh",
  "timeout": 300000
}
```

**DO:** This is a nice-to-have. `${VAR}` is already secure enough for launch. Do it
only after Builds 1 to 5 are finished, and only if a service needs refreshing tokens.

**CHECK:** The helper script prints valid headers and is `chmod 700`, owned by `aios`.

---

# BUILD 5 — The Vault

Their API keys and their company documents. On their own server. This is why we chose
student-owned hosting: we never hold anyone else's keys or documents.

### Task 5.1 — The folders

**DO:** Create this layout on the server, at `/opt/aios`.

```
/opt/aios/
  .env              chmod 600   all API keys live here, nowhere else
  app/                          the repo
  vault/
    documents/                  what they upload
    documents/processed/        after reading
    context/                    what the agents actually read
  var/
    activity.jsonl              the feed
```

Rules:

- `.env` is `chmod 600`, owned by the `aios` user. Nothing else reads it.
- `vault/` is `chmod 700`.
- `.env` and `vault/` are in `.gitignore`. Check this before your first commit.
- **Nothing writes a key anywhere except `.env`.** Not the yaml files, not
  `settings.json`, not the activity log, not the dashboard.

**CHECK:**
```bash
ls -la /opt/aios/.env          # -rw------- aios aios
git check-ignore -v .env vault # both ignored
grep -rIE 'sk-|ak_|xi-api' --exclude-dir=.git . | grep -v value_from_env
```
That last command must print nothing.

### Task 5.2 — Read their documents

**DO:** Create `skill-vault/ingest/SKILL.md`.
Wing `intelligence`, department `Knowledge`, function `Document Extraction`.

The owner drops files into `vault/documents/`. This agent reads each one and writes
what it learned into `vault/context/`.

- Handles `.md`, `.txt`, `.pdf`, `.csv`, `.docx`. Use `pypdf` for PDFs. Add it to
  `requirements.txt`.
- **Never overwrite an existing context file.** Either add a new dated section at the
  bottom, or write `<name>.proposed.md` next to it for the owner to approve.
- When a file is done, move it to `vault/documents/processed/`.
- If a file has no readable text, usually a scanned photo saved as PDF, say so by name.
  Never skip a file quietly.

**CHECK:** Drop in a 3-page PDF and a CSV. Run it. The context files gained accurate
content, both source files moved to `processed/`, and nothing that already existed was
overwritten.

### Task 5.2b — Search their documents for free, on Tier 1

**The problem this solves.** Once the owner has uploaded their business, agents constantly
need one paragraph out of forty pages — "what does my onboarding doc say about refunds."
The lazy answer is to hand the whole folder to Claude on every question. On a subscription
with a five-hour window, that is the fastest way to a silent AIOS by Wednesday. **This is
the largest avoidable token cost in the product.**

**DO:** Build vault search on the Tier 1 local embedding model from Task 0.5. No Claude in
the retrieval path at all.

1. `scripts/index_vault.py` — walks `vault/documents/processed/` and `vault/context/`,
   splits each file into passages of a few hundred words, calls `local_model.embed()`, and
   appends `{file, passage, offset, vector}` to `vault/index.jsonl`. Append-only, one line
   per passage, consistent with the no-database rule.
2. `scripts/search_vault.py "query"` — embeds the query, cosine-compares against the index,
   returns the top few passages with their filenames.
3. Re-index on the same timer that runs `ingest`, not on every question.

**Then the only Claude-shaped part:** an agent that needs vault content calls
`search_vault.py` and receives five passages instead of forty pages. **Claude reads the
answer, not the archive.**

Rules:

- **Cite the file every time.** A passage returned without its filename is an invitation to
  invent a source, and the spec bans an agent inventing anything.
- **Falls back to keyword search** when no local model is installed, per Task 0.5. Vault
  search must work on a box with no model at all, just less well.
- **The index is as private as the documents.** `vault/index.jsonl` lives under the
  `chmod 700` vault and is never served by the dashboard. It contains verbatim passages of
  the customer's business.
- **Never send the whole index to a model.** If a query matches nothing, say nothing
  matched.

**CHECK:** Ask a question whose answer is one line on page 30 of a PDF. The right passage
comes back with the right filename. Then confirm the search cost zero tokens — the activity
log shows a vault search with no model invocation. Delete the local model and confirm it
still answers, by keyword, without erroring.

### Task 5.3 — The interview

**DO:** Create `skill-vault/onboard/SKILL.md`. This fills in every context file the
other agents say they need.

- Read every skill's `requires-context`. Combine them into one list. **Drive the
  interview from that list.** Do not hardcode the questions. When someone adds an
  agent next month, the interview grows by itself.
- Ask **one question at a time.** Never a wall of twenty.
- Show progress: `3 of 9 done`.
- If a context file already exists, skip it and say so. The owner can stop and come
  back.

**CHECK:** On a fresh clone with an empty `context/`, run `onboard`, answer the
questions, then confirm every file listed in any `requires-context` now exists and is
not empty.

### Task 5.4 — Put it on a server, in one command

**DO:** Create `deploy/install.sh`. Target: a brand new Ubuntu 24.04 box, run as root.
Recommended: Hetzner CX22, about five dollars a month.

Steps, in order, printing `[4/15] ...` as it goes:

```
1.  Stop if this is not Ubuntu 24.04, or if /opt/aios already exists.
    Stop if ANTHROPIC_API_KEY is set in the environment, and say why:
    this system runs on a subscription, and that variable means per-token
    billing. See Build 0.
2.  apt-get install: python3 python3-pip python3-venv git ffmpeg curl ca-certificates
3.  Install Node 22. Claude Code and Remotion need it.
4.  npm install -g @anthropic-ai/claude-code
5.  Create the aios user, no shell login. Make the folders from Task 5.1.
6.  Clone the repo to /opt/aios/app. chown -R aios:aios /opt/aios
7.  Make the venv, pip install -r app/dashboard/requirements.txt
8.  Ask for: TELEGRAM_BOT_TOKEN, GROQ_API_KEY, ELEVEN_API_KEY (optional),
    DASHBOARD_PASSWORD, domain name (optional).
    Write them to /opt/aios/.env, chmod 600.
    Do NOT ask for ANTHROPIC_API_KEY. It is not part of this product.
9.  Tier 2 auth. Print the instruction to run, as the aios user:
        sudo -u aios claude setup-token
    Explain in one line: it prints a link, approve it on your phone, paste the
    code back. Then verify with `sudo -u aios claude -p "say ok"` and do not
    continue until it returns ok. This is the step that lets the timers run
    while nobody is logged in.
10. Tier 1, optional and never fatal. Download the local embedding model
    (about 130 MB) so vault search costs nothing. If the download fails, or
    if /proc/meminfo shows under 1 GB usable, warn once and carry on —
    vault search falls back to keyword matching (Task 5.2b).
11. Install systemd services aios-bridge and aios-dashboard.
    Both: EnvironmentFile=/opt/aios/.env, User=aios, Restart=always.
12. If they gave a domain: install Caddy, reverse proxy that domain to
    127.0.0.1:8000. Caddy gets the HTTPS certificate on its own.
    If they gave no domain: bind the dashboard to 127.0.0.1 only and print
    SSH tunnel instructions.
    Never expose the dashboard over plain HTTP. A password over HTTP is
    a password in public.
13. python3 scripts/build_map.py, then python3 scripts/build_diagrams.py
    Node is already there from step 3, so archify needs no extra install.
    If the diagram step fails, warn and carry on. The dashboard falls back to
    the plain map and a failed diagram must never fail an install.
14. systemctl enable --now aios-bridge aios-dashboard
15. Print the dashboard address, how to check status, where the logs are.
```

Rules:

- `set -euo pipefail` on line one.
- Safe to run twice. If `/opt/aios` exists it stops and explains, it does not overwrite.
- On failure, print which numbered step failed and how to retry it.
- **Steps 9 and 10 are the two tiers, and they fail differently on purpose.** Step 9 is
  mandatory: without Tier 2 there is no product, so it blocks. Step 10 is an optimisation:
  it warns and continues. Never let them behave the same way.

**CHECK:** On a brand new box, one command finishes in under ten minutes and the
dashboard loads over HTTPS. Then **destroy the box and do it again from scratch.**
Twice clean, or it is not done.

### Task 5.5 — Make it run on schedule

Day 7 currently teaches `cron`. On a server use systemd timers instead. They log
properly and they survive a reboot.

**DO:** Create `deploy/timers/` with a `.service` and a `.timer` for each scheduled
job: morning brief, weekly newsletter, inbox triage. Each one runs the skill and calls
`activity.log()`.

**CHECK:** `systemctl list-timers | grep aios` shows the next run times. Force one with
`systemctl start aios-brief.service` and see it land in the dashboard feed.

---

# BUILD 6 — The Panels: every section built out

Build 1 gives you the map: which agents exist and what they do. That is the skeleton.
This build is the flesh. Click Marketing and you see your actual numbers. Ask what is
happening with your Instagram and you get a chart, on the dashboard or on your phone.

## The rule that makes this possible. Read it twice.

There are seven wings and there will be dozens of connected services. If you build a
bespoke page per section you will never finish, and every new service will mean new code.

**So: one pattern, no bespoke pages. A panel is a list of cards, and a card is a file,
not code.**

```yaml
# panels/content.yaml — the Content wing's panel
cards:
  - title: Skool members
    shape: kpi
    source: { connection: skool, operation: skool_community_info, field: members }
    compare: last_week

  - title: Skool engagement, 30 days
    shape: line
    source: { connection: skool, operation: skool_posts_list, aggregate: comments_per_day }

  - title: Posts published this week
    shape: bar
    source: { connection: blotato, operation: list_published_posts, group_by: platform }

  - title: Views by platform, 30 days
    shape: line
    source: { connection: blotato, operation: analytics, metric: views, group_by: platform }

  - title: Waiting for approval
    shape: table
    source: { local: drafts/, columns: [file, agent, age] }
```

Adding Instagram later means **adding five lines to a yaml file.** It never means writing
a new page. If you find yourself writing a second chart component, stop, you have taken
the wrong turn.

### Task 6.1 — Collect the numbers on a schedule, never on page load

**DO:** Create `scripts/collect.py`. A timer runs it every 30 minutes. For every card in
every panel it calls the connection, and appends the raw answer to
`var/metrics/<card-id>.jsonl` with a timestamp.

Rules:

- **The dashboard never calls an API.** It reads files. This is not an optimisation. If
  the page calls live APIs it will be slow, it will hit rate limits, Blotato's is 30 a
  minute, and one dead service will hang the whole page.
- **Append, never replace.** The history is what makes a line chart possible. From the
  first day it collects, they have a time axis. If you overwrite, they have a number and
  no story, and the dashboard looks like a settings screen.
- If a service fails, write a row with `"status":"error"` and the reason. Do not skip
  silently, or the chart will show a straight line through a real outage.
- Every card gets a stable `id` so its history survives a title change.

**CHECK:** Let it run for an hour. `var/metrics/` has one file per card with at least two
timestamped rows. Kill a service's key and confirm the next run records an error row
rather than nothing.

### Task 6.2 — One chart renderer, two destinations

This is the most important decision in this build, so here is the reasoning before the
task.

The owner wants charts on the dashboard **and** the same answer on Telegram when they are
away from the laptop. A JavaScript chart library only solves the first one, and then
Telegram needs a headless browser to screenshot it. That is a whole second machine to
maintain.

**So we generate SVG on the server, in Python.** The dashboard drops the SVG straight
into the page, crisp at any size, no JavaScript. Telegram gets the same SVG converted to
PNG. One renderer, one visual language, both destinations, no build step.

**DO:** Create `scripts/chart.py`. It takes a small spec and returns an SVG string.

```python
render({"shape": "line",
        "title": "Views by platform, 30 days",
        "series": [{"label": "Instagram", "points": [[date, value], ...]},
                   {"label": "TikTok",    "points": [[date, value], ...]}],
        "note": "from Blotato"})   ->  "<svg ...>...</svg>"
```

**Five shapes and no more:** `kpi` a single big number with its change, `line`, `bar`,
`table`, `donut`. Five shapes cover every example the owner described. A sixth shape is
scope creep, resist it.

Rules:

- Same palette and same fonts as the dashboard. One accent colour. Charts that do not
  match the page look bolted on, and this is the screenshot that sells the product.
- **Every chart states where its numbers came from and when they were collected**, in
  small text at the bottom. "from Blotato, 14 minutes ago". A chart with no source is a
  chart nobody trusts.
- Readable at 700 pixels wide, because that is roughly how wide a Telegram photo is on a
  phone.
- For PNG, use `cairosvg`. Add it to `requirements.txt`. If it is missing, send the
  numbers as text rather than crashing.

**CHECK:** Render all five shapes to files and open them. Then send one to Telegram and
look at it on a real phone. If you cannot read the axis labels, the font is too small.

### Task 6.2b — The second renderer: diagrams, not charts

Task 6.2 covers numbers. It does not cover **structure**, and structure is half of what
makes this product legible to someone non-technical. "How is my AIOS actually wired?"
"What does the inbox agent do when it runs, and where does it stop and wait for me?"
Those are diagrams, and a line chart cannot answer them.

**Use `tt-a1i/archify` for these. Do not hand-build them.**

| | |
|---|---|
| Repo | `github.com/tt-a1i/archify` |
| Stars | 52,691 |
| Licence | **MIT** |
| What it is | A Claude skill. Give it typed JSON, get a self-contained interactive HTML diagram with inline SVG, light and dark, and PNG / SVG / WebM export. |
| Types | `architecture`, `workflow`, `sequence`, `dataflow`, `lifecycle` |
| Runtime cost | **Node 18+ and nothing else.** Verified: every file imports only `node:` builtins. `ajv`, `parse5`, `saxes` and `simple-icons` are dev dependencies. **There is no `npm install` and no build step.** |

That last row is why this is allowed in. Our rule was never "no JavaScript", it was **no
build step and no dependency tree**. A generator that runs on the server, needs only Node
itself, and emits static HTML does not break that rule. Confirm it yourself before you
commit to it: `grep -rE "^import .* from '[^.]" archify/renderers archify/bin` should
show only `node:` imports.

**Map each type to a question the owner actually asks:**

| Type | What we render with it |
|---|---|
| `architecture` | **The map itself.** Wings, departments, agents, generated from `map.json`. This replaces hand-building the map in Task 1.6 and it is the sales-page screenshot. |
| `dataflow` | "Show me how my AIOS is wired." Which agents read which context, which tentacles they reach, where the output lands. |
| `workflow` | "What does this agent actually do?" Its steps **including the approval gate.** This is the teaching device for the autonomy ladder. |
| `lifecycle` | The ladder itself: manual to assisted to autonomous. Its state model handles a recoverable failure state, which is exactly what an agent that stops and asks looks like. |
| `sequence` | Debugging a run that went wrong. Internal, not customer-facing. |

**DO:**

1. Vendor it into `vendor/archify/` and **pin the version.** It was created in April 2026
   and is on `2.17.0-dev.1` with commits landing daily. Record the commit SHA you pinned
   in `imports/ATTRIBUTION.md` with its MIT notice.
2. Neutralise the packaged update checker. It reaches out to compare versions, and a
   customer's business dashboard must not make surprise outbound calls or nag them to
   upgrade something they did not install. Pin, and do not run `scripts/check-update.mjs`.
3. Write `scripts/build_diagrams.py` — reads `map.json`, emits archify JSON, calls
   `node vendor/archify/bin/archify.mjs deliver <type> <in.json> <out.html>`.
4. **Generate diagrams on the timer, alongside the metric collector. Never live on
   request.** Two reasons. Archify's own instructions demand a validate-and-repair loop
   with nine artifact checks before it accepts an artifact, which is slow and token-hungry
   and can loop. And the structure only changes when an agent or connection changes, so
   there is nothing to gain from doing it live.
5. Archify emits a *standalone* page, and our dashboard is one page of bands. Either
   iframe the artifact or lift the inline SVG out of it. **Pick one and use it
   everywhere.** Do not do both, or the two will drift and look different.
6. Use its PNG export for the Telegram path, same as Task 6.2.
7. Skip `bin/visual-check.mjs` on customer servers. It spawns a browser. It is a
   development check for us, not something a customer's VPS should ever run.

**CHECK:** `map.json` produces an architecture diagram of all seven wings that you would
put on the sales page without editing. It renders with Node installed and **no
`node_modules` directory anywhere.** Then run it on a box with Node absent and confirm the
dashboard still loads and still shows every number, with the diagrams degrading to the
plain agent list rather than the page breaking.

**The division of labour, and do not blur it:**

> **Numbers over time go to the Python SVG renderer. Structure and flow go to archify.**

They are not competing and neither one replaces the other. If you find yourself trying to
make archify draw a bar chart of Instagram views, you have crossed the line and it will
fight you. If you find yourself hand-coding boxes and arrows in Python, you have crossed
it the other way.

### Task 6.3 — Ask for a chart in plain English

**DO:** Create `skill-vault/chart/SKILL.md`. This runs when the owner says "what is going
on with my Instagram" or "show me my Skool engagement".

1. Work out which numbers answer the question.
2. Read them from `var/metrics/`. **Do not call the API.**
3. Build the spec and call `scripts/chart.py`.
4. Send it where the question came from. Dashboard question, SVG in the page. Telegram
   question, PNG through Telegram's `sendPhoto`.
5. Write two or three sentences saying what the chart shows. The chart is the evidence,
   the sentences are the answer.

Rules:

- **Never invent a number.** If the metric was never collected, say exactly which card is
  missing and which connection would supply it. A plausible fake chart is the worst
  possible failure here, worse than no chart.
- If there is under a week of history, say so on the chart. Do not draw a trend line
  through four points and imply a trend.

**CHECK:** From Telegram, ask "how is my Skool doing this month" and get a readable
picture plus a short answer. Ask about a service you have not connected and get a
straight "you have not connected X yet", not an invented chart.

### Task 6.4 — Write the six panels

**DO:** Create one yaml file per wing in `panels/` — **seven files.** Start with the cards
below. These are a starting point, not a limit.

| Wing | Cards |
|---|---|
| **Intelligence** | things needing you today · sources watched · what changed this week · last brief |
| **Content** | Skool members and change · Skool engagement over time · posts published by platform · views by platform · drafts awaiting approval |
| **Growth** | leads scored this week · A/B/C split · reply rate on outreach · follow-ups due today · pipeline by stage |
| **Comms** | unread and triaged · drafts waiting for you · today's calendar · average time to reply |
| **Back office** | invoices out and unpaid · expenses this month · documents processed · what is still missing from the brain |
| **Command** | agents run in the last 7 days · failures and why · cost this month by service · connections and their health |
| **Build** | projects on the go · what changed this week · what is broken right now · last deploy |

**Every card needs a designed empty state.** This is the thing that decides whether the
product looks finished or looks broken. A card with no data yet says
`Connect Blotato to see your views` with a button, styled to look deliberate. **It never
shows a blank box, and it never shows a zero.** A zero that means "not connected" reads
as "my business has no views", which is worse than showing nothing.

**CHECK:** Open the dashboard on a fresh install with nothing connected. Every panel is
full of clear invitations and not one broken or empty box. Screenshot it. If that
screenshot is not good enough to put on the sales page, the empty states are not done.

### Task 6.5 — Skool. We already have this working.

We already have working Skool access over MCP in this project. The available operations
include community info, member list, pending members, post list, comments, notifications,
courses and lessons. That covers members, engagement, posts and DMs, which is most of
what the owner described for the Content wing.

**DO:** Wire the Skool MCP server as a Tier A tentacle in Build 4, then fill in the Skool
cards in `panels/content.yaml` from its real operations.

**CHECK:** The Content panel shows a real member count and a real engagement line drawn
from actual Skool data, not sample data.

### Task 6.6 — Social numbers. Take the easy road, not the obvious one.

The obvious road is the Instagram API directly. **Do not start there.** Instagram
insights require a Business or Creator account linked to a Facebook Page, a Meta
developer app, and Meta's app review for the insights permission. That is weeks of
review, and it is nothing like pasting a key. For a seven-day challenge it is a wall.

The easy road: **Blotato already has analytics endpoints**, and the owner connects it with
one pasted key. It gives views, engagement and comments across the platforms it posts to.
One connection covers Instagram, TikTok, LinkedIn and the rest.

**DO:** Build all social cards against Blotato first. Put direct Meta access on the later
list, and only if customers ask for numbers Blotato does not carry.

**CHECK:** The Content panel shows views per platform from a single pasted key, with no
Meta developer account anywhere in the setup.

---

The brain, how it connects and what it costs, is **Build 0**. It is at the front of this
plan because nothing else runs without it.

---

# What ships when

Build 6 roughly doubles the work. Sept 14 is a pre-sale, so what we promise has to be
what we deliver. Here is the split.

**Sept 14, real on the day:** Build 0 working on a subscription, the map, all 150 agents,
voice both ways, the vault, the installer, Composio and Google, Blotato, and **two panels
fully finished** — Command, because it needs no outside connection, and Content, because it
is the one with the best screenshot in it.

**Weekly drops after:** the other five panels, one per week, each with its cards and its
empty states. Then new agents on request from the community.

**Say the panel schedule out loud on the sales page.** "All 150 agents on day one, seven
department dashboards with two live at launch and one more every week" is a promise we keep,
and it is a stronger offer than a vague "fully built out" because it is specific. **The
library is the thing to lead with, because that is the part that is genuinely complete.**

**What to hold back from the sales page:** do not promise `autonomous` behaviour at launch.
The library ships at `manual` and `assisted`, and customers promote agents up the ladder
themselves. Sell that as the method, which it is.

---

# How this maps to the 7 days

The seven days are the setup. This is what each day installs.

| Day | What they set up | Build |
|---|---|---|
| 0 | **Buy the Claude plan.** Their server, one command, `claude setup-token`. Dashboard loads. | 0, 5.4 |
| 1 | The interview. Their business goes into the brain. | 5.3 |
| 2 | Upload company documents. Watch the brain fill up. | 5.2 |
| 3 | Meet the map. Turn on their first agents. | 1 |
| 4 | Content and video. Remotion. | existing |
| 5 | Connect Google, then connect their own tools. | 4 |
| 6 | Telegram. Talk to it, it talks back. | 2 |
| 7 | Schedules and their numbers. It runs without them. | 5.5, 6 |

Day 7 gains the best moment in the challenge, so build it that way. Once the collector
has run even once, they ask their own AIOS a question about their own business and get a
chart back. **That is the screenshot they post**, and it is the last thing they do before
the challenge ends, which is exactly where you want it.

That is a real seven days of work. Not seven days of reading.

---

# Appendix A — Environment variables

**On the brain, read Build 0 first.** Customers authenticate with `claude setup-token`
against a Claude subscription and set **none** of the variables in this first block. They
exist only for the owner's Bedrock test box.

| Name | Needed for |
|---|---|
| `ANTHROPIC_API_KEY` | **Nobody. Do not set this.** Per-token billing is what Build 0 exists to avoid. Its presence on a customer box is a bug. |
| `CLAUDE_CODE_USE_BEDROCK` | owner's AWS box only, set to `1` |
| `AWS_REGION` | owner's AWS box only |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | owner's AWS box. **Pin it, or Bedrock bills at the Opus rate.** |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL` | owner's AWS box, for the cheap background work |
| `TELEGRAM_BOT_TOKEN` | Telegram |
| `TELEGRAM_CHAT_ID` | locking the bot to one person |
| `GROQ_API_KEY` | hearing voice notes |
| `ELEVEN_API_KEY` | speaking back |
| `ELEVEN_VOICE_ID` | speaking back |
| `DASHBOARD_PASSWORD` | the dashboard |
| `COMPOSIO_API_KEY` | Google Workspace |
| `SOCIALCLAW_API_KEY` | social posting |
| `BLOTATO_API_KEY` | Blotato. **Quote it** — it usually ends in `=` |
| `MANYCHAT_API_KEY` | ManyChat |
| `AIOS_LOCAL_MODEL_URL` | Tier 1 only. Where the local model listens, default `http://127.0.0.1:11434`. Optional — unset means Tier 1 is off and vault search uses keywords. |
| `OPENROUTER_API_KEY` | **The advanced library module only (Task 0.6), never the curriculum.** If this is set on a box, `config/models.yaml` must say `route: openrouter` and a prepaid cap must be in place. |

All of them live in `/opt/aios/.env`, `chmod 600`, and nowhere else.

**Tier 1 must never need a key.** `AIOS_LOCAL_MODEL_URL` is a loopback address, not a
credential. If you find yourself adding an API key to make Tier 1 work, you have built a
hosted service and called it local.

Config files only ever hold `${THE_VARIABLE_NAME}`. Never a key.

# Appendix B — Things that have already gone wrong

1. **Skill frontmatter.** Custom fields go under `metadata:`. See "Two mistakes" at the
   top. This has broken skills twice already.
2. **YAML.** A list item starting with `"` is a parse error. Wrap the whole item in
   single quotes.
3. **Remotion.** Needs about 2 GB free for the Chrome headless shell on the first
   render. The command is `npx remotion render index.jsx <Composition> out.mp4` — it
   fails without the entry point. A 23-second vertical video takes about 2 minutes.
4. **Telegram voice notes** must be OGG/Opus. Send mp3 and it appears as a file
   attachment instead of a voice note.
5. **Composio** has no web page for creating MCP sessions. Use
   `scripts/create_composio_session.py`.
6. **`claude -p` needs the 300 second timeout** that `bridge.py` already has. Do not
   lower it. Longer skills will hit it.
7. **`contains-studio/agents` has no licence.** Do not copy from it. Ever.
8. **An unset `${VAR}` in an MCP config does not fail.** Claude Code passes the literal
   text through and only warns. The owner then sees a 401 they cannot explain. Check
   every referenced variable exists before you start anything.
9. **Blotato keys usually end in `=`.** An unquoted `=` gets mangled by shells and
   `.env` parsers. Their own docs call this the top cause of 401s. Quote the value.
10. **`api.blotato.com` does not exist.** The real host is `backend.blotato.com`.
    Models invent the wrong one constantly.
11. **Never register a big API without a tool whitelist.** HubSpot alone is 245 tools.
    Loading hundreds of tools makes Claude slower and worse at everything, and it will
    look like a Claude fault rather than your bug.
12. **`modelcontextprotocol/servers` on GitHub is not a server directory any more.**
    It holds seven reference examples. Use the registry API instead.
13. **`gh repo view` uses `stargazerCount`. `gh search repos` uses `stargazersCount`.**
    Singular and plural, different subcommands. The wrong one errors with
    "Unknown JSON field", which reads like the field does not exist.
14. **Archify is a skill, not a library, and its instructions are demanding.** It wants a
    validate-and-repair loop and will not accept an artifact until nine checks pass. That
    is why we run it on a timer and never live inside a customer's question. Left
    unbounded it can spend a long time repairing one diagram.
15. **Archify is very new and moves fast.** Created April 2026, still on a `-dev` version,
    commits daily. Pin a SHA. Do not track its main branch on customer servers.

# Appendix C — Not finished until all of these are true

- [ ] A customer-shaped box runs entirely on `claude setup-token` with **no**
      `ANTHROPIC_API_KEY` set anywhere, and timers fire with nobody logged in
- [ ] One box ran a full week on the cheapest recommended plan with the default schedule on,
      without hitting a weekly limit, and the recommendation cites that measurement
- [ ] `grep -rn "ANTHROPIC_API_KEY" curriculum/ deploy/` finds nothing that tells a customer
      to set one. The only permitted hit is `deploy/install.sh` refusing to run when it
      is already set.
- [ ] `scripts/collect.py` invokes no model — the dashboard refreshes for zero tokens
- [ ] Vault search invokes no Claude — a search over a 40-page PDF costs zero tokens, and
      the activity log proves it
- [ ] Every skill's `metadata.model` is `fast`, `smart` or `deep`. `grep -rn "model: sonnet\|model: opus\|model: haiku" skill-vault/` prints nothing
- [ ] Changing `route:` in `config/models.yaml` changes the model every agent actually runs
      on, with no skill file edited, proven from the activity log
- [ ] The install works end to end on a box with **no** local model installed, and vault
      search still returns answers by keyword
- [ ] The installer refuses to start when `ANTHROPIC_API_KEY` is set, and says why
- [ ] No skill ships as `autonomy: autonomous` at launch
- [ ] Every file from the zip that ships has a licence recorded in `imports/ATTRIBUTION.md`
- [ ] `python3 scripts/validate_skills.py` exits 0
- [ ] `python3 scripts/build_map.py` shows 150 or more agents
- [ ] Every agent in the vault has been run once by a human who read the output
- [ ] `grep -rl "You are a" skill-vault/` prints nothing. Skills are procedures, not
      personas. A hit means an imported file was edited instead of rewritten.
- [ ] No skill contains a KPI it cannot count from its own output
- [ ] `imports/ATTRIBUTION.md` covers every imported file, with the MIT notices
- [ ] Fresh Ubuntu box, one command, dashboard over HTTPS, done twice
- [ ] Voice note in, voice note out, on a real phone
- [ ] A tentacle added by pasting a key, working, with the key only in `.env`
- [ ] Blotato connected through its own MCP server, accounts listed by name
- [ ] ManyChat connected through the generic bridge, under 25 tools registered
- [ ] `decisions/oauth-on-a-headless-server.md` exists with a real tested answer
- [ ] Every `${VAR}` in every MCP config has a matching entry in `.env`
- [ ] Every card in every panel has a designed empty state, and a fresh install with
      nothing connected screenshots well enough for the sales page
- [ ] All five chart shapes render, and one has been read on a real phone via Telegram
- [ ] The archify map diagram is good enough for the sales page with no hand editing
- [ ] `find vendor/archify -name node_modules` prints nothing
- [ ] The pinned archify commit SHA and its MIT notice are in `imports/ATTRIBUTION.md`
- [ ] Nothing on a customer server runs archify's update checker or `visual-check.mjs`
- [ ] Rename Node out of `PATH` and confirm the dashboard still loads, still shows every
      number, and falls back to the plain map instead of breaking
- [ ] Asking about an unconnected service returns "not connected yet", never a chart
- [ ] Every chart on screen names its source and how old the numbers are
- [ ] Kill a connection's key, and the next collector run writes an error row rather
      than a silent gap in the chart
- [ ] The dashboard makes zero outbound API calls when a page loads
- [ ] `grep -rIE 'sk-|ak_|xi-api' --exclude-dir=.git .` prints nothing
- [ ] A stranger completes Day 0 to Day 7 using only the written docs

