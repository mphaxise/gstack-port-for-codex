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
| `browse` | `runtime-aware` | Workflow, command intent, evidence standards, fallback strategy | Actual browser automation, DOM interaction, persistent session implementation |
| `qa` | `runtime-aware` | Modes, issue taxonomy, report template, branch-scoped QA flow | Browser execution, screenshot capture, local app interaction |
| `setup-browser-cookies` | `runtime-aware` | Session setup flow, fallback options, safety notes | Cookie extraction/import tooling, browser-profile access, secure credential handling |

## Adoption Guidance

- Adopt `plan-ceo-review`, `plan-eng-review`, `review`, `ship`, and `retro` first if your goal is immediate reuse.
- Add `browse`, `qa`, and `setup-browser-cookies` when your Codex environment already exposes browser or session tooling, or when explicit blind spots are acceptable.
- Use `docs/adoption-examples.md` to see the expected difference between stable and runtime-aware usage.

## Codex Adaptation Strategy

When porting a runtime-heavy gstack skill into Codex, use this execution order:

1. Prefer repo-local or team-local browser tooling if it already exists.
2. Prefer host-provided Codex/browser capabilities when available.
3. Fall back to screenshots, HTTP checks, and explicit limitations when full automation is not available.
4. Never pretend full parity exists when the runtime is missing.

## What Counts As "Ported" Here

These skills are considered ported because:

- the operating workflow is preserved
- the expected outputs are preserved
- the decision points and evidence standards are preserved
- the runtime dependency boundary is documented instead of hidden

In other words, `ported` here means workflow parity with explicit runtime boundaries, not a guarantee that every Codex environment can execute the full browser path.

## Follow-On Work

- Add a concrete Codex-native browser runtime shim if one becomes stable enough to package.
- Add adapter scripts for cookie import or session seeding when the host environment supports them safely.
- Add example integrations for Playwright- or browser-based Codex environments.
