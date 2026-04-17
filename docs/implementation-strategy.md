# Implementation Strategy

## Build Goal

Port the full upstream GBrain skill surface into this repo alongside the existing full GStack port, while keeping the deepest runtime differences explicit.

## Problem Statement

The implementation challenge is not just to add another skill. It is to expand the repo from a single-upstream skillpack into a two-upstream Codex package without losing clarity, and to do it without faking a background GBrain service that does not actually exist here.

## Architecture

```text
full gstack port
      +
full gbrain registry + compatibility docs + resolver doc
      +
25 Codex skill ports
      +
local file-based brain substrate
      +
explicit workflow adaptations for ambient/runtime-heavy behaviors
      =
unified Codex package with honest parity
```

## Core Components

- `data/skill-map.json`
  - GStack source registry
- `data/gbrain-skill-map.json`
  - full GBrain source registry
- `docs/gbrain-compatibility-map.md`
  - full-surface parity view
- `docs/gbrain-resolver.md`
  - Codex-facing routing view for the GBrain layer
- `docs/codex-brain-substrate.md`
  - local substrate design and helper scripts
- `brain/`
  - file-backed local corpus for the memory-oriented skills
- `skills/*`
  - actual Codex ports
- `src/gstack_port_for_codex/brain.py`
  - deterministic helpers for the local substrate
- `src/gstack_port_for_codex/registry.py`
  - validation for both upstream surfaces

## Tech Choices

- keep skill ports Markdown-first
- use JSON registries for validation and status reporting
- add deterministic helper code only where it unlocks honest applicability
- use a local file-backed substrate before considering a larger backend recreation

## Ported Now

- all 8 upstream GStack skills
- all 25 upstream GBrain skills

The main implementation distinction is not "done versus blocked." It is:

- direct Codex fit
- workflow adaptation around local files, helpers, connectors, and automations

## Most Adapted Layer

- `brain-ops`
- `signal-detector`
- `idea-ingest`
- `media-ingest`
- `meeting-ingestion`
- `citation-fixer`
- `webhook-transforms`

These are the areas where upstream ambient/runtime behavior became explicit Codex workflow.

## Risks And Assumptions

- Risk: a large surface can drift without manifest-like artifacts.
  - Mitigation: registry plus compatibility map plus resolver doc.
- Risk: users may over-read the local substrate as full backend parity.
  - Mitigation: keep the adaptation notes concrete in each skill and in the compatibility docs.
- Risk: later higher-fidelity runtime support could want different primitives.
  - Mitigation: keep the current helpers small, local, and replaceable.

## 60-90 Minute First Milestone

- broaden the registry to the full upstream GBrain surface
- add compatibility and resolver docs
- port the first workflow tranche
- add the smallest honest substrate needed to unlock the memory layer

## End-Of-Day Outcome

- a materially larger GBrain port surface
- a working local substrate for the memory-oriented skills
- a credible full-surface Codex port rather than a sampler pack

## Not In Scope

- bundling a full GBrain retrieval engine into this repo today
- recreating live inbound webhook infrastructure or an always-on daemon
