# 架构说明与开发指南

> [English](architecture.md)

> 数据分析 Agent 的论证架构与后续 MVP 迭代指导见：[分析 Agent 论证架构与 MVP 迭代指南](analysis-agent-architecture.zh-CN.md)

本文说明当前运行时：真实模型链路仅保留一次性 `codex exec`。

## 总览

```text
Streamlit UI (app/streamlit_app.py)
  -> FastAPI 路由层 (backend/routers/*)
  -> Provider 选择 (backend/codex/factory.py)
       - MockProvider
       - LegacyCodexProvider (codex exec)
  -> 执行引擎 (backend/execution/engine.py)
  -> 可观测性与内存存储
```

## 运行时选择

- `CODEX_MOCK=true`（默认）：`MockProvider`
- `CODEX_MOCK=false`：`LegacyCodexProvider`

统一入口：
- `backend.codex.factory.get_provider()`

兼容生命周期钩子：
- `backend.codex.factory.shutdown_providers()`（当前为空实现）

## Codex 运行时模块

- `backend/codex/legacy.py`：`codex exec` 一次性子进程调用
- `backend/codex/mock.py`：离线确定性 mock
- `backend/codex/xinfei_sso.py`：Codex 可执行解析 + 信飞企业 SSO 检查
- `backend/codex/json_util.py`：从模型输出中提取 JSON
- `backend/codex/errors.py`：`CodexAdapterError`
- `backend/codex/adapter.py`：为旧脚本/测试保留的兼容重导出

## 技能体系

- SkillRegistry 扫描 `.agents/skills/*/SKILL.md`
- 运行时依赖 Codex 原生 skills discovery/progressive disclosure
- 提示词仅传短显式 hint（例如 `$analysis-planner`），不再注入技能全文
- 元数据接口：`GET /skills`

## 主要请求链路

- `/chat`：自由文本对话
- `/tasks`：文件 + 问题生成计划
- `/tasks/{id}/revise`：自然语言改计划
- `/tasks/{id}/review`：提交计划并执行，生成 summary/follow-ups
- `/data/profile`：仅做 schema 画像，不创建任务

## 分析 Agent 论证架构

当前 `/tasks` 主链路已经具备“计划 → Review → 确定性执行 → 结果”的基础能力。对于后续需要解释、归因、实验或复杂数据科学分析的迭代，不建议继续把所有逻辑堆入 `AnalysisPlan` 或构造成一个无限工具循环的超级 Agent。

推荐采用独立的分析论证层：

```text
Evidence → Claim → Warrant → Inference
```

其中：

- `Evidence` 表示可追溯的数据和方法结果
- `Claim` 表示 Evidence 允许准确陈述的事实
- `Warrant` 表示从 Claim 到 Inference 的候选推理模型和适用条件
- `Inference` 表示在当前 Belief、Claim、Warrant 和假设下形成的解释或判断

推荐的逻辑 Agent 角色为：

- `Analyst Agent`：推进分析、生成候选 Warrant、形成 Claim 和 Inference
- `Domain Agent`：按需提供业务语义和方法论约束
- `Critic Agent`：审计 Evidence、维护 Warrant、挑战 Inference
- `Human Gate`：在高风险结论和长期知识沉淀时承担最终责任

完整设计见[分析 Agent 论证架构与 MVP 迭代指南](analysis-agent-architecture.zh-CN.md)。

## 本地验证

```bash
uv sync
uv run uvicorn backend.main:app --reload
uv run streamlit run app/streamlit_app.py
uv run python tests/run_regression.py --mode mock
```

真实模式：

```bash
uv run python tests/run_regression.py --mode real
```
