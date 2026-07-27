# Model routing

## Selection rule

Choose the strongest task-suited model that fits the user's provider-cost
ceiling. Recent verified task evidence outweighs model size or reputation.
Record the classification and complete routing chain before starting an agent.

When the user sets no provider-cost ceiling, prefer a configured route whose
recent stored session cost is zero. Ask before using a route with a known
nonzero charge.

## Primary selection

| Assignment | Primary | Effort | Free fallback |
| --- | --- | --- | --- |
| Application code, JavaScript, TypeScript, APIs, tests, bug fixes | `nvidia/openai/gpt-oss-120b` | medium | `opencode/north-mini-code-free` |
| Visual CSS, responsive layout, design-system implementation | `nvidia/z-ai/glm-5.2` | high | `opencode/mimo-v2.5-free` |
| Compact semantic HTML or schema-constrained markup | `nvidia/stepfun-ai/step-3.7-flash` | minimal | `opencode/ling-3.0-flash-free` |
| Broad refactor or reasoning-heavy repository integration | `opencode/nemotron-3-ultra-free` | high | `opencode/north-mini-code-free` |
| Algorithmic or data-heavy code | `opencode/deepseek-v4-flash-free` | medium | `opencode/north-mini-code-free` |

Use GPT-OSS medium when an assignment spans several categories or lacks reliable
task-specific evidence.

`nvidia/nvidia/nemotron-3-ultra-550b-a55b` remains an opt-in primary for broad
reasoning work. A prior session recorded a nonzero provider cost, so require an
explicit cost allowance before selecting it.

## Bounded model canary

Use a canary when the work type is novel, at least three similar assignments
will follow, and model choice could materially affect quality or cost.

1. Select one small representative assignment with a deterministic evaluator.
2. Run at most two cost-compatible candidate models against the same commission.
3. Choose the higher-quality passing result. Break a tie with lower elapsed time
   and stored provider cost.
4. Use that winner for the remaining assignments of the same type.

Skip the canary when recent comparable evidence exists or its cost would exceed
the implementation it is meant to optimize.

## Fallback chain

1. Run the task-matched primary.
2. Retry once with the preselected free fallback after a qualifying provider
   failure.
3. Retry once with the exact installed Ollama model.

Keep the same commission, files, acceptance criteria, and correction budget
across tiers.

As observed on 2026-07-27, the local inventory contains
`ollama/qwen3.5:9b`. The requested Qwen Coder 3.5B model is absent. Re-run
`opencode models` and `ollama list` before relying on this snapshot.

## Routing cautions

- Treat missing-first-token failures as provider failures. Step 3.7 Flash
  exhibited this failure in a prior HTML assignment.
- Treat a claimed completion without the required file as an implementation
  failure. GPT-OSS produced this failure in a prior CSS assignment.
- Treat local-file WebFetch calls and malformed write-tool calls as runtime
  failures. The installed local Qwen model exhibited both.
- Use the evaluator and repository tests to judge output. Agent completion text
  cannot establish success.

## Failure signals

Fallback is allowed for:

- quota exhaustion or an explicit near-quota refusal
- rate limiting
- transient provider or 5xx failure
- timeout
- missing first token

An implementation defect is a correction case. Keep the current model when its
session remains healthy and issue one narrow evaluator-driven correction.

## Cost evidence

Capture stored session cost from OpenCode. A configured free route can still
change, so verify the provider ledger after every run. Report cache reads as
token traffic and keep them separate from Codex task tokens.
