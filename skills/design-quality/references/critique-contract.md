# Critique Contract

Run two evidence passes and synthesize them.

## Pass A: unanchored design judgment

Inspect the rendered interface and source before reading detector findings. Evaluate hierarchy, information architecture, interaction clarity, cognitive load, emotional fit, responsiveness, accessibility, states, copy, and product-specific character.

## Pass B: technical and deterministic evidence

Run the Impeccable detector when installed. Inspect source, browser behavior, console output, tests, and accessibility evidence. Record skipped paths and exact reasons.

Use independent subagents only when the user has authorized delegation. Otherwise, run the two passes sequentially and state the method.

## Synthesis

Report:

- method and target
- strongest current choices
- priority findings with P0 to P3 severity
- agreement and disagreement between judgment and deterministic evidence
- false positives or justified exceptions
- recommended local skill or Impeccable command
- verification gaps

When persistence is useful and authorized, save the report under `reports/design-reviews/` with a stable target slug, date, source commit, and evidence path. Read the latest report before a later polish pass and state whether the target improved, regressed, or changed scope.
