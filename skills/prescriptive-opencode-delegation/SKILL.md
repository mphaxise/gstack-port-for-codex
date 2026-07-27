---
name: prescriptive-opencode-delegation
description: Plan and orchestrate implementation through tightly bounded OpenCode agents while Codex retains architecture, file contracts, exception handling, assembly, and final verification. Use for coding or design-implementation tasks that can be split into non-overlapping files or modules, especially when the user requests OpenCode delegation, cheaper external coding agents, detailed agent commissions, or a Codex-orchestrated multi-agent build.
---

# Prescriptive OpenCode Delegation

Use Codex as the architect and verifier. Give each OpenCode agent one exact,
bounded implementation commission. Preserve the target repository's
instructions, ownership, privacy boundary, and test contract.

## Decide whether delegation fits

Delegate when the implementation has at least two independent files or modules,
stable interface contracts, and deterministic assembly checks. Work directly
when the change is tiny, tightly coupled, security-sensitive, or cheaper to
implement than to specify.

Keep planning, architecture, cross-file interfaces, acceptance criteria,
assembly, deployment, and final verification with Codex. Give agents
implementation authority only inside their assigned boundaries.

## Establish the execution contract

1. Inspect the live repository, applicable `AGENTS.md`, relevant source, tests,
   branch, upstream, and dirty state.
2. Name the owning repository and preserve unrelated changes.
3. Define the finished behavior, fixed evaluator, correction limit, and
   publication boundary.
4. Create an isolated worktree or candidate directory when parallel writes
   could collide with user work.
5. Draw the file and interface map before starting any agent.
6. Assign exclusive ownership for every delegated file. Keep shared files under
   Codex ownership or schedule them serially.

Use a bounded loop: one initial implementation per assignment, one retry per
model tier for provider failures, and one evaluator-driven product correction
unless the task contract specifies a tighter bound.

## Route models

Read [model-routing.md](references/model-routing.md) before starting delegated
runs. Default to `nvidia/openai/gpt-oss-120b` with medium reasoning.

Use one task-matched free OpenCode fallback for quota, rate-limit, transient
provider, 5xx, timeout, or missing-first-token failures. Use the installed local
Ollama model after that free tier. Preserve the original commission, target
files, and acceptance criteria across retries.

Never use a Codex/OpenAI-billed delegated model. The `openai` segment in the
NVIDIA-hosted GPT-OSS identifier describes the model family; verify the active
provider and stored cost before reporting.

## Write executable commissions

Read [commission-template.md](references/commission-template.md) and create one
commission per assignment. Specify:

- exact files the agent may read
- exact files the agent may create or edit
- locked interfaces with selectors, types, signatures, schemas, or import paths
- required behavior, edge cases, accessibility, and performance constraints
- allowed validation commands
- forbidden actions, including Git, deployment, installs, servers, and sibling
  file inspection unless explicitly required
- stop condition and failure handoff

Remove design choices from the commission when Codex has already made them.
Resolve cross-file decisions before delegation. Tell the agent to stop and
report an unmet contract instead of widening scope.

Validate every commission:

```bash
python3 scripts/validate_commission.py path/to/commission.md
```

## Run bounded agents

1. Start independent assignments in parallel only when their write sets do not
   overlap.
2. Invoke OpenCode with the exact model, reasoning effort, worktree, and
   commission file.
3. Track session ID, model, provider, variant, start time, terminal state,
   fallback, token fields, and stored cost.
4. Avoid continuous code review while agents run. Check process health only
   when output stalls or the provider emits a fallback signal.
5. Stop any agent that crosses its write boundary or expands authority.

Do not ask an agent to plan the complete product, reinterpret the architecture,
deploy, commit, or review sibling work.

## Assemble and correct

After all assignments reach a terminal state:

1. Inspect the write set and boundary compliance.
2. Assemble the files without redesigning successful agent output.
3. Run syntax, type, unit, integration, accessibility, performance, and visual
   checks that the task requires.
4. Translate a failed verifier into the smallest correction commission. Include
   only the observed failure, exact expected state, allowed file, and preserved
   constraints.
5. Reuse the same agent session when healthy. Apply the bounded fallback chain
   when the provider fails.
6. Stop at the correction limit and report the best verified state.

## Verify independently

Codex performs the final verification against the original user request and
repository contract. Confirm:

- behavior and tests
- cross-file integration
- accessibility, security, and privacy requirements
- output quality at required viewports or environments
- source size and runtime errors when relevant
- exact deployed or published state when authorized
- final diff and unrelated dirty state

Agent self-reports are evidence of attempted work. Independent checks establish
completion.

## Measure and close out

Keep Codex and OpenCode counters separate. Report:

- Codex tokens and elapsed time from the available task or goal counter
- each OpenCode session's input, output, reasoning, cache, and stored cost
- fallback path and correction count
- output quality using a fixed rubric
- read and write boundary findings
- final repository, commit, deployment, and remaining limits

Create a goal only when the user explicitly requests one. When comparing
workflows, freeze the implementation window after final verification and before
writing the benchmark report.
