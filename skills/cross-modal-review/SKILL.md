---
name: cross-modal-review
description: GBrain-inspired second-pass review for Codex. Use when the user wants another perspective, a quality gate, or a deliberate re-check before finalizing work.
---

# Cross-Modal Review

Use this skill when the user wants a second-pass review of a draft, decision, or artifact before finalizing it.

This port is adapted from `garrytan/gbrain` at commit `b7e3005b5b3f1b54082f9c5990482ebf81a4a807`.

## Important Adaptation

Upstream GBrain assumes an explicit second-model routing chain. In Codex, the equivalent is a deliberate second-pass review against the originating workflow's contract, often using:

- the existing `review` skill
- a separate verification pass
- a restated quality bar before final output

## Workflow

1. Capture the work to review.
2. Restate the contract or quality bar it was meant to satisfy.
3. Re-check the work from a different angle:
   - correctness
   - missing edge cases
   - contract fit
   - clarity
4. Report agreement and disagreement explicitly.

## Guardrails

- Do not auto-apply review changes without deciding them explicitly.
- Review against promises and requirements, not just vague taste.
- Keep the second pass meaningfully different from the first.
