#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Overwrite a skill-local water.json watermark file."
    )
    parser.add_argument("--skill-dir", required=True, help="Path to the skill directory.")
    parser.add_argument("--skill", required=True, help="Skill name.")
    parser.add_argument("--version", default="v1", help="Watermark schema/version label.")
    parser.add_argument(
        "--input-file",
        dest="input_files",
        action="append",
        default=[],
        help="Input file name or path. Repeat this flag to add multiple values.",
    )
    parser.add_argument(
        "--action",
        dest="actions",
        action="append",
        default=[],
        help="Action performed by the skill. Repeat this flag to add multiple values.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    skill_dir = Path(args.skill_dir).resolve()
    skill_dir.mkdir(parents=True, exist_ok=True)

    payload = {
        "skill": args.skill,
        "version": args.version,
        "input_files": args.input_files,
        "actions": args.actions,
    }

    water_path = skill_dir / "water.json"
    water_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
