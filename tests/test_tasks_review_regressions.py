"""Regression tests for plan/review boundary behavior in tasks router."""

from __future__ import annotations

import asyncio
import sys
import types
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Test environment may not install python-multipart; provide a minimal stub so
# FastAPI route registration can import successfully.
multipart_stub = types.ModuleType("multipart")
multipart_stub.__version__ = "0.0-test"
multipart_sub_stub = types.ModuleType("multipart.multipart")
multipart_sub_stub.parse_options_header = lambda value: ("", {})
sys.modules.setdefault("multipart", multipart_stub)
sys.modules.setdefault("multipart.multipart", multipart_sub_stub)

from backend.routers import tasks
from backend.schemas.plan import AnalysisPlan
from backend.schemas.task import TaskInput, TaskRecord, TaskStatus


def _blocked_plan() -> AnalysisPlan:
    return AnalysisPlan.model_validate(
        {
            "goal": "Need required clarification before run",
            "metrics": [{"column": "amount", "aggregation": "sum", "alias": "amount_sum"}],
            "dimensions": [{"column": "region", "role": "category"}],
            "filters": [],
            "output": {"chart_type": "bar", "show_table": True},
            "assumptions": [],
            "ambiguities": [{"field": "date_range", "issue": "missing date range"}],
            "confidence": 0.3,
            "completeness": {
                "status": "blocked",
                "score": 0.3,
                "rationale": "Date range is required to avoid ambiguous aggregation.",
                "missing_information": [{"field": "date_range", "issue": "missing date range"}],
                "open_questions": [
                    {
                        "question": "What date range should be analyzed?",
                        "reason": "required for aggregation scope",
                        "blocking": True,
                        "priority": "high",
                        "related_fields": ["date_range"],
                    }
                ],
                "exploration_tasks": [],
            },
        }
    )


def test_record_codex_failure_does_not_crash_and_sets_auto_mock(monkeypatch) -> None:
    monkeypatch.setenv("CODEX_AUTO_MOCK_THRESHOLD", "1")
    monkeypatch.delenv("CODEX_MOCK", raising=False)
    tasks.CODEX_FAILURE_COUNT = 0

    tasks._record_codex_failure("task-x", "boom")

    assert tasks.CODEX_FAILURE_COUNT == 1
    assert tasks.os.getenv("CODEX_MOCK") == "true"


def test_revise_from_review_re_attaches_completeness_gate(monkeypatch) -> None:
    task_id = "task-review-revise"
    record = TaskRecord(
        task_id=task_id,
        status=TaskStatus.REVIEWING,
        input=TaskInput(question="q", filename="x.csv", row_count=10, column_count=3),
        plan=_blocked_plan(),
    )
    tasks.TASK_SNAPSHOTS[task_id] = {"schema_profile": {"filename": "x.csv"}}

    async def _revise_plan(**kwargs):
        return _blocked_plan()

    provider = SimpleNamespace(revise_plan=_revise_plan)
    monkeypatch.setattr(tasks, "get_provider", lambda *args, **kwargs: provider)
    monkeypatch.setattr(tasks, "_persist_task", lambda _record: None)
    monkeypatch.setattr(tasks, "save_snapshot", lambda *args, **kwargs: None)
    monkeypatch.setattr(tasks, "log_event", lambda *args, **kwargs: None)

    asyncio.run(
        tasks._revise_record_plan_with_instruction(
            task_id=task_id,
            record=record,
            instruction="Please use last 30 days",
            use_mock=True,
            model=None,
            reasoning_effort=None,
            think_level=None,
        )
    )

    assert record.status == TaskStatus.REVIEWING
    assert record.pending_review is not None
    assert record.pending_review.review_type.value == "suggestion"
    assert "Plan completeness: blocked" in record.pending_review.title
