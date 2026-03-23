"""Schemas for analysis execution results."""

from __future__ import annotations

from pydantic import BaseModel, Field

from .plan import ChartType


class ChartPayload(BaseModel):
    chart_type: ChartType
    x: str
    y: str
    data: list[dict] = Field(default_factory=list)


class TablePayload(BaseModel):
    columns: list[str] = Field(default_factory=list)
    rows: list[dict] = Field(default_factory=list)


class ResultPayload(BaseModel):
    chart: ChartPayload
    table: TablePayload
    execution_summary: str
    summary: str | None = None
    follow_ups: list[str] = Field(default_factory=list)

