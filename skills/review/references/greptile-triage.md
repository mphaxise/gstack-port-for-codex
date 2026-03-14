# Greptile Triage

Use this only when `gh` is available and the current branch has an open PR.

## Fetch

- detect the current repo and PR with `gh repo view` and `gh pr view`
- fetch both line-level PR review comments and top-level issue comments
- filter to `greptile-apps[bot]`

## Classify

For each non-suppressed comment, classify it as one of:

- `VALID & ACTIONABLE`
- `VALID BUT ALREADY FIXED`
- `FALSE POSITIVE`
- `SUPPRESSED`

## Handling

- Include valid comments in the review findings when they still apply.
- Reply only if the user asks you to handle or resolve the comment.
- Keep per-project and global history if the team already uses Greptile triage tracking.

