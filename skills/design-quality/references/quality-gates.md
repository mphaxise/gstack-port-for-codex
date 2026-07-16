# Quality Gates

Apply the gates that match the target and user request.

## System fidelity

- read existing tokens and representative components
- reuse established primitives before adding page-specific vocabulary
- document deliberate exceptions
- distinguish current design truth from proposed direction

## Visual craft

- hierarchy is clear at a glance
- spacing creates grouping and rhythm
- typography remains readable across viewport sizes
- color roles are deliberate and contrast is verified
- cards, gradients, glass, oversized type, and decorative effects earn their place
- the interface has a product-specific point of view

## Interaction

- default, hover, focus, active, disabled, loading, empty, success, and error states are covered where applicable
- keyboard and pointer paths work
- overlays escape clipping and stacking-context failures
- destructive actions provide recovery proportional to risk

## Responsive and native adaptation

- verify narrow, medium, and wide layouts from rendered evidence when possible
- test content overflow, long labels, text scaling, and localization pressure
- use platform conventions and real simulator or device evidence for native claims

## Motion

- motion communicates state or spatial change
- content remains available when animation fails or pauses
- reduced-motion behavior exists
- performance-sensitive properties stay within the rendering budget

## Production hardening

- overflow, missing data, slow data, errors, retries, and boundary inputs are handled
- internationalization and bidirectional layout are considered when relevant
- images and assets have reliable sources and fallbacks
- performance claims use measured evidence

## Final evidence

Use the strongest available combination of source inspection, deterministic scan, browser or simulator evidence, screenshots, and automated tests. Name every unavailable path that materially limits confidence.
