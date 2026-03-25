"""Example contract runner for the skills-verification skill.

This is an indexed example script that demonstrates layer-aware reporting.
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class Finding:
    severity: str
    layer: str
    message: str


def check_csv_contract(csv_path: Path) -> list[Finding]:
    findings: list[Finding] = []
    required_columns = {"id", "target", "feature_num", "feature_cat", "event_date"}

    if not csv_path.exists():
        return [Finding("fatal", "contract", f"Missing fixture: {csv_path}")]

    with csv_path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        headers = set(reader.fieldnames or [])
        if not required_columns.issubset(headers):
            findings.append(
                Finding(
                    "major",
                    "negative-path",
                    "Fixture is missing one or more required columns.",
                )
            )

        rows = list(reader)
        if not rows:
            findings.append(Finding("major", "contract", "Fixture is empty."))

    if not findings:
        findings.append(Finding("warning", "contract", "Example contract check passed."))

    return findings


def summarize(findings: list[Finding]) -> dict[str, object]:
    severities = [finding.severity for finding in findings]
    confidence = "medium" if ("fatal" in severities or "major" in severities) else "high"
    return {
        "findings": [asdict(finding) for finding in findings],
        "confidence": confidence,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run an example contract check.")
    parser.add_argument("csv_fixture", type=Path, help="Path to a minimal CSV fixture")
    args = parser.parse_args()

    findings = check_csv_contract(args.csv_fixture)
    print(json.dumps(summarize(findings), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
