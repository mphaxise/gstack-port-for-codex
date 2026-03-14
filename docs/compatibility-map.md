# Compatibility Map

Pinned upstream source: `garrytan/gstack@2aa745cb0e4331d683e727ec77385d04cdbb45a2`

## Porting Rules

- Preserve the workflow intent and operating posture.
- Translate invocation from slash commands to Codex skill discovery.
- Remove Claude-specific update checks and runtime-only metadata.
- Favor concise `SKILL.md` files plus references over giant single-file prompts.
- Keep a machine-readable registry in sync with this table.

## Upstream To Codex Status

| Upstream gstack skill | Codex skill target | Status | Notes |
| --- | --- | --- | --- |
| `plan-ceo-review` | `plan-ceo-review` | ported | First reference port; adapted to Codex's ask-only-when-needed interaction model. |
| `plan-eng-review` | `plan-eng-review` | planned | Natural next port so strategy and execution review can pair together. |
| `review` | `review` | planned | Needs Codex-native diff-review output conventions. |
| `ship` | `ship` | planned | Needs safe git/push guidance tuned to Codex permissions. |
| `browse` | `browse` | planned | Depends on a Codex-native browser story; cannot be ported honestly as docs alone. |
| `qa` | `qa` | planned | Closely coupled to browser and diff-aware testing flows. |
| `setup-browser-cookies` | `setup-browser-cookies` | planned | Likely depends on platform-specific browser/session integration. |
| `retro` | `retro` | planned | Good candidate once repo-analysis conventions are stable. |

## Adaptation Notes

### Invocation

- Upstream: user enters `/plan-ceo-review`
- Codex: user names the skill, or the repo `AGENTS.md` directs Codex to use it when the request matches

### Questioning

- Upstream: heavily interactive `AskUserQuestion` flow
- Codex: make reasonable assumptions by default; ask one concise question only when ambiguity materially changes the recommendation

### Structure

- Upstream: very large single-file `SKILL.md`
- Codex port: concise `SKILL.md` with references for mode behavior and output structure

### Tooling

- Upstream: declares Claude-specific tools and update checks
- Codex port: omits runtime-only tool declarations and keeps the skill focused on workflow guidance

