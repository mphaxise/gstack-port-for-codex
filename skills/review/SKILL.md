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
2. Name the review mode before assigning a reviewer:
   - `acceptance`: determine whether the frozen package satisfies named criteria
   - `risk`: challenge assumptions, seek counterexamples, and find plausible
     failure paths across safety, privacy, data, authorization, and trust
     boundaries
   - `fresh-eyes discovery`: exercise the user journey without the
     implementation narrative and look for new interaction or comprehension
     failures
3. Review risk in two passes:
   - critical: safety, concurrency, data integrity, authorization, and trust boundaries
   - informational: consistency, tests, frontend behavior, prompt drift, and maintenance risks
4. Use additional review panels only when they own materially distinct risk surfaces.
5. Give every panel the same frozen package, the smallest context needed for its
   mode, and explicit read-only authority. For fresh-eyes discovery, provide the
   outcome contract, runnable artifact, states, and safety boundaries; withhold
   implementation rationale and prior reviewer conclusions.
6. Keep the controlling agent responsible for edits, builds, runtime or Simulator control, Git, and connected services.
7. If GitHub CLI and Greptile comments are available, optionally apply `references/greptile-triage.md`.

For a user-facing change, read the project's applicable prevention entries and
run a distinct UX recurrence pass against the frozen package. Check the named
journey and state invariants plus known issue families. Keep this separate from
a fresh-eyes discovery pass, which looks for new problems by exercising the
complete journey, including repeat entry, interruption, denial, cancellation,
and return when applicable. A reviewer should challenge any prerequisite or
status screen that gives the user no resolving action.

Confirm that the plan included applicable prior prevention entries, named
invariants, counterexamples, and adjacent surfaces. Route every material new
discovery into the project's single canonical backlog or feedback record with
an explicit classification and acceptance impact.

## Corrections And Receipts

- After a correction, rerun only panels and checks whose recorded inputs or risk surface changed.
- Reuse an unaffected receipt only when its base, head, evidence, requirements, and environment still match.
- Run one consolidated review after all required corrections are stable.
- For every corrected material issue, ask which safeguard would have caught it
  before acceptance. Replay the smallest reproduction against that safeguard.
- Record the UX recurrence result as `clear`, `clear with new prevention`,
  `blocked`, or `unknown`. A known recurrence without verified prevention blocks
  acceptance.
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
