# Compatibility Map

Baseline upstream source: `garrytan/gstack@2aa745cb0e4331d683e727ec77385d04cdbb45a2`

Latest checked upstream source: `garrytan/gstack@a3259400a366593e0c909dd9ac3e59752efd2488`

The July 16 audit records full skill-workflow parity through `skill_parity_commit`; explicit per-skill `source_commit` values override that boundary when needed.

This map tracks full upstream coverage, but the right way to read it is by adoption tier as well as by status.

## Adoption Tiers

- Stable core: `native` and `workflow-adapted` skills that Codex users can adopt immediately without extra browser or session runtime work
- Experimental runtime-aware layer: skills whose workflow is ported, but whose execution depth depends on the host Codex environment

`Status = ported` means the workflow has been translated into Codex form. It does not imply identical runtime parity for browser-heavy flows.

## Porting Rules

- Preserve the workflow intent and operating posture.
- Translate invocation from slash commands to Codex skill discovery.
- Remove Claude-specific update checks, telemetry, plan-mode shell preambles, and runtime-only metadata.
- Favor concise `SKILL.md` files plus references over giant single-file prompts.
- Keep a machine-readable registry in sync with this table.

## Upstream To Codex Status

`data/skill-map.json` is the machine-readable registry for the current Codex port surface: all 54 current upstream skills plus the local `gstack` router and `checkpoint` compatibility entry.

### Stable Core

- Routing and planning: `gstack`, `office-hours`, `spec`, `plan-ceo-review`, `plan-eng-review`, `plan-design-review`, `plan-devex-review`, `autoplan`, `plan-tune`
- Review and execution: `review`, `investigate`, `ship`, `document-release`, `setup-deploy`, `land-and-deploy`, `health`, `retro`
- Security and continuity: `cso`, `learn`, `checkpoint`, `codex`, `careful`, `freeze`, `guard`, `unfreeze`, `gstack-upgrade`
- Design creation and direction: `design-consultation`, `design-shotgun`, `design-html`, `diagram`

### Runtime-Aware Layer

- Browser and QA: `browse`, `qa`, `qa-only`, `setup-browser-cookies`, `benchmark`, `canary`, `design-review`, `devex-review`
- Browser utilities and coordination: `open-gstack-browser`, `connect-chrome`, `pair-agent`

### Reading The Registry

- `status = ported` means the workflow is represented in Codex form.
- `port_kind = runtime-aware` means the workflow depends on host browser, deploy, or runtime capabilities for full depth.
- `source_commit` on a skill means that skill was ported or refreshed against a newer upstream commit than the baseline pin.

## Adaptation Notes

### Invocation

- Upstream: user enters `/plan-ceo-review`
- Codex: user names the skill, or the repo `AGENTS.md` directs Codex to use it when the request matches

### Questioning

- Upstream: heavily interactive `AskUserQuestion` flow
- Codex: make reasonable assumptions by default; ask one concise question only when ambiguity materially changes the recommendation

### Structure

- Upstream: very large single-file `SKILL.md`
- Codex port: concise `SKILL.md` with references for mode behavior and output structure

### Tooling

- Upstream: declares Claude-specific tools and update checks
- Codex port: omits runtime-only tool declarations and keeps the skill focused on workflow guidance

### Runtime-Heavy Skills

The browser-centric workflows are fully ported as skills, but not as a bundled replacement for gstack's Playwright binary. Treat them as the experimental runtime-aware layer and see `docs/runtime-compatibility.md` plus `docs/adoption-examples.md` for the exact adaptation boundary and host-tool expectations.
