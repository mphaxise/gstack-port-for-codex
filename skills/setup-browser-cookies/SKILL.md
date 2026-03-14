---
name: setup-browser-cookies
description: Authenticated browser-session setup workflow for Codex. Use when QA or browser testing needs a logged-in session.
---

# Setup Browser Cookies

Use this skill when a browser-based workflow needs authentication and the best path is to import or recreate a logged-in session.

This port is adapted from `garrytan/gstack` at commit `2aa745cb0e4331d683e727ec77385d04cdbb45a2`.

## Workflow

1. Read `references/session-options.md`.
2. Choose the safest available session strategy.
3. Import or recreate the session.
4. Verify the session works before starting QA.

## Guardrails

- Never print raw cookie values.
- Prefer domain counts, session summaries, or successful page access as proof.
- If secure browser extraction is unavailable, fall back to cookie JSON import, manual login, or app-supported test-session seeding.

