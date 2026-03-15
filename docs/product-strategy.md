# Product Strategy

## Product Thesis

`gstack-port-for-codex` should make it easy to adopt high-rigor coding workflows in Codex without reverse-engineering Claude-specific prompt packs. The product is a compatibility layer: opinionated skills, explicit parity classes, clear migration notes, and lightweight tooling that make future ports faster and safer.

## Problem Statement

Power users want reliable operating modes such as founder-style planning, engineering review, PR review, QA, and shipping workflows. Those modes already exist in gstack, but not in a Codex-ready form. The remaining challenge is not raw coverage; it is making the adaptation trustworthy enough that users know what they can adopt immediately and what still depends on host runtime support.

## Target Users

- Solo builders who want a reusable operating system for Codex
- Teams standardizing how they plan, review, and ship with AI coding agents
- Contributors who want a documented path for maintaining parity as upstream and Codex diverge

## User Jobs To Be Done

- "Show me which gstack skills I can adopt in Codex today without extra runtime work."
- "Tell me honestly which ports depend on browser or session tooling in my host environment."
- "Help me port or maintain an upstream gstack skill without guessing what needs to change."
- "Make sure new ports stay structurally consistent."

## Current Product Scope

### Stable Core

- `plan-ceo-review`
- `plan-eng-review`
- `review`
- `ship`
- `retro`

### Experimental Runtime-Aware Layer

- `browse`
- `qa`
- `setup-browser-cookies`

### Included In The Public Repo

- Compatibility README and strategy docs that explain the adaptation model
- Full upstream-to-Codex coverage map
- All eight skill ports, classified by parity type
- Runtime compatibility notes and adoption examples
- Minimal validation and tests for structural consistency

### Explicitly Not Yet Included

- A bundled browser runtime replacement for upstream gstack
- Cookie extraction or import tooling built into this repo
- Auto-sync against upstream changes
- Packaging or installer automation

## Architecture And Tech Choices

- Keep the repo language-agnostic, with Python only for validation utilities
- Prefer plain Markdown and JSON over a heavy framework
- Use a stable source pin so each port can cite exactly what it adapted from
- Design each skill as concise `SKILL.md` plus references, aligned with Codex skill guidance
- Use parity classes to separate direct prompt portability from host-dependent runtime portability

## Risks And Assumptions

- Assumption: trust comes from explicit scope boundaries, not just saying every skill is ported.
- Risk: users may over-read `ported` as `full runtime parity` unless the README and examples stay clear.
- Risk: some upstream prompts are intentionally verbose, so ports need thoughtful condensation instead of naive copying.
- Risk: users may expect slash-command parity; the docs need to be explicit about Codex-native invocation.

## Public Launch Goal

Ship a repo that a new Codex user can understand in a few minutes: adopt the stable core immediately, evaluate the runtime-aware layer honestly, and contribute future maintenance without reverse-engineering the adaptation model.

## Near-Term Outcome

Anyone visiting the public repo should understand:

- which skills are ready for immediate adoption
- which skills depend on host browser or session tooling
- how the adaptation works
- where future parity work is still needed

## Success Signals

- A new adopter can identify the stable core in under two minutes.
- A runtime-aware user can tell whether their environment is sufficient before attempting QA or browser work.
- A reference skill is usable without reading the upstream repo first.
- The validator catches obvious structural regressions before review.
