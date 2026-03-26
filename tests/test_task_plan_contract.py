"""Tests for the plan-review contract defaults."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.schemas.plan import AnalysisPlan, PlanRecommendedAction


def test_plan_completeness_defaults_recommended_action() -> None:
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
            "status": "needs_exploration",
            "score": 0.8,
            "rationale": "Need to confirm the requested breakdown.",
            "missing_information": [],
            "open_questions": [],
            "exploration_tasks": [],
        },
    }

    parsed = AnalysisPlan.model_validate(payload)

    assert parsed.completeness.recommended_action == PlanRecommendedAction.CLARIFY
