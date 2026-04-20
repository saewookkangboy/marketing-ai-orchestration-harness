#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from typing import Any


def inline_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    return str(value)


def render_markdown(value: Any, indent: int = 0) -> list[str]:
    prefix = "  " * indent

    if isinstance(value, dict):
        lines: list[str] = []
        for key, item in value.items():
            if isinstance(item, (dict, list)):
                lines.append(f"{prefix}- **{key}**:")
                lines.extend(render_markdown(item, indent + 1))
            else:
                lines.append(f"{prefix}- **{key}**: {inline_scalar(item)}")
        return lines or [f"{prefix}- _(empty object)_"]

    if isinstance(value, list):
        lines = []
        for item in value:
            if isinstance(item, (dict, list)):
                lines.append(f"{prefix}-")
                lines.extend(render_markdown(item, indent + 1))
            else:
                lines.append(f"{prefix}- {inline_scalar(item)}")
        return lines or [f"{prefix}- _(empty list)_"]

    return [f"{prefix}- {inline_scalar(value)}"]


def build_document(payload: Any, title: str) -> str:
    lines: list[str] = [f"# {title}", ""]
    lines.extend(render_markdown(payload))
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert a stage JSON output into a markdown report."
    )
    parser.add_argument("--input", required=True, help="Input JSON file path")
    parser.add_argument(
        "--output",
        default=None,
        help="Optional output markdown path; default is <input_basename>.md",
    )
    parser.add_argument(
        "--title",
        default=None,
        help="Optional markdown title; default is '<stage> output report' when stage exists",
    )
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    payload = json.loads(input_path.read_text(encoding="utf-8"))

    if args.output:
        output_path = Path(args.output).resolve()
    else:
        output_path = input_path.with_suffix(".md")

    if args.title:
        title = args.title
    else:
        stage = payload.get("stage") if isinstance(payload, dict) else None
        title = f"{stage} output report" if stage else f"{input_path.stem} report"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_document(payload, title), encoding="utf-8")
    print(f"Markdown report saved to: {output_path}")


if __name__ == "__main__":
    main()
