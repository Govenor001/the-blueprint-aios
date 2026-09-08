from scripts.student_acceptance import run_acceptance


def test_student_acceptance_reports_complete_platform(tmp_path):
    (tmp_path / "curriculum" / "days").mkdir(parents=True)
    (tmp_path / "curriculum" / "README.md").write_text("# Curriculum\n", encoding="utf-8")
    for day in range(8):
        (tmp_path / "curriculum" / "days" / f"day-{day}.md").write_text(f"# Day {day}\n", encoding="utf-8")
    (tmp_path / "dashboard" / "static").mkdir(parents=True)
    (tmp_path / "dashboard" / "static" / "index.html").write_text("ok", encoding="utf-8")
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "build_map.py").write_text("ok", encoding="utf-8")
    (tmp_path / "config" / "panels").mkdir(parents=True)
    for name in ("intelligence", "content", "growth", "comms", "command", "back-office", "build"):
        (tmp_path / "config" / "panels" / f"{name}.yaml").write_text("cards: []", encoding="utf-8")
    for name in ("scout", "operator", "advisor"):
        (tmp_path / "skill-vault" / name).mkdir(parents=True)
        (tmp_path / "skill-vault" / name / "SKILL.md").write_text("ok", encoding="utf-8")
    (tmp_path / "deploy" / "timers").mkdir(parents=True)
    for index in range(5):
        (tmp_path / "deploy" / "timers" / f"job-{index}.timer").write_text("ok", encoding="utf-8")
    result = run_acceptance(tmp_path)
    assert result["passed"] is True

