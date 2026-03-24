# xyf-competition-mvp

> [English](README.md)

面向自然语言的数据分析工作台。上传 CSV 或 Excel，在 **对话（Chat）** 与 **任务（Task）** 两种模式下与助手协作：需要结构化跑数时用 `/task` 触发「计划 → 审阅 → 执行 → 结果」，平时则可自由问答 schema 与分析思路。

后端通过 **Mock**（离线）、**ACP**（Agent Client Protocol 长连接会话，例如 `codex-acp`）或 **Legacy**（每次一次 `codex exec`）调用大模型，由环境与可执行文件自动择优。

---

## 快速开始

### 1. 安装依赖

```bash
uv sync
```

会安装 **`agent-client-protocol`**（Python 里 import 名为 `acp`）。ACP 相关代码采用**延迟导入**，仅在真正走 ACP 路径时加载；Mock 开发也请先执行 `uv sync`，保证依赖完整。

### 2. 启动后端（终端 1）

```bash
# macOS / Linux
uv run uvicorn backend.main:app --reload

# Windows（ACP 必需 — 强制用 ProactorEventLoop，子进程管道可用）
uv run uvicorn backend.main:app --reload --loop backend.loop_factory.proactor_loop_factory
# 或等效：
uv run python scripts/run_uvicorn_windows.py --reload
```

> **Why?** uvicorn 在 `--reload` 时默认选 `SelectorEventLoop`（Windows），它不实现 `create_subprocess_exec`。`backend/loop_factory.py` 里的自定义工厂始终返回 `ProactorEventLoop`。

后端：`http://127.0.0.1:8000` · API 文档：`http://127.0.0.1:8000/docs`

### 3. 启动前端（终端 2）

```bash
uv run streamlit run app/streamlit_app.py
```

前端：`http://localhost:8501`

### 4. 一键启动（PowerShell）

```powershell
./scripts/start-dev.ps1 -CodexMock "true"
```

---

## 使用流程（Streamlit）

### 对话模式 vs 任务模式

| 模式 | 进入方式 | 行为 |
|------|----------|------|
| **对话 Chat** | 默认 | 围绕已上传文件的 schema、分析思路等自由问答，回复为纯文本。 |
| **任务 Task** | 输入 **`/task`** + 你的分析问题 | 走结构化链路：**生成计划 → 人工审阅 → 执行 → 结果**。 |
| **改计划** | 任务模式下、计划**待确认**时，直接发一条普通消息 | 调用 `POST /tasks/{id}/revise`，按你的说明重写计划。 |
| **结果之后** | 完成卡片 | **标记完成** 回到对话模式；**未完成 — 重新规划** 带着备注开新任务。 |

典型路径：

```
侧边栏  →  上传 CSV/Excel（schema 会缓存，供对话上下文使用）
对话区  →  自由提问，或输入 `/task …` 跑完整分析
审阅    →  看指标/筛选/图表类型；可在折叠区改 JSON 后确认执行
结果    →  图表 + 表格 + 摘要 + 追问按钮（可再触发新的 `/task`）
```

---

## 智能体后端（LLM 如何被调用）

`backend.acp.factory.get_provider()` 按请求选择实现：

| 提供者 | 条件 | 说明 |
|--------|------|------|
| **MockProvider** | `CODEX_MOCK=true`（默认） | 不调用 CLI；确定性计划与固定对话回复。 |
| **AcpProvider** | `CODEX_MOCK=false`、ACP 启动器在 `PATH`、且未强制 legacy | **stdio JSON-RPC** 长连接：默认 `codex-acp`，若无则用 `npx -y @zed-industries/codex-acp`。子进程里的 `codex` 通过解析后的可执行文件（Windows 上可自动指向 Xinfei 的 `codex.exe`）+ `PATH` 前置。 |
| **LegacyCodexProvider** | `CODEX_MOCK=false` 但无 ACP 或 `ACP_BACKEND=legacy` | 每次一次 `codex exec`，使用同一套解析出的 Codex 可执行文件。 |

仓库内 **`.agents/skills/`** 下的 Codex 风格 `SKILL.md`：当 **ACP 的 `session/new` 工作目录** 指向仓库根时，由 Codex 自动发现；非 Codex 类 agent 则通过 **提示词注入** 附带技能正文（可用 `ACP_AGENT_NATIVE_SKILLS` 控制）。

更完整的架构说明见 [`docs/architecture.zh-CN.md`](docs/architecture.zh-CN.md)。

---

## 信飞 Xinfei 企业版 Codex（Windows）

若已安装到 `%LOCALAPPDATA%\Programs\XinfeiCodex\bin\codex.exe`，在未设置 `CODEX_BINARY` / `CODEX_CLI_COMMAND` 时，后端会**优先使用该 `codex.exe`**，避免从子进程调用 `xinfei-codex.cmd`（PowerShell 对 `login status` 的 stderr 可能直接中止）。

- **ACP：**`codex-acp` 内部会启动 `codex`；我们会把解析出的 `codex.exe` 所在目录**前置到子进程 `PATH`**，确保走企业版二进制。
- **SSO：**首次非 Mock 请求时，若判定为 Xinfei 安装，会检查 `codex login status` 是否含 `Logged in using Enterprise SSO`。未登录时默认**只打日志**；`XINFEI_CODEX_ENFORCE_SSO=true` 会抛错；`XINFEI_CODEX_AUTO_LOGIN=true` 会执行 `codex login --enterprise-sso`（可能弹出浏览器）。

---

## 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `CODEX_MOCK` | `true` | `true` 使用 Mock；`false` 走真实模型（优先 ACP，否则 legacy）。 |
| `CODEX_BINARY` | *(自动)* | `codex.exe` / `codex` 的绝对路径；覆盖自动发现；用于 legacy 与 ACP 的 `PATH` 前置。 |
| `CODEX_CLI_COMMAND` | *(未设置则自动)* | 若设置：作为 legacy 解析输入；`.cmd`/`.bat`/`.ps1` 包装脚本在检测到 Xinfei 时会被替换为内层 `codex.exe`。 |
| `CODEX_TIMEOUT_SECONDS` | `60` | Legacy 等待超时；ACP 侧也可能读取。 |
| `CODEX_RETRY_COUNT` | `1` | 计划 / 改计划解析失败时的重试次数。 |
| `CODEX_AUTO_MOCK_THRESHOLD` | `3` | 连续失败达到 N 次后，进程内自动改走 Mock。 |
| `CODEX_HTTP_TRANSPORT_ONLY` | `true` | Legacy Codex：是否用自定义 HTTP/SSE provider（见架构文档）。 |
| `CODEX_SSE_PROVIDER_ID` | `openai_sse` | 自定义 provider 表名。 |
| `CODEX_EXTRA_CONFIG` | *(空)* | 额外 `codex -c`，分号分隔。 |
| `ACP_AGENT_COMMAND` | *(自动)* | 未设置时：有 `codex-acp` 用它，否则 `npx -y @zed-industries/codex-acp`。也可显式写完整路径。 |
| `ACP_AGENT_ARGS` | *(空)* | 额外参数（按 shell 分词）。 |
| `ACP_AGENT_PATH_PREPEND` | `true` | 非 `false`/`0`/`off` 时，把 `resolve_codex_executable()` 所在目录前置到 ACP 子进程 `PATH`。 |
| `ACP_AGENT_INHERIT_FULL_ENV` | `true` | 非 `false`/`0`/`off` 时，ACP 子进程继承后端完整的 `os.environ`（接近本机终端），而不是 SDK 的精简环境，可减少 **502**、鉴权、`npx` 等问题。 |
| `ACP_AGENT_STDERR` | `inherit` | `inherit`（默认）：子进程 stderr 打到 API 进程，与 uvicorn 日志一起看。`null`/`devnull`：丢弃。`pipe`：SDK 默认行为，若无人读 stderr 且输出多，**管道塞满会卡死**（界面一直 Thinking）。 |
| `STREAMLIT_CHAT_TIMEOUT_SECONDS` | `300` | 关闭 Mock 时 Streamlit 调用 `/chat` 的超时（秒）。 |
| `ACP_BACKEND` | *(自动)* | `legacy` / `exec` / `codex-exec` 强制不用 ACP。 |
| `XINFEI_CODEX_ENFORCE_SSO` | `false` | 为真且未处于企业 SSO 状态时，首次真实请求直接失败。 |
| `XINFEI_CODEX_AUTO_LOGIN` | `false` | 为真且未 SSO 时，执行 `codex login --enterprise-sso`（交互）。 |
| `ACP_CHAT_SESSION_KEY` | `xyf-global-chat` | `/chat` 使用的逻辑会话键，保证多轮连续。 |
| `ACP_SESSION_CWD` | *(仓库根)* | `session/new` 的工作目录，供 Codex 加载 `.agents/skills`、`AGENTS.md`。 |
| `ACP_AGENT_NATIVE_SKILLS` | *(自动)* | `true`/`false` 覆盖是否向提示词注入技能；未设置时，若命令名含 `codex` 则默认不注入（由 agent 自发现）。 |
| `API_BASE_URL` | `http://127.0.0.1:8000` | Streamlit 访问的后端地址。 |

---

## 技能（`.agents/skills`）

采用 **Codex / agentskills** 约定：每个子目录一个 `SKILL.md`，含 YAML 头（`name`、`description`）与正文说明。

- 内置示例：`analysis-planner`、`data-chat`、`plan-reviser`（与提示词构建函数对应）。
- **列出元数据：** `GET http://127.0.0.1:8000/skills`

---

## 常见问题

| 现象 | 可能原因 | 处理 |
|------|----------|------|
| `ModuleNotFoundError: No module named 'acp'` | 未安装依赖 | 在仓库根执行 `uv sync`，并用 `uv run …` 启动。 |
| `ImportError: ACP mode requires 'agent-client-protocol'` | 关了 Mock 但未装 SDK | `uv sync` 或 `pip install 'agent-client-protocol>=0.8.1'`。 |
| 后端能起但 ACP 调用失败 | 未安装 ACP 适配器 | 安装 `codex-acp`（如 `npm i -g @zed-industries/codex-acp`）或保证 `npx` 在 `PATH`（默认会 `npx -y …`），或 `ACP_BACKEND=legacy`。 |
| Legacy/ACP 在 Xinfei 下异常 | 包装脚本 + SSO 输出到 stderr | 不设 `CODEX_CLI_COMMAND` 即可自动用内层 `codex.exe`，或显式设置 `CODEX_BINARY` 指向该 `codex.exe`。 |
| ACP 报 `NotImplementedError`（`create_subprocess_exec`，Windows） | uvicorn `--reload` 在 Windows 上选了 `SelectorEventLoop`（无子进程管道） | 加 `--loop backend.loop_factory.proactor_loop_factory`，或用 `uv run python scripts/run_uvicorn_windows.py --reload`，或设 **`ACP_BACKEND=legacy`**。 |
| Streamlit 一直 **Thinking…**（真实模式） | 模型慢、**stderr 管道堵死**（勿用 `ACP_AGENT_STDERR=pipe`）、或首次 `npx` 下载久 | 用 **`--log-level debug`** 看 `CHAT begin`、`ACP spawning agent`、`ACP prompt start/end`。保持 **`ACP_AGENT_STDERR=inherit`**。按需加大 `CODEX_TIMEOUT_SECONDS` / `STREAMLIT_CHAT_TIMEOUT_SECONDS`。 |
| Codex 不加载技能 | `cwd` 不对 | 将 `ACP_SESSION_CWD` 设为仓库根目录的**绝对路径**。 |

---

## 分支与工作流

- `main`：日常集成分支  
- `master`：演示/答辩用稳定呈现  
- `dev/win`：Windows 原生开发  
- `dev/wsl`：WSL/Linux  

验证后合并回 `main`；不要把本机路径或密钥提交进共享分支。

---

## Windows / WSL 简述

**Windows：** `git checkout dev/win` → `uv sync` → `./scripts/start-dev.ps1 -CodexMock "true"`

**WSL：** `git checkout dev/wsl` → `uv sync` → 分别 `uv run uvicorn …` 与 `uv run streamlit …`

---

## 运行回归测试

```bash
uv run python tests/run_regression.py --mode mock
uv run python tests/run_regression.py --mode real   # 需本机 Codex CLI 已配置
```

输出为 JSON：`passed`、`total`、`success_rate` 及各用例明细。

---

## 项目结构

```
xyf-competition-mvp/
├── .agents/
│   └── skills/                 # SKILL.md（Codex 发现 + SkillRegistry）
├── app/
│   └── streamlit_app.py        # 对话/任务 UI、上传、审阅、结果
├── backend/
│   ├── main.py                 # FastAPI；lifespan 内 shutdown_providers()
│   ├── storage.py
│   ├── observability.py
│   ├── acp/                    # ACP 客户端、各 Provider、工厂、legacy 实现
│   ├── skills/                 # SkillRegistry、原生技能检测、提示词注入
│   ├── routers/
│   │   ├── tasks.py            # /tasks/*
│   │   ├── chat.py             # POST /chat
│   │   ├── data.py             # POST /data/profile
│   │   └── skills.py           # GET /skills
│   ├── schemas/
│   ├── codex/
│   │   ├── prompts.py          # 计划/总结/追问/对话/改计划 提示词
│   │   ├── adapter.py          # 兼容层 → LegacyCodexProvider
│   │   └── mock.py             # 兼容层 → MockProvider
│   ├── execution/
│   └── profiler/
├── tests/
├── artifacts/
├── scripts/
├── docs/
│   ├── architecture.md
│   ├── architecture.zh-CN.md
│   └── product-thoughts.md
└── pyproject.toml
```

---

## 给开发者

完整分层说明、ACP/Mock/Legacy 选择逻辑、Chat/改计划/画像接口、技能与提示词注入规则、扩展清单与 MVP 边界，见 [`docs/architecture.zh-CN.md`](docs/architecture.zh-CN.md)（或 [英文版](docs/architecture.md)）。
