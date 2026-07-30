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

### Closeout
- Observed:
- Reported:
- Unknown:
- Remaining feedback:
- Next action:
```

Omit empty optional sections. Keep the batch short enough to serve as a handoff without rereading the full task history.
