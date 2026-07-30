---
name: design-review
description: Live design audit and polish workflow for Codex. Use when an implemented UI should be reviewed for visual quality, interaction quality, and consistency.
---

# Design Review

Use this skill when a real interface exists and the task is to audit or improve its visual and interaction quality.

This port is adapted from `garrytan/gstack` at commit `4d2c8d94d00cc4f4f3d4c26316a4f939ceedc045`.

## Workflow

1. Resolve the target to a stable file, route, component, or URL. Load the project design context and representative source.
2. Run an unanchored visual and interaction pass before reading deterministic findings.
3. Inspect the implemented UI using the best available evidence path:
   - browser testing
   - screenshots
   - local rendering
   - source review when visual verification is limited
4. Run the optional Impeccable detector through `design-quality` when it is already installed. Record rule IDs, false positives, and skipped evidence paths.
5. Identify the highest-value design issues:
   - hierarchy
   - spacing
   - readability
   - consistency
   - responsiveness
   - motion or feedback
6. Run a distinct UX recurrence pass using the project's prevention entries,
   named invariants, and known issue families. Check applicable journey states,
   normal and maximum text sizes, action hierarchy, discoverability, clipping,
   geometry, semantic color, permission recovery, interruption, navigation
   continuity, and state restoration.
7. Keep a fresh-eyes discovery pass separate from recurrence review.
8. Tag findings P0 to P3 and separate aesthetic judgment from deterministic or accessibility evidence.
9. Record recurrence as `clear`, `clear with new prevention`, `blocked`, or
   `unknown`. Block acceptance for a known recurrence without verified
   prevention or insufficient material evidence.
10. Fix the most important issues directly in code when the user wants changes.
11. Re-check the result and verify that each new prevention would have caught
    the original issue before acceptance.
12. When persistence is useful and authorized, save the review under `reports/design-reviews/` and compare it with the latest report for the same target.

## Guardrails

- Preserve the existing design system when one already exists.
- Do not introduce generic AI-slop styling.
- Be explicit when you could only review source code and not the live UI.
- If the user wants critique only, report issues without making fixes.
- Use independent subagents only when the user has authorized delegation; otherwise run the evidence passes sequentially and state the method.

## Outputs

Always include:

- what was reviewed
- top design issues
- fixes made or recommended
- verification path used
- detector status and justified exceptions
- UX recurrence result and prevention added
- remaining blind spots
