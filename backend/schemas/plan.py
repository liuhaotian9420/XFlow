"""Schemas for analysis planning."""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, model_validator


class Aggregation(str, Enum):
    SUM = "sum"
    MEAN = "mean"
    COUNT = "count"
    MAX = "max"
    MIN = "min"
    MEDIAN = "median"


class DimensionRole(str, Enum):
    TIME = "time"
    CATEGORY = "category"
    GEO = "geo"


class FilterOperator(str, Enum):
    EQ = "eq"
    NEQ = "neq"
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"
    IN = "in"
    NOT_IN = "not_in"
    CONTAINS = "contains"


class ChartType(str, Enum):
    LINE = "line"
    BAR = "bar"
    HISTOGRAM = "histogram"


class SkillAnalysisType(str, Enum):
    DESCRIPTIVE = "descriptive"
    DIAGNOSTIC = "diagnostic"
    TREND = "trend"
    COMPARISON = "comparison"
    DISTRIBUTION = "distribution"
    SEGMENTATION = "segmentation"
    RANKING = "ranking"


class SkillMethodType(str, Enum):
    AGGREGATE = "aggregate"
    TIMESERIES = "timeseries"
    TOP_N = "top_n"
    DISTRIBUTION = "distribution"
    GROUP_COMPARE = "group_compare"
    PERIOD_COMPARE = "period_compare"


class SkillNullPolicy(str, Enum):
    INCLUDE = "include"
    EXCLUDE = "exclude"
    SEPARATE_BUCKET = "separate_bucket"


class SkillCompletionState(str, Enum):
    NEEDS_CLARIFICATION = "needs_clarification"
    MINIMALLY_COMPLETED = "minimally_completed"
    REVIEWED = "reviewed"


class PlanCompletenessStatus(str, Enum):
    COMPLETE = "complete"
    NEEDS_EXPLORATION = "needs_exploration"
    BLOCKED = "blocked"


class PlanRecommendedAction(str, Enum):
    CONFIRM = "confirm"
    CLARIFY = "clarify"
    REVISE_REQUIRED = "revise_required"


class ExplorationPriority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class MetricSpec(BaseModel):
    column: str
    aggregation: Aggregation
    alias: str | None = None


class DimensionSpec(BaseModel):
    column: str
    role: DimensionRole = DimensionRole.CATEGORY


class FilterSpec(BaseModel):
    column: str
    operator: FilterOperator
    value: Any


class OutputSpec(BaseModel):
    chart_type: ChartType = ChartType.BAR
    show_table: bool = True


class AmbiguitySpec(BaseModel):
    field: str
    issue: str


class PlanAssumptionSpec(BaseModel):
    statement: str
    impact: str | None = None


class PlanQuestionSpec(BaseModel):
    question: str
    reason: str
    blocking: bool = False
    priority: ExplorationPriority = ExplorationPriority.MEDIUM
    related_fields: list[str] = Field(default_factory=list)


class ExplorationTaskSpec(BaseModel):
    goal: str
    rationale: str
    priority: ExplorationPriority = ExplorationPriority.MEDIUM
    inputs: list[str] = Field(default_factory=list)
    success_criteria: list[str] = Field(default_factory=list)


class PlanCompletenessSpec(BaseModel):
    status: PlanCompletenessStatus = PlanCompletenessStatus.COMPLETE
    recommended_action: PlanRecommendedAction | None = None
    score: float = Field(default=1.0, ge=0.0, le=1.0)
    rationale: str = "Plan is ready to execute."
    missing_information: list[AmbiguitySpec] = Field(default_factory=list)
    open_questions: list[PlanQuestionSpec] = Field(default_factory=list)
    exploration_tasks: list[ExplorationTaskSpec] = Field(default_factory=list)

    @model_validator(mode="after")
    def _ensure_recommended_action(self) -> "PlanCompletenessSpec":
        if self.recommended_action is None:
            self.recommended_action = _recommended_action_for_status(self.status)
        return self


class AnalysisPlan(BaseModel):
    goal: str
    metrics: list[MetricSpec] = Field(default_factory=list)
    dimensions: list[DimensionSpec] = Field(default_factory=list)
    filters: list[FilterSpec] = Field(default_factory=list)
    output: OutputSpec = Field(default_factory=OutputSpec)
    assumptions: list[PlanAssumptionSpec] = Field(default_factory=list)
    ambiguities: list[AmbiguitySpec] = Field(default_factory=list)
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    completeness: PlanCompletenessSpec = Field(default_factory=PlanCompletenessSpec)
    raw_skill_plan: dict[str, Any] | None = None


class SkillGoalSpec(BaseModel):
    question: str
    decision_context: str | None = None
    success_criteria: str | None = None


class SkillScopeSpec(BaseModel):
    entity: str | None = None
    population: str
    assumptions: list[str] = Field(default_factory=list)


class SkillGrainSpec(BaseModel):
    primary_key: list[str] = Field(default_factory=list)
    answer_unit: str
    aggregation_level: str | None = None


class SkillMetricSpec(BaseModel):
    name: str
    column: str
    aggregation: Aggregation
    definition: str | None = None
    format: str | None = None
    constraints: list[str] = Field(default_factory=list)


class SkillDimensionSpec(BaseModel):
    column: str
    role: DimensionRole | None = None
    label: str | None = None
    reason: str | None = None


class SkillFilterSpec(BaseModel):
    column: str
    operator: FilterOperator
    value: Any
    required: bool | None = None


class SkillSegmentSpec(BaseModel):
    name: str | None = None
    column: str | None = None
    definition: str | None = None


class SkillTimeSpec(BaseModel):
    time_column: str | None = None
    grain: str | None = None
    window: str | None = None
    comparison_window: str | None = None


class SkillDerivedFieldSpec(BaseModel):
    name: str
    expression_logic: str
    source_columns: list[str] = Field(default_factory=list)


class SkillComparisonSpec(BaseModel):
    type: str
    left: str | None = None
    right: str | None = None
    metric_names: list[str] = Field(default_factory=list)
    expected_signal: str | None = None


class SkillMethodSpec(BaseModel):
    name: str
    type: SkillMethodType
    inputs: list[str] = Field(default_factory=list)
    description: str
    null_policy: SkillNullPolicy | None = None


class SkillValidationSpec(BaseModel):
    data_quality_checks: list[str] = Field(default_factory=list)
    metric_sanity_checks: list[str] = Field(default_factory=list)
    coverage_checks: list[str] = Field(default_factory=list)


class SkillOutputSpec(BaseModel):
    table_fields: list[str] = Field(default_factory=list)
    chart_type: str | None = None
    title: str | None = None
    sort: str | None = None
    limit: int | None = None
    narrative_focus: str | None = None


class SkillAmbiguitySpec(BaseModel):
    field: str | None = None
    issue: str
    severity: str | None = None
    blocks_minimal_completion: bool | None = None


class SkillAnalysisPlan(BaseModel):
    goal: SkillGoalSpec
    scope: SkillScopeSpec
    analysis_type: SkillAnalysisType
    grain: SkillGrainSpec
    metrics: list[SkillMetricSpec] = Field(default_factory=list)
    dimensions: list[SkillDimensionSpec] = Field(default_factory=list)
    filters: list[SkillFilterSpec] = Field(default_factory=list)
    segments: list[SkillSegmentSpec] = Field(default_factory=list)
    time: SkillTimeSpec = Field(default_factory=SkillTimeSpec)
    derived_fields: list[SkillDerivedFieldSpec] = Field(default_factory=list)
    comparisons: list[SkillComparisonSpec] = Field(default_factory=list)
    methods: list[SkillMethodSpec] = Field(default_factory=list)
    validation: SkillValidationSpec = Field(default_factory=SkillValidationSpec)
    output: SkillOutputSpec = Field(default_factory=SkillOutputSpec)
    ambiguities: list[SkillAmbiguitySpec] = Field(default_factory=list)
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    completion_state: SkillCompletionState | None = None

    @model_validator(mode="after")
    def _ensure_required_lists(self) -> "SkillAnalysisPlan":
        if not self.metrics:
            raise ValueError("metrics must contain at least one item")
        if not self.methods:
            raise ValueError("methods must contain at least one item")
        if not self.output.table_fields:
            raise ValueError("output.table_fields must contain at least one item")
        return self


def _recommended_action_for_status(
    status: PlanCompletenessStatus,
) -> PlanRecommendedAction:
    if status == PlanCompletenessStatus.COMPLETE:
        return PlanRecommendedAction.CONFIRM
    if status == PlanCompletenessStatus.NEEDS_EXPLORATION:
        return PlanRecommendedAction.CLARIFY
    return PlanRecommendedAction.REVISE_REQUIRED

