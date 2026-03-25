# xyf-competition-mvp

> [English](README.md)

一个自然语言驱动的数据分析工作台。上传 CSV/Excel 后，可自由聊天，也可用 `/task` 走结构化流程：计划 → 审阅 → 执行 → 结果。

当前后端仅保留两种模式：
- `MockProvider`（离线、确定性）
- `LegacyCodexProvider`（真实 `codex exec`）

## 快速开始

### 1. 安装依赖

```bash
uv sync
```

### 2. 启动后端

```bash
# macOS / Linux
uv run uvicorn backend.main:app --reload

# Windows（强制 ProactorEventLoop，保证子进程管道可用）
uv run uvicorn backend.main:app --reload --loop backend.loop_factory:proactor_loop_factory
# 或：
uv run python scripts/run_uvicorn_windows.py --reload
```

后端：`http://127.0.0.1:8000`  
文档：`http://127.0.0.1:8000/docs`

### 3. 启动前端

```bash
uv run streamlit run app/streamlit_app.py
```

前端：`http://localhost:8501`

## 运行时选择

`backend.codex.factory.get_provider()` 按请求选择：
- `CODEX_MOCK=true`（默认）→ `MockProvider`
- `CODEX_MOCK=false` → `LegacyCodexProvider`（`codex exec`）

另外 `/chat`、`/tasks`、`/tasks/{id}/revise`、`/tasks/{id}/review` 支持按请求覆盖：
- `model`
- `reasoning_effort`（别名：`think_level`）

调试 chat 时，`/chat` 还支持：
- `include_prompt_debug=true`（返回实际渲染后的 prompt 与元信息）

Chat 持久化：
- SQLite 路径：`CHAT_SQLITE_PATH`（默认 `artifacts/chat_sessions.sqlite3`）
- 查询会话：`GET /chat/sessions`
- 查询会话明细：`GET /chat/sessions/{session_id}/turns`

## 关键环境变量

| 变量 | 默认值 | 说明 |
|---|---|---|
| `CODEX_MOCK` | `true` | 为真时走 mock。 |
| `CODEX_BINARY` | 自动 | `codex.exe` / `codex` 绝对路径。 |
| `CODEX_CLI_COMMAND` | 未设置 | 可选命令/路径覆盖。 |
| `XINFEI_CODEX_BINARY` | 未设置 | 可选信飞 Codex 绝对路径（用于回退解析）。 |
| `XINFEI_CODEX_HOME` | 未设置 | 可选信飞安装根目录，后端会解析 `<home>/bin/codex(.exe)`。 |
| `XINFEI_CODEX_PREFER` | `false` | 当 PATH 与 Xinfei 同时可用时，是否优先使用 Xinfei。 |
| `CODEX_MODEL` | 未设置 | 可选模型覆盖（如 `gpt-5.4-mini`、`gpt-5.4-nano`）。 |
| `CODEX_REASONING_EFFORT` | 未设置 | 可选推理强度覆盖（`low`/`medium`/`high`）。 |
| `CODEX_THINK_LEVEL` | 未设置 | `CODEX_REASONING_EFFORT` 的别名。 |
| `CODEX_TIMEOUT_SECONDS` | `180` | `codex exec` 超时秒数。 |
| `CODEX_ASYNC_SUBPROCESS` | `true` | 使用 asyncio 子进程路径调用 Codex（可输出更细粒度时间拆解）。 |
| `CODEX_DISABLE_MCP` | `true` | 是否在后端 `codex exec` 调用中禁用 MCP 启动（可降低每次调用开销）。 |
| `CODEX_MCP_DISABLE_SERVERS` | `notion,linear,figma,playwright` | 当前后端路径已弃用该项；`CODEX_DISABLE_MCP=true` 会直接注入 `mcp_servers={}`，以规避 CLI 的 transport 解析报错。 |
| `CODEX_RETRY_COUNT` | `1` | 计划/改计划解析失败时重试次数。 |
| `CODEX_AUTO_MOCK_THRESHOLD` | `3` | 真实模式连续失败达到阈值后自动降级 mock。 |
| `CODEX_HTTP_TRANSPORT_ONLY` | `true` | 注入 Codex 的 HTTP/SSE 配置覆盖。 |
| `CODEX_SSE_PROVIDER_ID` | `openai_sse` | 配置覆盖使用的 provider id。 |
| `CODEX_EXTRA_CONFIG` | 空 | 额外 `codex -c` 配置，分号分隔。 |
| `XINFEI_CODEX_ENFORCE_SSO` | `false` | 未登录信飞企业 SSO 时直接失败。 |
| `XINFEI_CODEX_AUTO_LOGIN` | `false` | 未登录时尝试交互式 `codex login --enterprise-sso`。 |
| `STREAMLIT_CHAT_TIMEOUT_SECONDS` | `300` | 关闭 mock 后 `/chat` 请求超时秒数。 |
| `API_BASE_URL` | `http://127.0.0.1:8000` | Streamlit 使用的后端地址。 |

## 技能

仓库技能位于 `.agents/skills/*/SKILL.md`。
- `GET /skills` 可查看已发现的技能元数据。
- 运行时依赖 Codex 原生 skills discovery/progressive disclosure。
- 规划/对话/改计划提示词仅传短显式 hint（例如 `$analysis-planner`），不再注入技能全文。

## 回归测试

```bash
uv run python tests/run_regression.py --mode mock
uv run python tests/run_regression.py --mode real
```

## 架构文档

详见 [docs/architecture.zh-CN.md](docs/architecture.zh-CN.md)。
