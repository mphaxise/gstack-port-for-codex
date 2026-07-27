#!/usr/bin/env python3
"""Validate the minimum structure of a prescriptive OpenCode commission."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


REQUIRED_HEADINGS = (
    "## Objective",
    "## Model and effort",
    "## Ownership and boundaries",
    "## Allowed inputs",
    "## Required output",
    "## Implementation contract",
    "## Acceptance checks",
    "## Failure handoff",
    "## Stop condition",
)

REQUIRED_BOUNDARIES = (
    "Read only:",
    "Create or edit only:",
    "Do not use Git",
    "Do not widen scope",
)

PLACEHOLDER_MARKERS = (
    "[short assignment name]",
    "[One observable implementation outcome.]",
    "[exact provider/model ID]",
    "[absolute isolated worktree or candidate path]",
    "[exact input path]",
    "[exact output path]",
)


def validate(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []

    if not text.startswith("# Commission:"):
        errors.append("first line must start with '# Commission:'")

    for heading in REQUIRED_HEADINGS:
        if heading not in text:
            errors.append(f"missing heading: {heading}")

    for boundary in REQUIRED_BOUNDARIES:
        if boundary not in text:
            errors.append(f"missing boundary phrase: {boundary}")

    for marker in PLACEHOLDER_MARKERS:
        if marker in text:
            errors.append(f"unresolved placeholder: {marker}")

    if len(text.splitlines()) < 35:
        errors.append("commission is too short to carry an executable contract")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("commissions", nargs="+", type=Path)
    args = parser.parse_args()

    failed = False
    for path in args.commissions:
        if not path.is_file():
            print(f"{path}: file not found", file=sys.stderr)
            failed = True
            continue

        errors = validate(path)
        if errors:
            failed = True
            for error in errors:
                print(f"{path}: {error}", file=sys.stderr)
        else:
            print(f"{path}: valid")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
