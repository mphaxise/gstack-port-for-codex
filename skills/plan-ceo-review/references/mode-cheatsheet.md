# Mode Cheatsheet

## Default Modes

- Choose `SCOPE EXPANSION` for greenfield ideas, repositioning work, or requests that hint at "what is the best version of this?"
- Choose `HOLD SCOPE` for bug fixes, refactors, execution plans, or when the user already committed to a direction.
- Choose `SCOPE REDUCTION` for MVP, same-day shipping, rescue, or "what is the thinnest version that still works?"

## Choose Or Ask

- If one mode is clearly right, choose it and explicitly confirm the choice in the response.
- If two modes are plausibly right and would lead to materially different advice, ask one concise question and wait.
- Do not blend modes or continue with a fuzzy "somewhere between" answer.

## Behavior By Mode

### SCOPE EXPANSION

- push on the premise before polishing details
- describe the 12-month ideal and whether the current plan moves toward it
- look for adjacent improvements that materially increase product value
- if the expanded framing is clearly stronger, recommend it directly and explain the tradeoff

### HOLD SCOPE

- assume the scope is directionally right
- tighten architecture, dependencies, risks, and acceptance criteria
- focus on making the chosen plan more robust, not bigger

### SCOPE REDUCTION

- cut aggressively to the smallest credible version
- separate "must ship together" from "follow-up work"
- favor clarity, sequence, and reversibility over completeness

## When To Ask A Question

Ask a concise question only if one of these is true:

- the mode is genuinely ambiguous and changes the recommendation
- the user intent is split between two materially different product outcomes
- in `SCOPE EXPANSION`, there are multiple credible bigger bets and the wrong one would waste the review
- a hidden constraint such as deadline, audience, or deployment target would change the plan substantially

Otherwise, choose the best mode yourself and say what you assumed.
