#!/usr/bin/env python3

from pathlib import Path
import argparse
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from gstack_port_for_codex.brain import (  # noqa: E402
    DEFAULT_BRAIN_ROOT,
    default_today,
    upsert_page,
)


def load_compiled_truth(args: argparse.Namespace) -> str:
    if args.input_file:
        return Path(args.input_file).read_text(encoding="utf-8").strip()
    return args.text.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Create or update a page in the local Codex brain.")
    parser.add_argument("--title", required=True, help="Page title")
    parser.add_argument("--category", required=True, help="Brain category (people, companies, concepts, ideas, originals, sources, meetings, reports)")
    parser.add_argument("--input-file", help="File containing compiled truth content")
    parser.add_argument("--text", default="", help="Inline compiled truth content")
    parser.add_argument("--timeline", action="append", default=[], help="Timeline entry to append")
    parser.add_argument("--tag", action="append", default=[], help="Tag to add")
    parser.add_argument("--page-type", help="Optional explicit page type")
    args = parser.parse_args()

    if not args.input_file and not args.text.strip():
        parser.error("Provide either --input-file or --text.")

    compiled_truth = load_compiled_truth(args)
    if not args.timeline:
        args.timeline = [f"- {default_today()}: Page updated. [Source: local brain write, {default_today()}]"]

    page_path = upsert_page(
        REPO_ROOT / DEFAULT_BRAIN_ROOT,
        args.category,
        args.title,
        compiled_truth,
        timeline_entries=args.timeline,
        tags=args.tag,
        page_type=args.page_type,
    )
    print(f"Brain page ready: {page_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
