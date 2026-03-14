#!/usr/bin/env python3

from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from gstack_port_for_codex.registry import format_status_table, load_skill_map  # noqa: E402


def main() -> int:
    skill_map = load_skill_map(REPO_ROOT / "data" / "skill-map.json")
    print(format_status_table(skill_map))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

