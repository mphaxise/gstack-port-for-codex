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
    resolve_page_reference,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Add a backlink from one brain page to another.")
    parser.add_argument("--from-ref", required=True, help="Referencing page path, slug, or exact title")
    parser.add_argument("--to-ref", required=True, help="Target page path, slug, or exact title")
    parser.add_argument("--from-category", help="Optional category hint for the referencing page")
    parser.add_argument("--to-category", help="Optional category hint for the target page")
    parser.add_argument("--date", default=default_today(), help="Event date in YYYY-MM-DD format")
    parser.add_argument("--context", required=True, help="Short backlink context")
    args = parser.parse_args()

    brain_root = REPO_ROOT / DEFAULT_BRAIN_ROOT
    source_path = resolve_page_reference(brain_root, args.from_ref, category=args.from_category)
    target_path = resolve_page_reference(brain_root, args.to_ref, category=args.to_category)

    if source_path is None:
        parser.error(f"Could not resolve source page: {args.from_ref}")
    if target_path is None:
        parser.error(f"Could not resolve target page: {args.to_ref}")

    changed = add_backlink(target_path, source_path, args.date, args.context)
    verb = "Updated" if changed else "No change for"
    print(f"{verb} backlink on {target_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
