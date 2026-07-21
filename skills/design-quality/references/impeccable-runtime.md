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

Project configuration can scope manual scans through detector ignores and declared template extensions. Treat that configuration as a project decision. Use `--no-config` only when a raw detector run is needed for diagnosis, and preserve the reason for any confirmed exception.

## Live variants

Use Impeccable live mode only when:

- a web interface is running locally
- the runtime is already installed
- browser mutation and source mapping are available
- the user wants interactive variants

Keep source changes on the active task branch. Report session cleanup and accepted-source status.

For a Codex live session, keep the external runtime's one-shot poll in the yielded foreground execution lane. After every event or reply, start the foreground poll again. If the session is interrupted, inspect its external runtime status or recovery command before resuming. The external runtime owns its session journal, browser injection, and source-rewrite cleanup.

## Hooks

Project hooks require explicit installation and Codex trust review. A skill can recommend the hook after repeated detector findings. It cannot silently install, trust, enable, disable, or configure the hook.

When the external runtime is already present, its hook configuration is project-scoped. Keep shared policy in the project's reviewed configuration and developer consent in its local ignored configuration. Record a detector exception only after the user confirms it is intentional, and keep the exception as narrow as the finding allows.

Codex receives post-edit hook feedback from the external runtime. It does not use the external runtime to block a proposed write. This port keeps that runtime behavior upstream and continues to require normal Codex approval and trust boundaries.

## Boundaries

- keep Impeccable runtime code upstream
- retain Apache-2.0 attribution for adapted guidance
- avoid network installation during a review or automated fallback
- continue with local source and visual evidence when the runtime is unavailable
