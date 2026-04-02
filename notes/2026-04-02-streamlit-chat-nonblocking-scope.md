# Streamlit Chat Non-Blocking Scope

## Question

Investigate whether `app/ui_chat.py` can cause an in-progress message generation to block the whole page process, and estimate the scope of a fix aimed at this outcome:

- While a chat reply is generating, the page should remain usable.
- The fix should prefer Streamlit-native mechanisms where possible.
- The user specifically asked whether `st.fragment` can solve this.

## Current Behavior

The current chat flow is synchronous from the Streamlit session's point of view.

Relevant paths:

- `app/streamlit_app.py`
- `app/ui_chat.py`
- `app/chat_actions.py`
- `app/api_client.py`

Observed execution model:

1. User input appends a message with `type="thinking"` via `_enqueue_chat()`.
2. On the next Streamlit rerun, `render_chat_message()` sees the `thinking` message.
3. `render_chat_message()` immediately calls `_execute_chat_reply()` during rendering.
4. `_execute_chat_reply()` synchronously consumes `_stream_chat()` using `requests.post(..., stream=True)` and `iter_lines()`.
5. The Streamlit script thread stays occupied until the stream ends or fails.

Key code references:

- `app/ui_chat.py:303`
- `app/ui_chat.py:314`
- `app/chat_actions.py:279`
- `app/chat_actions.py:300`
- `app/chat_actions.py:301`
- `app/api_client.py:244`
- `app/api_client.py:252`
- `app/api_client.py:266`

## Conclusion

Yes. For the current Streamlit session, an in-progress generated message can block the page's interactive execution path.

Clarification:

- This is not necessarily a full-process global lock across all users.
- It is a blocking long-running script execution for the current page session.
- Under constrained server resources, this pattern can also reduce overall app throughput.

## Why `st.fragment` Alone Is Not Enough

`st.fragment` is useful for partial reruns and polling-style UI updates, but it is not a background execution primitive.

If the same synchronous streaming loop is moved into a fragment, the fragment run is still blocked until that loop completes. That means:

- `st.fragment` helps isolate reruns.
- `st.fragment` does not make a long synchronous task non-blocking by itself.

So the problem is not mainly "full-page rerun cost". The problem is "long work is executed in the render path".

## Viable Solution Shapes

### Option A: `st.write_stream`

This is a Streamlit-native improvement for visible streaming output, but it still runs in the current script execution.

What it solves:

- Better streaming UX.
- Simpler text streaming to the page.

What it does not solve:

- The current session remains occupied during generation.
- The page is still not truly free to handle unrelated interactions.

Assessment:

- Useful for UX polish.
- Not the right answer to the requested outcome.

### Option B: `st.fragment` + background job + polling

This is the correct shape for the requested outcome.

Required split:

- Submission path: create a chat job and return immediately.
- Execution path: run the actual Codex streaming work outside the Streamlit render path.
- Render path: use `st.fragment(run_every=...)` or equivalent polling to refresh only the chat region.

What it solves:

- The page is no longer blocked by the active chat generation in the same way.
- Partial UI reruns become practical.
- The message area can update independently.

## Backend Impact

### Can this be done without backend changes?

Yes, but it is not the preferred design.

Frontend-only version:

- Start a local background thread from Streamlit.
- That thread calls the existing `/chat/stream`.
- The page polls thread-owned state.

Problems:

- Job state lives only inside the Streamlit process.
- Reload/reconnect behavior is fragile.
- Multi-user and multi-process behavior is harder to reason about.
- Thread coordination with Streamlit session state is awkward.

Assessment:

- Technically possible.
- Lower engineering quality.

### Recommended backend changes

Backend changes are not strictly mandatory, but they are strongly recommended.

The backend already has:

- `/chat`
- `/chat/stream`
- chat turn persistence in `backend/chat_store.py`

That makes a small chat-job layer feasible.

Recommended additions:

1. `POST /chat/jobs`
   - Accepts the same input as chat.
   - Creates a job id.
   - Starts background execution.
   - Returns immediately.

2. `GET /chat/jobs/{job_id}`
   - Returns `queued/running/completed/failed`.
   - Returns incremental stream state or latest snapshot.
   - Returns final reply when complete.

3. Optional `DELETE /chat/jobs/{job_id}`
   - Cancels the job if supported.

4. Small persistence or in-memory job registry
   - In-memory is enough for a first MVP.
   - SQLite persistence is better if recovery after refresh matters.

### Recommended low-impact architecture

To minimize implementation risk, do not rewrite the current chat business logic.

Preferred shape:

- Keep the existing `/chat` and `/chat/stream` behavior as the source of truth for:
  - request parsing
  - provider selection
  - Codex fallback handling
  - timing/usage capture
  - final turn persistence
- Add a thin job orchestration layer around the existing streaming path.
- Move only the execution location, not the chat semantics.

Recommended module split:

- `backend/routers/chat.py`
  - Keep `/chat` and `/chat/stream`.
  - Add `POST /chat/jobs`.
  - Add `GET /chat/jobs/{job_id}`.
- `backend/chat_jobs.py`
  - Own job creation, in-memory registry, status updates, and background worker lifecycle.
- Optional shared runner helper
  - Extract the core stream execution flow so `/chat/stream` and the job worker can reuse the same logic instead of duplicating it.

Important constraint:

- The new job layer should not own prompt/provider logic.
- It should only own:
  - `job_id`
  - status (`queued/running/completed/failed`)
  - latest stream snapshot
  - final reply/error
  - background execution lifecycle

This keeps the change set smaller and reduces the chance of `/chat/stream` and `/chat/jobs` drifting apart behaviorally.

Additional compatibility constraints:

- The non-blocking path must preserve current chat session semantics.
  - `session_id` must still be assigned consistently and written back to the frontend state.
  - completed jobs must still produce normal chat turns that appear in `/chat/sessions` and `/chat/sessions/{session_id}/turns`
- The non-blocking path must preserve current replay semantics.
  - chat history reconstruction currently depends on persisted `reply_text`
  - loading an old session from the sidebar currently rebuilds frontend messages from stored turns
  - do not make job-local state the only place where final reply data exists
- The non-blocking path must preserve current result/artifact semantics.
  - if a final reply contains JSON with `result.artifacts`, the final stored reply must remain compatible with the current frontend parsing path
  - the implementation must not require live in-memory stream state in order for historical chat results or artifacts to render later

Implication:

- The job layer is allowed to hold transient progress state.
- It is not allowed to become the only source of truth for final chat content.
- Final persisted turn data must remain sufficient for later session restore and reproducibility-oriented inspection.

### Recommended frontend changes

The frontend also needs explicit changes, because the current blocking behavior is caused by work being executed inside render-time code.

Recommended frontend shape:

1. Keep `_enqueue_chat()` as the user action entry point.
   - It should still append a pending assistant message.

2. Change `_execute_chat_reply()` to submit a job instead of consuming SSE inline.
   - Replace the direct `_stream_chat(...)` loop with `POST /chat/jobs`.
   - Save the returned `job_id` into the pending message.

3. Render the active assistant message as a passive pending/running card.
   - The render path should not directly trigger a long backend stream.
   - The card can show:
     - pending/running status
     - latest partial text
     - latest reasoning/command preview
     - error state if failed

4. Add a chat-scoped polling fragment.
   - Use `st.fragment(run_every=...)` or equivalent polling only for the chat area.
   - Poll `GET /chat/jobs/{job_id}` for pending/running messages.
   - When the job completes, replace the pending message with the existing `chat_response` shape.

5. Keep the final frontend message schema close to the current one.
   - Reuse the existing `chat_response` rendering path where possible.
   - Avoid a full message model rewrite just to support non-blocking chat.

6. Preserve session restore and reproducibility flows.
   - Sidebar session load currently rebuilds messages from persisted chat turns.
   - The final completed message produced by a job should still map cleanly to that restore flow.
   - Avoid introducing a frontend-only completed shape that cannot be reconstructed from backend turn history.

Frontend files likely impacted:

- `app/ui_chat.py`
- `app/chat_actions.py`
- `app/api_client.py`
- possibly `app/streamlit_app.py` if the fragment placement needs app-level coordination

### Suggested job response shape

The first version does not need a full event-replay API.

A practical snapshot response is enough:

- `job_id`
- `status`
- `session_id`
- `turn_id`
- `latest_text`
- `latest_reasoning_text`
- `latest_command`
- `stream_events` (optional, possibly truncated)
- `final_reply`
- `timing`
- `usage`
- `error`

This fits the current frontend rendering model better than introducing a brand new event contract.

Important distinction:

- The job snapshot is for in-flight UI polling.
- It should not replace the final persisted chat turn representation used for history/reload.
- On completion, the job result should collapse back into the same durable final reply contract the app already relies on.

## Scope Estimate

### Minimal usable version

Estimated effort:

- About 1 day for a focused implementation.

Likely scope:

- Only fix chat generation.
- Do not change task planning or task execution flows yet.

Files likely touched:

- `app/ui_chat.py`
- `app/chat_actions.py`
- `app/streamlit_app.py`
- `app/api_client.py`
- `backend/routers/chat.py`
- `backend/chat_store.py`
- possibly a new file such as `backend/chat_jobs.py`

### More robust version

Estimated effort:

- About 1.5 to 2 days.

Additional work:

- Durable job state.
- Better error recovery.
- Refresh-safe resume behavior.
- Duplicate-run protection.
- Optional cancellation.

Complexity drivers:

- Extracting reusable chat execution flow from the current router path
- Designing a minimal but sufficient job snapshot/state model
- Preventing duplicate submission across Streamlit reruns
- Updating the frontend message lifecycle without breaking current rendering
- Handling failure/fallback semantics consistently across `/chat/stream` and `/chat/jobs`
- Preserving sidebar session restore behavior based on stored turns
- Preserving artifact/result rendering for both live responses and reloaded historical chats

## Recommended Plan

### Phase 1

Implement non-blocking chat only.

Changes:

- Keep current `/chat/stream` untouched.
- Add `POST /chat/jobs`.
- Add `GET /chat/jobs/{job_id}`.
- Add a thin in-memory backend job registry and background worker.
- Reuse the existing chat execution logic instead of reimplementing provider behavior in the job layer.
- Change Streamlit chat send flow to submit a job instead of executing inside `render_chat_message()`.
- Render the active message as a passive "pending/running" card.
- Add a chat-area fragment that polls job status and updates the message.
- Preserve final turn persistence so sidebar history loading and chat replay continue to work.
- Keep artifact-bearing final replies compatible with the current `chat_response` parsing/render path.

### Phase 2

Optionally extend the same pattern to:

- `create_task`
- `confirm_task`
- `revise_plan`
- `respond_review`

This can be deferred. The immediate pain point appears to be free-form chat generation.

## What Should Not Stay As-Is

Avoid keeping this pattern for non-blocking requirements:

- Render function directly triggering network execution.
- Long SSE loop inside Streamlit render code.
- Session state as the only source of truth for in-flight work.

## Bottom Line

The fix is a medium-sized refactor, not a large rewrite.

The core change is architectural:

- move chat execution out of the Streamlit render path
- keep rendering and execution separate

The lowest-risk implementation strategy is:

- keep the current chat execution logic
- add a thin backend job layer
- switch the frontend from inline SSE consumption to job submission plus polling

`st.fragment` is helpful in the final design, but only as the polling/render mechanism. It is not the mechanism that removes blocking.

## Backend Implementation Update (2026-04-02)

This section records what has already been implemented in backend for Phase 1.

### Implemented

1. New in-memory chat job registry
   - Added `backend/chat_jobs.py`
   - Provides job lifecycle and polling snapshot:
     - `queued/running/completed/failed`
     - latest text/reasoning/command snapshot
     - capped `stream_events`
     - final reply and timing/usage/runtime fields

2. Shared chat stream execution path
   - In `backend/routers/chat.py`, extracted shared execution helpers:
     - `_build_chat_context(...)`
     - `_iter_chat_events(...)`
   - `/chat/stream` now reuses `_iter_chat_events(...)` instead of owning a separate stream loop copy.
   - This keeps stream behavior and turn persistence semantics aligned for both direct stream and job mode.

3. New chat jobs API
   - Added `POST /chat/jobs`
   - Added `GET /chat/jobs/{job_id}`
   - `POST /chat/jobs` starts background execution and returns a polling snapshot immediately.
   - `GET /chat/jobs/{job_id}` returns latest snapshot for frontend polling.

### Contract Notes for Frontend

- `POST /chat/jobs` accepts the same body/query fields as `/chat/stream`.
- Response includes:
  - `job_id`
  - `status`
  - `session_id`
  - `turn_id`
  - `chat_id`
  - `latest_text`
  - `latest_reasoning_text`
  - `latest_command`
  - `stream_events`
  - `final_reply`
  - `timing`
  - `usage`
  - `runtime_vendor`
  - `runtime_binary`
  - `error`
- `GET /chat/jobs/{job_id}` returns the same snapshot shape.

### Persistence/Reproducibility Semantics Preserved

- Final turn persistence is still handled by the same chat execution path.
- Session/turn history endpoints (`/chat/sessions`, `/chat/sessions/{session_id}/turns`) remain the source of truth for historical replay.
- Job registry stores transient in-flight state only; it is not used as durable chat history.

### Current Scope Boundary

- Backend-only Phase 1 is implemented here.
- No frontend changes are included in this update.
- `DELETE /chat/jobs/{job_id}` is not implemented yet.
