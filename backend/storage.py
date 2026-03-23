"""In-memory storage for task records and dataframes."""

from __future__ import annotations

from typing import Any

import pandas as pd

from backend.schemas.task import TaskRecord


TASKS: dict[str, TaskRecord] = {}
TASK_DATAFRAMES: dict[str, pd.DataFrame] = {}
TASK_SNAPSHOTS: dict[str, dict[str, Any]] = {}
CODEX_FAILURE_COUNT: int = 0

