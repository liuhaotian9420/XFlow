# xyf-competition-mvp：需求、问题与可能解法（当前思路浓缩）

## 1. 项目目标

做一个面向数据分析场景的 Streamlit 应用：

- 用户用**自然语言**描述分析需求
- 用户通过**上传 Excel / CSV**，或**输入 SQL** 提供数据
- 系统在云端执行 SQL / 数据处理逻辑
- 最终返回给用户：
  - 结构化结果表
  - 图表
  - 关键结论摘要
  - 可追问、可复用的分析结果

一句话：

> 这是一个“自然语言驱动的数据分析工作台”，而不只是一个“问答机器人”或“SQL 生成器”。

---

## 2. 当前核心需求

### 2.1 自然语言分析入口
用户不应该被迫先写 SQL 或先理解数据结构，而是可以先说问题：

- 帮我看最近三个月华东区销售额变化
- 分析各区域转化率差异
- 找出异常月份和可能原因

系统需要把自然语言转成：
- 分析目标
- 指标（metrics）
- 维度（dimensions）
- 行过滤（row filters）
- 列选择（column selection）
- 输出形式（表 / 图 / 摘要）

---

### 2.2 数据输入支持
当前优先支持：

- 上传 Excel / CSV
- 用户直接输入 SQL

后续可扩展：
- 固定数据库连接
- 历史数据集复用
- 多数据源组合

---

### 2.3 云端执行
系统需要能够在后端执行：

- SQL 查询
- 基础数据变换
- 聚合 / 分组 / 过滤
- 结果统计与图表生成

模型负责“理解、规划、生成候选逻辑”，执行层负责“真正跑起来”。

---

### 2.4 结果交付
结果不应只是 raw table，而应至少包括：

- 结论摘要
- 图表
- 明细表
- SQL 草稿 / 执行逻辑（可选展示）
- 后续建议（follow-up questions / actions）

---

## 3. 关键 caveats / 难点

### 3.1 Row / Column Filter 能力
用户经常会提出：

- 只看华东地区
- 只看最近三个月
- 去掉退款订单
- 按产品线拆分

所以系统不能只做“生成 SQL”，而必须支持：

- 自动识别字段语义
- 自动抽取行过滤条件
- 自动识别需要保留/排除的列
- 允许用户修正这些过滤与映射

#### 对应解法
在“执行前”增加一个 **分析计划 / 结构化解析页**，展示：
- 识别出的字段
- 字段类型与角色
- 行过滤条件
- 维度 / 指标
- SQL 草稿（可选）

用户可在这里进行人工修正。

---

### 3.2 Human-in-the-loop
系统不能完全黑盒自动执行，因为可能会出现：

- 指标定义歧义
- 时间范围歧义
- 字段理解错误
- 过滤条件不正确
- SQL 生成不符合预期

#### 对应解法
先做 **Lite HITL（轻量人工介入）**，而不是重型工作流：

- 执行前确认
- 歧义问题澄清
- 字段类型 / 角色修正
- 过滤条件修正
- SQL 轻量查看与编辑

不建议一开始做：
- 复杂审批流
- 拖拽式工作流设计器
- 多人实时协同 review
- 超复杂中途分支控制

结论：

> Streamlit 适合做“审阅式 human-in-the-loop”，不适合做“重交互式流程编排”。

---

### 3.3 Skill / Memory 沉淀闭环
项目不应该只做“一次性分析”，而应形成：

> 分析越多，系统越懂这个业务、越会这个套路、越能复用历史经验。

这意味着系统要能把每次分析沉淀为知识资产。

#### 需要区分三类沉淀对象

##### Memory
记录长期上下文事实与偏好：
- 用户偏好（比如更喜欢摘要优先）
- 业务口径（如 GMV 不含退款）
- 字段语义（如 region_code 是大区编码）
- 默认时间窗口（如“最近”默认是 30 天）

##### Skill
记录可复用的方法与模板：
- 销售波动分析模板
- 渠道漏斗分析模板
- 常见 SQL pattern
- 解析字段角色的规则
- 生成计划 → SQL → 总结 的 workflow

##### Artifact
记录本次任务的运行产物：
- 用户问题
- 数据摘要
- SQL 草稿
- 执行日志
- 图表配置
- 结果表
- 人工修正记录

#### 对应解法
不要把所有结果自动写入 memory / skill，而是：

1. 每次分析先保存 artifact
2. 从 artifact 中抽取 knowledge candidates
3. 让用户确认哪些进入 memory / skill
4. 经确认后再沉淀

---

### 3.4 Codex client 集成
另一个关键点是：

- 希望 Streamlit App 能够调用本地大模型能力
- 具体希望对接 Codex client 作为“大模型输入/输出层”

#### 风险
如果让 Streamlit 直接调用 Codex client，会出现：
- UI 与 agent runtime 强耦合
- 任务生命周期难管理
- 不利于权限隔离
- 不利于调试、观测和回放

#### 对应解法
采用如下结构：

```text
Streamlit UI
    ↓
FastAPI Orchestrator
    ↓
Codex Adapter / Client Layer
    ↓
SQL Executor / Memory / Skill / Artifact / Git
```

即：
- Streamlit 只负责交互
- FastAPI 负责任务编排与状态管理
- Codex 负责理解、规划、生成
- 执行器负责真实执行
- 知识层负责沉淀与版本管理

结论：

> 不建议让 Streamlit 直接裸调 Codex CLI；建议通过 FastAPI orchestration layer 间接调用。

---

## 4. 推荐的产品流程（MVP）

### Step 1：Ask
用户：
- 输入自然语言问题
- 上传 Excel / CSV，或输入 SQL

### Step 2：Plan
系统生成：
- 需求理解
- 字段识别
- row / column filters
- metrics / dimensions
- SQL candidate
- 歧义点 / 风险点

### Step 3：Review
用户进行：
- 计划确认
- 字段修正
- 过滤修正
- 歧义回答

### Step 4：Run
后端执行：
- SQL / 数据处理
- 图表与结果生成
- 执行日志记录

### Step 5：Results
系统返回：
- 结论摘要
- 图表
- 表格
- SQL / 逻辑说明
- follow-up 建议

### Step 6：Learn
系统抽取知识候选：
- Memory candidates
- Skill candidates
- Artifact 保存

用户确认后沉淀。

一句话总结：

> Ask → Plan → Review → Run → Results → Learn

---

## 5. 推荐的页面结构

### 方案 A：先用单页 + tabs（MVP 友好）
推荐 tabs：
- Ask
- Plan
- Review
- Run
- Results
- Learn

优点：
- 开发快
- 状态容易集中管理
- 很适合 Streamlit 先做验证

---

### 方案 B：后续升级为多页面
可拆分为：
- 首页 / 分析发起页
- 分析计划页
- 执行与介入页
- 结果与沉淀页
- 历史 / 模板 / 资产页

---

## 6. 版本化与 Git 管理思路

### 为什么可以用 Git
Memory / Skill 本质上是：
- 文本化
- 结构化
- 可 diff
- 可 review
- 可回滚

所以非常适合 Git 管理。

---

### 建议的 Git 化对象
适合进入 Git：
- memory 条目（markdown / yaml / json）
- skills 模板
- SQL patterns
- prompts
- glossary / schema semantics
- review 记录摘要

不适合直接进入 Git：
- 大体量原始数据
- 高频噪声日志
- 敏感原始 Excel 文件

---

### 建议的 Git 工作方式

#### 方式 1：确认后自动 commit
每次用户确认沉淀后：
- 写入 memory / skill 文件
- 自动生成 commit message

示例：
- `memory: add GMV definition for project xyf`
- `skill: add sales anomaly diagnosis template`

#### 方式 2：staging → review → merge
更稳的做法：
- 先把候选内容写入 staging
- 生成 diff summary
- 用户确认
- merge 到正式知识库

这相当于：

> Knowledge PR Workflow

---

## 7. 推荐的系统分层

```text
[Streamlit UI]
- 用户输入
- 文件上传
- Plan / Review / Result 展示
- 人工确认

[FastAPI Orchestrator]
- task/job 生命周期
- 状态管理
- 调用 Codex Adapter
- 调用 SQL Executor
- 管理 memory/skill retrieval 与沉淀

[Codex Adapter]
- intent parsing
- planning
- SQL generation
- result explanation
- knowledge candidate extraction

[Execution Layer]
- SQL execution
- dataframe transforms
- chart preparation

[Knowledge Layer]
- memory store
- skill store
- artifact store
- git-backed versioning
```

---

## 8. 当前最现实的 MVP 边界

### P0（必须有）
- 自然语言输入
- Excel / SQL 输入
- 字段自动识别
- row / column filter 初步解析
- Lite HITL（执行前确认 + 修正）
- 结果摘要 + 图表 + 表格

### P1（应该有）
- 歧义澄清
- SQL 草稿可查看
- 执行日志
- 历史任务记录

### P2（加分项）
- 结果沉淀为 memory / skill
- Git 化知识版本管理
- 模板复用
- 用户偏好学习

---

## 9. 当前共识（浓缩版）

1. 这不是一个普通 chat-with-data 工具，而是一个 **自然语言驱动的数据分析工作台**。
2. 重点不只是“转 SQL”，而是“理解需求 → 规划 → 人工确认 → 执行 → 沉淀知识”。
3. Streamlit 适合做 **Lite HITL**，不适合重型流程编排。
4. Codex 更适合作为后端 agent brain，通过 FastAPI orchestration 层接入，而不是让 Streamlit 直接调用。
5. 长期壁垒在于 **memory + skill + artifact + git versioning** 这套知识闭环。

---

## 10. ACP（Agent Compute / Agent Runtime）作为 MVP 底座的补充思路

### 为什么 ACP 值得考虑
当前产品流程已经不是单次 LLM 问答，而是一个多阶段分析代理流程：

- 理解用户需求
- 读取 / 理解数据结构
- 生成分析计划
- 生成人工确认所需的结构化结果
- 生成 SQL / 数据处理逻辑
- 等待 human review
- 执行并返回结果
- 抽取 memory / skill candidates

这类流程天然更像一个 **有状态的 agent session**，而不是一次性 completion API。

---

### ACP 可能带来的帮助

#### 1. 承载多阶段、有状态的分析任务
ACP 可以更自然地表达如下状态：
- planning
- awaiting_clarification
- awaiting_review
- running
- completed
- failed

这对 human-in-the-loop 场景尤其重要。

#### 2. 更适合长任务与恢复
分析任务可能涉及：
- schema profiling
- SQL generation
- query execution
- result summarization
- knowledge extraction

这些不一定是一个同步请求就能优雅完成的，ACP 更适合做后台 agent runtime。

#### 3. 更适合和 memory / skill 结合
在一次分析任务中，系统可能需要：
- 先检索 memory
- 再命中 skill
- 再生成分析计划
- 再等待人类确认
- 再继续执行

ACP 这类会话型运行时对这种链路有天然优势。

---

### 需要注意的边界
ACP 不应该直接暴露给最终用户，也不建议让 Streamlit 前端直接裸调 ACP / Codex CLI。

更合理的结构是：

```text
Streamlit UI
    ↓
FastAPI Orchestrator
    ↓
ACP / Codex Runtime
    ↓
SQL Executor / Memory / Skill / Artifact / Git
```

即：
- Streamlit 负责交互
- FastAPI 负责业务接口与状态管理
- ACP / Codex 作为 agent runtime 承载多阶段分析流程
- 执行层与知识层负责真实执行与沉淀

---

### ACP 在本项目中的推荐定位
ACP 更适合作为：

> **分析代理的执行底座 / runtime substrate**

而不是：

> 面向用户的最终产品接口层

也就是说，前台产品仍然暴露业务语义清晰的 API：
- `POST /tasks`
- `GET /tasks/{id}`
- `POST /tasks/{id}/review`
- `GET /tasks/{id}/result`

但内部可以通过 ACP session 去推进整个分析生命周期。

---

### 适合 MVP 的引入方式
第一阶段不必把 ACP 用得太重，可以先只做：

- 一个 analysis session 对应一个用户分析任务
- 用 ACP 承载 plan → review → run → summarize → learn 这条主链路
- 由 FastAPI 对 ACP session 状态做包装和标准化

这样既能利用 ACP 的会话能力，又不会把产品层和运行时耦死。

---

### 当前结论
ACP 对这个 MVP 是有帮助的，但它最适合放在 **后端 agent runtime 层**，而不是直接作为前端调用接口。

一句话总结：

> ACP 适合做“分析代理的执行底座”，不适合直接做“用户产品层”。

---

## 10. 下一步建议

最推荐的后续动作：

1. 在项目里明确目录结构：
   - app/
   - backend/
   - knowledge/
   - artifacts/
   - docs/

2. 先做一个单页/多 tab 的 Streamlit MVP：
   - Ask
   - Plan
   - Review
   - Results
   - Learn

3. 后端先定义 task/job 接口：
   - 创建任务
   - 获取状态
   - 提交 review
   - 获取结果

4. 先把 Skill / Memory 设计成文件化 + Git 管理，而不是一开始上复杂数据库系统

5. 等 MVP 跑通后，再决定哪些沉淀逻辑自动化、哪些仍需 human review

---

## 11. 一句话收束

> 我们要做的不是“让模型帮用户写 SQL”，而是“做一个会随着分析过程持续成长、可审查、可沉淀、可版本化的数据分析代理工作台”。
