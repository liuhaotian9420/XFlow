"""Structured logging and snapshot utilities."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = ROOT_DIR / "artifacts"
LOG_FILE = ARTIFACT_DIR / "events.log"


def _ensure_artifact_dirs(task_id: str) -> Path:
    task_dir = ARTIFACT_DIR / "tasks" / task_id
    task_dir.mkdir(parents=True, exist_ok=True)
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    return task_dir


def log_event(task_id: str, stage: str, event_type: str, payload: dict[str, Any]) -> None:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    event = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "task_id": task_id,
        "stage": stage,
        "event_type": event_type,
        "payload": payload,
    }
    with LOG_FILE.open("a", encoding="utf-8") as fp:
        fp.write(json.dumps(event, ensure_ascii=False) + "\n")


def save_snapshot(task_id: str, name: str, payload: dict[str, Any]) -> Path:
    task_dir = _ensure_artifact_dirs(task_id)
    output = task_dir / f"{name}.json"
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return output


def diff_dicts(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    keys = sorted(set(before.keys()) | set(after.keys()))
    diff: dict[str, Any] = {}
    for key in keys:
        old = before.get(key)
        new = after.get(key)
        if old != new:
            diff[key] = {"before": old, "after": new}
    return diff

