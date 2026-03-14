---
name: browse
description: Browser QA and dogfooding workflow for Codex. Use when a user needs interactive verification of a web app, page flow, or deployment.
---

# Browse

Use this skill when the task requires browser-based verification instead of static code reading.

This port is adapted from `garrytan/gstack` at commit `2aa745cb0e4331d683e727ec77385d04cdbb45a2`.

## Important Adaptation

This repo ports the browse workflow, not the upstream Playwright binary itself. Before testing, read `references/runtime-strategy.md` and choose the best browser path available in the current Codex environment.

## Core Jobs

- verify a page loads and key elements appear
- test a user flow end to end
- capture before/after evidence for bug reports
- inspect console, network, or page state when the tooling allows it
- check responsive layouts and authenticated flows when possible

## Workflow

1. Choose the runtime path from `references/runtime-strategy.md`.
2. Translate the desired action using `references/browser-command-map.md`.
3. Test the target page or flow.
4. Collect evidence: screenshots, repro steps, state changes, and any blind spots.

## Guardrails

- Never claim browser automation happened if you only performed HTTP or static checks.
- If authenticated access is required, coordinate with `setup-browser-cookies` or manual login steps.
- Report what was tested, what was blocked, and what remains unverified.

