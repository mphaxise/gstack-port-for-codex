#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from gstack_port_for_codex.reconciliation import refresh_reconciliation_manifest  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Refresh alpha reconciliation hashes and retention.")
    parser.add_argument("--gstack-repo", type=Path, required=True)
    parser.add_argument("--gbrain-repo", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    target = REPO_ROOT / "data" / "reconciliation-alpha.json"
    manifest = json.loads(target.read_text(encoding="utf-8"))
    refreshed = refresh_reconciliation_manifest(
        manifest,
        REPO_ROOT,
        {"gstack": args.gstack_repo, "gbrain": args.gbrain_repo},
    )
    rendered = json.dumps(refreshed, indent=2) + "\n"
    if args.check:
        if target.read_text(encoding="utf-8") != rendered:
            print("Alpha reconciliation manifest is stale.", file=sys.stderr)
            return 1
        print("Alpha reconciliation manifest is current.")
        return 0

    target.write_text(rendered, encoding="utf-8")
    print(f"Wrote {target.relative_to(REPO_ROOT)}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
