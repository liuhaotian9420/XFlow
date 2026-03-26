"""SQLite persistence for chat sessions and turns."""

from __future__ import annotations

import os
import sqlite3
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from backend.schemas.task import TaskRecord


def _db_path() -> Path:
    raw = os.getenv("CHAT_SQLITE_PATH", "").strip()
    if raw:
        p = Path(raw).expanduser()
    else:
        p = Path("artifacts") / "chat_sessions.sqlite3"
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(str(_db_path()), timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


def init_chat_store() -> None:
    with _connect() as conn:
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS chat_sessions (
              session_id TEXT PRIMARY KEY,
              created_at TEXT NOT NULL,
              updated_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS chat_turns (
              turn_id TEXT PRIMARY KEY,
              session_id TEXT NOT NULL,
              chat_id TEXT NOT NULL,
              created_at TEXT NOT NULL,
              user_message TEXT NOT NULL,
              history_turns INTEGER NOT NULL DEFAULT 0,
              use_mock INTEGER NOT NULL DEFAULT 0,
              model TEXT,
              reasoning_effort TEXT,
              provider_name TEXT,
              reply_text TEXT,
              is_fallback INTEGER NOT NULL DEFAULT 0,
              error_text TEXT,
              prompt_chars INTEGER,
              input_tokens INTEGER,
              output_tokens INTEGER,
              cached_input_tokens INTEGER,
              codex_exec_elapsed_s REAL,
              codex_spawn_elapsed_s REAL,
              codex_ttft_elapsed_s REAL,
              codex_generation_elapsed_s REAL,
              codex_teardown_elapsed_s REAL,
              provider_elapsed_s REAL,
              provider_overhead_elapsed_s REAL,
              prompt_build_elapsed_s REAL,
              api_elapsed_s REAL,
              debug_prompt TEXT,
              FOREIGN KEY(session_id) REFERENCES chat_sessions(session_id)
            )
            """
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_chat_turns_session_created ON chat_turns(session_id, created_at)"
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS task_records (
              task_id TEXT PRIMARY KEY,
              created_at TEXT NOT NULL,
              updated_at TEXT NOT NULL,
              status TEXT NOT NULL,
              question TEXT,
              filename TEXT,
              record_json TEXT NOT NULL
            )
            """
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_task_records_updated ON task_records(updated_at DESC)"
        )


def upsert_session(session_id: str) -> None:
    now = datetime.now(timezone.utc).isoformat()
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO chat_sessions(session_id, created_at, updated_at)
            VALUES (?, ?, ?)
            ON CONFLICT(session_id) DO UPDATE SET updated_at=excluded.updated_at
            """,
            (session_id, now, now),
        )


def save_chat_turn(payload: dict[str, Any]) -> None:
    upsert_session(str(payload["session_id"]))
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO chat_turns(
              turn_id, session_id, chat_id, created_at,
              user_message, history_turns, use_mock, model, reasoning_effort,
              provider_name, reply_text, is_fallback, error_text, prompt_chars,
              input_tokens, output_tokens, cached_input_tokens,
              codex_exec_elapsed_s, codex_spawn_elapsed_s, codex_ttft_elapsed_s,
              codex_generation_elapsed_s, codex_teardown_elapsed_s,
              provider_elapsed_s, provider_overhead_elapsed_s, prompt_build_elapsed_s,
              api_elapsed_s, debug_prompt
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                payload["turn_id"],
                payload["session_id"],
                payload["chat_id"],
                datetime.now(timezone.utc).isoformat(),
                payload.get("user_message", ""),
                int(payload.get("history_turns", 0) or 0),
                1 if payload.get("use_mock") else 0,
                payload.get("model"),
                payload.get("reasoning_effort"),
                payload.get("provider_name"),
                payload.get("reply_text"),
                1 if payload.get("is_fallback") else 0,
                payload.get("error_text"),
                payload.get("prompt_chars"),
                payload.get("input_tokens"),
                payload.get("output_tokens"),
                payload.get("cached_input_tokens"),
                payload.get("codex_exec_elapsed_s"),
                payload.get("codex_spawn_elapsed_s"),
                payload.get("codex_ttft_elapsed_s"),
                payload.get("codex_generation_elapsed_s"),
                payload.get("codex_teardown_elapsed_s"),
                payload.get("provider_elapsed_s"),
                payload.get("provider_overhead_elapsed_s"),
                payload.get("prompt_build_elapsed_s"),
                payload.get("api_elapsed_s"),
                payload.get("debug_prompt"),
            ),
        )


def list_sessions(limit: int = 50) -> list[dict[str, Any]]:
    with _connect() as conn:
        rows = conn.execute(
            """
            SELECT s.session_id, s.created_at, s.updated_at, COUNT(t.turn_id) AS turn_count
            FROM chat_sessions s
            LEFT JOIN chat_turns t ON t.session_id = s.session_id
            GROUP BY s.session_id, s.created_at, s.updated_at
            ORDER BY s.updated_at DESC
            LIMIT ?
            """,
            (int(limit),),
        ).fetchall()
    return [dict(r) for r in rows]


def list_session_turns(session_id: str, limit: int = 200) -> list[dict[str, Any]]:
    with _connect() as conn:
        rows = conn.execute(
            """
            SELECT *
            FROM chat_turns
            WHERE session_id = ?
            ORDER BY created_at ASC
            LIMIT ?
            """,
            (session_id, int(limit)),
        ).fetchall()
    return [dict(r) for r in rows]


def recent_codex_exec_samples(
    *,
    model: str | None = None,
    reasoning_effort: str | None = None,
    limit: int = 40,
) -> list[float]:
    clauses = [
        "use_mock = 0",
        "is_fallback = 0",
        "codex_exec_elapsed_s IS NOT NULL",
        "codex_exec_elapsed_s > 0",
    ]
    params: list[Any] = []
    if (model or "").strip():
        clauses.append("model = ?")
        params.append((model or "").strip())
    if (reasoning_effort or "").strip():
        clauses.append("reasoning_effort = ?")
        params.append((reasoning_effort or "").strip())
    where_sql = " AND ".join(clauses)
    params.append(int(limit))
    with _connect() as conn:
        rows = conn.execute(
            f"""
            SELECT codex_exec_elapsed_s
            FROM chat_turns
            WHERE {where_sql}
            ORDER BY created_at DESC
            LIMIT ?
            """,
            tuple(params),
        ).fetchall()
    out: list[float] = []
    for row in rows:
        try:
            value = float(row["codex_exec_elapsed_s"])
        except (TypeError, ValueError):
            continue
        if value > 0:
            out.append(value)
    return out


def delete_session(session_id: str) -> int:
    with _connect() as conn:
        conn.execute("DELETE FROM chat_turns WHERE session_id = ?", (session_id,))
        cur = conn.execute("DELETE FROM chat_sessions WHERE session_id = ?", (session_id,))
        return int(cur.rowcount or 0)


def delete_all_sessions() -> int:
    with _connect() as conn:
        conn.execute("DELETE FROM chat_turns")
        cur = conn.execute("DELETE FROM chat_sessions")
        return int(cur.rowcount or 0)


def save_task_record(record: TaskRecord) -> None:
    payload = record.model_dump(mode="json")
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO task_records(task_id, created_at, updated_at, status, question, filename, record_json)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(task_id) DO UPDATE SET
              created_at=excluded.created_at,
              updated_at=excluded.updated_at,
              status=excluded.status,
              question=excluded.question,
              filename=excluded.filename,
              record_json=excluded.record_json
            """,
            (
                record.task_id,
                record.created_at.isoformat(),
                record.updated_at.isoformat(),
                record.status.value,
                record.input.question,
                record.input.filename,
                json.dumps(payload, ensure_ascii=False),
            ),
        )


def get_task_record(task_id: str) -> TaskRecord | None:
    with _connect() as conn:
        row = conn.execute(
            "SELECT record_json FROM task_records WHERE task_id = ?",
            (task_id,),
        ).fetchone()
    if not row:
        return None
    return TaskRecord.model_validate(json.loads(str(row["record_json"])))


def list_task_records(limit: int = 50) -> list[dict[str, Any]]:
    with _connect() as conn:
        rows = conn.execute(
            """
            SELECT task_id, created_at, updated_at, status, question, filename
            FROM task_records
            ORDER BY updated_at DESC
            LIMIT ?
            """,
            (int(limit),),
        ).fetchall()
    return [dict(r) for r in rows]


def delete_task_record(task_id: str) -> int:
    with _connect() as conn:
        cur = conn.execute("DELETE FROM task_records WHERE task_id = ?", (task_id,))
        return int(cur.rowcount or 0)


def load_recent_task_records(limit: int = 500) -> list[TaskRecord]:
    with _connect() as conn:
        rows = conn.execute(
            """
            SELECT record_json
            FROM task_records
            ORDER BY updated_at DESC
            LIMIT ?
            """,
            (int(limit),),
        ).fetchall()
    out: list[TaskRecord] = []
    for row in rows:
        try:
            out.append(TaskRecord.model_validate(json.loads(str(row["record_json"]))))
        except Exception:
            continue
    return out
