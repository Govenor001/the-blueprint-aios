import json

from scripts.chart import render
from scripts.collect import collect


def test_collect_writes_unavailable_rows_without_fake_zero(tmp_path):
    (tmp_path / "config" / "panels").mkdir(parents=True)
    (tmp_path / "config" / "panels" / "content.yaml").write_text(
        "cards:\n  - id: drafts\n    title: Waiting\n    shape: table\n    source: {local: drafts}\n",
        encoding="utf-8",
    )
    assert collect(tmp_path) == 1
    row = json.loads((tmp_path / "var" / "metrics" / "drafts.jsonl").read_text().strip())
    assert row["status"] == "unavailable"
    assert row["value"] is None


def test_collect_records_connection_source_without_calling_live_api(tmp_path):
    (tmp_path / "config" / "panels").mkdir(parents=True)
    (tmp_path / "config" / "panels" / "comms.yaml").write_text(
        "cards:\n  - id: inbox\n    title: Inbox\n    shape: kpi\n    source: {connection: gmail, operation: unread_count}\n",
        encoding="utf-8",
    )
    collect(tmp_path)
    row = json.loads((tmp_path / "var" / "metrics" / "inbox.jsonl").read_text().strip())
    assert row["source_label"] == "gmail: unread_count"
    assert row["status"] == "unavailable"


def test_collect_reads_an_explicit_local_endpoint_and_extracts_field(tmp_path, monkeypatch):
    (tmp_path / "config" / "panels").mkdir(parents=True)
    (tmp_path / "config" / "panels" / "comms.yaml").write_text(
        "cards:\n  - id: inbox\n    title: Inbox\n    shape: kpi\n    source:\n      connection: gmail\n      operation: unread_count\n      endpoint_env: TEST_INBOX_URL\n      field: unread\n",
        encoding="utf-8",
    )

    class Response:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def read(self, limit):
            return b'{"unread": 7}'

    monkeypatch.setenv("TEST_INBOX_URL", "http://127.0.0.1:9999/read")
    monkeypatch.setattr("scripts.collect.urllib.request.urlopen", lambda request, timeout: Response())
    collect(tmp_path)
    row = json.loads((tmp_path / "var" / "metrics" / "inbox.jsonl").read_text().strip())
    assert row["status"] == "available"
    assert row["value"] == 7


def test_chart_has_source_note_for_all_shapes():
    specs = [
        {"shape": "kpi", "title": "K", "value": 1},
        {"shape": "line", "title": "L", "series": []},
        {"shape": "bar", "title": "B", "series": []},
        {"shape": "table", "title": "T", "rows": []},
        {"shape": "donut", "title": "D", "value": 40},
    ]
    for spec in specs:
        svg = render(spec)
        assert "<svg" in svg
        assert "UNAVAILABLE" in svg
