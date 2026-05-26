---
name: workflow-router
description: Natural-language router for this repo's GStack and GBrain skillpack. Use when the user asks for help in or about this repo without naming a skill, and you should infer the right 1-3 skills and apply them automatically.
---

# Workflow Router

Use this skill when the user speaks naturally and should not have to remember the exact skill names.

This router is repo-local. Its job is to translate a plain-English request into the smallest useful combination of installed skills.

Read `references/intent-map.md` before routing if the match is not obvious.

## Workflow

1. Classify the request by intent:
   - planning
   - engineering design
   - brain lookup
   - signal capture
   - brain setup or sync
   - brain taxonomy or schema
   - source or meeting ingest
   - maintenance or testing
   - browser QA
   - automation
   - review or ship
   - publishing or reporting
2. Pick the smallest useful set of skills:
   - usually one skill
   - sometimes two in sequence
   - rarely three if there is a natural pipeline
3. Tell the user briefly which skill(s) you are using.
4. Execute the chosen skill workflow instead of asking the user to reformulate the request.

## Default Routing Rules

- If one specific skill clearly fits, use that skill and skip extra routing overhead.
- If the user asks for founder-style or scope pressure-testing, use `plan-ceo-review`.
- If the user is still brainstorming, validating whether to build something, or shaping a pre-plan idea, use `office-hours`.
- If the user wants the planning stack run in one pass, use `autoplan`.
- If the product direction is chosen and architecture or execution rigor is needed, use `plan-eng-review`.
- If the user wants pre-implementation design critique, use `plan-design-review`.
- If the user wants pre-implementation developer-experience critique, use `plan-devex-review`.
- If the user wants live visual polish or a design audit, use `design-review`.
- If the user wants a stronger design system or visual direction, use `design-consultation`.
- If the user wants multiple design directions, use `design-shotgun`.
- If the user wants a design turned into code, use `design-html`.
- If the user wants a real onboarding or docs audit for developers, use `devex-review`.
- If the user wants memory-grounded answers, use `query` or `brain-ops`.
- If the user wants to set up or refresh GBrain, use `setup-gbrain` or `sync-gbrain`.
- If the user wants something saved into the brain, use `capture`, then `brain-taxonomist` if the filing target is unclear.
- If the user wants a specialized ingest, use `signal-detector`, `ingest`, `idea-ingest`, `media-ingest`, or `meeting-ingestion` based on the artifact.
- If the user wants to change where brain pages belong, use `schema-author` after `brain-taxonomist`.
- If the user wants recurring work, use `cron-scheduler`.
- If the user is debugging or asking why something broke, use `investigate`.
- If the user wants pre-landing scrutiny, use `review`.
- If the user wants to push and open a PR, use `ship` after `review`.
- If the user wants to merge and verify production, use `land-and-deploy`.
- If the user wants a documentation sync after shipping, use `document-release`.
- If the user wants QA or browser verification, use `qa` and `browse`.
- If the user wants report-only QA, use `qa-only`.
- If the user wants a security audit, use `cso`.
- If the user wants to save or resume working state, use `context-save` or `context-restore`; use `checkpoint` only for legacy compatibility.
- If the user wants repo or corpus health, use `health`, `maintain`, or `testing`.

## Guardrails

- Do not ask the user to memorize skill keywords.
- Do not route to multiple skills when one will do.
- Do not claim a skill was used if you only borrowed the idea.
- If no installed skill meaningfully helps, proceed normally instead of forcing a bad match.
