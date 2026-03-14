# GStack Port for Codex

Codex-native ports of [garrytan/gstack](https://github.com/garrytan/gstack): a reusable migration kit for bringing high-rigor coding workflows from Claude-style slash commands into Codex skills.

This repo starts with one fully ported reference skill, a compatibility map for the rest of the upstream surface area, and lightweight validation so future ports stay consistent.

## Why This Exists

The source idea was captured on 2026-03-14 in `/Users/praneet/.codex/worktrees/114e/PraneetIdeas/manual_ideas.json` and `/Users/praneet/.codex/worktrees/114e/PraneetIdeas/memory.md`.

- Rationale: high leverage project that ports a known coding-skills system into Codex format and re-opens it for community reuse.
- First milestone: create repo scaffold with a SKILL format map, one fully ported reference skill, and a compatibility README.
- End-of-day target: public repo with initial ported skill, usage docs, and a clear migration checklist for the remaining skills.

## Current MVP

- `skills/plan-ceo-review/`: first Codex-native reference port
- `docs/compatibility-map.md`: upstream-to-Codex mapping for all eight gstack skills
- `data/skill-map.json`: machine-readable port registry pinned to an upstream commit
- `scripts/validate_repo.py`: repo health check for docs, registry, and ported skills
- `scripts/print_status.py`: terminal-friendly status table for the port backlog
- `tests/`: minimal regression checks for the registry and validator

## Repository Layout

```text
gstack-port-for-codex/
├── docs/
│   ├── idea-strategy.md
│   ├── product-strategy.md
│   ├── implementation-strategy.md
│   ├── mvp-plan.md
│   └── compatibility-map.md
├── data/
│   └── skill-map.json
├── skills/
│   └── plan-ceo-review/
│       ├── SKILL.md
│       └── references/
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

## Reference Port

The first port is `plan-ceo-review`, adapted from upstream gstack commit `2aa745cb0e4331d683e727ec77385d04cdbb45a2`.

What changed in the port:

- Removed Claude-specific update checks and tool declarations.
- Compressed the giant single-file skill into a Codex-friendly overview plus references.
- Preserved the three review modes: `SCOPE EXPANSION`, `HOLD SCOPE`, and `SCOPE REDUCTION`.
- Reframed user questioning around Codex's default behavior: ask only when ambiguity materially changes the recommendation.
- Kept the emphasis on problem framing, leverage, risks, and explicit "not in scope" decisions.

## Using The Port

1. Review the skill in `skills/plan-ceo-review/`.
2. Copy that folder into your Codex skills directory if you want to use it directly.
3. Use `docs/compatibility-map.md` and `data/skill-map.json` to plan the next ports.
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
- Upstream pinned commit for this MVP: `2aa745cb0e4331d683e727ec77385d04cdbb45a2`

Attribution details live in `NOTICE`.

## Roadmap

- Port `plan-eng-review` next so strategy and execution review can work as a pair.
- Decide the Codex-native equivalent for browser-heavy workflows like `browse` and `setup-browser-cookies`.
- Add a small import helper once two or more skills are ported and the shape is stable.

