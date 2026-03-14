# Mode Cheatsheet

## Default Choice

- Use `BIG CHANGE` for greenfield features, architecture work, or plans touching many files or systems.
- Use `SMALL CHANGE` for localized work, narrow feature tweaks, or contained bug fixes.
- Use `SCOPE REDUCTION` when the request sounds overbuilt, deadline-driven, or intentionally minimal.

## Mode Behavior

### SCOPE REDUCTION

- challenge extras aggressively
- separate "must ship together" from "follow-up work"
- optimize for minimal diff and reversibility

### BIG CHANGE

- review architecture, code quality, tests, and performance separately
- prefer explicit diagrams and clear risk tables
- surface all major decision points before implementation

### SMALL CHANGE

- run Step 0, then a combined pass over architecture, code quality, tests, and performance
- pick the single most important issue per area
- keep the output compact but still opinionated

