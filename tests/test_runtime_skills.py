from pathlib import Path

from scripts.sync_runtime_skills import sync_runtime_skills


def test_sync_runtime_skills_copies_vault_skills_without_overwriting_core(tmp_path: Path):
    vault_skill = tmp_path / "skill-vault" / "remember" / "SKILL.md"
    vault_skill.parent.mkdir(parents=True)
    vault_skill.write_text("remember procedure", encoding="utf-8")

    core_skill = tmp_path / ".claude" / "skills" / "blueprint" / "SKILL.md"
    core_skill.parent.mkdir(parents=True)
    core_skill.write_text("core procedure", encoding="utf-8")

    copied = sync_runtime_skills(tmp_path)

    assert copied == ["remember"]
    assert (tmp_path / ".claude" / "skills" / "remember" / "SKILL.md").read_text(encoding="utf-8") == "remember procedure"
    assert core_skill.read_text(encoding="utf-8") == "core procedure"
