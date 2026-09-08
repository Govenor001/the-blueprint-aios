from scripts.run_skill import build_prompt


def test_build_prompt_preserves_owner_request_without_logging_it():
    prompt = build_prompt("remember", "Save that my preferred meeting day is Tuesday.")
    assert prompt == "Use the /remember skill for the owner's request.\n\nOwner request:\nSave that my preferred meeting day is Tuesday."
