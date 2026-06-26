# Runtime Strategy

## Choose The Best Available Path

1. Host-provided Codex browser or Chrome tools when available in the current session.
2. Repo-local browser automation or Playwright tooling when the target repo already includes it.
3. Browser screenshots plus manual guidance.
4. HTTP-only fallback with explicit limitations.

## Current Codex Host Notes

- Prefer a visible host browser/Chrome tool for interactive flows, authentication, and visual verification.
- Prefer repo-local Playwright only when the target app already has dependencies, scripts, or fixtures for it.
- Do not import upstream GStack's browser daemon into this repo just to run one QA pass.
- If no browser tool is available, say so and downgrade the evidence claim.

## Local App Detection

When testing a local app:

- check the repo docs or dev scripts for the expected port
- verify the app is actually running before claiming QA coverage

## Session And State

- Prefer persistent browser sessions if the host tooling supports them.
- If not, note that each interaction may be stateless and plan the test accordingly.

## Blockers To Report Explicitly

- browser runtime unavailable
- local app not running
- auth required but no viable session path
- no way to capture evidence in the current environment
