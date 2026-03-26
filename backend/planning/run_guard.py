"""Run guard helpers for plan completeness."""

from __future__ import annotations

from fastapi import HTTPException

from backend.schemas.plan import AnalysisPlan, PlanCompletenessStatus, PlanRecommendedAction


def assert_plan_runnable_or_400(plan: AnalysisPlan) -> None:
    """Ensure only complete plans can run."""
    completeness = getattr(plan, "completeness", None)
    if completeness is None:
        return

    status = getattr(completeness, "status", PlanCompletenessStatus.COMPLETE)
    status_value = status.value if hasattr(status, "value") else str(status)
    if status_value == PlanCompletenessStatus.COMPLETE.value:
        return

    action = getattr(completeness, "recommended_action", PlanRecommendedAction.CONFIRM)
    action_value = action.value if hasattr(action, "value") else str(action)
    raise HTTPException(
        status_code=400,
        detail=(
            f"Plan is not runnable: completeness.status={status_value}. "
            f"Resolve required review action first (recommended_action={action_value})."
        ),
    )
