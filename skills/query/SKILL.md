---
name: query
description: GBrain-inspired local-brain query for Codex. Use when answering questions from the repo-local brain corpus with explicit file grounding.
---

# Query

Use this skill when the user wants an answer grounded in the local `brain/` corpus.

This port is adapted from `garrytan/gbrain` at commit `b7e3005b5b3f1b54082f9c5990482ebf81a4a807`.

## Important Adaptation

Upstream GBrain uses hybrid database-backed search. In this repo, the local brain substrate is file-based, so the deterministic search path is:

1. `python3 scripts/brain_search.py "<query>"`
2. read the top matching files
3. answer from those files with explicit path grounding

## Workflow

1. Search the local brain first.
2. Read the top relevant brain pages.
3. Synthesize only from what those pages actually say.
4. If nothing relevant exists, say the local brain does not yet contain the answer.

## Guardrails

- Do not answer from general memory when the user asked for brain-grounded context.
- Make missing coverage explicit.
- Cite the file paths you relied on.
