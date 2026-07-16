---
name: voice-note-ingest
description: Ingest a voice note while preserving exact phrasing and routing ideas, people, and concepts into the brain.
---

# Voice Note Ingest

Use this skill when the user provides a voice note transcript or asks to ingest a voice note.

## Workflow

1. Preserve the exact transcript as raw source.
2. Extract:
   - original phrasing
   - ideas
   - people or companies
   - tasks
   - concepts
   - emotional or strategic context
3. Use `brain-taxonomist` for new pages.
4. Use `capture` for the core note and specialized ingest skills for derived pages.
5. Return a receipt with created or recommended paths.

## Guardrails

- Do not paraphrase the user's exact words in the preserved source.
- Do not infer sensitive facts beyond the transcript.
- Do not overwrite existing brain pages without asking.
