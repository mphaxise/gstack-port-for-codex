# Runtime Compatibility

This repository ports the full gstack skill surface, but the browser-heavy workflows need a different kind of parity than the prompt-only skills.

These skills make up the experimental runtime-aware layer of the repo. Adopt the stable core first if you want immediate value with minimal setup.

## Problem Statement

Upstream gstack includes a custom `browse` runtime, browser-cookie decryption flow, and QA workflows built around that persistent Playwright session. Codex skills are portable instructions, not a bundled browser runtime by default. That means the workflow can be ported cleanly even when the exact executable cannot.

The important product distinction is:

- Stable core skills are ready for immediate adoption because they do not require bundled browser or session infrastructure.
- Runtime-aware skills are still useful, but their real-world depth depends on what the host Codex environment can do.

## Port Types

| Skill | Port type | What is included | What depends on host tooling |
| --- | --- | --- | --- |
| `browse` | `runtime-aware` | Workflow, command intent, evidence standards, Codex Browser/Chrome/Computer Use fallback strategy | Browser plugin availability, Chrome extension setup, Developer mode approval, repo-local browser tooling |
| `qa` | `runtime-aware` | Modes, issue taxonomy, report template, branch-scoped QA flow | Browser execution, screenshot capture, local app interaction |
| `setup-browser-cookies` | `runtime-aware` | Auth/session decision flow, safety notes, verification rules | Chrome extension setup, user login/test-user access, app session seeding, exceptional cookie import |
| `gstack` | `workflow-adapted` | Root skill router, Codex-native dispatch guidance | Upstream Claude shell preamble, telemetry, and first-run activation are intentionally omitted |
| `diagram` | `workflow-adapted` | Diagram workflow and editable-source guidance | Upstream bundled Excalidraw/rendering helpers are optional, not assumed |
| `spec` | `workflow-adapted` | Issue/spec workflow and acceptance-criteria structure | Upstream spawned Claude Code agent/worktree behavior requires explicit user request |
| `gbrain-advisor` | `workflow-adapted` | Local brain health checkup and optional CLI probes | Upstream advisor CLI/MCP is optional |
| `schema-unify` | `workflow-adapted` | Read-only taxonomy inventory and migration plan | Upstream protected database migration handlers require explicit local approval |
| `skill-optimizer` | `workflow-adapted` | Benchmark-first skill tuning workflow | Upstream SkillOpt runtime/model costs are optional and require approval |

## Adoption Guidance

- Adopt `plan-ceo-review`, `plan-eng-review`, `review`, `ship`, and `retro` first if your goal is immediate reuse.
- Add `browse`, `qa`, and `setup-browser-cookies` when your Codex environment already exposes browser or session tooling, or when explicit blind spots are acceptable.
- Use `docs/adoption-examples.md` to see the expected difference between stable and runtime-aware usage.

## Codex Adaptation Strategy

When porting a runtime-heavy gstack skill into Codex, use this execution order:

1. Prefer Codex in-app Browser / `@Browser` for local dev servers, file-backed previews, and public unauthenticated pages.
2. Prefer Codex Chrome / `@Chrome` when signed-in browser state, extensions, existing tabs, or Chrome-profile context matter.
3. Prefer Computer Use for desktop GUI flows that Browser/Chrome or structured integrations cannot cover.
4. Prefer repo-local Playwright, Cypress, or app-specific browser helpers only when the target repo already owns the scripts, fixtures, and dependencies.
5. Fall back to screenshots, HTTP checks, and explicit limitations when full automation is not available.
6. Never pretend full parity exists when the runtime is missing.

## What Counts As "Ported" Here

These skills are considered ported because:

- the operating workflow is preserved
- the expected outputs are preserved
- the decision points and evidence standards are preserved
- the runtime dependency boundary is documented instead of hidden

In other words, `ported` here means workflow parity with explicit runtime boundaries, not a guarantee that every Codex environment can execute the full browser path.

## Follow-On Work

- Add example integrations for Browser, Chrome, Computer Use, and repo-local Playwright/Cypress paths.
- Add adapter scripts for app-supported session seeding when the target repo supports them safely.
- Add a dedicated install smoke command if Codex exposes a stable local skill-discovery CLI.

See `docs/upstream-runtime-deepening-pass.md` for the June 26 decision not to vendor upstream daemons, databases, telemetry, or worker runtimes into this runtime-decoupled Codex port.
