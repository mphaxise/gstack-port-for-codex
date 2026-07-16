# Codex Brain Substrate

## Purpose

This repo includes a minimal local `brain/` corpus so the GBrain memory-oriented skills can run honestly in Codex without pretending a separate retrieval backend already exists.

## What It Enables

- `query`
- `ingest`
- `enrich`
- `brain-ops`
- `signal-detector`
- `idea-ingest`
- `media-ingest`
- `meeting-ingestion`
- `citation-fixer`
- `webhook-transforms`

## Shape

The substrate is file-based:

- `brain/people/`
- `brain/companies/`
- `brain/concepts/`
- `brain/ideas/`
- `brain/originals/`
- `brain/sources/`
- `brain/meetings/`
- `brain/reports/`

Each page uses frontmatter plus a compiled-truth-and-timeline split.

## Deterministic Helpers

- `python3 scripts/brain_init.py`
  - ensures the local brain directories exist
- `python3 scripts/brain_search.py "query"`
  - keyword-weighted search across brain pages
- `python3 scripts/brain_put.py ...`
  - create or update a page
- `python3 scripts/brain_link.py ...`
  - add backlinks between pages
- `python3 scripts/brain_citations.py --fix`
  - audit and normalize citation markup
- `python3 scripts/brain_ingest_source.py <file> ...`
  - ingest a local source file and preserve the raw artifact
- `python3 scripts/brain_ingest_meeting.py <file> ...`
  - turn a transcript or meeting-note file into a structured meeting page
- `python3 scripts/brain_transform_event.py payload.json --event-type auto`
  - replay a webhook-style JSON payload into the local brain
- `python3 scripts/brain_capture_signal.py --text "..."`
  - capture user phrasing into `ideas`, `originals`, or `concepts`
- `python3 scripts/brain_doctor.py`
  - corpus-health checks and counts

## Intentional Limits

This is not full upstream backend parity.

It does not provide:

- vector search
- a separate retrieval database
- a live inbound webhook server
- a true always-on daemon
- autonomous background write loops

It is the minimum honest substrate needed to make the memory-oriented GBrain ports real in this repo.
