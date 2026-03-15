# Compatibility Map

Pinned upstream source: `garrytan/gstack@2aa745cb0e4331d683e727ec77385d04cdbb45a2`

This map tracks full upstream coverage, but the right way to read it is by adoption tier as well as by status.

## Adoption Tiers

- Stable core: `native` and `workflow-adapted` skills that Codex users can adopt immediately without extra browser or session runtime work
- Experimental runtime-aware layer: skills whose workflow is ported, but whose execution depth depends on the host Codex environment

`Status = ported` means the workflow has been translated into Codex form. It does not imply identical runtime parity for browser-heavy flows.

## Porting Rules

- Preserve the workflow intent and operating posture.
- Translate invocation from slash commands to Codex skill discovery.
- Remove Claude-specific update checks and runtime-only metadata.
- Favor concise `SKILL.md` files plus references over giant single-file prompts.
- Keep a machine-readable registry in sync with this table.

## Upstream To Codex Status

| Upstream gstack skill | Codex skill target | Status | Port kind | Notes |
| --- | --- | --- | --- | --- |
| `plan-ceo-review` | `plan-ceo-review` | ported | `native` | Stable-core planning skill with Codex-friendly references and questioning rules. |
| `plan-eng-review` | `plan-eng-review` | ported | `native` | Stable-core engineering review with scope-mode handling and explicit output structure. |
| `review` | `review` | ported | `workflow-adapted` | Stable-core PR review preserving two-pass analysis and optional Greptile triage. |
| `ship` | `ship` | ported | `workflow-adapted` | Stable-core release workflow with conditional versioning and changelog behavior. |
| `browse` | `browse` | ported | `runtime-aware` | Experimental runtime-aware workflow; host browser/tooling determines execution depth. |
| `qa` | `qa` | ported | `runtime-aware` | Experimental runtime-aware QA flow; runtime depends on available browser tools. |
| `setup-browser-cookies` | `setup-browser-cookies` | ported | `runtime-aware` | Experimental runtime-aware session setup with Codex-native fallback strategies. |
| `retro` | `retro` | ported | `workflow-adapted` | Stable-core retrospective workflow with history and compare guidance. |

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
