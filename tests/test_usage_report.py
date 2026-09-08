from scripts.usage_report import usage_report


def test_usage_report_counts_without_inventing_cost():
    result = usage_report([{"status": "ok", "model": "smart"}, {"status": "error", "model": "smart"}])
    assert result["runs"] == 2
    assert result["statuses"] == {"ok": 1, "error": 1}
    assert "UNAVAILABLE" in result["cost"]
