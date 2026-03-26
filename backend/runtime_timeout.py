"""Per-request timeout selection helpers for Codex-backed routes."""

from __future__ import annotations

import math
from statistics import median

from backend.chat_store import recent_codex_exec_samples

DEFAULT_TIMEOUT_SECONDS = 180
MIN_TIMEOUT_SECONDS = 60
MAX_TIMEOUT_SECONDS = 1800


def _clamp_timeout(value: float) -> int:
    return max(MIN_TIMEOUT_SECONDS, min(MAX_TIMEOUT_SECONDS, int(math.ceil(value))))


def _estimate_from_samples(samples: list[float], *, route_kind: str) -> int | None:
    if not samples:
        return None
    ordered = sorted(float(x) for x in samples if x and x > 0)
    if not ordered:
        return None
    # Small-sample robust estimate: median and near-p95, then add a route-specific buffer.
    med = float(median(ordered))
    p95_index = min(len(ordered) - 1, max(0, math.ceil(len(ordered) * 0.95) - 1))
    p95 = float(ordered[p95_index])
    if route_kind == "chat":
        return _clamp_timeout(max(90.0, p95 * 2.0 + 20.0, med * 3.0 + 20.0))
    if route_kind in ("task_plan", "task_revise"):
        return _clamp_timeout(max(120.0, p95 * 2.5 + 30.0, med * 4.0 + 30.0))
    if route_kind == "task_postprocess":
        return _clamp_timeout(max(90.0, p95 * 2.0 + 20.0, med * 3.0 + 20.0))
    return _clamp_timeout(max(90.0, p95 * 2.0 + 20.0, med * 3.0 + 20.0))


def resolve_timeout_seconds(
    *,
    auto_timeout: bool,
    explicit_timeout_seconds: int | None,
    route_kind: str,
    model: str | None,
    reasoning_effort: str | None,
    env_default_timeout_seconds: int,
) -> int:
    """Resolve effective timeout.

    Priority:
    1. ``auto_timeout=True``: estimate from persisted Codex execution history.
    2. explicit timeout query/body value.
    3. environment default.
    """
    base_default = int(env_default_timeout_seconds or DEFAULT_TIMEOUT_SECONDS)
    if auto_timeout:
        samples = recent_codex_exec_samples(
            model=(model or "").strip() or None,
            reasoning_effort=(reasoning_effort or "").strip() or None,
            limit=40,
        )
        estimated = _estimate_from_samples(samples, route_kind=route_kind)
        if estimated is not None:
            return estimated
        return _clamp_timeout(base_default)
    if explicit_timeout_seconds is not None:
        return _clamp_timeout(int(explicit_timeout_seconds))
    return _clamp_timeout(base_default)
