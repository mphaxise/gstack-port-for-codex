# Skill Reconciliation Alpha

The alpha milestone makes adaptation decisions reproducible for the public GStack and GBrain Codex package. It establishes the manifest format, inventories every packaged skill, and proves the workflow on six representative records.

## Scope

The canonical inventory contains 117 packaged `SKILL.md` files:

- 115 connect to the GStack, GBrain, or public Praneet registries.
- `design-quality` and `workflow-router` are local-origin skills.
- The current public package contains no byte-identical skill files.

The earlier 264-package export audit covered a broader cross-runtime population and found 155 unique content groups. That population includes artifacts outside this public repository. Alpha preserves the finding as program evidence and keeps private or Claude-owned material outside the package.

## Representative tranche

The manifest records:

| Skill | Role | Host coupling | Local line overlap with adopted source |
| --- | --- | --- | ---: |
| `gstack` | upstream router | Codex adapter | 0.62% |
| `workflow-router` | local router | portable | local origin |
| `gstack-upgrade` | GStack upgrade workflow | Codex adapter | 1.33% |
| `gbrain-upgrade` | GBrain upgrade workflow | Codex adapter | 2.94% |
| `skillpack-check` | package health workflow | Codex adapter | 3.81% |
| `browse` | runtime-heavy browser workflow | runtime-heavy | 0.36% |

Line overlap measures normalized, nonblank source lines retained verbatim in the local target. It is a conservative review signal. Functional fidelity still depends on the recorded classifications, intentional-removal reasons, companion resources, runtime boundaries, and validation results.

The adopted and current upstream hashes are identical for all five upstream-backed records in this tranche. The wider GStack and GBrain repositories have advanced substantially, so later tranches still require source-path review before adoption.

## Files and validation

- `data/canonical-skill-inventory.json` assigns canonical IDs, content hashes, exact-content groups, provenance, ownership, and adapter labels.
- `data/reconciliation-record.schema.json` defines the portable record contract.
- `data/reconciliation-alpha.json` stores the reviewed tranche.
- `scripts/build_skill_inventory.py --check` detects inventory drift.
- `scripts/refresh_reconciliation_manifest.py` refreshes upstream hashes and retention from explicit public checkouts.
- `scripts/validate_repo.py` checks inventory freshness, local hashes, classifications, explained removals, companion metadata, and record decisions.

Reproduce the upstream-backed check with:

```bash
python3 scripts/refresh_reconciliation_manifest.py \
  --gstack-repo /path/to/gstack \
  --gbrain-repo /path/to/gbrain \
  --check
```

## Beta handoff

The [beta tranche](reconciliation-beta.md) reconciles the capture and filing family, reviews one known upstream change, and extends the schema with resource hashes and structured evaluator outcomes. Semantic retention remains a later option if line overlap proves insufficient for a future family.
