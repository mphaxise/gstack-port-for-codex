---
name: make-pdf
description: Convert markdown or brain pages into a polished PDF using available local document tooling.
---

# Make PDF

Use this skill when the user asks to turn markdown, a report, or a brain page into a PDF.

## Workflow

1. Identify the source markdown file.
2. Check whether it is a brain page with YAML frontmatter; if so, preserve the source and strip frontmatter only for rendering.
3. Choose the best available renderer:
   - upstream `gstack make-pdf` if installed
   - Pandoc, browser print, or repo-local tooling if available
4. Render with readable margins, page numbers, links, and a table of contents when appropriate.
5. Verify the output file exists and report the path.

## Guardrails

- Do not mutate the source markdown to make the PDF.
- Do not invent a PDF path if rendering failed.
- Mark drafts clearly when the source is draft content.
