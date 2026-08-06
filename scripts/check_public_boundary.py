#!/usr/bin/env python3
"""Reject private operating material and common credentials in tracked files."""

from __future__ import annotations

from pathlib import Path
import re
import subprocess


REPO_ROOT = Path(__file__).resolve().parents[1]
PRIVATE_MARKERS = (
    "prescriptive" + "-opencode-" + "delegation",
    "/Users/" + "praneet/" + "Marlowe",
    "marlowe-" + "ai-" + "systems-" + "handbook",
    "marlowe_" + "runtime_" + "state.py",
    "DELE" + "GATION.md",
)
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
)


def tracked_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return [REPO_ROOT / line for line in result.stdout.splitlines() if line]


def main() -> int:
    errors: list[str] = []
    files = tracked_files()
    tracked_brain = [
        path.relative_to(REPO_ROOT).as_posix()
        for path in files
        if path.relative_to(REPO_ROOT).as_posix().startswith("brain/")
    ]
    if tracked_brain != ["brain/README.md"]:
        errors.append(f"Generated brain content is tracked: {tracked_brain}")

    for path in files:
        if not path.is_file():
            continue
        rel = path.relative_to(REPO_ROOT).as_posix()
        if rel == "scripts/check_public_boundary.py":
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for marker in PRIVATE_MARKERS:
            if marker in text or marker in rel:
                errors.append(f"Private boundary marker in {rel}: {marker}")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                errors.append(f"Possible credential pattern in {rel}: {pattern.pattern}")

    if errors:
        print("Public-boundary check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Public-boundary check passed for {len(files)} candidate files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
