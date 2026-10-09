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
- prefer light, regular, and medium weights; reduce weight until hierarchy or
  legibility would weaken
- avoid heavy and bold weights; use them only when a lighter weight cannot preserve
  hierarchy or accessibility
- use no more than three intentional font sizes per page by default; document
  accessibility, data-density, or platform exceptions
- prefer sentence case and title case; reserve all caps for short labels,
  acronyms, and established conventions
- color roles are deliberate and contrast is verified
- cards, gradients, glass, oversized type, and decorative effects earn their place
- the interface has a product-specific point of view

Before adding a visual element, name the user value it provides: hierarchy,
orientation, status, affordance, comprehension, feedback, or brand recognition.
Remove elements that provide none of these benefits. Decoration can carry brand
character when it strengthens the composition and preserves usability.

## AI slop gate

Run this gate manually for every interface review. Use a deterministic detector when
one is already available, then compare its findings with rendered evidence. A pattern
signals generic defaults. Authorship remains unverified.

Classify the target before scoring:

- `marketing`: brand, editorial, campaign, portfolio, or conversion surfaces
- `product`: settings, dashboards, forms, tools, and operational workflows
- `native`: iOS, Android, and platform-adaptive screens
- `hybrid`: apply the matching register to each surface

Check for these pattern groups:

### Typography

- one generic family used for every role, especially Inter in a centered hero
- templated font combinations such as Space Grotesk, Instrument Serif, Geist, Syne,
  or Fraunces without a product-specific rationale
- one italic, serif, or colored hero word added as an isolated flourish
- heavy or bold weights used across headings, controls, and body copy
- more than three font sizes on one page without an accessibility, data-density, or
  platform reason
- all-caps navigation, headings, or labels used as the default voice

### Color and effects

- violet or indigo accents used as a default technology aesthetic
- pervasive gradients, gradient-clipped text, saturated glows, or colored shadows
- permanent dark mode with muted gray body text or marginal contrast
- glassmorphism or backdrop blur applied without a spatial or interaction purpose

### Layout and components

- a centered generic hero with a pill badge above the headline
- a symmetric three-column feature grid with repeated icon, title, and description
- identical icon-topped cards or icons in colored circles used as section decoration
- colored top or left stripes on cards
- numbered `1, 2, 3` process rows, stat banners, or templated FAQ accordions
- pill-shaped buttons, tabs, fields, and controls used as the default shape system
- uniform large corner radii across unrelated components
- decorative blobs, floating circles, wavy dividers, or ornamental illustrations used
  to fill empty space
- emoji used as navigation, section, or action icons
- a repeated hero, features, testimonials, pricing, and call-to-action rhythm with
  uniform section heights

Pill shapes are appropriate for tags, filters, compact status, segmented choices, and
other controls whose meaning benefits from a capsule boundary. Standard actions should
use the established button geometry unless a pill shape improves recognition or touch
behavior.

### Copy and system defaults

- generic hero claims such as `Welcome to`, `Unlock the power of`, or `All-in-one`
- library defaults, including unmodified shadcn/ui composition and styling
- visual sections whose purpose disappears when their decoration is removed

Score the cluster, then judge the composition:

- `0-1 patterns`: low signal; record only when the pattern harms the target
- `2-3 patterns`: moderate signal; inspect whether defaults are replacing product
  decisions
- `4+ patterns`: high risk; the gate fails when the patterns cluster in one view and
  lack product, usability, or accessibility justification

For every retained pattern, record the rendered evidence, user impact, and rationale.
False positives and deliberate exceptions stay in the report. The gate passes when the
page has a product-specific point of view, every visual element earns its place, and
the remaining patterns have clear functional or brand value.

Source guidance: [Adrian Krebs, "Scoring Show HN submissions for AI design
patterns"](https://www.adriankrebs.ch/blog/design-slop/) and the
[Design Slop Cop rule set](https://github.com/AdrianKrebs/design-slop-cop).

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
