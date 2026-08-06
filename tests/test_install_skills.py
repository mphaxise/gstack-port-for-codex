from pathlib import Path
from tempfile import TemporaryDirectory
import sys
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from install_skills import install_skills, resolve_skills  # noqa: E402


class InstallSkillsTests(unittest.TestCase):
    def test_core_bundle_contains_coding_workflow_entries(self) -> None:
        slugs = resolve_skills("core")
        self.assertIn("workflow-router", slugs)
        self.assertIn("plan-eng-review", slugs)
        self.assertIn("testing", slugs)
        self.assertNotIn("prescriptive" + "-opencode-" + "delegation", slugs)

    def test_extensions_bundle_is_public_only(self) -> None:
        slugs = resolve_skills("extensions")
        self.assertEqual(len(slugs), 7)
        self.assertNotIn("prescriptive" + "-opencode-" + "delegation", slugs)

    def test_named_install_refuses_overwrite_without_force(self) -> None:
        with TemporaryDirectory() as temp_dir:
            destination = Path(temp_dir) / "skills"
            install_skills(destination, ["spec"])
            with self.assertRaises(FileExistsError):
                install_skills(destination, ["spec"])

    def test_force_install_updates_existing_skill(self) -> None:
        with TemporaryDirectory() as temp_dir:
            destination = Path(temp_dir) / "skills"
            install_skills(destination, ["spec"])
            install_skills(destination, ["spec"], force=True)
            self.assertTrue((destination / "spec" / "SKILL.md").exists())


if __name__ == "__main__":
    unittest.main()
