# GBrain Adaptation Memo

## Goal

Translate the full upstream `garrytan/gbrain` surface into a practical Codex porting strategy for this repo.

## Sources Reviewed

- upstream repo: `https://github.com/garrytan/gbrain`
- source pin: `b7e3005b5b3f1b54082f9c5990482ebf81a4a807`
- `README.md`
- `INSTALL_FOR_AGENTS.md`
- `docs/GBRAIN_SKILLPACK.md`
- `skills/manifest.json`
- `skills/RESOLVER.md`
- selected upstream skill files across the operational, brain, setup, and ingestion layers

## Executive Read

GBrain is not a handful of cron rules. It is a full operating layer on top of GStack:

```text
resolver + conventions + recurring jobs + reporting + tasks + ingestion + enrichment + brain backend
```

The right Codex port target is the full surface, not a sampler pack.

## Architectural Takeaways

## 1. GStack And GBrain Are Distinct Layers

- GStack is the coding core.
- GBrain is the operating layer around memory, tasks, reporting, ingestion, and identity.

That separation is useful and should stay visible in this repo.

## 2. Full-Surface Representation Matters

The upstream GBrain package is legible because it has:

- a manifest
- a resolver
- conventions
- skills grouped by function

This repo needs equivalent artifacts, even before every skill is runtime-identical.

## 3. Local Substrate Beats Fake Parity

This repo now uses a minimal file-based `brain/` substrate rather than pretending a full backend already exists. The deeper upstream brain behaviors are adapted into explicit local workflows on top of that substrate.

## Portability Classification

## Full Surface Now Ported

- `brain-ops`
- `briefing`
- `citation-fixer`
- `cross-modal-review`
- `cron-scheduler`
- `data-research`
- `daily-task-manager`
- `daily-task-prep`
- `enrich`
- `idea-ingest`
- `ingest`
- `maintain`
- `media-ingest`
- `meeting-ingestion`
- `migrate`
- `publish`
- `query`
- `repo-architecture`
- `reports`
- `setup`
- `signal-detector`
- `skill-creator`
- `soul-audit`
- `testing`
- `webhook-transforms`

These now depend on prompts, files, automations, connectors, or the local `brain/` corpus that exists in the repo.

## Most Adapted Ports

- `brain-ops`
- `signal-detector`
- `idea-ingest`
- `media-ingest`
- `meeting-ingestion`
- `citation-fixer`
- `webhook-transforms`

These are the furthest from upstream runtime semantics. They are still honest ports, but they run as explicit Codex workflows rather than ambient infrastructure.

## Implication For This Repo

The full port strategy should be:

1. represent the entire upstream skill surface now
2. port every skill with the smallest honest local equivalent
3. add the smallest substrate where it unlocks materially better behavior
4. keep the adaptation boundaries visible in docs and registries

## What Changed In This Pass

- removed the collaboration/alignment checkpoint from `plan-ceo-review`
- replaced the narrow-slice framing with a full-surface port target
- expanded the registry and docs around the full GBrain surface
- ported the deeper brain layer as workflow-adapted Codex skills
- added a minimal local `brain/` substrate plus deterministic helper scripts for search, writing, backlinks, citation audit, ingest, meeting capture, signal capture, and event transforms
