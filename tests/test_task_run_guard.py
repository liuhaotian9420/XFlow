"""Tests for task run guard on plan completeness status."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from fastapi import HTTPException

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.planning.run_guard import assert_plan_runnable_or_400
from backend.schemas.plan import AnalysisPlan


def _plan_with_status(status: str) -> AnalysisPlan:
    payload = {
        "goal": "Analyze sales by region",
        "metrics": [{"column": "amount", "aggregation": "sum", "alias": "sales"}],
        "dimensions": [{"column": "region", "role": "category"}],
        "filters": [],
        "output": {"chart_type": "bar", "show_table": True},
        "assumptions": [],
        "ambiguities": [],
        "confidence": 0.8,
        "completeness": {
            "status": status,
            "score": 0.8,
            "rationale": "test",
            "missing_information": [],
            "open_questions": [],
            "exploration_tasks": [],
        },
    }
    return AnalysisPlan.model_validate(payload)


def test_runnable_guard_allows_complete_plan() -> None:
    assert_plan_runnable_or_400(_plan_with_status("complete"))


@pytest.mark.parametrize("status", ["blocked", "needs_exploration"])
def test_runnable_guard_rejects_incomplete_status(status: str) -> None:
    with pytest.raises(HTTPException) as exc:
        assert_plan_runnable_or_400(_plan_with_status(status))
    assert exc.value.status_code == 400
    assert "not runnable" in str(exc.value.detail)
