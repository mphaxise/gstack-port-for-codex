# MVP Plan

## Phase-Two MVP Definition

The current MVP is:

- the full upstream GBrain surface represented and ported in this repo
- a minimal local substrate that makes the memory-oriented ports honest
- explicit workflow adaptations for the parts of upstream GBrain that were ambient or service-backed

## Problem Statement

Without a full-surface map, the repo feels like a side project. Without actual skill ports, it feels like paperwork. Without a minimal substrate, the memory layer would still be aspirational. The MVP has to solve all three.

## Target Users

- current adopters of the GStack Codex ports
- contributors extending the GBrain layer
- Codex users who want operational and memory-adjacent workflows around the coding core

## Scope

### MVP

- refresh strategy docs for the full-port direction
- add full-surface GBrain compatibility and resolver docs
- track all 25 upstream GBrain skills in the registry
- port the full GBrain surface with honest workflow adaptations where needed
- add the local `brain/` substrate plus helper scripts
- keep validation and tests green

### Later

- add richer background/runtime support if higher-fidelity parity becomes worth it
- deepen ingest and transformation ergonomics
- decide whether a larger substrate should replace the current local helpers

## Architecture And Tech Choices

- preserve the existing GStack port and validation
- layer the GBrain port into parallel registries and docs
- classify each upstream skill by practical Codex fit
- use the local `brain/` corpus as the smallest honest substrate before a larger backend exists

## Risks And Assumptions

- Assumption: full-surface packaging is the right product shape for this repo.
- Assumption: explicit workflow adaptation is better than leaving high-value skills marked forever blocked.
- Risk: the current local substrate may still prove too thin for some future usage.
- Risk: users may confuse workflow-adapted parity with runtime-identical parity unless the docs stay clear.

## 60-90 Minute First Milestone

- remove the collaboration checkpoint that was artificially narrowing planning
- add the full GBrain registry and compatibility docs
- port the first workflow tranche
- add the smallest honest substrate for the memory skills

## End-Of-Day Outcome

- a credible full-port foundation
- a working file-backed local brain substrate
- a full-surface GBrain port with explicit adaptation notes

## Acceptance Criteria

- `README.md` reflects the full-port direction
- `data/gbrain-skill-map.json` includes the full upstream surface
- `docs/gbrain-compatibility-map.md`, `docs/gbrain-resolver.md`, and `docs/codex-brain-substrate.md` exist
- all 25 GBrain skills are ported with real `SKILL.md` files
- validation and tests pass

## Not In Scope

- full backend/runtime identity with upstream GBrain
- pretending a live webhook server or always-on daemon exists when it does not
