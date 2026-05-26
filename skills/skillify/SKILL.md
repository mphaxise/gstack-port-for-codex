---
name: skillify
description: Turn a proven workflow, scrape, or repeated task into a durable Codex skill with tests or validation notes.
---

# Skillify

Use this skill when the user asks to codify a workflow into a reusable skill.

This skill covers both upstream GStack's scrape-to-browser-skill flow and GBrain's broader meta-skill pattern.

## Workflow

1. Identify the proven workflow:
   - trigger language
   - required tools
   - ordered steps
   - inputs and outputs
   - guardrails
2. Decide whether it belongs in:
   - `skills/`
   - a plugin or app skill
   - documentation only
3. Create a concise `SKILL.md` with frontmatter and operational steps.
4. Update registries or routing when this repo owns the skill.
5. Add a validation path or smoke test.

## Guardrails

- Do not skillify a workflow that has not worked at least once.
- Keep skills short and executable.
- Do not encode secrets, private URLs, or brittle session state.
