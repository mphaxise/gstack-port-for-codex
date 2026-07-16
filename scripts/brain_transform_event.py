#!/usr/bin/env python3

from datetime import datetime
from pathlib import Path
import argparse
import json
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from gstack_port_for_codex.brain import (  # noqa: E402
    DEFAULT_BRAIN_ROOT,
    add_backlink,
    default_today,
    preserve_raw_text,
    sanitize_external_text,
    slugify,
    upsert_page,
)


def dead_letter(brain_root: Path, event_name: str, payload: str) -> Path:
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
    path = brain_root / "_dead-letter" / f"{timestamp}-{slugify(event_name)}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload, encoding="utf-8")
    return path


def transform_meeting(brain_root: Path, payload: dict, ingest_date: str) -> Path:
    title = payload.get("title") or "Webhook Meeting"
    attendees = payload.get("attendees") or []
    summary = payload.get("summary") or payload.get("transcript") or payload.get("notes") or ""
    attendee_lines = "\n".join(
        f"- {attendee} [Source: webhook payload, {ingest_date}]"
        for attendee in attendees
    ) or "- None provided"
    summary_lines = sanitize_external_text(summary)
    summary_block = "\n".join(f"> {line}" for line in summary_lines.splitlines()) or "No summary provided."
    compiled_truth = "\n".join(
        (
            f"**Event Source:** webhook [Source: webhook payload, {ingest_date}]",
            "",
            "## Attendees",
            attendee_lines,
            "",
            "## Summary",
            summary_block[:2200],
        )
    )
    page_path = upsert_page(
        brain_root,
        "meetings",
        f"{title} - {ingest_date}",
        compiled_truth,
        timeline_entries=[f"- {ingest_date}: Transformed from webhook payload. [Source: webhook payload, {ingest_date}]"],
        tags=["webhook", "meeting"],
    )
    for attendee in attendees:
        attendee_path = upsert_page(
            brain_root,
            "people",
            attendee,
            f"{attendee} appeared in webhook meeting {title}. [Source: webhook payload, {ingest_date}]",
            timeline_entries=[f"- {ingest_date}: Appeared in {title}. [Source: webhook payload, {ingest_date}]"],
        )
        add_backlink(attendee_path, page_path, ingest_date, "appeared in this webhook meeting")
    return page_path


def transform_generic(brain_root: Path, payload: dict, ingest_date: str, event_type: str) -> Path:
    title = payload.get("title") or payload.get("subject") or payload.get("author") or f"{event_type} event"
    body = payload.get("body") or payload.get("text") or payload.get("summary") or json.dumps(payload, indent=2, sort_keys=True)
    source = payload.get("url") or payload.get("source") or "webhook payload"
    compiled_truth = "\n".join(
        (
            f"**Event Type:** {event_type} [Source: webhook payload, {ingest_date}]",
            f"**Origin:** {source} [Source: webhook payload, {ingest_date}]",
            "",
            "## Content",
            "\n".join(f"> {line}" for line in sanitize_external_text(body).splitlines())[:2400],
        )
    )
    page_path = upsert_page(
        brain_root,
        "sources",
        title,
        compiled_truth,
        timeline_entries=[f"- {ingest_date}: Event transformed from webhook payload. [Source: webhook payload, {ingest_date}]"],
        tags=["webhook", event_type],
    )
    return page_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Transform a JSON event file into a Codex brain artifact.")
    parser.add_argument("event_file", help="Path to a JSON payload file")
    parser.add_argument("--event-type", default="auto", help="Event type (auto, meeting, sms, social, generic)")
    parser.add_argument("--date", default=default_today(), help="Event date")
    args = parser.parse_args()

    brain_root = REPO_ROOT / DEFAULT_BRAIN_ROOT
    event_path = Path(args.event_file)
    raw_payload = event_path.read_text(encoding="utf-8")
    try:
        payload = json.loads(raw_payload)
        event_type = args.event_type
        if event_type == "auto":
            if any(key in payload for key in ("attendees", "transcript", "notes")):
                event_type = "meeting"
            else:
                event_type = "generic"

        preserve_raw_text(brain_root, f"event-{slugify(event_path.stem)}", event_path.name, raw_payload)

        if event_type == "meeting":
            page_path = transform_meeting(brain_root, payload, args.date)
        else:
            page_path = transform_generic(brain_root, payload, args.date, event_type)
        print(f"Transformed event to: {page_path}")
        return 0
    except Exception:
        path = dead_letter(brain_root, args.event_type, raw_payload)
        print(f"Event transform failed. Dead-lettered payload: {path}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
