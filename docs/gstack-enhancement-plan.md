# GStack and GBrain Enhancement Plan

## Current snapshot

Reviewed on `2026-08-08`.

- The registries contain 56 GStack entries, 53 GBrain entries, and 7 public Praneet extensions.
- All mapped GStack skills were reviewed through `94993f74012782fd94416dd44b8314f6363a13a4`; accepted source pins and reviewed deferrals remain distinct.
- All mapped GBrain skills were reviewed through `0b47afbf402a4e27a648bb9d131ce584461461ea`; accepted source pins and reviewed deferrals remain distinct.
- Current Codex is `codex-cli 0.144.0`; current Claude Code is `2.1.224`.
- Claude and Codex can coexist on one machine. This repository owns the portable core and Codex adapters. Runtime-specific instructions and private personal context stay with their owning runtime or private workspace.

## Evidence behind the reset

The August export review found a canonicalization and fidelity problem before it found a coverage problem. Its 264 exported packages collapsed to 155 unique content groups. Among 70 recoverable adaptations, the median retained source content was 12%, and 62 retained less than half. The review also found missing removal manifests, unresolved router targets, non-portable metadata, hard-coded home paths, and target-specific intent that could disappear during export.

These findings are technical audit evidence for the public Codex tooling. Claude-owned personal skills, private context, and unrelated materials stay with their owners.

## Priorities

### P0: Keep the package portable and internally valid

The current milestone adds preventive checks for:

- portable skill names and required `name` and `description` metadata
- unsupported `user-invocable` frontmatter
- authoring-machine home paths
- explicit router references to absent packaged skills
- runtime-relative access to the official Codex manual helper

It also keeps personal delegation policy and provider routing outside the public package.

### P1: Canonicalize before broad upstream adoption

Build one canonical inventory across the tracked skill sources and export targets:

1. Assign a stable canonical identity to every skill.
2. Group exact and near-duplicate packages by content hash and provenance.
3. Record source commit, current upstream commit, local target, runtime adapter, and owner.
4. Classify each local difference as preserved, host-adapted, condensed, intentionally removed, user-edited, or obsolete.
5. Keep one canonical portable core per skill and small Claude or Codex adapters where host behavior differs.

This inventory is the prerequisite for a safe mass refresh. It prevents a newer upstream copy from overwriting a deliberate local adaptation or multiplying duplicate exports.

### P2: Make adaptation loss measurable

Each adapted export should carry a machine-readable reconciliation record with:

- source and target hashes
- source, local, and upstream commits
- retained-content measurement
- intentional-removal manifest with reasons
- required router targets and companion resources
- host-coupling classification
- validation commands and results

The export pipeline should fail closed when a removal is unexplained, a required target is absent, or retention falls below the configured threshold without an approved adaptation record.

The complete reconciliation configures the threshold at 50% and records an
explicit approval reason for every adaptation below it. The repository gate
validates both fields.

### P3: Reconcile upstream in representative tranches

Run a three-way comparison for each tranche:

```text
adopted source commit
        + current local skill
        + current upstream skill
        = reviewed portable core and runtime adapters
```

Start with routers, upgrade workflows, skillpack validation, and one runtime-heavy skill. Use the results to refine the manifest and evaluator before widening the refresh. Keep upstream movement, local review, and local adoption as separate states.

### P4: Deepen the combined skillpack

After canonicalization is stable:

- connect planning, review, QA, release, and retro skills to durable report artifacts
- share evidence paths across browser QA and design-quality workflows
- improve GBrain capture, citation, taxonomy, and source-sync loops
- retain honest boundaries for browser daemons, hooks, credentials, always-on services, and other host-variable capabilities

## Validation ladder

Every changed tranche must pass `python3 scripts/check_engineering_milestone.py`.
The command covers the local inventory, repository, unit, installer, public
boundary, brain, compilation, and diff checks. Use `--upstream` for the tracked
public drift checks. Changed public guidance also receives an editorial review.

## Milestone boundary

The guardrail milestone established portable metadata and routing checks.
Reconciliation alpha added the canonical inventory and representative tranche.
Reconciliation beta proved resource hashing and structured evaluator outcomes.
Engineering milestone alpha integrated those layers behind one gate. Complete
reconciliation now covers all 108 canonical GStack and GBrain skills and 109
mapped source lineages, with 68 accepted source pins and 41 reviewed deferrals.
The broader 264-package
export population remains outside this public repository and retains its own
ownership boundary.

## Definition of done for the reconciliation program

- Every packaged skill has one canonical identity and explicit provenance.
- Duplicate exports resolve to one portable core or a documented runtime adapter.
- Intentional removals and material adaptations are machine-readable and reviewable.
- Router targets, companion resources, metadata, and host coupling validate before export.
- Current upstream changes are classified and adopted or deferred with evidence.
- Codex and Claude adapters preserve their runtime contracts while private cross-runtime context stays with its owner.
