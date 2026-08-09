# Upstream Freshness Record

This record separates three states: a source commit observed during review, a
capability boundary that was actually inspected, and the conservative baseline
used by the local drift checker. A newer upstream commit does not mean that
all of its runtime or workflow changes are present here.

## Observed source heads

| Source | Observed head | Review interpretation |
| --- | --- | --- |
| [GStack](https://github.com/garrytan/gstack/commit/94993f74012782fd94416dd44b8314f6363a13a4) | `94993f74012782fd94416dd44b8314f6363a13a4` | All mapped skills were reviewed. Accepted source pins and host-specific deferrals are recorded separately. |
| [GBrain](https://github.com/garrytan/gbrain/commit/0b47afbf402a4e27a648bb9d131ce584461461ea) | `0b47afbf402a4e27a648bb9d131ce584461461ea` | All 53 mapped skills were reviewed. The optional database and CLI runtime remains outside the packaged guarantee. |
| [Impeccable](https://github.com/pbakaus/impeccable/commit/5d10bc842cbccd2ae7d3a88296d87d3be0b125b3) | `5d10bc842cbccd2ae7d3a88296d87d3be0b125b3` | The current head and hook movement were observed by the broader gate. The separate capability map remains at its prior reviewed boundary. |

## Local baselines

- GStack runtime baseline: `2aa745cb0e4331d683e727ec77385d04cdbb45a2`.
- GBrain runtime baseline: `b7e3005b5b3f1b54082f9c5990482ebf81a4a807`.
- GStack mapped-skill review boundary: `94993f74012782fd94416dd44b8314f6363a13a4`.
- GBrain mapped-skill review boundary: `0b47afbf402a4e27a648bb9d131ce584461461ea`.
- Impeccable capability baseline: `8259c28209b92792005cec14dad573df39f68eaf`.

The runtime baselines remain conservative because this repository packages
Codex adaptations. Upstream runtime stacks retain separate boundaries.
Mapped-skill freshness uses the review boundary, while `source_commit` records
accepted content. Use `scripts/check_upstream_drift.py` for the live report. A
network failure leaves the check unavailable and provides no parity result.

## Public scope decision

The public package contains planning, implementation, testing, review, and
release workflows. Personal delegation policy, private model routing,
benchmark evidence, provider inventories, and local operating controls are
outside this public freshness record and repository.
