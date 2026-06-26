# Codex Documentation Refresh

Date: 2026-06-26
Installed Codex: `codex-cli 0.142.2`
Source: official Codex manual fetched with `/Users/praneet/.codex/skills/.system/openai-docs/scripts/fetch-codex-manual.mjs`

This note records the one-time Codex documentation refresh requested during the June 26 GStack/GBrain port work and turns it into a repeatable gate for future porting.

## Sections Checked

- Agent Skills: skills are first-class across Codex CLI, IDE extension, and app; skill discovery uses progressive disclosure; symlinked skill folders are supported; repo-scoped `.agents/skills` and plugin packaging are documented distribution options.
- Custom instructions with `AGENTS.md`: Codex reads global and project guidance before work, layering from global scope down to the current directory.
- Model Context Protocol: MCP servers are configured through Codex config, can be CLI-managed, and may also be bundled by plugins.
- Plugins: plugins are the distribution unit for reusable skills, apps, and MCP servers.
- Automations: automations can invoke skills, run in local projects or worktrees, and inherit sandbox behavior.
- Sandbox and approvals: workspace-write plus on-request approval remains the appropriate default shape for local port work; wider access should be explicit.
- Hooks: hooks are available but require trust review; they are not a replacement for checked-in port guidance.
- Memories: memories are a helpful recall layer, but required rules belong in `AGENTS.md` or checked-in documentation.

## Port Decisions

- Keep authoring in this repo's `skills/` tree and local installation through symlinks under `~/.codex/skills`; this remains valid because Codex supports symlinked skill folders.
- Do not replace the current local install with a plugin yet. The docs confirm plugins are the right future distribution shape when the package should bundle skills, apps, MCP configuration, or lifecycle hooks for other users.
- Add `AGENTS.md` as the persistent project instruction surface for future portwork.
- Continue to prefer current Codex host features over Claude Code fallbacks. Keep fallbacks only for host-variable browser tooling, upstream `gbrain` CLI presence, remote credentials, optional MCP servers, and private local brain artifacts.
- Treat memories as non-authoritative for port rules. Durable port instructions should live in `AGENTS.md`, skills, and docs.

## Future Port Checklist

1. Run `codex --version`.
2. Fetch the current Codex manual with the OpenAI docs helper.
3. Read the manual sections relevant to the change.
4. Update skills/docs when Codex now has a direct capability that replaces an older fallback.
5. Reinstall or verify symlinked local skills.
6. Run repo validation and tests.
7. Record the installed Codex version and documentation-driven decisions in this file or a targeted audit doc.

## Official Docs Links

- Agent Skills: https://developers.openai.com/codex/skills
- AGENTS.md: https://developers.openai.com/codex/guides/agents-md
- MCP: https://developers.openai.com/codex/mcp
- Plugins: https://developers.openai.com/codex/plugins
- Automations: https://developers.openai.com/codex/app/automations
- Sandboxing: https://developers.openai.com/codex/concepts/sandboxing
- Hooks: https://developers.openai.com/codex/hooks
- Memories: https://developers.openai.com/codex/memories
