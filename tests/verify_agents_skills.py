"""Verify Cursor-style agent skills under `.agents/skills/`.

This is a lightweight "skills registry" verifier:
1) Validate `SKILL.md` frontmatter (`name`, `description`).
2) Run best-effort structural checks (warnings only).
3) Optionally run smoke tests for known skills (currently: scorecardpy).

Usage:
  python tests/verify_agents_skills.py
  python tests/verify_agents_skills.py --smoke
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
import shutil


REPO_ROOT = Path(__file__).resolve().parent.parent
AGENTS_SKILLS_DIR = REPO_ROOT / ".agents" / "skills"


FRONTMATTER_REQUIRED_KEYS = ("name", "description")
SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def _parse_frontmatter(text: str) -> dict[str, str]:
    """
    Parse the first YAML frontmatter block delimited by `---`.

    This intentionally keeps parsing simple (no PyYAML dependency) because
    we only need first-level `key: value` pairs.
    """

    # Match: ---\n ... \n---  (non-greedy)
    m = re.match(r"^---\s*\r?\n(.*?)\r?\n---\s*\r?\n", text, flags=re.DOTALL)
    if not m:
        return {}
    block = m.group(1)
    out: dict[str, str] = {}
    for raw_line in block.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        k, _, rest = line.partition(":")
        key = k.strip()
        value = rest.strip()
        if key:
            out[key] = value
    return out


def _is_skill_md(path: Path) -> bool:
    return path.is_file() and path.name == "SKILL.md"


@dataclass
class SkillCheck:
    skill_dir: str
    skill_md: str
    errors: list[str]
    warnings: list[str]


def _list_skill_dirs() -> list[Path]:
    if not AGENTS_SKILLS_DIR.is_dir():
        return []
    # Immediate subdirectories that contain SKILL.md
    out: list[Path] = []
    for p in AGENTS_SKILLS_DIR.iterdir():
        if not p.is_dir():
            continue
        if _is_skill_md(p / "SKILL.md"):
            out.append(p)
    return sorted(out)


def verify_layout_for_skill(skill_dir: Path) -> SkillCheck:
    skill_md = skill_dir / "SKILL.md"
    text = skill_md.read_text(encoding="utf-8")
    fm = _parse_frontmatter(text)

    errors: list[str] = []
    warnings: list[str] = []

    for k in FRONTMATTER_REQUIRED_KEYS:
        if k not in fm or not fm[k].strip():
            errors.append(f"frontmatter key `{k}` missing/empty")

    name = (fm.get("name") or "").strip()
    if name and not SKILL_NAME_RE.match(name):
        errors.append(f"frontmatter `name` has invalid format: {name!r}")

    # Authoring guideline: keep SKILL.md under 500 lines. We treat it as warning.
    line_count = len(text.splitlines())
    if line_count > 500:
        warnings.append(f"SKILL.md is {line_count} lines (>500 guideline)")

    desc = (fm.get("description") or "").strip().lower()
    if desc:
        # Heuristic: try to see if description includes WHEN.
        # Many of your skills use "Use when ...", so check that phrase.
        if ("use when" not in desc) and ("when the user" not in desc) and ("use for" not in desc):
            warnings.append("description does not seem to include a clear trigger phrase (heuristic)")

    # Quick sanity: ensure file has some body header.
    if re.search(r"^#\s+.+$", text, flags=re.MULTILINE) is None:
        warnings.append("SKILL.md has no top-level markdown header starting with `#` (heuristic)")

    return SkillCheck(
        skill_dir=str(skill_dir.relative_to(REPO_ROOT)),
        skill_md=str(skill_md.relative_to(REPO_ROOT)),
        errors=errors,
        warnings=warnings,
    )


def run_scorecardpy_smoke() -> tuple[bool, str]:
    """
    Run the existing dedicated smoke tests for the scorecardpy skill.
    """
    script = str(REPO_ROOT / "tests" / "verify_scorecardpy_skill.py")
    # 1) First try with current interpreter.
    cmd = [sys.executable, script, "--smoke"]
    proc = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True, check=False)
    out = (proc.stdout or "").strip()
    err = (proc.stderr or "").strip()
    detail = "\n".join([x for x in [out, err] if x])
    if proc.returncode == 0:
        return True, detail[:4000]

    # 2) If dependencies are missing, try uv-run to use the project's uv env.
    #    This keeps smoke usable without forcing you to pip-install everything globally.
    uv_path = shutil.which("uv")
    missing_markers = [
        "No module named 'duckdb'",
        "No module named \"duckdb\"",
        "Install: duckdb",
        "No module named 'scorecardpy'",
    ]
    if uv_path and any(m in detail for m in missing_markers):
        cmd2 = ["uv", "run", "python", script, "--smoke"]
        proc2 = subprocess.run(cmd2, cwd=str(REPO_ROOT), capture_output=True, text=True, check=False)
        out2 = (proc2.stdout or "").strip()
        err2 = (proc2.stderr or "").strip()
        detail2 = "\n".join([x for x in [out2, err2] if x])
        return proc2.returncode == 0, detail2[:4000]

    return False, detail[:4000]


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify `.agents/skills/*/SKILL.md` quality")
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="Run optional smoke tests for known skills (may require extra dependencies).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print a JSON report to stdout (useful for CI).",
    )
    args = parser.parse_args()

    skill_dirs = _list_skill_dirs()
    checks: list[SkillCheck] = []

    if not skill_dirs:
        if not args.json:
            print(f"No skills found under {AGENTS_SKILLS_DIR}")
        payload = {"skills": [], "smoke": None, "ok": False}
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 1

    layout_ok = True
    for sd in skill_dirs:
        sc = verify_layout_for_skill(sd)
        if sc.errors:
            layout_ok = False
        checks.append(sc)

    smoke_report: dict[str, object] | None = None
    smoke_ok = True
    if args.smoke:
        ok, detail = run_scorecardpy_smoke()
        smoke_ok = ok
        smoke_report = {
            "skill": "scorecardpy",
            "ok": ok,
            "detail": detail,
        }

    overall_ok = layout_ok and (smoke_ok if args.smoke else True)

    if args.json:
        payload = {
            "skills": [
                {
                    "skill_dir": c.skill_dir,
                    "skill_md": c.skill_md,
                    "errors": c.errors,
                    "warnings": c.warnings,
                }
                for c in checks
            ],
            "smoke": smoke_report,
            "ok": overall_ok,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0 if overall_ok else 1

    # Human-readable output
    print(f"Found {len(skill_dirs)} skill(s) under {AGENTS_SKILLS_DIR}")
    for c in checks:
        if c.errors:
            print(f"\n[ERROR] {c.skill_md}")
            for e in c.errors:
                print(f"  - {e}")
        if c.warnings:
            print(f"\n[WARN] {c.skill_md}")
            for w in c.warnings:
                print(f"  - {w}")

    if args.smoke:
        print("\n--- Smoke tests ---")
        if smoke_report:
            print(f"scorecardpy smoke ok: {smoke_report['ok']}")
            if smoke_report.get("detail"):
                print(smoke_report["detail"])

    return 0 if overall_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

