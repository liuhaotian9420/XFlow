"""Lightweight data utilities (schema preview without creating a task)."""

from __future__ import annotations

from fastapi import APIRouter, File, UploadFile

from backend.profiler.schema_profiler import profile_upload

router = APIRouter(prefix="/data", tags=["data"])


@router.post("/profile")
async def profile_data_file(file: UploadFile = File(...)) -> dict:
    """Return schema profile for an upload without starting a task (for chat context)."""
    _, schema_profile = profile_upload(file)
    return schema_profile
