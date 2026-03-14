# Review Sections

Use these sections after the Step 0 scope challenge.

## 1. Architecture

- component boundaries
- dependency graph and coupling
- data flow and single points of failure
- security boundaries
- whether the plan needs ASCII diagrams

## 2. Code Quality

- DRY violations
- error handling and missing edge cases
- module layout and abstraction level
- stale or missing inline diagrams in touched files

## 3. Tests

- diagram the new codepaths, UX branches, and branching logic
- identify which tests should exist for each new path
- call out any prompt or eval suites if the repo relies on them

## 4. Performance

- slow or high-complexity paths
- unnecessary repeated work
- memory or caching concerns
- likely bottlenecks under heavier load

