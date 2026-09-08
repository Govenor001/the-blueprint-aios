from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_student_installer_points_at_main_and_supports_https_route():
    install = (ROOT / "INSTALL.md").read_text(encoding="utf-8")
    script = (ROOT / "deploy" / "install.sh").read_text(encoding="utf-8")
    assert "raw.githubusercontent.com/Govenor001/the-blueprint-aios/main/deploy/install.sh" in install
    assert 'AIOS_DOMAIN' in install
    assert 'https://${AIOS_DOMAIN}' in script
    assert 'AIOS_MODEL_ROUTE:-claude-subscription' in script
    assert 'AIOS_API_KEY' not in script


def test_installer_keeps_schedules_disabled_until_owner_approval():
    script = (ROOT / "deploy" / "install.sh").read_text(encoding="utf-8")
    assert "Schedules are installed but disabled until the owner approves them on Day 7." in script
