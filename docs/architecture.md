# Architecture & Developer Guide

> [简体中文](architecture.zh-CN.md)

This document explains how the system is structured, how the layers connect, and how to extend it. Start here if you are contributing to this repo for the first time.

---

## System Overview

```
User (browser)
    │
    ▼
Streamlit frontend  (app/streamlit_app.py)
    │  HTTP (requests)
    ▼
FastAPI backend  (backend/main.py)
    ├── Schema profiler  →  extracts column metadata from uploaded file
    ├── Codex adapter    →  calls Codex CLI (or MockAdapter) to produce a plan
    ├── Execution engine →  runs the plan against a pandas DataFrame
    └── Observability    →  writes structured logs and JSON snapshots to artifacts/
```

The user never sees raw data or code. Everything is mediated through an **AnalysisPlan** — a structured JSON object that describes what to compute.

---

## Request Lifecycle

### Step 1 — Create task (`POST /tasks`)

1. Frontend sends the uploaded file + natural language question.
2. `schema_profiler.profile_upload()` parses the file into a `pd.DataFrame` and extracts column names, dtypes, null counts, and sample values.
3. The schema profile is passed to the **Codex adapter** (`generate_plan`), which returns an `AnalysisPlan`.
4. The task is stored in memory (`backend/storage.py`) with status `planned`.
5. The DataFrame is also kept in memory keyed by `task_id`.

### Step 2 — Review plan (`GET /tasks/{id}`, `Plan` + `Review` tabs)

1. Frontend fetches the task and displays the plan as editable JSON.
2. The user can modify any field: add/remove filters, change aggregation, adjust chart type.
3. If `confidence < 0.6` or `ambiguities` is non-empty, the UI warns the user.

### Step 3 — Submit review and run (`POST /tasks/{id}/review`)

1. Frontend sends the (possibly edited) `final_plan`.
2. Backend calls `execution.engine.run_plan(df, final_plan)` which applies filters, groupby/aggregation, and builds chart + table payloads.
3. The adapter is called again for `generate_summary` and `generate_followups`.
4. Task status transitions: `reviewing` → `running` → `completed` (or `failed`).

### Step 4 — Fetch result (`GET /tasks/{id}/result`)

Returns `ResultPayload`: chart data, table rows, execution summary, LLM summary, and follow-up questions.

---

## Key Data Structures

All schemas live in `backend/schemas/`. They are Pydantic models — read them as the canonical contract between layers.

### `AnalysisPlan` (`schemas/plan.py`)

The central object. Produced by the Codex adapter, consumed by the execution engine.

```
AnalysisPlan
├── goal: str                         # human-readable description of intent
├── metrics: list[MetricSpec]         # what to compute (column + aggregation + alias)
├── dimensions: list[DimensionSpec]   # what to group by (column + role: time/category/geo)
├── filters: list[FilterSpec]         # row filters (column + operator + value)
├── output: OutputSpec                # chart_type (line/bar/histogram) + show_table
├── ambiguities: list[AmbiguitySpec]  # fields the LLM was uncertain about
└── confidence: float | None          # 0.0–1.0 self-reported plan quality
```

### `TaskRecord` (`schemas/task.py`)

Tracks the full lifecycle of one analysis request.

```
TaskRecord
├── task_id: str
├── status: TaskStatus   # created → planned → reviewing → running → completed/failed
├── input: TaskInput     # question, filename, row/column counts
├── plan: AnalysisPlan   # LLM-generated plan (before user review)
├── final_plan: AnalysisPlan | None   # plan after user edits
├── result: ResultPayload | None
└── error: TaskError | None
```

### `ResultPayload` (`schemas/result.py`)

```
ResultPayload
├── chart: ChartPayload     # chart_type, x/y column names, data rows
├── table: TablePayload     # columns list + rows as list[dict]
├── execution_summary: str  # human-readable description of what pandas did
├── summary: str | None     # LLM-generated narrative summary
└── follow_ups: list[str]   # 3 suggested follow-up questions
```

---

## The Codex Adapter Layer (`backend/codex/`)

This is the most important abstraction in the codebase. It isolates all LLM interaction so the rest of the system does not care whether it is talking to a real CLI or a mock.

### `adapter.py` — `CodexAdapter`

Calls Codex CLI as a subprocess:

```python
await asyncio.create_subprocess_exec("codex", "exec", prompt, ...)
```

Output is raw text. `_extract_json_payload()` tries two strategies:
1. Direct `json.loads()` on the full output.
2. Locate the first `{` and last `}` and parse that substring.

If both fail, `CodexAdapterError` is raised and the router falls back to `MockAdapter`.

Configured via environment variables: `CODEX_CLI_COMMAND`, `CODEX_TIMEOUT_SECONDS`, `CODEX_RETRY_COUNT`.

### `mock.py` — `MockAdapter`

Produces deterministic plans without any CLI call. Uses simple heuristics:
- Picks a numeric column as the metric.
- Picks a date/time column as the time dimension.
- Picks a category column (region, dept, product…) as the group-by dimension.
- Detects keywords like "华东" or "分布" to add filters or change chart type.

**Use this for all local development and CI.** Set `CODEX_MOCK=true` (the default).

### `prompts.py`

Three prompt builders:
- `build_plan_prompt` — instructs Codex to return a JSON `AnalysisPlan`.
- `build_summary_prompt` — instructs Codex to return a 2–4 sentence Chinese summary.
- `build_followups_prompt` — instructs Codex to return a JSON array of 3 follow-up questions.

**To improve plan quality, edit the prompts here.** The output schema in `build_plan_prompt` must stay in sync with `AnalysisPlan`.

### Auto-degrade

If Codex fails `CODEX_AUTO_MOCK_THRESHOLD` times in a row (default 3), the backend automatically sets `CODEX_MOCK=true` for the remainder of the process lifetime. This prevents cascading failures when the CLI is unavailable.

---

## The Execution Engine (`backend/execution/engine.py`)

`run_plan(df, plan) → ResultPayload`

Pure pandas. No LLM involved. Three stages:

1. **`_apply_filters`** — iterates `plan.filters`, applies pandas boolean masks. Skips any filter referencing a column not in the DataFrame (safe degradation).
2. **`_aggregate`** — if `plan.metrics` is non-empty, calls `df.groupby(dimensions).agg(metrics)`. If no dimensions, aggregates the whole DataFrame. Caps output at 500 rows.
3. **`_build_chart`** — picks x/y columns and formats `ChartPayload`. For histograms, uses `value_counts()`.

**To add a new aggregation type**, add it to `Aggregation` enum in `schemas/plan.py` — the engine uses `metric.aggregation.value` directly as the pandas agg string, so `"sum"`, `"mean"`, etc. work automatically.

**To add a new filter operator**, add it to `FilterOperator` enum and add a branch in `_apply_filters`.

---

## The Schema Profiler (`backend/profiler/schema_profiler.py`)

`profile_upload(file: UploadFile) → (pd.DataFrame, dict)`

Accepts `.csv`, `.xlsx`, `.xls`. Rejects empty files. If the file has more than 10,000 rows, it samples 10,000 rows randomly (reproducible with `random_state=42`).

The returned `dict` is the schema profile passed to the Codex adapter. It contains column names, dtypes, null counts, and up to 5 sample values per column. This gives the LLM enough context to map natural language column references to actual column names.

---

## Observability (`backend/observability.py`)

Every task produces two kinds of artifacts, written to `artifacts/` (auto-created):

| Artifact | Location | What it contains |
|----------|----------|-----------------|
| Event log | `artifacts/events.log` | One JSON line per event: `ts`, `task_id`, `stage`, `event_type`, `payload` |
| Snapshots | `artifacts/tasks/<task_id>/<name>.json` | Full JSON dump of input, schema_profile, plan, final_plan, result, errors, diffs |

**To debug a failed task**, find its `task_id` in the UI, then read `artifacts/tasks/<task_id>/`. The `review_diff.json` snapshot shows exactly what the user changed in the Review tab.

---

## Storage (`backend/storage.py`)

Three in-memory dicts, module-level:

| Dict | Key | Value |
|------|-----|-------|
| `TASKS` | `task_id` | `TaskRecord` |
| `TASK_DATAFRAMES` | `task_id` | `pd.DataFrame` |
| `TASK_SNAPSHOTS` | `task_id` | raw schema profile dict |

**All state is lost on server restart.** This is intentional for the MVP. To add persistence, replace these dicts with a database (SQLite is the natural next step — see "What's not implemented" below).

---

## API Endpoints

All routes are under `/tasks` (`backend/routers/tasks.py`).

| Method | Path | Purpose |
|--------|------|---------|
| `POST` | `/tasks` | Create task: upload file + question → returns plan |
| `GET` | `/tasks/{id}` | Get full `TaskRecord` |
| `POST` | `/tasks/{id}/review` | Submit final plan → runs execution → returns completed record |
| `GET` | `/tasks/{id}/result` | Get `ResultPayload` (or status if not ready) |
| `POST` | `/tasks/{id}/fail` | Dev utility: manually mark task as failed |
| `POST` | `/tasks/{id}/reset` | Recovery: reset stuck task back to `planned` |

Interactive docs: `http://127.0.0.1:8000/docs`

---

## Adding a New Feature — Checklist

### New filter operator

1. Add value to `FilterOperator` in `backend/schemas/plan.py`.
2. Add branch in `_apply_filters` in `backend/execution/engine.py`.
3. Update the output schema string in `build_plan_prompt` in `backend/codex/prompts.py`.
4. Add a regression case in `tests/fixtures/cases.json` + matching CSV.

### New chart type

1. Add value to `ChartType` in `backend/schemas/plan.py`.
2. Add rendering branch in `_draw_chart` in `app/streamlit_app.py`.
3. Add chart-building logic in `_build_chart` in `backend/execution/engine.py`.

### New LLM capability (e.g. anomaly detection)

1. Add a prompt builder in `backend/codex/prompts.py`.
2. Add a method to `CodexAdapter` and `MockAdapter` (keep both in sync).
3. Call it from the appropriate router endpoint.
4. Add a new field to the relevant schema if the output needs to be stored.

### Improve plan quality

Edit `build_plan_prompt` in `backend/codex/prompts.py`. The most impactful changes:
- Add more example column names to help the model map natural language to schema columns.
- Add few-shot examples of good plans.
- Tighten the output schema description to reduce hallucinated field names.

---

## Running Tests

```bash
# Regression suite (mock mode — no Codex CLI needed)
uv run python tests/run_regression.py --mode mock

# Regression suite (real mode — requires Codex CLI)
uv run python tests/run_regression.py --mode real
```

Test fixtures are in `tests/fixtures/`. Each entry in `cases.json` specifies:
- `name` — test case identifier
- `file` — CSV filename relative to `fixtures/`
- `question` — natural language question
- `expected_chart_type` — `"line"`, `"bar"`, or `"histogram"`
- `expected_metric_column` — expected output column name (informational)

To add a new test case: drop a CSV into `tests/fixtures/` and add an entry to `cases.json`.

---

## What Is Deliberately Not Implemented (MVP Boundaries)

These are known gaps, not bugs. They are deferred to keep the MVP scope manageable.

| Feature | Status | Notes |
|---------|--------|-------|
| Persistent storage | Not implemented | In-memory only; restart loses all tasks |
| Authentication | Not implemented | No user accounts or API keys |
| Multi-turn conversation / memory | Not implemented | Each task is independent |
| Skill library | Not implemented | No reusable analysis templates |
| ACP / agent protocol integration | Not implemented | Codex CLI is called directly |
| Streaming responses | Not implemented | All results returned synchronously |
| Excel output | Not implemented | Table download is CSV only |
| Multi-file joins | Not implemented | One file per task |
| Column-level access control | Not implemented | All columns visible to LLM |

---

## Dependency Notes

| Package | Purpose |
|---------|---------|
| `fastapi` + `uvicorn` | Backend API server |
| `streamlit` | Frontend UI |
| `pandas` + `numpy` | Data manipulation in execution engine |
| `pydantic` | Schema validation for all data contracts |
| `python-multipart` | Required by FastAPI for file uploads |
| `requests` | Used by Streamlit to call the backend |
| `uv` | Package manager and virtual environment |

Codex CLI is **not** a Python package. It must be installed separately and available on `PATH` (or pointed to via `CODEX_CLI_COMMAND`). When `CODEX_MOCK=true`, it is never called.
