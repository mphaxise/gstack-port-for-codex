# Intent Map

Use this table when a natural-language request could map to several skills.

| User intent | Default skill | Optional follow-on |
| --- | --- | --- |
| "Pressure-test this idea or plan" | `plan-ceo-review` | `plan-eng-review` |
| "I have an idea" or "Is this worth building?" | `office-hours` | `plan-ceo-review` |
| "Run the planning stack for me" | `autoplan` | none |
| "How should we build this?" | `plan-eng-review` | `testing` |
| "Critique the design before we build it" | `plan-design-review` | `plan-eng-review` |
| "Critique the developer experience before we build it" | `plan-devex-review` | `plan-eng-review` |
| "Why is this broken?" or "Debug this" | `investigate` | `review` |
| "Audit the live design" | `design-review` | `qa` |
| "Audit the onboarding or docs flow" | `devex-review` | `investigate` |
| "Create a design system or visual direction" | `design-consultation` | `design-shotgun` |
| "Show me several design options" | `design-shotgun` | `design-html` |
| "Turn this design into code" | `design-html` | `design-review` |
| "What do we already know about X?" | `query` | `brain-ops` |
| "Save this thought or thesis" | `signal-detector` | `enrich` |
| "Save this memo, link, or source" | `idea-ingest` | `citation-fixer` |
| "Process this meeting note or transcript" | `meeting-ingestion` | `enrich` |
| "Process this PDF, screenshot, or transcript-like artifact" | `media-ingest` | `enrich` |
| "Set up a recurring reminder or repo job" | `cron-scheduler` | none |
| "Review this branch before it lands" | `review` | `ship` |
| "Push this and open a PR" | `ship` | none |
| "Merge and verify production" | `land-and-deploy` | `canary` |
| "Update docs after shipping" | `document-release` | `publish` |
| "Test this flow in the browser" | `qa` | `browse` |
| "Test this but don't fix anything" | `qa-only` | none |
| "Run a security audit" | `cso` | `review` |
| "Run a repo or brain health pass" | `health` | `maintain` |
| "Save progress so we can resume later" | `checkpoint` | `reports` |
| "Produce or publish a report" | `reports` | `publish` |

## Selection Notes

- Prefer the first skill alone when it fully covers the request.
- Add the follow-on skill only when the task naturally moves into that second stage.
- If the user explicitly names a skill, honor that instead of overriding it with this map.
