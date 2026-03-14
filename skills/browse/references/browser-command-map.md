# Browser Command Map

Map the upstream browse concepts to the best available Codex action.

| Upstream concept | Intent | Codex adaptation |
| --- | --- | --- |
| `goto` | navigate to a page | use available browser automation or the closest host/browser tool |
| `snapshot` | inspect current page structure | use DOM/tree inspection, accessible tree tools, or annotated screenshots |
| `click`, `fill`, `select`, `press` | interact with page elements | use browser automation if available; otherwise explain the limitation |
| `console`, `network` | inspect runtime issues | use browser devtools integration, logs, or app-side logs if browser tools are unavailable |
| `screenshot`, `responsive` | capture visual evidence | take screenshots directly or use the host screenshot skill where appropriate |
| `cookies`, `storage` | inspect session/browser state | use browser tooling or repo-local debug helpers if available |
| `diff` | compare environments or before/after state | use snapshots, screenshots, or text diffs depending on the tools available |

## Evidence Standard

For any meaningful bug report or QA result, try to capture:

- target URL or page identity
- action taken
- resulting state
- screenshot or equivalent evidence
- any runtime errors seen

