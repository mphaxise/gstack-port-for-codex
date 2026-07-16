#!/usr/bin/env python3

from pathlib import Path
import argparse
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from gstack_port_for_codex.brain import (  # noqa: E402
    DEFAULT_BRAIN_ROOT,
    add_backlink,
    default_today,
    detect_capitalized_entities,
    upsert_page,
)


def load_message(args: argparse.Namespace) -> str:
    if args.input_file:
        return Path(args.input_file).read_text(encoding="utf-8").strip()
    return args.text.strip()


def infer_title(text: str) -> str:
    sentence = text.splitlines()[0].strip()
    words = sentence.split()
    return " ".join(words[:12]).rstrip(".") or "Captured Signal"


def parse_entity(value: str) -> tuple[str, str]:
    if ":" not in value:
        raise ValueError("Expected entity in category:title form.")
    category, title = value.split(":", 1)
    return category.strip(), title.strip()


def mode_to_category(mode: str) -> str:
    if mode == "idea":
        return "ideas"
    if mode == "concept":
        return "concepts"
    return "originals"


def main() -> int:
    parser = argparse.ArgumentParser(description="Capture a user signal into the local Codex brain.")
    parser.add_argument("--text", default="", help="Inline message text")
    parser.add_argument("--input-file", help="File containing message text")
    parser.add_argument("--title", help="Optional page title")
    parser.add_argument("--mode", default="auto", choices=("auto", "original", "idea", "concept"), help="Signal destination type")
    parser.add_argument("--entity", action="append", default=[], help="Explicit entity in category:title form")
    parser.add_argument("--date", default=default_today(), help="Capture date")
    args = parser.parse_args()

    if not args.input_file and not args.text.strip():
        parser.error("Provide either --text or --input-file.")

    text = load_message(args)
    title = args.title or infer_title(text)
    category = mode_to_category("original" if args.mode == "auto" else args.mode)
    compiled_truth = "\n".join(
        (
            "## Captured Signal",
            f"> {text}",
            "",
            f"Signal captured verbatim from a user message. [Source: User, signal capture, {args.date}]",
        )
    )
    signal_path = upsert_page(
        REPO_ROOT / DEFAULT_BRAIN_ROOT,
        category,
        title,
        compiled_truth,
        timeline_entries=[f"- {args.date}: Captured signal from user message. [Source: User, signal capture, {args.date}]"],
        tags=["signal"],
    )

    updated_paths: list[Path] = []
    for entity in args.entity:
        entity_category, entity_title = parse_entity(entity)
        entity_path = upsert_page(
            REPO_ROOT / DEFAULT_BRAIN_ROOT,
            entity_category,
            entity_title,
            f"{entity_title} was referenced in the captured signal {title}. [Source: User, signal capture, {args.date}]",
            timeline_entries=[f"- {args.date}: Mentioned in captured signal {title}. [Source: User, signal capture, {args.date}]"],
        )
        add_backlink(entity_path, signal_path, args.date, "referenced in this captured signal")
        updated_paths.append(entity_path)

    print(f"Captured signal page: {signal_path}")
    detected = detect_capitalized_entities(text)
    if detected:
        print("Candidate entities:")
        for candidate in detected[:8]:
            print(f"- {candidate}")
    if updated_paths:
        print("Updated explicit entity pages:")
        for path in updated_paths:
            print(f"- {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
