# GStack Port for Codex

Codex-native ports of the full [garrytan/gstack](https://github.com/garrytan/gstack) skill surface: a reusable migration kit for bringing high-rigor coding workflows from Claude-style slash commands into Codex skills.

This repository now covers all eight upstream gstack skills, with Codex-native adaptations for planning, review, shipping, retros, browser work, QA, and session setup.

## Why This Exists

The source idea was captured on 2026-03-14 in `/Users/praneet/.codex/worktrees/114e/PraneetIdeas/manual_ideas.json` and `/Users/praneet/.codex/worktrees/114e/PraneetIdeas/memory.md`.

- Rationale: high leverage project that ports a known coding-skills system into Codex format and re-opens it for community reuse.
- First milestone: create repo scaffold with a SKILL format map, one fully ported reference skill, and a compatibility README.
- End-of-day target: public repo with initial ported skill, usage docs, and a clear migration checklist for the remaining skills.

## Current Coverage

- `skills/plan-ceo-review/`: founder-style plan review
- `skills/plan-eng-review/`: engineering execution review
- `skills/review/`: pre-landing PR review
- `skills/ship/`: release workflow orchestration
- `skills/retro/`: engineering retrospective workflow
- `skills/browse/`: browser QA and dogfooding workflow port
- `skills/qa/`: structured QA workflow with issue taxonomy and report template
- `skills/setup-browser-cookies/`: authenticated session setup workflow
- `docs/compatibility-map.md`: upstream-to-Codex map for the full surface
- `docs/runtime-compatibility.md`: explicit notes for browser/runtime-heavy adaptations
- `data/skill-map.json`: machine-readable port registry pinned to an upstream commit
- `scripts/validate_repo.py`: repo health check for docs, registry, and ported skills
- `scripts/print_status.py`: terminal-friendly status table for the port surface
- `tests/`: regression checks for the registry and validator

## Repository Layout

```text
gstack-port-for-codex/
├── docs/
│   ├── idea-strategy.md
│   ├── product-strategy.md
│   ├── implementation-strategy.md
│   ├── mvp-plan.md
│   ├── compatibility-map.md
│   └── runtime-compatibility.md
├── data/
│   └── skill-map.json
├── skills/
│   ├── browse/
│   ├── plan-ceo-review/
│   ├── plan-eng-review/
│   ├── qa/
│   ├── retro/
│   ├── review/
│   ├── setup-browser-cookies/
│   └── ship/
├── scripts/
│   ├── print_status.py
│   └── validate_repo.py
├── src/
│   └── gstack_port_for_codex/
└── tests/
```

## Compatibility Model

gstack is built around Claude Code slash commands. Codex skills work differently, so each port needs an adaptation layer rather than a direct copy.

Core translation rules in this repo:

- Slash-command invocation becomes skill discovery by name and description.
- Claude-only tool declarations are removed or rewritten into Codex-native guidance.
- Large monolithic prompts are split into a concise `SKILL.md` plus targeted references.
- Interactive `AskUserQuestion` flows are adapted to Codex's "ask only when necessary" collaboration style.
- Update-check and install-time shell behavior stay out of the skill unless they are essential to the workflow.

Port kinds used in this repo:

- `native`: direct Codex-friendly prompt workflow with minimal behavioral translation
- `workflow-adapted`: same workflow intent, but reshaped around Codex conventions and outputs
- `runtime-aware`: workflow ported, but execution depends on whatever browser/session tooling the host Codex environment provides

## Port Highlights

The initial reference port is `plan-ceo-review`, adapted from upstream gstack commit `2aa745cb0e4331d683e727ec77385d04cdbb45a2`.

Patterns reused across the full port:

- Remove Claude-specific update checks and runtime-only tool declarations.
- Compress giant single-file prompts into Codex-friendly overview files plus references.
- Preserve the core operating modes and review posture of each upstream skill.
- Reframe interactive questioning around Codex's default behavior: ask only when ambiguity materially changes the recommendation.
- Be explicit when a workflow depends on host runtime capabilities that this repo does not reimplement.

## Using The Port

1. Review any skill under `skills/`.
2. Copy the folders you want into your Codex skills directory, or use this repo as a porting reference.
3. Use `docs/compatibility-map.md`, `docs/runtime-compatibility.md`, and `data/skill-map.json` to understand port type and parity.
4. Run the validation checks before opening a PR.

## Checks

```bash
python3 scripts/validate_repo.py
python3 scripts/print_status.py
python3 -m unittest discover -s tests
```

## Upstream Source

- Upstream repo: [garrytan/gstack](https://github.com/garrytan/gstack)
- Upstream license: MIT
- Upstream pinned commit for this port snapshot: `2aa745cb0e4331d683e727ec77385d04cdbb45a2`

Attribution details live in `NOTICE`.

## Roadmap

- Deepen runtime parity for `browse`, `qa`, and `setup-browser-cookies`.
- Add upstream-diff tooling so future gstack changes can be compared against this port.
- Add contributor automation for new skill ports and validation.
