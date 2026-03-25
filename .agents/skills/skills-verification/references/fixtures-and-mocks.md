# Fixtures And Mocks

This file indexes the fixture and mocking guidance already described in `SKILL.md`.

## Fixture and mock resolution order

When runtime or contract testing is requested, obtain test inputs in this order:

1. skill-owned fixtures
2. example-backed fixtures
3. auto-generated fixtures

## Auto-generated fixture guidance

When generating fixtures automatically, prefer **minimal, interpretable, deterministic** samples.

Preferred patterns:

- CSV / DataFrame fixture with mixed types and stable headers
- SQL fixture with a tiny valid query or DDL+DML sample
- DuckDB fixture with 1-2 small local tables
- Excel fixture with one data sheet and a small rectangular dataset
- Scorecard fixture with binary `target`, mixed features, and class variation
- API / external-system fixture via mock response files, stub clients, fake local endpoints, or dry-run mode

## Runtime behavior rules

When executing checks:

1. Prefer local, reversible operations.
2. Avoid destructive actions.
3. Use temporary files/directories for generated fixtures.
4. Avoid real production side effects.
5. Prefer mocks, stubs, and local databases over live systems.
6. Never assume credentials should be used unless the user clearly requested live validation.
7. If live validation is requested, state clearly which parts are true integration tests rather than smoke/contract tests.

## Testability expectation

This skill treats **poor testability as a real design issue** in the target skill.
