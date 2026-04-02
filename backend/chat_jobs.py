"""In-memory chat job registry for non-blocking chat polling."""

from __future__ import annotations

import asyncio
import copy
import threading
import time
import uuid
from collections.abc import Awaitable, Callable
from typing import Any

TERMINAL_STATUSES = {"completed", "failed"}


class ChatJobRegistry:
    """Tracks in-flight chat jobs and latest polling snapshots."""

    def __init__(self, *, max_events: int = 200, max_jobs: int = 500) -> None:
        self._jobs: dict[str, dict[str, Any]] = {}
        self._tasks: dict[str, asyncio.Task[Any]] = {}
        self._lock = threading.Lock()
        self._max_events = max(20, int(max_events))
        self._max_jobs = max(50, int(max_jobs))

    def create_job(
        self,
        *,
        session_id: str,
        turn_id: str,
        chat_id: str,
        runner: Callable[[], Awaitable[None]],
        job_id: str | None = None,
    ) -> dict[str, Any]:
        resolved_job_id = (job_id or "").strip() or str(uuid.uuid4())
        now = time.time()
        with self._lock:
            self._jobs[resolved_job_id] = {
                "job_id": resolved_job_id,
                "status": "queued",
                "created_at": now,
                "updated_at": now,
                "session_id": session_id,
                "turn_id": turn_id,
                "chat_id": chat_id,
                "latest_text": "",
                "latest_reasoning_text": "",
                "latest_command": None,
                "stream_events": [],
                "final_reply": None,
                "timing": {},
                "usage": {},
                "runtime_vendor": None,
                "runtime_binary": None,
                "error": None,
            }
            self._trim_jobs_locked()
        task = asyncio.create_task(self._run_job(resolved_job_id, runner))
        with self._lock:
            self._tasks[resolved_job_id] = task
        return self.get_snapshot(resolved_job_id) or {
            "job_id": resolved_job_id,
            "status": "queued",
        }

    async def _run_job(
        self,
        job_id: str,
        runner: Callable[[], Awaitable[None]],
    ) -> None:
        self.mark_running(job_id)
        try:
            await runner()
        except Exception as exc:
            self.mark_failed(job_id, f"{type(exc).__name__}: {exc!s}")
        finally:
            with self._lock:
                task = self._tasks.pop(job_id, None)
                snapshot = self._jobs.get(job_id)
                if snapshot and snapshot.get("status") not in TERMINAL_STATUSES:
                    snapshot["status"] = "failed"
                    snapshot["error"] = "Chat job ended without terminal event."
                    snapshot["updated_at"] = time.time()
            if task and task.cancelled():
                self.mark_failed(job_id, "Cancelled")

    def mark_running(self, job_id: str) -> None:
        with self._lock:
            job = self._jobs.get(job_id)
            if not job:
                return
            if job.get("status") == "queued":
                job["status"] = "running"
                job["updated_at"] = time.time()

    def mark_failed(self, job_id: str, error: str) -> None:
        with self._lock:
            job = self._jobs.get(job_id)
            if not job:
                return
            if job.get("status") == "completed":
                return
            job["status"] = "failed"
            job["error"] = (error or "").strip() or "Unknown error"
            job["updated_at"] = time.time()

    def append_event(self, job_id: str, event: dict[str, Any]) -> None:
        et = str(event.get("type") or "").strip().lower()
        now = time.time()
        with self._lock:
            job = self._jobs.get(job_id)
            if not job:
                return
            events = job.setdefault("stream_events", [])
            if isinstance(events, list):
                events.append(dict(event))
                if len(events) > self._max_events:
                    del events[: len(events) - self._max_events]

            if isinstance(event.get("session_id"), str) and event.get("session_id"):
                job["session_id"] = str(event["session_id"])
            if isinstance(event.get("turn_id"), str) and event.get("turn_id"):
                job["turn_id"] = str(event["turn_id"])
            if isinstance(event.get("chat_id"), str) and event.get("chat_id"):
                job["chat_id"] = str(event["chat_id"])

            if et == "agent.message.completed":
                job["latest_text"] = str(event.get("text") or "").strip()
            elif et == "reasoning.completed":
                job["latest_reasoning_text"] = str(event.get("text") or "").strip()
            elif et == "command.completed":
                job["latest_command"] = {
                    "command": event.get("command"),
                    "exit_code": event.get("exit_code"),
                    "output_preview": event.get("output_preview"),
                }
            elif et == "error":
                detail = str(event.get("error") or "").strip()
                if detail:
                    job["error"] = detail
            elif et == "final":
                job["status"] = "completed"
                job["final_reply"] = str(event.get("reply") or "")
                timing = event.get("timing")
                usage = event.get("usage")
                job["timing"] = timing if isinstance(timing, dict) else {}
                job["usage"] = usage if isinstance(usage, dict) else {}
                job["runtime_vendor"] = event.get("runtime_vendor")
                job["runtime_binary"] = event.get("runtime_binary")
                if isinstance(event.get("error"), str) and str(event.get("error")).strip():
                    job["error"] = str(event.get("error")).strip()
            if job.get("status") == "queued":
                job["status"] = "running"
            job["updated_at"] = now

    def get_snapshot(self, job_id: str) -> dict[str, Any] | None:
        with self._lock:
            item = self._jobs.get(job_id)
            if item is None:
                return None
            return copy.deepcopy(item)

    def _trim_jobs_locked(self) -> None:
        if len(self._jobs) <= self._max_jobs:
            return
        candidates: list[tuple[float, str]] = []
        for job_id, snapshot in self._jobs.items():
            if snapshot.get("status") in TERMINAL_STATUSES:
                candidates.append((float(snapshot.get("updated_at") or 0.0), job_id))
        candidates.sort(key=lambda x: x[0])
        overflow = len(self._jobs) - self._max_jobs
        for _, job_id in candidates[:overflow]:
            self._jobs.pop(job_id, None)
            self._tasks.pop(job_id, None)


CHAT_JOBS = ChatJobRegistry()
