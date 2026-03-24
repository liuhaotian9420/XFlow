# xyf-competition-mvp

> [简体中文](README.zh-CN.md)

A natural-language-driven data analytics workbench. Upload a CSV or Excel file, talk to an assistant in **chat** or **task** mode, review structured analysis plans when you need them, and get charts, tables, and summaries — without writing SQL or code.

The backend can drive LLMs through **mock** (offline), **ACP** (long-lived Agent Client Protocol sessions, e.g. Codex via `codex-acp`), or **legacy** one-shot `codex exec`, selected automatically from environment and installed tools.

---

## Quick Start

### 1. Install dependencies

```bash
uv sync
```

This installs Python dependencies including **`agent-client-protocol`** (import name `acp`). The ACP SDK is loaded **lazily** when you first use ACP mode, so mock-only development still starts cleanly after `uv sync`.

### 2. Start the backend (terminal 1)

```bash
# macOS / Linux
uv run uvicorn backend.main:app --reload

# Windows (required for ACP — forces ProactorEventLoop so subprocess pipes work)
uv run uvicorn backend.main:app --reload --loop backend.loop_factory.proactor_loop_factory
# … or equivalently:
uv run python scripts/run_uvicorn_windows.py --reload
```

> **Why?** uvicorn's default loop factory returns `SelectorEventLoop` on Windows when `--reload` is active, and `SelectorEventLoop` does not implement `create_subprocess_exec`. The custom loop factory in `backend/loop_factory.py` always returns `ProactorEventLoop`.

Backend: `http://127.0.0.1:8000` · Swagger: `http://127.0.0.1:8000/docs`

### 3. Start the frontend (terminal 2)

```bash
uv run streamlit run app/streamlit_app.py
```

Frontend: `http://localhost:8501`

### 4. One-click startup (PowerShell)

```powershell
./scripts/start-dev.ps1 -CodexMock "true"
```

---

## User Flow (Streamlit)

### Chat vs task mode

| Mode | How to enter | What happens |
|------|----------------|---------------|
| **Chat** | Default after load | Free-form Q&A about the file schema and analysis ideas. Plain text replies. |
| **Task** | Type **`/task`** followed by your question | Creates a structured pipeline: **plan → review → execute → results**. |
| **Plan revision** | While in task mode with a **pending** plan, send a normal message | Backend calls `POST /tasks/{id}/revise` to rewrite the plan from your feedback. |
| **After results** | Completion card | **Mark complete** returns to chat mode; **Not done — replan** starts a new task with your note. |

Typical session:

```
Sidebar     →  upload CSV/Excel (schema is cached for chat context)
Chat        →  ask questions freely, or `/task …` for a full analysis run
Plan        →  review metrics, filters, chart type; edit JSON if needed; confirm
Results     →  chart + table + summary + follow-up chips (can spawn another `/task`)
```

---

## Agent backends (how the LLM is called)

`backend.acp.factory.get_provider()` picks one implementation per request:

| Provider | When | Notes |
|----------|------|--------|
| **MockProvider** | `CODEX_MOCK=true` (default) | No CLI; deterministic plans and canned chat. |
| **AcpProvider** | `CODEX_MOCK=false`, ACP launcher on `PATH`, `ACP_BACKEND` not forced to legacy | Long-lived stdio JSON-RPC to `codex-acp` (or `npx -y @zed-industries/codex-acp` if `codex-acp` is missing). The child `codex` used by the adapter is **`resolve_codex_executable()`** (Xinfei `codex.exe` auto-detected on Windows when unset). |
| **LegacyCodexProvider** | `CODEX_MOCK=false` but no ACP launcher or `ACP_BACKEND=legacy` | One-shot `codex exec` per call via the same resolved Codex binary. |

Skills under `.agents/skills/` are discovered by Codex when **ACP session `cwd`** points at the repo (see `ACP_SESSION_CWD`). Non-Codex agents get skill bodies **injected** into prompts unless `ACP_AGENT_NATIVE_SKILLS` disables injection.

Full detail: [`docs/architecture.md`](docs/architecture.md).

---

## Xinfei enterprise Codex (Windows)

If **Xinfei Codex** is installed under `%LOCALAPPDATA%\Programs\XinfeiCodex\bin\codex.exe`, the backend **prefers that binary** over `codex` on `PATH` when `CODEX_BINARY` and `CODEX_CLI_COMMAND` are unset. This avoids invoking `xinfei-codex.cmd` / `.ps1` from subprocesses (PowerShell `Stop` on `login status` stderr).

- **ACP:** `codex-acp` (or `npx`) spawns `codex` from `PATH`; we prepend the resolved `codex.exe` directory to the agent subprocess `PATH` so the enterprise binary wins.
- **SSO:** On first real (non-mock) request, if the resolved binary is under `XinfeiCodex`, we check `codex login status` for `Logged in using Enterprise SSO`. If missing, we **log a warning** unless `XINFEI_CODEX_ENFORCE_SSO=true` (fail fast) or `XINFEI_CODEX_AUTO_LOGIN=true` (run `codex login --enterprise-sso`).

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CODEX_MOCK` | `true` | `true` = MockProvider; `false` = real LLM path (ACP if available, else legacy `codex exec`). |
| `CODEX_BINARY` | *(auto)* | Absolute path to `codex.exe` / `codex`. Overrides auto-detection and is used for legacy `exec` and for ACP `PATH` prepending. |
| `CODEX_CLI_COMMAND` | *(unset → auto)* | If set: command or path passed to legacy `exec` resolution. Shell wrappers (`.cmd`/`.bat`/`.ps1`) are replaced by Xinfei's inner `codex.exe` when detected. |
| `CODEX_TIMEOUT_SECONDS` | `60` | Legacy default; ACP manager may use the same env where applicable. |
| `CODEX_RETRY_COUNT` | `1` | Retries on plan / revise parse failures. |
| `CODEX_AUTO_MOCK_THRESHOLD` | `3` | Consecutive failures → auto mock for process lifetime. |
| `CODEX_HTTP_TRANSPORT_ONLY` | `true` | Legacy Codex: prefer HTTP/SSE provider vs WebSocket (see architecture doc). |
| `CODEX_SSE_PROVIDER_ID` | `openai_sse` | Synthetic provider id for `-c` overrides. |
| `CODEX_EXTRA_CONFIG` | *(empty)* | Extra `codex -c` pairs, semicolon-separated. |
| `ACP_AGENT_COMMAND` | *(auto)* | If unset: use `codex-acp` when on `PATH`, else `npx -y @zed-industries/codex-acp`. Set explicitly to override (e.g. a full path to `codex-acp.exe`). |
| `ACP_AGENT_ARGS` | *(empty)* | Extra args (shell-tokenized). |
| `ACP_AGENT_PATH_PREPEND` | `true` | If not `false`/`0`/`off`, prepend the parent directory of `resolve_codex_executable()` to the ACP agent `PATH` (so `codex-acp` picks Xinfei Codex). |
| `ACP_AGENT_INHERIT_FULL_ENV` | `true` | If not `false`/`0`/`off`, the ACP subprocess receives the **full** backend `os.environ` (same idea as your terminal), not only the SDK’s trimmed set — fixes many `502` / auth / `npx` issues. |
| `ACP_AGENT_STDERR` | `inherit` | `inherit` (default): child stderr goes to the API process (see logs next to uvicorn). `null`/`devnull`: discard. `pipe`: SDK default — if nothing reads stderr and the agent is verbose, the pipe can **fill and block** (UI stuck on “Thinking…”). |
| `STREAMLIT_CHAT_TIMEOUT_SECONDS` | `300` | Streamlit → `/chat` timeout when mock is off (seconds). |
| `ACP_BACKEND` | *(auto)* | `legacy` / `exec` / `codex-exec` forces legacy despite ACP binary. |
| `XINFEI_CODEX_ENFORCE_SSO` | `false` | If truthy and Xinfei binary is not in enterprise SSO state, raise at startup of first real request. |
| `XINFEI_CODEX_AUTO_LOGIN` | `false` | If truthy and SSO missing, run `codex login --enterprise-sso` (interactive / browser). |
| `ACP_CHAT_SESSION_KEY` | `xyf-global-chat` | Logical session key for `POST /chat` continuity. |
| `ACP_SESSION_CWD` | *(repo root)* | `session/new` working directory so Codex loads `.agents/skills` and `AGENTS.md`. |
| `ACP_AGENT_NATIVE_SKILLS` | *(auto)* | `true`/`false` overrides prompt injection; unset → skip injection if command contains `codex`. |
| `API_BASE_URL` | `http://127.0.0.1:8000` | Streamlit → backend base URL. |

---

## Skills (`.agents/skills`)

Repository skills use the **Codex / agentskills** layout: each folder contains `SKILL.md` with YAML frontmatter (`name`, `description`) plus instructions.

- Shipped examples: `analysis-planner`, `data-chat`, `plan-reviser` (aligned with prompt builders).
- **List metadata:** `GET http://127.0.0.1:8000/skills`

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|----------------|-----|
| `ModuleNotFoundError: No module named 'acp'` | Dependencies not installed | Run `uv sync` from repo root; use `uv run …` so the project venv is active. |
| `ImportError: ACP mode requires 'agent-client-protocol'` | Mock off but SDK missing | `uv sync` or `pip install 'agent-client-protocol>=0.8.1'`. |
| Backend starts but ACP calls fail | Agent binary missing | Install `codex-acp` (`npm i -g @zed-industries/codex-acp`) or ensure `npx` is on `PATH` (default falls back to `npx -y @zed-industries/codex-acp`), or set `ACP_BACKEND=legacy`. |
| Legacy / ACP fails right after Xinfei install | Wrapper + SSO stderr | Set `CODEX_BINARY` to `%LOCALAPPDATA%\Programs\XinfeiCodex\bin\codex.exe` or leave env unset for auto-detect; do not point `CODEX_CLI_COMMAND` at `xinfei-codex.cmd` unless you accept wrapper behavior. |
| ACP fails with `NotImplementedError` in `create_subprocess_exec` (Windows) | uvicorn `--reload` forces `SelectorEventLoop` which lacks subprocess pipes. | Use `--loop backend.loop_factory.proactor_loop_factory` on the uvicorn command, or run `uv run python scripts/run_uvicorn_windows.py --reload`, or set **`ACP_BACKEND=legacy`**. |
| Streamlit stuck on “Thinking…” (real mode) | Long model run, or **stderr pipe deadlock** (`ACP_AGENT_STDERR=pipe`), or waiting on first `npx` download | Run uvicorn with **`--log-level debug`** and watch for `CHAT begin`, `ACP spawning agent`, `ACP prompt start/end`. Keep **`ACP_AGENT_STDERR=inherit`** (default). Increase `CODEX_TIMEOUT_SECONDS` / `STREAMLIT_CHAT_TIMEOUT_SECONDS` if needed. |
| Codex ignores skills | Wrong `cwd` | Set `ACP_SESSION_CWD` to the repo root (absolute path). |

---

## Dev Branch Workflow

- `main` — integration default
- `master` — presentation polish
- `dev/win` — Windows-native
- `dev/wsl` — WSL/Linux

Merge validated work into `main`; keep `master` for demos.

---

## Windows / WSL

**Windows (native):** `git checkout dev/win` → `uv sync` → `./scripts/start-dev.ps1 -CodexMock "true"`

**WSL:** `git checkout dev/wsl` → `uv sync` → `uv run uvicorn …` and `uv run streamlit …`

Avoid committing machine-specific paths or secrets.

---

## Running the Regression Suite

```bash
uv run python tests/run_regression.py --mode mock
uv run python tests/run_regression.py --mode real   # needs Codex CLI + config
```

Output: JSON with `passed`, `total`, `success_rate`, per-case results.

---

## Project Layout

```
xyf-competition-mvp/
├── .agents/
│   └── skills/                 # SKILL.md packs (Codex discovery + SkillRegistry)
├── app/
│   └── streamlit_app.py        # Chat/task UI, upload, plan review, results
├── backend/
│   ├── main.py                 # FastAPI + lifespan → shutdown_providers()
│   ├── storage.py
│   ├── observability.py
│   ├── acp/                    # ACP client, providers, factory, legacy exec, Xinfei/CLI resolution
│   ├── skills/                 # SkillRegistry, native-skill detection, prompt injection
│   ├── routers/
│   │   ├── tasks.py            # /tasks/*
│   │   ├── chat.py             # POST /chat
│   │   ├── data.py             # POST /data/profile
│   │   └── skills.py           # GET /skills
│   ├── schemas/
│   ├── codex/
│   │   ├── prompts.py          # Plan / summary / followups / chat / revise prompts
│   │   ├── adapter.py          # Shim → LegacyCodexProvider
│   │   └── mock.py             # Shim → MockProvider
│   ├── execution/
│   └── profiler/
├── tests/
├── artifacts/                  # Runtime logs + per-task JSON snapshots
├── scripts/
├── docs/
│   ├── architecture.md
│   ├── architecture.zh-CN.md
│   └── product-thoughts.md
└── pyproject.toml
```

---

## For Developers

See [`docs/architecture.md`](docs/architecture.md) for:

- End-to-end layer walkthrough (regression → API → Streamlit)
- **ACP vs legacy vs mock** wiring
- **Chat, revise, and profiling** request paths
- Skills and prompt injection rules
- How to extend filters, charts, and LLM surfaces
- MVP boundaries and dependency table
