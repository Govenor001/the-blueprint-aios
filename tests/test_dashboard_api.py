import base64
import json
import textwrap

from fastapi.testclient import TestClient

from dashboard.server import create_app
import dashboard.server as dashboard_server


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
    monkeypatch.setenv("CLAUDE_CODE_USE_BEDROCK", "1")
    monkeypatch.setenv("AWS_REGION", "us-east-1")
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "present")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "present")
    monkeypatch.setenv("BLOTATO_API_KEY", "present")
    skill = tmp_path / "skill-vault" / "scout" / "SKILL.md"
    skill.parent.mkdir(parents=True)
    skill.write_text(SKILL, encoding="utf-8")
    registry = tmp_path / "references" / "tool-registry.md"
    registry.parent.mkdir(parents=True)
    registry.write_text("| key | Display name | Brand hex |\n|---|---|---|\n| claude | Claude | #D97757 |\n", encoding="utf-8")
    panels = tmp_path / "config" / "panels"
    panels.mkdir(parents=True)
    (panels / "intelligence.yaml").write_text(
        "cards:\n  - id: intelligence-signals\n    title: Latest verified signals\n    shape: table\n    source: {local: context}\n",
        encoding="utf-8",
    )
    settings = tmp_path / ".claude" / "settings.json"
    settings.parent.mkdir(parents=True)
    settings.write_text(
        '{"mcpServers":{"blotato":{"url":"https://mcp.blotato.com/mcp","headers":{"blotato-api-key":"${BLOTATO_API_KEY}"},"tier":"A"}}}',
        encoding="utf-8",
    )
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
    models = tmp_path / "config" / "models.yaml"
    models.write_text(
        "route: claude-subscription\ntiers:\n  claude-subscription:\n    fast: haiku\n    smart: sonnet\n    deep: opus\n",
        encoding="utf-8",
    )
    launched = {}

    def fake_popen(command, **kwargs):
        launched["command"] = command
        launched["kwargs"] = kwargs

    monkeypatch.setattr(dashboard_server.subprocess, "Popen", fake_popen)
    accepted = client.post(
        "/api/run",
        headers=headers,
        json={"skill": "scout", "input": "Find three verified signals."},
    )
    assert accepted.status_code == 202
    assert "Find three verified signals." in launched["command"]
    assert launched["kwargs"]["cwd"] == tmp_path
    assert json.loads(client.get("/api/map", headers=headers).text)["counts"]["total"] == 1
    activity = client.get("/api/activity?limit=10", headers=headers)
    assert activity.status_code == 200
    assert activity.json() == {"items": []}
    connections = client.get("/api/connections", headers=headers)
    assert connections.status_code == 200
    assert "connections" in connections.json()
    telegram = next(item for item in connections.json()["connections"] if item["name"] == "Telegram")
    assert telegram["status"] == "connected"
    brain = next(item for item in connections.json()["connections"] if item["name"] == "Claude via Bedrock")
    assert brain["status"] == "connected"
    panel_cards = client.get("/api/panels", headers=headers).json()["panels"][0]["cards"]
    assert panel_cards[0]["id"] == "intelligence-signals"
    metrics = tmp_path / "var" / "metrics"
    metrics.mkdir(parents=True)
    (metrics / "intelligence-signals.jsonl").write_text(
        '{"status":"available","value":3,"source_label":"fixture","retrieved_at":"2026-01-01T00:00:00+00:00"}\n',
        encoding="utf-8",
    )
    chart = client.get("/api/chart/intelligence-signals", headers=headers)
    assert chart.status_code == 200
    assert chart.headers["content-type"].startswith("image/svg+xml")
    assert "fixture" in chart.text
    mcp = next(item for item in connections.json()["connections"] if item["name"] == "MCP: blotato")
    assert mcp["status"] == "connected"

def test_metric_question_never_invents_data(tmp_path):
    skill = tmp_path / "skill-vault" / "scout" / "SKILL.md"
    skill.parent.mkdir(parents=True)
    skill.write_text(SKILL, encoding="utf-8")
    registry = tmp_path / "references" / "tool-registry.md"
    registry.parent.mkdir(parents=True)
    registry.write_text("| key | Display name | Brand hex |\n|---|---|---|\n| claude | Claude | #D97757 |\n", encoding="utf-8")
    panels = tmp_path / "config" / "panels"
    panels.mkdir(parents=True)
    (panels / "content.yaml").write_text("cards:\n  - id: content-views\n    title: Views by platform\n    shape: line\n    source: {connection: blotato, operation: analytics}\n", encoding="utf-8")
    from scripts.build_map import build_map
    build_map(tmp_path)
    client = TestClient(create_app(tmp_path, password="test"))
    auth = base64.b64encode(b"owner:test").decode()
    response = client.post("/api/ask", headers={"Authorization": "Basic " + auth}, json={"question": "how are my views?"})
    assert response.status_code == 200
    assert response.json()["chart_url"] is None
    assert "not connected" in response.json()["message"].lower()

def test_chat_endpoint_runs_brain_and_rejects_unknown_agent(tmp_path, monkeypatch):
    skill = tmp_path / "skill-vault" / "scout" / "SKILL.md"
    skill.parent.mkdir(parents=True)
    skill.write_text(SKILL, encoding="utf-8")
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "models.yaml").write_text("route: claude-subscription\ntiers:\n  claude-subscription:\n    smart: sonnet\n", encoding="utf-8")
    registry = tmp_path / "references" / "tool-registry.md"
    registry.parent.mkdir(parents=True)
    registry.write_text("| key | Display name | Brand hex |\n|---|---|---|\n| claude | Claude | #D97757 |\n", encoding="utf-8")
    from scripts.build_map import build_map
    build_map(tmp_path)
    app = create_app(tmp_path, password="test")
    client = TestClient(app)
    auth = base64.b64encode(b"owner:test").decode()
    headers = {"Authorization": "Basic " + auth}
    assert client.post("/api/chat", headers=headers, json={"scope": "unknown", "message": "hello"}).status_code == 400

    async def fake_to_thread(function, command, **kwargs):
        assert command[:3] == ["claude", "--model", "sonnet"]
        assert "hello brain" in command[-1]
        return dashboard_server.subprocess.CompletedProcess(command, 0, stdout="Brain reply", stderr="")

    monkeypatch.setattr(dashboard_server.asyncio, "to_thread", fake_to_thread)
    response = client.post("/api/chat", headers=headers, json={"scope": "brain", "message": "hello brain"})
    assert response.status_code == 200
    assert response.json()["message"] == "Brain reply"
