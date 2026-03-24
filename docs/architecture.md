# Architecture & Developer Guide

> [简体中文](architecture.zh-CN.md)

This document describes the current runtime. The only real-model path is one-shot `codex exec`.

## Overview

```text
Streamlit UI (app/streamlit_app.py)
  -> FastAPI routers (backend/routers/*)
  -> Provider selection (backend/codex/factory.py)
       - MockProvider
       - LegacyCodexProvider (codex exec)
  -> Execution engine (backend/execution/engine.py)
  -> Observability + in-memory storage
```

## Runtime Selection

- `CODEX_MOCK=true` (default): `MockProvider`
- `CODEX_MOCK=false`: `LegacyCodexProvider`

Provider entrypoint:
- `backend.codex.factory.get_provider()`

Compatibility hook:
- `backend.codex.factory.shutdown_providers()` (currently no-op)

## Codex Runtime Modules

- `backend/codex/legacy.py`: one-shot subprocess calls via `codex exec`
- `backend/codex/mock.py`: deterministic offline fallback
- `backend/codex/xinfei_sso.py`: Codex binary resolution + Xinfei enterprise SSO checks
- `backend/codex/json_util.py`: robust JSON extraction from model output
- `backend/codex/errors.py`: `CodexAdapterError`
- `backend/codex/adapter.py`: compatibility re-export for older scripts/tests

## Skills

- Skill registry scans `.agents/skills/*/SKILL.md`
- Skill text is injected into prompts for planner/chat/reviser
- Metadata endpoint: `GET /skills`

## Request Lifecycles

- `/chat`: free-form text reply
- `/tasks`: create plan from file + question
- `/tasks/{id}/revise`: revise plan by natural language feedback
- `/tasks/{id}/review`: execute approved plan and generate summary/follow-ups
- `/data/profile`: schema profiling without creating task

## Local Verification

```bash
uv sync
uv run uvicorn backend.main:app --reload
uv run streamlit run app/streamlit_app.py
uv run python tests/run_regression.py --mode mock
```

For real mode:

```bash
uv run python tests/run_regression.py --mode real
```
