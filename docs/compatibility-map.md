# Compatibility Map

Pinned upstream source: `garrytan/gstack@2aa745cb0e4331d683e727ec77385d04cdbb45a2`

## Porting Rules

- Preserve the workflow intent and operating posture.
- Translate invocation from slash commands to Codex skill discovery.
- Remove Claude-specific update checks and runtime-only metadata.
- Favor concise `SKILL.md` files plus references over giant single-file prompts.
- Keep a machine-readable registry in sync with this table.

## Upstream To Codex Status

| Upstream gstack skill | Codex skill target | Status | Port kind | Notes |
| --- | --- | --- | --- | --- |
| `plan-ceo-review` | `plan-ceo-review` | ported | `native` | Founder-style plan review preserved with Codex-friendly references and questioning rules. |
| `plan-eng-review` | `plan-eng-review` | ported | `native` | Engineering review ported with scope-mode handling and explicit output structure. |
| `review` | `review` | ported | `workflow-adapted` | Preserves two-pass review and optional Greptile triage in Codex-native review style. |
| `ship` | `ship` | ported | `workflow-adapted` | Preserves automated release flow while making versioning/changelog steps conditional. |
| `browse` | `browse` | ported | `runtime-aware` | Workflow ported; host browser/tooling determines execution depth. |
| `qa` | `qa` | ported | `runtime-aware` | QA modes, taxonomy, and report template ported; runtime depends on available browser tools. |
| `setup-browser-cookies` | `setup-browser-cookies` | ported | `runtime-aware` | Session-setup workflow ported with Codex-native fallback strategies. |
| `retro` | `retro` | ported | `workflow-adapted` | Team-aware retrospective workflow ported with history and compare guidance. |

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

The browser-centric workflows are fully ported as skills, but not as a bundled replacement for gstack's Playwright binary. See `docs/runtime-compatibility.md` for the exact adaptation boundary and host-tool expectations.

