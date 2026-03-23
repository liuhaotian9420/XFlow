# xyf-competition-mvp

> [English](README.md)

面向自然语言的数据分析工作台。

上传 CSV 或 Excel，用日常语言描述你想分析什么，审阅系统生成的分析计划，即可获得图表、数据表和文字总结——全程无需写 SQL 或代码。

---

## 快速开始

### 1. 安装依赖

```bash
uv sync
```

### 2. 启动后端（终端 1）

```bash
uv run uvicorn backend.main:app --reload
```

后端地址：`http://127.0.0.1:8000`。交互式 API 文档：`http://127.0.0.1:8000/docs`。

### 3. 启动前端（终端 2）

```bash
uv run streamlit run app/streamlit_app.py
```

前端地址：`http://localhost:8501`。

### 4. 一键启动（PowerShell，会打开两个终端窗口）

```powershell
./scripts/start-dev.ps1 -CodexMock "true"
```

---

## 使用流程

```
Ask 页    →  上传文件 + 输入分析问题
Plan 页   →  查看系统生成的 AnalysisPlan
Review 页 →  按需修改筛选条件 / 指标 / 维度，然后提交
Results 页 →  图表 + 表格 + 总结 + 后续问题建议
```

---

## 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `CODEX_MOCK` | `true` | `true` 使用 MockAdapter（无需 Codex CLI）；`false` 调用真实 Codex CLI |
| `CODEX_CLI_COMMAND` | `codex` | Codex CLI 可执行文件的路径或名称 |
| `CODEX_TIMEOUT_SECONDS` | `60` | 等待 Codex CLI 返回的最长时间（秒） |
| `CODEX_RETRY_COUNT` | `1` | 解析失败时的重试次数 |
| `CODEX_AUTO_MOCK_THRESHOLD` | `3` | 连续 Codex 失败达到 N 次后自动降级为 Mock |
| `API_BASE_URL` | `http://127.0.0.1:8000` | Streamlit 前端访问的后端地址 |

---

## 运行回归测试

```bash
# Mock 模式（不需要安装 Codex CLI）
uv run python tests/run_regression.py --mode mock

# 真实模式（需要已安装并配置好的 Codex CLI）
uv run python tests/run_regression.py --mode real
```

输出为 JSON 报告，包含 `passed`、`total`、`success_rate` 以及每个用例的明细。

---

## 项目结构

```
xyf-competition-mvp/
├── app/
│   └── streamlit_app.py        # Streamlit 界面（Ask / Plan / Review / Results 四个页签）
├── backend/
│   ├── main.py                 # FastAPI 应用入口
│   ├── storage.py              # 内存任务存储（进程重启后清空）
│   ├── observability.py        # 结构化日志与快照工具
│   ├── routers/
│   │   └── tasks.py            # 所有 /tasks 相关接口
│   ├── schemas/
│   │   ├── plan.py             # AnalysisPlan 及相关类型
│   │   ├── task.py             # TaskRecord、TaskStatus
│   │   └── result.py           # ResultPayload、ChartPayload、TablePayload
│   ├── codex/
│   │   ├── adapter.py          # CodexAdapter：子进程调用 + JSON 解析
│   │   ├── mock.py             # MockAdapter：确定性计划，无需 CLI
│   │   └── prompts.py          # 计划 / 总结 / 追问的提示词模板
│   ├── execution/
│   │   └── engine.py           # AnalysisPlan → pandas 运算 → ResultPayload
│   └── profiler/
│       └── schema_profiler.py  # 文件上传 → 列元数据字典
├── tests/
│   ├── fixtures/
│   │   ├── cases.json          # 回归用例定义
│   │   ├── sales_data.csv
│   │   ├── employee_survey.csv
│   │   └── web_traffic.csv
│   └── run_regression.py       # 回归脚本（mock / real 两种模式）
├── artifacts/                  # 运行时自动创建：任务快照与事件日志
│   ├── events.log
│   └── tasks/<task_id>/        # 每个任务的 JSON 快照
├── scripts/
│   └── start-dev.ps1           # 一键本地开发启动（PowerShell）
├── docs/
│   ├── product-thoughts.md     # 产品思路笔记
│   ├── architecture.md         # 开发者指南（英文）
│   └── architecture.zh-CN.md   # 开发者指南（中文）
└── pyproject.toml
```

---

## 给开发者

更完整的架构说明、扩展方式与 MVP 边界，请阅读 [`docs/architecture.zh-CN.md`](docs/architecture.zh-CN.md)（或 [英文版](docs/architecture.md)），其中包括：

- 各层职责与代码位置
- 如何新增一种分析能力
- 如何提升 Codex 提示词与计划质量
- 如何添加测试夹具与回归用例
- 当前刻意未实现的功能及原因
