# Session Options

Choose the best available option in this order:

## 1. Chrome Extension / Signed-In Browser State

Use the Codex Chrome extension / `@Chrome` when the task needs the user's real signed-in browser state.

Best when:

- the site requires an existing login
- browser extensions, profile state, existing tabs, or real account context matter
- the user is present to approve the website/action prompts

Do not use Chrome profile state for local/public unauthenticated QA when the in-app Browser is enough.

## 2. Manual Login In Browser Session

Log in directly in the selected browser session.

Best when:

- the site has a normal sign-in flow
- the user can provide credentials, OAuth approval, or test-user access
- the session can be verified without exposing secrets

## 3. App-Specific Session Seeding

Use app-supported test helpers, dev login routes, or seeded sessions when they exist.

Best when:

- the repo has safe local-only auth shortcuts
- the test is against a local development server
- browser-level login would be noisy or brittle

## 4. Cookie JSON Import

Import a user-provided exported cookie jar only when the browser tooling supports it and safer options are unavailable.

Best when:

- the user already has a cookie export
- Chrome extension state and manual login are not viable
- the values can be handled without printing or committing them

## 5. Browser Importer Or Profile Reader

Use a repo-local or host-provided browser cookie importer only if one already exists and the user explicitly accepts the security tradeoff.

Do not install upstream GStack browser import machinery as an implicit side effect. Treat importer availability as a current-host capability.

## Verification

Confirm success by checking:

- authenticated page access
- presence of expected session state
- domain-level cookie counts or session metadata, never cookie values
