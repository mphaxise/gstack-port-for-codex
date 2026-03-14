from __future__ import annotations

from pathlib import Path
import sys
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from gstack_port_for_codex.registry import (  # noqa: E402
    extract_frontmatter_keys,
    format_status_table,
    load_skill_map,
    validate_repo,
    validate_skill_map,
)


class RegistryTests(unittest.TestCase):
    def test_extract_frontmatter_keys_reads_name_and_description(self) -> None:
        text = (
            "---\n"
            "name: demo-skill\n"
            "description: A short description.\n"
            "---\n"
            "\n"
            "# Demo\n"
        )

        self.assertEqual(
            extract_frontmatter_keys(text),
            {"name": "demo-skill", "description": "A short description."},
        )

    def test_validate_skill_map_rejects_duplicate_codex_slug(self) -> None:
        data = {
            "source": {
                "name": "gstack",
                "repo": "https://example.com",
                "license": "MIT",
                "commit": "abc123",
            },
            "skills": [
                {
                    "upstream_slug": "one",
                    "codex_slug": "shared",
                    "status": "planned",
                    "summary": "first",
                    "source_files": ["one/SKILL.md"],
                },
                {
                    "upstream_slug": "two",
                    "codex_slug": "shared",
                    "status": "planned",
                    "summary": "second",
                    "source_files": ["two/SKILL.md"],
                },
            ],
        }

        errors = validate_skill_map(data)
        self.assertTrue(any("Duplicate codex slug: shared." == error for error in errors))

    def test_validate_repo_passes_for_current_checkout(self) -> None:
        self.assertEqual(validate_repo(REPO_ROOT), [])

    def test_status_table_mentions_reference_port(self) -> None:
        skill_map = load_skill_map(REPO_ROOT / "data" / "skill-map.json")
        table = format_status_table(skill_map)

        self.assertIn("plan-ceo-review", table)
        self.assertIn("ported", table)


if __name__ == "__main__":
    unittest.main()
