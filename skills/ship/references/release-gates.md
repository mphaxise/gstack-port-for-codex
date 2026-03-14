# Release Gates

## Preflight

- confirm current branch is not `main`
- inspect `git status`
- inspect the diff and commit list being shipped

## Merge And Test

- merge or rebase `origin/main` into the branch before the final test pass
- run the repo's real test commands, not guessed substitutes
- if the repo has prompt/eval gates, run the relevant suites

## Review

- run a pre-landing review before pushing
- resolve or explicitly acknowledge any blocking issues

## Optional Repo Conventions

Only perform these if the repo already uses them:

- `VERSION`
- `CHANGELOG.md`
- release notes
- PR creation via `gh`

