#!/usr/bin/env python3

from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from gstack_port_for_codex.registry import format_status_table, load_skill_map  # noqa: E402


SKILL_MAPS = (
    ("GStack Core", REPO_ROOT / "data" / "skill-map.json"),
    ("GBrain Imports", REPO_ROOT / "data" / "gbrain-skill-map.json"),
)


def main() -> int:
    sections: list[str] = []
    for title, path in SKILL_MAPS:
        skill_map = load_skill_map(path)
        source = skill_map["source"]
        sections.append(
            "\n".join(
                (
                    title,
                    f"Source: {source['name']} @ {source['commit']}",
                    format_status_table(skill_map),
                )
            )
        )

    print("\n\n".join(sections))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
