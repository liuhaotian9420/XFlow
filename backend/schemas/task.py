"""Schemas for task state and lifecycle."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field

from .plan import AnalysisPlan
from .result import ResultPayload


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


class TaskStatus(str, Enum):
    CREATED = "created"
    PLANNED = "planned"
    REVIEWING = "reviewing"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskInput(BaseModel):
    question: str
    filename: str
    row_count: int
    column_count: int


class TaskError(BaseModel):
    error_type: str
    message: str
    detail: str | None = None


class TaskRecord(BaseModel):
    task_id: str
    status: TaskStatus = TaskStatus.CREATED
    created_at: datetime = Field(default_factory=now_utc)
    updated_at: datetime = Field(default_factory=now_utc)
    input: TaskInput
    plan: AnalysisPlan | None = None
    final_plan: AnalysisPlan | None = None
    result: ResultPayload | None = None
    error: TaskError | None = None

