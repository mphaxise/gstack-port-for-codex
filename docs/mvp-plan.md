# MVP Plan

## Public V0 Definition

The first public version is complete when the repo proves the compatibility model end to end:

- the idea and product intent are documented
- the upstream surface area is mapped
- all eight upstream skills are represented in Codex form
- stable-core and runtime-aware boundaries are explicit
- checks verify the structure
- usage examples prove how adoption should work in practice

## What Already Shipped

- Full compatibility inventory in Markdown and JSON
- Eight ported skills across `native`, `workflow-adapted`, and `runtime-aware` classes
- Runtime compatibility notes for browser-heavy workflows
- Structural validation and regression tests

## Public V0 Milestone

### Step 1: Clarify Positioning

- Recast the repo as a compatibility layer rather than a claim of identical runtime parity
- Split the top-level story into stable core versus runtime-aware ports
- Make adoption guidance visible in `README.md`

### Step 2: Add Proof

- Add one stable-core usage example
- Add one runtime-aware usage example with explicit blind spots
- Keep the examples short enough that a new adopter can copy the workflow without reading the whole repo

### Step 3: Preserve Integrity

- Keep the registry, compatibility docs, and README aligned
- Run validation and tests before publishing updates
- Avoid adding more breadth until the adoption story is crisp

## Acceptance Criteria

- `README.md` clearly distinguishes immediate-adoption skills from host-dependent skills
- `docs/product-strategy.md` and `docs/mvp-plan.md` match the repo's current shipped state
- At least one stable-core example and one runtime-aware example exist
- The compatibility map, runtime notes, and examples tell the same story
- `python3 scripts/validate_repo.py` passes
- `python3 scripts/print_status.py` passes
- `python3 -m unittest discover -s tests` passes

## Scope: Public V0 Vs Later

### Public V0

- Full compatibility inventory
- All current ports published with explicit parity classes
- Lightweight validation
- Public-ready docs and examples

### Later

- Concrete runtime adapters or shims for browser-heavy skills
- Import helpers
- CI workflow
- Upstream diffing and parity tracking

## Risks And Assumptions

- Assumption: explicit scope boundaries are more valuable than claiming seamless parity.
- Risk: contributor expectations may drift unless the registry and docs stay aligned.
- Risk: runtime-aware skills may be adopted incorrectly if examples do not show honest fallback behavior.
- Risk: browser tooling ports will require separate design work.

## Near-Term Outcome

The repo can be published as a credible compatibility layer for Codex users: useful immediately for the stable core, honest about runtime dependencies, and ready for incremental parity work rather than a big-bang rewrite.
