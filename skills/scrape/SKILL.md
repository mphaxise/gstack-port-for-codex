---
name: scrape
description: Extract structured data from a web page using browser evidence, returning JSON and a repeatable flow.
---

# Scrape

Use this skill when the user asks to pull data from a page, table, listing, or web app.

## Workflow

1. Clarify the target URL and desired fields if not obvious.
2. Use browser or web tooling to inspect the page.
3. Extract only the requested data.
4. Return JSON or a table with source notes.
5. If the flow is useful and repeated, suggest `skillify` to preserve it as a reusable browser skill.

## Guardrails

- Treat scraping as read-only.
- Respect authentication boundaries and site terms.
- Do not fabricate missing fields.
- Include selectors, URLs, or evidence notes when the extraction may need to be repeated.
