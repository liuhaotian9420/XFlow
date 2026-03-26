from __future__ import annotations

import io
import json
import os
import time
from typing import Any

import requests
import streamlit as st

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")


def _api_url(path: str) -> str:
    return f"{API_BASE_URL.rstrip('/')}{path}"


def _requests_error_message(exc: requests.RequestException) -> str:
    """Surface FastAPI ``detail`` instead of only generic HTTP errors."""
    if isinstance(exc, requests.HTTPError):
        resp = exc.response
        if resp is not None:
            try:
                body = resp.json()
                detail = body.get("detail")
                if isinstance(detail, str):
                    return detail
                if isinstance(detail, list):
                    parts: list[str] = []
                    for item in detail:
                        if isinstance(item, dict):
                            loc = item.get("loc", ())
                            msg = item.get("msg", "")
                            parts.append(f"{loc}: {msg}".strip() if loc else str(msg))
                        else:
                            parts.append(str(item))
                    return "; ".join(parts) if parts else str(body)
            except (ValueError, TypeError):
                pass
            raw = (resp.text or "").strip()
            if raw:
                return raw[:8000]
    return str(exc)


def _codex_mock_query_params() -> dict[str, str]:
    use_mock = bool(st.session_state.get("use_codex_mock", True))
    params: dict[str, str] = {"use_mock": "true" if use_mock else "false"}
    model = str(st.session_state.get("codex_model_override", "") or "").strip()
    reasoning = str(
        st.session_state.get("codex_reasoning_effort_override", "") or ""
    ).strip()
    if model:
        params["model"] = model
    if reasoning:
        params["reasoning_effort"] = reasoning
    return params


def _resolve_chat_timeout_seconds() -> int:
    use_mock = bool(st.session_state.get("use_codex_mock", True))
    smart_timeout_enabled = bool(st.session_state.get("smart_timeout_enabled", True))
    if smart_timeout_enabled:
        return 120 if use_mock else int(os.getenv("STREAMLIT_CHAT_TIMEOUT_SECONDS", "300"))
    raw_timeout = str(st.session_state.get("chat_timeout_seconds", "") or "").strip()
    try:
        return max(1, int(raw_timeout))
    except ValueError:
        return 120 if use_mock else int(os.getenv("STREAMLIT_CHAT_TIMEOUT_SECONDS", "300"))


def _chat_query_params(timeout_s: int) -> dict[str, str]:
    params = _codex_mock_query_params()
    params["timeout_seconds"] = str(timeout_s)
    if bool(st.session_state.get("smart_timeout_enabled", True)):
        params["autoTimeout"] = "true"
    if bool(st.session_state.get("show_prompt_debug", False)):
        params["include_prompt_debug"] = "true"
    return params


def _ensure_schema_profile() -> dict[str, Any] | None:
    meta = st.session_state.file_meta
    if not meta:
        return None
    name = meta["name"]
    if (
        st.session_state.get("schema_profile_for") == name
        and st.session_state.get("schema_profile") is not None
    ):
        return st.session_state.schema_profile  # type: ignore[return-value]
    try:
        files = {
            "file": (
                name,
                io.BytesIO(meta["data"]),
                meta.get("type") or "application/octet-stream",
            )
        }
        response = requests.post(_api_url("/data/profile"), files=files, timeout=120)
        response.raise_for_status()
        profile = response.json()
        st.session_state.schema_profile = profile
        st.session_state.schema_profile_for = name
        return profile
    except requests.RequestException:
        return {
            "filename": name,
            "note": "Could not load schema preview; chat may be limited until the server is reachable.",
        }


def _post_task_bytes(
    filename: str,
    file_bytes: bytes,
    mime: str,
    question: str,
) -> dict[str, Any]:
    payload = {"question": question}
    files = {"file": (filename, io.BytesIO(file_bytes), mime or "application/octet-stream")}
    response = requests.post(
        _api_url("/tasks"),
        data=payload,
        files=files,
        params=_codex_mock_query_params(),
        timeout=120,
    )
    response.raise_for_status()
    return response.json()


def _post_run_task(task_id: str, plan: dict[str, Any] | None) -> dict[str, Any]:
    params = _codex_mock_query_params()
    if bool(st.session_state.get("include_demo_artifacts", False)):
        params["include_demo_artifacts"] = "true"
    response = requests.post(
        _api_url(f"/tasks/{task_id}/run"),
        json={"plan": plan} if plan is not None else {},
        params=params,
        timeout=120,
    )
    response.raise_for_status()
    return response.json()


def _post_review_respond(task_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    response = requests.post(
        _api_url(f"/tasks/{task_id}/review/respond"),
        json=payload,
        params=_codex_mock_query_params(),
        timeout=120,
    )
    response.raise_for_status()
    return response.json()


def _post_create_review_request(task_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    response = requests.post(
        _api_url(f"/tasks/{task_id}/review"),
        json=payload,
        params=_codex_mock_query_params(),
        timeout=120,
    )
    response.raise_for_status()
    return response.json()


def _get_task(task_id: str) -> dict[str, Any]:
    response = requests.get(_api_url(f"/tasks/{task_id}"), timeout=30)
    response.raise_for_status()
    return response.json()


def _get_result(task_id: str) -> dict[str, Any]:
    response = requests.get(_api_url(f"/tasks/{task_id}/result"), timeout=120)
    response.raise_for_status()
    return response.json()


def _get_chat_sessions(limit: int = 50) -> list[dict[str, Any]]:
    response = requests.get(_api_url("/chat/sessions"), params={"limit": limit}, timeout=30)
    response.raise_for_status()
    return list(response.json() or [])


def _get_chat_session_turns(session_id: str, limit: int = 200) -> list[dict[str, Any]]:
    response = requests.get(
        _api_url(f"/chat/sessions/{session_id}/turns"),
        params={"limit": limit},
        timeout=30,
    )
    response.raise_for_status()
    return list(response.json() or [])


def _delete_chat_session(session_id: str) -> int:
    response = requests.delete(_api_url(f"/chat/sessions/{session_id}"), timeout=30)
    response.raise_for_status()
    body = response.json() or {}
    return int(body.get("deleted", 0) or 0)


def _delete_all_chat_sessions() -> int:
    response = requests.delete(_api_url("/chat/sessions"), timeout=30)
    response.raise_for_status()
    body = response.json() or {}
    return int(body.get("deleted", 0) or 0)


def _get_task_history(limit: int = 50) -> list[dict[str, Any]]:
    response = requests.get(_api_url("/tasks/history"), params={"limit": limit}, timeout=30)
    response.raise_for_status()
    return list(response.json() or [])


def _delete_task(task_id: str) -> int:
    response = requests.delete(_api_url(f"/tasks/{task_id}"), timeout=30)
    response.raise_for_status()
    body = response.json() or {}
    return int(body.get("deleted", 0) or 0)


def _post_chat(message: str, history: list[dict[str, str]], file_context: dict | None) -> dict[str, Any]:
    timeout_s = _resolve_chat_timeout_seconds()
    started = time.perf_counter()
    response = requests.post(
        _api_url("/chat"),
        json={
            "message": message,
            "session_id": st.session_state.get("chat_session_id"),
            "history": history,
            "file_context": file_context,
        },
        params=_chat_query_params(timeout_s),
        timeout=timeout_s,
    )
    response.raise_for_status()
    payload = response.json()
    payload["_client_elapsed_s"] = time.perf_counter() - started
    return payload


def _stream_chat(
    message: str,
    history: list[dict[str, str]],
    file_context: dict | None,
):
    timeout_s = _resolve_chat_timeout_seconds()
    started = time.perf_counter()
    response = requests.post(
        _api_url("/chat/stream"),
        json={
            "message": message,
            "session_id": st.session_state.get("chat_session_id"),
            "history": history,
            "file_context": file_context,
        },
        params=_chat_query_params(timeout_s),
        timeout=timeout_s,
        stream=True,
        headers={"Accept": "text/event-stream"},
    )
    response.raise_for_status()
    try:
        for raw_line in response.iter_lines(decode_unicode=True):
            if raw_line is None:
                continue
            line = raw_line.strip()
            if not line or not line.startswith("data:"):
                continue
            payload = line[5:].strip()
            if not payload:
                continue
            event = json.loads(payload)
            if isinstance(event, dict):
                event["_client_elapsed_s"] = time.perf_counter() - started
                yield event
    finally:
        response.close()


def _post_revise(task_id: str, instruction: str) -> dict[str, Any]:
    response = requests.post(
        _api_url(f"/tasks/{task_id}/revise"),
        json={"instruction": instruction},
        params=_codex_mock_query_params(),
        timeout=120,
    )
    response.raise_for_status()
    return response.json()
