# Model routing

## Default chain

1. Primary: `nvidia/openai/gpt-oss-120b`, medium reasoning.
2. Free fallback: select one task-matched `opencode/*-free` model.
3. Local fallback: use the exact installed Ollama model ID.

As observed on 2026-07-27, the local inventory contains
`ollama/qwen3.5:9b`. The requested Qwen Coder 3.5B model is absent. Re-run
`opencode models` and `ollama list` before relying on this snapshot.

## Free fallback selection

| Work type | Preferred free fallback |
| --- | --- |
| Application code, JavaScript, TypeScript, APIs | `opencode/north-mini-code-free` |
| Broad refactor or reasoning-heavy integration | `opencode/nemotron-3-ultra-free` |
| HTML, CSS, or compact interface implementation | `opencode/mimo-v2.5-free` |
| Compact markup or low-latency generation | `opencode/ling-3.0-flash-free` |
| Algorithmic or data-heavy code | `opencode/deepseek-v4-flash-free` |

Choose one free specialist before starting the assignment. Move to the local
tier after one qualifying provider failure. Keep the same scope and files.

## Failure signals

Fallback is allowed for:

- quota exhaustion or an explicit near-quota refusal
- rate limiting
- transient provider or 5xx failure
- timeout
- missing first token

An implementation defect is a correction case. Keep the current model when its
session is healthy and issue one narrow evaluator-driven correction.

## Cost evidence

Capture stored session cost from OpenCode. A configured free route can still
change, so verify the provider ledger after every run. Report cache reads as
token traffic and keep them separate from Codex task tokens.
