---
name: connect-chrome
description: Browser-attach compatibility workflow for Codex. Use when the user asks to connect Chrome or open a visible browser session for browser-driven work.
---

# Connect Chrome

Use this skill as the compatibility wrapper for `open-gstack-browser`.

This port is adapted from `garrytan/gstack` at commit `4d2c8d94d00cc4f4f3d4c26316a4f939ceedc045`.

## Workflow

1. Treat the request as a visible-browser request.
2. Follow the `open-gstack-browser` workflow.
3. Make the actual runtime capabilities explicit.

## Guardrails

- Do not imply that a Chrome-specific integration exists if the environment only supports a generic browser path.
