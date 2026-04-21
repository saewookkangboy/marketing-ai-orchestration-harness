#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path


def resolve_path(repo_root: Path, value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path.resolve()
    return (repo_root / path).resolve()


def run_local_intake_gate(
    repo_root: Path,
    docs_dir: Path,
    gate_report: Path,
    suggested_input: Path,
) -> None:
    command = [
        sys.executable,
        str(repo_root / "scripts" / "local_intake_gate.py"),
        "--docs-dir",
        str(docs_dir),
        "--output",
        str(gate_report),
        "--input-output",
        str(suggested_input),
    ]
    subprocess.run(command, check=True)


def merge_suggested_into_input(input_data: dict, suggested_data: dict) -> dict:
    merged = dict(input_data)
    for key, value in suggested_data.items():
        if key not in merged:
            merged[key] = value
            continue
        if isinstance(merged[key], str) and not merged[key].strip():
            merged[key] = value
            continue
        if isinstance(merged[key], list) and len(merged[key]) == 0:
            merged[key] = value
            continue
        if isinstance(merged[key], dict) and len(merged[key]) == 0:
            merged[key] = value
            continue
    return merged


def run_render_prompt(repo_root: Path, input_path: Path, stage: str, output_path: Path | None) -> None:
    command = [
        sys.executable,
        str(repo_root / "scripts" / "render_prompt.py"),
        "--input",
        str(input_path),
        "--stage",
        stage,
    ]
    if output_path is not None:
        command.extend(["--output", str(output_path)])
    subprocess.run(command, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run local intake gate and render prompt only when gate passes."
    )
    parser.add_argument("--docs-dir", required=True, help="Directory containing local source documents")
    parser.add_argument(
        "--input",
        default="examples/input-template.json",
        help="Base input JSON path (existing values take priority over suggested values)",
    )
    parser.add_argument(
        "--stage",
        default="orchestration",
        choices=["orchestration", "M1", "M2", "M3", "M4", "M5"],
        help="Prompt stage to render",
    )
    parser.add_argument(
        "--gate-report",
        default="dist/local_intake_gate_report.json",
        help="Gate report output path",
    )
    parser.add_argument(
        "--suggested-input",
        default="dist/local_intake_input_suggested.json",
        help="Suggested input output path from local intake gate",
    )
    parser.add_argument(
        "--resolved-input",
        default="dist/resolved_input.json",
        help="Merged input JSON path used for rendering",
    )
    parser.add_argument(
        "--render-output",
        default=None,
        help="Optional rendered prompt output path",
    )
    parser.add_argument(
        "--fail-on-gate-fail",
        action="store_true",
        help="Return non-zero exit code when gate fails",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    docs_dir = resolve_path(repo_root, args.docs_dir)
    input_path = resolve_path(repo_root, args.input)
    gate_report_path = resolve_path(repo_root, args.gate_report)
    suggested_input_path = resolve_path(repo_root, args.suggested_input)
    resolved_input_path = resolve_path(repo_root, args.resolved_input)
    render_output_path = resolve_path(repo_root, args.render_output) if args.render_output else None

    if not docs_dir.exists():
        raise SystemExit(f"docs-dir does not exist: {docs_dir}")
    if not input_path.exists():
        raise SystemExit(f"input file does not exist: {input_path}")

    run_local_intake_gate(repo_root, docs_dir, gate_report_path, suggested_input_path)

    gate_report = json.loads(gate_report_path.read_text(encoding="utf-8"))
    intake_status = gate_report.get("intake_status", {})
    gate_pass = bool(intake_status.get("gate_pass"))

    if not gate_pass:
        print("Gate failed. Rendering skipped.")
        missing = intake_status.get("missing_required", [])
        if missing:
            print("Missing required fields:")
            for item in missing:
                print(f"- {item}")
        questions = intake_status.get("follow_up_questions", [])
        if questions:
            print("Follow-up questions:")
            for question in questions:
                print(f"- {question}")
        if args.fail_on_gate_fail:
            raise SystemExit(2)
        return

    base_input = json.loads(input_path.read_text(encoding="utf-8"))
    suggested_input = json.loads(suggested_input_path.read_text(encoding="utf-8"))
    resolved_input = merge_suggested_into_input(base_input, suggested_input)

    resolved_input_path.parent.mkdir(parents=True, exist_ok=True)
    resolved_input_path.write_text(
        json.dumps(resolved_input, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    run_render_prompt(repo_root, resolved_input_path, args.stage, render_output_path)
    print(f"Resolved input saved to: {resolved_input_path}")


if __name__ == "__main__":
    main()
