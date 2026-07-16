# Quiet Hours

Codex automations open inbox items, so treat them like user-facing notifications even when the work itself is lightweight.

## Default Rule

If the user does not specify otherwise, avoid scheduling wakeups between `10:00 PM` and `8:00 AM` in the user's local time zone.

## Practical Guidance

- choose waking-hour schedules for reminders, summaries, and review loops
- if work can happen overnight, prefer a morning summary rather than an overnight wakeup
- if the user wants a workday cadence, default to weekdays
- if travel or timezone context would materially change the schedule, ask one concise question; otherwise use the current locale

## What To Avoid

- multiple overnight nudges for low-urgency work
- "just in case" reminders outside waking hours
- schedules that require the user to mentally translate time zones
