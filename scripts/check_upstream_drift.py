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
        description="Check drift between a pinned upstream source commit and the upstream default branch.",
    )
    parser.add_argument(
        "--map",
        choices=("gstack", "gbrain", "praneet", "impeccable"),
        default="gstack",
        help="Skill map to check. Defaults to gstack.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print the drift report as JSON.",
    )
    args = parser.parse_args()

    map_paths = {
        "gstack": REPO_ROOT / "data" / "skill-map.json",
        "gbrain": REPO_ROOT / "data" / "gbrain-skill-map.json",
        "praneet": REPO_ROOT / "data" / "praneet-skill-map.json",
        "impeccable": REPO_ROOT / "data" / "impeccable-capability-map.json",
    }
    skill_map = load_skill_map(map_paths[args.map])

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
