"""Xinfei enterprise Codex install detection, CLI path resolution, and SSO checks."""

from __future__ import annotations

import logging
import os
import shutil
import subprocess
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

ENTERPRISE_SSO_MARKER = "Logged in using Enterprise SSO"

_sso_gate_done: bool = False


def resolve_xinfei_binary() -> str | None:
    """Return an absolute path to Xinfei's ``codex.exe`` if the default layout exists."""
    if sys.platform != "win32":
        return None
    base = os.environ.get("LOCALAPPDATA", "").strip()
    if not base:
        return None
    candidate = Path(base) / "Programs" / "XinfeiCodex" / "bin" / "codex.exe"
    if candidate.is_file():
        return str(candidate.resolve())
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
    if inner is not None:
        return inner

    resolved = shutil.which("codex")
    return resolved if resolved else "codex"


def is_xinfei_enterprise_binary(codex_path: str) -> bool:
    """Return True if ``codex_path`` looks like Xinfei enterprise ``codex.exe``."""
    norm = codex_path.replace("\\", "/").lower()
    return "xinfeicodex" in norm


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
    enforce = os.getenv("XINFEI_CODEX_ENFORCE_SSO", "").strip().lower() in (
        "1",
        "true",
        "yes",
        "on",
    )
    if enforce:
        raise RuntimeError(detail)

    logger.warning("%s", detail)

    auto = os.getenv("XINFEI_CODEX_AUTO_LOGIN", "").strip().lower() in (
        "1",
        "true",
        "yes",
        "on",
    )
    if auto:
        ensure_enterprise_sso(codex_bin)

