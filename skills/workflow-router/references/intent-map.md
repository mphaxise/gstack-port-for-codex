# Intent Map

Use this table when a natural-language request could map to several skills.

| User intent | Default skill | Optional follow-on |
| --- | --- | --- |
| "Pressure-test this idea or plan" | `plan-ceo-review` | `plan-eng-review` |
| "I have an idea" or "Is this worth building?" | `office-hours` | `plan-ceo-review` |
| "Run the planning stack for me" | `autoplan` | none |
| "How should we build this?" | `plan-eng-review` | `testing` |
| "Why is this broken?" or "Debug this" | `investigate` | `review` |
| "What do we already know about X?" | `query` | `brain-ops` |
| "Save this thought or thesis" | `signal-detector` | `enrich` |
| "Save this memo, link, or source" | `idea-ingest` | `citation-fixer` |
| "Process this meeting note or transcript" | `meeting-ingestion` | `enrich` |
| "Process this PDF, screenshot, or transcript-like artifact" | `media-ingest` | `enrich` |
| "Set up a recurring reminder or repo job" | `cron-scheduler` | none |
| "Review this branch before it lands" | `review` | `ship` |
| "Push this and open a PR" | `ship` | none |
| "Test this flow in the browser" | `qa` | `browse` |
| "Test this but don't fix anything" | `qa-only` | none |
| "Run a repo or brain health pass" | `maintain` | `testing` |
| "Produce or publish a report" | `reports` | `publish` |

## Selection Notes

- Prefer the first skill alone when it fully covers the request.
- Add the follow-on skill only when the task naturally moves into that second stage.
- If the user explicitly names a skill, honor that instead of overriding it with this map.
