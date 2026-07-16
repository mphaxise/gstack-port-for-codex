#!/usr/bin/env python3

from pathlib import Path
import argparse
import json
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from gstack_port_for_codex.brain import DEFAULT_BRAIN_ROOT, sync_source_projection  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Synchronize a mutable UTF-8 local source into a managed local Codex brain projection."
    )
    parser.add_argument("input_file", type=Path, help="Mutable local source file to synchronize")
    parser.add_argument("--title", help="Projection title; defaults to the file stem")
    parser.add_argument("--category", default="sources", help="Destination brain category")
    parser.add_argument("--date", dest="sync_date", help="Synchronization date in YYYY-MM-DD form")
    parser.add_argument("--tag", action="append", default=[], help="Tag to add to the managed projection")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Print a machine-readable result")
    parser.add_argument(
        "--brain-root",
        type=Path,
        default=REPO_ROOT / DEFAULT_BRAIN_ROOT,
        help="Brain root; defaults to this repository's ignored local brain directory",
    )
    args = parser.parse_args()

    try:
        result = sync_source_projection(
            args.brain_root,
            args.input_file,
            title=args.title,
            category=args.category,
            sync_date=args.sync_date,
            tags=args.tag,
        )
    except (FileNotFoundError, OSError, ValueError) as exc:
        parser.error(str(exc))

    payload = {
        "path": str(result.path),
        "source_path": str(result.source_path),
        "source_sha256": result.source_sha256,
        "status": result.status,
        "version": result.version,
    }
    if args.as_json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"Source projection: {result.path}")
        print(f"Canonical source: {result.source_path}")
        print(f"Status: {result.status}")
        print(f"Version: {result.version}")
        print(f"SHA-256: {result.source_sha256}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
