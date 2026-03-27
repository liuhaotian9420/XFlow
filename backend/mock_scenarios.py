from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from threading import Lock
from typing import Any

from backend.schemas.plan import AnalysisPlan
from backend.schemas.result import ResultPayload
from backend.schemas.task import ReviewState, ReviewType, TaskReview, TaskStatus

LOG = logging.getLogger(__name__)
REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCENARIO_DIR = REPO_ROOT / "artifacts" / "mock_scenarios"
DEFAULT_SCENARIO_ID = "default"
_CURSOR_LOCK = Lock()
_CURSORS: dict[str, int] = {}
_SCENARIO_CACHE: dict[str, dict[str, Any] | None] = {}


def _scenario_dir() -> Path:
    raw = os.getenv("MOCK_SCENARIO_DIR", "").strip()
    if not raw:
        return DEFAULT_SCENARIO_DIR
    p = Path(raw)
    if not p.is_absolute():
        p = (REPO_ROOT / p).resolve()
    return p


def default_scenario_id() -> str:
    return os.getenv("MOCK_SCENARIO_ID", DEFAULT_SCENARIO_ID).strip() or DEFAULT_SCENARIO_ID


def _load_scenario(scenario_id: str) -> dict[str, Any] | None:
    sid = (scenario_id or "").strip() or DEFAULT_SCENARIO_ID
    cached = _SCENARIO_CACHE.get(sid, None)
    if sid in _SCENARIO_CACHE:
        return cached
    path = _scenario_dir() / f"{sid}.json"
    if not path.is_file():
        _SCENARIO_CACHE[sid] = None
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        LOG.warning("Failed to load mock scenario %s from %s: %s", sid, path, exc)
        _SCENARIO_CACHE[sid] = None
        return None
    if not isinstance(payload, dict):
        _SCENARIO_CACHE[sid] = None
        return None
    _SCENARIO_CACHE[sid] = payload
    return payload


def _steps_for(scenario: dict[str, Any], stage: str) -> tuple[list[dict[str, Any]], str]:
    block = scenario.get(stage)
    strategy = str(scenario.get("on_exhausted") or "repeat_last").strip().lower() or "repeat_last"
    if isinstance(block, dict):
        strategy = str(block.get("on_exhausted") or strategy).strip().lower() or strategy
        steps = block.get("steps")
    else:
        steps = block
    if not isinstance(steps, list):
        return [], strategy
    out = [step for step in steps if isinstance(step, dict)]
    return out, strategy


def _cursor_key(*parts: str) -> str:
    return ":".join(part.strip() for part in parts if part.strip())


def _select_step(cursor_key: str, steps: list[dict[str, Any]], strategy: str) -> dict[str, Any] | None:
    if not steps:
        return None
    with _CURSOR_LOCK:
        idx = _CURSORS.get(cursor_key, 0)
        if idx < len(steps):
            _CURSORS[cursor_key] = idx + 1
            return steps[idx]
        if strategy == "loop":
            idx = idx % len(steps)
            _CURSORS[cursor_key] = idx + 1
            return steps[idx]
        if strategy == "repeat_last":
            return steps[-1]
        return None


def _next_step(stage: str, scope: str, scope_id: str, scenario_id: str | None = None) -> dict[str, Any] | None:
    scenario = _load_scenario(scenario_id or default_scenario_id())
    if scenario is None:
        return None
    steps, strategy = _steps_for(scenario, stage)
    return _select_step(_cursor_key(scope, scope_id, stage), steps, strategy)


def next_chat_reply(session_id: str, *, scenario_id: str | None = None) -> str | None:
    step = _next_step("chat", "chat", session_id, scenario_id)
    if step is None:
        return None
    reply = step.get("reply")
    return str(reply).strip() if isinstance(reply, str) else None


def next_stream_events(session_id: str, *, scenario_id: str | None = None) -> list[dict[str, Any]] | None:
    scenario = _load_scenario(scenario_id or default_scenario_id())
    if scenario is None:
        return None
    steps, strategy = _steps_for(scenario, "chat_stream")
    step = _select_step(_cursor_key("chat", session_id, "chat_stream"), steps, strategy)
    if step is None:
        return None
    events = step.get("events")
    if not isinstance(events, list):
        reply = step.get("reply")
        if isinstance(reply, str) and reply.strip():
            return [{"type": "final", "reply": reply.strip()}]
        return None
    return [event for event in events if isinstance(event, dict)]


def next_task_create_payload(task_id: str, *, scenario_id: str | None = None) -> dict[str, Any] | None:
    return _next_step("task_create", "task", task_id, scenario_id)


def next_task_revise_payload(task_id: str, *, scenario_id: str | None = None) -> dict[str, Any] | None:
    return _next_step("task_revise", "task", task_id, scenario_id)


def next_task_review_payload(task_id: str, *, scenario_id: str | None = None) -> dict[str, Any] | None:
    return _next_step("task_review_respond", "task", task_id, scenario_id)


def next_task_run_payload(task_id: str, *, scenario_id: str | None = None) -> dict[str, Any] | None:
    return _next_step("task_run", "task", task_id, scenario_id)


def parse_plan_payload(payload: Any) -> AnalysisPlan | None:
    if not isinstance(payload, dict):
        return None
    try:
        return AnalysisPlan.model_validate(payload)
    except Exception as exc:
        LOG.warning("Invalid mock scenario plan payload: %s", exc)
        return None


def parse_result_payload(payload: Any) -> ResultPayload | None:
    if not isinstance(payload, dict):
        return None
    try:
        return ResultPayload.model_validate(payload)
    except Exception as exc:
        LOG.warning("Invalid mock scenario result payload: %s", exc)
        return None


def parse_review_payload(payload: Any) -> TaskReview | None:
    if not isinstance(payload, dict):
        return None
    try:
        review_type = ReviewType(str(payload.get("review_type") or "suggestion").strip().lower())
        state = ReviewState(str(payload.get("state") or "pending").strip().lower())
        title = str(payload.get("title") or "").strip()
        message = str(payload.get("message") or "").strip()
        if not title or not message:
            return None
        suggested_plan = parse_plan_payload(payload.get("suggested_plan"))
        return TaskReview(
            review_id=str(payload.get("review_id") or f"mock-review-{os.urandom(4).hex()}"),
            review_type=review_type,
            state=state,
            title=title,
            message=message,
            options=[str(x) for x in list(payload.get("options") or [])],
            suggested_plan=suggested_plan,
        )
    except Exception as exc:
        LOG.warning("Invalid mock scenario review payload: %s", exc)
        return None


def parse_status(value: Any, default: TaskStatus) -> TaskStatus:
    try:
        return TaskStatus(str(value or default.value).strip().lower())
    except Exception:
        return default
