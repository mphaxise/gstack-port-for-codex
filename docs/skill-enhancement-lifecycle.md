# Skill Enhancement Lifecycle

Every reusable skill improvement should move through one public, auditable issue
from candidate evidence to verified release. Project repositories retain raw
evidence and private context. This repository owns the generalized workflow
change.

## Promotion Gate

Create or update a skill-enhancement issue when one of these conditions is met:

- a critical safety, privacy, accessibility, commerce, destructive-action, or
  data-integrity finding requires an immediate reusable gate
- the same issue family reaches the project recurrence threshold defined by
  `feedback-integration`
- a milestone prevention review identifies a safeguard that repeatedly caught,
  missed, or obscured material issues
- direct evidence shows that an existing skill rule is ineffective, obsolete,
  or too ambiguous to execute consistently

Keep the first ordinary occurrence in the source project's prevention record.
Mark the second similar occurrence as recurring and inspect adjacent surfaces.
Promote the third accepted occurrence as a reusable-pattern candidate. A
critical issue can enter the lifecycle immediately.

## Evidence Packet

One issue owns one invariant or issue family. Include:

- the generalized symptom and smallest reliable reproduction
- recurrence count and detection stages
- the intended invariant
- the current safeguard and its observed limitation
- affected skill names and review modes
- a proposed prevention mechanism
- acceptance checks and one counterexample
- an owner, target milestone, and next review date

Summarize private or company evidence. Exclude product names, private paths,
screenshots, credentials, customer data, and raw communications from this public
repository.

## States

Use one state at a time:

1. `candidate`: evidence is recorded and the promotion gate is plausible
2. `accepted`: the reusable invariant, owner, scope, and acceptance checks are
   approved
3. `implementing`: the named skill and documentation changes are in progress
4. `validating`: structural validation and prevention replay are in progress
5. `released`: the change is present on a remote branch or the default branch,
   with its commit or pull request recorded
6. `declined`: evidence does not justify a reusable rule; preserve the reason
7. `superseded`: another issue or rule now owns the invariant

Reopen a released issue when new evidence invalidates its acceptance checks.

## Ownership

The lifecycle uses four explicit owners:

- `detection owner`: the project task that records the source evidence and
  creates or updates the generalized issue when external writes are authorized
- `lifecycle steward`: the weekly repository-health automation that audits open
  `skill-enhancement` issues, updates lifecycle evidence, flags missing or
  overdue actions, and closes terminal issues
- `implementation owner`: the named person or task responsible for the skill,
  test, template, and documentation change
- `release owner`: the repository maintainer who approves the merge or other
  publication action

The lifecycle steward never treats issue maintenance as implementation evidence.
An accepted issue without an implementation owner is blocked and must be
reported at the weekly review.

## Completion Gate

Close an enhancement as `released` only when:

- the changed skill passes repository and skill validation
- the new safeguard catches the generalized original reproduction
- one counterexample confirms that the rule does not overreach
- affected templates, routing, and operator documentation are current
- the remote commit or pull request is linked
- the source project records the reusable rule or issue link when its privacy
  boundary permits it

Close `declined` and `superseded` issues with a concise decision record. Open
issues always retain an owner and next review date.

## Milestone Review

At each project milestone:

1. review reusable-pattern candidates in the project prevention ledger
2. create or update the corresponding public issue with generalized evidence
3. inspect accepted and implementing issues for overdue next actions
4. verify released safeguards against any later recurrence
5. close, reopen, decline, or supersede each reviewed issue

The weekly repository-health automation performs the queue audit. It may comment
on, label, or close only `skill-enhancement` issues in this repository. Initial
candidate creation belongs to the detection owner. The automation does not edit
code, merge pull requests, or manufacture missing evidence.

Use [the skill-enhancement issue
template](../.github/ISSUE_TEMPLATE/skill-enhancement.md) for the canonical
record.
