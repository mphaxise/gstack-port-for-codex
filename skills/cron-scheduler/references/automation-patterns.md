# Automation Patterns

## Primitive Mapping

| Need | Best Codex primitive | Why |
| --- | --- | --- |
| "Check back in this conversation every 30 minutes." | thread heartbeat | stays in thread and supports sub-hour cadence |
| "Review this repo every weekday morning." | cron automation | workspace-scoped and independent of thread context |
| "Remind me tomorrow morning in this same chat." | thread heartbeat | context continuity matters more than workspace isolation |
| "Generate a weekly multi-repo report." | cron automation | clean separation from the current thread |

## Thin Prompt Rules

- keep the prompt focused on the task, not the schedule
- include the output expectation if it matters
- include skip rules when repeated runs should no-op
- reference an existing skill or workflow when that keeps the prompt shorter and clearer

## Staggering Rules

- avoid stacking several recurring jobs on the same minute when a 5-15 minute offset will do
- if multiple jobs support one workflow, schedule the prerequisite first
- prefer weekday schedules for work-shaped tasks unless the user says otherwise

## Good Prompt Shape

```text
Run the weekly repo health check. Only report issues that are new since the last run.
```

## Bad Prompt Shape

```text
Every Monday at 9 AM in this workspace, go to this repo, remember the previous schedule, explain the timing again, and then maybe run several different checks whether or not the results already exist.
```
