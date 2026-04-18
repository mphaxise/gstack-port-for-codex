---
name: design-html
description: Design-to-implementation workflow for Codex. Use when an approved design should become real HTML, CSS, or framework-native UI code.
---

# Design HTML

Use this skill when the user has an approved design direction and wants it translated into implementation code.

This port is adapted from `garrytan/gstack` at commit `4d2c8d94d00cc4f4f3d4c26316a4f939ceedc045`.

## Workflow

1. Confirm the design source:
   - approved mockup
   - design doc
   - existing UI direction
   - written description
2. Translate the design into the repo's actual UI stack.
3. Keep the implementation responsive, content-aware, and production-minded.
4. Verify at multiple viewport sizes or by inspecting the rendered result when possible.

## Guardrails

- Do not ship a one-viewport mockup disguised as finished UI.
- Preserve the repo's existing framework and design conventions.
- Avoid generic boilerplate layouts when the design calls for a stronger point of view.

## Outputs

Always include:

- source design used
- implementation approach
- responsive considerations
- what was verified
- remaining visual risks
