# Analysis Planning Loop

This file defines how `analysis-planner` should handle vague user requests through clarification and plan updates.

## Core idea

The skill should not assume the first user message is complete.

A real planning skill must be able to:

1. form an initial draft plan from incomplete intent
2. detect what is still underspecified
3. ask the user only for the missing information that matters
4. update the same plan object
5. stop asking once the plan is minimally complete
6. ask the user to review the plan

## Planning states

Use this mental state machine.

### `draft`

- the first best-effort plan exists
- ambiguities are known but not yet resolved

### `needs_clarification`

- one or more material planning gaps remain
- follow-up questions are justified

### `minimally_completed`

- the plan is coherent enough to implement or translate downstream
- some recommended or optional fields may still be empty
- remaining ambiguity is not critical to the core analytical contract

### `reviewed`

- the user has confirmed, adjusted, or explicitly accepted the plan

## What counts as a material gap

Ask the user if any of the following are still unclear and cannot be safely inferred:

- what KPI or metric should actually be analyzed
- what entity or population is in scope
- what answer grain is expected
- what time window matters
- what comparison is the main comparison
- what output form the user wants first

Do not ask just because:

- a recommended field is still empty
- the title can be improved
- a chart type is not decisive
- an optional comparison or segment is merely nice to have

## Minimal-completion rule

A plan is `minimally_completed` when all of the following are true:

1. `goal.question` is specific enough to restate the actual ask
2. `scope.population` is clear enough to know which rows/entities are included
3. `analysis_type` is selected
4. `grain.answer_unit` is selected
5. `metrics` contains at least one credible metric mapped to schema-backed columns or clearly identified placeholders needing confirmation
6. `methods` contains at least one executable step
7. `validation.coverage_checks` explains whether the schema supports the ask
8. `output.table_fields` defines what the downstream consumer should inspect first
9. remaining `ambiguities` do not block implementation of the core analysis path

If any of these conditions fail, the plan is not minimally complete.

## Question-asking policy

When asking follow-up questions:

- ask the fewest questions that can unlock the plan
- prefer bundled questions when they resolve one planning decision cleanly
- avoid speculative or stylistic questions
- ask in user language, not schema jargon, unless the user already speaks that way

Good examples:

- "你更关心销售额、订单数，还是转化率？"
- "这里分析对象是用户、订单，还是门店？"
- "你希望看最近 30 天、自然月，还是某个固定时间段？"

Bad examples:

- "你想要柱状图还是折线图？" when the metric itself is still unknown
- "要不要顺便加 cohort?" when no core plan exists yet

## Plan update rule

After every user answer:

1. update the existing plan object
2. reduce or remove resolved ambiguities
3. revise dependent fields such as `methods`, `validation`, and `output`
4. recompute whether the plan is minimally complete

Do not discard the plan and rebuild from scratch unless the user has changed the problem itself.

## Review handoff

Once the plan is minimally complete:

1. stop asking clarification questions
2. present the current plan as the working draft
3. ask the user to review or confirm it
4. move to `reviewed` only after explicit user confirmation or concrete revision feedback

This matters because "minimally complete" is not the same as "accepted by the user".

## Design principle

The skill should optimize for:

- enough questioning to resolve material ambiguity
- not so much questioning that planning becomes annoying
- a stable evolving plan object rather than disconnected one-off answers
