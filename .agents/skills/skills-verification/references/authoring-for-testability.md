# Skill Authoring Requirements for Testability

This document defines what a skill author should provide if a skill is expected to be testable in a repeatable, agent-usable way.

The point is simple: a verifier cannot reliably test a skill whose operational contract is only implied.

A skill is not truly testable just because it has a `SKILL.md`. A skill becomes testable when its author exposes enough structure for a verifier to construct a minimal, credible execution path.

## Why this matters

A large share of weak skills fail for the same reason:   

- the purpose is stated, but not the contract,
- the examples are illustrative, but not runnable,
- the dependency is named, but not bounded,
- the output is described, but not checkable.

That produces skills that are readable by humans but difficult for agents to validate, exercise, or safely reuse.

A testable skill should therefore be treated as a **designed interface**, not just a documentation page.

## Minimum authoring contract

A skill should make the following items explicit.

### 1. Purpose

The skill should clearly state:

- what problem it solves,
- what task boundary it owns,
- and what it does not try to do.

This lets the verifier determine whether the promised behavior is narrow enough to test.

### 2. Inputs

The skill should define the minimal valid input shape, including where relevant:

- accepted file types,
- required parameters,
- required columns or schema,
- environment variables,
- credentials or service endpoints,
- optional vs required inputs.

If the verifier cannot tell what counts as a valid minimal input, the skill is only weakly testable.

### 3. Outputs and side effects

The skill should define what success looks like.

Examples:

- creates a file,
- updates a table,
- returns a summary,
- writes an artifact,
- produces a model object,
- emits a report,
- performs a remote mutation.

These outputs must be specific enough to check.

### 4. Failure modes

The skill should describe expected failure classes such as:

- missing inputs,
- missing dependency,
- unsupported format,
- empty result,
- invalid schema,
- authentication failure,
- dry-run only.

This is necessary for negative-path testing.

### 5. Minimal runnable path

A skill should expose at least one minimal runnable path.

For example:

- a sample command,
- a sample script,
- a minimal fixture,
- a local test mode,
- a dry-run flow.

Without this, smoke and contract testing become guesswork.

## Recommended authoring structure

A test-friendly skill directory usually benefits from the following layout:

```text
skill_name/
├─ SKILL.md
├─ references/
├─ scripts/
└─ tests/
   ├─ fixtures/
   ├─ expected/
   └─ smoke.py
```

Not every skill needs every file, but the structure gives the verifier obvious places to look.

## Required declarations inside SKILL.md

A skill that aims to be testable should make these concepts easy to locate in the main skill doc:

- purpose
- when to use
- inputs
- outputs
- minimal execution path
- dependency boundary
- failure behavior
- references index
- scripts index

These do not have to be rigid headings, but they should be easy to infer.

## Strongly recommended additions

These are not always mandatory, but they make a big difference.

### Dry-run support

If the skill touches external systems, a dry-run path is strongly recommended.

Examples:

- `--dry-run`
- `MOCK=1`
- `USE_FAKE_BACKEND=1`
- stub transport or fake client

If the skill cannot be safely exercised without live mutation, its automated test coverage will usually be limited.

### Fixture-ready schema

A skill should expose enough schema detail for a verifier to generate synthetic inputs.

For example:

- required CSV columns,
- required SQL placeholders,
- expected table names,
- expected date fields,
- target column requirements,
- accepted categorical/numeric types.

The more explicit this is, the more realistic the generated fixtures can be.

### Expected artifact semantics

When a skill generates files or objects, describe what is stable enough to test.

Examples:

- file existence,
- sheet name,
- table name,
- JSON keys,
- row count constraints,
- expected status code,
- expected log markers.

This avoids brittle tests that depend on incidental output.

## What authors should avoid

Avoid these common anti-patterns.

### 1. Hidden assumptions

Do not assume the verifier knows:

- which Python environment to use,
- where the credentials live,
- which table must already exist,
- which local path is pre-created,
- which network service is reachable.

Anything that must exist should be documented.

### 2. Example-only instructions

A prose example is not the same as a runnable path.

“Use this skill to export SQL results to Excel” is helpful, but it is not testable until the skill also states the minimal accepted inputs and success criteria.

### 3. Unbounded external dependency

If a skill requires a production service, document whether the verifier is allowed to:

- skip live execution,
- substitute a mock,
- use local fallback,
- or run only dry-run checks.

### 4. Ambiguous success criteria

“Produces useful output” is not testable.

“Creates `output/report.xlsx` with sheet `summary`” is testable.

## Authoring checklist

Before considering a skill testable, ask:

- Can a verifier infer the minimal valid input?
- Can a verifier determine what success looks like?
- Can a verifier determine what controlled failure looks like?
- Is there a runnable path that does not rely on hidden context?
- Is there a mock, fixture, or dry-run path for external systems?
- Are references and scripts indexed clearly?

If several answers are no, the skill is likely under-specified.

## Severity guidance

The verifier can treat authoring gaps with different severity.

### Warning

- no dedicated fixtures, but auto-generation is possible
- no explicit negative-path section, but failure behavior can be inferred
- sparse examples, but runnable path exists

### Major

- inputs are incomplete or ambiguous
- outputs are described vaguely
- external dependency has no mock/dry-run guidance
- examples exist but are not runnable

### Fatal

- purpose is unclear
- no minimal execution path exists
- contract cannot be inferred
- success cannot be checked
- skill depends entirely on undocumented hidden context

## Long-term direction

A mature skill ecosystem should not rely on heroic inference from the verifier.

Instead, skill authors should publish skills in a way that makes them:

- readable,
- runnable,
- mockable,
- contract-checkable,
- and safe to validate automatically.

That is the real standard for testability.
