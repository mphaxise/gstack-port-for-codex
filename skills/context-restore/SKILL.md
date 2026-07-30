---
name: context-restore
description: Restore a compact saved-work packet, validate its source map and evidence receipts against current state, and resume without broad history scans or stale assumptions.
---

# Context Restore

Restore work from the latest relevant active packet when the user asks to resume, continue, or determine where a project stands.

## Restore Narrowly

1. Read the explicit user-provided packet or the latest canonical project checkpoint.
2. Inspect current repository state:
   - repository and worktree
   - branch
   - `git status --short`
   - only the commits and paths named by the packet
3. Follow the packet's source map. Read the smallest useful files or line windows first.
4. Do not scan full task history, the whole repository, or broad memory stores unless a named source is missing and the gap blocks safe continuation.

## Revalidate

1. Compare the packet with current files, requirements, and environment.
2. Classify each saved receipt:
   - `reusable` when recorded inputs and risk surface still match
   - `invalidated` when a covered input or requirement changed
   - `unknown` when the match cannot be established
3. Trust current source and Git state over a stale packet. Report the mismatch before acting when it affects scope, authority, or safety.
4. Reconstruct only:
   - active goal and slice
   - authority and stop gates
   - accepted decisions
   - reusable evidence
   - remaining work
   - single next action

## Decide Whether To Continue

- Continue in the current task when the packet is compact, the goal is unchanged, and no reset trigger is active.
- Recommend a fresh task when the saved packet records a reset recommendation or current evidence satisfies a `context-save` reset condition.
- Do not create or hand off to a new task unless the user explicitly asks.

Before implementation, state any material stale or unknown receipt and the verification tier needed to refresh it.

## Guardrails

- Do not overwrite local changes while restoring context.
- Do not assume untracked files are disposable or session-authored.
- Do not treat a prior test, build, screenshot, or review as current when its recorded inputs no longer match.
- Do not invent missing token telemetry, hashes, acceptance, or external-state results.
