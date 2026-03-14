# Review Checklist

Review the full diff against `origin/main` and use this checklist.

## Pass 1: Critical

### SQL And Data Safety

- string interpolation in SQL or query fragments
- non-atomic read-check-write sequences that can race
- `find_or_create_by` without matching uniqueness guarantees
- direct column writes that bypass validations on important fields

### Race Conditions And Concurrency

- concurrent status transitions without compare-and-set behavior
- duplicate creation paths without uniqueness protection
- unsafe multi-step writes around shared state

### Trust Boundaries

- LLM output written to storage or sent externally without validation
- tool output accepted without type or shape checks
- `html_safe`, `raw`, or other unsafe rendering paths on user-controlled data

## Pass 2: Informational

### Conditional Side Effects

- one branch applies a side effect while another silently skips it
- logs claim an action happened when it only happened conditionally

### Magic Coupling And Drift

- duplicated thresholds or strings that are likely to drift
- comments or docs that now describe old behavior
- prompts that name tools or capabilities no longer wired up

### Test Gaps

- missing negative-path tests
- missing assertions on side effects
- missing integration coverage for auth, rate limits, or enforcement logic

### Frontend And UX

- heavy inline styles in shared render paths
- repeated expensive lookups in views
- clear interactive regressions or broken empty states

## Suppressions

Do not flag:

- harmless readability redundancy
- speculative comments about "maybe tighter tests" when coverage is already sufficient
- style-only concerns with no reliability impact
- anything already fixed in the diff you are reviewing

