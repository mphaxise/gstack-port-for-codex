---
name: gstack-upgrade
description: Update workflow for this Codex port package. Use when the repo or local skill install should be refreshed and revalidated.
---

# GStack Upgrade

Use this skill when the local Codex port package should be updated, reinstalled, or checked against upstream changes.

This port is adapted from `garrytan/gstack` at commit `4d2c8d94d00cc4f4f3d4c26316a4f939ceedc045`.

## Workflow

1. Identify whether the request is about the repo, the local skill install, or both.
2. Refresh the relevant checkout or branch.
3. Reinstall or re-link local skills if needed.
4. Run validation and summarize what changed.

## Guardrails

- Do not claim an upgrade succeeded without revalidating the install.
- Be explicit about what was updated and what was left alone.
