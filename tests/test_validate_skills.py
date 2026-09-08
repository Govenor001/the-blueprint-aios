import textwrap

import pytest

from scripts.validate_skills import validate_skill


GOOD = textwrap.dedent("""---
name: qualify
description: Score a lead list.
metadata:
  wing: growth
  department: Sales
  function: Qualification
  replaces: Manual lead triage.
  the-human: The owner chooses who to contact.
  ladder:
    manual: Read the list.
    assisted: Rank the list.
    autonomous: Alert on score changes.
  trigger: A CSV is provided.
  outputs:
    - Ranked table
  kpis:
    - Leads scored
  tools:
    - claude
  requires-context:
    - context/about-business.md
  model: smart
  autonomy: assisted
  scaffolding-phase: 1
---

## What this does
Score leads.
""")

def test_valid_skill_has_no_errors(tmp_path):
    path = tmp_path / "SKILL.md"
    path.write_text(GOOD, encoding="utf-8")
    assert validate_skill(path, {"claude"}) == []

def test_rejects_top_level_custom_fields(tmp_path):
    path = tmp_path / "SKILL.md"
    path.write_text(GOOD.replace("metadata:\n", "scaffolding-phase: 1\nmetadata:\n"), encoding="utf-8")
    errors = validate_skill(path, {"claude"})
    assert any("top-level key" in error for error in errors)

def test_rejects_invalid_tool_and_model(tmp_path):
    path = tmp_path / "SKILL.md"
    bad = GOOD.replace("    - claude", "    - imaginary").replace("model: smart", "model: sonnet")
    path.write_text(bad, encoding="utf-8")
    errors = validate_skill(path, {"claude"})
    assert any("tools" in error for error in errors)
    assert any("model" in error for error in errors)
