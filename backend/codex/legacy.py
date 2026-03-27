"""One-shot ``codex exec`` subprocess provider."""

from __future__ import annotations

import asyncio
import contextlib
import json
import logging
import os
import tempfile
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

from pydantic import ValidationError

from backend.codex.errors import CodexAdapterError
from backend.codex.jsonl_encoding_fix import repair_jsonl_text
from backend.codex.json_util import extract_json_array_payload, extract_json_payload
from backend.codex.prompts import (
    build_chat_prompt,
    build_followups_prompt,
    build_plan_prompt,
    build_revise_plan_prompt,
    build_summary_prompt,
)
from backend.codex.xinfei_sso import resolve_codex_executable
from backend.observability import log_event, save_snapshot
from backend.planning.adapters import parse_plan_payload
from backend.schemas.plan import AnalysisPlan
from backend.skills import (
    SKILL_ANALYSIS_PLANNER,
    SKILL_DATA_CHAT,
    SKILL_PLAN_REVISER,
)

logger = logging.getLogger(__name__)
_CHAT_OUTPUT_SCHEMA_PATH = Path(__file__).with_name("chat_output.schema.json")


def _format_exception_for_logs(exc: BaseException, *, max_chain: int = 5) -> str:
    parts: list[str] = []
    cur: BaseException | None = exc
    for _ in range(max_chain):
        if cur is None:
            break
        name = type(cur).__name__
        text = str(cur).strip()
        if not text:
            if isinstance(cur, ValidationError):
                try:
                    text = cur.json()
                except Exception:
                    text = repr(cur)
            else:
                text = repr(cur)
        parts.append(f"{name}: {text}")
        cur = cur.__cause__ or cur.__context__
    return " | ".join(parts) if parts else repr(exc)


def _codex_exec_config_args(
    model_override: str | None = None,
    reasoning_override: str | None = None,
) -> list[str]:
    parts: list[str] = []
    model = (model_override or "").strip() or os.getenv("CODEX_MODEL", "").strip()
    if model:
        parts.extend(["-c", f"model={json.dumps(model, ensure_ascii=False)}"])

    reasoning = (reasoning_override or "").strip().lower()
    if not reasoning:
        reasoning = os.getenv("CODEX_REASONING_EFFORT", "").strip().lower()
    if not reasoning:
        reasoning = os.getenv("CODEX_THINK_LEVEL", "").strip().lower()
    if reasoning:
        parts.extend(
            [
                "-c",
                f"model_reasoning_effort={json.dumps(reasoning, ensure_ascii=False)}",
            ]
        )

    disable_mcp = os.getenv("CODEX_DISABLE_MCP", "true").strip().lower()
    if disable_mcp not in ("0", "false", "no", "off"):
        # Avoid per-server partial overrides like
        # `mcp_servers.<name>.enabled=false`; some Codex CLI builds treat these
        # as incomplete server definitions and fail validation ("invalid transport").
        parts.extend(["-c", "mcp_servers={}"])

    raw = os.getenv("CODEX_HTTP_TRANSPORT_ONLY", "true").strip().lower()
    if raw not in ("0", "false", "no", "off"):
        alias = os.getenv("CODEX_SSE_PROVIDER_ID", "openai_sse").strip() or "openai_sse"
        display_name = (
            os.getenv("CODEX_MODEL_PROVIDER_NAME", "OpenAI (HTTP/SSE)").strip()
            or "OpenAI (HTTP/SSE)"
        )
        name_toml = json.dumps(display_name, ensure_ascii=False)
        parts.extend(
            [
                "-c",
                f"model_providers.{alias}.name={name_toml}",
                "-c",
                f"model_providers.{alias}.requires_openai_auth=true",
                "-c",
                f"model_providers.{alias}.wire_api=responses",
                "-c",
                f"model_providers.{alias}.supports_websockets=false",
                "-c",
                f"model_provider={alias}",
            ]
        )

    extra = os.getenv("CODEX_EXTRA_CONFIG", "").strip()
    if extra:
        for segment in extra.split(";"):
            segment = segment.strip()
            if segment:
                parts.extend(["-c", segment])
    return parts


def _codex_exec_permission_args() -> list[str]:
    """Build sandbox / approval flags for ``codex exec``."""
    bypass = os.getenv("CODEX_BYPASS_APPROVALS_AND_SANDBOX", "").strip().lower() in (
        "1",
        "true",
        "yes",
        "on",
    )
    parts_before_exec: list[str] = []
    parts_after_exec: list[str] = []
    if bypass:
        parts_after_exec.append("--dangerously-bypass-approvals-and-sandbox")

    sandbox_mode = os.getenv("CODEX_SANDBOX_MODE", "danger-full-access").strip()
    if sandbox_mode and not bypass:
        parts_after_exec.extend(["-s", sandbox_mode])

    approval_policy = os.getenv("CODEX_APPROVAL_POLICY", "never").strip()
    if approval_policy and not bypass:
        parts_before_exec.extend(["-a", approval_policy])
    return [*parts_before_exec, "exec", *parts_after_exec]


def _codex_chat_output_schema_args() -> list[str]:
    """
    Add ``--output-schema`` only for chat flows.

    This keeps planner/reviser prompts on their current free-form JSON contract while
    allowing chat-mode experiments with a structured final response.
    """
    enabled = os.getenv("CODEX_CHAT_USE_OUTPUT_SCHEMA", "true").strip().lower()
    if enabled in ("0", "false", "no", "off"):
        return []
    if not _CHAT_OUTPUT_SCHEMA_PATH.exists():
        logger.warning(
            "Chat output schema file is missing; skipping --output-schema path=%s",
            _CHAT_OUTPUT_SCHEMA_PATH,
        )
        return []
    return ["--output-schema", str(_CHAT_OUTPUT_SCHEMA_PATH)]


def _log_codex_exec_launch(argv: list[str]) -> None:
    logger.warning("Launching codex exec argv=%r", argv)


def _stdio_to_codex_result(stdout: bytes, stderr: bytes, returncode: int) -> str:
    out_text = stdout.decode("utf-8", errors="ignore").strip()
    err_text = stderr.decode("utf-8", errors="ignore").strip()
    if returncode != 0:
        raise CodexAdapterError(f"Codex command failed (code={returncode}): {err_text}")
    if not out_text:
        raise CodexAdapterError("Codex returned empty stdout.")
    return out_text


def _run_codex_subprocess_sync(argv: list[str], prompt: str, timeout_seconds: int) -> str:
    started = time.perf_counter()
    try:
        completed = subprocess.run(
            argv,
            input=prompt.encode("utf-8"),
            capture_output=True,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired as exc:
        elapsed = time.perf_counter() - started
        logger.error(
            "Codex subprocess timeout (sync) elapsed_s=%.2f timeout_s=%s prompt_chars=%s argv=%r",
            elapsed,
            timeout_seconds,
            len(prompt),
            argv,
        )
        raise CodexAdapterError(
            "Codex command timed out "
            f"(timeout_s={timeout_seconds}, elapsed_s={elapsed:.2f}, "
            f"prompt_chars={len(prompt)}, argv={argv!r})"
        ) from exc
    elapsed = time.perf_counter() - started
    logger.debug(
        "Codex subprocess done (sync) elapsed_s=%.2f prompt_chars=%s argv=%r",
        elapsed,
        len(prompt),
        argv,
    )
    return _stdio_to_codex_result(
        completed.stdout or b"",
        completed.stderr or b"",
        int(completed.returncode if completed.returncode is not None else 0),
    )


def _build_codex_argv(command: str, *subargs: str) -> list[str]:
    resolved = shutil.which(command.strip()) or command
    tail = list(subargs)
    if sys.platform == "win32":
        low = resolved.lower()
        if low.endswith((".cmd", ".bat")):
            return ["cmd.exe", "/c", resolved, *tail]
    return [resolved, *tail]


def _extract_usage_from_jsonl(raw: str) -> dict[str, int] | None:
    """Extract usage counters from ``codex exec --json`` events."""
    usage_found: dict[str, int] | None = None
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") != "turn.completed":
            continue
        usage = event.get("usage")
        if not isinstance(usage, dict):
            continue
        usage_found = {
            "input_tokens": int(usage.get("input_tokens", 0) or 0),
            "output_tokens": int(usage.get("output_tokens", 0) or 0),
            "cached_input_tokens": int(usage.get("cached_input_tokens", 0) or 0),
        }
    return usage_found


def _extract_last_agent_message_from_jsonl(raw: str) -> str:
    """Fallback: extract last ``agent_message`` text from ``--json`` stream."""
    last = ""
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") != "item.completed":
            continue
        item = event.get("item")
        if not isinstance(item, dict):
            continue
        if item.get("type") != "agent_message":
            continue
        text = str(item.get("text") or "").strip()
        if text:
            last = text
    return last


def _resolve_reply_from_json_mode(
    *,
    out_path: Path,
    stdout_text: str,
) -> str:
    """
    Resolve final reply text from JSON mode outputs.

    Priority:
    1) ``-o`` output file
    2) last ``agent_message`` from JSONL stream
    """
    reply = ""
    try:
        reply = out_path.read_text(encoding="utf-8", errors="replace").strip()
    except OSError:
        reply = ""
    if reply:
        return reply
    return _extract_last_agent_message_from_jsonl(stdout_text)


def _maybe_persist_jsonl_stream(stdout_text: str) -> None:
    if not stdout_text.strip():
        return
    jsonl_dir = os.getenv("CODEX_JSONL_OUT_DIR", "").strip()
    jsonl_tag = os.getenv("CODEX_JSONL_TAG", "").strip()
    fix_jsonl_utf8 = os.getenv("CODEX_JSONL_FIX_UTF8", "true").strip().lower() in (
        "1",
        "true",
        "yes",
    )
    jsonl_repo_root = Path(
        os.getenv("CODEX_JSONL_REPO_ROOT", os.getcwd())
    ).resolve()
    if not jsonl_dir:
        return
    try:
        out_dir = Path(jsonl_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        name = jsonl_tag or f"codex_exec_{int(time.time())}"
        payload = stdout_text.rstrip() + "\n"
        if fix_jsonl_utf8:
            payload = repair_jsonl_text(payload, repo_root=jsonl_repo_root)
        (out_dir / f"{name}.jsonl").write_text(
            payload, encoding="utf-8", errors="replace"
        )
    except Exception:
        pass


def _apply_jsonl_timing_fields(
    provider: "LegacyCodexProvider",
    *,
    started: float,
    first_event_at: float | None,
    turn_started_at: float | None,
    first_agent_at: float | None,
    turn_completed_at: float | None,
) -> None:
    if first_event_at is not None:
        provider.last_spawn_elapsed_s = max(0.0, first_event_at - started)
    if first_agent_at is not None:
        base = turn_started_at or first_event_at or started
        provider.last_ttft_elapsed_s = max(0.0, first_agent_at - base)
    if first_agent_at is not None and turn_completed_at is not None:
        provider.last_generation_elapsed_s = max(0.0, turn_completed_at - first_agent_at)
    end = time.perf_counter()
    if turn_completed_at is not None:
        provider.last_teardown_elapsed_s = max(0.0, end - turn_completed_at)


def _safe_json_loads(line: str) -> dict | None:
    try:
        obj = json.loads(line)
    except json.JSONDecodeError:
        return None
    return obj if isinstance(obj, dict) else None


def _stream_event_from_jsonl(
    *,
    line: str,
    seq: int,
    chat_id: str,
) -> dict[str, object] | None:
    event = _safe_json_loads(line)
    if event is None:
        return None
    etype = str(event.get("type") or "").strip()
    base: dict[str, object] = {
        "seq": seq,
        "chat_id": chat_id,
        "timestamp": time.time(),
        "raw": event,
    }
    if etype == "turn.started":
        return {"type": "turn.started", **base}
    if etype == "turn.completed":
        usage = event.get("usage")
        payload: dict[str, object] = {"type": "turn.completed", **base}
        if isinstance(usage, dict):
            payload["usage"] = {
                "input_tokens": int(usage.get("input_tokens", 0) or 0),
                "output_tokens": int(usage.get("output_tokens", 0) or 0),
                "cached_input_tokens": int(usage.get("cached_input_tokens", 0) or 0),
            }
        return payload
    if etype != "item.completed":
        return {"type": "event", "event_type": etype or "unknown", **base}
    item = event.get("item")
    if not isinstance(item, dict):
        return None
    item_type = str(item.get("type") or "").strip()
    if item_type == "agent_message":
        text = str(item.get("text") or "")
        return {"type": "agent.message.completed", "text": text, **base}
    if item_type == "reasoning":
        text = str(item.get("text") or "")
        return {"type": "reasoning.completed", "text": text, **base}
    if item_type == "command_execution":
        command = str(item.get("command") or "")
        aggregated_output = str(item.get("aggregated_output") or "")
        exit_code = item.get("exit_code")
        return {
            "type": "command.completed",
            "command": command,
            "exit_code": int(exit_code) if isinstance(exit_code, int) else exit_code,
            "output_preview": aggregated_output[-4000:] if aggregated_output else "",
            **base,
        }
    return {"type": "item.completed", "item_type": item_type or "unknown", **base}


@dataclass
class LegacyCodexProvider:
    """Run ``codex exec`` as a one-shot subprocess per prompt."""

    command: str = "codex"
    timeout_seconds: int = 180
    retry_count: int = 1
    model: str | None = None
    reasoning_effort: str | None = None
    last_exec_elapsed_s: float | None = None
    last_prompt_chars: int | None = None
    last_argv: tuple[str, ...] | None = None
    last_chat_prompt_build_elapsed_s: float | None = None
    last_chat_total_elapsed_s: float | None = None
    last_chat_prompt_text: str | None = None
    last_spawn_elapsed_s: float | None = None
    last_ttft_elapsed_s: float | None = None
    last_generation_elapsed_s: float | None = None
    last_teardown_elapsed_s: float | None = None
    last_input_tokens: int | None = None
    last_output_tokens: int | None = None
    last_cached_input_tokens: int | None = None
    last_skill_hints: list[str] | None = None
    last_raw_skill_plan: dict | None = None
    async_subprocess_supported: bool | None = None

    def _should_try_async_subprocess(self) -> bool:
        """
        Decide whether to attempt asyncio subprocess APIs.

        On Windows, Proactor/event-loop support can be inconsistent across runtimes.
        Default to sync subprocess there unless explicitly enabled.
        """
        if self.async_subprocess_supported is False:
            return False
        raw = os.getenv("CODEX_ASYNC_SUBPROCESS", "").strip().lower()
        if raw in ("1", "true", "yes", "on"):
            return True
        if raw in ("0", "false", "no", "off"):
            return False
        return sys.platform != "win32"

    async def generate_plan(
        self, question: str, schema_profile: dict, task_id: str = "unknown"
    ) -> AnalysisPlan:
        self.last_skill_hints = [SKILL_ANALYSIS_PLANNER]
        self.last_input_tokens = None
        self.last_output_tokens = None
        self.last_cached_input_tokens = None
        self.last_raw_skill_plan = None
        prompt = build_plan_prompt(
            question=question,
            schema_profile=schema_profile,
            skill_hint=f"${SKILL_ANALYSIS_PLANNER}",
        )
        last_error: Exception | None = None
        last_stdout: str | None = None
        for _ in range(self.retry_count + 1):
            raw: str | None = None
            try:
                raw, usage = await self._run_prompt_with_usage(prompt)
                if usage is not None:
                    self.last_input_tokens = usage.get("input_tokens")
                    self.last_output_tokens = usage.get("output_tokens")
                    self.last_cached_input_tokens = usage.get("cached_input_tokens")
                last_stdout = raw
                payload = extract_json_payload(raw)
                plan, raw_skill_plan = parse_plan_payload(payload)
                self.last_raw_skill_plan = raw_skill_plan
                save_snapshot(
                    task_id,
                    "codex_plan_call",
                    {
                        "prompt": prompt,
                        "skill_hints": self.last_skill_hints,
                        "raw_output": raw,
                        "parsed_result": payload,
                        "usage": usage or {},
                        "parse_success": True,
                    },
                )
                log_event(task_id, "plan", "codex_call", {"parse_success": True})
                return plan
            except Exception as exc:  # pragma: no cover - runtime path
                last_error = exc
                log_event(
                    task_id,
                    "plan",
                    "codex_call",
                    {
                        "skill_hints": self.last_skill_hints,
                        "parse_success": False,
                        "error": _format_exception_for_logs(exc),
                    },
                )
        assert last_error is not None
        detail = _format_exception_for_logs(last_error)
        if last_stdout is not None:
            detail = (
                f"{detail}\n\n--- codex stdout (first 2000 chars) ---\n"
                f"{last_stdout[:2000]}"
            )
        raise CodexAdapterError(f"Failed to generate plan:\n{detail}") from last_error

    async def generate_summary(
        self, goal: str, result_df_summary: dict, task_id: str = "unknown"
    ) -> str:
        self.last_skill_hints = None
        prompt = build_summary_prompt(goal=goal, result_summary=result_df_summary)
        raw = await self._run_prompt(prompt)
        save_snapshot(
            task_id,
            "codex_summary_call",
            {"prompt": prompt, "raw_output": raw, "parse_success": True},
        )
        log_event(task_id, "summary", "codex_call", {"parse_success": True})
        return raw.strip()

    async def generate_followups(
        self, goal: str, result_df_summary: dict, task_id: str = "unknown"
    ) -> list[str]:
        self.last_skill_hints = None
        prompt = build_followups_prompt(goal=goal, result_summary=result_df_summary)
        raw = await self._run_prompt(prompt)
        try:
            payload = extract_json_array_payload(raw)
            followups = [str(item) for item in payload][:3]
        except CodexAdapterError:
            followups = []
        save_snapshot(
            task_id,
            "codex_followups_call",
            {"prompt": prompt, "raw_output": raw, "parsed_result": followups},
        )
        return followups

    async def chat(
        self,
        message: str,
        history: list[dict],
        file_context: dict | None,
        task_id: str = "chat",
    ) -> str:
        chat_started = time.perf_counter()
        self.last_input_tokens = None
        self.last_output_tokens = None
        self.last_cached_input_tokens = None
        self.last_spawn_elapsed_s = None
        self.last_ttft_elapsed_s = None
        self.last_generation_elapsed_s = None
        self.last_teardown_elapsed_s = None
        self.last_skill_hints = [SKILL_DATA_CHAT]
        prompt_started = time.perf_counter()
        prompt = build_chat_prompt(
            message=message,
            history=history,
            file_context=file_context,
            skill_hint=f"${SKILL_DATA_CHAT}",
        )
        self.last_chat_prompt_text = prompt
        self.last_chat_prompt_build_elapsed_s = time.perf_counter() - prompt_started
        raw, usage = await self._run_prompt_with_usage(prompt)
        if usage is not None:
            self.last_input_tokens = usage.get("input_tokens")
            self.last_output_tokens = usage.get("output_tokens")
            self.last_cached_input_tokens = usage.get("cached_input_tokens")
        save_snapshot(
            task_id,
            "codex_chat_call",
            {
                "prompt": prompt,
                "skill_hints": self.last_skill_hints,
                "raw_output": raw,
                "parse_success": True,
                "usage": usage or {},
            },
        )
        log_event(task_id, "chat", "codex_call", {"parse_success": True})
        self.last_chat_total_elapsed_s = time.perf_counter() - chat_started
        return raw.strip()

    async def stream_chat(
        self,
        message: str,
        history: list[dict],
        file_context: dict | None,
        *,
        chat_id: str = "chat",
    ):
        self.last_input_tokens = None
        self.last_output_tokens = None
        self.last_cached_input_tokens = None
        self.last_spawn_elapsed_s = None
        self.last_ttft_elapsed_s = None
        self.last_generation_elapsed_s = None
        self.last_teardown_elapsed_s = None
        self.last_skill_hints = [SKILL_DATA_CHAT]
        prompt_started = time.perf_counter()
        prompt = build_chat_prompt(
            message=message,
            history=history,
            file_context=file_context,
            skill_hint=f"${SKILL_DATA_CHAT}",
        )
        self.last_chat_prompt_text = prompt
        self.last_chat_prompt_build_elapsed_s = time.perf_counter() - prompt_started
        async for event in self._run_prompt_with_usage_stream(prompt, chat_id=chat_id):
            yield event

    async def revise_plan(
        self,
        current_plan: AnalysisPlan,
        instruction: str,
        schema_profile: dict,
        task_id: str = "unknown",
    ) -> AnalysisPlan:
        self.last_skill_hints = [SKILL_PLAN_REVISER]
        self.last_input_tokens = None
        self.last_output_tokens = None
        self.last_cached_input_tokens = None
        self.last_raw_skill_plan = None
        prompt = build_revise_plan_prompt(
            current_plan=current_plan.model_dump(),
            instruction=instruction,
            schema_profile=schema_profile,
            skill_hint=f"${SKILL_PLAN_REVISER}",
        )
        last_error: Exception | None = None
        last_stdout: str | None = None
        for _ in range(self.retry_count + 1):
            raw: str | None = None
            try:
                raw, usage = await self._run_prompt_with_usage(prompt)
                if usage is not None:
                    self.last_input_tokens = usage.get("input_tokens")
                    self.last_output_tokens = usage.get("output_tokens")
                    self.last_cached_input_tokens = usage.get("cached_input_tokens")
                last_stdout = raw
                payload = extract_json_payload(raw)
                plan, raw_skill_plan = parse_plan_payload(payload)
                self.last_raw_skill_plan = raw_skill_plan
                save_snapshot(
                    task_id,
                    "codex_revise_call",
                    {
                        "prompt": prompt,
                        "skill_hints": self.last_skill_hints,
                        "raw_output": raw,
                        "parsed_result": payload,
                        "usage": usage or {},
                        "parse_success": True,
                    },
                )
                log_event(task_id, "plan", "codex_revise", {"parse_success": True})
                return plan
            except Exception as exc:  # pragma: no cover - runtime path
                last_error = exc
                log_event(
                    task_id,
                    "plan",
                    "codex_revise",
                    {
                        "skill_hints": self.last_skill_hints,
                        "parse_success": False,
                        "error": _format_exception_for_logs(exc),
                    },
                )
        assert last_error is not None
        detail = _format_exception_for_logs(last_error)
        if last_stdout is not None:
            detail = (
                f"{detail}\n\n--- codex stdout (first 2000 chars) ---\n"
                f"{last_stdout[:2000]}"
            )
        raise CodexAdapterError(f"Failed to revise plan:\n{detail}") from last_error

    async def _run_prompt_async_subprocess(self, argv: list[str], prompt: str) -> str:
        started = time.perf_counter()
        process = await asyncio.create_subprocess_exec(
            *argv,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(input=prompt.encode("utf-8")),
                timeout=self.timeout_seconds,
            )
        except asyncio.TimeoutError as exc:
            process.kill()
            await process.wait()
            elapsed = time.perf_counter() - started
            logger.error(
                "Codex subprocess timeout (async) elapsed_s=%.2f timeout_s=%s prompt_chars=%s argv=%r",
                elapsed,
                self.timeout_seconds,
                len(prompt),
                argv,
            )
            raise CodexAdapterError(
                "Codex command timed out "
                f"(timeout_s={self.timeout_seconds}, elapsed_s={elapsed:.2f}, "
                f"prompt_chars={len(prompt)}, argv={argv!r})"
            ) from exc
        elapsed = time.perf_counter() - started
        logger.debug(
            "Codex subprocess done (async) elapsed_s=%.2f prompt_chars=%s argv=%r",
            elapsed,
            len(prompt),
            argv,
        )
        return _stdio_to_codex_result(
            stdout or b"",
            stderr or b"",
            int(process.returncode if process.returncode is not None else 0),
        )

    async def _run_prompt(self, prompt: str) -> str:
        argv = _build_codex_argv(
            self.command,
            *_codex_exec_permission_args(),
            *_codex_exec_config_args(
                model_override=self.model,
                reasoning_override=self.reasoning_effort,
            ),
            "-",
        )
        _log_codex_exec_launch(argv)
        self.last_argv = tuple(argv)
        self.last_prompt_chars = len(prompt)
        started = time.perf_counter()
        use_async_subprocess = self._should_try_async_subprocess()
        try:
            if not use_async_subprocess:
                return await asyncio.to_thread(
                    _run_codex_subprocess_sync, argv, prompt, self.timeout_seconds
                )
            try:
                return await self._run_prompt_async_subprocess(argv, prompt)
            except (NotImplementedError, PermissionError):
                self.async_subprocess_supported = False
                return await asyncio.to_thread(
                    _run_codex_subprocess_sync, argv, prompt, self.timeout_seconds
                )
        finally:
            self.last_exec_elapsed_s = time.perf_counter() - started

    async def _run_prompt_with_usage(
        self, prompt: str
    ) -> tuple[str, dict[str, int] | None]:
        """Run ``codex exec`` and return (reply, usage tokens).

        By default we use ``--json`` so we can extract usage counters reliably.
        Some environments (notably Windows wrappers or very verbose JSONL event
        streams) can be unstable; set ``CODEX_USE_JSON_EVENTS=false`` to fall
        back to non-JSON execution (usage will be ``None``).
        """
        use_json = os.getenv("CODEX_USE_JSON_EVENTS", "true").strip().lower() in (
            "1",
            "true",
            "yes",
        )
        if not use_json:
            reply = await self._run_prompt(prompt)
            return reply, None
        with tempfile.NamedTemporaryFile(
            delete=False, prefix="codex-last-", suffix=".txt"
        ) as f:
            out_path = Path(f.name)
        try:
            argv = _build_codex_argv(
                self.command,
                *_codex_exec_permission_args(),
                "--json",
                "-o",
                str(out_path),
                *_codex_chat_output_schema_args(),
                *_codex_exec_config_args(
                    model_override=self.model,
                    reasoning_override=self.reasoning_effort,
                ),
                "-",
            )
            _log_codex_exec_launch(argv)
            self.last_argv = tuple(argv)
            self.last_prompt_chars = len(prompt)
            started = time.perf_counter()
            use_async_subprocess = self._should_try_async_subprocess()
            first_event_at: float | None = None
            turn_started_at: float | None = None
            first_agent_at: float | None = None
            turn_completed_at: float | None = None
            stdout_text = ""
            stderr_text = ""
            returncode = 0
            if not use_async_subprocess:
                # Keep the proven sync path on Windows; detailed phase timing may be unavailable.
                try:
                    completed = await asyncio.to_thread(
                        subprocess.run,
                        argv,
                        input=prompt.encode("utf-8"),
                        capture_output=True,
                        timeout=self.timeout_seconds,
                    )
                except subprocess.TimeoutExpired as exc:
                    elapsed = time.perf_counter() - started
                    raise CodexAdapterError(
                        "Codex command timed out "
                        f"(timeout_s={self.timeout_seconds}, elapsed_s={elapsed:.2f}, "
                        f"prompt_chars={len(prompt)}, argv={argv!r})"
                    ) from exc
                stdout_text = (completed.stdout or b"").decode("utf-8", errors="ignore")
                stderr_text = (completed.stderr or b"").decode("utf-8", errors="ignore").strip()
                returncode = int(
                    completed.returncode if completed.returncode is not None else 0
                )
            else:
                try:
                    process = await asyncio.create_subprocess_exec(
                        *argv,
                        stdin=asyncio.subprocess.PIPE,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE,
                    )
                    assert process.stdin is not None
                    process.stdin.write(prompt.encode("utf-8"))
                    await process.stdin.drain()
                    process.stdin.close()

                    loop = asyncio.get_running_loop()
                    deadline = loop.time() + float(self.timeout_seconds)
                    lines: list[str] = []
                    assert process.stdout is not None
                    while True:
                        remaining = deadline - loop.time()
                        if remaining <= 0:
                            process.kill()
                            await process.wait()
                            elapsed = time.perf_counter() - started
                            raise CodexAdapterError(
                                "Codex command timed out "
                                f"(timeout_s={self.timeout_seconds}, elapsed_s={elapsed:.2f}, "
                                f"prompt_chars={len(prompt)}, argv={argv!r})"
                            )
                        try:
                            raw_line = await asyncio.wait_for(
                                process.stdout.readline(), timeout=remaining
                            )
                        except asyncio.TimeoutError as exc:
                            process.kill()
                            await process.wait()
                            elapsed = time.perf_counter() - started
                            raise CodexAdapterError(
                                "Codex command timed out "
                                f"(timeout_s={self.timeout_seconds}, elapsed_s={elapsed:.2f}, "
                                f"prompt_chars={len(prompt)}, argv={argv!r})"
                            ) from exc
                        if not raw_line:
                            break
                        t = time.perf_counter()
                        if first_event_at is None:
                            first_event_at = t
                        line = raw_line.decode("utf-8", errors="ignore").rstrip("\r\n")
                        lines.append(line)
                        try:
                            event = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        et = event.get("type")
                        if et == "turn.started" and turn_started_at is None:
                            turn_started_at = t
                        elif et == "turn.completed":
                            turn_completed_at = t
                        elif et == "item.completed":
                            item = event.get("item")
                            if (
                                isinstance(item, dict)
                                and item.get("type") == "agent_message"
                                and first_agent_at is None
                            ):
                                first_agent_at = t

                    remaining = max(0.0, deadline - loop.time())
                    assert process.stderr is not None
                    stderr_bytes = await asyncio.wait_for(
                        process.stderr.read(), timeout=remaining if remaining > 0 else 0.01
                    )
                    await asyncio.wait_for(
                        process.wait(), timeout=max(0.01, deadline - loop.time())
                    )
                    returncode = int(
                        process.returncode if process.returncode is not None else 0
                    )
                    stdout_text = "\n".join(lines)
                    stderr_text = (stderr_bytes or b"").decode(
                        "utf-8", errors="ignore"
                    ).strip()
                except (NotImplementedError, PermissionError):
                    self.async_subprocess_supported = False
                    try:
                        completed = await asyncio.to_thread(
                            subprocess.run,
                            argv,
                            input=prompt.encode("utf-8"),
                            capture_output=True,
                            timeout=self.timeout_seconds,
                        )
                    except subprocess.TimeoutExpired as exc:
                        elapsed = time.perf_counter() - started
                        raise CodexAdapterError(
                            "Codex command timed out "
                            f"(timeout_s={self.timeout_seconds}, elapsed_s={elapsed:.2f}, "
                            f"prompt_chars={len(prompt)}, argv={argv!r})"
                        ) from exc
                    stdout_text = (completed.stdout or b"").decode(
                        "utf-8", errors="ignore"
                    )
                    stderr_text = (completed.stderr or b"").decode(
                        "utf-8", errors="ignore"
                    ).strip()
                    returncode = int(
                        completed.returncode if completed.returncode is not None else 0
                    )
            self.last_exec_elapsed_s = time.perf_counter() - started
            _maybe_persist_jsonl_stream(stdout_text)
            _apply_jsonl_timing_fields(
                self,
                started=started,
                first_event_at=first_event_at,
                turn_started_at=turn_started_at,
                first_agent_at=first_agent_at,
                turn_completed_at=turn_completed_at,
            )
            if returncode != 0:
                raise CodexAdapterError(
                    f"Codex command failed (code={returncode}): {stderr_text}"
                )
            usage = _extract_usage_from_jsonl(stdout_text)
            reply = _resolve_reply_from_json_mode(
                out_path=out_path,
                stdout_text=stdout_text,
            )
            if not reply:
                # Last-resort fallback: run without JSON mode to avoid hard failure
                # when upstream emits usage/events but no terminal agent message.
                logger.warning(
                    "JSON mode produced empty reply; falling back to plain exec argv=%r",
                    argv,
                )
                reply = await self._run_prompt(prompt)
                if not reply.strip():
                    raise CodexAdapterError("Codex returned empty reply in JSON mode.")
            return reply, usage
        finally:
            try:
                out_path.unlink(missing_ok=True)
            except OSError:
                pass

    async def _run_prompt_with_usage_stream(
        self,
        prompt: str,
        *,
        chat_id: str,
    ):
        use_json = os.getenv("CODEX_USE_JSON_EVENTS", "true").strip().lower() in (
            "1",
            "true",
            "yes",
        )
        if not use_json:
            raise CodexAdapterError("Streaming chat requires CODEX_USE_JSON_EVENTS=true.")
        with tempfile.NamedTemporaryFile(
            delete=False, prefix="codex-last-", suffix=".txt"
        ) as f:
            out_path = Path(f.name)
        yield {
            "type": "session.started",
            "chat_id": chat_id,
            "timestamp": time.time(),
        }
        stdout_lines: list[str] = []
        stderr_text = ""
        returncode = 0
        seq = 0
        started = time.perf_counter()
        first_event_at: float | None = None
        turn_started_at: float | None = None
        first_agent_at: float | None = None
        turn_completed_at: float | None = None
        try:
            argv = _build_codex_argv(
                self.command,
                *_codex_exec_permission_args(),
                "--json",
                "-o",
                str(out_path),
                *_codex_chat_output_schema_args(),
                *_codex_exec_config_args(
                    model_override=self.model,
                    reasoning_override=self.reasoning_effort,
                ),
                "-",
            )
            _log_codex_exec_launch(argv)
            self.last_argv = tuple(argv)
            self.last_prompt_chars = len(prompt)
            use_async_subprocess = self._should_try_async_subprocess()
            if not use_async_subprocess:
                logger.warning(
                    "Streaming chat falling back to buffered sync subprocess chat_id=%s argv=%r",
                    chat_id,
                    argv,
                )
                try:
                    completed = await asyncio.to_thread(
                        subprocess.run,
                        argv,
                        input=prompt.encode("utf-8"),
                        capture_output=True,
                        timeout=self.timeout_seconds,
                    )
                except subprocess.TimeoutExpired as exc:
                    elapsed = time.perf_counter() - started
                    raise CodexAdapterError(
                        "Codex command timed out "
                        f"(timeout_s={self.timeout_seconds}, elapsed_s={elapsed:.2f}, "
                        f"prompt_chars={len(prompt)}, argv={argv!r})"
                    ) from exc

                stdout_text = (completed.stdout or b"").decode("utf-8", errors="ignore")
                stderr_text = (completed.stderr or b"").decode("utf-8", errors="ignore").strip()
                returncode = int(
                    completed.returncode if completed.returncode is not None else 0
                )
                for line in stdout_text.splitlines():
                    observed_at = time.perf_counter()
                    event = _safe_json_loads(line)
                    if event is not None:
                        etype = str(event.get("type") or "").strip()
                        if first_event_at is None:
                            first_event_at = observed_at
                        if etype == "turn.started" and turn_started_at is None:
                            turn_started_at = observed_at
                        elif etype == "turn.completed":
                            turn_completed_at = observed_at
                        elif etype == "item.completed":
                            item = event.get("item")
                            if (
                                isinstance(item, dict)
                                and item.get("type") == "agent_message"
                                and first_agent_at is None
                            ):
                                first_agent_at = observed_at
                    normalized = _stream_event_from_jsonl(
                        line=line,
                        seq=seq,
                        chat_id=chat_id,
                    )
                    seq += 1
                    if normalized is not None:
                        yield normalized

                self.last_exec_elapsed_s = time.perf_counter() - started
                _maybe_persist_jsonl_stream(stdout_text)
                _apply_jsonl_timing_fields(
                    self,
                    started=started,
                    first_event_at=first_event_at,
                    turn_started_at=turn_started_at,
                    first_agent_at=first_agent_at,
                    turn_completed_at=turn_completed_at,
                )
                if returncode != 0:
                    raise CodexAdapterError(
                        f"Codex command failed (code={returncode}): {stderr_text}"
                    )
                usage = _extract_usage_from_jsonl(stdout_text)
                if usage is not None:
                    self.last_input_tokens = usage.get("input_tokens")
                    self.last_output_tokens = usage.get("output_tokens")
                    self.last_cached_input_tokens = usage.get("cached_input_tokens")
                reply = ""
                try:
                    reply = out_path.read_text(encoding="utf-8", errors="replace").strip()
                except OSError:
                    reply = ""
                if not reply:
                    reply = _extract_last_agent_message_from_jsonl(stdout_text)
                if not reply:
                    raise CodexAdapterError("Codex returned empty reply in JSON mode.")
                yield {
                    "type": "final",
                    "chat_id": chat_id,
                    "timestamp": time.time(),
                    "reply": reply,
                    "usage": usage or {},
                    "timing": {
                        "codex_exec_elapsed_s": self.last_exec_elapsed_s,
                        "codex_spawn_elapsed_s": self.last_spawn_elapsed_s,
                        "codex_ttft_elapsed_s": self.last_ttft_elapsed_s,
                        "codex_generation_elapsed_s": self.last_generation_elapsed_s,
                        "codex_teardown_elapsed_s": self.last_teardown_elapsed_s,
                        "prompt_build_elapsed_s": self.last_chat_prompt_build_elapsed_s,
                    },
                    "prompt_chars": self.last_prompt_chars,
                    "debug_prompt": self.last_chat_prompt_text,
                    "skill_hints": self.last_skill_hints,
                }
                return
            try:
                process = await asyncio.create_subprocess_exec(
                    *argv,
                    stdin=asyncio.subprocess.PIPE,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
            except (NotImplementedError, PermissionError):
                self.async_subprocess_supported = False
                logger.warning(
                    "Streaming chat async subprocess unsupported; using buffered sync chat_id=%s argv=%r",
                    chat_id,
                    argv,
                )
                completed = await asyncio.to_thread(
                    subprocess.run,
                    argv,
                    input=prompt.encode("utf-8"),
                    capture_output=True,
                    timeout=self.timeout_seconds,
                )
                stdout_text = (completed.stdout or b"").decode("utf-8", errors="ignore")
                stderr_text = (completed.stderr or b"").decode("utf-8", errors="ignore").strip()
                returncode = int(
                    completed.returncode if completed.returncode is not None else 0
                )
                for line in stdout_text.splitlines():
                    observed_at = time.perf_counter()
                    event = _safe_json_loads(line)
                    if event is not None:
                        etype = str(event.get("type") or "").strip()
                        if first_event_at is None:
                            first_event_at = observed_at
                        if etype == "turn.started" and turn_started_at is None:
                            turn_started_at = observed_at
                        elif etype == "turn.completed":
                            turn_completed_at = observed_at
                        elif etype == "item.completed":
                            item = event.get("item")
                            if (
                                isinstance(item, dict)
                                and item.get("type") == "agent_message"
                                and first_agent_at is None
                            ):
                                first_agent_at = observed_at
                    normalized = _stream_event_from_jsonl(line=line, seq=seq, chat_id=chat_id)
                    seq += 1
                    if normalized is not None:
                        yield normalized
                self.last_exec_elapsed_s = time.perf_counter() - started
                _maybe_persist_jsonl_stream(stdout_text)
                _apply_jsonl_timing_fields(
                    self,
                    started=started,
                    first_event_at=first_event_at,
                    turn_started_at=turn_started_at,
                    first_agent_at=first_agent_at,
                    turn_completed_at=turn_completed_at,
                )
                if returncode != 0:
                    raise CodexAdapterError(
                        f"Codex command failed (code={returncode}): {stderr_text}"
                    )
                usage = _extract_usage_from_jsonl(stdout_text)
                if usage is not None:
                    self.last_input_tokens = usage.get("input_tokens")
                    self.last_output_tokens = usage.get("output_tokens")
                    self.last_cached_input_tokens = usage.get("cached_input_tokens")
                reply = _resolve_reply_from_json_mode(
                    out_path=out_path,
                    stdout_text=stdout_text,
                )
                if not reply:
                    logger.warning(
                        "Streaming JSON mode produced empty reply; falling back to plain exec argv=%r",
                        argv,
                    )
                    reply = await self._run_prompt(prompt)
                    if not reply.strip():
                        raise CodexAdapterError("Codex returned empty reply in JSON mode.")
                yield {
                    "type": "final",
                    "chat_id": chat_id,
                    "timestamp": time.time(),
                    "reply": reply,
                    "usage": usage or {},
                    "timing": {
                        "codex_exec_elapsed_s": self.last_exec_elapsed_s,
                        "codex_spawn_elapsed_s": self.last_spawn_elapsed_s,
                        "codex_ttft_elapsed_s": self.last_ttft_elapsed_s,
                        "codex_generation_elapsed_s": self.last_generation_elapsed_s,
                        "codex_teardown_elapsed_s": self.last_teardown_elapsed_s,
                        "prompt_build_elapsed_s": self.last_chat_prompt_build_elapsed_s,
                    },
                    "prompt_chars": self.last_prompt_chars,
                    "debug_prompt": self.last_chat_prompt_text,
                    "skill_hints": self.last_skill_hints,
                }
                return
            assert process.stdin is not None
            process.stdin.write(prompt.encode("utf-8"))
            await process.stdin.drain()
            process.stdin.close()

            loop = asyncio.get_running_loop()
            deadline = loop.time() + float(self.timeout_seconds)
            assert process.stdout is not None
            while True:
                remaining = deadline - loop.time()
                if remaining <= 0:
                    process.kill()
                    await process.wait()
                    elapsed = time.perf_counter() - started
                    raise CodexAdapterError(
                        "Codex command timed out "
                        f"(timeout_s={self.timeout_seconds}, elapsed_s={elapsed:.2f}, "
                        f"prompt_chars={len(prompt)}, argv={argv!r})"
                    )
                try:
                    raw_line = await asyncio.wait_for(
                        process.stdout.readline(), timeout=remaining
                    )
                except asyncio.TimeoutError as exc:
                    process.kill()
                    await process.wait()
                    elapsed = time.perf_counter() - started
                    raise CodexAdapterError(
                        "Codex command timed out "
                        f"(timeout_s={self.timeout_seconds}, elapsed_s={elapsed:.2f}, "
                        f"prompt_chars={len(prompt)}, argv={argv!r})"
                    ) from exc
                if not raw_line:
                    break
                observed_at = time.perf_counter()
                if first_event_at is None:
                    first_event_at = observed_at
                line = raw_line.decode("utf-8", errors="ignore").rstrip("\r\n")
                stdout_lines.append(line)
                event = _safe_json_loads(line)
                if event is not None:
                    etype = str(event.get("type") or "").strip()
                    if etype == "turn.started" and turn_started_at is None:
                        turn_started_at = observed_at
                    elif etype == "turn.completed":
                        turn_completed_at = observed_at
                    elif etype == "item.completed":
                        item = event.get("item")
                        if (
                            isinstance(item, dict)
                            and item.get("type") == "agent_message"
                            and first_agent_at is None
                        ):
                            first_agent_at = observed_at
                normalized = _stream_event_from_jsonl(line=line, seq=seq, chat_id=chat_id)
                seq += 1
                if normalized is not None:
                    yield normalized

            remaining = max(0.0, deadline - loop.time())
            assert process.stderr is not None
            stderr_bytes = await asyncio.wait_for(
                process.stderr.read(), timeout=remaining if remaining > 0 else 0.01
            )
            await asyncio.wait_for(
                process.wait(), timeout=max(0.01, deadline - loop.time())
            )
            returncode = int(process.returncode if process.returncode is not None else 0)
            stderr_text = (stderr_bytes or b"").decode("utf-8", errors="ignore").strip()
            stdout_text = "\n".join(stdout_lines)
            self.last_exec_elapsed_s = time.perf_counter() - started
            _maybe_persist_jsonl_stream(stdout_text)
            _apply_jsonl_timing_fields(
                self,
                started=started,
                first_event_at=first_event_at,
                turn_started_at=turn_started_at,
                first_agent_at=first_agent_at,
                turn_completed_at=turn_completed_at,
            )
            if returncode != 0:
                raise CodexAdapterError(
                    f"Codex command failed (code={returncode}): {stderr_text}"
                )
            usage = _extract_usage_from_jsonl(stdout_text)
            if usage is not None:
                self.last_input_tokens = usage.get("input_tokens")
                self.last_output_tokens = usage.get("output_tokens")
                self.last_cached_input_tokens = usage.get("cached_input_tokens")
                reply = _resolve_reply_from_json_mode(
                    out_path=out_path,
                    stdout_text=stdout_text,
                )
                if not reply:
                    logger.warning(
                        "Streaming JSON mode produced empty reply after async run; falling back to plain exec argv=%r",
                        argv,
                    )
                    reply = await self._run_prompt(prompt)
                    if not reply.strip():
                        raise CodexAdapterError("Codex returned empty reply in JSON mode.")
                yield {
                    "type": "final",
                    "chat_id": chat_id,
                    "timestamp": time.time(),
                    "reply": reply,
                "usage": usage or {},
                "timing": {
                    "codex_exec_elapsed_s": self.last_exec_elapsed_s,
                    "codex_spawn_elapsed_s": self.last_spawn_elapsed_s,
                    "codex_ttft_elapsed_s": self.last_ttft_elapsed_s,
                    "codex_generation_elapsed_s": self.last_generation_elapsed_s,
                    "codex_teardown_elapsed_s": self.last_teardown_elapsed_s,
                    "prompt_build_elapsed_s": self.last_chat_prompt_build_elapsed_s,
                },
                "prompt_chars": self.last_prompt_chars,
                "debug_prompt": self.last_chat_prompt_text,
                "skill_hints": self.last_skill_hints,
            }
        except Exception as exc:
            yield {
                "type": "error",
                "chat_id": chat_id,
                "timestamp": time.time(),
                "error": _format_exception_for_logs(exc),
            }
            raise
        finally:
            with contextlib.suppress(OSError):
                out_path.unlink(missing_ok=True)


_LEGACY_SINGLETON: LegacyCodexProvider | None = None


def get_legacy_codex_provider() -> LegacyCodexProvider:
    """Process-wide singleton for scripts expecting a stable adapter instance."""
    global _LEGACY_SINGLETON
    if _LEGACY_SINGLETON is None:
        command = resolve_codex_executable()
        timeout_seconds = int(os.getenv("CODEX_TIMEOUT_SECONDS", "180"))
        retry_count = int(os.getenv("CODEX_RETRY_COUNT", "1"))
        _LEGACY_SINGLETON = LegacyCodexProvider(
            command=command,
            timeout_seconds=timeout_seconds,
            retry_count=retry_count,
        )
    return _LEGACY_SINGLETON
