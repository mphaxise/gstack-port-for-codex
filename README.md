# GStack Port for Codex

Codex-native ports of [garrytan/gstack](https://github.com/garrytan/gstack) plus a workflow port of [garrytan/gbrain](https://github.com/garrytan/gbrain).

This repo started as a GStack compatibility layer. It now bundles GStack's coding engine and GBrain's operating layer into one Codex-native package, with explicit notes where upstream ambient behavior has been adapted into deliberate local workflows.

## What Exists Today

### GStack Surface

This repo tracks the upstream GStack direction while preserving the local Codex/GBrain adaptations. As of the `2026-06-26` refresh, `data/skill-map.json` contains 56 ported GStack entries: the prior 52-skill surface, the legacy local `checkpoint` compatibility skill, and the latest upstream router/`diagram`/`spec` additions ported into Codex-native form.

High-level groups:

- Router and planning: `gstack`, `office-hours`, `spec`, `plan-ceo-review`, `plan-eng-review`, `plan-design-review`, `plan-devex-review`, `autoplan`, `plan-tune`
- Review and QA: `review`, `investigate`, `browse`, `qa`, `qa-only`, `design-review`, `devex-review`, `scrape`
- Design creation: `design-consultation`, `design-shotgun`, `design-html`, `diagram`
- Release and ops: `ship`, `document-release`, `document-generate`, `setup-deploy`, `land-and-deploy`, `benchmark`, `benchmark-models`, `canary`, `health`, `retro`, `landing-report`, `make-pdf`
- Security and safety: `cso`, `careful`, `freeze`, `guard`, `unfreeze`
- GBrain bridge and continuity: `setup-gbrain`, `sync-gbrain`, `context-save`, `context-restore`, `checkpoint`, `learn`
- iOS runtime: `ios-qa`, `ios-fix`, `ios-design-review`, `ios-sync`, `ios-clean`
- Utilities: `open-gstack-browser`, `connect-chrome`, `pair-agent`, `setup-browser-cookies`, `codex`, `gstack-upgrade`, `skillify`

For the adaptation boundary and parity notes, see:

- `docs/compatibility-map.md`
- `docs/gstack-enhancement-plan.md`

### GBrain Surface

The GBrain port is intentionally local-first: the lighter operational layer ports directly, while the deeper memory layer is rewritten around the local `brain/` substrate and helper scripts. As of the `2026-06-26` refresh, `data/gbrain-skill-map.json` tracks 53 ported GBrain skills, including the latest advisor, upgrade, lineage, schema-unification, and skill-optimization workflows adapted for Codex.

Core GBrain ports:

- `academic-verify`
- `archive-crawler`
- `article-enrichment`
- `ask-user`
- `book-mirror`
- `brain-ops`
- `brain-pdf`
- `brain-taxonomist`
- `briefing`
- `capture`
- `citation-fixer`
- `cold-start`
- `concept-synthesis`
- `cron-scheduler`
- `cross-modal-review`
- `daily-task-manager`
- `daily-task-prep`
- `data-research`
- `eiirp`
- `enrich`
- `frontmatter-guard`
- `functional-area-resolver`
- `gbrain-advisor`
- `gbrain-upgrade`
- `idea-lineage`
- `idea-ingest`
- `ingest`
- `install`
- `maintain`
- `media-ingest`
- `meeting-ingestion`
- `migrate`
- `minion-orchestrator`
- `perplexity-research`
- `publish`
- `query`
- `repo-architecture`
- `reports`
- `schema-author`
- `schema-unify`
- `setup`
- `signal-detector`
- `skill-creator`
- `skill-optimizer`
- `skillify`
- `skillpack-check`
- `skillpack-harvest`
- `smoke-test`
- `soul-audit`
- `strategic-reading`
- `testing`
- `voice-note-ingest`
- `webhook-transforms`

### Natural-Language Routing

You do not need to remember the skill names. The repo now also includes:

- `workflow-router`

Its job is to infer the right 1-3 skills from a normal request and apply them automatically.

`workflow-router` now uses a chief-of-staff selection pattern:

1. Cast a generous first-pass net across skills that could plausibly help.
2. Critically pare that list down based on task context, repetition, stakes, memory value, and whether each skill adds real leverage.
3. Use the smallest useful final set instead of asking the user to know or name the right skill.

This means Codex should proactively consider planning, memory, responsible design, accessibility, research, review, QA, and reporting skills when they fit the work, while avoiding unnecessary process for simple one-off tasks.

### Praneet Extensions

This repo also includes a local extension layer in `data/praneet-skill-map.json`. These are hand-port enhancements that preserve GStack/GBrain parity while adding Praneet's design leadership, social ethics, responsible design, founder judgment, and outcome-learning lens.

Praneet extension skills:

- `responsible-design-review`
- `accessibility-review`
- `research-synthesis`
- `startup-memo`
- `market-map`
- `design-leadership-review`
- `outcome-memory`

## Local Brain Substrate

To make the memory-oriented skills honest instead of aspirational, the repo includes a minimal local `brain/` corpus plus deterministic helpers:

- `python3 scripts/brain_init.py`
- `python3 scripts/brain_search.py "query"`
- `python3 scripts/brain_put.py --title ... --category ... --text "..."`
- `python3 scripts/brain_link.py --from-ref ... --to-ref ... --context "..."`
- `python3 scripts/brain_citations.py --fix --verbose`
- `python3 scripts/brain_ingest_source.py <file> --title ...`
- `python3 scripts/brain_ingest_meeting.py <file> --title ... --date ...`
- `python3 scripts/brain_transform_event.py payload.json --event-type auto`
- `python3 scripts/brain_capture_signal.py --text "..." --mode original`
- `python3 scripts/brain_doctor.py`

See [docs/codex-brain-substrate.md](/Users/praneet/gstack-port-for-codex/docs/codex-brain-substrate.md) and [brain/README.md](/Users/praneet/gstack-port-for-codex/brain/README.md).

## Repo Direction

The working shape is:

```text
GStack coding core + GBrain ops layer + local brain substrate + explicit workflow adaptations
```

That means:

- direct Codex fits stay `native`
- upstream runtime-heavy behaviors become `workflow-adapted` when a local, honest equivalent exists
- parity notes stay explicit in the registries and docs

## GBrain Porting Artifacts

- `docs/gbrain-adaptation-memo.md`
- `docs/gbrain-import-inventory.md`
- `docs/gbrain-compatibility-map.md`
- `docs/gbrain-resolver.md`
- `docs/codex-brain-substrate.md`
- `docs/codex-host-refresh-audit.md`
- `docs/codex-documentation-refresh.md`
- `docs/upstream-runtime-deepening-pass.md`
- `docs/praneet-extension-layer.md`
- `data/gbrain-skill-map.json`
- `data/praneet-skill-map.json`

## Quick Start

Copy any skill you want into your Codex skills directory:

```bash
mkdir -p "$CODEX_HOME/skills"
cp -R skills/office-hours "$CODEX_HOME/skills/"
cp -R skills/plan-ceo-review "$CODEX_HOME/skills/"
cp -R skills/autoplan "$CODEX_HOME/skills/"
cp -R skills/investigate "$CODEX_HOME/skills/"
cp -R skills/review "$CODEX_HOME/skills/"
cp -R skills/qa-only "$CODEX_HOME/skills/"
cp -R skills/query "$CODEX_HOME/skills/"
cp -R skills/ingest "$CODEX_HOME/skills/"
cp -R skills/enrich "$CODEX_HOME/skills/"
cp -R skills/brain-ops "$CODEX_HOME/skills/"
cp -R skills/capture "$CODEX_HOME/skills/"
cp -R skills/brain-taxonomist "$CODEX_HOME/skills/"
cp -R skills/setup-gbrain "$CODEX_HOME/skills/"
cp -R skills/sync-gbrain "$CODEX_HOME/skills/"
cp -R skills/scrape "$CODEX_HOME/skills/"
cp -R skills/skillify "$CODEX_HOME/skills/"
cp -R skills/skillpack-check "$CODEX_HOME/skills/"
cp -R skills/responsible-design-review "$CODEX_HOME/skills/"
cp -R skills/accessibility-review "$CODEX_HOME/skills/"
cp -R skills/research-synthesis "$CODEX_HOME/skills/"
cp -R skills/startup-memo "$CODEX_HOME/skills/"
cp -R skills/market-map "$CODEX_HOME/skills/"
cp -R skills/design-leadership-review "$CODEX_HOME/skills/"
cp -R skills/outcome-memory "$CODEX_HOME/skills/"
cp -R skills/signal-detector "$CODEX_HOME/skills/"
cp -R skills/cron-scheduler "$CODEX_HOME/skills/"
cp -R skills/testing "$CODEX_HOME/skills/"
cp -R skills/workflow-router "$CODEX_HOME/skills/"
```

Examples:

- Use `$office-hours` when an idea is still fuzzy and needs better framing.
- Use `$autoplan` when you want one pass over the current planning stack.
- Use `$investigate` before speculative debugging changes.
- Use `$qa-only` when you want a report without code changes.
- Use `$query` to search the local brain corpus.
- Use `$setup-gbrain` and `$sync-gbrain` to verify or refresh the local brain substrate.
- Use `$capture` when the user says to remember or save a thought.
- Use `$brain-taxonomist`, `$schema-author`, and `$frontmatter-guard` to keep local brain pages filed and structured cleanly.
- Use `$skillpack-check` or `$smoke-test` after upgrades and restarts.
- Use `$scrape` for read-only data extraction and `$skillify` when a repeated flow should become a reusable skill.
- Use `$responsible-design-review`, `$accessibility-review`, and `$design-leadership-review` when quality depends on ethics, inclusion, and executive design judgment.
- Use `$startup-memo`, `$market-map`, and `$research-synthesis` when founder judgment needs stronger evidence and market context.
- Use `$outcome-memory` when a prior recommendation should update future judgment.
- Use `$ingest`, `$idea-ingest`, or `$meeting-ingestion` to turn files into durable brain pages.
- Use `$brain-ops` before outside research when local memory should shape the answer.
- Use `$signal-detector` to capture the user's own phrasing into `brain/originals/` or `brain/ideas/`.
- Use `$citation-fixer` for citation audits.
- Use `$cron-scheduler` for recurring Codex automations.
- Or just ask naturally and let `$workflow-router` choose the right skill flow.

## Checks

```bash
python3 scripts/validate_repo.py
python3 -m unittest discover -s tests
python3 scripts/brain_doctor.py
python3 scripts/print_status.py
```

For GStack/GBrain portwork or install refreshes, also check the installed Codex version and current official Codex manual before deciding whether older fallbacks still belong:

```bash
codex --version
node /Users/praneet/.codex/skills/.system/openai-docs/scripts/fetch-codex-manual.mjs
```

## Upstream Sources

- GStack baseline source pin: `2aa745cb0e4331d683e727ec77385d04cdbb45a2`; May refresh entries use `cf50443b63e461a7c0796857f69d572781acab8e`; June 26 router/diagram/spec entries use `11de390be1be6849eb9a15f91ff4922dd16c589a`.
- GBrain baseline source pin: `b7e3005b5b3f1b54082f9c5990482ebf81a4a807`; May refresh entries use `32f8be96c2409b8ccd35b7835692fd56b640f5c4`; June 26 advisor/upgrade/lineage/schema/optimizer entries use `814258dda67945ffec9457a1e73980e947b7e462`.

The baseline pins stay intentionally conservative so `scripts/check_upstream_drift.py` continues to reveal upstream runtime drift instead of claiming full parity after a partial Codex-native refresh.

## Most Adapted GBrain Ports

These are ported, but their upstream ambient/runtime behavior is intentionally rewritten around local files and explicit invocation:

- `brain-ops`
- `capture`
- `brain-taxonomist`
- `schema-author`
- `frontmatter-guard`
- `signal-detector`
- `idea-ingest`
- `media-ingest`
- `meeting-ingestion`
- `citation-fixer`
- `webhook-transforms`
- `frontmatter-guard`
- `schema-author`
