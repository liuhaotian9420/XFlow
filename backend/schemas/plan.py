"""Schemas for analysis planning."""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


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


class AnalysisPlan(BaseModel):
    goal: str
    metrics: list[MetricSpec] = Field(default_factory=list)
    dimensions: list[DimensionSpec] = Field(default_factory=list)
    filters: list[FilterSpec] = Field(default_factory=list)
    output: OutputSpec = Field(default_factory=OutputSpec)
    ambiguities: list[AmbiguitySpec] = Field(default_factory=list)
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)

