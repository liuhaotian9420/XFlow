"""Unit tests for :mod:`backend.codex.two_skill_chain` JSONL heuristics (no Codex)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.codex.two_skill_chain import analyze_two_skill_serial_jsonl


def _line(obj: dict) -> str:
    return json.dumps(obj, ensure_ascii=False)


def test_analyze_two_skill_serial_detects_ordering() -> None:
    events = [
        {"type": "item.completed", "item": {"type": "reasoning", "text": "Using $sql-generator"}},
        {"type": "item.completed", "item": {"type": "command_execution", "command": "cat .agents/skills/sql-generator/SKILL.md"}},
        {"type": "item.completed", "item": {"type": "reasoning", "text": "Now $sql-export-agent"}},
        {
            "type": "item.completed",
            "item": {"type": "command_execution", "command": "python .agents/skills/dataworks/scripts/run_sql_export.py x.sql"},
        },
    ]
    text = "\n".join(_line(e) for e in events)
    ev = analyze_two_skill_serial_jsonl(text)
    assert ev.mentions_sql_generator_hint
    assert ev.mentions_sql_export_or_dataworks
    assert ev.command_touches_sql_generator_tree
    assert ev.command_touches_dataworks_run_sql_export
    assert ev.step1_before_step2_order_ok
    assert ev.looks_like_serial_two_skill


def test_analyze_two_skill_serial_fails_when_dw_before_sg() -> None:
    events = [
        {"type": "item.completed", "item": {"type": "command_execution", "command": "python .agents/skills/dataworks/scripts/run_sql_export.py x.sql"}},
        {"type": "item.completed", "item": {"type": "command_execution", "command": "cat .agents/skills/sql-generator/SKILL.md"}},
    ]
    text = "\n".join(_line(e) for e in events)
    ev = analyze_two_skill_serial_jsonl(text)
    assert not ev.step1_before_step2_order_ok
    assert not ev.looks_like_serial_two_skill
