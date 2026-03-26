"""Compatibility adapters for skill-native and execution-native analysis plans."""

from __future__ import annotations

from typing import Any

from backend.schemas.plan import (
    AmbiguitySpec,
    AnalysisPlan,
    ChartType,
    DimensionRole,
    DimensionSpec,
    FilterSpec,
    MetricSpec,
    OutputSpec,
    PlanAssumptionSpec,
    PlanCompletenessSpec,
    PlanRecommendedAction,
    PlanCompletenessStatus,
    PlanQuestionSpec,
    SkillAnalysisPlan,
    SkillCompletionState,
)


def skill_plan_shape_hint(payload: dict[str, Any]) -> bool:
    """Heuristic check for the skill-native 16-field contract."""
    required = {
        "goal",
        "scope",
        "analysis_type",
        "grain",
        "metrics",
        "dimensions",
        "filters",
        "segments",
        "time",
        "derived_fields",
        "comparisons",
        "methods",
        "validation",
        "output",
        "ambiguities",
        "confidence",
    }
    return required.issubset(set(payload.keys()))


def map_skill_completion_to_plan_status(
    skill_plan: SkillAnalysisPlan,
) -> PlanCompletenessStatus:
    if skill_plan.completion_state == SkillCompletionState.REVIEWED:
        return PlanCompletenessStatus.COMPLETE
    if skill_plan.completion_state == SkillCompletionState.MINIMALLY_COMPLETED:
        return PlanCompletenessStatus.COMPLETE
    if skill_plan.completion_state == SkillCompletionState.NEEDS_CLARIFICATION:
        return PlanCompletenessStatus.BLOCKED

    for item in skill_plan.ambiguities:
        if item.blocks_minimal_completion is True:
            return PlanCompletenessStatus.BLOCKED
        if (item.severity or "").lower() == "blocking":
            return PlanCompletenessStatus.BLOCKED

    if skill_plan.validation.coverage_checks:
        return PlanCompletenessStatus.NEEDS_EXPLORATION
    return PlanCompletenessStatus.COMPLETE


def map_plan_status_to_recommended_action(
    status: PlanCompletenessStatus,
) -> PlanRecommendedAction:
    if status == PlanCompletenessStatus.COMPLETE:
        return PlanRecommendedAction.CONFIRM
    if status == PlanCompletenessStatus.NEEDS_EXPLORATION:
        return PlanRecommendedAction.CLARIFY
    return PlanRecommendedAction.REVISE_REQUIRED


def _coerce_chart_type(chart_type: str | None) -> tuple[ChartType, list[AmbiguitySpec]]:
    issues: list[AmbiguitySpec] = []
    if not chart_type:
        return ChartType.BAR, issues
    value = chart_type.strip().lower()
    if value == "table":
        issues.append(
            AmbiguitySpec(
                field="output.chart_type",
                issue="Skill chart_type=table was downgraded to bar for execution compatibility.",
            )
        )
        return ChartType.BAR, issues
    if value == ChartType.LINE.value:
        return ChartType.LINE, issues
    if value == ChartType.BAR.value:
        return ChartType.BAR, issues
    if value == ChartType.HISTOGRAM.value:
        return ChartType.HISTOGRAM, issues
    issues.append(
        AmbiguitySpec(
            field="output.chart_type",
            issue=f"Unsupported chart_type '{chart_type}' was downgraded to bar.",
        )
    )
    return ChartType.BAR, issues


def normalize_skill_plan_to_analysis_plan(skill_plan: SkillAnalysisPlan) -> AnalysisPlan:
    chart_type, chart_issues = _coerce_chart_type(skill_plan.output.chart_type)

    metrics = [
        MetricSpec(
            column=item.column,
            aggregation=item.aggregation,
            alias=item.name or None,
        )
        for item in skill_plan.metrics
    ]
    dimensions = [
        DimensionSpec(
            column=item.column,
            role=item.role or DimensionRole.CATEGORY,
        )
        for item in skill_plan.dimensions
    ]

    filters = [
        FilterSpec(
            column=item.column,
            operator=item.operator,
            value=item.value,
        )
        for item in skill_plan.filters
    ]
    ambiguities = [
        AmbiguitySpec(
            field=item.field or "unknown",
            issue=item.issue,
        )
        for item in skill_plan.ambiguities
    ]
    ambiguities.extend(chart_issues)

    assumptions: list[PlanAssumptionSpec] = []
    for text in skill_plan.scope.assumptions:
        assumptions.append(PlanAssumptionSpec(statement=text, impact=None))

    open_questions = [
        PlanQuestionSpec(
            question=item.issue,
            reason="Derived from skill ambiguity list.",
            blocking=(
                item.blocks_minimal_completion is True
                or (item.severity or "").lower() == "blocking"
            ),
            related_fields=[item.field] if item.field else [],
        )
        for item in skill_plan.ambiguities
    ]

    status = map_skill_completion_to_plan_status(skill_plan)
    rationale = (
        "Mapped from skill-native completion state and ambiguity severity."
    )
    completeness = PlanCompletenessSpec(
        status=status,
        recommended_action=map_plan_status_to_recommended_action(status),
        score=float(skill_plan.confidence),
        rationale=rationale,
        missing_information=ambiguities,
        open_questions=open_questions,
        exploration_tasks=[],
    )

    return AnalysisPlan(
        goal=skill_plan.goal.question,
        metrics=metrics,
        dimensions=dimensions,
        filters=filters,
        output=OutputSpec(chart_type=chart_type, show_table=True),
        assumptions=assumptions,
        ambiguities=ambiguities,
        confidence=skill_plan.confidence,
        completeness=completeness,
        raw_skill_plan=skill_plan.model_dump(mode="json"),
    )


def parse_plan_payload(payload: dict[str, Any]) -> tuple[AnalysisPlan, dict[str, Any] | None]:
    """Parse either skill-native plan payload or execution-native plan payload."""
    if skill_plan_shape_hint(payload):
        skill_plan = SkillAnalysisPlan.model_validate(payload)
        normalized = normalize_skill_plan_to_analysis_plan(skill_plan)
        return normalized, skill_plan.model_dump(mode="json")
    parsed = AnalysisPlan.model_validate(payload)
    return parsed, parsed.raw_skill_plan
