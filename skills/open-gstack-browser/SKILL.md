---
name: open-gstack-browser
description: Visible-browser launch workflow for Codex. Use when a headed browser session is needed for browser testing, inspection, or human handoff.
---

# Open GStack Browser

Use this skill when the user wants a visible browser session rather than a purely headless or code-only review path.

This port is adapted from `garrytan/gstack` at commit `4d2c8d94d00cc4f4f3d4c26316a4f939ceedc045`.

## Workflow

1. Identify the best available browser runtime in the current environment.
2. Launch or attach to a visible browser session when the tooling allows it.
3. Use that browser for inspection, QA, or handoff.
4. Report clearly if the environment only supports headless or read-only alternatives.

## Guardrails

- Do not claim a headed browser was opened if the environment could not do it.
- Prefer the repo's normal browser workflow when one already exists.
- Keep the handoff path explicit when human interaction is required.
