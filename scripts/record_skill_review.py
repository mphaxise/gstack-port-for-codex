#!/usr/bin/env python3
"""Record a reviewed upstream boundary and accepted per-skill source pins."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from gstack_port_for_codex.reconciliation import (  # noqa: E402
    resolve_repo_path,
    validate_git_commit,
)


def record_review(
    data: dict,
    reviewed_commit: str,
    adopted_slugs: list[str],
    reviewed_at: str | None = None,
) -> dict:
    reviewed_commit = validate_git_commit(reviewed_commit)
    refreshed = json.loads(json.dumps(data))
    skills = {skill["upstream_slug"]: skill for skill in refreshed["skills"]}
    unknown = sorted(set(adopted_slugs) - set(skills))
    if unknown:
        raise ValueError(f"Unknown upstream skill slug(s): {', '.join(unknown)}")

    refreshed["source"]["skill_reviewed_commit"] = reviewed_commit
    refreshed["source"]["latest_checked_commit"] = reviewed_commit
    if reviewed_at:
        refreshed["source"]["latest_checked_at"] = reviewed_at
    for slug in adopted_slugs:
        skills[slug]["source_commit"] = reviewed_commit
    return refreshed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--map", type=Path, required=True)
    parser.add_argument("--reviewed-commit", required=True)
    parser.add_argument("--reviewed-at")
    parser.add_argument("--adopted", action="append", default=[])
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    target = resolve_repo_path(REPO_ROOT, args.map)
    data = json.loads(target.read_text(encoding="utf-8"))
    refreshed = record_review(
        data, args.reviewed_commit, args.adopted, reviewed_at=args.reviewed_at
    )
    rendered = json.dumps(refreshed, indent=2) + "\n"
    relative_target = target.relative_to(REPO_ROOT.resolve())
    if args.check:
        if target.read_text(encoding="utf-8") != rendered:
            print(f"{relative_target} review metadata is stale.")
            return 1
        print(f"{relative_target} review metadata is current.")
        return 0

    target.write_text(rendered, encoding="utf-8")
    print(f"Wrote {relative_target}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
