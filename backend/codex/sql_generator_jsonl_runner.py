"""Run `codex exec --json` for sql-generator eval cases (shared by CLI + Streamlit + E2E)."""

from __future__ import annotations

import json
import subprocess
import tempfile
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from backend.codex.jsonl_encoding_fix import repair_jsonl_text
from backend.codex.xinfei_sso import resolve_codex_executable

Mode = Literal["raw", "hint"]


@dataclass(frozen=True)
class SqlGeneratorJsonStreamResult:
    """Outcome of a single `codex exec --json` run for one case + mode."""

    argv: list[str]
    case_id: str
    mode: Mode
    jsonl_text: str
    last_message: str
    stderr: str
    elapsed_s: float
    returncode: int
    jsonl_path: Path | None
    last_message_path: Path | None


def load_cases_dicts(cases_path: Path) -> list[dict[str, Any]]:
    return json.loads(cases_path.read_text(encoding="utf-8"))


def load_case(cases_path: Path, case_id: str) -> dict[str, Any]:
    for c in load_cases_dicts(cases_path):
        if c.get("id") == case_id:
            return c
    raise KeyError(f"Unknown case id: {case_id}")


def build_prompt(*, business_request: str, mode: Mode) -> str:
    hint = "Skill hint: $sql-generator\n\n" if mode == "hint" else ""
    return (
        "You are a senior data analyst writing ODPS SQL.\n"
        + hint
        + "CRITICAL OUTPUT RULES:\n"
        + "- Output ONLY the SQL script.\n"
        + "- No markdown, no code fences, no explanations.\n"
        + "- Use ODPS-compatible SQL style.\n"
        + "- Use placeholders like ${bizdate} when date partition is required.\n"
        + "- If you need MAX_PT(...) per local convention, include it.\n\n"
        + "Business request (written by a stakeholder):\n"
        + business_request.strip()
        + "\n"
    )


def _run_codex_sql_generator_prompt(
    *,
    repo_root: Path,
    case_id: str,
    mode: Mode,
    prompt: str,
    timeout_s: int,
    out_dir: Path | None,
    fix_shell_utf8: bool,
    sandbox_mode: str | None,
    approval_policy: str | None,
    bypass_sandbox: bool,
    codex_config_overrides: list[str] | None,
) -> SqlGeneratorJsonStreamResult:
    codex = resolve_codex_executable()

    jsonl_path: Path | None = None
    last_msg_path: Path | None = None
    out_dir_resolved: Path | None = None
    if out_dir is not None:
        out_dir_resolved = out_dir.resolve()
        out_dir_resolved.mkdir(parents=True, exist_ok=True)
        jsonl_path = out_dir_resolved / f"codex_exec__{case_id}__{mode}.jsonl"
        last_msg_path = out_dir_resolved / f"codex_last_message__{case_id}__{mode}.txt"

    tmp_last: Path | None = None
    if last_msg_path is None:
        with tempfile.NamedTemporaryFile(
            mode="w+b", delete=False, prefix="codex-last-", suffix=".txt"
        ) as tmp:
            tmp_last = Path(tmp.name)
    out_for_codex_path = last_msg_path if last_msg_path is not None else tmp_last
    assert out_for_codex_path is not None

    try:
        out_for_codex = str(out_for_codex_path)
        argv: list[str] = [codex]
        if bypass_sandbox:
            # Codex CLI forbids combining bypass flag with explicit approval policy.
            argv.append("--dangerously-bypass-approvals-and-sandbox")
        else:
            if approval_policy:
                argv.extend(["-a", approval_policy])
        argv.append("exec")
        if not bypass_sandbox:
            if sandbox_mode:
                argv.extend(["-s", sandbox_mode])
        for override in codex_config_overrides or []:
            if (override or "").strip():
                argv.extend(["-c", override.strip()])
        argv.extend(
            [
                "--json",
                "-o",
                out_for_codex,
                "-",
            ]
        )
        t0 = time.perf_counter()
        completed_stdout: bytes = b""
        completed_stderr: bytes = b""
        completed_rc = 0
        timed_out = False
        try:
            # Keep timeout cleanup and stream reads under our control so we can
            # provide live diagnostics and avoid Windows cleanup hangs.
            proc = subprocess.Popen(
                argv,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            if proc.stdin is not None:
                proc.stdin.write(prompt.encode("utf-8"))
                proc.stdin.close()

            out_buf = bytearray()
            err_buf = bytearray()
            state_lock = threading.Lock()
            reconnect_count = 0
            saw_transport_fallback = False
            saw_turn_completed = False

            def _drain(pipe: Any, sink: bytearray, *, stream_name: str) -> None:
                nonlocal reconnect_count, saw_transport_fallback, saw_turn_completed
                pending = b""
                while True:
                    chunk = pipe.read(4096)
                    if not chunk:
                        break
                    sink.extend(chunk)
                    pending += chunk
                    while True:
                        nl = pending.find(b"\n")
                        if nl < 0:
                            break
                        line = pending[:nl]
                        pending = pending[nl + 1 :]
                        text = line.decode("utf-8", errors="replace").rstrip()
                        if text:
                            if stream_name == "stdout":
                                if "Reconnecting..." in text:
                                    with state_lock:
                                        reconnect_count += 1
                                if "Falling back from WebSockets to HTTPS transport" in text:
                                    with state_lock:
                                        saw_transport_fallback = True
                                if '"type":"turn.completed"' in text:
                                    with state_lock:
                                        saw_turn_completed = True
                            print(f"[codex-runner][{stream_name}] {text}", flush=True)
                if pending:
                    text = pending.decode("utf-8", errors="replace").rstrip()
                    if text:
                        print(f"[codex-runner][{stream_name}] {text}", flush=True)

            out_thread = threading.Thread(
                target=_drain,
                args=(proc.stdout, out_buf),
                kwargs={"stream_name": "stdout"},
                daemon=True,
            )
            err_thread = threading.Thread(
                target=_drain,
                args=(proc.stderr, err_buf),
                kwargs={"stream_name": "stderr"},
                daemon=True,
            )
            out_thread.start()
            err_thread.start()

            deadline = t0 + float(timeout_s)
            heartbeat_s = 10.0
            deadline_extended = False
            reconnect_grace_s = 180.0
            while True:
                rc_now = proc.poll()
                if rc_now is not None:
                    completed_rc = int(rc_now)
                    break
                with state_lock:
                    reconnect_now = reconnect_count
                    fallback_now = saw_transport_fallback
                    turn_completed_now = saw_turn_completed
                if (
                    (reconnect_now >= 2 or fallback_now)
                    and not turn_completed_now
                    and not deadline_extended
                ):
                    deadline += reconnect_grace_s
                    deadline_extended = True
                    new_remaining = max(0.0, deadline - time.perf_counter())
                    print(
                        (
                            "[codex-runner] transport fallback detected; "
                            f"extending timeout by {int(reconnect_grace_s)}s "
                            f"(new_remaining={new_remaining:.0f}s)"
                        ),
                        flush=True,
                    )
                now = time.perf_counter()
                remaining = deadline - now
                if remaining <= 0:
                    timed_out = True
                    break

                wait_s = heartbeat_s if remaining > heartbeat_s else remaining
                time.sleep(wait_s)
                if wait_s == heartbeat_s:
                    elapsed_heartbeat = time.perf_counter() - t0
                    out_size = len(out_buf)
                    err_size = len(err_buf)
                    out_file_size = (
                        out_for_codex_path.stat().st_size if out_for_codex_path.exists() else 0
                    )
                    print(
                        (
                            "[codex-runner] still running "
                            f"case={case_id} mode={mode} "
                            f"elapsed={elapsed_heartbeat:.0f}s timeout={timeout_s}s "
                            f"stdout={out_size}B stderr={err_size}B last_msg_file={out_file_size}B"
                        ),
                        flush=True,
                    )

            if timed_out:
                elapsed = time.perf_counter() - t0
                # On Windows, codex.cmd may spawn child processes; kill process tree.
                kill_note = ""
                try:
                    subprocess.run(
                        ["taskkill", "/PID", str(proc.pid), "/T", "/F"],
                        capture_output=True,
                        timeout=5,
                        check=False,
                    )
                    kill_note = "[kill] taskkill /T /F issued\n"
                except OSError as exc:
                    kill_note = f"[kill] taskkill failed: {exc}\n"
                    try:
                        proc.kill()
                    except OSError:
                        pass
                except subprocess.TimeoutExpired:
                    kill_note = "[kill] taskkill timeout after 5s\n"
                    try:
                        proc.kill()
                    except OSError:
                        pass

                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    pass

                out_thread.join(timeout=3)
                err_thread.join(timeout=3)
                partial_out = bytes(out_buf).decode("utf-8", errors="replace")
                partial_err = bytes(err_buf).decode("utf-8", errors="replace")
                partial_jsonl_text = (
                    repair_jsonl_text(partial_out, repo_root=repo_root.resolve())
                    if fix_shell_utf8
                    else partial_out
                )
                if jsonl_path is not None:
                    try:
                        jsonl_path.write_text(partial_jsonl_text, encoding="utf-8", newline="\n")
                    except OSError:
                        pass
                stderr = f"[argv] {json.dumps(argv, ensure_ascii=False)}\n"
                stderr += f"[timeout] timed out after {timeout_s}s\n"
                stderr += kill_note
                stderr += (
                    "[stream_state] "
                    f"stdout_bytes={len(out_buf)} stderr_bytes={len(err_buf)} "
                    f"stdout_thread_alive={out_thread.is_alive()} "
                    f"stderr_thread_alive={err_thread.is_alive()}\n"
                )
                if partial_err.strip():
                    stderr += f"\n[partial_stderr]\n{partial_err}\n"
                if partial_out.strip():
                    stderr += f"\n[partial_stdout]\n{partial_out}\n"
                if out_dir_resolved:
                    stderr_path = out_dir_resolved / f"codex_stderr__{case_id}__{mode}.txt"
                    try:
                        stderr_path.write_text(stderr, encoding="utf-8", newline="\n")
                    except OSError:
                        pass
                return SqlGeneratorJsonStreamResult(
                    argv=argv,
                    case_id=case_id,
                    mode=mode,
                    jsonl_text=partial_jsonl_text,
                    last_message="",
                    stderr=stderr,
                    elapsed_s=elapsed,
                    returncode=124,
                    jsonl_path=jsonl_path,
                    last_message_path=last_msg_path,
                )
            out_thread.join(timeout=3)
            err_thread.join(timeout=3)
            completed_stdout = bytes(out_buf)
            completed_stderr = bytes(err_buf)
            if completed_rc == 0 and proc.returncode is not None:
                completed_rc = int(proc.returncode)
        except OSError as exc:
            elapsed = time.perf_counter() - t0
            stderr = f"[argv] {json.dumps(argv, ensure_ascii=False)}\n"
            stderr += "[spawn_error] failed to start or communicate with subprocess\n"
            stderr += f"[exception] {exc}\n"
            if out_dir_resolved:
                stderr_path = out_dir_resolved / f"codex_stderr__{case_id}__{mode}.txt"
                try:
                    stderr_path.write_text(stderr, encoding="utf-8", newline="\n")
                except OSError:
                    pass
            return SqlGeneratorJsonStreamResult(
                argv=argv,
                case_id=case_id,
                mode=mode,
                jsonl_text="",
                last_message="",
                stderr=stderr,
                elapsed_s=elapsed,
                returncode=125,
                jsonl_path=jsonl_path,
                last_message_path=last_msg_path,
            )
        elapsed = time.perf_counter() - t0

        jsonl_raw = completed_stdout.decode("utf-8", errors="replace")
        jsonl_text = (
            repair_jsonl_text(jsonl_raw, repo_root=repo_root.resolve())
            if fix_shell_utf8
            else jsonl_raw
        )

        if jsonl_path is not None:
            jsonl_path.write_text(jsonl_text, encoding="utf-8", newline="\n")

        last_msg_file = out_for_codex_path
        last_message = ""
        try:
            last_message = last_msg_file.read_text(encoding="utf-8", errors="replace").strip()
        except OSError:
            pass

        stderr = completed_stderr.decode("utf-8", errors="replace")
        stderr = (
            f"[argv] {json.dumps(argv, ensure_ascii=False)}\n"
            + stderr
            + f"\n\n[exit_code]={completed_rc} elapsed_s={elapsed:.3f}\n"
        )

        if json_dir := out_dir_resolved:
            stderr_path = json_dir / f"codex_stderr__{case_id}__{mode}.txt"
            try:
                stderr_path.write_text(stderr, encoding="utf-8", newline="\n")
            except OSError:
                pass

        rc = completed_rc
        return SqlGeneratorJsonStreamResult(
            argv=argv,
            case_id=case_id,
            mode=mode,
            jsonl_text=jsonl_text,
            last_message=last_message,
            stderr=stderr,
            elapsed_s=elapsed,
            returncode=rc,
            jsonl_path=jsonl_path,
            last_message_path=last_msg_path,
        )
    finally:
        if tmp_last is not None:
            tmp_last.unlink(missing_ok=True)


def run_codex_json_stream_raw_prompt(
    *,
    repo_root: Path,
    run_id: str,
    prompt: str,
    mode: Mode = "raw",
    timeout_s: int = 300,
    out_dir: Path | None = None,
    fix_shell_utf8: bool = True,
    sandbox_mode: str | None = None,
    approval_policy: str | None = None,
    bypass_sandbox: bool = False,
    codex_config_overrides: list[str] | None = None,
) -> SqlGeneratorJsonStreamResult:
    """Run ``codex exec --json`` with a **fully custom** prompt (e.g. multi-skill serial instructions).

    Artifact names use ``run_id`` and ``mode`` (default ``raw``) like other runners.
    """
    if not (prompt or "").strip():
        raise ValueError("prompt is empty")
    return _run_codex_sql_generator_prompt(
        repo_root=repo_root,
        case_id=run_id,
        mode=mode,
        prompt=prompt,
        timeout_s=timeout_s,
        out_dir=out_dir,
        fix_shell_utf8=fix_shell_utf8,
        sandbox_mode=sandbox_mode,
        approval_policy=approval_policy,
        bypass_sandbox=bypass_sandbox,
        codex_config_overrides=codex_config_overrides,
    )


def run_sql_generator_json_stream_inline(
    *,
    repo_root: Path,
    case_id: str,
    business_request: str,
    mode: Mode,
    timeout_s: int = 300,
    out_dir: Path | None = None,
    fix_shell_utf8: bool = True,
    sandbox_mode: str | None = None,
    approval_policy: str | None = None,
    bypass_sandbox: bool = False,
    codex_config_overrides: list[str] | None = None,
) -> SqlGeneratorJsonStreamResult:
    """Like :func:`run_sql_generator_json_stream` but takes NL directly (no cases JSON lookup)."""
    if not business_request.strip():
        raise ValueError("business_request is empty")
    prompt = build_prompt(business_request=business_request, mode=mode)
    return _run_codex_sql_generator_prompt(
        repo_root=repo_root,
        case_id=case_id,
        mode=mode,
        prompt=prompt,
        timeout_s=timeout_s,
        out_dir=out_dir,
        fix_shell_utf8=fix_shell_utf8,
        sandbox_mode=sandbox_mode,
        approval_policy=approval_policy,
        bypass_sandbox=bypass_sandbox,
        codex_config_overrides=codex_config_overrides,
    )


def run_sql_generator_json_stream(
    *,
    repo_root: Path,
    case_id: str,
    mode: Mode,
    cases_relative: str = "tests/sql_generator_eval_cases.json",
    timeout_s: int = 300,
    out_dir: Path | None = None,
    fix_shell_utf8: bool = True,
    sandbox_mode: str | None = None,
    approval_policy: str | None = None,
    bypass_sandbox: bool = False,
    codex_config_overrides: list[str] | None = None,
) -> SqlGeneratorJsonStreamResult:
    """Spawn `codex exec --json`, return stdout JSONL (optionally repaired) and paths if ``out_dir`` set."""
    cases_path = repo_root / cases_relative
    case = load_case(cases_path, case_id)
    br = case.get("business_request")
    if not isinstance(br, str) or not br.strip():
        raise ValueError(f"Case {case_id!r} has no business_request")
    prompt = build_prompt(business_request=br, mode=mode)
    return _run_codex_sql_generator_prompt(
        repo_root=repo_root,
        case_id=case_id,
        mode=mode,
        prompt=prompt,
        timeout_s=timeout_s,
        out_dir=out_dir,
        fix_shell_utf8=fix_shell_utf8,
        sandbox_mode=sandbox_mode,
        approval_policy=approval_policy,
        bypass_sandbox=bypass_sandbox,
        codex_config_overrides=codex_config_overrides,
    )
