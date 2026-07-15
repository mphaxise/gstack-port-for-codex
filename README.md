# GStack Port for Codex

**A reusable migration kit for bringing high-rigor coding workflows into Codex without overstating runtime parity.**

This repository ports the full [garrytan/gstack](https://github.com/garrytan/gstack) skill surface into Codex-native workflows for planning, review, shipping, retrospectives, browser work, QA, and session setup.

The product challenge is not simple file conversion. Claude-style slash commands and Codex skills have different invocation models, tool assumptions, and collaboration patterns. This project makes those differences explicit through compatibility classes, runtime boundaries, validation tooling, and practical adoption examples.

## Start here

For the fastest path to value, begin with one stable-core skill such as `plan-ceo-review` or `review`.

```bash
mkdir -p "$CODEX_HOME/skills"
cp -R skills/plan-ceo-review "$CODEX_HOME/skills/"
cp -R skills/review "$CODEX_HOME/skills/"
```

Then invoke the skill directly in a Codex session:

```text
/plan-ceo-review
Review our rollout plan for preview deployments before we start coding.
```

```text
Use $review on this branch and look for blocking issues.
```

Add `plan-eng-review`, `ship`, and `retro` for a fuller workflow set. Add `browse`, `qa`, and `setup-browser-cookies` only after reviewing [`docs/runtime-compatibility.md`](docs/runtime-compatibility.md).

## Current coverage

### Stable core

- `plan-ceo-review`: founder-style plan review
- `plan-eng-review`: engineering execution review
- `review`: pre-landing PR review
- `ship`: release workflow orchestration
- `retro`: engineering retrospective workflow

### Experimental runtime-aware layer

- `browse`: browser QA and dogfooding workflow port
- `qa`: structured QA workflow with issue taxonomy and report template
- `setup-browser-cookies`: authenticated-session setup workflow

## Why this exists

This project began as an experiment in translating a rigorous Claude-oriented coding workflow into reusable, Codex-native skills without pretending every capability had identical host support.

The resulting product shape is a public compatibility layer with explicit parity classes:

- **Native:** direct Codex-friendly prompt workflows with minimal behavioral translation
- **Workflow-adapted:** the same operating intent, reshaped around Codex conventions and outputs
- **Runtime-aware:** a ported workflow whose execution still depends on browser, session, or host tooling

That framing lets users adopt stable skills immediately while understanding what extra tooling the runtime-heavy skills require.

## Translation principles

- Replace slash-command assumptions with skill discovery by name and description.
- Remove or rewrite Claude-only tool declarations.
- Split large monolithic prompts into concise `SKILL.md` files plus targeted references.
- Adapt interactive questioning to Codex’s ask-only-when-necessary collaboration style.
- Keep update checks and install-time shell behavior out of the skill unless essential.
- State runtime limitations rather than implying unsupported parity.

## Repository map

- [`docs/compatibility-map.md`](docs/compatibility-map.md): upstream-to-Codex map for the full surface
- [`docs/runtime-compatibility.md`](docs/runtime-compatibility.md): browser and runtime boundaries
- [`docs/adoption-examples.md`](docs/adoption-examples.md): stable-skill and runtime-aware examples
- [`data/skill-map.json`](data/skill-map.json): machine-readable port registry pinned to an upstream commit
- [`scripts/check_upstream_drift.py`](scripts/check_upstream_drift.py): compare the pinned upstream commit against current upstream `main`
- [`scripts/validate_repo.py`](scripts/validate_repo.py): repository health checks
- [`scripts/print_status.py`](scripts/print_status.py): terminal-friendly port status
- [`tests/`](tests/): regression checks for the registry and validator

## Validation

```bash
python3 scripts/check_upstream_drift.py
python3 scripts/validate_repo.py
python3 scripts/print_status.py
python3 -m unittest discover -s tests
```

## Upstream source

- Upstream repository: [garrytan/gstack](https://github.com/garrytan/gstack)
- Upstream license: MIT
- Pinned upstream commit: `2aa745cb0e4331d683e727ec77385d04cdbb45a2`

Attribution details live in `NOTICE`.

## Roadmap

- Deepen runtime parity for `browse`, `qa`, and `setup-browser-cookies`.
- Improve upstream-drift tooling so future changes can be triaged faster.
- Add contributor automation for new skill ports and validation.