# Impeccable Compatibility Map

## Current boundary

The complete Impeccable design surface is tracked at `pbakaus/impeccable@8259c28209b92792005cec14dad573df39f68eaf`, observed July 16, 2026. The machine-readable source is [`data/impeccable-capability-map.json`](../data/impeccable-capability-map.json).

The integration combines three modes:

| Mode | Meaning |
| --- | --- |
| `codex-adapted` | The workflow is represented in local skills and follows Codex permissions, evidence, and routing rules. |
| `external-runtime` | The local skill can use Impeccable when it is already installed; runtime code stays upstream. |
| `tracking-only` | Drift is monitored while local adoption remains deferred or unnecessary. |

## Integrated capabilities

The local `design-quality` bridge and existing design skills now cover:

- product and design context loading
- direction-to-implementation flow
- two-pass critique with visual and deterministic evidence
- optional detector execution with an explicit manual fallback
- severity, false-positive, and evidence-limit reporting
- responsive, state, motion, accessibility, overflow, error, and internationalization gates
- handoffs into accessibility, responsible-design, and design-leadership review
- deterministic registry, routing, and drift-classification tests

## External runtime capabilities

These capabilities remain in Impeccable:

- deterministic detector implementation and its 46-rule registry
- provider-native edit hooks
- live browser selection, variant generation, steering, acceptance, and source rewriting
- specialized commands such as `bolder`, `quieter`, `animate`, `colorize`, `typeset`, `layout`, and `overdrive`

Keeping these upstream preserves their release path, framework adapters, browser fixes, and Apache-2.0 boundary. Local skills use `npx --no-install impeccable` for availability and execution. They never install the package implicitly.

## Local authority

The local system remains authoritative for:

- accessibility scope and compliance caveats
- responsible design, power, consent, autonomy, fairness, and data dignity
- design-leadership and organizational decisions
- evidence provenance, privacy, and durable memory
- product-specific exceptions to generic anti-pattern guidance

## Drift model

Run:

```bash
python3 scripts/check_upstream_drift.py --map impeccable
python3 scripts/check_upstream_drift.py --map impeccable --json
```

The tracker compares the baseline and each capability's source boundary with the current default branch. Explicit `upstream_paths` map changes in the source skill, command references, detector, hooks, live runtime, provider build, and tests to the affected local capability.

Every review reports three independent states:

1. **Upstream movement:** commits and paths changed after the tracked boundary.
2. **Local review:** affected capabilities were inspected and classified.
3. **Local adoption:** local skills, tests, or docs changed and their source boundary advanced.

The repository-level baseline advances only after the complete mapped surface is reviewed. Partial refreshes use per-capability `source_commit` values.

## Triage rules

Immediate focused review is required when changes touch:

- `skill/SKILL.src.md`
- `skill/reference/critique.md`
- `skill/reference/audit.md`
- `skill/reference/document.md`
- `skill/reference/live.md`
- `skill/reference/hooks.md`
- `cli/engine/`
- Codex hook or provider packaging
- license or security boundaries

Site-only and marketing-only changes remain monitored unless they alter published usage or installation contracts.

## Automation contract

The scheduled check runs weekly against the local project because its report includes ignored local-brain state. It performs repository validation, tests, status output, and drift checks for GStack, GBrain, and Impeccable. It creates a focused review item only when a tracked capability changed, a validation failed, or the latest reviewed boundary is stale. Clean runs produce a concise no-change report and leave the repository untouched.
