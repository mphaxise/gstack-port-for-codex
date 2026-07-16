# Product Strategy

## Product Thesis

`gstack-port-for-codex` should be a unified Codex package for both upstream systems:

- GStack for coding workflows
- GBrain for operating-system and memory-adjacent workflows

The goal is not a tiny GBrain sampler. The goal is a full-surface Codex port with explicit adaptation notes and the smallest honest substrate needed to support the memory layer.

## Problem Statement

GStack covers coding rigor. GBrain covers the surrounding operating model: recurring jobs, daily briefing, task management, maintenance, ingestion, enrichment, reporting, and identity. Codex users who want the whole operating system should not have to stitch those layers together by hand.

## Target Users

- solo builders running Codex as a daily operator
- teams that want the coding and ops layers in one repo
- contributors extending the port without reverse-engineering upstream intent

## User Jobs To Be Done

- "Give me the full upstream skill surface, not just the coding core."
- "Show me how the deeper GBrain workflows map into Codex."
- "Give me a usable local substrate for the memory-oriented workflows."
- "Keep the port package coherent as new skills land."

## Scope

### Current Phase

- full-surface GBrain registry and compatibility map
- resolver-level framing for the GBrain layer
- full GBrain skill ports
- a local `brain/` substrate for the memory-oriented workflows
- validation strong enough to keep the package coherent as the surface expands

### Later

- higher-fidelity runtime support for background signal capture or live event intake
- stronger ingest ergonomics and richer conformance checks
- a larger substrate decision if the local file-backed brain stops being enough

## Architecture And Tech Choices

- one repo, two upstream sources
- one registry per upstream source
- Markdown skill ports as the primary deliverable
- explicit parity categories:
  - `ported`
  - `planned`
  - `blocked`
- a file-backed local brain before any larger backend recreation

## Risks And Assumptions

- Assumption: unified packaging is more valuable than splitting GBrain into a separate Codex repo too early.
- Assumption: a resolver and compatibility map are required once the GBrain surface is represented.
- Risk: users may over-read the local substrate as full GBrain parity unless the compatibility docs are honest.
- Risk: some higher-fidelity runtime semantics still depend on infrastructure this repo does not yet ship.

## 60-90 Minute First Milestone

- add full-surface GBrain tracking
- port the first workflow tranche
- add a minimal local substrate for the memory skills

## End-Of-Day Outcome

- a repo that reads as "GStack core plus full-surface GBrain Codex port"
- a usable local brain layer for the memory-adjacent skills
- a clear articulation of where runtime-identical parity still differs

## Not In Scope

- claiming live ambient, webhook, or daemon parity before it exists
- reducing the repo back to a GStack-only package
