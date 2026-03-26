#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path


TOP_LEVEL_REQUIRED = [
    "goal",
    "scope",
    "analysis_type",
    "grain",
    "metrics",
    "dimensions",
    "filters",
    "segments",
    "time",
    "derived_fields",
    "comparisons",
    "methods",
    "validation",
    "output",
    "ambiguities",
    "confidence",
]

TOP_LEVEL_REQUESTED_LEVELS = {
    "goal": "required",
    "scope": "required",
    "analysis_type": "required",
    "grain": "required",
    "metrics": "required",
    "dimensions": "recommended",
    "filters": "recommended",
    "segments": "optional",
    "time": "recommended",
    "derived_fields": "optional",
    "comparisons": "optional",
    "methods": "required",
    "validation": "required",
    "output": "required",
    "ambiguities": "required",
    "confidence": "required",
}

ALLOW_EMPTY_REQUIRED_FIELDS = {"ambiguities"}

ALLOWED_ANALYSIS_TYPES = {
    "descriptive",
    "diagnostic",
    "trend",
    "comparison",
    "distribution",
    "segmentation",
    "ranking",
}
ALLOWED_AGGREGATIONS = {"sum", "mean", "count", "max", "min", "median"}
ALLOWED_OPERATORS = {"eq", "neq", "gt", "gte", "lt", "lte", "in", "not_in", "contains"}
ALLOWED_ROLES = {"time", "category", "geo"}
ALLOWED_CHART_TYPES = {"line", "bar", "histogram", "table"}
ALLOWED_METHOD_TYPES = {
    "aggregate",
    "timeseries",
    "top_n",
    "distribution",
    "group_compare",
    "period_compare",
}


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def is_meaningfully_populated(value) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return value.strip() != ""
    if isinstance(value, (list, dict)):
        return len(value) > 0
    return True


def collect_schema_columns(schema_profile: dict) -> set[str]:
    columns = schema_profile.get("schema_profile", {}).get("columns")
    if isinstance(columns, list):
        result = set()
        for item in columns:
            if isinstance(item, dict) and item.get("name"):
                result.add(item["name"])
            elif isinstance(item, str):
                result.add(item)
        return result
    return set()


def validate_required_top_level(plan: dict, errors: list[str]) -> None:
    for key in TOP_LEVEL_REQUIRED:
        if key not in plan:
            errors.append(f"missing top-level field: {key}")
            continue
        if (
            TOP_LEVEL_REQUESTED_LEVELS[key] == "required"
            and key not in ALLOW_EMPTY_REQUIRED_FIELDS
            and not is_meaningfully_populated(plan[key])
        ):
            errors.append(f"required field is empty: {key}")


def validate_enums(plan: dict, errors: list[str]) -> None:
    analysis_type = plan.get("analysis_type")
    if analysis_type not in ALLOWED_ANALYSIS_TYPES:
        errors.append(f"invalid analysis_type: {analysis_type}")

    for idx, metric in enumerate(plan.get("metrics", [])):
        agg = metric.get("aggregation")
        if agg not in ALLOWED_AGGREGATIONS:
            errors.append(f"metrics[{idx}].aggregation invalid: {agg}")

    for idx, dimension in enumerate(plan.get("dimensions", [])):
        role = dimension.get("role")
        if role is not None and role not in ALLOWED_ROLES:
            errors.append(f"dimensions[{idx}].role invalid: {role}")

    for idx, item in enumerate(plan.get("filters", [])):
        op = item.get("operator")
        if op not in ALLOWED_OPERATORS:
            errors.append(f"filters[{idx}].operator invalid: {op}")

    output = plan.get("output", {})
    chart_type = output.get("chart_type")
    if chart_type is not None and chart_type not in ALLOWED_CHART_TYPES:
        errors.append(f"output.chart_type invalid: {chart_type}")

    for idx, method in enumerate(plan.get("methods", [])):
        method_type = method.get("type")
        if method_type not in ALLOWED_METHOD_TYPES:
            errors.append(f"methods[{idx}].type invalid: {method_type}")


def validate_nested_requireds(plan: dict, errors: list[str]) -> None:
    goal = plan.get("goal", {})
    if not is_meaningfully_populated(goal.get("question")):
        errors.append("goal.question is required")

    scope = plan.get("scope", {})
    if not is_meaningfully_populated(scope.get("population")):
        errors.append("scope.population is required")

    grain = plan.get("grain", {})
    if not is_meaningfully_populated(grain.get("answer_unit")):
        errors.append("grain.answer_unit is required")

    if not plan.get("metrics"):
        errors.append("metrics must contain at least one item")
    for idx, metric in enumerate(plan.get("metrics", [])):
        for field in ("name", "column", "aggregation"):
            if not is_meaningfully_populated(metric.get(field)):
                errors.append(f"metrics[{idx}].{field} is required")

    if not plan.get("methods"):
        errors.append("methods must contain at least one item")
    for idx, method in enumerate(plan.get("methods", [])):
        for field in ("name", "type", "description"):
            if not is_meaningfully_populated(method.get(field)):
                errors.append(f"methods[{idx}].{field} is required")

    validation = plan.get("validation", {})
    for field in ("data_quality_checks", "coverage_checks"):
        if not is_meaningfully_populated(validation.get(field)):
            errors.append(f"validation.{field} is required")

    output = plan.get("output", {})
    if not is_meaningfully_populated(output.get("table_fields")):
        errors.append("output.table_fields is required")

    confidence = plan.get("confidence")
    if not isinstance(confidence, (int, float)) or not (0 <= confidence <= 1):
        errors.append("confidence must be a number between 0 and 1")


def validate_schema_references(plan: dict, schema_columns: set[str], errors: list[str]) -> None:
    if not schema_columns:
        return

    def check_column(value, label: str) -> None:
        if value is not None and value not in schema_columns:
            errors.append(f"{label} references missing schema column: {value}")

    for idx, metric in enumerate(plan.get("metrics", [])):
        check_column(metric.get("column"), f"metrics[{idx}].column")

    for idx, dimension in enumerate(plan.get("dimensions", [])):
        check_column(dimension.get("column"), f"dimensions[{idx}].column")

    for idx, item in enumerate(plan.get("filters", [])):
        check_column(item.get("column"), f"filters[{idx}].column")

    time_obj = plan.get("time", {})
    check_column(time_obj.get("time_column"), "time.time_column")

    for idx, item in enumerate(plan.get("derived_fields", [])):
        for src_idx, source in enumerate(item.get("source_columns", [])):
            check_column(source, f"derived_fields[{idx}].source_columns[{src_idx}]")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate an AnalysisPlan JSON contract.")
    parser.add_argument("--plan", required=True, help="Path to plan JSON.")
    parser.add_argument(
        "--schema-profile",
        required=False,
        help="Path to request/schema fixture containing schema_profile.columns.",
    )
    parser.add_argument(
        "--check-minimally-completed",
        action="store_true",
        help="Also enforce the minimal-completion rule for interactive planning.",
    )
    return parser.parse_args()


def validate_minimal_completion(plan: dict, errors: list[str]) -> None:
    blocking_ambiguities = []
    for item in plan.get("ambiguities", []):
        if isinstance(item, dict):
            severity = item.get("severity")
            blocking = item.get("blocks_minimal_completion")
            if severity == "blocking" or blocking is True:
                blocking_ambiguities.append(item)
        elif isinstance(item, str) and item.strip():
            # Plain strings are treated as informational unless explicitly modeled.
            continue

    if blocking_ambiguities:
        errors.append("plan is not minimally complete: blocking ambiguities remain")

    output = plan.get("output", {})
    table_fields = output.get("table_fields")
    if not isinstance(table_fields, list) or len(table_fields) == 0:
        errors.append("plan is not minimally complete: output.table_fields must identify the first review surface")


def main() -> int:
    args = parse_args()
    plan = load_json(Path(args.plan))
    errors: list[str] = []

    if not isinstance(plan, dict):
        print("plan must be a JSON object", file=sys.stderr)
        return 1

    validate_required_top_level(plan, errors)
    validate_enums(plan, errors)
    validate_nested_requireds(plan, errors)

    if args.schema_profile:
        schema_input = load_json(Path(args.schema_profile))
        validate_schema_references(plan, collect_schema_columns(schema_input), errors)

    if args.check_minimally_completed:
        validate_minimal_completion(plan, errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("AnalysisPlan contract validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
