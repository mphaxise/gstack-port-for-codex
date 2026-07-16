#!/usr/bin/env python3

from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from gstack_port_for_codex.brain import DEFAULT_BRAIN_ROOT, BRAIN_DIRS, ensure_brain_root  # noqa: E402


def main() -> int:
    brain_root = REPO_ROOT / DEFAULT_BRAIN_ROOT
    ensure_brain_root(brain_root)

    print(f"Brain root ready: {brain_root}")
    for directory in BRAIN_DIRS:
        print(f"- {brain_root / directory}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
