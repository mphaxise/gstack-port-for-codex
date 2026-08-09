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

    def test_force_install_rejects_unsafe_receipt_path(self) -> None:
        with TemporaryDirectory() as temp_dir:
            destination = Path(temp_dir) / "skills"
            target = install_skills(destination, ["spec"])[0]
            receipt_path = target / INSTALL_RECEIPT
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            receipt["files"]["../outside.txt"] = hashlib.sha256(b"outside\n").hexdigest()
            receipt_path.write_text(json.dumps(receipt), encoding="utf-8")

            with self.assertRaisesRegex(FileExistsError, "Unsafe path"):
                install_skills(destination, ["spec"], force=True)

    def test_force_install_rejects_symlinked_receipt_parent(self) -> None:
        with TemporaryDirectory() as temp_dir:
            destination = Path(temp_dir) / "skills"
            target = install_skills(destination, ["spec"])[0]
            external = Path(temp_dir) / "external"
            external.mkdir()
            (target / "linked").symlink_to(external, target_is_directory=True)
            receipt_path = target / INSTALL_RECEIPT
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            receipt["files"]["linked/stale.txt"] = hashlib.sha256(b"stale\n").hexdigest()
            receipt_path.write_text(json.dumps(receipt), encoding="utf-8")

            with self.assertRaisesRegex(FileExistsError, "symlinked parent"):
                install_skills(destination, ["spec"], force=True)

    def test_force_install_refuses_symlink_replacing_stale_receipted_file(self) -> None:
        with TemporaryDirectory() as temp_dir:
            source_root = Path(temp_dir) / "source"
            source_skill = source_root / "demo"
            source_skill.mkdir(parents=True)
            (source_skill / "SKILL.md").write_text("skill\n", encoding="utf-8")
            (source_skill / "stale.txt").write_text("managed\n", encoding="utf-8")
            destination = Path(temp_dir) / "skills"
            target = install_skills(destination, ["demo"], skills_root=source_root)[0]

            (source_skill / "stale.txt").unlink()
            (target / "stale.txt").unlink()
            external = Path(temp_dir) / "external.txt"
            external.write_text("user file\n", encoding="utf-8")
            (target / "stale.txt").symlink_to(external)

            with self.assertRaisesRegex(FileExistsError, "symlinked stale file"):
                install_skills(destination, ["demo"], skills_root=source_root, force=True)

            self.assertEqual(external.read_text(encoding="utf-8"), "user file\n")

    def test_force_install_rejects_invalid_receipt_files(self) -> None:
        with TemporaryDirectory() as temp_dir:
            destination = Path(temp_dir) / "skills"
            target = install_skills(destination, ["spec"])[0]
            receipt_path = target / INSTALL_RECEIPT
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            receipt["files"] = []
            receipt_path.write_text(json.dumps(receipt), encoding="utf-8")

            with self.assertRaisesRegex(FileExistsError, "Invalid install receipt"):
                install_skills(destination, ["spec"], force=True)

    def test_force_install_rejects_mismatched_receipt_identity(self) -> None:
        with TemporaryDirectory() as temp_dir:
            destination = Path(temp_dir) / "skills"
            target = install_skills(destination, ["spec"])[0]
            receipt_path = target / INSTALL_RECEIPT
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            receipt["slug"] = "another-skill"
            receipt_path.write_text(json.dumps(receipt), encoding="utf-8")

            with self.assertRaisesRegex(FileExistsError, "unowned skill"):
                install_skills(destination, ["spec"], force=True)

    def test_force_install_rejects_unowned_file_at_packaged_path(self) -> None:
        with TemporaryDirectory() as temp_dir:
            source_root = Path(temp_dir) / "source"
            source_skill = source_root / "demo"
            source_skill.mkdir(parents=True)
            (source_skill / "SKILL.md").write_text("upstream\n", encoding="utf-8")
            destination = Path(temp_dir) / "skills"
            target = install_skills(destination, ["demo"], skills_root=source_root)[0]
            receipt_path = target / INSTALL_RECEIPT
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            receipt["files"].pop("SKILL.md")
            receipt_path.write_text(json.dumps(receipt), encoding="utf-8")

            with self.assertRaisesRegex(FileExistsError, "unowned file"):
                install_skills(destination, ["demo"], skills_root=source_root, force=True)


if __name__ == "__main__":
    unittest.main()
