from pathlib import Path

import yaml


def test_core_roles_preserve_safety_contract():
    roles = yaml.safe_load(Path("config/core-roles.yaml").read_text(encoding="utf-8"))["roles"]
    assert set(roles) == {"scout", "operator", "advisor"}
    assert roles["scout"]["output"]["unavailable_token"] == "UNAVAILABLE"
    assert roles["operator"]["output"]["requires_approval_for"]
    assert roles["advisor"]["output"]["recommendation_count"] == 3
