# Skill Reconciliation Beta

Beta tests resource-level export fidelity on the bounded capture and filing family. It compares the adopted GBrain source, current upstream, and the local Codex adapter. The conservative source pins remain unchanged.

## Findings and decisions

Current upstream GBrain is `0b47afbf402a4e27a648bb9d131ce584461461ea`; the adopted skill commit is `5008b287e47bf791132eedfebf66bdef11e9398c`.

- `capture` has one upstream change after the adopted commit. Upstream now says its CLI title is capped at 80 characters and appends an ellipsis when truncated. The local `brain_capture_signal.py` helper derives a title from the first 12 words. Beta records the upstream change as reviewed and deferred because copying the CLI rule would misdescribe the Codex adapter.
- `brain-taxonomist/SKILL.md` is unchanged between the adopted and current upstream commits. Its `routing-eval.jsonl` companion is also unchanged. Beta preserves that six-case fixture byte for byte.
- The local taxonomist now names the fixture and its contract. The imported surface contains only the public routing fixture.

## Deterministic evidence

`data/reconciliation-beta.json` adds one resource record with adopted, current-upstream, and local SHA-256 hashes. The three hashes are equal for the preserved routing fixture.

The manifest also records five evaluator outcomes:

- every nonblank line is a valid routing case
- the fixture is nonempty
- intents are unique
- every expected skill is packaged
- every ambiguity target is packaged

Repository validation recomputes the resource hash, fixture hash, case count, and outcomes. A stale or failing result invalidates the manifest.

Refresh and verify the tranche with:

```bash
python3 scripts/refresh_reconciliation_manifest.py \
  --manifest data/reconciliation-beta.json \
  --gstack-repo /path/to/gstack \
  --gbrain-repo /path/to/gbrain \
  --check
```

## Codex documentation decision

Verified on 2026-08-08 with `codex-cli 0.144.0` and the current official Codex manual. Codex packages skills as directories with `SKILL.md` and can load supporting files from the skill directory through progressive disclosure. Beta therefore keeps the routing fixture beside the skill and validates its relative packaged targets. Claude permissions, hooks, tools, and personal context stay outside this public Codex artifact.

## Next boundary

Continue with another small family only after its current upstream delta is identified. Resource adoption, skill-text adoption, and source-pin movement remain separate decisions.
