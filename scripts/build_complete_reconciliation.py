#!/usr/bin/env python3
"""Build or verify the complete reviewed GStack and GBrain skill manifest."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from gstack_port_for_codex.reconciliation import (  # noqa: E402
    build_complete_reconciliation_manifest,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gstack-repo", type=Path, required=True)
    parser.add_argument("--gbrain-repo", type=Path, required=True)
    parser.add_argument("--reviewed-at", default="2026-08-08")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    target = REPO_ROOT / "data/reconciliation-complete.json"
    manifest = build_complete_reconciliation_manifest(
        REPO_ROOT,
        {"gstack": args.gstack_repo, "gbrain": args.gbrain_repo},
        args.reviewed_at,
    )
    rendered = json.dumps(manifest, indent=2) + "\n"
    if args.check:
        if not target.exists() or target.read_text(encoding="utf-8") != rendered:
            print("Complete reconciliation manifest is stale.", file=sys.stderr)
            return 1
        print("Complete reconciliation manifest is current.")
        return 0

    target.write_text(rendered, encoding="utf-8")
    print(
        f"Wrote {target.relative_to(REPO_ROOT)} with {len(manifest['records'])} "
        f"canonical records and {len(manifest['alternate_source_records'])} "
        "alternate source record(s)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
