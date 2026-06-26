---
name: skillpack-check
description: Produce a health report for the local combined GStack and GBrain skillpack.
---

# Skillpack Check

Use this skill when the user asks whether the installed skillpack is healthy.

## Workflow

1. Run repository validation.
2. Run unit tests.
3. Check registry coverage against upstream snapshots when available:
   - `python3 scripts/check_upstream_drift.py`
   - `python3 scripts/check_upstream_drift.py --map gbrain`
4. Check local installed symlinks under `$CODEX_HOME/skills` or `~/.codex/skills`.
5. Run `brain_doctor.py` when the local brain substrate is in scope.
6. Run `brain_citations.py --verbose` when citation quality is in scope.
7. Report pass/fail with exact gaps.

## Guardrails

- Do not say healthy if local install or registry validation failed.
- Do not mutate files during a check.
- Separate repo health from upstream parity.
