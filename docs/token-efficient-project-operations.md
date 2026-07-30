# Token-Efficient Project Operations

Use this playbook for long-running Codex projects where context, review, QA, and iterative feedback can grow faster than the implementation itself. Preserve the project's quality and authority gates throughout.

## Start With A Compact Operating Packet

Record the goal, owning repository, authority boundary, acceptance criteria, source map, and first coherent slice. Establish deterministic checks and name the evidence needed to complete the slice.

Keep the initial packet small. Load broader context once during orientation, then replace repeated history reads with exact paths, narrow line windows, and current receipts.

## Work In Coherent Slices

Define one bounded outcome, a file or artifact allowlist, and a verification ladder for each slice. Complete the slice before expanding scope.

Record token and process telemetry when the host exposes direct evidence. Useful fields include token totals, context loads, compactions, correction passes, builds, review panels, and completed verification tiers. Mark unavailable values as unknown.

## Evolve The Context Strategy

During exploration, allow a wider source scan to discover the relevant system. At implementation, freeze the source map and prefer targeted reads. During review and QA, freeze one evidence package and identify every receipt by the inputs it covers.

As the project grows, use `context-save` to maintain an active packet of no more than 1,500 words. Use `context-restore` to validate that packet against current source. Reserve full-history reconstruction for a named gap that blocks safe continuation.

## Integrate Feedback In Coherent Batches

Use `feedback-integration` to classify new feedback as interrupt, batch, or record. Group batch items by one screen, interaction, component, or acceptance outcome. Apply one coherent correction pass, then verify it in tiers.

Interrupt active work only for a safety, privacy, data-loss, production, or blocking risk; an explicit instruction to act now; or a change that requires a new user decision.

## Review And Verify Once Per Stable Package

Give distinct reviewers the same frozen package and read-only authority. The controlling agent owns mutations, builds, runtime control, Git, and connected services.

After a correction, rerun only the checks and panels whose inputs changed. Finish with the required consolidated suite and one build or runtime pass after the package stabilizes. Expand coverage whenever the risk surface or product contract requires it.

## Reset At Meaningful Boundaries

Recommend a fresh task when direct evidence shows repeated oversized inputs, multiple compactions in one slice, a new risk class, a materially new outcome after acceptance, a second material correction, or an active packet that cannot stay within 1,500 words.

Carry forward the compact packet, source map, reusable receipts, invalidated evidence, and single next action. Leave the full history behind unless a named gap makes it necessary.
