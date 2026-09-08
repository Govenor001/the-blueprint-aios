from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_agent_drawer_accepts_a_plain_language_request():
    html = (ROOT / "dashboard" / "static" / "index.html").read_text(encoding="utf-8")
    javascript = (ROOT / "dashboard" / "static" / "app.js").read_text(encoding="utf-8")
    assert 'id="view-map"' in html
    assert 'id="view-chat"' in html
    assert 'id="view-dashboards"' in html
    assert '/api/chat' in javascript
    assert 'SpeechRecognition' in javascript
    assert 'whole-brain' in html
