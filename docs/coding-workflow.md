# Coding Workflow

This repository gives Codex a reusable path from an unclear coding request to
a tested change. The skills are composable. Start with the smallest useful
entry point and add review lenses when the change needs them.

## The default path

1. Clarify the outcome with `office-hours` or `spec`.
2. Pressure-test scope with `plan-ceo-review` when the product decision is
   still open.
3. Shape the implementation with `plan-eng-review`. Include architecture,
   interfaces, sequencing, failure cases, and tests.
4. Slice the work into units with one clear outcome, readable inputs, an
   explicit write set, and a deterministic check. Keep coupled changes in one
   sequence. Separate independent units only after their interfaces are clear.
5. Implement with the repository's normal tools and instructions.
6. Run `testing`, `qa`, and `review` at the appropriate depth.
7. Use `ship` when the branch is ready for its local release gates.

`autoplan` combines the planning lenses into one reviewed recommendation. The
`workflow-router` skill selects a small path from ordinary language, so users
can ask for the outcome without memorizing the catalog.

## Choosing the planning depth

| Change shape | Useful starting point |
| --- | --- |
| Small, local bug | `investigate`, then `testing` |
| New feature with settled direction | `spec`, then `plan-eng-review` |
| Product idea with open scope | `office-hours`, then `plan-ceo-review` |
| User-facing interaction | Add `plan-design-review` |
| Developer-facing API, CLI, or docs | Add `plan-devex-review` |
| Broad repository change | `autoplan`, then `plan-eng-review` |

## A good implementation slice

Each slice should make one observable part of the outcome true. Record the
files it may change, the behavior it owns, its dependencies, and the check
that proves it. A slice that shares mutable state with another slice belongs in
the same sequence or needs an explicit interface before it is separated.

Keep planning artifacts honest. Mark assumptions, open questions, and deferred
work separately from decisions. A green unit test proves the exercised
behavior; it does not prove that the whole feature is accepted.

## Public boundary

The package documents provider-neutral planning, implementation, testing, and
review workflows. Personal operating policies, private model routing, private
benchmarks, credentials, and local memory remain outside this repository.
