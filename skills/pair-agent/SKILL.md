---
name: pair-agent
description: Multi-agent collaboration workflow for Codex. Use when another agent or tool should work alongside the current session on a clearly defined subtask.
---

# Pair Agent

Use this skill when the task benefits from a paired agent, shared browser work, or a clearly scoped collaboration path.

This port is adapted from `garrytan/gstack` at commit `4d2c8d94d00cc4f4f3d4c26316a4f939ceedc045`.

## Workflow

1. Define the subtask and ownership boundary clearly.
2. Share only the context needed for that subtask.
3. Keep browser or runtime coordination explicit when external tools are involved.
4. Merge the result back into the main workflow cleanly.

## Guardrails

- Do not split work without a clear ownership boundary.
- Be explicit about what environment or browser access is actually available.
- Prefer collaboration that reduces ambiguity instead of creating parallel confusion.
