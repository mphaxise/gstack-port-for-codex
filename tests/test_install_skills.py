from pathlib import Path
from tempfile import TemporaryDirectory
import hashlib
import json
import sys
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from install_skills import INSTALL_RECEIPT, install_skills, resolve_skills  # noqa: E402


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
            self.assertTrue((destination / "spec" / INSTALL_RECEIPT).exists())

    def test_force_install_refuses_unowned_existing_skill(self) -> None:
        with TemporaryDirectory() as temp_dir:
            destination = Path(temp_dir) / "skills"
            target = destination / "spec"
            target.mkdir(parents=True)
            (target / "SKILL.md").write_text("user owned\n", encoding="utf-8")

            with self.assertRaisesRegex(FileExistsError, "unowned skill"):
                install_skills(destination, ["spec"], force=True)

            self.assertEqual(
                (target / "SKILL.md").read_text(encoding="utf-8"), "user owned\n"
            )

    def test_force_install_removes_only_stale_receipted_files(self) -> None:
        with TemporaryDirectory() as temp_dir:
            destination = Path(temp_dir) / "skills"
            target = install_skills(destination, ["spec"])[0]
            receipt_path = target / INSTALL_RECEIPT
            (target / "stale.txt").write_text("old\n", encoding="utf-8")
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            receipt["files"]["stale.txt"] = hashlib.sha256(b"old\n").hexdigest()
            receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
            (target / "user-note.txt").write_text("keep\n", encoding="utf-8")

            install_skills(destination, ["spec"], force=True)

            self.assertFalse((target / "stale.txt").exists())
            self.assertTrue((target / "user-note.txt").exists())

    def test_force_install_refuses_locally_modified_receipted_file(self) -> None:
        with TemporaryDirectory() as temp_dir:
            destination = Path(temp_dir) / "skills"
            target = install_skills(destination, ["spec"])[0]
            (target / "SKILL.md").write_text("local edit\n", encoding="utf-8")

            with self.assertRaisesRegex(FileExistsError, "locally modified"):
                install_skills(destination, ["spec"], force=True)

            self.assertEqual(
                (target / "SKILL.md").read_text(encoding="utf-8"), "local edit\n"
            )

    def test_force_install_refuses_symlinked_receipted_file(self) -> None:
        with TemporaryDirectory() as temp_dir:
            destination = Path(temp_dir) / "skills"
            target = install_skills(destination, ["spec"])[0]
            external = Path(temp_dir) / "external.md"
            external.write_bytes((target / "SKILL.md").read_bytes())
            (target / "SKILL.md").unlink()
            (target / "SKILL.md").symlink_to(external)

            with self.assertRaisesRegex(FileExistsError, "symlinked file"):
                install_skills(destination, ["spec"], force=True)

            self.assertEqual(
                external.read_bytes(),
                (REPO_ROOT / "skills/spec/SKILL.md").read_bytes(),
            )


if __name__ == "__main__":
    unittest.main()
