# Intent Map

Use this table when a natural-language request could map to several skills.

| User intent | Default skill | Optional follow-on |
| --- | --- | --- |
| "Pressure-test this idea or plan" | `plan-ceo-review` | `plan-eng-review` |
| "I have an idea" or "Is this worth building?" | `office-hours` | `plan-ceo-review` |
| "Run the planning stack for me" | `autoplan` | none |
| "How should we build this?" | `plan-eng-review` | `testing` |
| "Critique the design before we build it" | `plan-design-review` | `plan-eng-review` |
| "Review this for responsible design or ethics" | `responsible-design-review` | `accessibility-review` |
| "Review accessibility" | `accessibility-review` | `design-review` |
| "Run a CDO-level design leadership review" | `design-leadership-review` | `responsible-design-review` |
| "Critique the developer experience before we build it" | `plan-devex-review` | `plan-eng-review` |
| "Why is this broken?" or "Debug this" | `investigate` | `review` |
| "Audit the live design" | `design-review` | `qa` |
| "QA this iOS app" | `ios-qa` | `ios-fix` |
| "Fix this iOS bug" | `ios-fix` | `ios-qa` |
| "Review this iOS design" | `ios-design-review` | `ios-fix` |
| "Refresh iOS debug bridge" | `ios-sync` | `ios-qa` |
| "Remove iOS debug bridge" | `ios-clean` | none |
| "Audit the onboarding or docs flow" | `devex-review` | `investigate` |
| "Create a design system or visual direction" | `design-consultation` | `design-shotgun` |
| "Show me several design options" | `design-shotgun` | `design-html` |
| "Turn this design into code" | `design-html` | `design-review` |
| "What do we already know about X?" | `query` | `brain-ops` |
| "Set up GBrain for this repo" | `setup-gbrain` | `sync-gbrain` |
| "Refresh or re-index the brain" | `sync-gbrain` | `frontmatter-guard` |
| "Save this thought or thesis" | `capture` | `brain-taxonomist` |
| "Where should this brain page go?" | `brain-taxonomist` | `schema-author` |
| "Change the brain schema or page types" | `schema-author` | `frontmatter-guard` |
| "Validate brain frontmatter" | `frontmatter-guard` | `citation-fixer` |
| "Save this memo, link, or source" | `idea-ingest` | `citation-fixer` |
| "Enrich this article" | `article-enrichment` | `citation-fixer` |
| "Verify this paper or claim" | `academic-verify` | `perplexity-research` |
| "Research this with current sources" | `perplexity-research` | `capture` |
| "Synthesize this research" | `research-synthesis` | `responsible-design-review` |
| "Write a startup or founder memo" | `startup-memo` | `market-map` |
| "Map this market" | `market-map` | `research-synthesis` |
| "Synthesize these concepts" | `concept-synthesis` | `brain-taxonomist` |
| "Read this strategically" | `strategic-reading` | `query` |
| "Ingest this voice note" | `voice-note-ingest` | `capture` |
| "Crawl this archive" | `archive-crawler` | `media-ingest` |
| "Make a PDF from this brain page" | `brain-pdf` | `make-pdf` |
| "Process this meeting note or transcript" | `meeting-ingestion` | `enrich` |
| "Process this PDF, screenshot, or transcript-like artifact" | `media-ingest` | `enrich` |
| "Set up a recurring reminder or repo job" | `cron-scheduler` | none |
| "Review this branch before it lands" | `review` | `ship` |
| "Push this and open a PR" | `ship` | none |
| "Merge and verify production" | `land-and-deploy` | `canary` |
| "Update docs after shipping" | `document-release` | `publish` |
| "Generate missing documentation" | `document-generate` | `document-release` |
| "Make a PDF" | `make-pdf` | none |
| "Show the landing queue" | `landing-report` | none |
| "Test this flow in the browser" | `qa` | `browse` |
| "Scrape this page" | `scrape` | `skillify` |
| "Test this but don't fix anything" | `qa-only` | none |
| "Run a security audit" | `cso` | `review` |
| "Run a repo or brain health pass" | `health` | `maintain` |
| "Check the skillpack" | `skillpack-check` | `smoke-test` |
| "Smoke test after restart" | `smoke-test` | `skillpack-check` |
| "Organize everything from this session" | `eiirp` | `reports` |
| "Did our previous recommendation work?" | `outcome-memory` | `retro` |
| "Generate missing documentation" | `document-generate` | `document-release` |
| "Save progress so we can resume later" | `context-save` | `reports` |
| "Resume where we left off" | `context-restore` | `query` |
| "Produce or publish a report" | `reports` | `publish` |

## Selection Notes

- Prefer the first skill alone when it fully covers the request.
- Add the follow-on skill only when the task naturally moves into that second stage.
- If the user explicitly names a skill, honor that instead of overriding it with this map.
