# Codex Documentation Refresh

Latest verification: 2026-07-21
Installed Codex: `codex-cli 0.144.0`
Documentation access: the local manual helper could not resolve `developers.openai.com` during this port refresh. The last successful local manual review remains the July 16 refresh recorded below.
Resulting port decision: retain the documented Codex skill, approval, hook-trust, Browser, Chrome, Computer Use, automation, memory, and local-runtime boundaries. The GStack review required no update. GBrain's new upstream runtime work remains outside the file-backed port. The Impeccable bridge adopted only current guidance for project-scoped hooks and live-session recovery.

Latest verification: 2026-07-06
Installed Codex: `codex-cli 0.142.5`
Documentation access: the local manual helper failed to refresh the official manual on 2026-07-06 because `developers.openai.com` could not be resolved from this run. The most recent successful cached refresh remains the 2026-07-02 fetch via `/Users/praneet/.codex/skills/.system/openai-docs/scripts/fetch-codex-manual.mjs`.
Resulting port decision: no new runtime-surface changes were required for this weekly repo-health pass. With live docs unavailable, the pass relied on the installed Codex version plus the repo's existing checked-in Codex refresh notes and runtime docs; those still match the current local workflow boundaries for automations, approvals, skills, MCP, memories, and local/browser behavior.

Date: 2026-06-26
Installed Codex: `codex-cli 0.142.2`
Source: official Codex manual fetched with `/Users/praneet/.codex/skills/.system/openai-docs/scripts/fetch-codex-manual.mjs`

Runtime surface follow-up: 2026-06-27 with `codex-cli 0.142.3`; the official manual helper refreshed the local manual again before updating browser, automation, subagent, and runtime-compatibility guidance.

README and integration follow-up: 2026-07-15 with `codex-cli 0.144.0`; the official manual helper reported the local manual current. The review reconfirmed skills and `AGENTS.md` as durable instruction surfaces, explicit subagent delegation with inherited permissions, and host-specific browser, automation, plugin, and external-tool boundaries. No new runtime fallback was added. The public README was simplified around three separately tracked layers: upstream GStack ports, upstream GBrain adaptations, and Praneet-specific behavioral extensions.

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
- Runtime surface follow-up: Browser, Chrome extension, Computer Use, worktrees, local environments, and subagents were rechecked before the deeper runtime pass.

## Port Decisions

- Keep authoring in this repo's `skills/` tree and local installation through symlinks under `~/.codex/skills`; this remains valid because Codex supports symlinked skill folders.
- Do not replace the current local install with a plugin yet. The docs confirm plugins are the right future distribution shape when the package should bundle skills, apps, MCP configuration, or lifecycle hooks for other users.
- Add `AGENTS.md` as the persistent project instruction surface for future portwork.
- Continue to prefer current Codex host features over Claude Code fallbacks. Keep fallbacks only for host-variable browser tooling, upstream `gbrain` CLI presence, remote credentials, optional MCP servers, and private local brain artifacts.
- Treat memories as non-authoritative for port rules. Durable port instructions should live in `AGENTS.md`, skills, and docs.
- Prefer the documented Browser/Chrome/Computer Use ladder over generic "browser tooling" language in runtime-aware skills.
- Treat Codex subagents as explicit, bounded parallel-agent workflows, not as ambient or durable upstream GBrain minions.

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

## 2026-07-16 Upstream Drift Audit

Installed Codex: `codex-cli 0.144.0`. The official Codex manual helper completed successfully and reported its local manual current. The audit rechecked the documented `AGENTS.md`, skills, plugins, MCP, sandbox/approval, hooks, memories, automations, browser, and local/cloud-environment guidance.

The upstream-drift report now evaluates each skill against its own `source_commit` or the map's full-surface `skill_parity_commit`, while retaining the map-level pin for broad upstream-runtime visibility. This preserves the conservative baseline without falsely reporting files from before a later skill refresh as new skill drift. The full GStack and GBrain workflow surfaces were audited through `a325940` and `5008b28` respectively. No upstream browser-daemon code was ported because Codex's documented Browser, Chrome, and Computer Use surfaces remain the intended runtime boundary.

## 2026-07-16 Impeccable Integration

Installed Codex: `codex-cli 0.144.0`. The official manual helper refreshed successfully after the sandboxed DNS attempt failed. The review covered project skills, project hooks, hook trust, plugins, and worktree-backed scheduled tasks.

Resulting decisions:

- `skills/design-quality/` is the Codex-native orchestration and fallback layer.
- Impeccable's detector, project hooks, browser server, and live source-rewrite runtime remain optional external capabilities.
- Project hooks require explicit installation and `/hooks` trust review.
- The recurring Impeccable drift check runs against the local project so it can include ignored local-brain health. It remains report-only and reports three states separately: upstream movement, local review, and local adoption.
- The upstream map classifies explicit source paths because Impeccable uses one source skill plus references and runtime modules instead of one directory per command.
