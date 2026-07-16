#!/usr/bin/env python3

from pathlib import Path
import argparse
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from gstack_port_for_codex.brain import (  # noqa: E402
    DEFAULT_BRAIN_ROOT,
    format_search_hits,
    search_brain,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Search the local Codex brain corpus.")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--limit", type=int, default=10, help="Maximum number of hits")
    args = parser.parse_args()

    brain_root = REPO_ROOT / DEFAULT_BRAIN_ROOT
    hits = search_brain(brain_root, args.query, limit=args.limit)
    print(format_search_hits(hits, brain_root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
