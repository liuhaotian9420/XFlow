"""Tests for skill-plan compatibility adapters."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.planning.adapters import parse_plan_payload
from backend.schemas.plan import ChartType, PlanCompletenessStatus, PlanRecommendedAction


def _skill_plan_payload() -> dict:
    return {
        "goal": {
            "question": "Analyze weekly sales trend by region",
            "decision_context": "weekly ops review",
            "success_criteria": "identify top rising region",
        },
        "scope": {
            "entity": "orders",
            "population": "all paid orders",
            "assumptions": ["exclude test orders"],
        },
        "analysis_type": "trend",
        "grain": {
            "primary_key": ["order_id"],
            "answer_unit": "region-week",
            "aggregation_level": "week x region",
        },
        "metrics": [
            {
                "name": "sales",
                "column": "amount",
                "aggregation": "sum",
                "definition": "sum of paid amount",
                "format": "currency",
                "constraints": [],
            }
        ],
        "dimensions": [
            {"column": "week", "role": "time", "label": "week", "reason": "trend axis"},
            {"column": "region", "role": "geo", "label": "region", "reason": "comparison"},
        ],
        "filters": [{"column": "status", "operator": "eq", "value": "paid", "required": True}],
        "segments": [],
        "time": {"time_column": "week", "grain": "week", "window": "last 12 weeks"},
        "derived_fields": [],
        "comparisons": [],
        "methods": [
            {
                "name": "aggregate_sales",
                "type": "timeseries",
                "inputs": ["amount", "week", "region"],
                "description": "group and aggregate by week-region",
                "null_policy": "exclude",
            }
        ],
        "validation": {
            "data_quality_checks": ["check nulls on amount/week/region"],
            "metric_sanity_checks": ["sum amount non-negative"],
            "coverage_checks": ["all requested columns are present"],
        },
        "output": {
            "table_fields": ["week", "region", "sales"],
            "chart_type": "table",
            "title": "Weekly regional sales",
            "sort": "week asc",
            "limit": 200,
            "narrative_focus": "recent trend by region",
        },
        "ambiguities": [],
        "confidence": 0.78,
        "completion_state": "minimally_completed",
    }


def test_parse_skill_plan_payload_into_normalized_analysis_plan() -> None:
    parsed, raw = parse_plan_payload(_skill_plan_payload())

    assert parsed.goal == "Analyze weekly sales trend by region"
    assert len(parsed.metrics) == 1
    assert parsed.metrics[0].column == "amount"
    assert parsed.dimensions[0].column == "week"
    assert parsed.output.show_table is True
    assert parsed.output.chart_type == ChartType.BAR
    assert parsed.completeness.status == PlanCompletenessStatus.COMPLETE
    assert parsed.completeness.recommended_action == PlanRecommendedAction.CONFIRM
    assert isinstance(raw, dict)
    assert raw.get("analysis_type") == "trend"


def test_parse_legacy_plan_payload_still_works() -> None:
    legacy_payload = {
        "goal": "Analyze data",
        "metrics": [{"column": "amount", "aggregation": "sum", "alias": "amount_sum"}],
        "dimensions": [{"column": "region", "role": "category"}],
        "filters": [{"column": "status", "operator": "eq", "value": "paid"}],
        "output": {"chart_type": "bar", "show_table": True},
        "assumptions": [],
        "ambiguities": [],
        "confidence": 0.9,
        "completeness": {
            "status": "complete",
            "score": 1.0,
            "rationale": "ready",
            "missing_information": [],
            "open_questions": [],
            "exploration_tasks": [],
        },
    }
    parsed, raw = parse_plan_payload(legacy_payload)
    assert parsed.goal == "Analyze data"
    assert parsed.output.chart_type == ChartType.BAR
    assert parsed.completeness.status == PlanCompletenessStatus.COMPLETE
    assert parsed.completeness.recommended_action == PlanRecommendedAction.CONFIRM
    assert raw is None


def test_parse_legacy_blocked_plan_backfills_recommended_action() -> None:
    legacy_payload = {
        "goal": "Analyze blocked data",
        "metrics": [{"column": "amount", "aggregation": "sum", "alias": "amount_sum"}],
        "dimensions": [{"column": "region", "role": "category"}],
        "filters": [],
        "output": {"chart_type": "bar", "show_table": True},
        "assumptions": [],
        "ambiguities": [{"field": "date", "issue": "date range missing"}],
        "confidence": 0.4,
        "completeness": {
            "status": "blocked",
            "score": 0.4,
            "rationale": "date range is required",
            "missing_information": [],
            "open_questions": [],
            "exploration_tasks": [],
        },
    }
    parsed, _ = parse_plan_payload(legacy_payload)
    assert parsed.completeness.status == PlanCompletenessStatus.BLOCKED
    assert parsed.completeness.recommended_action == PlanRecommendedAction.REVISE_REQUIRED
