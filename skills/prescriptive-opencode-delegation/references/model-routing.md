# Model routing

## Selection rule

Choose the strongest task-suited model that fits the user's provider-cost
ceiling. Recent verified task evidence outweighs model size or reputation.
Record the classification and complete routing chain before starting an agent.

When the user sets no provider-cost ceiling, prefer a configured route whose
recent stored session cost is zero. Ask before using a route with a known
nonzero charge.

## Primary selection

| Assignment | Primary | Effort | Free fallback | Status |
| --- | --- | --- | --- |
| Three or more meaningful independent implementation units | `nvidia/openai/gpt-oss-120b` | medium | `opencode/north-mini-code-free` | Qualification-only |
| Compact schema batch | `nvidia/stepfun-ai/step-3.7-flash` | minimal | `opencode/ling-3.0-flash-free` | Evidence-only |
| Visual CSS or responsive layout | `nvidia/z-ai/glm-5.2` | high | matching configured `opencode/*-free` model | Qualification required |
| Broad refactor or reasoning-heavy integration | strongest available task-suited NVIDIA model | medium or high | `opencode/north-mini-code-free` | Qualification required |
| Algorithmic or data-heavy code | strongest available task-suited NVIDIA model | medium | `opencode/north-mini-code-free` | Qualification required |

Use GPT-OSS medium only for an isolated qualification trial when the whole task
clears the three-unit, stable-interface, deterministic-check, privacy, and 40%
projected-savings gates. The measured implementation evidence currently splits
the durable gates: one run delivered 98/100 quality with 84.0% direct-token
savings, while another reached full functional parity with 35.1% savings. Keep
the route experimental until one accepted run for the task class simultaneously
reaches full functional parity and 40% delivered savings.

GLM 5.2, Mistral Nemotron, Nemotron 3 Super, and Nemotron 3 Ultra have no
automatic task class. Step 3.7 Flash still needs a third passing qualification
and a real batch that clears the 40% delivered-savings gate. Require an
explicit cost allowance before any route with a known nonzero provider charge.

The live model inventory on 2026-07-30 still exposed GPT-OSS 120B, GLM 5.2,
Step 3.7 Flash, Mistral Nemotron, Nemotron 3 Super, Nemotron 3 Ultra, the named
free fallbacks, and local Qwen 3.5 9B. Catalog presence establishes availability
for qualification and does not establish an automatic route.

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
2. Retry once with the preselected matching free fallback after a qualifying
   provider failure. Use an isolated canary when that fallback lacks comparable
   task evidence.
3. Retry once with the exact installed Ollama model only when that model has
   passed the same task-class qualification.
4. Return the task to Codex when no qualified fallback remains.

Keep the same commission, files, acceptance criteria, and correction budget
across tiers.

As observed again on 2026-07-30, the local inventory contains
`ollama/qwen3.5:9b`. The requested Qwen Coder 3.5B model is absent. Re-run
`opencode models` and `ollama list` before relying on this snapshot.

The July 28 qualification found that `ollama/qwen3.5:9b` failed exact extraction
and a resumed correction. It remains disabled for autonomous coding, testing,
mapping, review, and extraction until a model, runtime, or prompt-wrapper
upgrade passes a fresh read-only qualification.

## Routing cautions

- Treat missing-first-token failures as provider failures. Step 3.7 Flash
  exhibited this failure in a prior HTML assignment.
- Treat a claimed completion without the required file as an implementation
  failure. GPT-OSS produced this failure in a prior CSS assignment.
- Treat local-file WebFetch calls and malformed write-tool calls as runtime
  failures. The installed local Qwen model exhibited both.
- Use the evaluator and repository tests to judge output. Agent completion text
  cannot establish success.
- Treat a model catalog entry as availability evidence. Require task evidence
  before adding it to an automatic route.

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
