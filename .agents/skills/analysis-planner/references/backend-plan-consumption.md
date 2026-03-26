# Backend Plan Consumption

This file describes how a backend should consume an `AnalysisPlan`.

The focus here is not the exact current backend schema.
The focus is the set of backend behaviors that a plan object must support.

## Core principle

The backend should not treat a plan as a passive blob.

It should consume the plan through a few explicit responsibilities:

1. validate the plan structurally
2. judge whether the plan is runnable
3. decide whether user clarification or user review is needed
4. execute only the executable subset of the plan
5. preserve the plan as the source of truth across revisions

In other words, a plan is both:

- an execution contract
- a review contract
- a state-carrying object across turns

## Backend consumption surfaces

### 1. Validation surface

The backend should be able to validate:

- top-level shape
- enum values
- schema-column references
- required versus recommended versus optional elements
- minimal-completion status

This is the first consumer of the plan object.

If validation is weak, every later step becomes fragile.

### 2. Completeness-judgment surface

The backend should not ask "is this JSON parseable?"
It should ask "is this plan ready for the next step?"

A useful judgment layer should support at least:

- `complete`
  - the plan is runnable without hidden assumptions on the core analysis path
- `needs_exploration`
  - the plan is directionally useful but should surface open questions or exploration before autonomous execution
- `blocked`
  - the plan is not safely runnable because a material contract decision is unresolved

This is why a plan should carry explicit completeness metadata rather than forcing the backend to reverse-infer readiness.

### 3. User-review surface

When a plan is not clearly runnable, the backend should be able to turn plan metadata into a user-facing review request.

The backend should be able to read from the plan:

- rationale for the current completeness judgment
- missing information
- open questions
- exploration tasks
- blocking versus non-blocking issues

This makes the review flow explainable rather than opaque.

The existing backend already points in this direction by building review messages from completeness rationale, open questions, and exploration tasks.

### 4. Execution surface

The backend executor should consume only the directly executable slice of the plan.

At minimum this usually means:

- metrics
- dimensions
- filters
- output preferences

Other elements such as:

- assumptions
- ambiguities
- validation
- comparisons
- methods

may not all be executed directly, but they still matter because they:

- constrain execution choices
- justify why execution is safe
- explain what the result does and does not answer

So the backend should distinguish:

- executable fields
- review and trust fields
- orchestration fields

instead of flattening everything into one execution-only structure.

### 5. Revision surface

A plan should be revisable without losing continuity.

That means backend revision logic should:

1. keep the prior plan
2. apply user feedback to the same evolving object
3. recompute completeness
4. update dependent fields
5. preserve review history and diffs

This is important because plan revision is not a fresh generation event.
It is a state transition on the same analytical object.

The current backend already reflects this pattern in its revise flow and review diff handling.

### 6. Persistence and observability surface

The backend should persist the plan because it is the canonical intermediate artifact between:

- user intent
- schema reasoning
- execution
- result interpretation

Useful persisted views include:

- original generated plan
- revised plan
- final accepted plan
- review diffs
- completeness status over time

This makes the planning loop debuggable and inspectable.

## Recommended backend mental model

The backend should treat plan fields in three buckets.

### A. Execution-critical

These fields directly drive data operations:

- `metrics`
- `dimensions`
- `filters`
- `output`

### B. Decision-critical

These fields determine whether execution is valid:

- `goal`
- `scope`
- `analysis_type`
- `grain`
- `time`
- `comparisons`
- `validation`

### C. Interaction-critical

These fields determine what the system should ask or show next:

- `ambiguities`
- completeness status
- open questions
- exploration tasks
- assumptions
- confidence

This split is more useful for backend design than thinking only in terms of JSON nesting.

## Suggested backend methods

If the backend evolves toward a richer plan model, these are the main methods worth preserving conceptually:

- `validate_plan(plan, schema_profile) -> ValidationResult`
- `judge_plan_completeness(plan) -> CompletenessDecision`
- `build_review_request(plan) -> ReviewPayload | None`
- `extract_execution_spec(plan) -> ExecutionSpec`
- `apply_plan_revision(plan, user_feedback) -> AnalysisPlan`
- `record_plan_transition(before, after, reason) -> None`

The current backend already has partial versions of these behaviors spread across schemas, router helpers, and execution code.
The long-term design can make them more explicit.

## Most important design takeaway

For backend purposes, the most important question is not:

- "What fields exist in the plan?"

It is:

- "What decisions can the backend make from this plan without guessing?"

A good plan object lets the backend answer all of these without hidden inference:

- Can I run this?
- Should I ask the user something first?
- What exactly should I ask?
- Which part is blocked?
- Which fields actually drive execution?
- What changed after revision?

That is the real consumer-oriented standard for a data-analysis plan object.
