---
name: careful
description: Destructive-action guardrail for Codex. Use when the user wants extra caution around risky commands, production work, or irreversible changes.
---

# Careful

Use this skill when the work touches destructive commands, production systems, or changes that are hard to undo.

This port is adapted from `garrytan/gstack` at commit `4d2c8d94d00cc4f4f3d4c26316a4f939ceedc045`.

## Workflow

1. Identify the risky action before taking it.
2. State the specific risk plainly.
3. Prefer a safer alternative when one exists.
4. If the destructive action is still the right move, make the minimum necessary change and verify the result immediately.

## Guardrails

- Never treat destructive commands as routine.
- Prefer reversible operations over irreversible ones.
- Be especially cautious around production, shared branches, and data deletion.
