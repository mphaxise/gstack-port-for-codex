# Browser Command Map

Map the upstream browse concepts to the best available Codex action.

| Upstream concept | Intent | Codex adaptation |
| --- | --- | --- |
| `goto` | navigate to a page | use `@Browser` for local/public pages, `@Chrome` for signed-in pages, or repo-local browser tooling when it owns the target flow |
| `snapshot` | inspect current page structure | use Browser/Chrome DOM or accessibility inspection when available; otherwise use annotated screenshots |
| `click`, `fill`, `select`, `press` | interact with page elements | use Browser/Chrome automation when available; otherwise explain the limitation |
| `console`, `network` | inspect runtime issues | use Browser Developer mode/CDP only when enabled and approved; otherwise use app logs or repo-local test output |
| `screenshot`, `responsive` | capture visual evidence | use Browser/Chrome screenshots when available; otherwise use host screenshot tooling or explicit manual evidence |
| `cookies`, `storage` | inspect session/browser state | prefer Chrome for signed-in browser state; use app-supported test sessions or repo-local debug helpers before raw cookie handling |
| `diff` | compare environments or before/after state | use snapshots, screenshots, or text diffs depending on the tools available |

## Tool Preference

Use documented Codex surfaces before upstream GStack command names. Translate upstream commands into intent, not literal shell invocations.

## Evidence Standard

For any meaningful bug report or QA result, try to capture:

- target URL or page identity
- action taken
- resulting state
- screenshot or equivalent evidence
- any runtime errors seen
