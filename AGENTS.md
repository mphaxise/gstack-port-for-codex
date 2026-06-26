# GStack/GBrain Codex Port Guidance

## Codex Documentation Gate

Before any GStack or GBrain port, upgrade, install refresh, or runtime-compatibility claim, check the installed Codex version and the current official Codex documentation.

Use the local OpenAI docs skill/manual helper when available:

```bash
codex --version
node /Users/praneet/.codex/skills/.system/openai-docs/scripts/fetch-codex-manual.mjs
```

Review the manual sections relevant to the change, especially skills, plugins, MCP, AGENTS.md, sandboxing and approvals, hooks, memories, automations, browser behavior, and local/cloud environments. Prefer documented current Codex behavior over older Claude Code compatibility fallbacks. Keep fallbacks only where the current host, credentials, browser tools, upstream CLI, or external runtime is genuinely variable.

Record the documentation date, installed Codex version, and any resulting port decisions in `docs/codex-documentation-refresh.md` or the specific runtime/audit doc changed by the work.
