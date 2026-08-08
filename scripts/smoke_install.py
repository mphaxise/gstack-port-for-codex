#!/usr/bin/env python3
"""Exercise the public installer in an isolated temporary directory."""

from __future__ import annotations

from pathlib import Path
import sys
import tempfile


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(REPO_ROOT / "src"))

from install_skills import INSTALL_RECEIPT, install_skills, resolve_skills  # noqa: E402
from gstack_port_for_codex.registry import extract_frontmatter_keys  # noqa: E402


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="gstack-install-") as temp_dir:
        destination = Path(temp_dir) / "skills"
        slugs = resolve_skills("core")
        installed = install_skills(destination, slugs)
        if len(installed) != len(slugs):
            print("Installer smoke test failed: incomplete install.")
            return 1

        for path in installed:
            skill_file = path / "SKILL.md"
            frontmatter = extract_frontmatter_keys(skill_file.read_text(encoding="utf-8"))
            if frontmatter.get("name") != path.name:
                print(f"Installer smoke test failed: invalid frontmatter in {skill_file}.")
                return 1
            if not (path / INSTALL_RECEIPT).is_file():
                print(f"Installer smoke test failed: missing ownership receipt in {path}.")
                return 1

        private_slug = "prescriptive" + "-opencode-" + "delegation"
        if (destination / private_slug).exists():
            print("Installer smoke test failed: private delegation skill was installed.")
            return 1

    print(f"Installer smoke test passed for {len(slugs)} core skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
