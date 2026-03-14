# Session Options

Choose the best available option in this order:

## 1. Browser Importer

Use a repo-local or host-provided browser cookie importer if one exists.

Best when:

- the environment can safely read browser profiles
- the user wants parity with their real browser session

## 2. Cookie JSON Import

Import an exported cookie jar if the browser tooling supports it.

Best when:

- the user already has a cookie export
- browser-profile access is not available

## 3. Manual Login In Automation Session

Log in directly in the test browser session.

Best when:

- the site has normal sign-in flows
- the user can provide credentials or test-user access

## 4. App-Specific Session Seeding

Use app-supported test helpers, dev login routes, or seeded sessions when they exist.

Best when:

- the repo has safe local-only auth shortcuts
- browser-level import is unavailable

## Verification

Confirm success by checking:

- authenticated page access
- presence of expected session state
- domain-level cookie counts or session metadata, never cookie values

