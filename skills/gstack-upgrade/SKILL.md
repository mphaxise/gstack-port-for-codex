---
name: gstack-upgrade
description: Update workflow for this Codex port package. Use when the repo or local skill install should be refreshed and revalidated.
---

# GStack Upgrade

Use this skill when the local Codex port package should be updated, reinstalled, or checked against upstream changes.

This port is adapted from `garrytan/gstack` at commit `11de390be1be6849eb9a15f91ff4922dd16c589a`.

## Workflow

1. Identify whether the request is about the repo, the local skill install, or both.
2. Refresh upstream refs for both `garrytan/gstack` and `garrytan/gbrain` when parity is in scope.
3. Port upstream changes into Codex-native skill files instead of copying Claude-specific preambles.
4. Reinstall or re-link local skills if needed.
5. Run validation and summarize what changed.

## Codex Host Audit

When upstream changed since the last port, explicitly decide which parts are:

- clean to port into `skills/`, `data/`, `docs/`, or `tests/`
- useful locally but not publishable, such as generated `brain/` corpus pages
- blocked on upstream runtime, database, MCP, browser daemon, or Claude-specific behavior

Prefer current Codex install behavior over older Claude Code fallbacks when Codex has a direct equivalent. Keep fallbacks only for host-variable runtimes such as browser automation, upstream `gbrain` CLI availability, and remote credentials.

## Guardrails

- Do not claim an upgrade succeeded without revalidating the install.
- Be explicit about what was updated and what was left alone.
- Do not move baseline source pins forward if only a subset of upstream changes was ported; use per-skill `source_commit` metadata instead.
