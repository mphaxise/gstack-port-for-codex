---
name: gbrain-upgrade
description: Check and apply upstream gbrain upgrades safely, while keeping the Codex port's local substrate honest.
---

# GBrain Upgrade

Use this skill when the user asks to update, upgrade, or verify upstream GBrain availability.

This port's current GBrain workflow-parity boundary is `garrytan/gbrain@5008b287e47bf791132eedfebf66bdef11e9398c`.

## Workflow

1. Determine which layer is being updated:
   - upstream `gbrain` CLI
   - this Codex port's GBrain skill files
   - this repo's local `brain/` substrate
2. Check local state before mutation:
   - `git status --short`
   - `codex --version`
   - `command -v gbrain`
   - `python3 scripts/brain_doctor.py`
3. Refresh the current official Codex manual before judging whether a local fallback is still necessary:
   - `node /Users/praneet/.codex/skills/.system/openai-docs/scripts/fetch-codex-manual.mjs`
   - review the relevant skills, MCP, plugins, memories, automations, sandboxing, and local environment sections
4. If the upstream CLI exists, use read-only upgrade checks first:
   - `gbrain self-upgrade --check-only --json` when available
   - `gbrain --version`
   - `gbrain doctor`
5. Apply upgrades only after the user approves, unless they explicitly requested the upgrade.
6. Re-run local validation after any update.

## Codex Adaptation

- This skill never runs a command parsed out of an `UPGRADE_AVAILABLE` marker.
- The only allowed upstream self-upgrade commands are hardcoded `gbrain self-upgrade` or `gbrain upgrade`.
- If the upstream CLI is absent, continue with this repo's file-backed GBrain port and report the absence plainly.
- Prefer current documented Codex capabilities over older Claude Code compatibility fallbacks; keep the file-backed brain and CLI/MCP fallbacks only where current host state requires them.

## Guardrails

- Do not block unrelated work on an optional upstream CLI upgrade.
- Do not convert this repo's local `brain/` corpus into another storage backend during an upgrade.
- Do not claim full upstream parity after only updating the Codex skill port.
- Do not rely on stale memory for Codex host behavior when the official manual can be refreshed.
