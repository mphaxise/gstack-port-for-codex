---
name: citation-fixer
description: GBrain-inspired citation audit for Codex. Use when the local brain corpus needs citation normalization or a pass over remaining uncited lines.
---

# Citation Fixer

Use this skill when the user wants citation cleanup or when a brain-writing change touched enough pages that citation drift is a risk.

This port is adapted from `garrytan/gbrain` at commit `b7e3005b5b3f1b54082f9c5990482ebf81a4a807`.

## Workflow

1. Audit first:
   - `python3 scripts/brain_citations.py --verbose`
2. Normalize formatting when useful:
   - `python3 scripts/brain_citations.py --fix --verbose`
3. Read the remaining gaps manually.
4. Fix missing citations with real sources or leave them explicitly unresolved.

## Guardrails

- Do not invent citations for unsupported facts.
- Do not bulk-normalize without reading the remaining unresolved lines.
- Treat this as a quality pass, not a reason to rewrite unrelated content.
