# Codex Brain

This directory is the minimal local substrate that makes the GBrain memory skills applicable in Codex without a separate database.

## Layout

- `people/`
- `companies/`
- `concepts/`
- `ideas/`
- `originals/`
- `sources/`
- `meetings/`
- `reports/`

## Page Shape

Use simple Markdown pages with frontmatter, compiled truth above the separator, and timeline evidence below it:

```md
---
title: Jane Doe
type: person
tags: [founder, ai]
---

Jane Doe is the founder of Example Labs. [Source: meeting notes, 2026-04-16]

---

- 2026-04-16: Met in the product review. [Source: meeting notes, 2026-04-16]
```

## Helper Scripts

- `python3 scripts/brain_init.py`
- `python3 scripts/brain_search.py "query"`
- `python3 scripts/brain_put.py --title ... --category ... --text "..."`
- `python3 scripts/brain_link.py --from-ref ... --to-ref ... --context "..."`
- `python3 scripts/brain_citations.py --fix --verbose`
- `python3 scripts/brain_ingest_source.py <file> --title ...`
- `python3 scripts/brain_sync_source.py <file> --title ...`
- `python3 scripts/brain_ingest_meeting.py <file> --title ... --date ...`
- `python3 scripts/brain_transform_event.py payload.json --event-type auto`
- `python3 scripts/brain_capture_signal.py --text "..." --mode original`
- `python3 scripts/brain_doctor.py`

Use `brain_ingest_source.py` for a one-time capture. Use
`brain_sync_source.py` for a mutable authoritative file: it replaces current
compiled truth when the source hash changes, retains a cited version and
supersession timeline, and performs a byte-for-byte no-op when unchanged.
The canonical resolved source path is the stable identity key. Managed
projections refuse unmanaged-page and source-path collisions.

All generated brain content is private and ignored by default. Only this
`brain/README.md` substrate description is tracked.
