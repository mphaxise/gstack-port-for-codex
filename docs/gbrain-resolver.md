# GBrain Resolver

This is the Codex-facing resolver view for the GBrain layer in this repo. It mirrors the role of upstream `skills/RESOLVER.md`, but it routes into the current Codex ports and their local helper scripts.

## Local Brain

| Trigger | Skill |
| --- | --- |
| "what do we know about", "look up", "search the brain" | `skills/query/SKILL.md` |
| save notes, links, meetings, or observations into the brain | `skills/ingest/SKILL.md` |
| deepen an existing person, company, or concept page | `skills/enrich/SKILL.md` |
| memory-sensitive work that should check or update the brain first | `skills/brain-ops/SKILL.md` |
| capture a user's idea, thesis, or memorable phrasing | `skills/signal-detector/SKILL.md` |
| ingest a text-bearing source, article notes, or memo | `skills/idea-ingest/SKILL.md` |
| ingest PDFs, transcripts, screenshots, or repo notes already readable by Codex | `skills/media-ingest/SKILL.md` |
| turn transcript or meeting-note files into structured meeting memory | `skills/meeting-ingestion/SKILL.md` |
| audit or normalize citations in brain pages | `skills/citation-fixer/SKILL.md` |
| replay a webhook-style JSON payload into the local brain | `skills/webhook-transforms/SKILL.md` |
| trace how one idea evolved through the brain | `skills/idea-lineage/SKILL.md` |
| inspect brain setup health and next best fixes | `skills/gbrain-advisor/SKILL.md` |
| clean up or migrate page types and schema packs | `skills/schema-unify/SKILL.md` |

## Operational

| Trigger | Skill |
| --- | --- |
| "daily briefing", "morning briefing", "what's happening today" | `skills/briefing/SKILL.md` |
| "second opinion", "double check this", "cross-modal review" | `skills/cross-modal-review/SKILL.md` |
| recurring follow-up, automation, reminder cadence | `skills/cron-scheduler/SKILL.md` |
| "research", "track", "build a tracker" | `skills/data-research/SKILL.md` |
| task add/complete/defer/review | `skills/daily-task-manager/SKILL.md` |
| morning prep, "what's on my plate" | `skills/daily-task-prep/SKILL.md` |
| package health, maintenance, citation or structure audit | `skills/maintain/SKILL.md` |
| migrate from another note or wiki system | `skills/migrate/SKILL.md` |
| share a report or memo outside the repo | `skills/publish/SKILL.md` |
| save or load recurring reports | `skills/reports/SKILL.md` |
| set up the package or define its substrate expectations | `skills/setup/SKILL.md` |
| identity, cadence, or operating-profile setup | `skills/soul-audit/SKILL.md` |
| update or verify the upstream gbrain CLI | `skills/gbrain-upgrade/SKILL.md` |

## Meta

| Trigger | Skill |
| --- | --- |
| create a new GBrain-style skill | `skills/skill-creator/SKILL.md` |
| tune a skill against benchmarks or examples | `skills/skill-optimizer/SKILL.md` |
| validate the skill surface | `skills/testing/SKILL.md` |
| where new files or future ports should live | `skills/repo-architecture/SKILL.md` |
