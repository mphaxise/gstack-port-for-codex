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
    preserve_raw_file,
    sanitize_external_text,
    slugify,
    upsert_page,
)


def summarize_text(text: str, limit: int = 5) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return "- No summary extracted."
    return "\n".join(f"- {line}" for line in lines[:limit])


def load_analysis(args: argparse.Namespace) -> str:
    if args.analysis_file:
        return Path(args.analysis_file).read_text(encoding="utf-8").strip()
    if args.analysis:
        return args.analysis.strip()
    return "Initial ingest captured the source and raw artifact. Follow with `enrich` for deeper synthesis. [Source: source ingest, {date}]"


def parse_related(value: str) -> tuple[str, str]:
    if ":" not in value:
        raise ValueError("Expected related entity in category:title form.")
    category, title = value.split(":", 1)
    return category.strip(), title.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest a local text-bearing source file into the Codex brain.")
    parser.add_argument("input_file", help="Local source file to ingest")
    parser.add_argument("--title", help="Page title; defaults to the file stem")
    parser.add_argument("--category", default="sources", help="Destination category")
    parser.add_argument("--author", help="Author or primary thinker behind the source")
    parser.add_argument("--published", help="Optional published date or source timestamp")
    parser.add_argument("--analysis-file", help="Optional file with analysis text")
    parser.add_argument("--analysis", help="Optional inline analysis text")
    parser.add_argument("--source-url", help="Optional canonical source URL")
    parser.add_argument("--related", action="append", default=[], help="Explicit related entity in category:title form")
    parser.add_argument("--tag", action="append", default=[], help="Tag to add")
    parser.add_argument("--date", default=default_today(), help="Ingest date")
    args = parser.parse_args()

    input_path = Path(args.input_file)
    title = args.title or input_path.stem.replace("-", " ").replace("_", " ").title()
    source_text = sanitize_external_text(input_path.read_text(encoding="utf-8"))
    summary = "\n".join(
        f"{line} [Source: local file, {args.date}]"
        for line in summarize_text(source_text).splitlines()
    )
    analysis = load_analysis(args).format(date=args.date)

    brain_root = REPO_ROOT / DEFAULT_BRAIN_ROOT
    raw_path = preserve_raw_file(brain_root, slugify(title), input_path)
    source_label = args.source_url or str(input_path)
    compiled_truth = "\n".join(
        (
            f"**Source:** {source_label} [Source: local file, {args.date}]",
            f"**Raw Copy:** {raw_path.relative_to(REPO_ROOT)} [Source: local file, {args.date}]",
            f"**Published:** {args.published or 'unknown'} [Source: local file, {args.date}]",
            "",
            "## Summary",
            summary,
            "",
            "## Analysis",
            analysis,
        )
    )
    timeline = [f"- {args.date}: Ingested {title}. [Source: local file, {args.date}]"]
    page_path = upsert_page(brain_root, args.category, title, compiled_truth, timeline_entries=timeline, tags=args.tag)

    related_updates: list[Path] = []
    if args.author:
        author_note = f"{args.author} authored {title}. [Source: source ingest, {args.date}]"
        author_path = upsert_page(
            brain_root,
            "people",
            args.author,
            author_note,
            timeline_entries=[f"- {args.date}: Authored {title}. [Source: source ingest, {args.date}]"],
            tags=["author"],
        )
        add_backlink(author_path, page_path, args.date, "authored this source")
        related_updates.append(author_path)

    for related in args.related:
        category, entity_title = parse_related(related)
        entity_path = upsert_page(
            brain_root,
            category,
            entity_title,
            f"{entity_title} is referenced in {title}. [Source: source ingest, {args.date}]",
            timeline_entries=[f"- {args.date}: Mentioned in {title}. [Source: source ingest, {args.date}]"],
        )
        add_backlink(entity_path, page_path, args.date, "mentioned in this source")
        related_updates.append(entity_path)

    print(f"Ingested source page: {page_path}")
    print(f"Raw source preserved: {raw_path}")
    if related_updates:
        print("Updated related pages:")
        for related_path in related_updates:
            print(f"- {related_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
