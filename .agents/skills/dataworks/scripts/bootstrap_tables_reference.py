#!/usr/bin/env python3
"""
Bootstrap dataworks references/tables.md from a trusted markdown source.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


SECTION_HEADER = "# tables"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Bootstrap tables.md from a trusted markdown source."
    )
    parser.add_argument("--source-md", required=True, help="Trusted source markdown path.")
    parser.add_argument(
        "--target-md",
        default=".agents/skills/dataworks/references/tables.md",
        help="Target markdown path.",
    )
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Replace target fully instead of merging missing sections.",
    )
    return parser.parse_args()


def fail(message: str) -> None:
    print(f"[ERROR] ground-truth bootstrap failure: {message}", file=sys.stderr)
    sys.exit(1)


def normalize_heading(text: str) -> str:
    return text.strip().rstrip()


def split_sections(content: str) -> tuple[str, dict[str, str]]:
    body = content.strip()
    if not body.startswith(SECTION_HEADER):
        fail("source markdown must start with '# tables'")

    pattern = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
    matches = list(pattern.finditer(body))
    if not matches:
        return body.rstrip() + "\n", {}

    preamble = body[: matches[0].start()].rstrip() + "\n\n"
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        heading = normalize_heading(match.group(1))
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        sections[heading] = body[match.start() : end].strip() + "\n"
    return preamble, sections


def merge_content(source_text: str, target_text: str) -> str:
    source_preamble, source_sections = split_sections(source_text)
    if not target_text.strip():
        target_preamble = source_preamble
        target_sections: dict[str, str] = {}
    else:
        target_preamble, target_sections = split_sections(target_text)

    merged_sections = dict(target_sections)
    for heading, section in source_sections.items():
        if heading not in merged_sections:
            merged_sections[heading] = section

    ordered_headings = list(source_sections.keys()) + [
        heading for heading in target_sections.keys() if heading not in source_sections
    ]

    lines = [target_preamble.rstrip() or source_preamble.rstrip(), ""]
    for heading in ordered_headings:
        lines.append(merged_sections[heading].rstrip())
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    args = parse_args()
    source_path = Path(args.source_md)
    target_path = Path(args.target_md)

    if not source_path.exists():
        fail(f"source markdown not found: {source_path}")

    source_text = source_path.read_text(encoding="utf-8")
    if args.replace or not target_path.exists():
        output = source_text.rstrip() + "\n"
    else:
        target_text = target_path.read_text(encoding="utf-8")
        output = merge_content(source_text, target_text)

    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(output, encoding="utf-8")
    print(f"[INFO] Source markdown: {source_path}")
    print(f"[INFO] Target markdown: {target_path}")


if __name__ == "__main__":
    main()
