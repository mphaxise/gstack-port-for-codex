# OpenCode commission template

Use this structure for every delegated assignment. Replace every bracketed
field with a concrete value.

```markdown
# Commission: [short assignment name]

## Objective

[One observable implementation outcome.]

## Model and effort

- Model: `[exact provider/model ID]`
- Reasoning: `[minimal|low|medium|high]`

## Ownership and boundaries

- Working directory: `[absolute isolated worktree or candidate path]`
- Read only:
  - `[exact input path]`
- Create or edit only:
  - `[exact output path]`
- Do not inspect sibling files.
- Do not use Git, install packages, start a server, deploy, or create notes.
- Stop and report the conflict if the contract cannot be satisfied inside this
  boundary.

## Allowed inputs

[Include the complete local contract the agent needs. Avoid requiring discovery
outside the read list.]

## Required output

[Name the exact file, format, exports, selectors, schema, or generated artifact.]

## Implementation contract

1. [Locked architecture or structure.]
2. [Exact interface with types, signatures, selectors, or data shape.]
3. [Required behavior and state transitions.]
4. [Edge cases and failure behavior.]
5. [Accessibility, security, privacy, and performance constraints.]
6. [Forbidden dependencies or patterns.]

## Acceptance checks

Run only:

1. `[exact narrow validation command]`
2. `[second command when required]`

The assignment passes when:

- [deterministic acceptance condition]
- [deterministic acceptance condition]

## Failure handoff

Report the failing command, concise error, files changed, and safest next action.
Do not widen scope.

## Stop condition

Stop after the assigned file passes the allowed checks or after reporting one
blocked contract.
```

## Correction form

A correction commission contains:

- the original ownership and forbidden-action boundary
- the evaluator command and observed failure
- the exact expected result
- the single file or module allowed to change
- requirements that already pass and must remain unchanged
- the same validation and stop condition

Exclude speculative redesign and unrelated cleanup.
