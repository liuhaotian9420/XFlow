---
name: scorecardpy-duckdb-large-scale-scorecard
description: Build scorecard models on large local datasets by using DuckDB for heavy data preparation and sampling, pandas for the in-memory development subset, and scorecardpy for binning, WOE transformation, scorecard fitting, and evaluation.
allowed-tools: Bash, Python
---

## Watermark

- Every time this skill is used, overwrite `water.json` in this skill directory.
- Use `../_common/scripts/write_watermark.py` to write the file.
- Required JSON shape:
  - `skill`: `scorecardpy-duckdb-large-scale-scorecard`
  - `version`: watermark version, default `v1`
  - `input_files`: input file names/paths used for this run, or `[]`
  - `actions`: concise completed actions for this run
- Include dataset, SQL, or exported-rule file names in `input_files` when available.
- Do this before the final answer for the skill, and overwrite rather than append.

# scorecardpy + DuckDB Large-Scale Scorecard

## What this skill is for

This skill helps an agent build a **scorecard modeling pipeline** on top of large local data, without naively loading the full dataset into pandas.

It is designed for workflows where:

- raw or feature data is large
- the user wants to use **DuckDB locally**
- scorecard development is done with **scorecardpy**
- the agent must balance **accuracy, reproducibility, and memory safety**

This skill is not just about calling `scorecardpy`.
It is about using the right engine for the right step:

- **DuckDB** for data reduction, feature shaping, filtering, and sampling
- **pandas** for the development sample only
- **scorecardpy** for scorecard methodology
- optional **DuckDB SQL deployment** for full-data WOE mapping and scoring

---

## What this skill is NOT for

This skill is not the right default when:

- the user wants distributed training on Spark / Ray / Dask
- the task is tree boosting, deep learning, or non-scorecard modeling
- the full dataset is already small enough for a simple pandas-only workflow
- the task is just generic SQL querying without scorecard development

---

## Core operating principles

The agent should follow these principles strictly:

1. **Never default to exporting the full raw table into pandas.**
2. **Do as much preprocessing as possible in DuckDB first.**
3. **Use scorecardpy on a development sample, not on the full large table.**
4. **Freeze binning rules once acceptable.**
5. **Prefer pushing full-scale mapping/scoring back to DuckDB after binning is finalized.**
6. **Be explicit about sampling logic, target definition, and modeling grain.**
7. **Treat reproducibility as a requirement, not a nice-to-have.**

---

## Skill directory contract

This skill is designed as a directory-based skill.

Expected structure:

```text
scorecardpy-duckdb-large-scale-scorecard/
├── SKILL.md
├── references/
│   ├── workflow.md
│   ├── sampling.md
│   ├── scorecardpy.md
│   ├── duckdb-deployment.md
│   └── pitfalls.md
└── scripts/
    ├── build_feature_table.sql
    ├── sample_dev_data.sql
    ├── run_scorecardpy.py
    ├── export_breaks.py
    └── apply_woe_in_duckdb.sql
```

The agent should treat this `SKILL.md` as the **entry point** and use `references/` for deeper guidance and `scripts/` for reusable implementation patterns.

---

## Skill verification

For automated layout checks and an optional pipeline smoke test (`run_scorecardpy.py` + `export_breaks.py`), see [references/skill-verification.md](references/skill-verification.md).

---

## How the agent should use this skill

When this skill is invoked, the agent should:

1. understand the business target and modeling grain
2. identify the source table / query / local data asset
3. decide whether the data is too large for direct pandas processing
4. construct or inspect a DuckDB-side modeling table
5. choose an appropriate sampling strategy
6. export only the sampled development data into pandas
7. run scorecardpy on the sampled dataset
8. freeze binning rules and selected variables
9. prepare deployment logic for full-data mapping/scoring if needed

The agent should not jump directly into `scorecardpy` before reasoning about the data path.

---

## Inputs the agent should identify

The agent should infer or request the following inputs when needed:

- source data location or SQL query
- binary target column name
- modeling grain:
  - user-level
  - account-level
  - application-level
  - order-level
- candidate feature columns
- optional handpicked modeling columns (`x_cols`) the user selects from `run_summary.json` / `selected_variables.json`
- optional partition fields:
  - train / valid / test flag
  - business date
  - snapshot date
- class imbalance condition
- optional business constraints:
  - special values
  - fixed bin cut points
  - monotonicity expectations
  - excluded variables

If some of these are missing, the agent should still push forward with a best-effort workflow and make assumptions explicit.

---

## Outputs this skill should help produce

Depending on the task, the agent may produce:

- DuckDB SQL for feature-table construction
- DuckDB SQL for development sampling
- pandas-ready sampled dataset
- scorecardpy binning result
- frozen `breaks_list`
- selected variable list
- WOE-transformed modeling dataset
- fitted scorecard model artifacts
- model evaluation outputs
- optional plot artifacts (`.png` + self-contained `.html`) under `plots/` when `--save-plots` is enabled
- deployment-ready SQL logic for WOE mapping / score computation

---

## Required workflow

The agent should follow the workflow below unless the user explicitly requests otherwise.

### Step 1: Define the modeling table in DuckDB

The agent should first define or inspect a **modeling table** in DuckDB.

The modeling table should:

- contain one row per modeling entity
- include the target column
- include only candidate features relevant to scorecard development
- avoid raw event-level detail unless that is truly the modeling grain

Typical DuckDB-side work includes:

- deduplication
- joins to labels
- aggregation from event-level to entity-level
- windowed feature generation
- missing-value normalization
- feature cleanup
- date-based slicing

The agent should prefer a narrow, stable modeling table over a giant all-purpose export.

---

### Step 2: Reduce feature complexity before scorecardpy

Before data enters pandas, the agent should simplify the feature space where possible.

Good DuckDB-side reductions include:

- dropping ID-like columns
- dropping leakage columns
- merging rare categories into `OTHER`
- removing constant / near-constant features
- converting booleans into integer flags
- deriving cleaner categorical or numeric features from messy raw columns

The agent should be especially careful with **high-cardinality categorical variables**, because they can slow scorecard binning materially.

---

### Step 3: Choose a sampling strategy in DuckDB

If the modeling table is large, the agent should sample **inside DuckDB** before exporting to pandas.

Preferred sampling strategies:

#### A. Fixed-size random sample
Use when the class distribution is acceptable and a representative sample is sufficient.

#### B. Stratified sample by target
Use when the positive / bad class is rare or the user needs better class-balance control.

#### C. Keep all bads + downsample goods
This is often the best practical default for imbalanced scorecard development.

The agent should avoid naive full-table export followed by pandas-side sampling.

---

### Step 4: Export only the development sample to pandas

Only after sampling should the agent load data into pandas.

The exported development dataset should usually contain only:

- target
- selected candidate features
- optionally an entity key for traceability

The agent should avoid `SELECT *` unless the table is genuinely small and well-controlled.

---

### Step 5: Run scorecardpy on the development sample

The agent should use `scorecardpy` only on the sampled development subset.

Typical pipeline:

1. variable filtering
2. automatic or semi-manual binning
3. WOE transformation
4. model fitting
5. scorecard generation
6. performance evaluation
7. PSI or stability checking if applicable

The agent should treat `woebin` as the expensive methodological step and should not casually run it on a large full table.

---

### Step 6: Freeze the binning rules

Once acceptable bins are found, the agent should freeze:

- `breaks_list`
- special values
- selected variables
- WOE mapping logic
- score scaling logic if scorecard points are generated

This is a critical step.
The sample exists to discover stable rules, not to justify repeated uncontrolled re-binning.

---

### Step 7: Push full-data mapping and scoring back to DuckDB

For large-scale application, the agent should prefer full-data scoring in DuckDB rather than reloading everything into pandas.

Typical patterns include:

- `CASE WHEN` bin assignment
- join with a bin mapping table
- SQL-based WOE transformation
- SQL-based points summation

The agent should separate:

- **development logic** in pandas / scorecardpy
- **production-style scoring logic** in DuckDB

---

## Decision rules

### When data is small
The agent may use a simple pandas + scorecardpy workflow without much DuckDB staging.

### When data is medium
The agent should still prefer DuckDB preprocessing and should consider sampling before binning.

### When data is large
The agent should default to:

- DuckDB feature preparation
- DuckDB sampling
- pandas on sample only
- scorecardpy on sample
- DuckDB for full-scale deployment logic

### When the bad rate is low
The agent should prefer:

- stratified sampling
- or all bads + sampled goods

### When categorical variables are high-cardinality
The agent should reduce or collapse categories before scorecardpy.

### When the user wants reproducible modeling
The agent should use fixed seeds / repeatable sampling and should materialize reusable development samples when appropriate.

---

## Sampling guidance

The agent should use DuckDB-side sampling first.

General rules:

- use fixed-size samples for iterative development speed
- use stratified sampling for imbalanced targets
- preserve reproducibility with repeatable seeds
- persist the sampled dev table if repeated tuning is expected

For severe imbalance, a strong default is:

- keep all bads
- downsample goods to a manageable size

The agent should clearly state the sampling design because it affects binning stability and model interpretation.

For deeper strategy details, consult:

- `references/sampling.md`

For ready-to-run patterns, consult:

- `scripts/sample_dev_data.sql`

---

## scorecardpy usage guidance

The agent should use scorecardpy for what it is good at:

- scorecard-style variable filtering
- binning
- WOE conversion
- scorecard generation
- evaluation

The agent should not treat scorecardpy as a large-scale compute engine.

Typical function flow:

- `var_filter`
- `woebin`
- `woebin_ply`
- downstream model fitting
- `scorecard`
- `scorecard_ply`
- `perf_eva`
- `perf_psi`

The agent should:

- reduce candidate variables before `woebin`
- avoid unnecessary reruns of automatic binning
- freeze binning outputs once validated

For more details, consult:

- `references/scorecardpy.md`
- `scripts/run_scorecardpy.py`

---

## DuckDB deployment guidance

After bins are finalized, the agent should prefer one of two deployment modes:

### Mode A: pandas deployment
Use only when the full dataset is still modest in size.

### Mode B: DuckDB SQL deployment
Preferred for large-scale local scoring.

DuckDB-side deployment should typically represent:

- bin assignment
- WOE lookup
- score point lookup
- final score aggregation

The agent should keep the final logic auditable and deterministic.

For deeper guidance, consult:

- `references/duckdb-deployment.md`
- `scripts/apply_woe_in_duckdb.sql`

---

## references/ responsibilities

The `references/` directory should hold **human-readable, stable conceptual guidance**.

Recommended responsibilities:

### `references/workflow.md`
Explain the end-to-end workflow:
DuckDB preparation → DuckDB sampling → pandas dev sample → scorecardpy → frozen bins → DuckDB scoring.

### `references/sampling.md`
Explain sampling choices:
random sample, stratified sample, all bads + sampled goods, reproducibility, class imbalance handling.

### `references/scorecardpy.md`
Explain scorecardpy function roles, parameter considerations, and practical limitations on large data.

### `references/duckdb-deployment.md`
Explain how to represent binning / WOE / score logic in DuckDB SQL.

### `references/pitfalls.md`
Collect common failure modes:
memory blow-ups, unstable samples, leakage fields, high-cardinality categories, repeated re-binning, train/oot confusion.

The agent should consult these when the task becomes ambiguous, complex, or repetitive.

---

## scripts/ responsibilities

The `scripts/` directory should hold **task-oriented implementation templates**, not vague notes.

Recommended responsibilities:

### `scripts/build_feature_table.sql`
Construct or materialize the modeling feature table in DuckDB.

### `scripts/sample_dev_data.sql`
Generate reproducible development samples in DuckDB.

### `scripts/run_scorecardpy.py`
Run scorecardpy on the sampled pandas dataset and save artifacts.

### `scripts/export_breaks.py`
Export finalized bin definitions, special values, and mapping artifacts into reusable structured files.

### `scripts/apply_woe_in_duckdb.sql`
Apply finalized bins and WOE/points logic back to the full DuckDB table.

The agent should reuse these scripts as patterns, not blindly execute them without checking column names, target definitions, and data grain.

---

## Agent behavior requirements

When using this skill, the agent must:

- state assumptions clearly when the schema is incomplete
- prefer smaller, safer development subsets over reckless full exports
- preserve target and sample definitions explicitly
- distinguish development-time logic from full-scale scoring logic
- avoid hidden resampling or silent re-binning
- keep outputs reproducible and inspectable

The agent must not:

- assume the full data fits into pandas
- feed raw wide tables directly into scorecardpy without reduction
- treat scorecardpy as a distributed or out-of-core engine
- rerun binning carelessly after bins have already been approved
- mix train and OOT logic without being explicit

---

## Common failure modes

### 1. pandas memory explosion
Cause:
too many rows or columns exported from DuckDB.

Response:
reduce columns, sample earlier, aggregate earlier, avoid full export.

### 2. scorecardpy binning is too slow
Cause:
too many rows, too many variables, or high-cardinality categories.

Response:
sample smaller, reduce variables, merge sparse categories earlier, freeze known breakpoints when possible.

### 3. bad class is underrepresented in dev sample
Cause:
naive global random sampling on an imbalanced dataset.

Response:
use stratified sampling or keep all bads + sampled goods.

### 4. bins differ every iteration
Cause:
unstable sampling or repeated uncontrolled binning.

Response:
use fixed seeds, materialize a stable development sample, freeze bin rules.

### 5. leakage or invalid features enter scorecardpy
Cause:
insufficient pre-filtering.

Response:
drop identifiers, post-event features, decision outputs, and business leakage fields before modeling.

For a fuller catalog, consult:

- `references/pitfalls.md`

---

## What good execution looks like

A strong execution of this skill will produce:

- a clean DuckDB modeling table
- a reproducible and documented development sample
- a controlled scorecardpy modeling run on the sample only
- frozen binning artifacts
- a clear full-data scoring path in DuckDB or another deterministic runtime

The end result should be:

- memory-safe
- reproducible
- explainable
- suitable for iterative scorecard development on large local data

---

## Minimal execution checklist

Before starting:
- identify target
- identify modeling grain
- identify candidate features
- assess whether full pandas export is unsafe
- assess class imbalance

Before scorecardpy:
- ensure DuckDB preprocessing is done
- ensure sampling logic is documented
- ensure only needed columns are exported

Before finalizing:
- freeze bins
- save dev-sample assumptions
- define how full-scale scoring will be done
- avoid leaving the workflow dependent on full raw-data pandas exports

---

## Invocation hint

Use this skill whenever the user wants to build a scorecard with scorecardpy on data that is large enough that naive pandas-first processing is risky.

The correct mental model is:

- DuckDB is the data engine
- pandas is the development buffer
- scorecardpy is the scorecard methodology layer
- DuckDB can also be the deployment engine for full-scale scoring
