---
name: context-save
description: Save a compact active-work packet with repository state, decisions, evidence receipts, token telemetry, reset signals, and exact next steps so a future Codex task can resume without rereading full history.
---

# Context Save

Create one durable active-work packet when the user asks to save progress, checkpoint work, hand off a project, or prepare a fresh task.

Upstream GStack renamed this workflow from `checkpoint`. Keep `checkpoint` as the compatibility entry and use this skill as the canonical save format.

## Capture The Active Packet

Keep the packet at or below 1,500 words after removing repetition. Include:

1. goal and current coherent slice
2. primary repository, branch, worktree, and concise Git state
3. authority, privacy, release, and stop gates
4. accepted decisions and acceptance criteria
5. exact files or artifacts changed in the current slice
6. source map: exact path or source, why it matters, and freshness
7. receipts: check or review, covered inputs, direct fingerprint or hash when available, result, and status
8. remaining work, blockers, unknowns, and the single next action
9. compact slice telemetry

Do not reconstruct a complete chronology. Preserve only information required to continue safely.

## Classify Receipts

Use one of these statuses:

- `reusable`: the covered inputs and risk surface are unchanged
- `invalidated`: a covered input, requirement, environment, or risk surface changed
- `unknown`: the evidence does not establish whether reuse is safe

Record hashes, build identifiers, token counts, and timings only when a tool or artifact reports them directly. Never invent a fingerprint.

## Record Slice Telemetry

Capture available direct evidence:

- goal token total at slice start and end
- active time
- input, cached input, output, and reasoning tokens when exposed
- context loads and compactions
- correction passes
- builds or runtime passes
- review panels
- verification tiers completed

Use `unknown` for unavailable fields. Label computed differences as estimates unless both endpoints are directly observed.

## Recommend A Fresh Task

Recommend a fresh task when any condition is directly observed. Creating that task requires an explicit user request.

- three consecutive events exceed 100,000 input tokens
- two compactions occur in the same slice
- the work enters a new risk class or authority boundary
- an accepted milestone gains a materially new outcome
- a second material correction is needed for the same slice
- the active packet remains above 1,500 words after pruning

If none applies, record `reset recommendation: no`.

## Storage

- Prefer one timestamped repo-local report or the project's canonical checkpoint.
- Use `reports` for a reviewable report.
- Use `capture` or `brain-ops` only when the user authorizes durable memory.
- Preserve older checkpoints when overwriting would destroy useful history.

## Guardrails

- Do not claim work is committed, pushed, installed, tested, or accepted unless direct evidence establishes it.
- Do not include secrets, credentials, or private content outside the authorized artifact.
- Preserve unrelated dirty work and unresolved user decisions.
