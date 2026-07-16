---
name: enrich
description: GBrain-inspired local-brain enrichment for Codex. Use when improving a person, company, or concept page with newly learned context and evidence.
---

# Enrich

Use this skill when the user wants to deepen an existing `brain/` page rather than create a fresh one.

This port is adapted from `garrytan/gbrain` at commit `b7e3005b5b3f1b54082f9c5990482ebf81a4a807`.

## Important Adaptation

Upstream GBrain enrichment can rely on APIs and a deeper backend. In this repo, enrichment means updating file-backed pages with better compiled truth, new timeline items, and clearer citations.

## Workflow

1. Find the existing page.
2. Read the compiled truth and timeline before editing.
3. Add the new evidence or synthesize a better compiled truth section.
4. Keep timeline entries dated and explicit.

## Guardrails

- Do not overwrite useful prior context without reading it.
- Keep new facts tied to a source note when available.
- Prefer updating the right existing page over scattering context across duplicates.
