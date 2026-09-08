from scripts.interview import save_interview


def test_interview_saves_missing_answers_as_unavailable(tmp_path):
    path = save_interview(tmp_path, {"business_name": "Example"})
    text = path.read_text(encoding="utf-8")
    assert "Example" in text
    assert "UNAVAILABLE" in text
