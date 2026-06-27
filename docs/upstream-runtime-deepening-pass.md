# Upstream Runtime Deepening Pass

Date: 2026-06-26
Installed Codex checked during follow-up: `codex-cli 0.142.2`
Runtime surface follow-up: 2026-06-27 with `codex-cli 0.142.3`

This pass covers the runtime-heavy upstream areas that were intentionally left out of the first clean Codex-port refresh.

## Verdict

Do not vendor upstream runtime stacks into this repo right now.

The useful Codex-port shape is:

- keep readable Codex-native skill workflows in `skills/`
- prefer current Codex host tools when available
- use repo-local helper scripts for this package's file-backed brain
- call upstream `gbrain` or GStack browser tooling only when it is already installed and explicitly in scope
- document runtime gaps instead of claiming bundled parity

## GStack Runtime Areas

### Browser Daemon

Upstream GStack now carries a substantial browser daemon and CDP/security/runtime layer. This Codex port should not copy it wholesale.

Codex order of preference:

1. In-app Browser / `@Browser` for local dev servers, file-backed previews, and public unauthenticated pages.
2. Chrome extension / `@Chrome` for signed-in browser state, browser extensions, existing tabs, or Chrome-profile context.
3. Computer Use for desktop GUI flows that Browser/Chrome cannot cover.
4. Repo-local Playwright or app-specific browser helpers when the target repo already has scripts, fixtures, and dependencies.
5. Screenshots, HTTP checks, logs, or manual browser handoff with explicit limitations.

Changes made in this pass:

- strengthened `browse` runtime guidance
- strengthened `open-gstack-browser` headed-browser guidance
- kept `setup-browser-cookies` as a safe session strategy, not a cookie extractor implementation
- clarified Chrome/session use as a signed-in-state path, not a generic browser default
- aligned minion/pair-agent guidance with explicit Codex subagents and inherited sandbox/approval behavior

### First-Run Activation

Upstream first-run activation is useful product direction, but its shell preamble and Claude-specific activation files do not belong in this Codex port.

Codex equivalent:

- route broad requests through `gstack`
- use `workflow-router` for natural-language selection
- keep onboarding guidance in docs and skills, not hidden shell state

### Telemetry

Do not port upstream telemetry prompts or analytics writes.

Codex equivalent:

- validation commands
- explicit reports
- user-approved memory/corpus writes

## GBrain Runtime Areas

### Database And Sync Runtime

Upstream GBrain has a real database, migrations, sync, sources, and queue machinery. This repo intentionally keeps a Markdown/file-backed local brain.

Codex equivalent:

- `brain_doctor.py`
- `brain_citations.py`
- `brain_search.py`
- `brain_ingest_source.py`
- optional read-only upstream `gbrain` CLI probes when installed

### MCP

MCP-backed GBrain operations remain optional. Do not claim availability unless the tools are present in the current Codex session.

### Minions

Upstream minions are durable workers. This port keeps `minion-orchestrator` as bounded job coordination over available Codex tools, shell sessions, and explicit artifacts.

Codex subagents are a direct fit for explicitly requested parallel exploration, tests, triage, and summarization, but they are not an always-on minion runtime. They inherit the current sandbox and approval policy, and the port should avoid parallel write-heavy jobs unless file ownership is clear.

### Schema Packs

Upstream schema-pack migration is powerful but mutating. This port keeps `schema-unify` audit-first, with explicit approval before any protected upstream handler or local bulk migration.

### SkillOpt

Upstream SkillOpt is not bundled. This port keeps `skill-optimizer` benchmark-first and validation-gated, using local edits by default and external optimizers only with explicit approval.

## Clean To Publish

- adapter docs
- skill guidance that prefers current Codex tools
- ignore rules keeping local brain corpus private

## Local Only

- generated `brain/` corpus pages
- raw ingested source snapshots
- transient runtime artifacts

## Remaining Future Work

- Add a stable Codex browser smoke command if Codex exposes one.
- Add a local install-discovery command if Codex exposes one.
- Add optional adapters for upstream `gbrain doctor --json` and `gbrain advisor --json` once a real CLI is installed.
- Consider plugin packaging once the port should distribute skills together with apps, MCP server defaults, or lifecycle hooks.
- Consider `.codex` local environment actions for repeatable worktree setup when this repo needs app-level run/test buttons.
