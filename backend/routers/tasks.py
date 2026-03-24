"""Task CRUD endpoints."""

from __future__ import annotations

import os
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, File, Form, HTTPException, Query, UploadFile
from pydantic import BaseModel

from backend.chat_store import (
    delete_task_record,
    get_task_record,
    list_task_records,
    save_task_record,
)
from backend.codex.errors import CodexAdapterError
from backend.codex.factory import get_provider
from backend.codex.mock import MockProvider
from backend.execution.engine import run_plan
from backend.observability import diff_dicts, log_event, save_snapshot
from backend.profiler.schema_profiler import profile_upload
from backend.schemas.plan import AnalysisPlan
from backend.schemas.task import TaskError, TaskInput, TaskRecord, TaskStatus
from backend.storage import CODEX_FAILURE_COUNT, TASK_DATAFRAMES, TASK_SNAPSHOTS, TASKS

router = APIRouter(prefix="/tasks", tags=["tasks"])


def _effective_use_mock(explicit: bool | None) -> bool:
    """Per-request override; if omitted, follow process env CODEX_MOCK (default true)."""
    if explicit is not None:
        return explicit
    return os.getenv("CODEX_MOCK", "true").lower() == "true"


def _effective_reasoning_effort(
    reasoning_effort: str | None,
    think_level: str | None,
) -> str | None:
    value = (reasoning_effort or "").strip() or (think_level or "").strip()
    return value or None


class ReviewRequest(BaseModel):
    final_plan: AnalysisPlan
    use_mock: bool | None = None


class ReviseRequest(BaseModel):
    instruction: str
    use_mock: bool | None = None


class RevisePlanResponse(BaseModel):
    task_id: str
    plan: AnalysisPlan


class CreateTaskResponse(BaseModel):
    task_id: str
    status: TaskStatus
    plan: AnalysisPlan


class TaskHistoryItem(BaseModel):
    task_id: str
    created_at: str
    updated_at: str
    status: str
    question: str | None = None
    filename: str | None = None


def _update_status(record: TaskRecord, status: TaskStatus) -> None:
    record.status = status
    record.updated_at = datetime.now(timezone.utc)


def _persist_task(record: TaskRecord) -> None:
    save_task_record(record)


def _get_task_or_404(task_id: str) -> TaskRecord:
    record = TASKS.get(task_id)
    if record is not None:
        return record
    persisted = get_task_record(task_id)
    if persisted is None:
        raise HTTPException(status_code=404, detail="Task not found")
    TASKS[task_id] = persisted
    return persisted


def _record_codex_failure(task_id: str, message: str) -> None:
    # pylint: disable=global-statement
    global CODEX_FAILURE_COUNT
    CODEX_FAILURE_COUNT += 1
    threshold = int(os.getenv("CODEX_AUTO_MOCK_THRESHOLD", "3"))
    if CODEX_FAILURE_COUNT >= threshold:
        os.environ["CODEX_MOCK"] = "true"
        log_event(
            task_id,
            "codex",
            "auto_degrade",
            {"failure_count": CODEX_FAILURE_COUNT, "reason": message},
        )


def _reset_codex_failure_counter() -> None:
    # pylint: disable=global-statement
    global CODEX_FAILURE_COUNT
    CODEX_FAILURE_COUNT = 0


@router.post("", response_model=CreateTaskResponse)
async def create_task(
    question: str = Form(...),
    file: UploadFile = File(...),
    use_mock: bool | None = Query(
        default=None,
        description="If set, overrides CODEX_MOCK for this request. Prefer query string "
        "so clients using multipart file upload do not lose this flag.",
    ),
    model: str | None = Query(
        default=None,
        description="Optional per-request Codex model override (e.g. gpt-5.4-mini).",
    ),
    reasoning_effort: str | None = Query(
        default=None,
        description="Optional per-request reasoning effort override (low/medium/high).",
    ),
    think_level: str | None = Query(
        default=None,
        description="Alias of reasoning_effort.",
    ),
) -> CreateTaskResponse:
    task_id = str(uuid.uuid4())
    df, schema_profile = profile_upload(file)
    explicit = use_mock
    use_mock_flag = _effective_use_mock(explicit)
    adapter = get_provider(
        use_mock_flag,
        model=model,
        reasoning_effort=_effective_reasoning_effort(reasoning_effort, think_level),
    )
    try:
        plan = await adapter.generate_plan(
            question=question, schema_profile=schema_profile, task_id=task_id
        )
        log_event(task_id, "plan", "plan_generated", {"use_mock": use_mock_flag})
    except (CodexAdapterError, Exception) as exc:
        _record_codex_failure(task_id, str(exc))
        if not use_mock_flag:
            if explicit is False:
                raise HTTPException(
                    status_code=502,
                    detail=f"Codex plan generation failed (mock fallback disabled for this request): {exc}",
                ) from exc
            # Env-driven real Codex: allow silent mock fallback when CLI is unavailable.
            plan = await MockProvider().generate_plan(
                question=question, schema_profile=schema_profile, task_id=task_id
            )
            schema_profile["codex_fallback_reason"] = str(exc)
            log_event(
                task_id,
                "plan",
                "codex_fallback",
                {"error_type": "codex_error", "error": str(exc)},
            )
        else:
            raise
    else:
        if not use_mock_flag:
            _reset_codex_failure_counter()

    record = TaskRecord(
        task_id=task_id,
        status=TaskStatus.PLANNED,
        input=TaskInput(
            question=question,
            filename=schema_profile["filename"],
            row_count=schema_profile["row_count"],
            column_count=schema_profile["column_count"],
        ),
        plan=plan,
    )
    TASKS[task_id] = record
    TASK_DATAFRAMES[task_id] = df
    TASK_SNAPSHOTS[task_id] = {"schema_profile": schema_profile}
    _persist_task(record)
    save_snapshot(task_id, "input", record.input.model_dump())
    save_snapshot(task_id, "schema_profile", schema_profile)
    save_snapshot(task_id, "plan", plan.model_dump())
    log_event(task_id, "create_task", "task_created", {"status": record.status.value})

    return CreateTaskResponse(task_id=task_id, status=record.status, plan=plan)


@router.post("/{task_id}/revise", response_model=RevisePlanResponse)
async def revise_plan(
    task_id: str,
    payload: ReviseRequest,
    use_mock: bool | None = Query(
        default=None,
        description="If set, overrides JSON body use_mock for this request.",
    ),
    model: str | None = Query(
        default=None,
        description="Optional per-request Codex model override (e.g. gpt-5.4-mini).",
    ),
    reasoning_effort: str | None = Query(
        default=None,
        description="Optional per-request reasoning effort override (low/medium/high).",
    ),
    think_level: str | None = Query(
        default=None,
        description="Alias of reasoning_effort.",
    ),
) -> RevisePlanResponse:
    """Regenerate the analysis plan from user feedback before execution."""
    record = TASKS.get(task_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if record.plan is None:
        raise HTTPException(status_code=400, detail="Task has no plan to revise")
    if record.status != TaskStatus.PLANNED:
        raise HTTPException(
            status_code=400,
            detail="Plan can only be revised while the task is in planned state",
        )

    instruction = payload.instruction.strip()
    if not instruction:
        raise HTTPException(status_code=400, detail="instruction must not be empty")

    snapshots = TASK_SNAPSHOTS.get(task_id) or {}
    schema_profile = snapshots.get("schema_profile")
    if not schema_profile:
        raise HTTPException(
            status_code=500,
            detail="Schema profile missing for task; cannot revise plan",
        )

    explicit = use_mock if use_mock is not None else payload.use_mock
    use_mock_flag = _effective_use_mock(explicit)
    adapter = get_provider(
        use_mock_flag,
        model=model,
        reasoning_effort=_effective_reasoning_effort(reasoning_effort, think_level),
    )

    try:
        new_plan = await adapter.revise_plan(
            current_plan=record.plan,
            instruction=instruction,
            schema_profile=schema_profile,
            task_id=task_id,
        )
        log_event(task_id, "plan", "plan_revised", {"use_mock": use_mock_flag})
    except (CodexAdapterError, Exception) as exc:
        _record_codex_failure(task_id, str(exc))
        if not use_mock_flag:
            if explicit is False:
                raise HTTPException(
                    status_code=502,
                    detail=f"Codex plan revision failed (mock fallback disabled): {exc}",
                ) from exc
            new_plan = await MockProvider().revise_plan(
                current_plan=record.plan,
                instruction=instruction,
                schema_profile=schema_profile,
                task_id=task_id,
            )
            log_event(
                task_id,
                "plan",
                "codex_revise_fallback",
                {"error_type": "codex_error", "error": str(exc)},
            )
    else:
        if not use_mock_flag:
            _reset_codex_failure_counter()

    record.plan = new_plan
    record.updated_at = datetime.now(timezone.utc)
    _persist_task(record)
    save_snapshot(task_id, "plan", new_plan.model_dump())
    log_event(task_id, "revise", "plan_updated", {"status": record.status.value})

    return RevisePlanResponse(task_id=task_id, plan=new_plan)


@router.get("/history", response_model=list[TaskHistoryItem])
async def get_task_history(
    limit: int = Query(default=50, ge=1, le=500),
) -> list[TaskHistoryItem]:
    rows = list_task_records(limit=limit)
    return [TaskHistoryItem.model_validate(r) for r in rows]


@router.get("/{task_id}", response_model=TaskRecord)
async def get_task(task_id: str) -> TaskRecord:
    return _get_task_or_404(task_id)


@router.post("/{task_id}/review", response_model=TaskRecord)
async def submit_review(
    task_id: str,
    payload: ReviewRequest,
    use_mock: bool | None = Query(
        default=None,
        description="If set, overrides JSON body use_mock for this request.",
    ),
    model: str | None = Query(
        default=None,
        description="Optional per-request Codex model override (e.g. gpt-5.4-mini).",
    ),
    reasoning_effort: str | None = Query(
        default=None,
        description="Optional per-request reasoning effort override (low/medium/high).",
    ),
    think_level: str | None = Query(
        default=None,
        description="Alias of reasoning_effort.",
    ),
) -> TaskRecord:
    record = _get_task_or_404(task_id)

    if record.plan is not None:
        review_diff = diff_dicts(record.plan.model_dump(), payload.final_plan.model_dump())
        save_snapshot(task_id, "review_diff", review_diff)
        log_event(
            task_id,
            "review",
            "review_submitted",
            {"diff_keys": list(review_diff.keys())},
        )

    record.final_plan = payload.final_plan
    _update_status(record, TaskStatus.REVIEWING)
    _persist_task(record)
    _update_status(record, TaskStatus.RUNNING)
    _persist_task(record)
    try:
        df = TASK_DATAFRAMES.get(task_id)
        if df is None:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Task source data is not in memory (likely server restart). "
                    "Please create a new /task with the original file."
                ),
            )
        record.result = run_plan(df=df, plan=payload.final_plan)
        result_summary = {
            "row_count": len(record.result.table.rows),
            "columns": record.result.table.columns,
            "chart_type": record.result.chart.chart_type.value,
        }
        explicit = use_mock if use_mock is not None else payload.use_mock
        use_mock_flag = _effective_use_mock(explicit)
        adapter = get_provider(
            use_mock_flag,
            model=model,
            reasoning_effort=_effective_reasoning_effort(
                reasoning_effort, think_level
            ),
        )
        try:
            summary_text = await adapter.generate_summary(
                goal=payload.final_plan.goal,
                result_df_summary=result_summary,
                task_id=task_id,
            )
            record.result.summary = summary_text
        except Exception:
            record.result.summary = (
                f"目标：{payload.final_plan.goal}。"
                f"返回 {result_summary['row_count']} 行结果。"
            )
            _record_codex_failure(task_id, "summary_generation_failed")
            log_event(
                task_id,
                "summary",
                "summary_fallback",
                {"error_type": "codex_error"},
            )
        try:
            follow_ups = await adapter.generate_followups(
                goal=payload.final_plan.goal,
                result_df_summary=result_summary,
                task_id=task_id,
            )
            record.result.follow_ups = follow_ups
        except Exception:
            record.result.follow_ups = [
                "是否需要按时间维度继续钻取？",
                "是否需要按类别维度做分组对比？",
                "是否需要查看异常值对应明细？",
            ]
        save_snapshot(task_id, "final_plan", payload.final_plan.model_dump())
        save_snapshot(task_id, "result", record.result.model_dump())
        log_event(task_id, "run", "task_completed", {"status": TaskStatus.COMPLETED.value})
        _update_status(record, TaskStatus.COMPLETED)
        _persist_task(record)
    except Exception as exc:  # pragma: no cover - runtime defensive handling
        if isinstance(exc, HTTPException):
            _update_status(record, TaskStatus.FAILED)
            record.error = TaskError(error_type="data_missing", message=str(exc.detail))
            _persist_task(record)
            raise
        error_type = "exec_error"
        message = str(exc).lower()
        if "timeout" in message:
            error_type = "codex_timeout"
        elif "parse" in message:
            error_type = "parse_error"
        record.error = TaskError(error_type=error_type, message=str(exc))
        save_snapshot(task_id, "error", record.error.model_dump())
        log_event(
            task_id,
            "run",
            "task_failed",
            {"status": TaskStatus.FAILED.value, "error_type": error_type},
        )
        _update_status(record, TaskStatus.FAILED)
        _persist_task(record)
    return record


@router.get("/{task_id}/result")
async def get_result(task_id: str) -> dict:
    record = _get_task_or_404(task_id)
    if record.result is None:
        return {
            "task_id": task_id,
            "status": record.status,
            "message": "Result not ready yet",
        }
    return record.result.model_dump()


@router.post("/{task_id}/fail", response_model=TaskRecord)
async def fail_task(task_id: str, message: str = Form(...)) -> TaskRecord:
    """Utility route to mark task as failed during development."""
    record = _get_task_or_404(task_id)
    record.error = TaskError(error_type="manual_fail", message=message)
    _update_status(record, TaskStatus.FAILED)
    _persist_task(record)
    return record


@router.post("/{task_id}/reset", response_model=TaskRecord)
async def reset_task(task_id: str) -> TaskRecord:
    """Recover a stuck task by setting it back to planned."""
    record = _get_task_or_404(task_id)
    _update_status(record, TaskStatus.PLANNED)
    _persist_task(record)
    log_event(task_id, "recovery", "task_reset", {"status": TaskStatus.PLANNED.value})
    return record


@router.delete("/{task_id}")
async def delete_task(task_id: str) -> dict[str, int]:
    TASKS.pop(task_id, None)
    TASK_DATAFRAMES.pop(task_id, None)
    TASK_SNAPSHOTS.pop(task_id, None)
    deleted = delete_task_record(task_id)
    return {"deleted": deleted}

