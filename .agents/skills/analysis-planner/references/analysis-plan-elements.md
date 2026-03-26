# AnalysisPlan Elements

This file defines what an `AnalysisPlan` is composed of for a data-analysis skill.

The goal is to make the plan usable as an intermediate representation between:

- user intent
- schema-aware reasoning
- downstream execution or revision

## Requested-level semantics

- `required`
  - core to the analytical contract; the field must appear and should be meaningfully populated
- `recommended`
  - strongly useful for downstream execution and review; include whenever the request or schema supports it
- `optional`
  - include only when the analytical question actually needs it

If a `required` element cannot be filled confidently, the planner should:

1. keep the field
2. use the best defensible placeholder value
3. explain the gap in `ambiguities`
4. lower `confidence`

## Top-level element matrix

| Element | Requested level | Why it exists | Minimum expected content |
| --- | --- | --- | --- |
| `goal` | required | anchors the business question | normalized question and intended decision use |
| `scope` | required | states what population is in scope | entity or population plus assumptions |
| `analysis_type` | required | selects the dominant analytical mode | one enum value |
| `grain` | required | defines answer granularity | answer unit or aggregation level |
| `metrics` | required | states what numerical outcomes are measured | at least one metric item |
| `dimensions` | recommended | enables decomposition and slicing | zero or more meaningful breakdowns |
| `filters` | recommended | constrains row inclusion | explicit or inferred row filters |
| `segments` | optional | supports subgroup or cohort analysis | cohort ideas or subgroup lists |
| `time` | recommended | captures period logic for time-aware questions | time column or explicit "not time-based" framing |
| `derived_fields` | optional | records computed inputs required before analysis | named computed fields with source columns |
| `comparisons` | optional | defines comparison intent explicitly | before/after, A/B, benchmark, ranking comparisons |
| `methods` | required | makes the plan executable | ordered analysis operations |
| `validation` | required | makes the plan trustworthy | data quality, coverage, and sanity checks |
| `output` | required | defines what downstream consumers should see | table fields or chart presentation |
| `ambiguities` | required | makes uncertainty explicit | unresolved gaps or unsupported asks |
| `confidence` | required | signals reliability of the plan | numeric 0 to 1 |

## Nested element guidance

### `goal`

| Field | Requested level | Notes |
| --- | --- | --- |
| `question` | required | normalized restatement of user intent |
| `decision_context` | recommended | what decision or judgment the analysis supports |
| `success_criteria` | recommended | what makes the output useful |

### `scope`

| Field | Requested level | Notes |
| --- | --- | --- |
| `entity` | recommended | primary business entity if inferable |
| `population` | required | rows or business population in scope |
| `assumptions` | recommended | scope assumptions inferred from request or schema |

### `grain`

| Field | Requested level | Notes |
| --- | --- | --- |
| `primary_key` | optional | best-effort row or entity key columns |
| `answer_unit` | required | the unit the user will interpret |
| `aggregation_level` | recommended | final reporting grain |

### `metrics[]`

| Field | Requested level | Notes |
| --- | --- | --- |
| `name` | required | stable metric name |
| `column` | required | source column from schema |
| `aggregation` | required | one allowed aggregation enum |
| `definition` | recommended | plain-language metric definition |
| `format` | recommended | `number`, `percentage`, or `currency` |
| `constraints` | optional | denominator caveats or business notes |

### `dimensions[]`

| Field | Requested level | Notes |
| --- | --- | --- |
| `column` | required | source column from schema |
| `role` | recommended | `time`, `category`, or `geo` when clear |
| `label` | recommended | user-facing name |
| `reason` | optional | why the dimension matters analytically |

### `filters[]`

| Field | Requested level | Notes |
| --- | --- | --- |
| `column` | required | source column from schema |
| `operator` | required | one allowed operator enum |
| `value` | required | scalar or list value |
| `required` | recommended | whether it is essential or inferred |

### `segments[]`

| Field | Requested level | Notes |
| --- | --- | --- |
| `name` | recommended | segment label |
| `column` | recommended | source column when segment is schema-backed |
| `definition` | recommended | plain-language subgroup logic |

### `time`

| Field | Requested level | Notes |
| --- | --- | --- |
| `time_column` | recommended | source time column when applicable |
| `grain` | recommended | day, week, month, quarter, year |
| `window` | recommended | explicit or inferred analysis window |
| `comparison_window` | optional | prior period, same period last year, and similar |

### `derived_fields[]`

| Field | Requested level | Notes |
| --- | --- | --- |
| `name` | required | derived field name |
| `expression_logic` | required | plain-language derivation logic |
| `source_columns` | required | schema-backed source column list |

### `comparisons[]`

| Field | Requested level | Notes |
| --- | --- | --- |
| `type` | required | comparison type label |
| `left` | recommended | left comparison side |
| `right` | recommended | right comparison side |
| `metric_names` | recommended | metrics included in the comparison |
| `expected_signal` | optional | what the analyst is looking for |

### `methods[]`

| Field | Requested level | Notes |
| --- | --- | --- |
| `name` | required | step label |
| `type` | required | allowed method enum |
| `inputs` | recommended | columns, metrics, or derived fields used |
| `description` | required | what the step does |

### `validation`

| Field | Requested level | Notes |
| --- | --- | --- |
| `data_quality_checks` | required | nulls, duplicates, invalid values, type mismatches |
| `metric_sanity_checks` | recommended | denominator checks, totals, outliers |
| `coverage_checks` | required | whether schema supports the requested analysis |

### `output`

| Field | Requested level | Notes |
| --- | --- | --- |
| `table_fields` | required | output columns to surface first |
| `chart_type` | recommended | allowed chart enum or `table` |
| `title` | recommended | concise presentation title |
| `sort` | optional | sort instruction |
| `limit` | optional | row limit for rankings or summaries |
| `narrative_focus` | recommended | what should be noticed first |

## Design principle

A good `AnalysisPlan` is not just a list of metrics and charts.

It should expose:

- analytical intent
- data scope
- answer grain
- quantitative measures
- comparison logic
- execution steps
- trust checks
- uncertainty

That is the minimum abstraction needed for a real data-analysis skill.

## Consumer-oriented grouping

When backend systems consume a plan, these elements are useful in three groups.

### Execution-critical

These directly influence computation:

- `metrics`
- `dimensions`
- `filters`
- `output`

### Decision-critical

These determine whether execution is answering the right question:

- `goal`
- `scope`
- `analysis_type`
- `grain`
- `time`
- `comparisons`
- `validation`

### Interaction-critical

These determine what the system should ask, show, or review next:

- `ambiguities`
- `confidence`
- completeness and open-question metadata carried alongside the plan
- `assumptions`

This grouping matters because backend consumers should not treat every field as if it served the same purpose.
