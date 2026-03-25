# xyf-competition-mvp

> [简体中文](README.zh-CN.md)

A natural-language-driven data analytics workbench. Upload CSV/Excel, chat freely, or run a structured `/task` flow: plan → review → execute → results.

The backend supports:
- `MockProvider` (offline deterministic behavior)
- `LegacyCodexProvider` (real one-shot `codex exec`)

## Quick Start

### 1. Install dependencies

```bash
uv sync
```

### 2. Start backend

```bash
# macOS / Linux
uv run uvicorn backend.main:app --reload

# Windows (forces ProactorEventLoop so subprocess pipes work)
uv run uvicorn backend.main:app --reload --loop backend.loop_factory:proactor_loop_factory
# or:
uv run python scripts/run_uvicorn_windows.py --reload
```

Backend: `http://127.0.0.1:8000`  
Swagger: `http://127.0.0.1:8000/docs`

### 3. Start frontend

```bash
uv run streamlit run app/streamlit_app.py
```

Frontend: `http://localhost:8501`

## Runtime Selection

`backend.codex.factory.get_provider()` chooses provider per request:
- `CODEX_MOCK=true` (default) → `MockProvider`
- `CODEX_MOCK=false` → `LegacyCodexProvider` (`codex exec`)

Per-request overrides are also supported on `/chat`, `/tasks`, `/tasks/{id}/revise`, `/tasks/{id}/review` via query params:
- `model`
- `reasoning_effort` (alias: `think_level`)

For chat debugging, `/chat` also supports:
- `include_prompt_debug=true` (returns rendered prompt text and prompt metadata)

Chat persistence:
- SQLite file path: `CHAT_SQLITE_PATH` (default: `artifacts/chat_sessions.sqlite3`)
- Query sessions: `GET /chat/sessions`
- Query turns: `GET /chat/sessions/{session_id}/turns`

## Key Environment Variables

| Variable | Default | Description |
|---|---|---|
| `CODEX_MOCK` | `true` | Use mock mode when true. |
| `CODEX_BINARY` | auto | Absolute path to `codex.exe` / `codex`. |
| `CODEX_CLI_COMMAND` | unset | Optional command/path override for Codex CLI resolution. |
| `XINFEI_CODEX_BINARY` | unset | Optional absolute path to Xinfei Codex binary (used for fallback resolution). |
| `XINFEI_CODEX_HOME` | unset | Optional Xinfei install root; backend resolves `<home>/bin/codex(.exe)`. |
| `XINFEI_CODEX_PREFER` | `false` | Prefer Xinfei binary over `PATH` `codex` when both are available. |
| `CODEX_MODEL` | unset | Optional model override for `codex exec` (e.g. `gpt-5.4-mini`, `gpt-5.4-nano`). |
| `CODEX_REASONING_EFFORT` | unset | Optional reasoning effort override (`low`/`medium`/`high`). |
| `CODEX_THINK_LEVEL` | unset | Alias of `CODEX_REASONING_EFFORT`. |
| `CODEX_TIMEOUT_SECONDS` | `180` | Timeout for `codex exec`. |
| `CODEX_ASYNC_SUBPROCESS` | `true` | Use asyncio subprocess path for Codex calls (enables detailed phase timings). |
| `CODEX_DISABLE_MCP` | `true` | Disable MCP server startup for backend `codex exec` calls (reduces per-call overhead). |
| `CODEX_MCP_DISABLE_SERVERS` | `notion,linear,figma,playwright` | Deprecated in current backend path; `CODEX_DISABLE_MCP=true` now forces `mcp_servers={}` to avoid CLI transport-parse failures. |
| `CODEX_RETRY_COUNT` | `1` | Retry count for plan/revise parse failures. |
| `CODEX_AUTO_MOCK_THRESHOLD` | `3` | Consecutive real-mode failures before process auto-degrades to mock. |
| `CODEX_HTTP_TRANSPORT_ONLY` | `true` | Inject Codex config overrides for HTTP/SSE provider. |
| `CODEX_SSE_PROVIDER_ID` | `openai_sse` | Provider id used in config overrides. |
| `CODEX_EXTRA_CONFIG` | empty | Extra `codex -c` values, semicolon-separated. |
| `XINFEI_CODEX_ENFORCE_SSO` | `false` | Fail if Xinfei enterprise SSO is missing. |
| `XINFEI_CODEX_AUTO_LOGIN` | `false` | Attempt interactive `codex login --enterprise-sso` when missing SSO. |
| `STREAMLIT_CHAT_TIMEOUT_SECONDS` | `300` | Streamlit timeout for `/chat` when mock is off. |
| `API_BASE_URL` | `http://127.0.0.1:8000` | Backend base URL used by Streamlit. |

## Skills

Repository skills live under `.agents/skills/*/SKILL.md`.
- `GET /skills` lists discovered skill metadata.
- Runtime uses Codex native skill discovery/progressive disclosure.
- Backend prompts only pass short skill hints (for example, `$analysis-planner`) and keep templates minimal.

## Regression

```bash
uv run python tests/run_regression.py --mode mock
uv run python tests/run_regression.py --mode real
```

## Architecture

See [docs/architecture.md](docs/architecture.md) for layering, request lifecycle, and extension points.
