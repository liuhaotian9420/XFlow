"""Example fixture generator for the skills-verification skill.

This is an indexed example script, not the production verifier.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


CSV_ROWS = [
    {
        "id": 1,
        "target": 1,
        "feature_num": 10,
        "feature_cat": "A",
        "event_date": "2026-01-01",
    },
    {
        "id": 2,
        "target": 0,
        "feature_num": 20,
        "feature_cat": "B",
        "event_date": "2026-01-02",
    },
    {
        "id": 3,
        "target": 1,
        "feature_num": 15,
        "feature_cat": "A",
        "event_date": "2026-01-03",
    },
    {
        "id": 4,
        "target": 0,
        "feature_num": 30,
        "feature_cat": "C",
        "event_date": "2026-01-04",
    },
]


def infer_profile(skill_text: str) -> str:
    lowered = skill_text.lower()
    if any(token in lowered for token in ("api", "odps", "credential", "service")):
        return "external-system"
    if any(token in lowered for token in ("scorecard", "model", "analytics", "woe", "iv")):
        return "model-analytics"
    if any(token in lowered for token in ("csv", "xlsx", "parquet", "duckdb", "sql")):
        return "file-processing"
    return "documentation-only"


def write_csv_fixture(output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "sample.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(CSV_ROWS[0].keys()))
        writer.writeheader()
        writer.writerows(CSV_ROWS)
    return path


def write_sql_fixture(output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "sample.sql"
    path.write_text(
        "select 1 as id, 'A' as segment, 100 as amount\n"
        "union all\n"
        "select 2 as id, 'B' as segment, 200 as amount;\n",
        encoding="utf-8",
    )
    return path


def write_mock_response(output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "mock_response.json"
    payload = {
        "status": "ok",
        "items": [{"id": 1, "segment": "A", "amount": 100}],
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate minimal deterministic fixtures.")
    parser.add_argument("skill_md", type=Path, help="Path to the target SKILL.md")
    parser.add_argument("output_dir", type=Path, help="Directory for generated fixtures")
    args = parser.parse_args()

    skill_text = args.skill_md.read_text(encoding="utf-8")
    profile = infer_profile(skill_text)

    created = [write_csv_fixture(args.output_dir)]

    if profile in {"file-processing", "model-analytics"}:
        created.append(write_sql_fixture(args.output_dir))
    if profile == "external-system":
        created.append(write_mock_response(args.output_dir))

    print(json.dumps({"profile": profile, "created": [str(path) for path in created]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
