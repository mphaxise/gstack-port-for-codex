# QA Issue Taxonomy

## Severity

| Severity | Meaning | Examples |
| --- | --- | --- |
| `critical` | blocks a core workflow or causes data loss | checkout broken, destructive action without confirmation |
| `high` | major feature broken with no good workaround | upload fails, auth loop, dead form submit |
| `medium` | feature works but noticeably degrades quality | mobile layout broken, confusing validation, slow interactions |
| `low` | minor polish issue | typo, spacing, non-blocking visual mismatch |

## Categories

- `visual`: broken layout, clipping, wrong layering, missing images
- `functional`: dead buttons, broken links, wrong state transitions, bad validation
- `ux`: confusing flow, missing feedback, bad errors, dead ends
- `content`: typos, outdated text, placeholder copy, poor empty states
- `performance`: slow loads, layout shifts, excessive requests
- `console`: JS errors, failed requests, warnings that indicate breakage
- `accessibility`: unlabeled inputs, broken keyboard navigation, missing alt text

## Per-Page Checklist

1. Visual scan
2. Interactive elements
3. Forms and edge cases
4. Navigation in and out
5. Empty, loading, and error states
6. Console or network health
7. Responsive behavior if relevant
8. Auth or role boundaries if relevant

