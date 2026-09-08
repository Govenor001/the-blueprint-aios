import json
from pathlib import Path

from scripts.build_diagrams import build_diagrams


def test_build_diagrams_creates_architecture_spec_and_fallback(tmp_path: Path):
    static = tmp_path / "dashboard" / "static"
    static.mkdir(parents=True)
    (static / "map.json").write_text(
        json.dumps(
            {
                "wings": [
                    {"wing": name, "departments": []}
                    for name in ["intelligence", "content", "growth", "comms", "back-office", "command", "build"]
                ]
            }
        ),
        encoding="utf-8",
    )

    result = build_diagrams(tmp_path)

    assert result["architecture"]["components"] == 8
    spec = json.loads((tmp_path / "var" / "diagrams" / "aios-architecture.json").read_text(encoding="utf-8"))
    assert len(spec["components"]) == 8
    assert (tmp_path / "dashboard" / "static" / "diagrams" / "aios-architecture.html").exists()
