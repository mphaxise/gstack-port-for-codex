# Complete Skill Reconciliation

Reviewed on 2026-08-08 with `codex-cli 0.144.0` and the current official Codex
manual.

## Result

The complete manifest covers 108 canonical GStack and GBrain skills and all
109 mapped upstream lineages in the public package. `skillify` has one canonical
package with GStack and GBrain provenance:

- 56 GStack lineages reviewed through `94993f74012782fd94416dd44b8314f6363a13a4`
- 53 GBrain-backed skills reviewed through `0b47afbf402a4e27a648bb9d131ce584461461ea`
- 68 accepted source pins
- 41 reviewed deferrals

Each record includes the adopted and reviewed commits, three content hashes,
line-retention measurements, host coupling, companion resources, intentional
removals, validation commands, and a decision reason grounded in the registry's
skill-specific adaptation note.

## Accepted portable changes

The refresh updates the reusable Codex guidance for:

- destructive commands that use chained syntax, command substitution, or
  uppercase `rm -R`
- current-branch-first checkpoint and context restoration
- remote GBrain thin clients without a local database engine
- single-capability boundaries during skill creation
- preservation of native plugin fields during testing and harvesting
- explicit preview and apply separation for protected schema migrations
- host-neutral transcription when a voice note arrives without text

Unchanged upstream skill files also advance their adopted source pin after
review. Their concise Codex adaptations remain covered by explicit removal and
retention evidence.

## Reviewed deferrals

Forty GStack lineages retain their prior adopted source. Their current
mapped delta is Claude Code question-preference hook wiring, which does not
belong in the Codex adapter. `capture` retains the file-backed Codex title
contract reviewed in beta instead of adopting GBrain's 80-character ellipsis
rule. The alternate GStack `skillify` record preserves its host-specific
question-hook deferral while the canonical package adopts the portable GBrain
scope improvements.

The full review imports no Claude settings, permission hooks, personal context,
provider defaults, or external-worker requirements.

## Compatibility audit

The affected skill and tooling surface was checked for the reported host
compatibility risks:

- permission and destructive-command guidance remains approval-aware and now
  covers the latest upstream guard semantics
- paired agents and minion-style work require explicit user authorization;
  headless workers are not a prerequisite
- no packaged skill introduces a `--bare` runtime requirement
- `AGENTS.md` remains the Codex instruction surface, while `CLAUDE.md` mutation
  and Claude-specific hooks remain outside the package
- OpenCode delegation is absent from the public bundles and is not required by
  the refreshed workflows

Impeccable is a separately tracked runtime-capability map. Its current hook
movement is visible in the broader upstream gate and does not change this
GStack and GBrain skill decision set.

## Installation boundary

Current Codex documentation places user skills in `~/.agents/skills` and does
not merge duplicate names. The installer now writes an ownership and file-hash
receipt for each copy. A forced refresh can update only a matching receipted
directory. Shared symlinks, unowned files, and local edits fail closed.

Use a staging destination before any user-surface change:

```bash
python3 scripts/install_skills.py --bundle all --dest /path/to/staging/skills
python3 scripts/check_engineering_milestone.py
```

The local acceptance run staged and hash-verified all 117 public package skills.
It then installed only seven missing names into the user surface. The 120
existing shared symlinks remained unchanged, including the 110 names that
overlap this package. This preserves the richer shared skill sources while
making the previously absent package entries discoverable.

The repository gate remains the package acceptance command. Add `--upstream`
to confirm that no mapped GStack or GBrain skill changed after these review
boundaries.
