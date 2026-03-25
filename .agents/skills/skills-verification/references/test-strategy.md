# Test Strategy

This file indexes the test-strategy guidance already described in `SKILL.md`.

## 1) Detect the target skill profile

Infer the skill type from its `SKILL.md`, scripts, references, filenames, and examples.

## 2) Fixture and mock resolution order

When runtime or contract testing is requested, obtain test inputs in this order:

### First choice: skill-owned fixtures
Use explicit fixtures if they already exist under the target skill, for example:

```text
tests/fixtures/
tests/expected/
examples/
scripts/examples/
```

### Second choice: example-backed fixtures
If the skill references concrete sample files in `SKILL.md`, `scripts/`, or `references/`, use those.

### Third choice: auto-generated fixtures
If the skill does not provide fixtures, synthesize the smallest valid fixtures possible from the declared contract.

This fallback is a core capability of this verification skill.

## 3) Auto-generation policy

When generating fixtures automatically, prefer **minimal, interpretable, deterministic** samples.

### CSV / DataFrame fixture
Use a small mixed-type table, for example:

```text
id,target,feature_num,feature_cat,event_date
1,1,10,A,2026-01-01
2,0,20,B,2026-01-02
3,1,15,A,2026-01-03
4,0,30,C,2026-01-04
```

### SQL fixture
Use a tiny valid query or DDL+DML sample matching the skill's domain.

Example:

```sql
select 1 as id, 'A' as segment, 100 as amount
union all
select 2 as id, 'B' as segment, 200 as amount;
```

### DuckDB fixture
Create a minimal local DuckDB database with 1-2 small tables and simple schemas.

### Excel fixture
Generate a workbook with:
- one data sheet
- stable headers
- a small rectangular dataset

### Scorecard / binary classification fixture
Generate a small dataset with:
- binary `target`
- numeric features
- categorical features
- a few missing values
- enough class variation to avoid degenerate behavior

### API / external-system fixture
Prefer one of:
- mock response files
- stub client
- fake local endpoint
- dry-run mode

If none are possible, explicitly report that integration testing is blocked by the target skill design.

## 4) Negative fixtures

When feasible, generate at least one intentionally invalid fixture.

Examples:
- missing required column
- wrong file extension
- empty dataset
- all-one-class target
- invalid SQL
- invalid output path
- illegal table name

The goal is to verify that the skill fails in a controlled, interpretable way.
