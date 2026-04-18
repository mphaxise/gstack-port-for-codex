# GStack Enhancement Plan

## Snapshot

- Reviewed on `2026-04-18`.
- Local pinned upstream commit: `2aa745cb0e4331d683e727ec77385d04cdbb45a2`.
- Latest upstream commit reviewed: `4d2c8d94d00cc4f4f3d4c26316a4f939ceedc045`.
- Upstream delta since the current pin: `178` commits and `300` changed files.
- Current local GStack ports: `office-hours`, `plan-ceo-review`, `plan-eng-review`, `autoplan`, `review`, `investigate`, `ship`, `browse`, `qa`, `qa-only`, `setup-browser-cookies`, and `retro`.
- Current local GBrain layer: the full tracked GBrain surface in `data/gbrain-skill-map.json`, plus `workflow-router` and the local `brain/` helper scripts.

This plan focuses on two jobs:

1. strengthen the GStack skills that are already ported
2. use the earlier GBrain work to make the next GStack ports deeper instead of just broader

## Progress In This Branch

This branch completes the first high-leverage tranche from the plan:

- added `office-hours`
- added `autoplan`
- added `investigate`
- added `qa-only`
- added per-skill source freshness metadata in `data/skill-map.json`
- updated `workflow-router`, `README.md`, and `docs/compatibility-map.md` to reflect the broader GStack surface honestly

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

- `office-hours`
- `plan-ceo-review`
- `plan-eng-review`
- `autoplan`
- `review`
- `investigate`
- `ship`
- `browse`
- `qa`
- `qa-only`
- `setup-browser-cookies`
- `retro`

### Prior GBrain enhancements that should shape the next phase

- `brain-ops` and `query` give us a usable memory and lookup loop.
- `ingest`, `idea-ingest`, `media-ingest`, and `meeting-ingestion` already create durable local context.
- `reports` gives us a place to persist review, QA, release, and retro artifacts.
- `cron-scheduler` creates a clean path for recurring canary, benchmark, or follow-up loops.
- `cross-modal-review` and `testing` can deepen review quality and validation.
- `workflow-router` already gives us a place to wire multi-skill orchestration such as `office-hours -> plan -> review`.

## What Changed Upstream That Matters Most

### Existing local ports that drifted upstream

These are the already-ported skills that changed upstream after the local pin and should be refreshed first:

- `plan-ceo-review`
- `plan-eng-review`
- `review`
- `browse`
- `qa`
- `retro`

The biggest drift is in the runtime-heavy area:

- `browse`: `81` changed files upstream
- `review`: `9` changed files upstream
- `qa`: changed prompt and reporting surface

`ship` and `setup-browser-cookies` look comparatively more stable since the current pin.

### High-leverage missing skills

These are the missing upstream skills that most directly strengthen the current sprint loop:

- pre-implementation design and DX review: `plan-design-review`, `plan-devex-review`
- live design and DX audit: `design-review`, `devex-review`
- release and operational closure: `document-release`, `setup-deploy`, `land-and-deploy`, `benchmark`, `canary`
- security and continuity: `cso`, `health`, `learn`, `checkpoint`

### Lower-priority or host-specific follow-ons

- `careful`
- `codex`
- `design-consultation`
- `design-html`
- `design-shotgun`
- `freeze`
- `gstack-upgrade`
- `guard`
- `open-gstack-browser`
- `pair-agent`
- `plan-tune`
- `unfreeze`

## Enhancement Roadmap

### Phase 1: Re-baseline the eight existing GStack ports

- Refresh `plan-ceo-review`, `plan-eng-review`, `review`, `browse`, `qa`, and `retro` against upstream HEAD.
- Add per-skill freshness metadata or a reviewed-against note so the repo shows both the original pin and the last audited upstream commit.
- Upgrade the drift tooling so it reports:
  - changed already-ported skills
  - newly added upstream skills
  - shared-doc or runtime drift
- Tighten validation so prompt references, templates, and supporting docs are checked together.

Why this comes first:
The current repo is strongest when it is honest about where parity exists and where it does not. Tightening the ports we already have creates a better base for everything else.

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

### Phase 4: Close the missing design and developer-experience review loop

Port in this order:

- `plan-design-review`
- `plan-devex-review`
- `design-review`
- `devex-review`

Then consider:

- `design-consultation`
- `design-shotgun`
- `design-html`

Rationale:
After the full skill audit, this lane should come earlier than a pure release-ops expansion. Without it, the repo still has a strong engineering loop but an incomplete product-quality loop.

### Phase 5: Add post-merge, post-deploy, security, and memory loops

Port and integrate:

- `document-release`
- `land-and-deploy`
- `setup-deploy`
- `benchmark`
- `canary`
- `cso`
- `health`
- `learn`
- `checkpoint`

Suggested GBrain tie-ins:

- `learn` should reuse `brain-ops`, `query`, `signal-detector`, and `reports`.
- `document-release` should reuse `publish`, `citation-fixer`, and `repo-architecture`.
- `benchmark` and `canary` should reuse `reports` and `cron-scheduler`.
- `land-and-deploy` should reuse the release artifacts produced by the improved `ship` flow.
- `checkpoint` should reuse `reports` or another stable saved-artifact path instead of inventing a parallel memory layer.

### Phase 6: Treat safety wrappers, creation tools, and host-specific utilities as last-mile work

- `careful`
- `freeze`
- `guard`
- `unfreeze`
- `gstack-upgrade`
- `codex`
- `pair-agent`
- `open-gstack-browser`
- `plan-tune`

These are useful, but they should not come before the core workflow and memory improvements.

## Recommended Order Of Execution

1. Refresh the existing eight GStack ports and improve drift tracking.
2. Add report and memory integration to `plan-*`, `review`, `qa`, `ship`, and `retro`.
3. Harden `office-hours`, `autoplan`, `investigate`, and `qa-only` as a clean bridge into the planning and QA stack.
4. Port `plan-design-review` and `plan-devex-review`, then add `design-review` and `devex-review`.
5. Add deploy, security, monitoring, and memory-loop skills.
6. Backfill safety wrappers, creation tools, and host-specific utilities.

## Guardrail

Do not spend the next phase chasing full parity with upstream browser packaging such as `open-gstack-browser`. The better near-term move is:

1. keep `browse`, `qa`, and `setup-browser-cookies` honest about runtime limits
2. improve their Codex-native execution paths
3. only revisit full browser-runtime parity after the core workflow is stronger

## Definition Of Done For The Next Milestone

- The eight current GStack ports are reviewed against upstream HEAD and marked with freshness metadata.
- `review`, `qa`, `ship`, and `retro` produce durable artifacts through `reports/` or the local `brain/` substrate.
- `office-hours`, `investigate`, `qa-only`, and `autoplan` exist as first-class skills and are wired into routing.
- `workflow-router` knows when to invoke the new skills.
- Repo docs clearly distinguish pinned historical parity from latest-upstream gap analysis.
