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


class ArtifactPayload(BaseModel):
    """
    Optional non-tabular renderables returned with a result.

    Preferred contract:
    - provide a lightweight artifact reference via `artifact_id` and/or repo-relative `path`.

    Legacy compatibility:
    - For PNG: `mime="image/png"` with inline `data_base64` (base64 of raw bytes).
    - For HTML: `mime="text/html"` with inline `html`.
    """

    name: str
    mime: str
    artifact_id: str | None = None
    path: str | None = None
    data_base64: str | None = None
    html: str | None = None
    display_width: int | None = None
    display_height: int | None = None


class ResultPayload(BaseModel):
    chart: ChartPayload
    table: TablePayload
    execution_summary: str
    summary: str | None = None
    follow_ups: list[str] = Field(default_factory=list)
    artifacts: list[ArtifactPayload] = Field(default_factory=list)

