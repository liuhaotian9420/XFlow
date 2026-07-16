# 数据分析 Agent 论证架构与 MVP 迭代指南

> 本文记录当前项目对“数据分析 Agent”核心架构的共识，并作为后续 MVP 迭代的设计约束。
>
> 当前产品运行时与 Codex 集成的说明见 [`docs/architecture.zh-CN.md`](architecture.zh-CN.md)。本文关注的是更上层的分析推理架构：如何从一个具体分析需求，形成可追溯、可审阅的分析结论。

## 1. 设计结论

本项目不把数据分析 Agent 定义成“不断调用工具直到模型说完成”的通用自主 Agent，也不试图为所有分析类型写一套统一的 `done` 规则。

核心设计是：

```text
分析需求
  -> 候选解释模型（Candidate Warrant Space）
  -> 区分候选模型的 Evidence Action
  -> 可追溯 Evidence
  -> Atomic Claims
  -> Warrant 更新
  -> Inference
  -> 独立审阅 / 人工维护
```

优秀分析的核心不是“拿到一个数”，也不只是“数值计算正确”，而是：

> **构造一条可追溯的 Evidence -> Claim -> Inference 论证链，并明确每条推理依赖的 Warrant、假设和不确定性。**

简单取数可以在 Claim 层结束；只有需要解释、归因、预测或决策建议时，才继续形成 Inference。

## 2. 核心概念

### 2.1 Analysis Spec

分析任务的显式契约，至少包含：

- 用户问题和分析对象
- 数据范围、时间范围和目标人群
- 期望的交付物
- 当前已知的业务上下文
- 需要回答的开放问题
- 是否需要解释、预测、归因或决策建议

它不负责预先写死最终答案，而是定义分析要解决的问题边界。

### 2.2 Belief

当前对分析对象的假设、判断或不确定认识。

示例：

```text
渠道结构可能影响整体通过率。
```

Belief 是分析上下文，不是所有任务的必需输出。简单取数可以没有 Belief，也不需要强行产生 belief update。

### 2.3 Evidence

由数据、计算和方法产生的可审计观察结果。Evidence 不是一句自然语言，而是一个带有来源和推导过程的对象：

```text
Evidence
  ├── source / dataset / version
  ├── scope / filters / population
  ├── derivation / SQL / code
  ├── methodology
  ├── observed result
  ├── assumptions
  └── limitations
```

Evidence 的目标是让其他人能够回答：

```text
这个结果从哪里来？
使用了哪些数据和范围？
使用了什么计算或方法？
能否复现？
```

### 2.4 Claim

对 Evidence 做出的、范围明确的原子陈述。

示例：

```text
2025 年 6 月整体放款通过率比 5 月下降 4.2 个百分点。
```

Claim 主要回答：

```text
Evidence 允许我们准确地说什么？
```

### 2.5 Warrant

Warrant 是把 Claim 连接到 Inference 的推理规则、模型或适用前提。

示例：

```text
如果整体通过率是各渠道通过率按申请量加权得到的，
且低通过率渠道的权重上升、渠道口径保持稳定，
那么该结构变化会对整体通过率产生向下影响。
```

Warrant 不是 Agent 为目标结论补写的一句理由，而是一个需要：

- 有来源或独立依据
- 有适用条件
- 能产生可观测预测
- 有反证条件
- 可以随 Evidence 变化而修订

的候选关系模型。

### 2.6 Inference

基于：

```text
Prior Belief + Claims + Supported Warrant + Assumptions
```

形成的解释性判断、预测或决策建议。

Inference 必须带有适当强度和限制，例如：

```text
observed
supported
likely
plausible
associational
causal
```

不能把“可能的关联因素”直接表达为“确定的因果原因”。

### 2.7 Warrant Ledger

Warrant 不是静态注册表中的固定规则，而是一个可版本化、可维护的对象。

```text
candidate
  -> supported
  -> weakened
  -> specialized
  -> split
  -> rejected
```

每次更新都应记录：

- Warrant 版本
- 变化类型
- 支持或削弱它的 Evidence
- 新增或移除的假设
- 当前适用范围
- 当前验证状态

## 3. 不同任务的两条路径

### 3.1 事实性取数路径

对于“查一个数”“计算一个指标”“输出一张分组表”等任务，不需要强行生成 Warrant 或 Inference：

```text
Analysis Spec
  -> Evidence Plan
  -> 确定性执行
  -> Evidence Soundness
  -> Claim Sufficiency
  -> 输出 Claim
```

例如：

```text
Evidence：2025 年 6 月销售额合计为 1.25 亿元。
Claim：2025 年 6 月销售额为 1.25 亿元。
```

### 3.2 解释性分析路径

对于“为什么”“可能原因”“是否有效”“是否建议采用”等任务，进入 Warrant Loop：

```text
Analysis Spec
  -> 初始 Belief / 开放问题
  -> Candidate Warrant Space
  -> Evidence Actions
  -> Evidence
  -> Claims
  -> Warrant 更新
  -> Inference
  -> Critic / Domain / Human 审阅
```
## 4. Agent 角色设计

推荐保留三个逻辑 Agent，加一个按风险启用的人类 Gate。

### 4.1 Analyst Agent

Analyst 是主分析推进者，负责：

- 解析 Analysis Spec
- 初始化 Belief State
- 生成 Candidate Warrant Space
- 为候选 Warrant 提出预测、反证条件和 Evidence Requirements
- 形成 Atomic Claims
- 生成 Candidate Inference
- 根据 Critic 和 Domain 反馈修订分析

Analyst 不负责单方面宣布 Warrant 已经成立、Inference 已经被证明或分析可以结束。

### 4.2 Domain Agent

Domain Agent 是可插拔的业务和方法约束层，不需要每个任务都启用。

**分析前：**

- 检查指标口径
- 补充业务机制和领域假设
- 判断方法是否适用
- 指出不允许的推理方式

**Inference 形成后：**

- 检查结论是否符合业务语义
- 检查因果、关联、预测表述是否越界
- 提供领域替代解释
- 要求降低结论强度或增加限制

Domain Agent 不负责替代 Analyst，也不负责独立执行全部数据分析。

### 4.3 Critic Agent

Critic 是过程中的证据链和 Warrant 审计者，同时承担原先独立 Reviewer 的主要职责：

- 挑战 Candidate Warrant
- 检查 Warrant 是否只是目标结论的重述
- 生成可观测预测和反证条件
- 选择最能区分候选 Warrant 的 Evidence Action
- 检查 Evidence Soundness
- 检查 Evidence -> Claim 是否充分
- 更新 Warrant Ledger
- 检查 Claim + Warrant -> Inference
- 发现过度推断、循环论证和缺失假设
- 决定继续、修订、转人工或接受

Critic 参与过程，而不是只在最后打分。

### 4.4 Human Gate

人不需要参与每一轮普通分析，但应在以下情况介入：

- 高风险因果或经营结论
- 新 Warrant 需要长期沉淀
- Warrant Space 无法收敛
- 多个解释均无法被当前数据区分
- 需要对外发布、执行策略或发布模型

Human 的职责是最终业务责任和长期知识维护，不是替代所有自动化验证。

## 5. 从需求到 Inference 的完整流程

```mermaid
flowchart TD
    A[用户提交具体分析需求]

    subgraph ANALYST[Analyst Agent]
        B[解析 Analysis Spec]
        B1[明确对象、范围、目标和输出]
        B2[读取 Schema、上下文和已有 Beliefs]
        C[初始化 Belief State]
        D[生成 Candidate Warrant Space]
        E[形成 Evidence Requirements]
        J[从 Evidence 形成 Atomic Claims]
        O[基于 Claims 和 Supported Warrants 生成 Candidate Inference]
        R[根据反馈修订分析]
    end

    subgraph DOMAIN[Domain Agent]
        F[检查指标口径与业务语义]
        F1[补充领域机制和方法假设]
        F2[检查方法适用条件]
        P[审查 Candidate Inference]
        P1[检查结论强度与领域风险]
    end

    subgraph CRITIC[Critic Agent]
        G[审查 Candidate Warrants]
        G1[生成预测与反证条件]
        H[选择最能区分 Warrants 的 Evidence Action]
        I[Evidence Soundness Test]
        K[Claim Sufficiency Test]
        L[更新 Warrant Ledger]
        M{是否存在足够支持的 Warrant}
        Q[审查最终论证链]
        S{是否接受当前 Inference}
    end

    subgraph TOOLS[Deterministic Tool Layer]
        T[执行 Evidence Action]
        T1[SQL / pandas / DuckDB]
        T2[统计、实验和数据质量检查]
        T3[生成 Evidence Package]
    end

    subgraph HUMAN[Human Gate]
        U[高风险或长期维护 Review]
        U1[接受 / 修改 / 补证据 / 拒绝]
    end

    A --> B --> B1 --> B2 --> C --> D
    D --> F
    F --> F1 --> F2 --> G
    G --> G1 --> E --> H
    H --> T --> T1 --> T3
    T --> T2 --> T3
    T3 --> I

    I -->|不通过| R
    I -->|通过| J
    J --> K
    K -->|Evidence 不足或 Claim 过强| H
    K -->|通过| L
    L --> M

    M -->|继续寻找区分证据| H
    M -->|无足够证据| N[输出 Inconclusive / 请求人工判断]
    M -->|存在支持的 Warrant| O

    O --> P --> P1 --> Q
    Q --> S
    S -->|需要补证据| H
    S -->|需要修改推理| O
    S -->|需要人工或长期维护| U
    S -->|普通任务可接受| V[输出最终 Inference]
    U --> U1
    U1 -->|接受| V
    U1 -->|修改或补证据| R
    U1 -->|拒绝| N
    R --> D
```

## 6. Warrant 的自主生产和维护

### 6.1 不从目标结论反向编 Warrant

不允许采用这种流程：

```text
Claim + Target Inference
  -> Agent 反向生成一个能解释结论的 Warrant
```

这会导致事后合理化。

如果用户已经提出一个结论，它应当被标记为：

```text
Hypothesis / Candidate Inference
```

而不是直接作为最终 Inference。

### 6.2 先生成 Candidate Warrant Space

Agent 不选择一个唯一 Warrant，而是生成多个候选关系：

```text
W1：渠道结构变化
W2：渠道内部表现变化
W3：用户结构变化
W4：数据质量或指标口径变化
```

每个候选 Warrant 必须包含：

- statement
- assumptions
- predictions
- disconfirming conditions
- required evidence
- current status

### 6.3 选择区分性 Evidence Action

Agent 的下一步不是“继续做一个看起来有用的分析”，而是选择最能区分候选 Warrant 的分析动作：

```text
W1 / W2 / W3 / W4
  -> 生成各自预测
  -> 找到最能区分它们的 Evidence Action
  -> 执行
  -> 更新 Warrant 状态
```

### 6.4 发现与验证分离

探索阶段允许 Agent 根据已有 Evidence 提出新的 Candidate Warrant，但该 Warrant 不能直接用同一批 Evidence 证明自己。

```text
Discovery Evidence
  -> Candidate Warrant
  -> Predictions
  -> Validation Evidence
  -> Warrant 状态更新
```

当无法使用新的数据时，至少需要明确标记：

```text
post_hoc
hypothesized
unverified
```

并限制最终 Inference 的强度。

### 6.5 Warrant Ledger 不是人工静态注册表

系统不需要人工提前登记所有业务 Warrant。人工主要提供基础能力和高风险维护：

- 指标定义
- 基础分析操作
- 方法约束
- 业务领域上下文
- 高风险知识审核

具体任务中的 Warrant 由 Agent 自主组合和维护，验证后可以选择沉淀到长期知识库。
## 7. 最小可复用测试内核

不按“趋势分析、因果分析、实验分析、建模分析”等任务类型拆出大量测试体系，而是保留以下通用内核。

### Test A：Evidence Soundness

```text
Evidence 的来源、范围、计算和方法是否 sound、correct、可复现？
```

### Test B：Claim Sufficiency

```text
Evidence 是否足以支持 Claim？
Claim 是否超出了 Evidence 的范围、粒度和语义？
```

### Test C：Inference Warrant

```text
Prior Belief + Claim + Warrant + Assumptions
是否足以支持 Inference？
Inference 是否超出了 Warrant 的强度？
```

### Test D：Traceability

```text
每个 Claim 是否引用 Evidence？
每个 Inference 是否引用 Belief、Claim、Warrant 和 Assumptions？
```

测试结果不应只有 `pass/fail`，建议使用：

```text
supported
partially_supported
unsupported
inconclusive
```

## 8. 当前项目映射

当前实现已经具备一部分基础，但还没有完整落地上述论证图。

### 8.1 已有能力

| 目标能力 | 当前实现 |
|---|---|
| 文件与 Schema 输入 | `backend/profiler/schema_profiler.py` |
| 结构化分析计划 | `backend/schemas/plan.py:157` |
| Skill-native Plan 兼容 | `backend/planning/adapters.py:189` |
| 计划完整性 Review | `backend/routers/tasks.py:217` |
| 计划修改 | `backend/routers/tasks.py:689` |
| 执行前 Gate | `backend/planning/run_guard.py:10` |
| 确定性数据执行 | `backend/execution/engine.py:13` |
| 任务状态和 Review | `backend/schemas/task.py:17` |
| 运行快照和事件 | `backend/observability.py:22` |
| Codex Provider | `backend/codex/factory.py:21` |

### 8.2 当前缺口

当前 `AnalysisPlan` 和 `ResultPayload` 主要表达：

```text
怎么执行
执行出了什么结果
```

还没有正式表达：

```text
Evidence 对象
Atomic Claim
Candidate Warrant
Warrant Ledger
Inference
Claim / Warrant / Inference 的审计结果
```

此外，当前的 `completeness` 主要表示：

```text
Plan 是否准备好执行
```

而不是：

```text
结果是否足以支持最终 Inference
```

因此后续不要继续把所有推理字段都塞入 `AnalysisPlan`，建议在执行结果外增加独立的分析论证对象。

## 9. 建议的目标对象

后续可以新增以下内部对象，不要求第一阶段立即暴露为公开 API。

```text
AnalysisArgumentGraph
  ├── analysis_spec
  ├── belief_state
  ├── evidence_items
  ├── claims
  ├── warrant_versions
  ├── inferences
  ├── assumptions
  ├── alternatives
  └── review_verdict
```

推荐的内部模型：

```text
EvidenceItem
  - evidence_id
  - source_refs
  - scope
  - derivation
  - methodology
  - observed_result
  - assumptions
  - limitations

Claim
  - claim_id
  - statement
  - evidence_refs
  - scope
  - claim_strength

WarrantVersion
  - warrant_id
  - version
  - statement
  - assumptions
  - predictions
  - disconfirming_conditions
  - evidence_refs
  - status

Inference
  - inference_id
  - statement
  - prior_belief_refs
  - claim_refs
  - warrant_refs
  - limitations
  - strength
```

## 10. MVP 迭代建议

### P0：保留当前主链，增加论证产物

目标：不改变现有用户流程和执行能力。

建议：

1. 保留当前 `AnalysisPlan -> run_plan -> ResultPayload` 主链。
2. 在执行后生成结构化 `EvidenceItem`，不要只保存表格和自然语言摘要。
3. 将摘要中的事实性句子拆成 Atomic Claims。
4. 为每个 Claim 保存 Evidence 引用。
5. 暂时只实现 Evidence Soundness 和 Claim Sufficiency。

### P1：增加 Critic Loop

目标：让系统能够发现证据不足和结论过强。

建议：

1. 增加 Candidate Warrant 输出格式。
2. 为 Warrant 强制生成 predictions 和 falsifiers。
3. 增加 Critic Agent 节点。
4. 当 Claim 不被支持时，允许收窄 Claim 或补充 Evidence。
5. 记录 `supported / partially_supported / unsupported / inconclusive`。

### P2：增加 Warrant Ledger 和 Domain Agent

目标：让复杂分析能够维护多个候选解释。

建议：

1. 用版本化 Ledger 保存 Warrant。
2. 支持 strengthen、weaken、specialize、split、reject。
3. 对因果、实验、评分卡等高风险任务启用 Domain Agent。
4. Domain Agent 负责领域语义和方法边界，不替代 Critic。
5. 将高价值、人工确认过的 Warrant 沉淀到知识库。

### P3：迁移到 LangChain / LangGraph 或其他纯 API Runtime

目标：去除对 Codex Runtime 的依赖，同时保留业务架构。

建议映射：

```text
LegacyCodexProvider
  -> LLM API / LangChain ChatModel

AnalysisPlan / TaskRecord
  -> LangGraph State

pending_review
  -> interrupt / checkpoint / human resume

Warrant Proposer / Critic / Domain
  -> LangGraph nodes 或 subgraphs

execution.engine.py
  -> 保留为确定性工具节点

artifacts / events.log
  -> 保留为证据和审计存储
```

不要在 P0 阶段直接把整个项目改成一个自由调用工具的超级 Agent。
## 11. 设计原则

### 原则一：流程节点不等于 Agent

执行、解析、验证、保存、生成图表都可以是确定性节点，不应为了“Agent 化”而强行交给 LLM。

### 原则二：Warrant 不能是事后理由

Warrant 必须带有预测、反证条件和证据来源。不能只因为它能解释当前结果，就认为它成立。

### 原则三：Discovery 和 Justification 分离

Agent 可以探索和提出候选解释，但候选 Warrant 需要新的 Evidence 或独立方法验证。

### 原则四：结论强度不能超过 Warrant 强度

如果 Warrant 只支持关联性，Inference 就不能写成确定因果。

### 原则五：支持多个候选解释

在证据无法区分时，输出 `inconclusive` 或保留多个候选解释，不要强行选择一个故事。

### 原则六：所有重要结论都要可回溯

最终 Inference 必须能够回溯到：

```text
Prior Belief
  -> Claims
  -> Evidence
  -> Warrant
  -> Assumptions
```

### 原则七：高风险结论保留人工责任

自动化系统可以提高分析效率，但不应自动承担重大因果、经营和风控决策的最终责任。

## 12. 非目标

当前 MVP 不追求：

- 为所有分析类型预先设计完整测试树
- 让 Agent 自由执行任意 shell 或 Python
- 让 Agent 自动把所有 Warrant 写入长期知识库
- 用一个分数概括“分析质量”
- 证明现实世界中的绝对因果真理
- 为每个流程节点都创建独立 Agent

当前最重要的目标是：

```text
让分析过程产生结构化、可追溯、可审阅的 Evidence / Claim / Warrant / Inference 链。
```
