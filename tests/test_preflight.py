from scripts.preflight import validate_environment


def test_preflight_rejects_key_and_missing_password():
    problems = validate_environment({"route": "claude-subscription", "allowed_routes": ["claude-subscription"]}, {"ANTHROPIC_API_KEY": "present"})
    assert any("ANTHROPIC_API_KEY" in problem for problem in problems)
    assert any("DASHBOARD_PASSWORD" in problem for problem in problems)


def test_preflight_accepts_bedrock_with_region():
    assert validate_environment({"route": "bedrock", "allowed_routes": ["bedrock"]}, {"DASHBOARD_PASSWORD": "x", "AWS_REGION": "us-east-1"}) == []
