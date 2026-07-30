---
name: feedback-integration
description: Integrate iterative user or reviewer feedback into active work while preserving unrelated work. Use for corrections, preferences, acceptance notes, bugs, UX recurrence findings, or review feedback that need triage, prevention, verification, and a checkpoint.
---

# Feedback Integration

Turn incoming feedback into a small, traceable correction loop while preserving required quality and the user's authority boundaries.

Read `references/feedback-loop-template.md` when creating a feedback batch or handoff.

## Triage

1. Record each feedback item in plain language and link it to its source.
2. Classify it:
   - `interrupt`: address now because it identifies a safety, privacy, data-loss, production, or blocking risk, or because the user explicitly says to act now
   - `batch`: group it with related feedback for the next coherent correction slice
   - `record`: retain it as a preference or future consideration without changing the active slice
3. Continue the current work for `batch` and `record` items. Do not request an immediate response.
4. Stop and ask only when feedback changes the goal, authority boundary, risk class, or acceptance criteria in a way that requires the user's decision.

## Build A Correction Slice

1. Group related feedback by one screen, interaction, component, or acceptance outcome.
2. Define:
   - the exact feedback items included
   - a narrow file or artifact allowlist
   - acceptance criteria
   - evidence that the change invalidates
   - evidence that remains reusable
3. Freeze a baseline package before editing. Include only the source map, relevant diff or artifact, applicable requirements, and current receipts.
4. Apply one coherent correction pass. Avoid opportunistic cleanup and unrelated improvements.

## Prevent Recurrence

For every material bug or UX issue, add one compact prevention entry to the
existing project feedback or decision record:

- symptom and smallest reliable reproduction
- intended product, UX, visual, accessibility, privacy, or service invariant
- introduction point when known
- why existing planning, implementation, tests, or review missed it
- affected journeys, states, screens, and platforms
- fix evidence
- strongest prevention added

Prefer prevention in this order: deterministic test, invariant with evidence
gate, reusable fixture or harness, project acceptance rule, then reusable skill
guidance. Verify that the prevention would have caught the original issue before
acceptance.

Before closing a user-facing slice, check prior project prevention entries for
the same issue family. Include action hierarchy, discoverability, clipping,
geometry, semantic color, text scaling, permission timing and recovery,
interruption, navigation continuity, and state restoration when applicable.

Use these escalation rules:

- first ordinary occurrence: project-local prevention
- second similar occurrence: mark recurring and inspect related surfaces
- third accepted occurrence: propose reusable skill guidance
- critical safety, privacy, accessibility, commerce, destructive-action, or
  data-integrity issue: add the appropriate gate immediately

Keep discovery separate. Recurrence review checks known patterns; a fresh-eyes
discovery pass looks for new problems.

## Verify In Tiers

Run the narrowest sufficient sequence, expanding only when the prior tier passes or exposes a wider dependency:

1. focused deterministic checks for the changed slice
2. affected tests, states, or flows
3. required consolidated suites
4. one build or runtime pass after the correction set is stable

Repeat a tier only when an input changed, a failure needs diagnosis, or new evidence requires it. Do not reduce accessibility, privacy, safety, backend, test, build, or acceptance coverage.

## Review And Close

- Give every reviewer the same frozen package.
- Use only panels whose concerns are affected by the correction.
- For a user-facing slice, require one UX recurrence result: `clear`, `clear with
  new prevention`, `blocked`, or `unknown`.
- Block acceptance when a known issue recurs without verified prevention or when
  evidence is insufficient to classify a material recurrence risk.
- Keep reviewers read-only. The controlling agent owns edits, builds, Simulator or browser control, Git, and connected-service actions.
- Reuse a receipt only when its recorded inputs still match. Mark it `invalidated` or `unknown` otherwise.
- Save a compact checkpoint after the slice. Include the updated source map, receipt status, remaining feedback, and the next action.
- Recommend a fresh task when the active packet or reset rules in `context-save` say continuation is no longer efficient. Do not create one unless the user asks.

## Guardrails

- Treat user feedback as evidence. Limit changes to the authority it grants.
- Preserve explicit stop, approval, privacy, release, and external-state gates.
- Separate observed facts, user-supplied claims, estimates, and unknowns.
- Do not quantify token, time, or quality savings without direct evidence.
- Do not reopen completed review panels when their inputs and risk surface are unchanged.
