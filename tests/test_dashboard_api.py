import base64
import json
import textwrap

from fastapi.testclient import TestClient

from dashboard.server import create_app


SKILL = textwrap.dedent("""---
name: scout
description: Gather verified facts.
metadata:
  wing: intelligence
  department: Intelligence
  function: Scout
  replaces: Manual research.
  the-human: The owner decides.
  ladder:
    manual: Search.
    assisted: Gather.
    autonomous: Schedule.
  trigger: A schedule.
  outputs: [Brief]
  kpis: [Sources checked]
  tools: [claude]
  autonomy: assisted
  scaffolding-phase: 1
---

## What this does
Gather facts.
""")

def test_dashboard_requires_auth_and_rejects_unknown_skill(tmp_path, monkeypatch):
    skill = tmp_path / "skill-vault" / "scout" / "SKILL.md"
    skill.parent.mkdir(parents=True)
    skill.write_text(SKILL, encoding="utf-8")
    registry = tmp_path / "references" / "tool-registry.md"
    registry.parent.mkdir(parents=True)
    registry.write_text("| key | Display name | Brand hex |\n|---|---|---|\n| claude | Claude | #D97757 |\n", encoding="utf-8")
    from scripts.build_map import build_map
    build_map(tmp_path)
    app = create_app(tmp_path, password="test")
    client = TestClient(app)
    assert client.get("/api/map").status_code == 401
    auth = base64.b64encode(b"owner:test").decode()
    headers = {"Authorization": "Basic " + auth}
    assert client.get("/api/map", headers=headers).status_code == 200
    response = client.post("/api/run", headers=headers, json={"skill": "../etc/passwd"})
    assert response.status_code == 400
    assert json.loads(client.get("/api/map", headers=headers).text)["counts"]["total"] == 1
    activity = client.get("/api/activity?limit=10", headers=headers)
    assert activity.status_code == 200
    assert activity.json() == {"items": []}
    connections = client.get("/api/connections", headers=headers)
    assert connections.status_code == 200
    assert "connections" in connections.json()
