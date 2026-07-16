# Project Context

Use the project's live files as the authority.

## Load order

1. Existing product, brief, research, or requirements document.
2. Root `PRODUCT.md` when present.
3. Root `DESIGN.md` when present.
4. Existing tokens, theme, representative component, and route or screen source.
5. Current rendered evidence when available.

A scoped change to an existing interface can proceed from code and rendered evidence when `PRODUCT.md` or `DESIGN.md` is absent. Mention the missing context once and continue.

## Register

Classify the target by its primary job:

- `brand`: marketing, campaign, editorial, portfolio, or identity-bearing surfaces
- `product`: application UI, dashboard, settings, forms, tools, and operational workflows
- `native`: iOS, Android, or adaptive application surfaces

## PRODUCT.md minimum

When the user wants durable context, capture:

- register and platform
- users and primary job
- product purpose
- brand personality or interaction tone
- anti-references
- design principles
- accessibility and inclusion commitments

## DESIGN.md minimum

Capture the current system with evidence:

- design thesis and constraints
- color roles and tokens
- typography hierarchy
- spacing, layout, elevation, and motion rules
- component vocabulary and state behavior
- accessibility requirements
- approved exceptions and anti-goals
- source files and observed date

Use machine-readable token values only when they are recoverable from code. Label proposed values as proposals.
