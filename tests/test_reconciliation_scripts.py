from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
import importlib.util
import io
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]


def load_script(name: str):
    path = REPO_ROOT / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"test_{name}_script", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


build_script = load_script("build_complete_reconciliation")
inventory_script = load_script("build_skill_inventory")
refresh_script = load_script("refresh_reconciliation_manifest")
review_script = load_script("record_skill_review")
smoke_script = load_script("smoke_install")


class BuildSkillInventoryScriptTests(unittest.TestCase):
    def test_write_check_and_stale_paths(self) -> None:
        inventory = {"schema_version": 1, "scope": "public-packaged-skills", "entries": []}
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "data").mkdir()
            with (
                patch.object(inventory_script, "REPO_ROOT", root),
                patch.object(inventory_script, "build_canonical_inventory", return_value=inventory),
                patch.object(sys, "argv", ["build_skill_inventory.py"]),
                redirect_stdout(io.StringIO()) as output,
            ):
                self.assertEqual(inventory_script.main(), 0)
            self.assertIn("Wrote data/canonical-skill-inventory.json", output.getvalue())

            with (
                patch.object(inventory_script, "REPO_ROOT", root),
                patch.object(inventory_script, "build_canonical_inventory", return_value=inventory),
                patch.object(sys, "argv", ["build_skill_inventory.py", "--check"]),
                redirect_stdout(io.StringIO()) as output,
            ):
                self.assertEqual(inventory_script.main(), 0)
            self.assertIn("inventory is current", output.getvalue())

            (root / "data/canonical-skill-inventory.json").write_text("{}\n", encoding="utf-8")
            with (
                patch.object(inventory_script, "REPO_ROOT", root),
                patch.object(inventory_script, "build_canonical_inventory", return_value=inventory),
                patch.object(sys, "argv", ["build_skill_inventory.py", "--check"]),
                redirect_stderr(io.StringIO()) as error,
            ):
                self.assertEqual(inventory_script.main(), 1)
            self.assertIn("inventory is stale", error.getvalue())


class SmokeInstallScriptTests(unittest.TestCase):
    def test_main_runs_public_core_install(self) -> None:
        with redirect_stdout(io.StringIO()) as output:
            self.assertEqual(smoke_script.main(), 0)
        self.assertIn("Installer smoke test passed", output.getvalue())

    def test_main_rejects_missing_receipt(self) -> None:
        with TemporaryDirectory() as temp_dir:
            installed = Path(temp_dir) / "spec"
            installed.mkdir()
            (installed / "SKILL.md").write_text(
                "---\nname: spec\ndescription: Test.\n---\n", encoding="utf-8"
            )
            with (
                patch.object(smoke_script, "resolve_skills", return_value=["spec"]),
                patch.object(smoke_script, "install_skills", return_value=[installed]),
                redirect_stdout(io.StringIO()) as output,
            ):
                self.assertEqual(smoke_script.main(), 1)
        self.assertIn("missing ownership receipt", output.getvalue())


class BuildCompleteReconciliationScriptTests(unittest.TestCase):
    def test_write_and_check_current_manifest(self) -> None:
        manifest = {"records": [{"canonical_id": "skill:one"}], "alternate_source_records": []}
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "data").mkdir()
            argv = [
                "build_complete_reconciliation.py",
                "--gstack-repo",
                str(root / "gstack"),
                "--gbrain-repo",
                str(root / "gbrain"),
            ]
            with (
                patch.object(build_script, "REPO_ROOT", root),
                patch.object(build_script, "build_complete_reconciliation_manifest", return_value=manifest),
                patch.object(sys, "argv", argv),
                redirect_stdout(io.StringIO()) as output,
            ):
                self.assertEqual(build_script.main(), 0)
            self.assertIn("1 canonical records", output.getvalue())

            with (
                patch.object(build_script, "REPO_ROOT", root),
                patch.object(build_script, "build_complete_reconciliation_manifest", return_value=manifest),
                patch.object(sys, "argv", [*argv, "--check"]),
                redirect_stdout(io.StringIO()) as output,
            ):
                self.assertEqual(build_script.main(), 0)
            self.assertIn("manifest is current", output.getvalue())

    def test_check_reports_stale_manifest(self) -> None:
        manifest = {"records": [], "alternate_source_records": []}
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "data").mkdir()
            (root / "data/reconciliation-complete.json").write_text("{}\n", encoding="utf-8")
            argv = [
                "build_complete_reconciliation.py",
                "--gstack-repo",
                str(root / "gstack"),
                "--gbrain-repo",
                str(root / "gbrain"),
                "--check",
            ]
            with (
                patch.object(build_script, "REPO_ROOT", root),
                patch.object(build_script, "build_complete_reconciliation_manifest", return_value=manifest),
                patch.object(sys, "argv", argv),
                redirect_stderr(io.StringIO()) as error,
            ):
                self.assertEqual(build_script.main(), 1)
            self.assertIn("manifest is stale", error.getvalue())


class RefreshReconciliationScriptTests(unittest.TestCase):
    def test_write_and_check_current_manifest(self) -> None:
        original = {"milestone": "alpha", "records": []}
        refreshed = {"milestone": "alpha", "records": [{"canonical_id": "skill:one"}]}
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            target = root / "data/reconciliation-alpha.json"
            target.parent.mkdir()
            target.write_text(json.dumps(original) + "\n", encoding="utf-8")
            argv = [
                "refresh_reconciliation_manifest.py",
                "--gstack-repo",
                str(root / "gstack"),
                "--gbrain-repo",
                str(root / "gbrain"),
            ]
            with (
                patch.object(refresh_script, "REPO_ROOT", root),
                patch.object(refresh_script, "refresh_reconciliation_manifest", return_value=refreshed),
                patch.object(sys, "argv", argv),
                redirect_stdout(io.StringIO()) as output,
            ):
                self.assertEqual(refresh_script.main(), 0)
            self.assertIn("Wrote data/reconciliation-alpha.json", output.getvalue())

            with (
                patch.object(refresh_script, "REPO_ROOT", root),
                patch.object(refresh_script, "refresh_reconciliation_manifest", return_value=refreshed),
                patch.object(sys, "argv", [*argv, "--check"]),
                redirect_stdout(io.StringIO()) as output,
            ):
                self.assertEqual(refresh_script.main(), 0)
            self.assertIn("manifest is current", output.getvalue())

    def test_check_reports_stale_manifest(self) -> None:
        original = {"milestone": "beta", "records": []}
        refreshed = {"milestone": "beta", "records": [{"canonical_id": "skill:one"}]}
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            target = root / "data/reconciliation-beta.json"
            target.parent.mkdir()
            target.write_text(json.dumps(original) + "\n", encoding="utf-8")
            argv = [
                "refresh_reconciliation_manifest.py",
                "--gstack-repo",
                str(root / "gstack"),
                "--gbrain-repo",
                str(root / "gbrain"),
                "--manifest",
                "data/reconciliation-beta.json",
                "--check",
            ]
            with (
                patch.object(refresh_script, "REPO_ROOT", root),
                patch.object(refresh_script, "refresh_reconciliation_manifest", return_value=refreshed),
                patch.object(sys, "argv", argv),
                redirect_stderr(io.StringIO()) as error,
            ):
                self.assertEqual(refresh_script.main(), 1)
            self.assertIn("manifest is stale", error.getvalue())


class RecordSkillReviewScriptTests(unittest.TestCase):
    def test_write_and_check_current_review(self) -> None:
        data = {"source": {}, "skills": [{"upstream_slug": "accepted"}]}
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            target = root / "data/map.json"
            target.parent.mkdir()
            target.write_text(json.dumps(data) + "\n", encoding="utf-8")
            argv = [
                "record_skill_review.py",
                "--map",
                "data/map.json",
                "--reviewed-commit",
                "a" * 40,
                "--reviewed-at",
                "2026-08-08",
                "--adopted",
                "accepted",
            ]
            with (
                patch.object(review_script, "REPO_ROOT", root),
                patch.object(sys, "argv", argv),
                redirect_stdout(io.StringIO()) as output,
            ):
                self.assertEqual(review_script.main(), 0)
            self.assertIn("Wrote data/map.json", output.getvalue())

            with (
                patch.object(review_script, "REPO_ROOT", root),
                patch.object(sys, "argv", [*argv, "--check"]),
                redirect_stdout(io.StringIO()) as output,
            ):
                self.assertEqual(review_script.main(), 0)
            self.assertIn("metadata is current", output.getvalue())

    def test_check_reports_stale_review(self) -> None:
        data = {"source": {}, "skills": [{"upstream_slug": "accepted"}]}
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            target = root / "data/map.json"
            target.parent.mkdir()
            target.write_text(json.dumps(data) + "\n", encoding="utf-8")
            argv = [
                "record_skill_review.py",
                "--map",
                "data/map.json",
                "--reviewed-commit",
                "a" * 40,
                "--adopted",
                "accepted",
                "--check",
            ]
            with (
                patch.object(review_script, "REPO_ROOT", root),
                patch.object(sys, "argv", argv),
                redirect_stdout(io.StringIO()) as output,
            ):
                self.assertEqual(review_script.main(), 1)
            self.assertIn("metadata is stale", output.getvalue())


if __name__ == "__main__":
    unittest.main()
