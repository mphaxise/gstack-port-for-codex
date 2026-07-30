---
name: ios-qa
description: Perform structured, evidence-backed iOS QA with a frozen source and build package, tiered verification, reusable receipts, and strict device, privacy, and controller boundaries.
---

# iOS QA

Perform QA for a SwiftUI or iOS app using available simulator or physical-device tooling.

## Prepare

1. Read the project's instructions, accepted checkpoint, and narrow source map before scanning broadly.
2. Discover the project or workspace, scheme, configuration, and target device.
3. Freeze a QA package:
   - source revision or direct file fingerprints
   - build identifier and configuration
   - simulator or physical-device identity and OS
   - required flows, states, accessibility coverage, and privacy constraints
   - existing receipts and their covered inputs
4. Keep reviewers read-only. The controlling agent owns builds, app launch, Simulator or device control, screenshots, Git, and connected services.

## Verify In Tiers

Run the narrowest sufficient sequence:

1. deterministic source, configuration, or harness checks
2. focused tests for the changed slice
3. affected screens, flows, states, and accessibility paths
4. required consolidated suites
5. one build and runtime pass after the change set is stable

Repeat a build or runtime pass only when source, configuration, target, data state, or acceptance evidence changed, or when a failure requires diagnosis.

## Exercise Required Coverage

Cover applicable paths:

- launch and restoration
- navigation and selection
- forms and validation
- permissions and privacy disclosures
- empty, error, loading, and offline states
- Dynamic Type, VoiceOver, contrast, motion, and reduced-motion behavior
- orientation and size changes
- backend or transaction acceptance where the product contract requires it

Use the same screen, state, device, viewport, and data when comparing visual evidence.

For user-facing changes, also check applicable known recurrence families:

- hierarchy, discoverability, and primary versus utility action priority
- clipping, safe areas, overlays, spacing, and control geometry
- semantic color and destructive-action meaning
- maximum supported Dynamic Type, content reflow, and target size
- permission timing, denial, restriction, and recovery
- interruption, cancellation, return, and state restoration

Compare normal and maximum supported text sizes using the same state and data.
Build, test, or accessibility success does not replace visual and interaction
evidence. Read the project's prevention entries and record one UX recurrence
result: `clear`, `clear with new prevention`, `blocked`, or `unknown`.

## Record Receipts

For each check, record:

- frozen-package identity
- device and environment
- covered flow or risk surface
- observed result
- evidence location
- `reusable`, `invalidated`, or `unknown` status

For each material bug found and corrected, preserve its smallest reproduction,
intended invariant, escape reason when known, fix evidence, and prevention.
Verify that the prevention catches the original reproduction before acceptance.

Reuse a receipt only while every covered input remains unchanged. After a correction, rerun affected checks and one required consolidated pass; do not repeat unrelated flows.

## Closeout

Report findings with reproduction steps, severity, evidence, and remaining unknowns. Distinguish simulator from physical-device coverage. If the user asks for fixes, route to `ios-fix` and preserve the affected receipt list.

## Guardrails

- Do not claim hardware-specific coverage without a physical-device run.
- Keep QA report-only when the user asks for no fixes.
- Use isolated, account-free test state unless the user explicitly authorizes another boundary.
- Never enter or retain reviewer credentials.
- Do not reduce required accessibility, privacy, safety, backend, build, test, or acceptance coverage to save time or tokens.
