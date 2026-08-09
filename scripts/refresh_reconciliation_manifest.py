#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from gstack_port_for_codex.reconciliation import (  # noqa: E402
    refresh_reconciliation_manifest,
    resolve_repo_path,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Refresh reconciliation hashes, retention, and evaluators.")
    parser.add_argument("--gstack-repo", type=Path, required=True)
    parser.add_argument("--gbrain-repo", type=Path, required=True)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("data/reconciliation-alpha.json"),
        help="Manifest path relative to the repository root",
    )
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    target = resolve_repo_path(REPO_ROOT, args.manifest)
    manifest = json.loads(target.read_text(encoding="utf-8"))
    refreshed = refresh_reconciliation_manifest(
        manifest,
        REPO_ROOT,
        {"gstack": args.gstack_repo, "gbrain": args.gbrain_repo},
    )
    rendered = json.dumps(refreshed, indent=2) + "\n"
    relative_target = target.relative_to(REPO_ROOT.resolve())
    if args.check:
        if target.read_text(encoding="utf-8") != rendered:
            print(f"{manifest['milestone'].title()} reconciliation manifest is stale.", file=sys.stderr)
            return 1
        print(f"{manifest['milestone'].title()} reconciliation manifest is current.")
        return 0

    target.write_text(rendered, encoding="utf-8")
    print(f"Wrote {relative_target}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
