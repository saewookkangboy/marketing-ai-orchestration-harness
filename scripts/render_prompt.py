#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


STAGE_TO_FILE = {
    "orchestration": "prompts/orchestration/master_orchestration_agent.md",
    "M1": "prompts/stages/M1_content_strategy_agent.md",
    "M2": "prompts/stages/M2_content_execution_agent.md",
    "M3": "prompts/stages/M3_optimization_agent.md",
    "M4": "prompts/stages/M4_performance_analysis_agent.md",
    "M5": "prompts/stages/M5_executive_reporting_agent.md",
}


def flatten_slots(payload):
    slots = {}
    for key, value in payload.items():
        placeholder = "{{" + key + "}}"
        if isinstance(value, (dict, list)):
            slots[placeholder] = json.dumps(value, ensure_ascii=False, indent=2)
        else:
            slots[placeholder] = str(value)
    return slots


def render_template(template, slots):
    output = template
    for k, v in slots.items():
        output = output.replace(k, v)
    return output


def main():
    parser = argparse.ArgumentParser(description="Render marketing orchestration prompts.")
    parser.add_argument("--input", required=True, help="Input JSON file path")
    parser.add_argument(
        "--stage",
        required=True,
        choices=["orchestration", "M1", "M2", "M3", "M4", "M5"],
        help="Prompt stage to render",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Optional output file path; default is dist/<stage>_rendered.md",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    template_path = repo_root / STAGE_TO_FILE[args.stage]
    input_path = Path(args.input)
    if not input_path.is_absolute():
        input_path = (repo_root / input_path).resolve()

    payload = json.loads(input_path.read_text(encoding="utf-8"))
    template = template_path.read_text(encoding="utf-8")

    rendered = render_template(template, flatten_slots(payload))

    output_path = Path(args.output) if args.output else repo_root / "dist" / f"{args.stage}_rendered.md"
    if not output_path.is_absolute():
        output_path = (repo_root / output_path).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered, encoding="utf-8")
    print(f"Rendered prompt saved to: {output_path}")


if __name__ == "__main__":
    main()
