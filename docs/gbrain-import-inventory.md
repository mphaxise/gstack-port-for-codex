# GBrain Import Inventory

## Full Upstream Surface

| Skill | Current status | Port kind | Notes |
| --- | --- | --- | --- |
| `ingest` | ported | workflow-adapted | Uses the local `brain/` corpus for file-backed ingestion. |
| `query` | ported | workflow-adapted | Uses deterministic search and page reads over the local `brain/` corpus. |
| `maintain` | ported | workflow-adapted | Portable as a package-health and corpus-health maintenance workflow. |
| `enrich` | ported | workflow-adapted | Uses the local `brain/` corpus for file-backed enrichment. |
| `briefing` | ported | workflow-adapted | Good Codex fit through connectors and local context. |
| `migrate` | ported | workflow-adapted | Portable as a Codex-side import and verification workflow. |
| `setup` | ported | workflow-adapted | Portable as a Codex-side package setup workflow. |
| `publish` | ported | workflow-adapted | Portable as a file-based sharing workflow. |
| `signal-detector` | ported | workflow-adapted | Rewritten from always-on sidecar capture into explicit signal capture with `scripts/brain_capture_signal.py`. |
| `brain-ops` | ported | workflow-adapted | Rewritten from ambient behavior into a deliberate brain-first lookup and write-back workflow. |
| `idea-ingest` | ported | workflow-adapted | Uses local-file ingest, raw-source preservation, and explicit entity propagation. |
| `media-ingest` | ported | workflow-adapted | Handles text-bearing media already readable by Codex and preserves the raw artifact. |
| `meeting-ingestion` | ported | workflow-adapted | Creates meeting pages and propagates attendee/company context with `scripts/brain_ingest_meeting.py`. |
| `citation-fixer` | ported | workflow-adapted | Audits and normalizes citation markup with `scripts/brain_citations.py`. |
| `repo-architecture` | ported | native | Easy fit as a repo-filing decision skill for this package. |
| `skill-creator` | ported | workflow-adapted | Strong fit for maintaining the growing skill surface. |
| `daily-task-manager` | ported | workflow-adapted | Portable via repo-local or user-chosen task files. |
| `daily-task-prep` | ported | workflow-adapted | Portable with calendar and task context. |
| `cross-modal-review` | ported | workflow-adapted | Portable as a second-pass review workflow using Codex model choice or the `review` skill. |
| `cron-scheduler` | ported | workflow-adapted | Strong fit via Codex automations. |
| `reports` | ported | workflow-adapted | Good fit via timestamped local report files. |
| `testing` | ported | native | Strong fit for registry and skill validation. |
| `soul-audit` | ported | workflow-adapted | Portable as a file-generating identity and cadence workflow. |
| `webhook-transforms` | ported | workflow-adapted | Uses offline JSON payload replay plus dead-letter handling rather than a live endpoint. |
| `data-research` | ported | workflow-adapted | Portable as a research-to-tracker workflow using files, reports, and connectors. |

## Ported In This Pass

- `brain-ops`
- `signal-detector`
- `idea-ingest`
- `media-ingest`
- `meeting-ingestion`
- `citation-fixer`
- `webhook-transforms`

## Full-Port Takeaway

The upstream GBrain surface is now fully represented and fully ported in this repo. The main distinction is no longer `ported` versus `blocked`; it is direct Codex fit versus workflow adaptation:

- direct operational or package-fit skills stay close to upstream intent
- memory-heavy and runtime-heavy skills are rewritten around local files, explicit invocation, and deterministic helper scripts
