---
name: sql-generator
description: Generate a single runnable ODPS SQL script from a business request, with a stable output contract that can be handed directly to the dataworks skill for execution.
---

## Watermark

- Every time this skill is used, overwrite `water.json` in this skill directory.
- Use `../_common/scripts/write_watermark.py` to write the file.
- Required JSON shape:
  - `skill`: `sql-generator`
  - `version`: watermark version, default `v1`
  - `input_files`: input file names/paths used for this run, or `[]`
  - `actions`: concise completed actions for this run
- Include generated `.sql` file names in `actions` or `input_files` when available.
- Do this before the final answer for the skill, and overwrite rather than append.

# SQL Generator

## Purpose

This skill turns a business request into a single runnable ODPS SQL script.

It owns:

1. business-intent classification
2. metric and grain selection
3. source-table and join-path selection from local references
4. SQL generation in a format that downstream execution skills can consume directly

It does **not** own:

- SQL execution
- Excel export
- DuckDB persistence
- multi-file SQL orchestration
- post-execution validation against live ODPS data

The core value of this skill is not generic SQL writing. The core value is choosing the correct business context first, then producing SQL that is usable without manual restructuring.

## Primary downstream consumer

This skill is designed to feed `.agents/skills/dataworks/SKILL.md`.

That means the default output from this skill must be stable enough to:

1. save as one `.sql` file
2. pass as `file_path` into the `dataworks` skill
3. execute without the downstream skill having to infer missing structure

If the generated result cannot be saved as one SQL file and executed as-is, the output contract has not been met.

## Directory index

```text
.
├── SKILL.md
└── references/
    ├── business_overview.md
    ├── business_requirements_patterns.md
    ├── business_theme_existing_customer.md
    ├── business_theme_monitoring.md
    ├── business_theme_new_customer.md
    ├── relations.md
    ├── tables.md
    ├── prompts/
    │   ├── relation_extraction.md
    │   └── table_extraction.md
    └── sql代码/
```

## When to use

Use this skill when the user asks for:

- a SQL script from a business request
- a monitoring / dashboard SQL
- a funnel / conversion SQL
- a monthly review / weekly review SQL
- a strategy-evaluation SQL
- a commercial-revenue SQL
- a SQL rewrite that should follow the local corpus style

Use this skill especially when the request depends on:

- picking the correct business口径
- reusing local business labels and metrics
- choosing the right physical tables
- following the house style of the ODPS corpus

## When not to use

Do **not** use this skill as the primary tool when the task is:

- "run this SQL file"
- "export SQL result to Excel"
- "cache SQL result into DuckDB"
- "fix an ODPS credential problem"
- "debug a runtime SQL error from a specific execution job"

Those are downstream execution tasks and belong to `dataworks`.

## Inputs

### Required

- `business_request`
  - natural-language description of what the user wants to measure, report, or analyze

### Optional

- `bizdate`
  - one business date placeholder or concrete date
- `date_range`
  - explicit start/end dates if the request is windowed
- `date_grain`
  - `day`, `week`, `month`, or another explicit grain
- `required_dimensions`
  - dimensions that must appear in the result
- `required_metrics`
  - metrics that must appear in the result
- `filters`
  - business filters the user explicitly requires
- `output_table_name`
  - target table if the user wants a materialized table
- `output_mode`
  - `query_only`, `create_table_as`, or `insert_overwrite`
- `reference_hint`
  - file or topic hint if the user points to a known SQL example

### Implicit local context

This skill is allowed to use:

- `references/business_overview.md`
- `references/business_requirements_patterns.md`
- `references/business_theme_monitoring.md`
- `references/business_theme_new_customer.md`
- `references/business_theme_existing_customer.md`
- `references/tables.md`
- `references/relations.md`
- `references/sql代码/`

## Outputs

### Required output contract

The final deliverable must contain:

1. `sql_file_name`
2. `sql_file_content`
3. `output_mode`
4. `assumptions`
5. `required_placeholders`
6. `execution_notes`

### Output semantics

#### `sql_file_name`

- one suggested file name ending in `.sql`
- stable and descriptive
- suitable for handing to `dataworks`

#### `sql_file_content`

- one complete SQL script
- ODPS-compatible style
- can be saved directly as a single `.sql` file
- must not rely on hidden conversational context
- must not be split across multiple independent files

#### `output_mode`

One of:

- `query_only`
- `create_table_as`
- `insert_overwrite`

Default rule:

- if the user does not explicitly ask for a target table, prefer `query_only`
- only emit `create_table_as` or `insert_overwrite` when the request or reference corpus clearly requires materialization

#### `assumptions`

- brief list of business assumptions chosen by the generator
- must include grain and main口径 when these were not explicit

#### `required_placeholders`

- list placeholders used in the SQL, for example `${bizdate}`
- empty list if none are used

#### `execution_notes`

- only execution-relevant notes
- examples:
  - expected partition behavior
  - whether `MAX_PT(...)` is required
  - target table expectation
  - whether the SQL is read-only

### Important formatting requirement

The SQL itself must be easy for a downstream skill to extract cleanly.

Preferred format:

1. one short metadata section
2. one fenced `sql` block containing only SQL

Do not mix explanatory prose into the SQL block.

## Success criteria

This skill succeeds only if:

- the business request is mapped to the correct theme or nearest valid theme
- the generated SQL has a clear grain
- the SQL uses plausible source tables from local references
- joins are explicit enough to be credible
- partition/date logic is present where needed
- the output can be saved as one `.sql` file
- the output is usable by `dataworks` without manual cleanup

## Failure behavior

If the request is underspecified or risky, the skill should fail in a controlled way.

Expected failure classes:

- unclear business口径
- missing required metric definition
- missing date scope when date logic materially changes the SQL
- no credible source tables found in local references
- request implicitly needs multiple scripts instead of one

When failing:

- do not fabricate a confident SQL script
- state the blocking ambiguity explicitly
- if possible, provide a minimal template SQL plus the missing assumptions

## Minimal runnable path

The minimum valid path for this skill is:

1. receive `business_request`
2. classify it into one business theme
3. inspect the nearest local references
4. generate one SQL script
5. return:
   - `sql_file_name`
   - `sql_file_content`
   - `output_mode`
   - `assumptions`
   - `required_placeholders`
   - `execution_notes`
6. save that script as a local `.sql` file
7. hand the file path to `dataworks`

If a verifier cannot construct this path, the skill is under-specified.

## Business themes

The local corpus falls into three themes. Always classify the request before generating SQL.

### 1. Monitoring and approval tracking

Typical files:

- `ads_inloan_loan_monitor_screen_df.sql`
- `ads_inloan_loan_pass_monitor_df.sql`
- `dws_inloan_loan_channel_stat_df.sql`
- `dws_inloan_loan_pass_stat_df.sql`
- `dws_inloan_loan_risk_stat_df.sql`
- `ads_inloan_loan_balance_mthly_df.sql`

Typical intents:

- daily monitoring
- month-to-date completion
- approval pass rate
- funding pass rate
- balance and on-book tracking

### 2. New-customer conversion and credit operations

Typical files:

- `APP新客转化-授信口径.ipynb`
- `APP新客转化-注册口径.ipynb`
- `授信口径转化率_虚假给额.ipynb`

Typical intents:

- registration-to-credit funnel
- credit-to-loan funnel
- channel conversion
- fake-credit-line analysis
- credit segmentation

### 3. Existing-customer operations, reloan analysis, and commercial revenue

Typical files:

- `老客月会sql代码.ipynb`
- `xyf_jingying.weekly_analysis_report_df_lss.txt`
- `xyf_jingying.weekly_analysis_report_vip_dynamic_income_lss.txt`

Typical intents:

- monthly review
- reloan analysis
- vintage / MOB analysis
- card-product revenue
- customer-pool analysis

## Business request patterns

### Monitoring dashboard

Typical language:

- today's loan status
- month completion
- pass rate
- balance monitoring

Primary references:

- `references/business_theme_monitoring.md`

### Funnel conversion

Typical language:

- registration to credit
- credit to withdrawal
- withdrawal to loan
- channel conversion

Primary references:

- `references/business_theme_new_customer.md`

### Strategy evaluation

Typical language:

- fake credit line impact
- extra release impact
- API-to-APP pullback effect
- pricing-band effect

Primary references:

- `references/business_requirements_patterns.md`
- `references/business_theme_new_customer.md`
- `references/business_theme_existing_customer.md`

### Monthly or weekly business review

Typical language:

- monthly review
- weekly report
- special-topic analysis

Primary references:

- `references/business_theme_existing_customer.md`

### Commercial revenue

Typical language:

- member-card revenue
- refund and net revenue
- T0/T7/T30/T60 cumulative income

Primary references:

- `references/business_theme_existing_customer.md`

## Reference usage order

Use references in this order:

1. `references/business_overview.md`
   - classify the request
2. business-theme documents
   - choose metrics, grain, and typical cuts
3. `references/business_requirements_patterns.md`
   - map loose business language to SQL pattern
4. `references/tables.md`
   - choose physical tables and repeated fields
5. `references/relations.md`
   - choose credible join paths
6. `references/sql代码/`
   - borrow stable query shapes, filters, labels, and date logic

## SQL generation rules

When generating SQL:

- prefer ODPS-style SQL used in the local corpus
- preserve local naming and result-shape conventions where possible
- use explicit partitions or date filters when the table appears partitioned
- use `MAX_PT(...)` only when it fits the referenced table pattern
- keep result grain explicit
- avoid inventing business labels not supported by the corpus or user request
- do not silently switch business口径
- prefer the simplest runnable script that meets the request

## Downstream compatibility rules

Because `dataworks` executes a single SQL file, this skill must default to the following compatibility contract:

- one business request produces one SQL script
- the SQL script can be saved directly to disk
- no hidden preprocessing step is required
- no multiple-file dependency chain is required
- no markdown-only pseudo-SQL is acceptable as final output

If the request naturally expands into multiple SQL scripts, the skill should:

1. say that the task exceeds the default single-file contract
2. either reduce scope to one runnable script
3. or explicitly label the result as a multi-script plan instead of pretending it is directly executable

## Dependency boundary

This skill is intentionally offline and reference-driven.

It depends on:

- local markdown references
- local SQL examples
- local extracted table and relation context

It does **not** depend on:

- ODPS credentials
- live database access
- network access
- file execution privileges

That makes the skill suitable for deterministic authoring and contract testing.

## Minimal check before finalizing

Before returning the result, verify:

- the SQL is one coherent script
- table names are plausible in local references
- joins are explicit
- date or partition logic is not missing
- output mode is stated
- placeholders are listed
- assumptions are short and concrete

## Failure modes to surface clearly

Call out these failure modes explicitly when they occur:

- wrong theme classification
- wrong grain
- wrong date window
- wrong source-table family
- overfitting to a highly specific example SQL
- returning advisory SQL text that cannot be executed directly

## Minimal operating principle

This skill should behave as:

- first a business-demand router
- then a SQL composer
- finally a single-file SQL supplier for `dataworks`

If forced to choose, prioritize downstream executability over stylistic flourish.
