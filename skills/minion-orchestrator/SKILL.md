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

## Codex Adaptation

- Prefer Codex tool calls, shell sessions, or explicit subagents available in the current session.
- Treat upstream GBrain minions as an optional external runtime, not something bundled by this port.
- Use parallelism only for independent read-only work or isolated outputs.
- For mutating work, define ownership before starting the job.

## Guardrails

- Do not spawn unbounded background work.
- Do not lose track of running sessions.
- Do not use parallelism when jobs mutate the same files.
- Do not claim durable worker semantics unless an actual durable worker runtime is present.
