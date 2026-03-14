# Implementation Strategy

## Build Goal

Stand up a maintainable public repository that can absorb additional gstack skill ports without turning into a pile of one-off prompt files.

## Problem Statement

A direct copy of gstack into Codex would carry over too much agent-specific behavior. The implementation needs to preserve the useful workflow intent while translating the mechanics into Codex-native skills and keeping the resulting repo easy to extend.

## Architecture

```text
          upstream gstack repo
                   |
                   v
        docs/compatibility-map.md
                   +
            data/skill-map.json
                   |
                   v
       skills/<codex-skill>/SKILL.md
                   +
             skills/.../references
                   |
                   v
      scripts/validate_repo.py + tests/
```

## Core Components

- `docs/`: product, strategy, and migration context
- `data/skill-map.json`: single source of truth for upstream skill status
- `skills/`: the actual Codex ports
- `src/gstack_port_for_codex/`: reusable validation and reporting logic
- `scripts/`: small CLIs for validation and status output
- `tests/`: regression coverage for the registry and validator

## Tech Choices

- Python stdlib only: fast to run, no bootstrapping friction
- JSON registry: easy to diff, test, and consume from scripts
- Markdown skills with progressive disclosure: keep `SKILL.md` concise and push details into references

## Porting Rules

- Keep upstream intent, not upstream ceremony.
- Remove Claude-only runtime glue such as update checks and tool declarations.
- Preserve naming where it helps contributors correlate upstream and ported skills.
- Document every non-trivial behavioral change in the compatibility map.

## Risks And Assumptions

- Browser-dependent workflows may need Codex-specific tooling before they can be ported honestly.
- Some upstream skills are intentionally huge; their Codex ports should be compressed without losing the operating posture.
- The first port must feel representative enough to guide later contributors.

## 60-90 Minute First Milestone

1. Initialize the repo and write the strategy documents.
2. Publish the upstream-to-Codex map as both Markdown and JSON.
3. Port `plan-ceo-review` into a concise Codex skill with supporting references.
4. Add validation and tests.

## End-Of-Day Outcome

The repo should be ready for public push, with one real skill, one clear migration system, and a small amount of code that keeps future contributions honest.

