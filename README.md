# xyf-competition-mvp

> [简体中文](README.zh-CN.md)

A natural-language-driven data analytics workbench.

Upload a CSV/Excel file, describe what you want to analyze in plain language, review the generated analysis plan, and get back a chart, table, and summary — all without writing SQL or code.

---

## Quick Start

### 1. Install dependencies

```bash
uv sync
```

### 2. Start the backend (terminal 1)

```bash
uv run uvicorn backend.main:app --reload
```

Backend runs at `http://127.0.0.1:8000`. Interactive API docs at `http://127.0.0.1:8000/docs`.

### 3. Start the frontend (terminal 2)

```bash
uv run streamlit run app/streamlit_app.py
```

Frontend runs at `http://localhost:8501`.

### 4. One-click startup (PowerShell, opens two terminals)

```powershell
./scripts/start-dev.ps1 -CodexMock "true"
```

---

## Dev Branch Workflow

- `main`: stable integration branch / default branch for ongoing mainline work
- `master`: final presentation branch
- `dev/win`: Windows-native development branch
- `dev/wsl`: WSL/Linux development branch

Recommended flow:
- do day-to-day Windows work in `dev/win`
- do WSL/Linux-side work in `dev/wsl`
- merge validated work back into `main`
- keep `master` for polished final presentation/demo state

---

## Windows / WSL Development Notes

### On Windows (native)

Recommended when you want:
- PowerShell-first development
- easiest local app startup via `scripts/start-dev.ps1`
- testing Windows-specific CLI/runtime behavior

Basic flow:

```powershell
git checkout dev/win
uv sync
./scripts/start-dev.ps1 -CodexMock "true"
```

### On WSL

Recommended when you want:
- Linux-like CLI behavior
- easier shell scripting and backend iteration
- parity with deployment/runtime environments

Basic flow:

```bash
git checkout dev/wsl
uv sync
uv run uvicorn backend.main:app --reload
uv run streamlit run app/streamlit_app.py
```

### Branch guidance

- Prefer OS-specific environment/setup tweaks in `dev/win` or `dev/wsl`
- Avoid putting temporary machine-specific paths or secrets into shared branches
- After verification, merge clean cross-platform changes into `main`

---

## User Flow

```
Ask tab        →  upload file + type question
Plan tab       →  review the generated AnalysisPlan
Review tab     →  edit filters / metrics / dimensions, then submit
Results tab    →  chart + table + summary + follow-up suggestions
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CODEX_MOCK` | `true` | `true` = use MockAdapter (no Codex CLI needed); `false` = call real Codex CLI |
| `CODEX_CLI_COMMAND` | `codex` | Path or name of the Codex CLI binary |
| `CODEX_TIMEOUT_SECONDS` | `60` | Max seconds to wait for a Codex CLI response |
| `CODEX_RETRY_COUNT` | `1` | Number of retries on Codex parse failure |
| `CODEX_AUTO_MOCK_THRESHOLD` | `3` | Auto-degrade to mock after N consecutive Codex failures |
| `API_BASE_URL` | `http://127.0.0.1:8000` | Backend URL used by the Streamlit frontend |

---

## Running the Regression Suite

```bash
# Mock mode (no Codex CLI required)
uv run python tests/run_regression.py --mode mock

# Real mode (requires Codex CLI installed and configured)
uv run python tests/run_regression.py --mode real
```

Output is a JSON report with `passed`, `total`, `success_rate`, and per-case results.

---

## Project Layout

```
xyf-competition-mvp/
├── app/
│   └── streamlit_app.py        # Streamlit UI (4 tabs: Ask/Plan/Review/Results)
├── backend/
│   ├── main.py                 # FastAPI app entry point
│   ├── storage.py              # In-memory task store (resets on restart)
│   ├── observability.py        # Structured logging + snapshot utilities
│   ├── routers/
│   │   └── tasks.py            # All /tasks endpoints
│   ├── schemas/
│   │   ├── plan.py             # AnalysisPlan and related types
│   │   ├── task.py             # TaskRecord, TaskStatus
│   │   └── result.py           # ResultPayload, ChartPayload, TablePayload
│   ├── codex/
│   │   ├── adapter.py          # CodexAdapter: subprocess + JSON parsing
│   │   ├── mock.py             # MockAdapter: deterministic plans, no CLI needed
│   │   └── prompts.py          # Prompt templates for plan/summary/followups
│   ├── execution/
│   │   └── engine.py           # AnalysisPlan → pandas ops → ResultPayload
│   └── profiler/
│       └── schema_profiler.py  # File upload → column metadata dict
├── tests/
│   ├── fixtures/
│   │   ├── cases.json          # Regression test case definitions
│   │   ├── sales_data.csv
│   │   ├── employee_survey.csv
│   │   └── web_traffic.csv
│   └── run_regression.py       # Regression runner (mock + real modes)
├── artifacts/                  # Auto-created; task snapshots + event log
│   ├── events.log
│   └── tasks/<task_id>/        # Per-task JSON snapshots
├── scripts/
│   └── start-dev.ps1           # One-click dev startup (PowerShell)
├── docs/
│   ├── product-thoughts.md     # Product design notes
│   ├── architecture.md         # Developer guide (English)
│   └── architecture.zh-CN.md   # Developer guide (简体中文)
└── pyproject.toml
```

---

## For Developers

See [`docs/architecture.md`](docs/architecture.md) for:

- How each layer works and where to find it
- How to add a new analysis capability
- How to improve Codex prompt quality
- How to add new test fixtures
- What is deliberately not implemented yet (and why)
