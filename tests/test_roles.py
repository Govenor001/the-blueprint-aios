from scripts.run_role import run_advisor, run_operator, run_scout


def test_scout_preserves_source_time_and_unavailable():
    result = run_scout({"sources": [{"source": "fixture", "retrieved_at": "2026-01-01T00:00:00Z", "value": 4}, {"value": None}]})
    assert result["observations"][0]["source"] == "fixture"
    assert result["observations"][0]["retrieved_at"] == "2026-01-01T00:00:00Z"
    assert result["observations"][1]["source"] == "UNAVAILABLE"
    assert result["status"] == "available"


def test_operator_requires_approval_for_consequential_request():
    result = run_operator({"request": "send this campaign"}, {"faq": "approved boundaries"})
    assert result["status"] == "draft"
    assert result["approval_required"] is True


def test_advisor_always_returns_exactly_three_ranked_recommendations():
    result = run_advisor(run_scout({"sources": []}), run_operator({}, {}))
    assert [item["rank"] for item in result["recommendations"]] == [1, 2, 3]
    assert all("UNAVAILABLE" in item["evidence"] for item in result["recommendations"])
    assert result["status"] == "unavailable"


def test_scout_with_only_failed_sources_stays_unavailable():
    result = run_scout({"sources": [{"source": "broken", "status": "error", "value": None}]})
    assert result["status"] == "unavailable"
