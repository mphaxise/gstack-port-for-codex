# GStack Enhancement Plan

## Snapshot

- Reviewed on `2026-05-26`.
- Local pinned upstream commit: `2aa745cb0e4331d683e727ec77385d04cdbb45a2`.
- Latest upstream GStack commit reviewed: `cf50443b63e461a7c0796857f69d572781acab8e`.
- Latest upstream GBrain commit reviewed: `32f8be96c2409b8ccd35b7835692fd56b640f5c4`.
- Current local GStack ports: `52 / 52` current upstream GStack skills are represented under current upstream names, plus the legacy `checkpoint` compatibility skill.
- Current local GBrain layer: `48 / 48` current upstream GBrain skills are represented, plus `workflow-router` and the local `brain/` helper scripts.

This plan focuses on two jobs:

1. strengthen the GStack skills that are already ported
2. use the earlier GBrain work to make the next GStack ports deeper instead of just broader

## Progress In This Branch

This branch completed the April coverage pass and now has the first May 26 refresh tranche:

- added the planning bridge skills
- added the full design and developer-experience layer
- added release, security, health, learning, and checkpoint skills
- added safety, browser, and utility skills
- added the new upstream GBrain bridge and continuity skills: `setup-gbrain`, `sync-gbrain`, `context-save`, `context-restore`, `document-generate`
- added the first GBrain memory-governance refresh: `capture`, `brain-taxonomist`, `schema-author`, `frontmatter-guard`
- added the remaining May 26 GStack skills: `benchmark-models`, `ios-clean`, `ios-design-review`, `ios-fix`, `ios-qa`, `ios-sync`, `landing-report`, `make-pdf`, `scrape`, `skillify`
- added the remaining May 26 GBrain skills, including research, enrichment, orchestration, install, smoke-test, and skillpack workflows
- added per-skill source freshness metadata in the registries
- updated `workflow-router`, `README.md`, and `docs/compatibility-map.md` to reflect the full-surface port honestly

## Skills Used To Build This Plan

### Local skills I explicitly used as planning lenses

- `workflow-router` to frame which existing repo skills actually apply
- `plan-ceo-review` to check scope and leverage
- `plan-eng-review` to check execution order, dependency shape, and testability
- `review`, `qa`, `browse`, `ship`, and `retro` to assess the current sprint loop that already exists
- `repo-architecture` to keep new artifacts in the right places
- `testing` and `maintain` to make sure the plan includes validation and drift control
- `reports`, `brain-ops`, `cross-modal-review`, and `cron-scheduler` to factor in the earlier GBrain enhancements instead of treating them as unrelated
- `skill-creator` to keep future ports concise and registry-aware

### Upstream skill families I reviewed to rebalance the plan

- product framing: `office-hours`, `autoplan`, `plan-tune`
- design planning and execution: `plan-design-review`, `design-review`, `design-consultation`, `design-shotgun`, `design-html`
- developer experience: `plan-devex-review`, `devex-review`
- debugging and quality: `investigate`, `qa-only`, `health`
- security and safety: `cso`, `careful`, `freeze`, `guard`, `unfreeze`
- release and post-deploy: `document-release`, `setup-deploy`, `land-and-deploy`, `benchmark`, `canary`
- memory and continuity: `learn`, `checkpoint`

## Full Skill Coverage Lanes

Looking at the full current and upstream skill surface, the repo needs to cover seven lanes well:

- product framing: `office-hours`, `plan-ceo-review`, `autoplan`, `plan-tune`
- engineering execution: `plan-eng-review`, `investigate`, `review`, `health`
- design quality: `plan-design-review`, `design-review`, `design-consultation`, `design-shotgun`, `design-html`
- developer experience: `plan-devex-review`, `devex-review`
- QA and browser runtime: `browse`, `setup-browser-cookies`, `qa`, `qa-only`, `open-gstack-browser`, `pair-agent`
- release and operations: `ship`, `document-release`, `setup-deploy`, `land-and-deploy`, `benchmark`, `canary`
- memory, reporting, and continuity: `learn`, `reports`, `brain-ops`, `workflow-router`, `cross-modal-review`, `cron-scheduler`, `checkpoint`

The first version of this plan was strongest in engineering execution and release. After the full skill audit, the main correction is to pull design and developer-experience review earlier in the roadmap instead of leaving them as a late add-on.

## What Is Already Working

### Current GStack ports

The repo now covers the full current upstream GStack surface. The remaining roadmap is about freshness, integration depth, and runtime parity, not missing-skill coverage.

### Prior GBrain enhancements that should shape the next phase

- `brain-ops` and `query` give us a usable memory and lookup loop.
- `ingest`, `idea-ingest`, `media-ingest`, and `meeting-ingestion` already create durable local context.
- `reports` gives us a place to persist review, QA, release, and retro artifacts.
- `cron-scheduler` creates a clean path for recurring canary, benchmark, or follow-up loops.
- `cross-modal-review` and `testing` can deepen review quality and validation.
- `workflow-router` already gives us a place to wire multi-skill orchestration such as `office-hours -> plan -> review`.

## What Changed Upstream That Matters Most In May

The latest upstream direction is GStack plus GBrain together. GStack now includes bridge skills that expect a GBrain setup and sync loop, and GBrain has grown a stronger schema, capture, and frontmatter governance layer.

The first refresh tranche has been ported locally:

- `setup-gbrain`
- `sync-gbrain`
- `context-save`
- `context-restore`
- `document-generate`
- `capture`
- `brain-taxonomist`
- `schema-author`
- `frontmatter-guard`

No current upstream GStack or GBrain skill names are missing after this refresh. The remaining work is depth: improving runtime fidelity, drift tooling, docs, and integration quality.

### Next Parity Targets

Now that coverage is complete, the next engineering work is:

- refresh the older pre-existing ports against upstream HEAD, especially `plan-ceo-review`, `plan-eng-review`, `review`, `browse`, `qa`, and `retro`
- deepen the design and DX layer so it leaves behind reusable artifacts and evidence instead of one-shot guidance
- deepen release, security, health, learning, and checkpoint workflows around the GBrain reporting and memory substrate
- improve runtime-heavy browser utilities and visible-browser flows without pretending their host support is stronger than it is

## Enhancement Roadmap

### Phase 1: Maintain latest-upstream coverage

- Keep upstream coverage checks runnable against fresh GStack and GBrain clones.
- Refresh older low-freshness ports against upstream HEAD.
- Keep per-skill freshness metadata on all changed entries.
- Preserve the local `checkpoint` compatibility skill until users fully migrate to `context-save` and `context-restore`.

Why this comes first:
The repo is now complete against the May 26 upstream skill-name surface, so the risk moves from missing coverage to future drift.

### Phase 2: Deepen the existing ports with the GBrain substrate

- Make `plan-ceo-review` and `plan-eng-review` save reusable artifacts into `reports/` or the local `brain/` corpus.
- Make `review` feed `cross-modal-review`, `testing`, or follow-up task capture when the user wants a second pass.
- Make `browse` and `qa` share one evidence path for screenshots, blind spots, and QA reports.
- Make `ship` write a structured release artifact instead of only acting as an execution checklist.
- Make `retro` write durable summaries that can be compared over time.
- Expand `setup-browser-cookies` with clearer runtime adapters and host-specific fallback guidance.

Why this matters:
The earlier GBrain work is already the best differentiator in this repo. The next step is to let the current GStack ports accumulate context instead of acting like isolated one-shot prompts.

### Phase 3: Harden the newly added planning and debugging bridge skills

The next step for the newly landed skills is not more breadth, but tighter integration:

- make `office-hours` emit or update a reusable planning artifact when the user wants one saved
- make `autoplan` consume those saved artifacts cleanly and hand off into the next review step
- make `investigate` produce durable debugging reports or follow-up tasks when the fix is deferred
- make `qa-only` and `qa` share the same evidence and reporting path

### Phase 4: Deepen the design and developer-experience layer

- make `plan-design-review` and `plan-devex-review` produce reusable planning artifacts
- make `design-review` and `devex-review` share clearer evidence and scoring paths
- connect `design-consultation`, `design-shotgun`, and `design-html` into a coherent creation pipeline instead of isolated prompts

### Phase 5: Deepen release, security, health, and memory loops

- make `document-release`, `land-and-deploy`, `setup-deploy`, `benchmark`, and `canary` produce durable reports
- make `cso`, `health`, `learn`, and `checkpoint` reuse the GBrain substrate instead of inventing parallel storage
- connect deploy verification and benchmark/canary follow-ups through `cron-scheduler` when recurring checks are useful

### Phase 6: Deepen safety, browser, and utility workflows

- tighten `careful`, `freeze`, `guard`, `unfreeze`, and `plan-tune` into clearer reusable operating modes
- improve `open-gstack-browser`, `connect-chrome`, and `pair-agent` around the actual browser/runtime capabilities available in Codex
- keep `gstack-upgrade` and `codex` useful as higher-level operator workflows rather than thin wrappers

## Recommended Order Of Execution

1. Refresh older low-freshness ports against upstream HEAD.
2. Add report and memory integration to `plan-*`, `review`, `qa`, `ship`, and `retro`.
3. Deepen the iOS cluster with XcodeBuildMCP-backed verification where available.
4. Deepen deploy, security, monitoring, and memory workflows around the GBrain substrate.
5. Tighten safety wrappers and browser utilities around real Codex runtime behavior.
6. Add an automated parity checker for future upstream drift.

## Guardrail

Do not spend the next phase chasing full parity with upstream browser packaging such as `open-gstack-browser`. The better near-term move is:

1. keep `browse`, `qa`, and `setup-browser-cookies` honest about runtime limits
2. improve their Codex-native execution paths
3. only revisit full browser-runtime parity after the core workflow is stronger

## Definition Of Done For The Next Milestone

- The May 26 upstream GStack and GBrain skill-name surfaces are fully represented locally.
- `review`, `qa`, `ship`, and `retro` produce durable artifacts through `reports/` or the local `brain/` substrate.
- the full current upstream GStack surface exists as first-class skills and is wired into routing where the intent is clear, or the remaining runtime-specific gaps are documented as deferred.
- `workflow-router` knows when to invoke the new skills.
- Repo docs clearly distinguish pinned historical parity from latest-upstream gap analysis.
