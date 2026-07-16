---
name: maintain
description: GBrain-inspired maintenance for Codex. Use when the user wants a health check, consistency audit, stale-doc sweep, or package cleanup pass.
---

# Maintain

Use this skill when the user wants a maintenance pass over the repo, docs, trackers, or saved reports.

This port is adapted from `garrytan/gbrain` at commit `b7e3005b5b3f1b54082f9c5990482ebf81a4a807`.

## Important Adaptation

Upstream GBrain runs health checks against a brain database, backlinks, and citation-bearing pages. In this repo, the closest equivalents are:

- registry and docs consistency
- missing or stale skill artifacts
- report/task file drift
- structural validation and targeted audits

## Workflow

1. Run the package checks first:
   - `python3 scripts/validate_repo.py`
   - `python3 -m unittest discover -s tests`
2. Inspect the relevant layer:
   - registries and docs
   - task or report files
   - skills and supporting references
3. Identify concrete issues:
   - stale docs
   - missing files
   - inconsistent paths or naming
   - uncategorized or duplicated reports
4. Fix what is safe and explicit.
5. Save or summarize a maintenance report when helpful.

## Guardrails

- Do not delete content without clear justification.
- Prefer specific fixes over vague "health check passed" language.
- Read before rewriting when a file is non-trivial.
