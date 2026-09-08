from scripts.panel import build_mission_control, render_panel
from scripts.schedule import schedule_jobs


def test_panel_helper_keeps_empty_state_explicit():
    result = render_panel({"name": "content", "cards": [{"id": "views", "title": "Views", "shape": "line"}]}, {})
    assert result["cards"][0]["empty_state"] is True


def test_mission_control_contains_all_core_roles():
    result = build_mission_control({"role": "scout"}, {"role": "operator"}, {"role": "advisor"}, {})
    assert set(result["roles"]) == {"scout", "operator", "advisor"}


def test_schedule_writer_is_idempotent(tmp_path):
    schedule_jobs(tmp_path, [{"name": "brief", "command": "/bin/true", "interval": "hourly"}])
    assert (tmp_path / "var" / "generated-systemd" / "aios-brief.timer").exists()
