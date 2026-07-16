from __future__ import annotations

from pathlib import Path
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from gstack_port_for_codex.brain import (  # noqa: E402
    BRAIN_DIRS,
    audit_citations,
    parse_brain_page,
    render_page,
    sync_source_projection,
)


class BrainSyncSourceTests(unittest.TestCase):
    def test_create_managed_projection_with_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "living-note.md"
            source.write_text("# Living Note\n\nStable current truth.\n", encoding="utf-8")

            result = sync_source_projection(
                root / "brain",
                source,
                title="Living Note",
                sync_date="2026-07-15",
                tags=["identity"],
            )
            page = parse_brain_page(result.path)
            expected_hash = hashlib.sha256(source.read_bytes()).hexdigest()

            self.assertEqual(result.status, "created")
            self.assertEqual(result.version, 1)
            self.assertEqual(result.source_path, source.resolve())
            self.assertEqual(page.frontmatter["source_sha256"], expected_hash)
            self.assertEqual(page.frontmatter["source_version"], "1")
            self.assertEqual(page.frontmatter["first_synced"], "2026-07-15")
            self.assertEqual(page.frontmatter["last_changed"], "2026-07-15")
            self.assertIn(str(source.resolve()), page.compiled_truth)
            self.assertIn("> Stable current truth.", page.compiled_truth)
            self.assertIn("synced-source", page.frontmatter["tags"])
            self.assertIn("identity", page.frontmatter["tags"])
            self.assertEqual(audit_citations(root / "brain"), [])

    def test_changed_source_replaces_truth_and_records_supersession(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "mutable.md"
            source.write_text("Old compiled truth.\n", encoding="utf-8")
            first = sync_source_projection(root / "brain", source, sync_date="2026-07-15")
            old_hash = first.source_sha256

            source.write_text("New compiled truth.\n", encoding="utf-8")
            second = sync_source_projection(root / "brain", source, sync_date="2026-07-16")
            page = parse_brain_page(second.path)

            self.assertEqual(second.status, "updated")
            self.assertEqual(second.version, 2)
            self.assertNotEqual(second.source_sha256, old_hash)
            self.assertIn("New compiled truth", page.compiled_truth)
            self.assertNotIn("Old compiled truth", page.compiled_truth)
            self.assertIn(f"superseded version 1 (`{old_hash}`)", page.timeline)
            self.assertIn(second.source_sha256, page.timeline)
            self.assertEqual(page.frontmatter["supersedes_sha256"], old_hash)
            self.assertEqual(page.frontmatter["last_changed"], "2026-07-16")
            self.assertEqual(audit_citations(root / "brain"), [])

    def test_unchanged_source_is_byte_for_byte_no_op(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "stable.md"
            source.write_text("Stable content.\n", encoding="utf-8")
            first = sync_source_projection(root / "brain", source, sync_date="2026-07-15")
            before = first.path.read_bytes()

            second = sync_source_projection(root / "brain", source, sync_date="2026-07-31")

            self.assertEqual(second.status, "no-op")
            self.assertEqual(second.version, 1)
            self.assertEqual(second.path.read_bytes(), before)

    def test_cli_prints_machine_readable_status(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "cli-source.md"
            source.write_text("CLI source.\n", encoding="utf-8")
            command = [
                sys.executable,
                str(REPO_ROOT / "scripts" / "brain_sync_source.py"),
                str(source),
                "--brain-root",
                str(root / "brain"),
                "--title",
                "CLI Source",
                "--category",
                "sources",
                "--tag",
                "cli-test",
                "--date",
                "2026-07-15",
                "--json",
            ]

            created = subprocess.run(command, check=True, capture_output=True, text=True)
            no_op = subprocess.run(command, check=True, capture_output=True, text=True)

            created_payload = json.loads(created.stdout)
            self.assertEqual(created_payload["status"], "created")
            self.assertEqual(created_payload["source_path"], str(source.resolve()))
            self.assertEqual(json.loads(no_op.stdout)["status"], "no-op")

    def test_generated_brain_outputs_are_ignored_but_readme_is_tracked(self) -> None:
        private_paths = [f"brain/{directory}/private.md" for directory in BRAIN_DIRS]
        private_paths.extend(
            (
                "brain/.raw/private.txt",
                "brain/_dead-letter/private.json",
                "brain/future-private-category/private.md",
            )
        )
        for relative_path in private_paths:
            with self.subTest(path=relative_path):
                result = subprocess.run(
                    ["git", "check-ignore", "--quiet", "--no-index", relative_path],
                    cwd=REPO_ROOT,
                    check=False,
                )
                self.assertEqual(result.returncode, 0)

        readme_result = subprocess.run(
            ["git", "check-ignore", "--quiet", "--no-index", "brain/README.md"],
            cwd=REPO_ROOT,
            check=False,
        )
        self.assertEqual(readme_result.returncode, 1)
        tracked = subprocess.run(
            ["git", "ls-files", "--error-unmatch", "brain/README.md"],
            cwd=REPO_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(tracked.returncode, 0)

    def test_missing_and_invalid_inputs_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            brain_root = root / "brain"

            with self.assertRaisesRegex(FileNotFoundError, "does not exist"):
                sync_source_projection(brain_root, root / "missing.md")

            with self.assertRaisesRegex(ValueError, "not a regular file"):
                sync_source_projection(brain_root, root)

            empty = root / "empty.md"
            empty.write_text("  \n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "empty"):
                sync_source_projection(brain_root, empty)

            binary = root / "binary.md"
            binary.write_bytes(b"\xff\xfe")
            with self.assertRaisesRegex(ValueError, "not valid UTF-8"):
                sync_source_projection(brain_root, binary)

            valid = root / "valid.md"
            valid.write_text("Valid source.\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "YYYY-MM-DD"):
                sync_source_projection(brain_root, valid, sync_date="07/15/2026")

    def test_refuses_to_overwrite_unmanaged_or_different_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            brain_root = root / "brain"
            source = root / "one.md"
            source.write_text("One.\n", encoding="utf-8")
            result = sync_source_projection(brain_root, source, title="Shared", sync_date="2026-07-15")

            other = root / "two.md"
            other.write_text("Two.\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "different source"):
                sync_source_projection(brain_root, other, title="Shared", sync_date="2026-07-16")

            result.path.write_text(
                render_page("Shared", "source", "Manual truth. [Source: notes, 2026-07-15]"),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "unmanaged"):
                sync_source_projection(brain_root, source, title="Shared", sync_date="2026-07-16")


if __name__ == "__main__":
    unittest.main()
