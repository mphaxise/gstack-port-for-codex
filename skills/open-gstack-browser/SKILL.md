---
name: open-gstack-browser
description: Visible-browser launch workflow for Codex. Use when a headed browser session is needed for browser testing, inspection, or human handoff.
---

# Open GStack Browser

Use this skill when the user wants a visible browser session rather than a purely headless or code-only review path.

This port is adapted from `garrytan/gstack` at commit `11de390be1be6849eb9a15f91ff4922dd16c589a`.

## Workflow

1. Identify the best available browser runtime in the current environment.
2. Prefer current Codex browser/Chrome tooling when available.
3. Launch or attach to a visible browser session when the tooling allows it.
4. Use that browser for inspection, QA, or handoff.
5. Report clearly if the environment only supports headless or read-only alternatives.

## Guardrails

- Do not claim a headed browser was opened if the environment could not do it.
- Prefer the repo's normal browser workflow when one already exists.
- Keep the handoff path explicit when human interaction is required.
- Do not install or vendor upstream GStack browser daemons as a side effect of opening a browser.
