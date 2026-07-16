# GStack Port for Codex — Extended

**Codex-native versions of Garry Tan’s GStack and GBrain, plus a separate Praneet extension layer for design leadership, responsible product judgment, research rigor, and outcome learning.**

This repository started as a port of [GStack](https://github.com/garrytan/gstack). It now has three distinct layers, tracked separately so their provenance stays clear.

| Layer | What it contributes | Current registry |
| --- | --- | ---: |
| **GStack** | Planning, design, review, debugging, QA, release, and engineering workflows | [56 ports](data/skill-map.json) |
| **GBrain** | Capture, research, ingestion, daily operations, local memory, and knowledge maintenance | [53 ports](data/gbrain-skill-map.json) |
| **Praneet extensions** | Responsible design, accessibility, research synthesis, design leadership, market judgment, and outcome learning | [7 extensions](data/praneet-skill-map.json) |

## What changed from upstream

This is not a line-for-line copy.

- **Codex-native skills:** upstream commands were rewritten as focused `SKILL.md` workflows with Codex-oriented invocation and outputs.
- **Explicit runtime boundaries:** browser, automation, subagent, permission, and external-tool dependencies are labeled instead of being treated as universal capabilities.
- **Local GBrain substrate:** ambient memory behavior was adapted into explicit Markdown-backed capture, search, linking, ingestion, citation, and health-check tools.
- **Natural-language routing:** [`workflow-router`](skills/workflow-router/SKILL.md) chooses a small, useful skill set from an ordinary request; users do not need to memorize the catalog.
- **Validation and drift tracking:** machine-readable registries, tests, health checks, and upstream-drift tooling keep the port inspectable as both upstream projects evolve.

See the [GStack compatibility map](docs/compatibility-map.md), [GBrain adaptation memo](docs/gbrain-adaptation-memo.md), and [runtime compatibility notes](docs/runtime-compatibility.md) for the detailed boundaries.

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

## Honest boundaries

- `native` means the workflow maps cleanly to Codex.
- `workflow-adapted` means the operating intent is preserved but the interaction or runtime model changed.
- `runtime-aware` means the skill still depends on available browser, session, automation, device, credential, or host tooling.
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
```

Current Codex behavior is checked against the official Codex manual before compatibility or runtime guidance is updated. See [`AGENTS.md`](AGENTS.md) and the [documentation refresh log](docs/codex-documentation-refresh.md).

## Upstream and attribution

- [garrytan/gstack](https://github.com/garrytan/gstack)
- [garrytan/gbrain](https://github.com/garrytan/gbrain)
- MIT license; see [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE)
