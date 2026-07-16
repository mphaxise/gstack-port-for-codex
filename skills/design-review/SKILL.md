---
name: design-review
description: Live design audit and polish workflow for Codex. Use when an implemented UI should be reviewed for visual quality, interaction quality, and consistency.
---

# Design Review

Use this skill when a real interface exists and the task is to audit or improve its visual and interaction quality.

This port is adapted from `garrytan/gstack` at commit `4d2c8d94d00cc4f4f3d4c26316a4f939ceedc045`.

## Workflow

1. Inspect the implemented UI using the best available evidence path:
   - browser testing
   - screenshots
   - local rendering
   - source review when visual verification is limited
2. Identify the highest-value design issues:
   - hierarchy
   - spacing
   - readability
   - consistency
   - responsiveness
   - motion or feedback
3. Fix the most important issues directly in code when the user wants changes.
4. Re-check the result and summarize what improved and what is still unverified.

## Guardrails

- Preserve the existing design system when one already exists.
- Do not introduce generic AI-slop styling.
- Be explicit when you could only review source code and not the live UI.
- If the user wants critique only, report issues without making fixes.

## Outputs

Always include:

- what was reviewed
- top design issues
- fixes made or recommended
- verification path used
- remaining blind spots
