# GBrain Compatibility Map

## Summary

This file is the parity map for the GBrain surface ported into this repo. The conservative baseline source pin is `b7e3005b5b3f1b54082f9c5990482ebf81a4a807`; the latest checked upstream commit is `814258dda67945ffec9457a1e73980e947b7e462`.

## Port Kinds

- `native`: direct Codex fit with only prompt-level adaptation
- `workflow-adapted`: same intent, but rewritten around Codex files, connectors, automations, and the local `brain/` corpus
- `runtime-aware`: reserved for future cases that still need runtime or storage infrastructure this repo does not ship

## Status Table

| Upstream skill | Status | Port kind | Current Codex stance |
| --- | --- | --- | --- |
| `briefing` | ported | workflow-adapted | Uses connectors, local files, and explicit source handling. |
| `brain-ops` | ported | workflow-adapted | Rewritten as a deliberate brain-first operating workflow over the local corpus. |
| `citation-fixer` | ported | workflow-adapted | Uses deterministic citation audit and normalization helpers. |
| `cross-modal-review` | ported | workflow-adapted | Uses Codex review patterns or a second-pass model choice rather than an upstream routing chain. |
| `cron-scheduler` | ported | workflow-adapted | Uses Codex automations instead of raw cron. |
| `data-research` | ported | workflow-adapted | Uses files, reports, connectors, and explicit tracker outputs instead of brain pages. |
| `daily-task-manager` | ported | workflow-adapted | Uses repo-local or user-selected task files. |
| `daily-task-prep` | ported | workflow-adapted | Uses calendar plus task context. |
| `enrich` | ported | workflow-adapted | Uses the local `brain/` corpus for file-backed page enrichment. |
| `gbrain-advisor` | ported | workflow-adapted | Runs repo-local health checks first, then optional upstream CLI advisor checks when available. |
| `gbrain-upgrade` | ported | workflow-adapted | Hardcoded, approval-gated upstream CLI upgrade flow with local validation. |
| `idea-lineage` | ported | workflow-adapted | Traces one idea through local Markdown brain pages with cited evidence and gaps. |
| `idea-ingest` | ported | workflow-adapted | Uses local-file ingest, raw preservation, and explicit entity updates. |
| `ingest` | ported | workflow-adapted | Uses the local `brain/` corpus for file-backed ingestion. |
| `maintain` | ported | workflow-adapted | Uses repo/package checks, report files, and targeted audits instead of gbrain health APIs. |
| `media-ingest` | ported | workflow-adapted | Handles text-bearing media already accessible to Codex. |
| `meeting-ingestion` | ported | workflow-adapted | Builds meeting pages plus attendee and company propagation from local files. |
| `migrate` | ported | workflow-adapted | Uses sample-first import and verification into Codex-side files or a future substrate. |
| `publish` | ported | workflow-adapted | Uses file-based publishing and sharing conventions instead of `gbrain publish`. |
| `query` | ported | workflow-adapted | Uses deterministic search and page reads over the local `brain/` corpus. |
| `repo-architecture` | ported | native | Advises where new GBrain-port files belong in this repo. |
| `reports` | ported | workflow-adapted | Uses timestamped report files. |
| `schema-unify` | ported | workflow-adapted | Plans schema/type consolidation with dry-run inventory before any migration. |
| `setup` | ported | workflow-adapted | Sets up the Codex package direction, registries, and local substrate expectations. |
| `signal-detector` | ported | workflow-adapted | Rewritten as explicit signal capture instead of an always-on sidecar. |
| `skill-creator` | ported | workflow-adapted | Maintains skill quality and registry updates. |
| `skill-optimizer` | ported | workflow-adapted | Uses benchmark-first local validation instead of automatic external optimizer mutation. |
| `soul-audit` | ported | workflow-adapted | Writes identity and cadence files locally rather than into a brain repo. |
| `testing` | ported | native | Validates the growing skill surface. |
| `webhook-transforms` | ported | workflow-adapted | Uses offline event replay and dead-letter handling instead of a live webhook service. |

## Takeaway

The GBrain workflow surface represented here is ported into this repo. The main compatibility boundary is semantic rather than binary: upstream ambient/runtime behavior becomes explicit Codex workflow when that is the smallest honest equivalent. Upstream database, MCP, minion, schema-pack, and optimizer runtimes remain optional integrations rather than bundled guarantees.
