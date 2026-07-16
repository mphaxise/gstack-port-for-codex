---
name: autoplan
description: Automatic planning pipeline for Codex. Use when the user wants one command to run the current planning stack and consolidate the result into a single reviewed plan.
---

# Autoplan

Use this skill when the user wants the repo's planning stack applied in one pass instead of invoking each planning skill manually.

This port is adapted from `garrytan/gstack` at commit `4d2c8d94d00cc4f4f3d4c26316a4f939ceedc045`.

## Important Adaptation

The current Codex port has a partial planning surface:

- `office-hours`
- `plan-ceo-review`
- `plan-eng-review`

The upstream design and DX planning skills are not ported here yet. Do not pretend they ran. Instead, call out design and DX blind spots explicitly in the final output.

## Workflow

1. Read the plan, idea note, or repo context.
2. If the idea is still fuzzy or pre-plan, start with `office-hours`.
3. Apply the `plan-ceo-review` lens to pressure-test framing and scope.
4. Apply the `plan-eng-review` lens to pressure-test architecture, sequencing, and tests.
5. Add an explicit section for missing design and developer-experience review coverage.
6. Consolidate the result into one recommended plan with concrete next actions.

## Guardrails

- Do not claim that `plan-design-review` or `plan-devex-review` ran unless those skills exist in the current repo and you actually used them.
- Ask at most one concise question when a real ambiguity would change the recommendation materially.
- Do not start implementation unless the user explicitly pivots from planning to coding.
- Prefer one final integrated recommendation over dumping three disconnected mini-reviews.

## Outputs

Always include:

- what inputs were reviewed
- whether `office-hours` was used
- CEO/framing findings
- engineering/execution findings
- design and DX blind spots
- consolidated recommendation
- next 1-3 actions
