#!/usr/bin/env python3
"""Install selected public Codex skills into a local skills directory."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPO_ROOT / "skills"
INSTALL_RECEIPT = ".gstack-port-for-codex-install.json"
PACKAGE_ID = "mphaxise/gstack-port-for-codex"


def _safe_target_file(target: Path, relative: str) -> Path:
    relative_path = Path(relative)
    if relative_path.is_absolute() or ".." in relative_path.parts:
        raise FileExistsError(f"Unsafe path in install receipt: {relative!r}.")
    candidate = target / relative_path
    try:
        candidate.parent.resolve(strict=False).relative_to(target.resolve())
    except ValueError as exc:
        raise FileExistsError(
            f"Unsafe symlinked parent in install target: {candidate}."
        ) from exc
    return candidate


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
        target_exists = target.exists() or target.is_symlink()
        if target_exists and not force:
            raise FileExistsError(
                f"Skill already exists at {target}; use --force to update it."
            )
        source_files = {
            path.relative_to(source).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in source.rglob("*")
            if path.is_file()
        }
        if target_exists:
            receipt_path = target / INSTALL_RECEIPT
            if target.is_symlink() or not receipt_path.is_file():
                raise FileExistsError(
                    f"Refusing to overwrite unowned skill at {target}; "
                    "install to another destination or remove it explicitly."
                )
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            if receipt.get("package") != PACKAGE_ID or receipt.get("slug") != slug:
                raise FileExistsError(f"Refusing to overwrite unowned skill at {target}.")
            previous_files = receipt.get("files", {})
            if not isinstance(previous_files, dict):
                raise FileExistsError(f"Invalid install receipt at {receipt_path}.")
            for relative, new_hash in source_files.items():
                existing_path = _safe_target_file(target, relative)
                if not (existing_path.is_file() or existing_path.is_symlink()):
                    continue
                if existing_path.is_symlink():
                    raise FileExistsError(
                        f"Refusing to overwrite symlinked file at {existing_path}."
                    )
                if relative not in previous_files:
                    raise FileExistsError(
                        f"Refusing to overwrite unowned file at {existing_path}."
                    )
                actual_hash = hashlib.sha256(existing_path.read_bytes()).hexdigest()
                if actual_hash not in {previous_files[relative], new_hash}:
                    raise FileExistsError(
                        f"Refusing to overwrite locally modified file at {existing_path}."
                    )
            for relative in sorted(set(previous_files) - set(source_files)):
                stale_path = _safe_target_file(target, relative)
                if stale_path.is_symlink():
                    raise FileExistsError(
                        f"Refusing to remove symlinked stale file at {stale_path}."
                    )
                if (
                    stale_path.is_file()
                    and hashlib.sha256(stale_path.read_bytes()).hexdigest()
                    == previous_files[relative]
                ):
                    stale_path.unlink()
                    parent = stale_path.parent
                    while parent != target:
                        try:
                            parent.rmdir()
                        except OSError:
                            break
                        parent = parent.parent

        shutil.copytree(source, target, dirs_exist_ok=target_exists)
        receipt = {
            "schema_version": 1,
            "package": PACKAGE_ID,
            "slug": slug,
            "files": source_files,
        }
        (target / INSTALL_RECEIPT).write_text(
            json.dumps(receipt, indent=2) + "\n", encoding="utf-8"
        )
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
    default_destination = Path.home() / ".agents" / "skills"
    parser.add_argument(
        "--dest",
        type=Path,
        default=default_destination,
        help=f"Destination directory (default: {default_destination}).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Update only skill directories previously installed by this package.",
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
