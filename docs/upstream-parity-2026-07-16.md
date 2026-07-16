# Upstream Parity Audit — 2026-07-16

## Verified Sources

- Installed Codex: `codex-cli 0.144.0`
- Official Codex manual: current via `/Users/praneet/.codex/skills/.system/openai-docs/scripts/fetch-codex-manual.mjs`
- GStack: `garrytan/gstack@a3259400a366593e0c909dd9ac3e59752efd2488`
- GBrain: `garrytan/gbrain@5008b287e47bf791132eedfebf66bdef11e9398c`

## Surface Result

- GStack upstream exposes 54 skill directories. This port maps all 54 and retains two local compatibility entries: `gstack` and `checkpoint`.
- GBrain upstream exposes 53 skill directories. This port maps all 53.
- Local installation uses symlinks from `/Users/praneet/.codex/skills/<skill>` to this checkout, so validated repo updates are immediately active locally.

## Port Decisions

The parity target is workflow parity on Codex, not byte-for-byte copying of Claude-specific prompt scaffolding. Current upstream session preambles, telemetry, update daemons, `CLAUDE.md` mutation, AskUserQuestion transport rules, bundled Playwright/browser binaries, Supabase/Postgres services, and worker/minion infrastructure are not vendored. Codex-native `AGENTS.md`, skills, plans, approvals, hooks, memories, automations, Browser, Chrome, Computer Use, connectors, and local file-backed brain helpers cover those host responsibilities.

Substantive changes ported in this audit include:

- full Autoplan coverage across CEO, engineering, design, and developer-experience reviews, with a decision audit trail
- source-aware upstream drift attribution using per-skill freshness boundaries
- expanded provenance, backlink, graph traversal, source precedence, media/meeting propagation, migration, maintenance, and test-tier guidance across GBrain workflows
- current frontmatter validation classes and optional pre-commit mode
- current PDF input, diagram, image, publication, preview, and CI expectations
- explicit protected-action and safe-exception rules in `careful`

The historical map pins remain conservative to measure broad runtime drift. `skill_parity_commit` records the current full workflow audit boundary, and explicit `source_commit` metadata can override it for future partial refreshes.

## Runtime Non-Goals

- do not vendor the upstream GStack browser daemon, telemetry, or bundled model runners
- do not bundle the upstream GBrain database, Supabase, Postgres, MCP server, live-sync daemon, or minion workers
- do not publish private generated `brain/` corpus state as package source

These are explicit adaptation boundaries, not unreported parity gaps.
