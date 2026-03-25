---
name: agents-skills-verification
description: Validate agent skills under `.agents/skills/` for structural correctness, runnable execution paths, and behavioral contracts using built-in or auto-generated fixtures, mocks, and sample data. Use when the user asks to test, verify, or harden one or more skills, especially `SKILL.md` quality, references/scripts integrity, smoke checks, or whether a skill is actually usable by an agent.
---

## Watermark

- Every time this skill is used, overwrite `water.json` in this skill directory.
- Use `../_common/scripts/write_watermark.py` to write the file.
- Required JSON shape:
  - `skill`: `agents-skills-verification`
  - `version`: watermark version, default `v1`
  - `input_files`: input file names/paths used for this run, or `[]`
  - `actions`: concise completed actions for this run
- Include validated skill paths or generated fixture paths in `input_files` when available.
- Do this before the final answer for the skill, and overwrite rather than append.

# Agents Skills Verification

## Purpose

This skill verifies whether a target skill is not only well-formed, but also genuinely usable by an agent.

It should detect four classes of issues:

1. **Structural problems**
   - Invalid or missing frontmatter
   - Missing referenced files
   - Broken `references/` or `scripts/` indexes
   - Missing required sections in `SKILL.md`

2. **Execution problems**
   - Example commands do not run
   - Entrypoint scripts fail immediately
   - Required dependencies are unavailable
   - Minimal happy-path execution is broken

3. **Contract problems**
   - The skill claims capabilities that do not actually work
   - The declared input/output behavior is unclear or false
   - The skill cannot consume the file types it says it supports
   - The produced artifacts do not match the expected outputs

4. **Testability problems**
   - The skill does not expose enough information to generate a minimal test case
   - The skill cannot be executed against a mock, fixture, stub, or dry-run path
   - External dependencies are hard-coded with no fallback or simulation path

This skill treats **poor testability as a real design issue** in the target skill.

---

## When to use

Use this skill when the user asks to:

- test all skills under `.agents/skills/`
- validate a specific skill directory
- check whether a `SKILL.md` is agent-usable, not just well-written
- run smoke tests for a skill
- generate mock data / fixtures / synthetic inputs for a skill
- verify references and scripts are aligned with the skill description
- harden skill quality before publishing or sharing

---

## Scope resolution

Determine the scope before running validation.

### Verify all skills
If the user says things like:
- “test all skills”
- “validate everything under `.agents/skills/`”
- “check all SKILL.md files”

Then test every subdirectory containing:

```text
.agents/skills/*/SKILL.md
```

### Verify one skill
If the user names a specific skill, only validate that skill directory.

If the skill name is ambiguous, resolve by matching the directory name first, then the frontmatter `name`.

---

## Verification model

Always validate in **layers**, from cheapest to most behaviorally meaningful.

Indexed references:

- `references/layers.md` — verification layers and the core principle for meaningful validation

### Layer 1 — Structural validation
Check the target skill for:

- valid YAML frontmatter
- required frontmatter keys:
  - `name`
  - `description`
- presence of `SKILL.md`
- valid directory shape
- section completeness
- all indexed files under `references/` and `scripts/` actually exist
- all example paths and local file references are resolvable

This layer should be fast and non-destructive.

### Layer 2 — Smoke validation
Run the target skill’s minimal execution path, if one exists.

Typical checks:
- a help command works
- an example script starts successfully
- dependencies import correctly
- a smallest happy path completes without immediate crash

If the environment is missing dependencies, try the most local and reproducible runner available, for example:

```bash
python ...
uv run python ...
```

Do not silently skip smoke checks without reporting why.

If any temporary files or directories should be used for smoke checks, tear them down when smoke checks are done (successful or not).

### Layer 3 — Contract validation
Test whether the skill actually does what it claims.

Examples:
- if a skill claims to support CSV input, feed it a minimal CSV
- if it claims to export Excel, verify an Excel file is produced
- if it claims to write DuckDB tables, verify the table exists afterward
- if it claims to reject invalid inputs, verify that the rejection is clear and intentional

This is the most important layer.

### Layer 4 — Negative-path validation
Test at least one invalid input path when feasible.

Examples:
- missing required columns
- empty query or empty dataset
- invalid file type
- malformed config
- impossible table name
- absent environment variable

A good skill should fail **clearly**, not just crash.

---

## Core principle

A skill is **not** considered fully verified merely because:
- its markdown is valid
- its example command starts
- its script does not crash immediately

A skill is only meaningfully verified when the verifier can establish a minimal executable contract between:

- declared inputs
- expected behavior
- produced outputs
- understandable failure modes

If that contract cannot be tested because the skill is too vague, report the skill as **insufficiently testable**.

---

## Test strategy

## 1) Detect the target skill profile
Infer the skill type from its `SKILL.md`, scripts, references, filenames, and examples.

Indexed references:

- `references/skill-type-matrix.md` — skill profile matrix and example validation heuristics

Common skill profiles:

### A. Documentation-only skill
The skill is instructional and does not execute code.

Validate:
- structure
- completeness
- file references
- example correctness

### B. File-processing skill
The skill consumes or produces files such as:
- csv
- parquet
- json
- xlsx
- sql
- duckdb

Validate:
- minimal fixture generation
- file ingestion
- output creation
- schema assumptions

### C. Model / analytics skill
The skill trains, scores, transforms, bins, or analyzes data.

Validate:
- minimal synthetic dataset
- required columns
- target/feature assumptions
- output object or artifact structure

### D. External-system skill
The skill depends on:
- ODPS
- APIs
- services
- cloud databases
- credentials

Validate:
- mock/stub/dry-run readiness
- graceful failure when credentials are missing
- minimal offline behavior if supported

### E. Hybrid skill
The skill spans multiple categories. Validate each layer conservatively.

---

## 2) Fixture and mock resolution order
When runtime or contract testing is requested, obtain test inputs in this order:

Indexed references:

- `references/test-strategy.md` — fixture resolution order, auto-generation policy, and negative fixtures
- `references/fixtures-and-mocks.md` — fixture sourcing priorities, mocking guidance, and runtime behavior rules
- `scripts/fixture_generator_example.py` — example fixture generator for minimal deterministic samples

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

---

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
Use a tiny valid query or DDL+DML sample matching the skill’s domain.

Example:

```sql
select 1 as id, 'A' as segment, 100 as amount
union all
select 2 as id, 'B' as segment, 200 as amount;
```

### DuckDB fixture
Create a minimal local DuckDB database with 1–2 small tables and simple schemas.

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

---

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

---

## Expected target-skill conventions

This verifier should reward skills that are explicit about their contracts.

Indexed references:

- `references/contract-testing.md` — contract checks, negative-path checks, expected conventions, and failure interpretation
- `scripts/contract_runner_example.py` — example contract checker that reports by layer and severity

A strong target `SKILL.md` should ideally state:

- accepted input types
- required columns / parameters / files
- expected outputs
- minimal runnable path
- failure conditions
- dependency boundaries
- whether mock / dry-run / local-only validation is supported

If these are absent, the verifier should still do best-effort inference, but report reduced confidence.

---

## Recommended target skill layout

Encourage the following layout where possible:

```text
skill_name/
├─ SKILL.md
├─ references/
│  └─ ...
├─ scripts/
│  └─ ...
├─ tests/
│  ├─ fixtures/
│  ├─ expected/
│  └─ smoke.py
```

Interpretation:
- `references/`: static supporting docs, schemas, notes, contracts
- `scripts/`: runnable examples, helpers, validators, demos
- `tests/fixtures/`: canonical sample inputs
- `tests/expected/`: expected outputs or golden files
- `tests/smoke.py`: skill-specific smoke/contract checks

If these test resources do not exist, this verifier may synthesize minimal equivalents.

---

## Runtime behavior rules

When executing checks:

1. Prefer local, reversible operations.
2. Avoid destructive actions.
3. Use temporary files/directories for generated fixtures.
4. Avoid real production side effects.
5. Prefer mocks, stubs, and local databases over live systems.
6. Never assume credentials should be used unless the user clearly requested live validation.
7. If live validation is requested, state clearly which parts are true integration tests rather than smoke/contract tests.

---

## Result reporting

Always report results by **severity** and by **validation layer**.

Indexed references:

- `references/reporting-format.md` — severity, required report sections, output style, and confidence language

### Severity levels
- **fatal**: the skill is unusable or unverifiable in a meaningful way
- **major**: the skill behavior contradicts its description or fails the main contract
- **minor**: non-blocking structural or clarity problems
- **warning**: reduced confidence, skipped checks, fallback to generated fixtures, or environment limitations

### Required report sections
For each skill, report:

1. **Structural validation**
2. **Smoke validation**
3. **Contract validation**
4. **Negative-path validation**
5. **Fixture/mocking notes**
6. **Skipped checks and why**

### Output style
Separate:
- must-fix errors
- warnings
- skipped items
- confidence notes

Do not collapse everything into a single PASS/FAIL unless the user explicitly wants a terse summary.

---

## Confidence model

Use confidence language based on how strong the verification really was.

### High confidence
Use when:
- the skill provided concrete fixtures or tests
- the verifier executed a real minimal path
- outputs were verified
- at least one negative-path test was checked

### Medium confidence
Use when:
- the skill ran successfully
- some fixtures were auto-generated
- outputs were partly checked
- some behaviors were inferred rather than explicit

### Low confidence
Use when:
- only structural checks ran
- runtime checks were skipped
- the skill was too vague to construct a meaningful contract
- live dependency boundaries prevented testing

---

## Canonical workflow

### Case 1 — Validate all skills
1. Discover `.agents/skills/*/SKILL.md`
2. Run structural validation for all
3. Run smoke validation where feasible
4. Run contract validation when fixtures exist or can be generated safely
5. Report per-skill and overall summary

### Case 2 — Validate one named skill
1. Resolve the skill directory
2. Run structural validation
3. Inspect for scripts, references, test assets, and examples
4. Select fixture strategy
5. Run smoke + contract + negative-path checks as appropriate
6. Report issues with precise file-level references

### Case 3 — User asks for runtime validation specifically
1. Run structural checks first
2. Attempt smoke checks
3. Attempt contract checks with fixtures
4. Distinguish clearly between:
   - local smoke
   - offline contract test
   - real integration test

---

## Example validation heuristics

### For a SQL export skill
Verify:
- SQL input exists or can be mocked
- DuckDB fixture can be created
- query execution produces rows
- empty result path is handled intentionally
- invalid table name is rejected clearly
- declared export artifact is actually created

### For a scorecardpy skill
Verify:
- binary target exists
- sample dataset has valid class diversity
- required package imports
- a minimal binning / iv / woe path runs
- bad target or missing columns fail clearly

### For a pure documentation skill
Verify:
- frontmatter valid
- references and scripts paths valid
- examples are coherent
- no false implication of runtime capability

---

## Failure interpretation rules

Do not confuse these cases:

### Environment issue
Examples:
- missing Python package
- no `uv`
- no system executable

This is not always a skill defect, but it must still be reported.

### Skill defect
Examples:
- broken example command
- missing referenced file
- unsupported file type despite claiming support
- impossible-to-test contract because the skill is underspecified

### Integration-boundary issue
Examples:
- real credentials needed
- external service unavailable
- production-only runtime path

Report these separately and recommend mockable or dry-run design improvements.

---

## Improvement guidance

When the verifier finds a weak target skill, recommend improvements such as:

- add explicit `tests/fixtures/`
- add a minimal runnable example
- document accepted schemas and required columns
- support `--dry-run`
- support local/mock mode for external systems
- add negative-path examples
- declare outputs more concretely
- index `references/` and `scripts/` clearly inside `SKILL.md`

---

## References

Use the following as indexed support material for this skill:

- `references/skill-contracts.md` — how to express testable input/output/failure contracts for skills
- `references/fixture-generation.md` — minimal fixture generation patterns for csv/sql/duckdb/xlsx/modeling skills
- `references/report-severity.md` — severity model and reporting conventions

If these files do not yet exist in the repository, treat them as the intended documentation structure for this skill.

---

## Scripts

This skill expects or benefits from the following scripts:

- `scripts/verify_skills_registry.py` — structural/frontmatter/index verifier
- `scripts/verify_skill_runtime.py` — smoke runner for a single skill or all skills
- `scripts/generate_skill_fixture.py` — auto-generates minimal fixtures based on inferred skill type
- `scripts/verify_skill_contract.py` — contract and negative-path validator

If these scripts do not yet exist, treat them as the intended executable structure for this skill.

---

## Examples

### Example 1
User request:
> 测试 `.agents/skills/` 下所有 SKILL 是否符合描述且能正常工作

What this skill should do:
1. discover all skills
2. run structural validation on all
3. run smoke validation where possible
4. generate fixtures when safe and useful
5. run contract checks for skills that can be meaningfully exercised
6. report errors, warnings, skips, and confidence per skill

### Example 2
User request:
> 只验证 scorecardpy 这个 skill 是否正常

What this skill should do:
1. locate the `scorecardpy` skill
2. validate frontmatter and indexed files
3. generate or load a binary classification fixture
4. run minimal runtime and contract checks
5. test one negative case, such as missing target column
6. report the failing step if anything breaks

### Example 3
User request:
> 帮我看这个 skill 为什么很难测试

What this skill should do:
1. inspect the target skill contract clarity
2. determine whether minimal runnable inputs can be constructed
3. identify missing fixture hooks, dry-run paths, or output definitions
4. explain whether the issue is structural, behavioral, or testability-related

---

## Final rule

When in doubt, prefer this order:

1. verify structure
2. verify minimal execution
3. verify behavioral contract
4. verify graceful failure

A skill that is readable but not testable is still incomplete.
