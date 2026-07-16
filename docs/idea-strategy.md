# Idea Strategy

## Source Context

- Title: `Gbrain Port for Codex`
- Source: `Manual backlog (user idea, captured 2026-04-16)`
- Review date: `2026-04-16`
- Priority: `9`
- Impact / Effort / Momentum: `5 / 2 / 5`
- Idea link: `https://github.com/mphaxise/gstack-port-for-codex`

## Problem Statement

The repo already ports GStack's coding workflows into Codex, but GBrain adds the broader operating-system layer: identity, recurring jobs, reporting, task management, ingestion, enrichment, maintenance, and knowledge workflows around the coding core.

If we only import isolated pieces, we lose the architecture of the whole system. The repo needs to represent the full GBrain surface and provide honest local equivalents for the runtime-heavy parts.

## Target Users

- Codex users who want both coding and operating-system workflows in one package
- maintainers who want a full upstream map instead of one-off imports
- teams standardizing agent behavior around planning, reporting, automation, and memory-adjacent work

## What Already Exists

- full GStack port with eight upstream skills already adapted
- strategy docs, registry validation, and public README structure
- full-surface GBrain registry and compatibility docs
- a local `brain/` substrate plus helper scripts

## Scope

### Current Phase

- represent the full 25-skill GBrain surface in the repo
- port every GBrain skill with the smallest honest Codex equivalent
- add compatibility and resolver docs so the whole system is legible
- keep runtime differences explicit rather than hidden

### Later

- deeper runtime-aware support for ambient capture and live event intake
- richer substrate decisions if the local file-backed brain reaches its ceiling
- stronger conformance and adoption tooling

## Architecture And Tech Choices

- keep the repo as the combined GStack + GBrain Codex package
- use `data/skill-map.json` for GStack and `data/gbrain-skill-map.json` for GBrain
- add compatibility and resolver docs rather than pretending unresolved runtime differences do not exist
- continue using Markdown skills plus lightweight Python validation and helper scripts

## Risks And Assumptions

- Assumption: the right product goal is a full-surface GBrain port, not a narrow sidecar.
- Assumption: explicit workflow adaptation is more useful than leaving valuable skills in a permanent blocked bucket.
- Risk: the repo becomes confusing unless parity and dependency boundaries stay explicit.
- Risk: some runtime-heavy GBrain semantics may still want a second architecture pass later.

## 60-90 Minute First Milestone

- map the full upstream GBrain surface
- remove the collaboration/co-production bias from the planning skill that was narrowing scope
- port the first tranche of GBrain skills
- publish compatibility and resolver docs for the full surface

## End-Of-Day Outcome

- the repo clearly targets a full GBrain port
- the full upstream surface is tracked in the registry
- a meaningful local substrate and a full-surface Codex port are in place

## Not In Scope

- shipping the entire upstream backend stack in one session
- hiding unresolved runtime differences behind false parity claims
- splitting this work into a separate repo before the unified package direction is validated
