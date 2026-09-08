import json

from scripts.metric_query import answer


def test_metric_question_returns_chart_from_local_history(tmp_path):
    panels = tmp_path / "config" / "panels"
    panels.mkdir(parents=True)
    (panels / "content.yaml").write_text(
        "cards:\n  - id: content-views\n    title: Views by platform\n    shape: line\n    source: {connection: blotato, operation: analytics}\n",
        encoding="utf-8",
    )
    metrics = tmp_path / "var" / "metrics"
    metrics.mkdir(parents=True)
    rows = [
        {"status": "available", "value": 10, "source_label": "fixture", "retrieved_at": "2026-01-01T00:00:00+00:00"},
        {"status": "available", "value": 12, "source_label": "fixture", "retrieved_at": "2026-01-02T00:00:00+00:00"},
    ]
    (metrics / "content-views.jsonl").write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
    result = answer(tmp_path, "how are my views doing?")
    assert result["chart_url"] == "/api/chart/content-views"
    assert "fixture" in result["svg"]


def test_metric_question_reports_missing_connection(tmp_path):
    panels = tmp_path / "config" / "panels"
    panels.mkdir(parents=True)
    (panels / "content.yaml").write_text(
        "cards:\n  - id: content-views\n    title: Views by platform\n    shape: line\n    source: {connection: blotato, operation: analytics}\n",
        encoding="utf-8",
    )
    result = answer(tmp_path, "show views")
    assert result["chart_url"] is None
    assert "not connected" in result["message"].lower()
