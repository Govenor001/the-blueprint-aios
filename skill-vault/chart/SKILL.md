---
name: chart
description: Answer a metric question with collected evidence and a source-labelled chart.

metadata:
  wing: command
  department: Command
  function: Reporting
  replaces: Reading disconnected metric exports and guessing at trends.
  the-human: The owner decides what action the evidence supports.
  ladder:
    manual: Build one requested chart from collected files and review it.
    assisted: Prepare a chart and explanation for owner approval.
    autonomous: Generate only after the owner approves the reporting schedule.
  trigger: Run when the owner asks what is happening with a connected metric.
  outputs:
    - A chart with source and collection time
    - A short evidence-based explanation
  kpis:
    - Charts with a verified source
    - Missing data reported without invention
  tools: [claude]
  requires-context: []
  model: smart
  autonomy: assisted
  scaffolding-phase: 3
---

## What this does

Turns a question such as "how is my content doing?" into a chart from the files in
`var/metrics/`. It never calls a live service from the dashboard or invents a number.

## Execution

1. Identify the panel card that answers the question.
2. Read its JSONL history from `var/metrics/` and keep the newest valid rows.
3. If the card is missing, unavailable, or has fewer than two points, say exactly that and
   name the connection or collection needed. Do not manufacture a trend.
4. Build a spec for `scripts/chart.py` using the correct one of `kpi`, `line`, `bar`,
   `table`, or `donut`.
5. Include the real source and `retrieved_at` timestamp in the chart note. If either is
   absent, use `UNAVAILABLE`.
6. Return the chart and two or three sentences that distinguish evidence from advice.

## Safety

The chart is evidence, not permission to publish, spend, send, delete, or change a
connection. Any consequential action waits for the owner.
