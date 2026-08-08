# Implementation Strategy

## Goal

Maintain one inspectable GStack and GBrain package with a portable skill core, explicit runtime adapters, measurable export fidelity, and conservative upstream adoption.

## Architecture

```text
upstream sources and adopted commits
                |
       canonical skill inventory
                |
   reconciliation and removal records
                |
         portable skill core
          /             \
 Codex adapter       Claude adapter
          \             /
   target validation and drift reports
```

The portable core contains reusable intent, workflow, acceptance criteria, and provenance. An adapter contains only host-specific invocation, tools, permissions, or runtime behavior. Private personal context stays outside the package.

## Current components

- `data/skill-map.json`: GStack source and per-skill provenance
- `data/gbrain-skill-map.json`: GBrain source and per-skill provenance
- `data/praneet-skill-map.json`: separately tracked extensions
- `data/impeccable-capability-map.json`: external design-runtime capabilities
- `src/gstack_port_for_codex/registry.py`: registry and portability validation
- `scripts/check_upstream_drift.py`: upstream movement reporting
- `skills/`: portable workflows and the current Codex adapters
- `brain/` and `src/gstack_port_for_codex/brain.py`: local file-backed substrate
- compatibility, runtime, and documentation-refresh notes under `docs/`

## Delivery sequence

### 1. Prevent new portability regressions

Validate names, required metadata, authoring-machine paths, unsupported frontmatter, and routed skill targets. Resolve installed helpers from runtime context. Keep private provider and delegation policy outside the public package.

### 2. Introduce the reconciliation record

Define a small machine-readable schema for source hashes, target hashes, adopted and current upstream commits, retention, intentional removals, host coupling, companion resources, and evaluator results. Add fixtures for faithful, adapted, removed, and invalid exports.

### 3. Canonicalize the inventory

Hash the source and export population, group duplicates, assign canonical identities, and connect each target to its source and adapter. Preserve user edits as a distinct class until reviewed.

### 4. Prove one representative tranche

Reconcile routers, upgrade workflows, skillpack checks, and one runtime-heavy skill. Run a three-way comparison across adopted source, current local state, and current upstream. Measure retention and record every intentional removal.

### 5. Expand upstream adoption

Process the remaining skills in bounded tranches. Keep movement, review, and adoption separate. Update per-skill source commits only after validation establishes the adopted state.

### 6. Deepen runtime integrations

Improve durable reports, browser evidence, GBrain source integrity, and optional host integrations after the canonical package is stable.

## Runtime rules

- Claude and Codex are peer runtimes selected by the operator. They exchange written handoffs when work crosses runtimes.
- `AGENTS.md` carries Codex instructions. Claude-specific adapters use their native instruction surfaces.
- Shared skill content stays portable; runtime adapters stay narrow and explicit.
- Personal delegation and provider-routing policy belongs in the operator's private workspace.

## Acceptance checks

- deterministic unit tests for parsers and manifest rules
- repository-wide registry and skill portability validation
- skill-specific script checks and fixtures
- full skillpack health and upstream drift checks
- exact diff and clean-worktree review before commit
- current official Codex documentation review before runtime claims
- current Claude Code version and official Claude documentation review before Claude-specific claims

## Out of scope for the current milestone

- wholesale migration of Claude skills or personal context
- full reconciliation of the audit population in one commit
- private provider routing and delegation policy
- bundled parity with browser daemons, private credentials, or always-on external services
- push, merge, release, or publication
