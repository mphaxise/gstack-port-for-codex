---
name: gbrain-upgrade
description: Check and apply upstream gbrain upgrades safely, while keeping the Codex port's local substrate honest.
---

# GBrain Upgrade

Use this skill when the user asks to update, upgrade, or verify upstream GBrain availability.

This port is adapted from `garrytan/gbrain` at commit `814258dda67945ffec9457a1e73980e947b7e462`.

## Workflow

1. Determine which layer is being updated:
   - upstream `gbrain` CLI
   - this Codex port's GBrain skill files
   - this repo's local `brain/` substrate
2. Check local state before mutation:
   - `git status --short`
   - `command -v gbrain`
   - `python3 scripts/brain_doctor.py`
3. If the upstream CLI exists, use read-only upgrade checks first:
   - `gbrain self-upgrade --check-only --json` when available
   - `gbrain --version`
   - `gbrain doctor`
4. Apply upgrades only after the user approves, unless they explicitly requested the upgrade.
5. Re-run local validation after any update.

## Codex Adaptation

- This skill never runs a command parsed out of an `UPGRADE_AVAILABLE` marker.
- The only allowed upstream self-upgrade commands are hardcoded `gbrain self-upgrade` or `gbrain upgrade`.
- If the upstream CLI is absent, continue with this repo's file-backed GBrain port and report the absence plainly.

## Guardrails

- Do not block unrelated work on an optional upstream CLI upgrade.
- Do not convert this repo's local `brain/` corpus into another storage backend during an upgrade.
- Do not claim full upstream parity after only updating the Codex skill port.
