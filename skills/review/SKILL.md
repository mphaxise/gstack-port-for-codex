---
name: review
description: Review a branch or change package before landing, using one frozen evidence package, focused risk panels, reusable receipts, and findings-first output.
---

# Review

Find bugs and material risks before a change lands.

This port is adapted from `garrytan/gstack` at commit `2aa745cb0e4331d683e727ec77385d04cdbb45a2`.

## Prepare One Frozen Package

1. Confirm the current branch is not `main` and a real diff exists against the intended base.
2. Read `references/checklist.md`.
3. Freeze one package containing:
   - base and head revisions
   - full diff
   - applicable instructions and acceptance criteria
   - changed-file allowlist
   - tests, builds, screenshots, or other direct evidence already produced
4. Record direct fingerprints or hashes when available. Do not modify the package during a review pass.

## Review

1. Read the full frozen diff once.
2. Review in two passes:
   - critical: safety, concurrency, data integrity, authorization, and trust boundaries
   - informational: consistency, tests, frontend behavior, prompt drift, and maintenance risks
3. Use additional review panels only when they own materially distinct risk surfaces.
4. Give every panel the same frozen package and explicit read-only authority.
5. Keep the controlling agent responsible for edits, builds, runtime or Simulator control, Git, and connected services.
6. If GitHub CLI and Greptile comments are available, optionally apply `references/greptile-triage.md`.

## Corrections And Receipts

- After a correction, rerun only panels and checks whose recorded inputs or risk surface changed.
- Reuse an unaffected receipt only when its base, head, evidence, requirements, and environment still match.
- Run one consolidated review after all required corrections are stable.
- Avoid duplicate panels, full-history forks, and repeated full-diff reads without changed evidence.

## Output Rules

- Put findings first, ordered by severity.
- Include file and line references when possible.
- Distinguish blocking from non-blocking findings.
- For each clean panel, record its scope and frozen-package identity as a receipt.
- If no issues remain, say so explicitly and name any unverified or invalidated evidence.

## Guardrails

- Keep review read-only unless the user explicitly asks for fixes.
- Skip stylistic nitpicks unless they create real risk.
- Never reuse a receipt after its covered inputs change.
- Do not reduce required security, privacy, accessibility, test, build, or acceptance coverage to save tokens.
