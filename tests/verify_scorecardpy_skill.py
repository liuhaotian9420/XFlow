"""Verify the scorecardpy agent skill layout and optionally run a pipeline smoke test.

Run from repository root:

    python tests/verify_scorecardpy_skill.py
    python tests/verify_scorecardpy_skill.py --smoke

Smoke mode requires: duckdb, pandas, scorecardpy, scikit-learn (not in core project deps).
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path


REQUIRED_REFERENCES = (
    "workflow.md",
    "sampling.md",
    "scorecardpy.md",
    "duckdb-deployment.md",
    "pitfalls.md",
)

REQUIRED_SCRIPTS = (
    "build_feature_table.sql",
    "sample_dev_data.sql",
    "run_scorecardpy.py",
    "export_breaks.py",
    "apply_woe_in_duckdb.sql",
)

FRONTMATTER_KEYS = ("name", "description")


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def skill_dir() -> Path:
    return repo_root() / ".agents" / "skills" / "scorecardpy"


def parse_simple_frontmatter(text: str) -> dict[str, str]:
    """Parse first YAML-like frontmatter block; values are single-line strings."""
    m = re.match(r"^---\s*\r?\n(.*?)\r?\n---\s*\r?\n", text, re.DOTALL)
    if not m:
        return {}
    block = m.group(1)
    out: dict[str, str] = {}
    for line in block.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, rest = line.partition(":")
        k = key.strip()
        v = rest.strip()
        if k:
            out[k] = v
    return out


def verify_layout() -> list[str]:
    errors: list[str] = []
    root = skill_dir()
    if not root.is_dir():
        errors.append(f"Skill directory missing: {root}")
        return errors

    skill_md = root / "SKILL.md"
    if not skill_md.is_file():
        errors.append(f"Missing {skill_md}")
        return errors

    body = skill_md.read_text(encoding="utf-8")
    fm = parse_simple_frontmatter(body)
    for key in FRONTMATTER_KEYS:
        if key not in fm or not fm[key]:
            errors.append(f"SKILL.md frontmatter missing or empty: {key}")

    ref_dir = root / "references"
    for name in REQUIRED_REFERENCES:
        p = ref_dir / name
        if not p.is_file():
            errors.append(f"Missing reference file: {p.relative_to(root)}")

    script_dir = root / "scripts"
    for name in REQUIRED_SCRIPTS:
        p = script_dir / name
        if not p.is_file():
            errors.append(f"Missing script: {p.relative_to(root)}")

    return errors


def run_smoke() -> list[str]:
    errors: list[str] = []
    try:
        import duckdb  # noqa: F401
        import pandas as pd
    except ImportError as exc:
        return [f"Smoke test imports failed ({exc}). Install: duckdb numpy pandas scorecardpy scikit-learn"]

    try:
        import scorecardpy as sc
    except ImportError as exc:
        return [f"Smoke test imports failed ({exc}). Install: scorecardpy scikit-learn"]

    root = skill_dir()
    run_script = root / "scripts" / "run_scorecardpy.py"
    export_script = root / "scripts" / "export_breaks.py"
    py = sys.executable

    # Use the library's German credit sample so var_filter retains predictors (Gaussian-only fixtures often IV-fail).
    raw = sc.germancredit()
    df = raw.drop(columns=["creditability"]).copy()
    df.insert(0, "entity_id", range(len(df)))
    df["target"] = (raw["creditability"] == "bad").astype(int)

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        db_path = tmp_path / "smoke.duckdb"
        out_dir = tmp_path / "out"
        con = duckdb.connect(str(db_path))
        try:
            con.register("df_in", df)
            con.execute("CREATE TABLE dev_smoke_test AS SELECT * FROM df_in")
        finally:
            con.close()

        r1 = subprocess.run(
            [
                py,
                str(run_script),
                "--db-path",
                str(db_path),
                "--table",
                "dev_smoke_test",
                "--target",
                "target",
                "--id-col",
                "entity_id",
                "--out-dir",
                str(out_dir),
            ],
            cwd=str(repo_root()),
            capture_output=True,
            text=True,
            check=False,
        )
        if r1.returncode != 0:
            err = (r1.stderr or r1.stdout or "").strip()
            errors.append(f"run_scorecardpy.py failed (exit {r1.returncode}): {err[:2000]}")
            return errors

        bins_pkl = out_dir / "bins.pkl"
        if not bins_pkl.is_file():
            errors.append(f"Smoke test: expected {bins_pkl} after run_scorecardpy.py")
            return errors

        r2 = subprocess.run(
            [py, str(export_script), "--bins-pkl", str(bins_pkl), "--out-dir", str(out_dir)],
            cwd=str(repo_root()),
            capture_output=True,
            text=True,
            check=False,
        )
        if r2.returncode != 0:
            err = (r2.stderr or r2.stdout or "").strip()
            errors.append(f"export_breaks.py failed (exit {r2.returncode}): {err[:2000]}")
            return errors

        breaks_json = out_dir / "breaks_export.json"
        if not breaks_json.is_file():
            errors.append(f"Smoke test: expected {breaks_json} after export_breaks.py")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify scorecardpy skill directory and optional smoke run")
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="Run end-to-end smoke (requires duckdb, scorecardpy, scikit-learn, etc.)",
    )
    args = parser.parse_args()

    layout_errors = verify_layout()
    if layout_errors:
        print("Layout verification failed:", file=sys.stderr)
        for e in layout_errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print(f"OK: skill layout at {skill_dir()}")

    if args.smoke:
        smoke_errors = run_smoke()
        if smoke_errors:
            print("Smoke test failed:", file=sys.stderr)
            for e in smoke_errors:
                print(f"  - {e}", file=sys.stderr)
            return 1
        print("OK: smoke test (run_scorecardpy.py + export_breaks.py)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
