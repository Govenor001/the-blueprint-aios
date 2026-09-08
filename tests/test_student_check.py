import json

from scripts.student_check import check


def test_student_check_reports_missing_setup(tmp_path, monkeypatch):
    (tmp_path / "config").mkdir()
    (tmp_path / "dashboard" / "static").mkdir(parents=True)
    (tmp_path / "business-os-150").mkdir()
    (tmp_path / "business-os-150" / "skills-manifest.json").write_text(
        json.dumps({"skill_count": 150, "skills": [{"name": str(i), "path": str(i), "repo": "borghei/Claude-Skills", "category": "build"} for i in range(150)]}),
        encoding="utf-8",
    )
    monkeypatch.delenv("DASHBOARD_PASSWORD", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    result = check(tmp_path)
    assert result["passed"] is False
    assert result["checks"]["no_anthropic_api_key"] is True
    assert result["checks"]["seven_wings"] is False
    assert result["checks"]["diagram_builder"] is False


def test_student_check_accepts_server_env_file_password(tmp_path, monkeypatch):
    (tmp_path / ".env").write_text("DASHBOARD_PASSWORD=stored\n", encoding="utf-8")
    monkeypatch.delenv("DASHBOARD_PASSWORD", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    result = check(tmp_path)
    assert result["checks"]["dashboard_password"] is True
