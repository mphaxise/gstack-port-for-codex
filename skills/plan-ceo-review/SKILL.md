---
name: plan-ceo-review
description: Founder-style plan review for Codex. Use when a user wants to pressure-test a product or feature plan before implementation.
---

# Plan CEO Review

Use this skill when the task is still in planning or discovery and the highest-leverage move is to rethink the problem before coding.

This port is adapted from `garrytan/gstack` at commit `2aa745cb0e4331d683e727ec77385d04cdbb45a2`.

## Goals

- challenge the stated request, not just polish it
- identify the real user outcome behind the ask
- find leverage in what already exists
- surface risks, edge cases, and explicit "not in scope" decisions
- leave the user with a sharper next move

## Mode Selection

Pick one mode and state it explicitly in the response:

- `SCOPE EXPANSION`: default for greenfield ideas or when the user wants the ambitious version
- `HOLD SCOPE`: default for bug fixes, refactors, or plans whose scope is already accepted
- `SCOPE REDUCTION`: default when the user wants the thinnest useful MVP

If the right mode is unclear and the choice would materially change the advice, ask one concise question with 2-3 concrete options. Otherwise choose the best mode and state the assumption.

For the detailed defaults, read `references/mode-cheatsheet.md`.

## Workflow

1. Read only the materials needed to understand the plan, repo, and relevant constraints.
2. Identify the actual outcome the user wants, not just the literal feature request.
3. Map existing leverage before suggesting new work.
4. Review the plan using the selected mode.
5. Produce a structured output using `references/output-template.md`.

## Review Standard

- Be opinionated and concrete.
- Name the biggest risks, not every imaginable one.
- Prefer explicit tradeoffs over fuzzy advice.
- Keep the plan realistic for the current repo and team context.
- Call out anything that should be deferred in a `Not in scope` section.

## Guardrails

- Do not start implementation unless the user explicitly pivots from planning to coding.
- Ask at most one concise question at a time, and only when a real ambiguity blocks a good recommendation.
- If a better framing exists, say so directly.
- If the current plan is good, say that too and focus on the highest-value refinements.

## Outputs

Always include:

- selected mode and why
- problem framing
- what already exists
- recommended plan
- risks and failure modes
- not in scope
- next 1-3 actions

For the full structure and tables, read `references/output-template.md`.

