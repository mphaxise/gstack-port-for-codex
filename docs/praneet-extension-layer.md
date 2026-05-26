# Praneet Extension Layer

The Praneet extension layer sits on top of the upstream GStack and GBrain parity surface.

It is intentionally tracked separately in `data/praneet-skill-map.json` so the repo can say two true things at once:

- upstream parity remains exact for Garry Tan's latest GStack and GBrain skill-name surfaces
- Praneet's local Codex install carries additional hand-port enhancements for design leadership, responsible design, social ethics, founder judgment, and outcome memory

## Skills

- `responsible-design-review`: human-impact review for autonomy, consent, dark patterns, vulnerable users, fairness, and data dignity
- `accessibility-review`: accessibility review for assistive technology paths, WCAG-oriented checks, cognitive load, motion, language, and inclusive use
- `research-synthesis`: decision-ready synthesis with evidence grading, participant bias checks, quotes-to-insights traceability, and unknowns
- `startup-memo`: founder and startup judgment memo that includes market, product, distribution, traction, risks, ethics, and diligence questions
- `market-map`: category, competitor, wedge, buyer, timing, and social-impact mapping
- `design-leadership-review`: CDO-level review for principles, quality bar, critique cadence, organizational implications, stakeholder alignment, and decision records
- `outcome-memory`: learning loop that records whether prior recommendations worked, failed, or need revised judgment

## Design Leadership Lens

These skills are not generic review prompts. They are meant to make the port more useful for Praneet as a design-minded operator:

- user agency matters alongside speed
- accessibility is a first-class quality bar
- design decisions should leave durable records
- market judgment should include social consequences
- research claims should carry confidence and source quality
- prior recommendations should teach future judgment

## Routing

`workflow-router` routes natural-language requests into these skills when the user asks about responsible design, accessibility, market judgment, research synthesis, executive design review, or whether a prior recommendation worked.
