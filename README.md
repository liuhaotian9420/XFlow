# xyf-competition-mvp

> [简体中文](README.zh-CN.md)

A natural-language-driven data analytics workbench. Upload CSV/Excel, chat freely, or run a structured `/task` flow: plan -> review -> execute -> results.

The backend supports:
- `MockProvider` (offline deterministic behavior)
- `LegacyCodexProvider` (real one-shot `codex exec`)

## Quick Start

### Demo mode

Use this when you want the app to run on any machine without a Codex CLI or ODPS account.

### 1. Install dependencies

```bash
uv sync
```

### 2. One-click start on Windows

```bash
.\scripts\start-demo.ps1
```

The launcher checks `python` and `uv`, runs `uv sync`, then opens backend and frontend in separate terminals.

Frontend: `http://localhost:8501`
Backend: `http://127.0.0.1:8000`
Swagger: `http://127.0.0.1:8000/docs`

### Real mode setup

Use your own Codex executable and your own ODPS account. Copy `.env.example` into a local `.env` or export the same variables in your shell.

Minimum real-mode variables:

```bash
APP_MODE=real
CODEX_CLI_COMMAND=/path/to/codex
ODPS_ACCESS_KEY_ID=...
ODPS_ACCESS_KEY_SECRET=...
ODPS_PROJECT=...
ODPS_ENDPOINT=...
```

Validate the environment before starting services:

```bash
uv run python scripts/preflight.py --mode real
```

The backend exposes `GET /runtime/status`, and the Streamlit sidebar shows whether Codex and ODPS are ready.

### One-click real start on Windows

```bash
.\scripts\start-real.ps1
```

This launcher requires `.env`, runs `uv sync`, runs real-mode preflight, then starts backend and frontend only if the runtime is ready.

### Manual backend/frontend commands

Use these only when you need manual control instead of the launchers.

```bash
# macOS / Linux backend
APP_MODE=mock uv run uvicorn backend.main:app --reload

# Windows backend
uv run python scripts/run_uvicorn_windows.py --reload

# Frontend
uv run streamlit run app/streamlit_app.py
```

## Runtime Selection

`backend.codex.factory.get_provider()` chooses provider per request:
- `APP_MODE=mock` (or `CODEX_MOCK=true`) -> `MockProvider`
- `APP_MODE=real` (or `CODEX_MOCK=false`) -> `LegacyCodexProvider` (`codex exec`)

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
| `APP_MODE` | auto | Preferred top-level runtime selector: `mock` or `real`. |
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
| `CODEX_MCP_DISABLE_SERVERS` | `notion,linear,figma,playwright` | Deprecated in current backend path; `CODEX_DISABLE_MCP=true` now forces `mcp_servers={}`. |
| `CODEX_RETRY_COUNT` | `1` | Retry count for plan/revise parse failures. |
| `CODEX_AUTO_MOCK_THRESHOLD` | `3` | Consecutive real-mode failures before process auto-degrades to mock. |
| `CODEX_HTTP_TRANSPORT_ONLY` | `true` | Inject Codex config overrides for HTTP/SSE provider. |
| `CODEX_SSE_PROVIDER_ID` | `openai_sse` | Provider id used in config overrides. |
| `CODEX_EXTRA_CONFIG` | empty | Extra `codex -c` values, semicolon-separated. |
| `XINFEI_CODEX_ENFORCE_SSO` | `false` | Fail if Xinfei enterprise SSO is missing. |
| `XINFEI_CODEX_AUTO_LOGIN` | `false` | Attempt interactive `codex login --enterprise-sso` when missing SSO. |
| `STREAMLIT_CHAT_TIMEOUT_SECONDS` | `300` | Streamlit timeout for `/chat` when mock is off. |
| `API_BASE_URL` | `http://127.0.0.1:8000` | Backend base URL used by Streamlit. |
| `ODPS_ACCESS_KEY_ID` | unset | Preferred ODPS access key id for real data exports. |
| `ODPS_ACCESS_KEY_SECRET` | unset | Preferred ODPS access key secret for real data exports. |
| `ODPS_PROJECT` | unset | Preferred ODPS project for real data exports. |
| `ODPS_ENDPOINT` | unset | Preferred ODPS endpoint for real data exports. |

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
