# Automation Patterns

## Primitive Mapping

| Need | Best Codex primitive | Why |
| --- | --- | --- |
| "Check back in this conversation every 30 minutes." | thread heartbeat | stays in thread and supports sub-hour cadence |
| "Review this repo every weekday morning." | project automation on a worktree | workspace-scoped, independent of thread context, and isolated from active local changes |
| "Remind me tomorrow morning in this same chat." | thread heartbeat | context continuity matters more than workspace isolation |
| "Generate a weekly multi-repo report." | standalone automation | clean separation from the current thread |
| "Run a local memo refresh in my active checkout." | project automation in local mode | direct local files matter more than isolation; warn that it can touch active files |

## Local Vs Worktree

- Choose a worktree for Git repositories when automation may edit files, create branches, or run independently of active local work.
- Choose local mode only when the automation must read or write ignored/private files that are not available in a worktree, or when the user explicitly wants the main checkout updated.
- For ignored local files needed by worktrees, document whether `.worktreeinclude` is required rather than assuming the file will be present.
- Mention that automations inherit sandbox settings; if the run needs network, app access, or writes outside the workspace, design the prompt to report the approval blocker.

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
