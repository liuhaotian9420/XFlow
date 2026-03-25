"""Unit tests for :mod:`backend.codex.full_integration_chain` (no Codex)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.codex.full_integration_chain import (
    FullIntegrationLayout,
    analyze_full_integration_onego_jsonl,
    build_full_integration_onego_prompt,
)


def _line(obj: dict) -> str:
    return json.dumps(obj, ensure_ascii=False)


def test_prompt_contains_three_skill_hints() -> None:
    p = build_full_integration_onego_prompt(business_request="SELECT 1", layout=FullIntegrationLayout.default_layout())
    assert "$sql-generator" in p
    assert "$sql-export-agent" in p
    assert "$scorecardpy-duckdb-large-scale-scorecard" in p
    assert "run_sql_export.py" in p
    assert "run_scorecardpy.py" in p
    assert "export_breaks.py" in p


def test_analyze_full_chain_order() -> None:
    events = [
        {"type": "item.completed", "item": {"type": "reasoning", "text": "$sql-generator"}},
        {"type": "item.completed", "item": {"type": "command_execution", "command": "cat .agents/skills/sql-generator/SKILL.md"}},
        {"type": "item.completed", "item": {"type": "reasoning", "text": "run_sql_export"}},
        {"type": "item.completed", "item": {"type": "command_execution", "command": "python .agents/skills/dataworks/scripts/run_sql_export.py a.sql"}},
        {"type": "item.completed", "item": {"type": "reasoning", "text": "scorecardpy"}},
        {"type": "item.completed", "item": {"type": "command_execution", "command": "python .agents/skills/scorecardpy/scripts/run_scorecardpy.py"}},
    ]
    text = "\n".join(_line(e) for e in events)
    ev = analyze_full_integration_onego_jsonl(text)
    assert ev.mentions_sql_generator
    assert ev.mentions_dataworks
    assert ev.mentions_scorecardpy
    assert ev.order_sg_dw_sc_ok
    assert ev.looks_like_full_chain


def test_analyze_bad_order() -> None:
    events = [
        {"type": "item.completed", "item": {"type": "command_execution", "command": "python run_scorecardpy.py"}},
        {"type": "item.completed", "item": {"type": "command_execution", "command": "python run_sql_export.py a.sql"}},
    ]
    text = "\n".join(_line(e) for e in events)
    ev = analyze_full_integration_onego_jsonl(text)
    assert not ev.order_sg_dw_sc_ok
