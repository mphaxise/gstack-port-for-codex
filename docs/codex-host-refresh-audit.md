# Codex Host Refresh Audit

Date: 2026-06-26

This audit covers the June 26 refresh against current upstream GStack and GBrain plus the local Codex install. The goal is to preserve upstream workflow intent while removing Claude Code assumptions that no longer belong in this Codex port.

## What Changed

- Added the upstream GStack root router as `gstack`, adapted to Codex skill dispatch instead of Claude shell preambles.
- Added GStack `diagram` and `spec` as Codex-native workflow ports.
- Added GBrain `gbrain-advisor`, `gbrain-upgrade`, `idea-lineage`, `schema-unify`, and `skill-optimizer`.
- Added latest upstream commit metadata to the registries without moving the conservative baseline pins used by drift checks.

## Fallbacks Removed From New Ports

These upstream assumptions are intentionally not copied into the new Codex ports:

- `~/.claude/skills/gstack` path probing
- Claude-specific plan-mode environment checks such as `CLAUDE_PLAN_FILE`
- Claude `AskUserQuestion` stop-point mechanics
- upstream telemetry prompts and `~/.gstack/analytics` writes
- first-run activation shell preambles
- automatic spawned Claude Code agent/worktree behavior

Codex already has explicit tool calls, skill routing, and local workspace context. The port should use those directly.

## Fallbacks Still Worth Keeping

- Browser/runtime fallbacks for `browse`, `qa`, and visual review remain necessary because Codex environments vary in browser tool availability.
- Upstream `gbrain` CLI fallbacks remain necessary because this repo's file-backed `brain/` substrate is useful even when the CLI is absent.
- Explicit approval gates remain necessary for upgrades, schema migrations, issue creation, remote mutation, and any command that writes outside the repo.
- Citation debt reporting remains necessary because `brain_doctor.py` can pass while `brain_citations.py --verbose` still finds source gaps.

## Publishability

Clean to publish:

- new Codex-native skill files
- registry metadata for newly ported upstream workflows
- README and compatibility documentation
- validation and drift-check improvements

Keep local-only unless explicitly promoted:

- generated `brain/` corpus pages under untracked `brain/.raw`, `brain/concepts`, `brain/ideas`, `brain/people`, and `brain/sources`
- transient `.tmp/` files

Needs another pass before claiming full parity:

- upstream GStack browser daemon, first-run activation scripts, telemetry, and Claude TUI skill-discovery harnesses
- upstream GBrain database-backed sync, minions, schema-pack migration machinery, and SkillOpt runtime
- any MCP-backed GBrain operations that require a live upstream service or credentials

## Deeper Runtime Pass

The follow-up runtime pass is recorded in `docs/upstream-runtime-deepening-pass.md`.

Result: the port should not vendor upstream runtime stacks wholesale. Browser, GBrain database, MCP, minion, schema-pack, and SkillOpt runtimes stay optional integrations. The publishable work is stronger adapter guidance, explicit approval gates, private-corpus ignores, and validation.
