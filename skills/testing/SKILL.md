---
name: testing
description: GBrain-inspired skill conformance checks for Codex. Use when validating the growing combined GStack and GBrain skill surface.
---

# Testing

Use this skill when validating that the skill package still hangs together after changes.

This port is adapted from `garrytan/gbrain` at commit `b7e3005b5b3f1b54082f9c5990482ebf81a4a807`.

## Workflow

1. Validate required docs and registries.
2. Check that every `ported` skill has a real `SKILL.md` with valid frontmatter.
3. Run the lightweight repo checks:
   - `python3 scripts/validate_repo.py`
   - `python3 -m unittest discover -s tests`
4. If the surface changed materially, inspect `python3 scripts/print_status.py`.
5. Report failures concretely and in priority order.

## Guardrails

- Do not declare the package healthy without running the checks.
- Prefer structural issues and regressions over style notes.
- Keep the validation rules aligned with the real repo structure.
