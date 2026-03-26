---
name: analysis-planner
description: Create a testable AnalysisPlan JSON from a business question and schema profile for tabular data analysis tasks.
---

## Watermark

- Every time this skill is used, overwrite `water.json` in this skill directory.
- Use `../_common/scripts/write_watermark.py` to write the file.
- Required JSON shape:
  - `skill`: `analysis-planner`
  - `version`: watermark version, default `v1`
  - `input_files`: input file names/paths used for this run, or `[]`
  - `actions`: concise completed actions for this run
- Do this before the final answer for the skill, and overwrite rather than append.

# Analysis Planner

## Purpose

Turn a user question plus a schema profile into one structured `AnalysisPlan` JSON object that an agent can inspect, revise, translate into SQL, or execute as downstream analysis work.

This skill is iterative by design. It should:

1. draft an initial plan from incomplete intent
2. identify material gaps
3. ask focused follow-up questions
4. update the plan with user answers
5. stop asking once the plan is minimally complete
6. ask the user to review the resulting plan before downstream execution

This skill owns:

1. normalizing analytical intent
2. choosing the main analysis type
3. defining the answer grain and required metrics
4. capturing filters, dimensions, time framing, and comparisons
5. making assumptions and ambiguities explicit
6. deciding whether more user clarification is needed
7. returning a plan that is specific enough to validate and reuse
8. asking for user review once the plan is minimally complete

This skill does **not** own:

- running SQL
- drawing charts
- querying databases
- inventing missing business columns
- silently resolving material ambiguities

## Directory index

```text
.
+-- SKILL.md
+-- references/
|   +-- analysis-plan-elements.md
|   +-- analysis-planning-loop.md
|   +-- backend-plan-consumption.md
|   `-- analysis-plan-schema.json
+-- scripts/
|   `-- validate_analysis_plan.py
`-- tests/
    +-- fixtures/
    |   +-- ambiguous_request.json
    |   `-- minimal_request.json
    `-- expected/
        +-- invalid_missing_required.json
        `-- minimal_valid_plan.json
```

## When to use

Use this skill when the user asks for:

- a best-effort decomposition of a vague analytical request into executable parts
- an analysis plan before implementation
- help turning a fuzzy analytical idea into a precise, reviewable plan
- a structured plan from a business question and schema
- a planning artifact for SQL generation, dashboard design, or notebook analysis

## When not to use

Do **not** use this skill as the main tool when the task is:

- "run this analysis now"
- "write the SQL directly"
- "explain the insight in plain prose only"
- "revise an existing AnalysisPlan"

Use `plan-reviser` for plan revision and execution-oriented skills for runtime work.

## Inputs

### Required

- `user_question`
  - natural-language analysis request
- `schema_profile`
  - table/schema metadata that includes:
    - `columns`
    - `row_count` when known
    - `dtypes` or per-column types

### Optional

- `business_context`
  - domain hints, KPI definitions, or reporting context
- `analysis_preferences`
  - preferred chart type, ranking rule, comparison style, or deliverable format
- `known_constraints`
  - mandated filters, date windows, excluded populations, or governance rules
- `user_answers`
  - answers collected through clarification questions in previous turns

## Interaction contract

This skill should support a multi-turn planning loop.

### Step 1. Draft an initial plan

- build the best possible `AnalysisPlan` from the current request and schema
- mark unresolved items in `ambiguities`
- estimate whether the plan is already minimally complete

### Step 2. Decide whether clarification is necessary

Ask follow-up questions only when the missing information would materially change:

- the target metric
- the answer grain
- the population in scope
- the time window
- the key comparison
- the intended output

Do not ask for details that are merely nice to have.

### Step 3. Ask focused questions

When clarification is needed:

- ask the minimum number of high-value questions
- prefer questions that resolve multiple plan gaps at once
- update the plan after each answer or answer batch
- avoid reopening already-resolved parts of the plan

### Step 4. Re-check minimal completeness

After incorporating user answers, decide whether the plan has reached `minimally_completed`.

The decision rule is defined in `references/analysis-planning-loop.md`.

### Step 5. Ask for review

Once the plan is minimally complete:

- stop asking clarification questions
- present the latest plan
- explicitly ask the user to review or confirm it before downstream execution or SQL generation

## Output

### Required output contract

Return exactly one JSON object and no surrounding prose.

The object must preserve this top-level shape:

1. `goal`
2. `scope`
3. `analysis_type`
4. `grain`
5. `metrics`
6. `dimensions`
7. `filters`
8. `segments`
9. `time`
10. `derived_fields`
11. `comparisons`
12. `methods`
13. `validation`
14. `output`
15. `ambiguities`
16. `confidence`

### Requested-level policy

The skill should treat plan elements with three request levels:

- `required`
  - must be populated when inferable; if truly unknown, keep the field and record the gap in `ambiguities`
- `recommended`
  - should be populated when supported by the question or schema; omission is allowed if not inferable
- `optional`
  - include only when the request genuinely needs it

The canonical element matrix lives in `references/analysis-plan-elements.md`.

### Minimal-completion policy

A plan can be:

- `needs_clarification`
  - important fields are still unresolved and follow-up questions are justified
- `minimally_completed`
  - the plan is coherent enough for user review and downstream implementation
- `reviewed`
  - the user has reviewed or confirmed the plan

Minimal completion does not require every recommended or optional field to be filled.
It does require the plan to be implementable without making hidden assumptions about the core analytical contract.

### Allowed enums

- `aggregation`: `sum`, `mean`, `count`, `max`, `min`, `median`
- `operator`: `eq`, `neq`, `gt`, `gte`, `lt`, `lte`, `in`, `not_in`, `contains`
- `role`: `time`, `category`, `geo`
- `chart_type`: `line`, `bar`, `histogram`, `table`
- `analysis_type`: `descriptive`, `diagnostic`, `trend`, `comparison`, `distribution`, `segmentation`, `ranking`
- `method.type`: `aggregate`, `timeseries`, `top_n`, `distribution`, `group_compare`, `period_compare`
- `null_policy`: `include`, `exclude`, `separate_bucket`

## AnalysisPlan semantics

Use these rules when constructing the object:

- `goal`
  - why the analysis exists and what decision it supports
- `scope`
  - which business population is in scope and what assumptions were made
- `analysis_type`
  - dominant analytical intent, even if the request mixes multiple intents
- `grain`
  - the unit and final aggregation level of the answer
- `metrics`
  - numeric outcomes to compute
- `dimensions`
  - useful breakdown fields for the metrics
- `filters`
  - hard row-level inclusion constraints
- `segments`
  - subgrouping ideas or cohorts worth comparing
- `time`
  - time column, period window, and comparison window handling
- `derived_fields`
  - computed fields required before analysis
- `comparisons`
  - explicit A vs B, before vs after, or benchmark comparisons
- `methods`
  - concrete analysis operations to run in sequence
- `validation`
  - checks that make the analysis trustworthy
- `output`
  - expected table/chart presentation contract
- `ambiguities`
  - unresolved gaps, definition risks, or unsupported asks
- `confidence`
  - numeric estimate from `0` to `1`

For exact element-level requirements, read `references/analysis-plan-elements.md`.
For the interactive completion loop, read `references/analysis-planning-loop.md`.
For backend-side consumption guidance, read `references/backend-plan-consumption.md`.

## Success criteria

This skill succeeds only if:

- the output is one valid `AnalysisPlan` JSON object
- all top-level plan elements are present
- required elements are substantively populated
- all referenced columns exist in `schema_profile`
- missing business logic is surfaced as ambiguity rather than invented
- the plan is specific enough for a downstream agent to implement
- the skill asks clarification questions when the plan is not minimally complete
- the skill asks the user for review once the plan becomes minimally complete

## Failure behavior

If the request is incomplete or risky, the skill should still return a best-effort plan unless the input is unusable.


Expected failure classes:

- missing or malformed `schema_profile`
- no usable columns
- user question too vague to identify even a dominant analysis type
- requested metric cannot be mapped to any available column
- conflicting constraints that cannot coexist

When partial failure happens:

- keep the full object shape
- lower `confidence`
- record the missing assumptions in `ambiguities`
- record schema insufficiency in `validation.coverage_checks`

If the plan is still not minimally complete after best-effort drafting:

- do not pretend execution readiness
- ask targeted clarification questions
- update the plan incrementally rather than restarting from scratch

## Minimal runnable path

This skill is documentation-led, but it exposes a contract that can be validated locally.

Minimal smoke path:

```bash
python .agents/skills/analysis-planner/scripts/validate_analysis_plan.py \
  --plan .agents/skills/analysis-planner/tests/expected/minimal_valid_plan.json \
  --schema-profile .agents/skills/analysis-planner/tests/fixtures/minimal_request.json \
  --check-minimally-completed
```

Negative-path check:

```bash
python .agents/skills/analysis-planner/scripts/validate_analysis_plan.py \
  --plan .agents/skills/analysis-planner/tests/expected/invalid_missing_required.json \
  --schema-profile .agents/skills/analysis-planner/tests/fixtures/minimal_request.json
```

Expected behavior:

- the first command exits successfully
- the second command fails clearly and reports the missing required element

## References

- `references/analysis-plan-elements.md`
  - canonical list of plan elements, sub-elements, and their requested levels
- `references/analysis-planning-loop.md`
  - clarification-question policy, minimal-completion decision rule, and review handoff
- `references/backend-plan-consumption.md`
  - how backend services should judge, review, execute, revise, and persist a plan object
- `references/analysis-plan-schema.json`
  - machine-readable contract for top-level shape and common enums

## Scripts

- `scripts/validate_analysis_plan.py`
  - validates a produced plan against the top-level contract, required elements, enums, schema-column references, and minimal-completion criteria

## Boundaries

- Do not invent columns absent from the schema profile.
- Do not return markdown around the JSON object.
- Do not collapse ambiguity into fake certainty.
- Prefer a plan that is executable and reviewable over one that is merely concise.
