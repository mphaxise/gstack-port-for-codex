---
name: skillpack-check
description: Produce a health report for the local combined GStack and GBrain skillpack.
---

# Skillpack Check

Use this skill when the user asks whether the installed skillpack is healthy.

## Workflow

1. Run repository validation.
2. Run unit tests.
3. Check registry coverage against upstream snapshots when available.
4. Check local installed symlinks under `~/.codex/skills`.
5. Run `brain_doctor.py` when the local brain substrate is in scope.
6. Report pass/fail with exact gaps.

## Guardrails

- Do not say healthy if local install or registry validation failed.
- Do not mutate files during a check.
- Separate repo health from upstream parity.
