import json
import textwrap

from scripts.build_map import build_map


SKILL = textwrap.dedent("""---
name: scout
description: Gather verified facts.
metadata:
  wing: intelligence
  department: Intelligence
  function: Scout
  replaces: Manual research.
  the-human: The owner decides what matters.
  ladder:
    manual: Search manually.
    assisted: Gather and summarize.
    autonomous: Gather on schedule.
  trigger: A scheduled run.
  outputs:
    - Brief
  kpis:
    - Sources checked
  tools:
    - claude
  model: deep
  autonomy: assisted
  scaffolding-phase: 1
---

## What this does
Gather facts.
""")

def test_build_map_groups_and_counts(tmp_path):
    skill = tmp_path / "skill-vault" / "scout" / "SKILL.md"
    skill.parent.mkdir(parents=True)
    skill.write_text(SKILL, encoding="utf-8")
    registry = tmp_path / "references" / "tool-registry.md"
    registry.parent.mkdir(parents=True)
    registry.write_text("| key | Display name | Brand hex |\n|---|---|---|\n| claude | Claude | #D97757 |\n", encoding="utf-8")
    result = build_map(tmp_path)
    assert result["counts"]["total"] == 1
    assert result["wings"][0]["wing"] == "intelligence"
    assert result["wings"][0]["departments"][0]["functions"][0]["agents"][0]["name"] == "scout"
    output = json.loads((tmp_path / "dashboard" / "static" / "map.json").read_text())
    assert output["counts"]["assisted"] == 1
