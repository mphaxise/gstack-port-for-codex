#!/usr/bin/env python3

from pathlib import Path
import argparse
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from gstack_port_for_codex.brain import (  # noqa: E402
    DEFAULT_BRAIN_ROOT,
    brain_stats,
    ensure_brain_root,
    report_as_json,
    validate_brain,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check the health of the local Codex brain corpus.")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Print JSON output")
    args = parser.parse_args()

    brain_root = REPO_ROOT / DEFAULT_BRAIN_ROOT
    ensure_brain_root(brain_root)
    stats = brain_stats(brain_root)
    errors = validate_brain(brain_root)
    report = {
        "stats": stats,
        "errors": errors,
        "status": "ok" if not errors else "issues",
    }

    if args.as_json:
        print(report_as_json(report))
    else:
        print(f"Brain root: {brain_root}")
        print(f"Pages: {stats['page_count']}")
        print(f"Categories: {stats['categories']}")
        if errors:
            print("Issues:")
            for error in errors:
                print(f"- {error}")
        else:
            print("Brain health passed.")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
