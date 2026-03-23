# 架构说明与开发者指南

> [English](architecture.md)

本文说明系统如何分层、请求如何流转，以及后续迭代时该改哪里。如果你是第一次参与本仓库，建议从这里读起。

---

## 系统总览

```
用户（浏览器）
    │
    ▼
Streamlit 前端  (app/streamlit_app.py)
    │  HTTP（requests）
    ▼
FastAPI 后端  (backend/main.py)
    ├── Schema profiler  →  从上传文件抽取列元数据
    ├── Codex adapter    →  调用 Codex CLI（或 MockAdapter）生成计划
    ├── Execution engine →  在 pandas DataFrame 上执行计划
    └── Observability    →  将结构化日志与 JSON 快照写入 artifacts/
```

用户不会直接看到原始数据或代码；所有分析意图都通过 **AnalysisPlan** 这一份结构化 JSON 在中间传递，它描述「要算什么、怎么分组、怎么筛、怎么出图」。

---

## 请求生命周期

### 第一步：创建任务（`POST /tasks`）

1. 前端把上传文件与自然语言问题发给后端。
2. `schema_profiler.profile_upload()` 将文件解析为 `pd.DataFrame`，并抽取列名、dtype、空值数、样本值等。
3. 这份 schema profile 交给 **Codex 适配层** 的 `generate_plan`，得到 `AnalysisPlan`。
4. 任务写入内存（`backend/storage.py`），状态为 `planned`。
5. 同一份 DataFrame 也以 `task_id` 为键保存在内存中，供后续执行使用。

### 第二步：审阅计划（`GET /tasks/{id}`，对应 Plan / Review 页签）

1. 前端拉取任务，把计划以可编辑 JSON 形式展示。
2. 用户可改任意字段：增删筛选、改聚合方式、调整图表类型等。
3. 若 `confidence < 0.6` 或 `ambiguities` 非空，界面会给出提醒，提示仔细核对。

### 第三步：提交审阅并执行（`POST /tasks/{id}/review`）

1. 前端提交（可能已编辑的）`final_plan`。
2. 后端调用 `execution.engine.run_plan(df, final_plan)`：应用筛选、分组聚合，并组装图表与表格载荷。
3. 再次调用适配层的 `generate_summary` 与 `generate_followups`。
4. 任务状态依次经历：`reviewing` → `running` → `completed`（失败则为 `failed`）。

### 第四步：获取结果（`GET /tasks/{id}/result`）

返回 `ResultPayload`：图表数据、表格行、执行过程说明、模型生成的文字总结，以及若干后续分析问题。

---

## 核心数据结构

所有契约类型都在 `backend/schemas/` 下，用 Pydantic 定义，可视为层与层之间的「唯一真相来源」。

### `AnalysisPlan`（`schemas/plan.py`）

系统的中心对象：由 Codex 适配层产出，由执行引擎消费。

```
AnalysisPlan
├── goal: str                         # 用自然语言概括分析意图
├── metrics: list[MetricSpec]         # 要算的指标（列 + 聚合方式 + 别名）
├── dimensions: list[DimensionSpec]   # 分组维度（列 + 角色：时间/类别/地理）
├── filters: list[FilterSpec]         # 行级筛选（列 + 操作符 + 取值）
├── output: OutputSpec                # 图表类型（折线/柱状/直方）+ 是否展示表格
├── ambiguities: list[AmbiguitySpec]  # 模型认为不确定的字段说明
└── confidence: float | None          # 0.0–1.0，模型自评计划可靠度
```

### `TaskRecord`（`schemas/task.py`）

跟踪单次分析请求的完整生命周期。

```
TaskRecord
├── task_id: str
├── status: TaskStatus   # created → planned → reviewing → running → completed / failed
├── input: TaskInput     # 问题原文、文件名、行列规模
├── plan: AnalysisPlan   # 用户审阅前的 LLM 初版计划
├── final_plan: AnalysisPlan | None   # 用户确认或修改后的计划
├── result: ResultPayload | None
└── error: TaskError | None
```

### `ResultPayload`（`schemas/result.py`）

```
ResultPayload
├── chart: ChartPayload       # 图表类型、x/y 列名、数据行
├── table: TablePayload       # 列名列表 + 行数据（list[dict]）
├── execution_summary: str    # 用自然语言描述 pandas 实际做了什么
├── summary: str | None       # LLM 生成的结果解读
└── follow_ups: list[str]     # 建议的 3 条后续分析问题
```

---

## Codex 适配层（`backend/codex/`）

这是代码里最重要的抽象：所有与大模型相关的交互都集中在这里，上层不必关心背后是真实 CLI 还是 Mock。

### `adapter.py` — `CodexAdapter`

通过子进程调用 Codex CLI：

```python
await asyncio.create_subprocess_exec("codex", "exec", prompt, ...)
```

标准输出是纯文本。`_extract_json_payload()` 采用两种策略：
1. 对整段输出直接 `json.loads()`。
2. 取第一个 `{` 与最后一个 `}` 之间的子串再解析。

若均失败，抛出 `CodexAdapterError`，路由层会回退到 `MockAdapter`。

可通过环境变量配置：`CODEX_CLI_COMMAND`、`CODEX_TIMEOUT_SECONDS`、`CODEX_RETRY_COUNT`。

### `mock.py` — `MockAdapter`

不调用任何 CLI，按规则生成确定性计划，例如：
- 选一个数值列作为指标；
- 若有日期/时间列则作为时间维度；
- 优先选 region、dept、product 等作为类别维度；
- 识别「华东」「分布」等关键词以追加筛选或切换图表类型。

**本地开发与 CI 建议始终使用 Mock**：设置 `CODEX_MOCK=true`（也是当前默认值）。

### `prompts.py`

三个提示词构建函数：
- `build_plan_prompt` — 要求 Codex 只返回符合结构的 JSON `AnalysisPlan`。
- `build_summary_prompt` — 要求返回 2–4 句中文短总结。
- `build_followups_prompt` — 要求返回含 3 个追问的 JSON 数组。

**若要提升计划质量，优先改这里的文案**；`build_plan_prompt` 里的输出结构说明必须与 `AnalysisPlan` 字段保持同步。

### 自动降级

当 Codex 连续失败达到 `CODEX_AUTO_MOCK_THRESHOLD` 次（默认 3），后端会在当前进程剩余生命周期内把 `CODEX_MOCK` 设为 `true`，避免 CLI 不可用时错误雪崩。

---

## 执行引擎（`backend/execution/engine.py`）

`run_plan(df, plan) → ResultPayload`

纯 pandas，不经过 LLM。分三步：

1. **`_apply_filters`** — 遍历 `plan.filters`，用布尔索引筛选；若某列不存在则跳过该条（温和降级）。
2. **`_aggregate`** — 若 `plan.metrics` 非空，则 `df.groupby(dimensions).agg(metrics)`；无维度时对整表聚合；结果最多保留 500 行。
3. **`_build_chart`** — 选择 x/y 列并组装 `ChartPayload`；直方图场景用 `value_counts()`。

**新增聚合方式**：在 `schemas/plan.py` 的 `Aggregation` 枚举中增加取值即可；引擎直接把 `metric.aggregation.value` 传给 pandas，如 `sum`、`mean` 等。

**新增筛选操作符**：在 `FilterOperator` 中增加枚举，并在 `_apply_filters` 里补分支。

---

## Schema 画像（`backend/profiler/schema_profiler.py`）

`profile_upload(file: UploadFile) → (pd.DataFrame, dict)`

支持 `.csv`、`.xlsx`、`.xls`；拒绝空文件。若行数超过 1 万，会随机抽样 1 万行（`random_state=42`，结果可复现）。

返回的 `dict` 即传给 Codex 的 schema profile：含列名、dtype、空值数、每列最多 5 个样本值，便于模型把自然语言里的「销售额」「区域」等对到真实列名。

---

## 可观测性（`backend/observability.py`）

每个任务会在 `artifacts/`（自动创建）下产生两类产物：

| 产物 | 路径 | 内容 |
|------|------|------|
| 事件日志 | `artifacts/events.log` | 每行一条 JSON：`ts`、`task_id`、`stage`、`event_type`、`payload` |
| 快照 | `artifacts/tasks/<task_id>/<name>.json` | input、schema_profile、plan、final_plan、result、错误、diff 等的完整 JSON |

**排查失败任务**：在界面记下 `task_id`，打开 `artifacts/tasks/<task_id>/`；`review_diff.json` 可对照用户在 Review 页改了哪些字段。

---

## 存储（`backend/storage.py`）

三个模块级内存字典：

| 字典 | 键 | 值 |
|------|----|----|
| `TASKS` | `task_id` | `TaskRecord` |
| `TASK_DATAFRAMES` | `task_id` | `pd.DataFrame` |
| `TASK_SNAPSHOTS` | `task_id` | 原始 schema profile 等 |

**服务重启后数据全部丢失**——这是 MVP 有意为之。若要持久化，可把这些字典换成数据库（SQLite 通常是第一步），详见下文「刻意未实现的能力」。

---

## API 一览

所有路由挂在 `/tasks`（`backend/routers/tasks.py`）。

| 方法 | 路径 | 作用 |
|------|------|------|
| `POST` | `/tasks` | 创建任务：上传文件 + 问题 → 返回计划 |
| `GET` | `/tasks/{id}` | 获取完整 `TaskRecord` |
| `POST` | `/tasks/{id}/review` | 提交最终计划 → 执行 → 返回更新后的记录 |
| `GET` | `/tasks/{id}/result` | 获取 `ResultPayload`（未就绪时返回状态说明） |
| `POST` | `/tasks/{id}/fail` | 开发用：手动标记任务失败 |
| `POST` | `/tasks/{id}/reset` | 恢复：将卡住的任务重置为 `planned` |

交互式文档：`http://127.0.0.1:8000/docs`

---

## 扩展功能时的检查清单

### 新增筛选操作符

1. 在 `backend/schemas/plan.py` 的 `FilterOperator` 中增加枚举值。
2. 在 `backend/execution/engine.py` 的 `_apply_filters` 中增加分支。
3. 在 `backend/codex/prompts.py` 的 `build_plan_prompt` 里更新输出结构说明。
4. 在 `tests/fixtures/cases.json` 增加用例，并配上对应 CSV。

### 新增图表类型

1. 在 `backend/schemas/plan.py` 的 `ChartType` 中增加枚举。
2. 在 `app/streamlit_app.py` 的 `_draw_chart` 中增加渲染分支。
3. 在 `backend/execution/engine.py` 的 `_build_chart` 中补充数据构造逻辑。

### 新增 LLM 能力（例如异常检测）

1. 在 `backend/codex/prompts.py` 增加提示词构建函数。
2. 在 `CodexAdapter` 与 `MockAdapter` 中各增加对应方法（两边行为要对齐）。
3. 在合适的 router 中调用。
4. 若结果需要持久化，在相关 schema 中增加字段。

### 提升计划质量

编辑 `backend/codex/prompts.py` 中的 `build_plan_prompt`。常见有效手段：
- 补充示例列名，帮助模型对齐 schema；
- 加入少量高质量计划的 few-shot；
- 收紧 JSON 结构描述，减少虚构字段名。

---

## 运行测试

```bash
# 回归（Mock 模式，无需 Codex CLI）
uv run python tests/run_regression.py --mode mock

# 回归（真实模式，需要 Codex CLI）
uv run python tests/run_regression.py --mode real
```

夹具在 `tests/fixtures/`。`cases.json` 里每条包含：
- `name` — 用例标识
- `file` — 相对 `fixtures/` 的 CSV 文件名
- `question` — 自然语言问题
- `expected_chart_type` — `"line"`、`"bar"` 或 `"histogram"`
- `expected_metric_column` — 期望的指标列名（仅供参考）

新增用例：把 CSV 放进 `tests/fixtures/`，再在 `cases.json` 里追加一条即可。

---

## 刻意未实现的能力（MVP 边界）

下列项是已知取舍，不是遗漏的 bug；为控制 MVP 范围而暂缓。

| 能力 | 状态 | 说明 |
|------|------|------|
| 持久化存储 | 未实现 | 仅内存；重启任务清空 |
| 身份认证 | 未实现 | 无账号、无 API Key |
| 多轮对话 / 记忆 | 未实现 | 每个任务相互独立 |
| Skill 库 | 未实现 | 无可复用的分析模板体系 |
| ACP 等 Agent 协议 | 未实现 | 直接调 Codex CLI |
| 流式响应 | 未实现 | 结果同步返回 |
| Excel 导出 | 未实现 | 表格仅支持 CSV 下载 |
| 多表关联 | 未实现 | 单次任务单文件 |
| 列级权限 | 未实现 | LLM 可见全部列元数据 |

---

## 依赖说明

| 包 | 用途 |
|----|------|
| `fastapi` + `uvicorn` | 后端 API 服务 |
| `streamlit` | 前端界面 |
| `pandas` + `numpy` | 执行引擎中的数据处理 |
| `pydantic` | 各层数据契约校验 |
| `python-multipart` | FastAPI 文件上传所需 |
| `requests` | Streamlit 调用后端 |
| `uv` | 包管理与虚拟环境 |

Codex CLI **不是** Python 包，需单独安装并能在 `PATH` 中找到（或通过 `CODEX_CLI_COMMAND` 指定）。当 `CODEX_MOCK=true` 时不会调用 CLI。
