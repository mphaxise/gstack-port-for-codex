# Optional Impeccable Runtime

Impeccable supplies an Apache-2.0 detector, provider hooks, and live browser iteration. Treat it as an optional external runtime.

## Detection

Check availability without installing packages:

```bash
npx --no-install impeccable --version
```

When available, scan the narrowest relevant target:

```bash
npx --no-install impeccable detect --json <target>
```

Exit code `0` means clean. Exit code `2` means findings. Preserve rule identifiers, file paths, and false-positive judgments. A missing runtime triggers manual review through `quality-gates.md`.

## Live variants

Use Impeccable live mode only when:

- a web interface is running locally
- the runtime is already installed
- browser mutation and source mapping are available
- the user wants interactive variants

Keep source changes on the active task branch. Report session cleanup and accepted-source status.

## Hooks

Project hooks require explicit installation and Codex trust review. A skill can recommend the hook after repeated detector findings. It cannot silently install, trust, or enable the hook.

## Boundaries

- keep Impeccable runtime code upstream
- retain Apache-2.0 attribution for adapted guidance
- avoid network installation during a review or automated fallback
- continue with local source and visual evidence when the runtime is unavailable
