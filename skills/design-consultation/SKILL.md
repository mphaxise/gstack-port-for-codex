---
name: design-consultation
description: Design-system creation and direction-setting for Codex. Use when a project needs a stronger visual point of view, design principles, or a reusable design language.
---

# Design Consultation

Use this skill when the user wants a design direction, design system, or a stronger visual language before polishing or implementation.

This port is adapted from `garrytan/gstack` at commit `4d2c8d94d00cc4f4f3d4c26316a4f939ceedc045`.

## Workflow

1. Understand the product, audience, constraints, and existing brand cues.
2. Propose a cohesive design direction across:
   - aesthetic
   - typography
   - color
   - spacing
   - layout
   - motion
3. Identify deliberate risks worth taking so the product does not collapse into generic AI output.
4. If the user wants a saved source of truth, create or update a design document in `docs/`.

## Guardrails

- Do not generate a design system that ignores the actual product or audience.
- Avoid default-safe palettes and generic component language when the project needs a stronger identity.
- Preserve established systems when the repo already has one.

## Outputs

Always include:

- design thesis
- visual direction
- design principles
- constraints or anti-goals
- recommended next artifacts to create
