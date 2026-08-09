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
- `data/canonical-skill-inventory.json`: deterministic identity and exact-content groups for every packaged skill
- `data/reconciliation-alpha.json`: the first reviewed three-way reconciliation tranche
- `data/reconciliation-beta.json`: the capture and filing resource-fidelity tranche
- `data/reconciliation-complete.json`: 108 canonical skills and all 109 mapped source lineages
- `data/reconciliation-record.schema.json`: the machine-readable reconciliation contract
- `docs/engineering-milestone-alpha.md`: the integrated acceptance record
- `scripts/check_engineering_milestone.py`: the shared local and CI acceptance gate
- `src/gstack_port_for_codex/registry.py`: registry and portability validation
- `src/gstack_port_for_codex/reconciliation.py`: inventory, hashing, retention, refresh, and validation logic
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

Alpha completed steps 2 through 4 on `2026-08-08`. The deterministic inventory covers all 117 packaged skills. The representative tranche covers `gstack`, `workflow-router`, `gstack-upgrade`, `gbrain-upgrade`, `skillpack-check`, and `browse`. Repository validation checks the tracked inventory and each record's local hash. The refresh command verifies upstream hashes and retention when public source checkouts are available.

Beta completed the first bounded step 5 tranche on `2026-08-08`. It retained the Codex adapter's 12-word title behavior after reviewing the current `capture` change, preserved the stable `brain-taxonomist` routing fixture, and added deterministic resource hashes and structured routing outcomes.

### 5. Expand upstream adoption

Complete as of 2026-08-08 for the canonically owned GStack and GBrain skill
surface. `source_commit` records adopted content; `reviewed_commit` or
`skill_reviewed_commit` records freshness after an accepted update or an
evidence-backed deferral. Future upstream movement reopens only affected mapped
skills.

### 6. Deepen runtime integrations

Improve durable reports, browser evidence, GBrain source integrity, and optional host integrations after the canonical package is stable.

## Runtime rules

- Claude and Codex are peer runtimes selected by the operator. They exchange written handoffs when work crosses runtimes.
- `AGENTS.md` carries Codex instructions. Claude-specific adapters use their native instruction surfaces.
- Shared skill content stays portable; runtime adapters stay narrow and explicit.
- Personal delegation and provider-routing policy belongs in the operator's private workspace.

## Acceptance checks

`python3 scripts/check_engineering_milestone.py` runs the required local acceptance ladder. Use `--upstream` for network-backed drift checks. Runtime claims still require current official vendor documentation, and every commit receives an exact diff and clean-worktree review.

## Historical alpha exclusions

These boundaries applied when engineering milestone alpha was accepted. The
full mapped-skill reconciliation is now complete; the remaining exclusions
still apply.

- wholesale migration of Claude skills or personal context
- private provider routing and delegation policy
- bundled parity with browser daemons, private credentials, or always-on external services
- push, merge, release, or publication
