#!/usr/bin/env python3

from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from gstack_port_for_codex.registry import (  # noqa: E402
    format_capability_status_table,
    format_status_table,
    load_skill_map,
)


SKILL_MAPS = (
    ("GStack Core", REPO_ROOT / "data" / "skill-map.json"),
    ("GBrain Imports", REPO_ROOT / "data" / "gbrain-skill-map.json"),
    ("Praneet Extensions", REPO_ROOT / "data" / "praneet-skill-map.json"),
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
                    f"Baseline source: {source['name']} @ {source['commit']}",
                    "Per-skill source freshness appears in the Source column when a skill was ported from a newer upstream commit.",
                    format_status_table(skill_map),
                )
            )
        )

    impeccable_map = load_skill_map(REPO_ROOT / "data" / "impeccable-capability-map.json")
    impeccable_source = impeccable_map["source"]
    sections.append(
        "\n".join(
            (
                "Impeccable Integration",
                f"Baseline source: {impeccable_source['name']} @ {impeccable_source['commit']}",
                "Per-capability freshness appears in the Source column.",
                format_capability_status_table(impeccable_map),
            )
        )
    )

    print("\n\n".join(sections))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
