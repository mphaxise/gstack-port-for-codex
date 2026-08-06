# Contributing

Thanks for improving the Codex workflow port. Keep changes small enough to
review and preserve the repository's provenance boundaries.

## Before opening a change

- Read the relevant skill and its source or adaptation note.
- Keep upstream behavior, Codex adaptation, and local extension work clearly
  separated.
- Add or update deterministic tests for scripts and registries.
- Do not add private memories, credentials, provider inventories, benchmark
  transcripts, or machine-specific paths.

## Local checks

```bash
python3 scripts/validate_repo.py
python3 -m unittest discover -s tests
python3 scripts/smoke_install.py
python3 scripts/check_public_boundary.py
python3 -m compileall -q scripts src tests
git diff --check
```

The upstream drift checker needs network access to GitHub. A failed network
request should be reported as an unavailable freshness check, not as proof of
parity.

## Skill changes

Every ported skill needs a `SKILL.md` with valid frontmatter and a registry
entry in the appropriate map. Record the upstream source commit when the
skill is adapted from an upstream source. Use the coding workflow guide when
the change affects planning, slicing, implementation, or review behavior.

## Pull requests

Describe the user-visible or maintainer-visible outcome, the files changed,
the checks run, and any remaining external or network-dependent gate. Do not
claim upstream parity when only a partial capability was reviewed.
