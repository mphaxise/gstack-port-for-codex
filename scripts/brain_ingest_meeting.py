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


def bulletize(items: list[str], fallback: str) -> str:
    if not items:
        return f"- {fallback}"
    return "\n".join(f"- {item}" for item in items)


def summarize_text(text: str, limit: int = 6) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return "- No meeting summary extracted."
    return "\n".join(f"- {line}" for line in lines[:limit])


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest a meeting transcript or notes file into the Codex brain.")
    parser.add_argument("input_file", help="Meeting transcript or note file")
    parser.add_argument("--title", help="Meeting title; defaults to the file stem")
    parser.add_argument("--date", default=default_today(), help="Meeting date")
    parser.add_argument("--duration", help="Optional meeting duration")
    parser.add_argument("--attendee", action="append", default=[], help="Attendee name")
    parser.add_argument("--company", action="append", default=[], help="Company discussed")
    parser.add_argument("--action-item", action="append", default=[], help="Action item")
    args = parser.parse_args()

    input_path = Path(args.input_file)
    title = args.title or input_path.stem.replace("-", " ").replace("_", " ").title()
    notes = sanitize_external_text(input_path.read_text(encoding="utf-8"))
    raw_path = preserve_raw_file(REPO_ROOT / DEFAULT_BRAIN_ROOT, f"meeting-{slugify(title)}", input_path)
    attendees = "\n".join(
        f"{line} [Source: meeting transcript, {args.date}]"
        for line in bulletize(args.attendee, "Attendees not yet listed.").splitlines()
    )
    summary = "\n".join(
        f"{line} [Source: meeting transcript, {args.date}]"
        for line in summarize_text(notes).splitlines()
    )
    action_items = "\n".join(
        f"{line} [Source: meeting transcript, {args.date}]"
        for line in bulletize(args.action_item, "No explicit action items captured.").splitlines()
    )
    discussion_notes = "\n".join(f"> {line}" for line in notes.splitlines()) if notes else "No notes captured."

    compiled_truth = "\n".join(
        (
            f"**Date:** {args.date} [Source: meeting transcript, {args.date}]",
            f"**Duration:** {args.duration or 'unknown'} [Source: meeting transcript, {args.date}]",
            "",
            "## Attendees",
            attendees,
            "",
            "## Summary",
            summary,
            "",
            "## Action Items",
            action_items,
            "",
            "## Discussion Notes",
            discussion_notes[:2400],
            "",
            f"**Raw Copy:** {raw_path.relative_to(REPO_ROOT)} [Source: meeting transcript, {args.date}]",
        )
    )
    meeting_path = upsert_page(
        REPO_ROOT / DEFAULT_BRAIN_ROOT,
        "meetings",
        f"{title} - {args.date}",
        compiled_truth,
        timeline_entries=[f"- {args.date}: Meeting ingested. [Source: meeting transcript, {args.date}]"],
        tags=["meeting"],
    )

    updated_paths: list[Path] = []
    for attendee in args.attendee:
        person_path = upsert_page(
            REPO_ROOT / DEFAULT_BRAIN_ROOT,
            "people",
            attendee,
            f"{attendee} attended {title} on {args.date}. [Source: meeting transcript, {args.date}]",
            timeline_entries=[f"- {args.date}: Attended {title}. [Source: meeting transcript, {args.date}]"],
        )
        add_backlink(person_path, meeting_path, args.date, "attended this meeting")
        updated_paths.append(person_path)

    for company in args.company:
        company_path = upsert_page(
            REPO_ROOT / DEFAULT_BRAIN_ROOT,
            "companies",
            company,
            f"{company} was discussed in {title}. [Source: meeting transcript, {args.date}]",
            timeline_entries=[f"- {args.date}: Discussed in {title}. [Source: meeting transcript, {args.date}]"],
        )
        add_backlink(company_path, meeting_path, args.date, "discussed in this meeting")
        updated_paths.append(company_path)

    print(f"Ingested meeting page: {meeting_path}")
    print(f"Raw transcript preserved: {raw_path}")
    if updated_paths:
        print("Updated entity pages:")
        for path in updated_paths:
            print(f"- {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
