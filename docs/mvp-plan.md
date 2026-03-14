# MVP Plan

## MVP Definition

The first vertical slice is complete when this repo proves the porting model works end to end:

- the idea and product intent are documented
- the upstream surface area is mapped
- one skill is ported in native Codex form
- checks verify the structure

## 60-90 Minute First Milestone

### Minute 0-20

- Read source backlog files and extract the idea context
- Inspect upstream gstack structure
- Lock the initial repo layout and the first reference skill

### Minute 20-45

- Write `README.md`
- Create the required strategy docs
- Publish `docs/compatibility-map.md`
- Create `data/skill-map.json`

### Minute 45-70

- Port `plan-ceo-review`
- Split the port into concise skill guidance plus references
- Add attribution and source pinning

### Minute 70-90

- Add validator and status scripts
- Add tests
- Run checks
- Commit in logical slices

## Acceptance Criteria

- `README.md` clearly explains the repo, source, MVP, and next steps
- All requested docs exist and include problem statement, target users, scope, risks, architecture, first milestone, and end-of-day outcome
- One skill exists under `skills/` and validates cleanly
- `python3 scripts/validate_repo.py` passes
- `python3 -m unittest discover -s tests` passes

## Scope: MVP Vs Later

### MVP

- One reference port
- Full compatibility inventory
- Lightweight validation
- Public-ready docs

### Later

- More skill ports
- Import helpers
- CI workflow
- Upstream diffing and parity tracking

## Risks And Assumptions

- Assumption: one excellent port beats several shallow ones.
- Risk: contributor expectations may drift unless the registry and docs stay aligned.
- Risk: browser tooling ports will require separate design work.

## End-Of-Day Outcome

The repo can be published as a credible starting point for a public community porting effort rather than a private sketchpad.

