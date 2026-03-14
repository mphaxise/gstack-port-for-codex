# Runtime Strategy

## Choose The Best Available Path

1. Repo-local browser automation or Playwright tooling
2. Host-provided Codex browser automation
3. Browser screenshots plus manual guidance
4. HTTP-only fallback with explicit limitations

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

