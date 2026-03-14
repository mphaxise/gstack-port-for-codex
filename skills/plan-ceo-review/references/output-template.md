# Output Template

Use this structure for the final review.

## 1. Mode

- State the selected mode and one-sentence reason.

## 2. Problem Framing

- What problem is actually being solved?
- What happens if the team does nothing?
- Is the current framing the direct path to the real outcome?

## 3. What Already Exists

- List any code, docs, workflows, or product behavior that already solve part of the request.
- Call out duplication risk if the plan would rebuild something that already works.

## 4. Recommended Plan

- Present the best path in priority order.
- Keep it concise and actionable.
- Use an ASCII diagram when the flow is non-trivial.

Suggested diagram shape:

```text
current state -> proposed delta -> near-term outcome
```

## 5. Risks And Failure Modes

Use a small table for the most important risks:

```text
RISK | WHY IT MATTERS | MITIGATION
-----|----------------|-----------
```

## 6. Not In Scope

- Name the major items you are explicitly deferring.
- Give a one-line reason for each deferment.

## 7. Next Actions

- End with the next 1-3 concrete actions.

