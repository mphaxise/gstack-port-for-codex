#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from gstack_port_for_codex.registry import load_skill_map  # noqa: E402
from gstack_port_for_codex.upstream_drift import (  # noqa: E402
    UpstreamDriftError,
    check_upstream_drift,
    format_drift_report,
    github_token_from_env,
    report_as_json,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check drift between the pinned upstream gstack commit and upstream default branch.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print the drift report as JSON.",
    )
    args = parser.parse_args()

    skill_map = load_skill_map(REPO_ROOT / "data" / "skill-map.json")

    try:
        report = check_upstream_drift(skill_map, token=github_token_from_env())
    except UpstreamDriftError as exc:
        print(f"Upstream drift check failed: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(report_as_json(report))
    else:
        print(format_drift_report(report))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
