"""Extract JSON payloads from noisy agent stdout (fences, extra text)."""

from __future__ import annotations

import json

from backend.acp.errors import CodexAdapterError


def extract_json_array_payload(raw: str) -> list:
    """Parse a JSON array from agent stdout."""
    raw = raw.strip()
    try:
        payload = json.loads(raw)
        if isinstance(payload, list):
            return payload
    except json.JSONDecodeError:
        pass

    start = raw.find("[")
    end = raw.rfind("]")
    if start == -1 or end == -1 or end <= start:
        raise CodexAdapterError("Cannot locate JSON array in agent output.")
    candidate = raw[start : end + 1]
    try:
        payload = json.loads(candidate)
    except json.JSONDecodeError as exc:
        raise CodexAdapterError(
            f"Invalid JSON array extracted from agent output: {exc}"
        ) from exc
    if not isinstance(payload, list):
        raise CodexAdapterError("Extracted JSON is not an array.")
    return payload


def extract_json_payload(raw: str) -> dict:
    """Parse a JSON object from agent stdout."""
    raw = raw.strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    start = raw.find("{")
    end = raw.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise CodexAdapterError("Cannot locate JSON object in agent output.")
    candidate = raw[start : end + 1]
    try:
        return json.loads(candidate)
    except json.JSONDecodeError as exc:
        raise CodexAdapterError(
            f"Invalid JSON extracted from agent output: {exc}"
        ) from exc
