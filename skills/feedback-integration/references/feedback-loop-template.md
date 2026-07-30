# Feedback Loop Template

Use this compact structure for an active correction batch.

```md
## Feedback Batch

Outcome:
Scope:
Authority and stop gates:

### Included
- [feedback item] — source: [user, reviewer, test, or artifact]

### Deferred Or Recorded
- [feedback item] — reason:

### Correction Slice
- Allowlist:
- Acceptance criteria:
- Applicable prior prevention entries:
- Named invariants:
- Counterexamples:
- Adjacent surfaces:
- Full journey and repeat-use sequence:
- Visible gates and their resolving actions:
- Invalidated receipts:
- Reusable receipts:

### Verification
- Focused:
- Affected:
- Consolidated:
- Build or runtime:

### Prevention
- Symptom and reproduction:
- Intended invariant:
- Introduction or escape point:
- Affected journeys, states, screens, or platforms:
- Fix evidence:
- Prevention added:
- Original issue caught by prevention: yes / no / unknown
- Recurrence status: first / recurring / reusable-pattern candidate
- UX recurrence result: clear / clear with new prevention / blocked / unknown
- Skill-enhancement issue:
- Detection owner:
- Implementation owner:
- Enhancement state and next review date:
- Completion evidence:

### Discovery Routing
- Discovery:
- Review mode: acceptance / risk / fresh-eyes discovery
- Classification: block current slice / next correction slice / scheduled backlog / product decision / observe / closed
- Severity and confidence:
- Canonical issue family:
- Owner or decision gate:
- Acceptance method:
- Non-blocking rationale:

### Closeout
- Observed:
- Reported:
- Unknown:
- Remaining feedback:
- Next action:

### Milestone Prevention Review
- Effective safeguards:
- Bypassed, noisy, or ineffective safeguards:
- Project-local rules:
- Reusable-guidance candidates:
- Open skill-enhancement issues:
- Rules to remove:
- Optional escape counts by detection stage:
```

Omit empty optional sections. Keep the batch short enough to serve as a handoff without rereading the full task history.
