"""Runtime mode and environment readiness endpoints."""

from __future__ import annotations

from fastapi import APIRouter

from backend.runtime_config import get_runtime_status

router = APIRouter(prefix="/runtime", tags=["runtime"])


@router.get("/status")
def runtime_status() -> dict[str, object]:
    return get_runtime_status()
