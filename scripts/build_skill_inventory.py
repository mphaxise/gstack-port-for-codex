#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from gstack_port_for_codex.reconciliation import build_canonical_inventory  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the canonical packaged-skill inventory.")
    parser.add_argument("--check", action="store_true", help="Fail when the tracked inventory is stale.")
    args = parser.parse_args()

    target = REPO_ROOT / "data" / "canonical-skill-inventory.json"
    rendered = json.dumps(build_canonical_inventory(REPO_ROOT), indent=2) + "\n"
    if args.check:
        if not target.exists() or target.read_text(encoding="utf-8") != rendered:
            print("Canonical skill inventory is stale.", file=sys.stderr)
            return 1
        print("Canonical skill inventory is current.")
        return 0

    target.write_text(rendered, encoding="utf-8")
    print(f"Wrote {target.relative_to(REPO_ROOT)}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
