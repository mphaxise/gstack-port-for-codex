# Upstream Freshness Record

This record separates three states: a source commit observed during review, a
capability boundary that was actually inspected, and the conservative baseline
used by the local drift checker. A newer upstream commit does not mean that
all of its runtime or workflow changes are present here.

## Observed source heads

| Source | Observed head | Review interpretation |
| --- | --- | --- |
| [GStack](https://github.com/garrytan/gstack/commit/a3259400a366593e0c909dd9ac3e59752efd2488) | `a3259400a366593e0c909dd9ac3e59752efd2488` | The local skill surface was audited through this commit. Runtime changes after the local baseline still need a separate review. |
| [GBrain](https://github.com/garrytan/gbrain/commit/15b9863d13635d173562a54f55a1d388bfcf546b) | `15b9863d13635d173562a54f55a1d388bfcf546b` | The current default-branch head and mapped skill drift were observed. They have not been represented as a blanket local runtime upgrade. |
| [Impeccable](https://github.com/pbakaus/impeccable/commit/a075d89bdbe60b2b00220cb0527fb5091e84215e) | `a075d89bdbe60b2b00220cb0527fb5091e84215e` | Recent source, provider, and detector changes were observed. The local capability map remains the reviewed partial-adoption boundary. |

## Local baselines

- GStack runtime baseline: `2aa745cb0e4331d683e727ec77385d04cdbb45a2`.
- GBrain runtime baseline: `b7e3005b5b3f1b54082f9c5990482ebf81a4a807`.
- GBrain skill-workflow parity baseline: `5008b287e47bf791132eedfebf66bdef11e9398c`.
- Impeccable capability baseline: `8259c28209b92792005cec14dad573df39f68eaf`.

The baselines remain conservative because this repository ports selected
workflow guidance into Codex. Advancing a baseline requires reviewing the
mapped source files, adapting the relevant local behavior, and rerunning the
validation surface. Use `scripts/check_upstream_drift.py` for the live report;
network failure is an unavailable check, not a parity result.

## Public scope decision

The public package contains planning, implementation, testing, review, and
release workflows. Personal delegation policy, private model routing,
benchmark evidence, provider inventories, and local operating controls are
outside this public freshness record and repository.
