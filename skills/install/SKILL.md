---
name: install
description: Install or verify the local GBrain-style skill surface for Codex.
---

# Install

Use this skill when the user asks to install, reinstall, or verify the GBrain skillpack locally.

## Workflow

1. Inspect current local skill links under `$CODEX_HOME/skills` or `~/.codex/skills`.
2. Link missing repo-owned skills to this checkout.
3. Do not replace existing non-repo skills.
4. Run repo validation.
5. Report missing, installed, and already-present skills.

## Guardrails

- Do not overwrite a real directory with a symlink.
- Do not install upstream global tools unless explicitly requested.
- Keep the install idempotent.
