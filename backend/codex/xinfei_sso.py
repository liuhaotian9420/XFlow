"""Xinfei enterprise Codex install detection, CLI path resolution, and SSO checks."""

from __future__ import annotations

import logging
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

ENTERPRISE_SSO_MARKER = "Logged in using Enterprise SSO"

_sso_gate_done: bool = False


def _is_truthy_env(name: str, default: str = "") -> bool:
    return os.getenv(name, default).strip().lower() in ("1", "true", "yes", "on")


def resolve_xinfei_binary() -> str | None:
    """Return an absolute path to Xinfei enterprise ``codex`` binary when discoverable."""
    direct = os.getenv("XINFEI_CODEX_BINARY", "").strip()
    if direct:
        p = Path(direct).expanduser()
        if p.is_file():
            return str(p.resolve())
        logger.warning("XINFEI_CODEX_BINARY points to a missing file (%s); ignoring.", direct)

    home = os.getenv("XINFEI_CODEX_HOME", "").strip()
    if home:
        root = Path(home).expanduser()
        filename = "codex.exe" if sys.platform == "win32" else "codex"
        p = root / "bin" / filename
        if p.is_file():
            return str(p.resolve())
        logger.warning(
            "XINFEI_CODEX_HOME does not contain expected binary at %s; ignoring.",
            p,
        )

    if sys.platform == "win32":
        base = os.environ.get("LOCALAPPDATA", "").strip()
        if base:
            candidate = Path(base) / "Programs" / "XinfeiCodex" / "bin" / "codex.exe"
            if candidate.is_file():
                return str(candidate.resolve())

        # Support portable enterprise packages such as:
        # C:\Users\<user>\Documents\codex-enterprise-1.0.3-windows-x64-gnu\bin\codex.exe
        user_profile = os.environ.get("USERPROFILE", "").strip()
        if user_profile:
            docs = Path(user_profile) / "Documents"
            pattern = re.compile(r"^codex-enterprise-\d+\.\d+\.\d+-windows-.*$")
            portable_candidates: list[Path] = []
            if docs.is_dir():
                for folder in docs.iterdir():
                    if not folder.is_dir() or not pattern.match(folder.name.lower()):
                        continue
                    p = folder / "bin" / "codex.exe"
                    if p.is_file():
                        portable_candidates.append(p)
            if portable_candidates:
                portable_candidates.sort(
                    key=lambda x: x.stat().st_mtime, reverse=True
                )
                return str(portable_candidates[0].resolve())

    return None


def resolve_codex_executable() -> str:
    """Resolve the Codex CLI used for ``codex exec``."""
    raw_bin = os.getenv("CODEX_BINARY", "").strip()
    if raw_bin:
        p = Path(raw_bin).expanduser()
        if p.is_file():
            return str(p.resolve())
        logger.warning("CODEX_BINARY points to a missing file (%s); ignoring.", raw_bin)

    cli = os.getenv("CODEX_CLI_COMMAND", "").strip()
    if cli:
        low = cli.lower()
        if low.endswith(".ps1"):
            # If the user points to a PowerShell wrapper, prefer the underlying
            # enterprise binary for subprocess compatibility.
            inner = resolve_xinfei_binary()
            if inner is not None:
                return inner
            resolved = shutil.which(cli)
            return resolved if resolved else cli
        if low.endswith((".cmd", ".bat", ".ps1")):
            inner = resolve_xinfei_binary()
            if inner is not None:
                logger.info(
                    "CODEX_CLI_COMMAND is a shell wrapper (%s); using Xinfei binary %s",
                    cli,
                    inner,
                )
                return inner
            p = Path(cli).expanduser()
            if p.is_file():
                return str(p.resolve())
            resolved = shutil.which(cli)
            return resolved if resolved else cli

        if low.endswith(".exe"):
            p = Path(cli).expanduser()
            if p.is_file():
                return str(p.resolve())
            resolved = shutil.which(cli)
            return resolved if resolved else cli

        resolved = shutil.which(cli)
        return resolved if resolved else cli

    inner = resolve_xinfei_binary()
    # Default to prefer Xinfei enterprise Codex when discoverable, because some
    # upstream Codex CLI builds do not support enterprise-only auth variants
    # (e.g. `enterprise_sso`) present in managed environments.
    prefer_xinfei = _is_truthy_env("XINFEI_CODEX_PREFER", "true")
    if prefer_xinfei and inner is not None:
        return inner

    # Prefer the explicitly-named enterprise wrapper if present.
    # Some environments install Xinfei Codex as `xinfei-codex` to avoid clashing
    # with the upstream `codex` CLI.
    #
    # NOTE: on Windows this may resolve to a PowerShell wrapper (`.ps1`). For
    # subprocess use, it's more reliable to execute the underlying `codex.exe`
    # directly (PowerShell may treat `-c ...` arguments as script params).
    resolved = shutil.which("xinfei-codex")
    if resolved:
        low = resolved.lower()
        if low.endswith((".ps1", ".cmd", ".bat")):
            inner = resolve_xinfei_binary()
            if inner is not None:
                return inner
        return resolved

    resolved = shutil.which("codex")
    if resolved:
        return resolved
    if inner is not None:
        return inner
    return "codex"


def is_xinfei_enterprise_binary(codex_path: str) -> bool:
    """Return True if ``codex_path`` looks like Xinfei enterprise ``codex.exe``."""
    norm = codex_path.replace("\\", "/").lower()
    return ("xinfeicodex" in norm) or ("codex-enterprise-" in norm)


def _combined_login_status_output(codex_bin: str) -> tuple[int, str]:
    """Run ``codex login status`` and return exit code plus merged stdout/stderr text."""
    try:
        completed = subprocess.run(
            [codex_bin, "login", "status"],
            capture_output=True,
            text=True,
            timeout=60,
            encoding="utf-8",
            errors="replace",
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        logger.warning("Could not run %s login status: %s", codex_bin, exc)
        return 1, str(exc)
    out = (completed.stdout or "") + (completed.stderr or "")
    code = int(completed.returncode if completed.returncode is not None else 0)
    return code, out.strip()


def check_enterprise_sso(codex_bin: str) -> bool:
    """Return True if ``codex login status`` reports enterprise SSO."""
    _code, text = _combined_login_status_output(codex_bin)
    return ENTERPRISE_SSO_MARKER in text


def ensure_enterprise_sso(codex_bin: str) -> None:
    """Block until enterprise SSO login succeeds (may open a browser)."""
    logger.info("Starting enterprise SSO login for %s …", codex_bin)
    proc = subprocess.run(
        [codex_bin, "login", "--enterprise-sso"],
        timeout=600,
        encoding="utf-8",
        errors="replace",
    )
    if proc.returncode != 0:
        msg = f"Enterprise SSO login failed (exit code {proc.returncode})."
        raise RuntimeError(msg)
    if not check_enterprise_sso(codex_bin):
        raise RuntimeError(
            "Login finished but enterprise SSO was not detected. "
            f"Expected '{ENTERPRISE_SSO_MARKER}' in `codex login status` output."
        )


def ensure_xinfei_sso_gate(codex_bin: str) -> None:
    """Run once per process: warn or enforce Xinfei enterprise SSO when using that binary."""
    global _sso_gate_done
    if _sso_gate_done:
        return

    if not is_xinfei_enterprise_binary(codex_bin):
        _sso_gate_done = True
        return

    _sso_gate_done = True

    if check_enterprise_sso(codex_bin):
        return

    detail = (
        f"Xinfei Codex at {codex_bin} is not logged in with enterprise SSO. "
        "Run `codex login --enterprise-sso` in a terminal (or set "
        "XINFEI_CODEX_AUTO_LOGIN=true for an interactive login at backend startup)."
    )
    enforce = _is_truthy_env("XINFEI_CODEX_ENFORCE_SSO")
    if enforce:
        raise RuntimeError(detail)

    logger.warning("%s", detail)

    auto = _is_truthy_env("XINFEI_CODEX_AUTO_LOGIN")
    if auto:
        ensure_enterprise_sso(codex_bin)

