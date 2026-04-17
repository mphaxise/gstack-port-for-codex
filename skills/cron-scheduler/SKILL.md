---
name: cron-scheduler
description: GBrain-inspired automation scheduling for Codex. Use when the user wants recurring work, a heartbeat follow-up, or help translating a cadence into a safe Codex automation.
---

# Cron Scheduler

Use this skill when the user wants recurring agent work, reminders, a recurring follow-up, or help deciding how a Codex automation should run.

This port is adapted from `garrytan/gbrain` at commit `b7e3005b5b3f1b54082f9c5990482ebf81a4a807`.

## Important Adaptation

Upstream GBrain assumes raw cron jobs, host schedulers, and held notification queues. In Codex, the closest native primitives are:

- thread heartbeats for same-thread wakeups and sub-hour follow-ups
- cron automations for standalone recurring work against one or more workspaces

Before scheduling anything, read:

- `references/automation-patterns.md`
- `references/quiet-hours.md`

## Workflow

1. Decide whether the task should stay in the current thread or run as a standalone recurring job.
2. Write a thin automation prompt:
   - describe only the durable task
   - keep schedule and workspace details out of the prompt body
   - add gating rules such as "only if new commits landed" or "skip if the report already exists"
3. Choose the cadence in the user's local time:
   - prefer waking hours unless the user explicitly wants overnight activity
   - offset multiple recurring jobs by 5-15 minutes when they would otherwise bunch up
   - prefer a morning digest or follow-up over noisy overnight wakeups
4. Create or update the automation with `automation_update`.
5. Confirm the schedule in plain language and state any assumption you made.
6. If a similar automation already exists, update or replace it instead of creating a duplicate.

## Decision Rules

- Prefer a thread heartbeat when:
  - the work depends on current thread context
  - the user asked for follow-up in this conversation
  - the cadence is below one hour
- Prefer a cron automation when:
  - the work should run independently of this thread
  - the task is workspace-oriented
  - the cadence is hourly or weekly and does not need conversational context

## Guardrails

- Do not stuff giant prompts into an automation when a short task description will do.
- Do not create duplicate automations when an update is cleaner.
- Avoid schedules that create overnight inbox churn unless the user explicitly asks for that tradeoff.
- Keep recurring tasks idempotent so repeated runs do not duplicate work.
- Use `ACTIVE` by default; only start paused if the user asks.
