# Adoption Examples

These examples show the intended difference between the stable core and the runtime-aware layer.

## Example 1: Stable Core With `plan-ceo-review`

Use this when you want immediate value from the repo with no extra host setup.

### User request

```text
/plan-ceo-review
Review our plan to add branch-based preview deployments to the app. We want founder-style feedback before coding.
```

### Expected Codex behavior

- Detect `plan-ceo-review` and open `skills/plan-ceo-review/SKILL.md`
- Choose a review mode based on the user intent
- Read only the plan docs or code needed for context
- Deliver a concrete review with problem framing, what already exists, recommended plan, risks, not in scope, and next actions

### Why this is stable

- No browser or session runtime is required
- The main dependencies are repository context and the Codex skill system itself
- The output contract is fully captured in the ported skill and references

## Example 2: Runtime-Aware QA With Partial Tooling

Use this when you want the QA workflow, but the host Codex environment may or may not have browser automation.

### User request

```text
Use $qa on this feature branch and give me a diff-aware report for the settings flow.
```

### Expected Codex behavior

1. Open `skills/qa/SKILL.md` and follow the diff-aware flow.
2. Check the branch diff to infer the most likely affected pages or routes.
3. Choose the best available browser path using `skills/browse/SKILL.md`.
4. If full browser automation exists, test the changed surface and gather screenshots.
5. If only partial tooling exists, fall back to HTTP checks, screenshots, or manual evidence and state the blind spots explicitly.
6. Write the report using `skills/qa/templates/qa-report-template.md`.

### Honest success criteria

- The workflow still applies even when runtime support is limited.
- The report must say what was tested, what evidence was collected, and what remained unverified.
- The skill should never claim full parity with upstream gstack if browser execution was unavailable.

## Example 3: Starter Brain Backfill

Use this when you want to pressure-test the new GBrain layer against real material instead of just validating the package structure.

### User request

```text
Seed the local brain with a small real corpus and prove that query, signal capture, meeting ingestion, and source ingest all work together.
```

### Recommended first tranche

1. Ingest 5-10 real artifacts:
   - one meeting note or transcript
   - one memo, article, or research note
   - one report or status update
   - one idea note in the user's own phrasing
   - one webhook-style JSON payload
2. Run the helpers:
   - `python3 scripts/brain_ingest_meeting.py ...`
   - `python3 scripts/brain_ingest_source.py ...`
   - `python3 scripts/brain_capture_signal.py ...`
   - `python3 scripts/brain_transform_event.py ...`
   - `python3 scripts/brain_citations.py --fix --verbose`
3. Verify the outputs:
   - `python3 scripts/brain_search.py "<query>"`
   - `python3 scripts/brain_doctor.py`
4. Write one short demo walkthrough showing:
   - what was ingested
   - which pages were created or updated
   - which backlinks and citations were added
   - what still felt awkward

### Why this should be next

- It turns the current port from package parity into lived usage.
- It will surface the real rough edges in the ingest and memory workflow faster than more abstract planning.
- It gives future contributors a concrete example corpus and validation story.

## Adoption Guidance

- Adopt the stable core first if your goal is immediate team-wide reuse.
- Add the runtime-aware skills when your Codex environment already has browser or session tooling, or when explicit limitations are acceptable.
- Use `docs/runtime-compatibility.md` alongside these examples when deciding whether a runtime-aware skill is ready for your environment.
- For this repo specifically, the highest-value next tranche is the starter-brain backfill above.
