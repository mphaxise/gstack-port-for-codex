# November 17 upstream review

The Codex port adds four workflows and updates both upgrade skills. Each adopted workflow has its own source pin. The August review remains the baseline for other skills.

| Source snapshot | Entry points compared with the August map | Result |
| --- | --- | --- |
| [GStack 1.100.0.0](https://github.com/garrytan/gstack/tree/76535826f5d50c721f95820f300037a3efe833a9) | Root SKILL.md and one-level skill directories | 53 mapped files changed, 10 paths appeared, and the investigate path disappeared. |
| [GBrain 0.60.737.0](https://github.com/garrytan/gbrain/tree/a64fb58b9d407f4ee412249dbf4660b158f55f31) | Direct children of skills/ containing SKILL.md | 52 mapped files changed, 24 paths appeared, and the install path disappeared. |

The counts compare Git trees at the linked revisions with the source paths in the August reconciliation. Multiple port entries can share one upstream path. Nested host packages, generated documentation, scripts, and database features fall outside these entry-point counts. A changed file can include generated preamble changes.

For large comparisons the drift checker now reads the Git trees on both sides.
GitHub's compare response caps its file list at 300. A truncated tree yields
an incomplete check. [GitHub comparison limits](https://docs.github.com/en/rest/commits/commits#compare-two-commits)

## Adopted changes

- **GStack** adds `eval-plan` for preregistered comparisons and `design-motion` for checking a looping animation against an approved frame. The upgrade workflow distinguishes the configured release channel from the source head. The router now directs routine debugging to a focused cause check and regression test. The explicit local `investigate` entry remains available for existing callers. [GStack change log](https://github.com/garrytan/gstack/blob/76535826f5d50c721f95820f300037a3efe833a9/CHANGELOG.md)
- **GBrain** adds `fact-check` for claim-level verification and `resolve-before-asking` for ambiguous identities. The upgrade workflow checks queue state, restart eligibility and build skew for a running service. The local `install` entry continues to install this port. [GBrain upgrade workflow](https://github.com/garrytan/gbrain/blob/a64fb58b9d407f4ee412249dbf4660b158f55f31/skills/gbrain-upgrade/SKILL.md)

## Other new entry points

| Area | Source names | Port decision |
| --- | --- | --- |
| Engineering checks | deslop-shared-libs, modernize, test-audit, verify | Keep existing review, testing, and milestone commands. These four specialized workflows await an individual adaptation. |
| Agent operations and infrastructure | captain, runaway-stopper, ubicloud | Keep upstream. They depend on a particular supervisory or infrastructure environment. |
| Skill authoring | write-skill | Keep the existing skill-creator entry. |
| Ingestion and editing | blog-ingest, brain-ingest-gate, brain-link-discipline, bulk-ingestion, citation-graph-ingest, correction-pipeline, draft-in-voice, research-compendium, two-tier-extraction | Keep the file-backed capture and citation workflows. Schema-specific writes, bulk ingestion, and personal voice capture need their own acceptance cases. |
| Account and organization workflows | chat-connectors, company-brainify, conversation-archive, google-loops | Keep optional. These routes involve new data sources, account access, or recurring ingestion. |
| Brain operations | context-audit, data-loss-gate, db-repair, mcp-access, postgres-adopt, remote-mcp, storage-manifest | Keep upstream for operators of the matching runtime. The local file-backed workflow has no database migration or remote administration step. |
| Evaluation | measure-before-you-fix, skill-autobench | The port adds eval-plan. These additional measurement protocols await individual review. |

## Native Codex support

GStack now has an experimental Codex host adapter, installed upstream with `./setup --host codex`. Its adapter generates Codex metadata and uses advisory safety hooks. Its smaller model-specific instruction set was measured for Opus 5.5. An unknown model receives the full set. Keep the port's project rules and verify a new model on representative tasks before shortening its prompt. [Host adapter](https://github.com/garrytan/gstack/blob/76535826f5d50c721f95820f300037a3efe833a9/hosts/codex.ts) · [Model loadouts](https://github.com/garrytan/gstack/blob/76535826f5d50c721f95820f300037a3efe833a9/docs/loadouts.md)

GBrain provides a Codex plugin and MCP setup. Its dry run previews local registration and hooks. Hosted storage, local database setup, transcript capture and provider access each have distinct effects. The file-backed port can run independently. [Codex integration](https://github.com/garrytan/gbrain/blob/a64fb58b9d407f4ee412249dbf4660b158f55f31/docs/mcp/CODEX.md)

The Codex manual was refreshed on November 17. The shell CLI reported 0.144.0 and the desktop-bundled CLI reported 0.169.0-alpha.11.1. Check the executable a task actually launches. Install named port skills into a discovery root and verify the resolved definition in a fresh host session. [Codex manual](https://developers.openai.com/codex/codex-manual.md)
