# 架构说明与开发指南

> [English](architecture.md)

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
- 规划/对话/改计划提示词都会注入技能正文
- 元数据接口：`GET /skills`

## 主要请求链路

- `/chat`：自由文本对话
- `/tasks`：文件 + 问题生成计划
- `/tasks/{id}/revise`：自然语言改计划
- `/tasks/{id}/review`：提交计划并执行，生成 summary/follow-ups
- `/data/profile`：仅做 schema 画像，不创建任务

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
