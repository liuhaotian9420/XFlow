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


class ReviewType(str, Enum):
    CONFIRMATION = "confirmation"
    SUGGESTION = "suggestion"


class ReviewState(str, Enum):
    PENDING = "pending"
    RESOLVED = "resolved"
    SUPERSEDED = "superseded"


class TaskInput(BaseModel):
    question: str
    filename: str
    row_count: int
    column_count: int


class TaskError(BaseModel):
    error_type: str
    message: str
    detail: str | None = None


class TaskReview(BaseModel):
    review_id: str
    review_type: ReviewType
    state: ReviewState = ReviewState.PENDING
    title: str
    message: str
    options: list[str] = Field(default_factory=list)
    suggested_plan: AnalysisPlan | None = None
    user_choice: str | None = None
    user_text: str | None = None
    created_at: datetime = Field(default_factory=now_utc)
    resolved_at: datetime | None = None


class TaskRecord(BaseModel):
    task_id: str
    status: TaskStatus = TaskStatus.CREATED
    created_at: datetime = Field(default_factory=now_utc)
    updated_at: datetime = Field(default_factory=now_utc)
    input: TaskInput
    plan: AnalysisPlan | None = None
    final_plan: AnalysisPlan | None = None
    pending_review: TaskReview | None = None
    review_history: list[TaskReview] = Field(default_factory=list)
    result: ResultPayload | None = None
    error: TaskError | None = None

