from scripts.usage_report import usage_report


def test_usage_report_counts_without_inventing_cost():
    result = usage_report([
        {"event": "skill_started", "status": "ok", "model": "smart"},
        {"event": "skill_finished", "status": "ok", "model": "smart"},
        {"event": "skill_started", "status": "ok", "model": "smart"},
        {"event": "skill_finished", "status": "error", "model": "smart"},
    ])
    assert result["runs"] == 2
    assert result["statuses"] == {"ok": 1, "error": 1}
    assert result["models"] == {"smart": 2}
    assert "UNAVAILABLE" in result["cost"]
