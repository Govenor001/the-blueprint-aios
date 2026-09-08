from pathlib import Path

from scripts.run_skill import build_prompt


def test_build_prompt_preserves_owner_request_without_logging_it():
    prompt = build_prompt("remember", "Save that my preferred meeting day is Tuesday.")
    assert prompt == "Use the /remember skill for the owner's request.\n\nOwner request:\nSave that my preferred meeting day is Tuesday."


def test_runner_logs_start_after_model_resolution():
    source = (Path(__file__).resolve().parents[1] / "scripts" / "run_skill.py").read_text(encoding="utf-8")
    assert 'log("skill_started", skill=skill, model=resolved_model)' in source
    assert 'return 1\n        log("skill_started"' not in source
