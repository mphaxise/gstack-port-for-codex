---
name: install
description: Install or verify the local GBrain-style skill surface for Codex.
---

# Install

Use this skill when the user asks to install, reinstall, or verify the GBrain skillpack locally.

## Workflow

1. Inspect current local skill links under `$CODEX_HOME/skills` or `~/.codex/skills`.
2. Prefer the current Codex install location when `$CODEX_HOME` is set; otherwise use `~/.codex/skills`.
3. Link missing repo-owned skills to this checkout.
4. Do not replace existing non-repo skills.
5. Run repo validation and a local skill discovery smoke check.
6. Report missing, installed, and already-present skills.

## Guardrails

- Do not overwrite a real directory with a symlink.
- Do not install upstream global tools unless explicitly requested.
- Keep the install idempotent.
- Prefer symlinks for this local port so future repo changes are reflected without recopying.
