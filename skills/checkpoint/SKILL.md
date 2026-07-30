---
name: checkpoint
description: Legacy save-and-resume compatibility workflow. Use when a user asks for a checkpoint; route the save through context-save and the resume through context-restore.
---

# Checkpoint

Preserve compatibility with requests that use the older `checkpoint` name.

This port is adapted from `garrytan/gstack` at commit `4d2c8d94d00cc4f4f3d4c26316a4f939ceedc045`.

## Workflow

1. Use `context-save` when capturing current work.
2. Produce its compact active packet, source map, receipt classifications, slice telemetry, and reset recommendation.
3. Use `context-restore` when resuming from that packet.
4. Prefer one canonical checkpoint over scattered status narration.

## Guardrails

- Keep the packet at or below the `context-save` limit.
- Do not maintain a parallel checkpoint format.
- Preserve timestamped history when replacing a checkpoint would destroy useful evidence.
- Do not claim a saved receipt is reusable until `context-restore` validates its inputs.
