# Runtime Strategy

## Choose The Best Available Path

1. Codex in-app Browser / `@Browser` for local dev servers, file-backed previews, public unauthenticated pages, rendered-page inspection, screenshots, and ordinary click/type flows.
2. Codex Chrome extension / `@Chrome` for signed-in websites, Chrome-profile state, browser extensions, existing tabs, or workflows that need the user's real browser context.
3. Computer Use when the work depends on a desktop app, OS UI, native simulator/app window, or browser task that cannot be reached through Browser or Chrome tooling.
4. Repo-local Playwright, Cypress, or app-specific browser helpers when the target repo already includes scripts, dependencies, and fixtures for them.
5. Browser screenshots plus manual guidance.
6. HTTP-only fallback with explicit limitations.

## Current Codex Host Notes

- Prefer `@Browser` for local/public unauthenticated web QA.
- Prefer `@Chrome` when authentication, browser profile state, or extensions matter.
- Prefer Computer Use for GUI workflows outside the browser-tool surface.
- Use Browser Developer mode or full CDP access only when it is enabled and explicitly approved for the target site.
- Prefer repo-local Playwright only when the target app already has dependencies, scripts, or fixtures for it.
- Do not import upstream GStack's browser daemon into this repo just to run one QA pass.
- If no browser tool is available, say so and downgrade the evidence claim.

## Local App Detection

When testing a local app:

- check the repo docs or dev scripts for the expected port
- verify the app is actually running before claiming QA coverage

## Session And State

- Treat in-app Browser sessions as unauthenticated unless the environment proves otherwise.
- Use Chrome when persistent signed-in browser state is the point of the test.
- If not, note that each interaction may be stateless and plan the test accordingly.

## Blockers To Report Explicitly

- browser runtime unavailable
- local app not running
- auth required but no viable session path
- no way to capture evidence in the current environment
