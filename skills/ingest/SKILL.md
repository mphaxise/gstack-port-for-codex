---
name: ingest
description: GBrain-inspired local-brain ingest for Codex. Use when turning notes, links, meetings, or observations into durable pages under the local brain corpus.
---

# Ingest

Use this skill when the user wants to save material into the local `brain/` corpus.

This port is adapted from `garrytan/gbrain` at commit `b7e3005b5b3f1b54082f9c5990482ebf81a4a807`.

## Important Adaptation

Upstream GBrain writes into a separate brain system. In this repo, ingestion means creating or updating Markdown pages under `brain/`.

## Workflow

1. Identify the primary subject:
   - person
   - company
   - concept
   - original idea
   - source
   - meeting
2. Search for an existing page before creating a new one.
3. Create or update the page with:
   - frontmatter
   - compiled truth
   - timeline evidence
4. Preserve citations or source notes inline when possible.

## Guardrails

- Do not create duplicate pages if a matching one already exists.
- Keep raw evidence separate from synthesized compiled truth.
- Favor small, durable updates over giant dumps of unstructured text.
