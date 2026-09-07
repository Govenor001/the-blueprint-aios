import json

from scripts.install_business_os import install_command, load_manifest


def test_manifest_has_exactly_150_unique_skills():
    manifest = load_manifest()
    assert manifest["skill_count"] == 150
    assert len(manifest["skills"]) == 150
    assert len({item["name"] for item in manifest["skills"]}) == 150
    assert len({item["path"] for item in manifest["skills"]}) == 150


def test_installer_is_explicit_and_noninteractive():
    manifest = load_manifest()
    command = install_command(manifest)
    assert command[:4] == ["npx", "skills", "add", "borghei/Claude-Skills"]
    assert command[-3:] == ["-a", "claude-code", "-y"]
    assert command.count("--skill") == 150
