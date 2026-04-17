---
name: setup
description: GBrain-inspired setup for Codex. Use when establishing the local package, file conventions, identity files, or a future substrate for the GBrain layer.
---

# Setup

Use this skill when the user wants to initialize or normalize the Codex-side GBrain package setup.

This port is adapted from `garrytan/gbrain` at commit `b7e3005b5b3f1b54082f9c5990482ebf81a4a807`.

## Workflow

1. Inspect what already exists in the repo.
2. Decide which setup layer is needed:
   - docs and registries
   - identity files
   - task/report directories
   - future memory-substrate placeholders
3. Create only the minimal durable structure needed.
4. Verify the package still validates after setup changes.

## Guardrails

- Do not bootstrap a fake backend just to mimic upstream GBrain setup.
- Prefer explicit conventions over hidden magic.
- Keep setup reversible and easy to understand from the repo itself.
