from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.codex.prompts import (
    build_chat_prompt,
    build_followups_prompt,
    build_revise_plan_prompt,
    build_summary_prompt,
)


def test_chat_prompt_requires_reference_only_artifact_metadata() -> None:
    prompt = build_chat_prompt(
        message="Summarize this run result",
        history=[],
        file_context=None,
    )
    assert "path" in prompt
    assert "each artifact object must include exactly `name`, `mime`, and `path`" in prompt
    assert "set `path` to null instead of inventing a path" in prompt
    assert "Never emit `data_base64`" in prompt
    assert "full HTML bodies" in prompt


def test_chat_prompt_distinguishes_code_from_saved_artifacts() -> None:
    prompt = build_chat_prompt(
        message="Please write a very simple HTML page",
        history=[],
        file_context=None,
    )
    assert "return the code directly in `content`" in prompt
    assert "save it to a controlled local artifact path first" in prompt
    assert "Only mention an artifact in structured result metadata after the file has actually been written successfully." in prompt
    assert "Do not move user-requested source code into `result.artifacts`" in prompt


def test_chat_prompt_mentions_reply_result_and_artifact_field_contract() -> None:
    prompt = build_chat_prompt(
        message="Summarize the generated artifacts",
        history=[],
        file_context=None,
    )
    assert "always return both `reply` and `result`" in prompt
    assert "each artifact object must include exactly `name`, `mime`, and `path`" in prompt
    assert "set `path` to null instead of inventing a path" in prompt
    assert "Never use absolute filesystem paths in `path`" in prompt
    assert "text/html" in prompt
    assert "image/png" in prompt


def test_summary_prompt_forbids_inline_artifact_bodies() -> None:
    prompt = build_summary_prompt(
        goal="Summarize result",
        result_summary={"artifacts": [{"name": "plot.png", "mime": "image/png"}]},
    )
    assert "Do not generate machine-readable result JSON" in prompt
    assert "base64 payloads" in prompt
    assert "raw HTML bodies" in prompt


def test_revise_plan_prompt_uses_completion_state_not_completeness() -> None:
    prompt = build_revise_plan_prompt(
        current_plan={"goal": {"question": "x"}},
        instruction="Change it to a regional comparison",
        schema_profile={"columns": [{"name": "region"}]},
    )
    assert '"completion_state" must be one of' in prompt
    assert 'Update "ambiguities", "confidence", and "completion_state"' in prompt
    assert "including completeness assessment fields" not in prompt
    assert 'Update "ambiguities", "confidence", and "completeness"' not in prompt


def test_followups_prompt_no_longer_contains_garbled_example() -> None:
    prompt = build_followups_prompt(
        goal="Analyze sales",
        result_summary={"row_count": 10},
    )
    assert "Example:" in prompt
    assert "base64 payloads" in prompt
    assert "閺勵垰" not in prompt
