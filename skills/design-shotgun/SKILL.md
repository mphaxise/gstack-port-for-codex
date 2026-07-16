---
name: design-shotgun
description: Rapid design-variant exploration for Codex. Use when the user wants multiple UI directions, visual options, or a faster feedback loop on taste.
---

# Design Shotgun

Use this skill when the user wants to see several substantially different design directions before committing to one.

This port is adapted from `garrytan/gstack` at commit `4d2c8d94d00cc4f4f3d4c26316a4f939ceedc045`.

## Workflow

1. Capture the product surface, constraints, and non-negotiables.
2. Produce 4-6 meaningfully different directions, not tiny variations.
3. For each direction, name:
   - the thesis
   - the visual mood
   - the main tradeoff
4. If the environment supports it, generate or assemble visual variants; otherwise describe them in a structured way.
5. Narrow based on the user's reaction and iterate.

## Guardrails

- Do not waste cycles on superficial color swaps.
- Keep each direction distinct enough that the user can develop taste preferences.
- Stay anchored to the product goal rather than free-associating visually.

## Outputs

Always include:

- the set of design directions
- what makes each one distinct
- recommended favorite and why
- what feedback to collect next
