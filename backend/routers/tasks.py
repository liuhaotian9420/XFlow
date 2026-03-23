"""Task CRUD endpoints."""

from __future__ import annotations

import os
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel

from backend.codex.adapter import CodexAdapterError, get_adapter
from backend.codex.mock import MockAdapter
from backend.execution.engine import run_plan
from backend.observability import diff_dicts, log_event, save_snapshot
from backend.profiler.schema_profiler import profile_upload
from backend.schemas.plan import AnalysisPlan
from backend.schemas.task import TaskError, TaskInput, TaskRecord, TaskStatus
from backend.storage import CODEX_FAILURE_COUNT, TASK_DATAFRAMES, TASK_SNAPSHOTS, TASKS

router = APIRouter(prefix="/tasks", tags=["tasks"])


class ReviewRequest(BaseModel):
    final_plan: AnalysisPlan


class CreateTaskResponse(BaseModel):
    task_id: str
    status: TaskStatus
    plan: AnalysisPlan


def _update_status(record: TaskRecord, status: TaskStatus) -> None:
    record.status = status
    record.updated_at = datetime.now(timezone.utc)


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
    question: str = Form(...), file: UploadFile = File(...)
) -> CreateTaskResponse:
    task_id = str(uuid.uuid4())
    df, schema_profile = profile_upload(file)
    use_mock = os.getenv("CODEX_MOCK", "true").lower() == "true"
    adapter = MockAdapter() if use_mock else get_adapter()
    try:
        plan = await adapter.generate_plan(
            question=question, schema_profile=schema_profile, task_id=task_id
        )
        log_event(task_id, "plan", "plan_generated", {"use_mock": use_mock})
    except (CodexAdapterError, Exception) as exc:
        _record_codex_failure(task_id, str(exc))
        if not use_mock:
            # Fallback to mock when Codex runtime is unavailable.
            plan = await MockAdapter().generate_plan(
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
        if not use_mock:
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
    save_snapshot(task_id, "input", record.input.model_dump())
    save_snapshot(task_id, "schema_profile", schema_profile)
    save_snapshot(task_id, "plan", plan.model_dump())
    log_event(task_id, "create_task", "task_created", {"status": record.status.value})

    return CreateTaskResponse(task_id=task_id, status=record.status, plan=plan)


@router.get("/{task_id}", response_model=TaskRecord)
async def get_task(task_id: str) -> TaskRecord:
    record = TASKS.get(task_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return record


@router.post("/{task_id}/review", response_model=TaskRecord)
async def submit_review(task_id: str, payload: ReviewRequest) -> TaskRecord:
    record = TASKS.get(task_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Task not found")

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
    _update_status(record, TaskStatus.RUNNING)
    try:
        df = TASK_DATAFRAMES[task_id]
        record.result = run_plan(df=df, plan=payload.final_plan)
        result_summary = {
            "row_count": len(record.result.table.rows),
            "columns": record.result.table.columns,
            "chart_type": record.result.chart.chart_type.value,
        }
        use_mock = os.getenv("CODEX_MOCK", "true").lower() == "true"
        adapter = MockAdapter() if use_mock else get_adapter()
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
    except Exception as exc:  # pragma: no cover - runtime defensive handling
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
    return record


@router.get("/{task_id}/result")
async def get_result(task_id: str) -> dict:
    record = TASKS.get(task_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Task not found")
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
    record = TASKS.get(task_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Task not found")
    record.error = TaskError(error_type="manual_fail", message=message)
    _update_status(record, TaskStatus.FAILED)
    return record


@router.post("/{task_id}/reset", response_model=TaskRecord)
async def reset_task(task_id: str) -> TaskRecord:
    """Recover a stuck task by setting it back to planned."""
    record = TASKS.get(task_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Task not found")
    _update_status(record, TaskStatus.PLANNED)
    log_event(task_id, "recovery", "task_reset", {"status": TaskStatus.PLANNED.value})
    return record

