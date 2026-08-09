# Engineering Milestone Alpha

Engineering milestone alpha gives the public Codex package one deterministic acceptance gate. It integrates the portability guardrails, canonical inventory, reconciliation alpha and beta records, installer, public boundary, and local brain health into a single maintainer command.

## Integrated state

The milestone includes:

- portable metadata, path, and router-target validation
- canonical identities and content hashes for all packaged skills
- alpha reconciliation records for six representative skills
- beta resource hashes and structured routing outcomes for the capture and filing family
- installer and public-data boundary checks
- current Codex documentation and runtime-boundary records

## Acceptance gate

Run the complete local gate with:

```bash
python3 scripts/check_engineering_milestone.py
```

The command runs every required local check and reports each result separately:

1. canonical inventory freshness
2. repository registry and reconciliation validation
3. the complete unit test suite
4. installer smoke coverage
5. the public boundary scan
6. local brain health
7. Python source compilation
8. staged and unstaged diff formatting

The gate runs `gbrain skillpack-check` when the GBrain CLI is installed. A missing CLI produces a visible skipped result and leaves the repository checks as the local fallback.

Add network-backed drift checks for all tracked public sources with:

```bash
python3 scripts/check_engineering_milestone.py --upstream
```

Before a parity claim or release, also verify every recorded complete-manifest
hash and retention value against local Git checkouts containing the pinned
GStack and GBrain commits:

```bash
python3 scripts/check_engineering_milestone.py --upstream \
  --gstack-repo /path/to/gstack \
  --gbrain-repo /path/to/gbrain
```

Use `--json` when another tool needs structured outcomes.

## Verified result

The 2026-08-08 checkout-backed upstream run completed with 14 passed checks,
one skipped check, and zero failures. The GBrain CLI was absent, so its optional
skillpack command was the skipped check. The run rebuilt the complete manifest
against its pinned Git blobs. Live drift reporting reached these public heads:

- GStack: `94993f74012782fd94416dd44b8314f6363a13a4`
- GBrain: `0b47afbf402a4e27a648bb9d131ce584461461ea`
- public Praneet extension source: `2b46f495fb36f3fbea3b33efd1b29e6a75171072`
- Impeccable: `5d10bc842cbccd2ae7d3a88296d87d3be0b125b3`

## CI and release use

GitHub Actions runs the local gate on every push and pull request. Maintainers
add `--upstream` for live drift and provide both source checkouts before a
parity claim or release. This separates ordinary CI from the stronger
checkout-backed integrity gate.

## Ownership and external state

This repository owns the public portable core, Codex adapters, validation code, and milestone records. Claude-owned runtime surfaces and private Marlowe context stay with their owners. Automation activation, push, merge, release, and publication remain explicit operator actions.
