#!/usr/bin/env python3
"""Install selected public Codex skills into a local skills directory."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPO_ROOT / "skills"

CORE_SKILLS = (
    "gstack",
    "workflow-router",
    "autoplan",
    "office-hours",
    "spec",
    "plan-ceo-review",
    "plan-eng-review",
    "plan-design-review",
    "plan-devex-review",
    "investigate",
    "repo-architecture",
    "testing",
    "qa",
    "review",
    "ship",
)
EXTENSION_SKILLS = (
    "responsible-design-review",
    "accessibility-review",
    "research-synthesis",
    "startup-memo",
    "market-map",
    "design-leadership-review",
    "outcome-memory",
)


def available_skills(skills_root: Path = SKILLS_ROOT) -> list[str]:
    return sorted(
        path.name
        for path in skills_root.iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    )


def resolve_skills(
    bundle: str | None = None,
    requested: list[str] | None = None,
    skills_root: Path = SKILLS_ROOT,
) -> list[str]:
    if bundle and requested:
        raise ValueError("Choose --bundle or --skill, not both.")

    if requested:
        slugs = requested
    elif bundle == "core":
        slugs = list(CORE_SKILLS)
    elif bundle == "extensions":
        slugs = list(EXTENSION_SKILLS)
    elif bundle == "all":
        slugs = available_skills(skills_root)
    else:
        slugs = list(CORE_SKILLS)

    available = set(available_skills(skills_root))
    unknown = sorted(set(slugs) - available)
    if unknown:
        raise ValueError(f"Unknown or unavailable skill(s): {', '.join(unknown)}")

    return list(dict.fromkeys(slugs))


def install_skills(
    destination: Path,
    slugs: list[str],
    skills_root: Path = SKILLS_ROOT,
    force: bool = False,
) -> list[Path]:
    destination.mkdir(parents=True, exist_ok=True)
    installed: list[Path] = []
    for slug in slugs:
        source = skills_root / slug
        target = destination / slug
        if target.exists() and not force:
            raise FileExistsError(
                f"Skill already exists at {target}; use --force to update it."
            )
        shutil.copytree(source, target, dirs_exist_ok=force)
        installed.append(target)
    return installed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--bundle",
        choices=("core", "extensions", "all"),
        help="Public bundle to install. Defaults to core.",
    )
    parser.add_argument(
        "--skill",
        action="append",
        dest="skills",
        help="Install one named skill; repeat for multiple skills.",
    )
    default_destination = Path.home() / ".codex" / "skills"
    codex_home = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
    parser.add_argument(
        "--dest",
        type=Path,
        default=codex_home / "skills",
        help=f"Destination directory (default: {default_destination}).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Update existing skill directories without deleting other files.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        slugs = resolve_skills(args.bundle, args.skills)
        installed = install_skills(args.dest.expanduser(), slugs, force=args.force)
    except (FileExistsError, OSError, ValueError) as exc:
        print(f"Installation failed: {exc}", file=sys.stderr)
        return 1

    print(f"Installed {len(installed)} skill(s) into {args.dest.expanduser()}")
    for path in installed:
        print(f"- {path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
