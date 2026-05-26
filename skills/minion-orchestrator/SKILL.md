---
name: minion-orchestrator
description: Coordinate background jobs, shell tasks, or subagent-style work with explicit ownership and status.
---

# Minion Orchestrator

Use this skill when the user wants durable background work, multiple independent investigations, or queued tasks.

## Workflow

1. Split work into independent jobs.
2. For each job, define:
   - goal
   - inputs
   - command or agent path
   - expected artifact
   - timeout or stop condition
3. Run jobs only with available local tooling and permissions.
4. Track status and collect outputs.
5. Merge findings into one report with unresolved gaps.

## Guardrails

- Do not spawn unbounded background work.
- Do not lose track of running sessions.
- Do not use parallelism when jobs mutate the same files.
