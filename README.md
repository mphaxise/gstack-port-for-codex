# GStack Port for Codex — Extended

**Codex-native versions of Garry Tan’s GStack and GBrain, a Praneet extension layer for responsible product judgment, and a tracked Impeccable design-quality integration.**

This repository started as a port of [GStack](https://github.com/garrytan/gstack). It now has four distinct layers, tracked separately so their provenance stays clear.

| Layer | What it contributes | Current registry |
| --- | --- | ---: |
| **GStack** | Planning, design, review, debugging, QA, release, and engineering workflows | [56 ports](data/skill-map.json) |
| **GBrain** | Capture, research, ingestion, daily operations, local memory, and knowledge maintenance | [53 ports](data/gbrain-skill-map.json) |
| **Praneet extensions** | Responsible design, accessibility, research synthesis, design leadership, market judgment, and outcome learning | [7 extensions](data/praneet-skill-map.json) |
| **Impeccable integration** | Project-aware design quality, optional deterministic checks, critique evidence, and external live-mode routing | [capability map](data/impeccable-capability-map.json) |

## What changed from upstream

This is not a line-for-line copy. The `2026-07-16` full-surface audit confirms that all 54 current upstream GStack skills and all 53 current upstream GBrain skills are represented; the GStack registry also retains the local `gstack` router and legacy `checkpoint` compatibility skill.

- **Codex-native skills:** upstream commands were rewritten as focused `SKILL.md` workflows with Codex-oriented invocation and outputs.
- **Explicit runtime boundaries:** browser, automation, subagent, permission, and external-tool dependencies are labeled instead of being treated as universal capabilities.
- **Local GBrain substrate:** ambient memory behavior was adapted into explicit Markdown-backed capture, search, linking, ingestion, synchronization, citation, and health-check tools.
- **Natural-language routing:** [`workflow-router`](skills/workflow-router/SKILL.md) chooses a small, useful skill set from an ordinary request; users do not need to memorize the catalog.
- **Validation and drift tracking:** machine-readable registries, tests, health checks, and upstream-drift tooling keep the port inspectable as the tracked upstream sources evolve.
- **Tracked design runtime:** selected [Impeccable](https://github.com/pbakaus/impeccable) guidance is adapted into a concise Codex bridge. Its Apache-2.0 detector, hooks, and live browser runtime remain optional upstream capabilities.

See the [GStack compatibility map](docs/compatibility-map.md), [GBrain adaptation memo](docs/gbrain-adaptation-memo.md), [Impeccable compatibility map](docs/impeccable-compatibility-map.md), and [runtime compatibility notes](docs/runtime-compatibility.md) for the detailed boundaries.

## What is distinctly mine

The Praneet layer is not a cosmetic persona. It changes what the system checks and how it makes recommendations.

- [`responsible-design-review`](skills/responsible-design-review/SKILL.md) checks autonomy, consent, dark patterns, fairness, vulnerable users, and data dignity.
- [`accessibility-review`](skills/accessibility-review/SKILL.md) makes accessibility a first-class quality bar rather than a small visual-QA check.
- [`research-synthesis`](skills/research-synthesis/SKILL.md) grades evidence, checks bias, preserves quote-to-insight traceability, and names what remains unknown.
- [`design-leadership-review`](skills/design-leadership-review/SKILL.md) adds a CDO-level lens for quality bars, critique, organizational implications, alignment, and durable decision records.
- [`startup-memo`](skills/startup-memo/SKILL.md) and [`market-map`](skills/market-map/SKILL.md) combine founder judgment with user impact, ethics, and social consequences.
- [`outcome-memory`](skills/outcome-memory/SKILL.md) compares recommendations with real results so future judgment can improve instead of repeating the same assumptions.

The router also uses a chief-of-staff selection pattern: consider the skills that could add leverage, then deliberately pare them down to the smallest useful set. That favors judgment over process for its own sake.

## Try it

Copy only the skills you want into your Codex skills directory:

```bash
mkdir -p "$CODEX_HOME/skills"
cp -R skills/workflow-router "$CODEX_HOME/skills/"
cp -R skills/responsible-design-review "$CODEX_HOME/skills/"
cp -R skills/research-synthesis "$CODEX_HOME/skills/"
```

Then ask naturally:

```text
Review this feature for user agency, accessibility, and unintended harm.
```

```text
Synthesize these interviews, grade the evidence, and separate participant voice from interpretation.
```

```text
Choose the smallest useful workflow for taking this feature from plan review through QA.
```

Other useful entry points:

- [`gstack`](skills/gstack/SKILL.md) — route across the engineering and product-development surface
- [`brain-ops`](skills/brain-ops/SKILL.md) — use local memory before outside research or new conclusions
- [`office-hours`](skills/office-hours/SKILL.md) — pressure-test an idea before implementation planning
- [`design-leadership-review`](skills/design-leadership-review/SKILL.md) — review whether the organization is making the right design decision
- [`design-quality`](skills/design-quality/SKILL.md) — apply project context, design gates, optional Impeccable checks, and evidence-aware fallbacks

## Mutable sources and privacy

GBrain’s local substrate can synchronize a changing authoritative file—such as a living strategy, identity, or operating document—without publishing its contents:

```bash
python3 scripts/brain_sync_source.py path/to/source.md --title "Source title"
```

When the source changes, the managed projection replaces its current compiled truth while retaining version, hash, and supersession provenance. An unchanged source is a byte-for-byte no-op. Generated brain content is ignored by Git by default; only the public [`brain/README.md`](brain/README.md) contract is tracked.

## Honest boundaries

- `native` means the workflow maps cleanly to Codex.
- `workflow-adapted` means the operating intent is preserved but the interaction or runtime model changed.
- `runtime-aware` means the skill still depends on available browser, session, automation, device, credential, or host tooling.
- Impeccable `external-runtime` capabilities stay upstream and run only when already installed in the target project.
- The repository includes a file-backed brain substrate and helper scripts; it does not publish a user’s private local brain corpus.
- Registry pins are conservative snapshots. Run the drift checker before claiming current upstream parity.

## Repository map

- [`skills/`](skills/) — GStack, GBrain, and Praneet workflow definitions
- [`data/`](data/) — separate provenance and compatibility registries
- [`docs/`](docs/) — adaptation decisions, compatibility maps, and runtime audits
- [`scripts/`](scripts/) — validation, drift, status, and local-brain helpers
- [`brain/README.md`](brain/README.md) — local brain structure and operating contract

## Validate the package

```bash
python3 scripts/validate_repo.py
python3 -m unittest discover -s tests
python3 scripts/print_status.py
python3 scripts/brain_doctor.py
python3 scripts/check_upstream_drift.py --map impeccable
```

Current Codex behavior is checked against the official Codex manual before compatibility or runtime guidance is updated. See [`AGENTS.md`](AGENTS.md) and the [documentation refresh log](docs/codex-documentation-refresh.md).

## Upstream and attribution

- [garrytan/gstack](https://github.com/garrytan/gstack)
- [garrytan/gbrain](https://github.com/garrytan/gbrain)
- [pbakaus/impeccable](https://github.com/pbakaus/impeccable)
- GStack and GBrain adaptations use their MIT-licensed sources. Impeccable-derived guidance retains Apache-2.0 attribution. See [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE).

- GStack conservative runtime baseline: `2aa745cb0e4331d683e727ec77385d04cdbb45a2`; skill-workflow parity was audited at `a3259400a366593e0c909dd9ac3e59752efd2488` on July 16.
- GBrain conservative runtime baseline: `b7e3005b5b3f1b54082f9c5990482ebf81a4a807`; skill-workflow parity was audited at `5008b287e47bf791132eedfebf66bdef11e9398c` on July 16.
- Impeccable capability baseline: `8259c28209b92792005cec14dad573df39f68eaf`; the complete command, detector, hook, live-mode, provider, and behavior-test surface was classified on July 16.

The baseline pins stay intentionally conservative so `scripts/check_upstream_drift.py` continues to reveal broad upstream runtime drift. Per-skill freshness uses each skill's `source_commit` or the map's `skill_parity_commit`, so old runtime churn is not misreported as new skill drift. See the [July 16 parity audit](docs/upstream-parity-2026-07-16.md) for the exact workflow and runtime boundary.
