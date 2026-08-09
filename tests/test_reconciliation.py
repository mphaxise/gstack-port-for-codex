from __future__ import annotations

import copy
from collections import Counter
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from gstack_port_for_codex.reconciliation import (  # noqa: E402
    build_canonical_inventory,
    evaluate_routing_jsonl,
    normalized_line_retention,
    validate_canonical_inventory,
    validate_reconciliation_manifest,
)
import gstack_port_for_codex.reconciliation as reconciliation  # noqa: E402


def init_test_repo(repo: Path) -> None:
    repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    subprocess.run(
        ["git", "config", "user.email", "tests@example.invalid"],
        cwd=repo,
        check=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test Suite"],
        cwd=repo,
        check=True,
    )


def commit_test_file(
    repo: Path, path: str, text: str, message: str, empty_hooks: Path
) -> str:
    target = repo / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    subprocess.run(["git", "add", path], cwd=repo, check=True)
    subprocess.run(
        [
            "git",
            "-c",
            "commit.gpgsign=false",
            "-c",
            f"core.hooksPath={empty_hooks}",
            "commit",
            "-q",
            "-m",
            message,
        ],
        cwd=repo,
        check=True,
    )
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


class ReconciliationTests(unittest.TestCase):
    def test_line_retention_uses_nonblank_multiset_overlap(self) -> None:
        source = "one\ntwo\ntwo\n\nthree\n"
        target = "two\ntwo\nfour\n"
        self.assertEqual(normalized_line_retention(source, target), 50.0)

    def test_line_retention_treats_empty_source_as_fully_retained(self) -> None:
        self.assertEqual(normalized_line_retention("\n", "anything\n"), 100.0)

    def test_git_blob_batch_rejects_unsafe_specs_before_subprocess(self) -> None:
        unsafe_requests = [
            [("-c core.pager=cat", "SKILL.md")],
            [("a" * 40, "skills/one/SKILL.md\n" + "b" * 40 + ":secret")],
        ]
        for requests in unsafe_requests:
            with (
                self.subTest(requests=requests),
                patch.object(reconciliation.subprocess, "run") as run,
                self.assertRaises(ValueError),
            ):
                reconciliation.git_blob_text_batch(Path("/tmp/upstream"), requests)
            run.assert_not_called()

    def test_repository_path_resolution_rejects_traversal_and_symlink_escape(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "repo"
            outside = Path(temp_dir) / "outside"
            root.mkdir()
            outside.mkdir()
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            (root / "safe.txt").write_text("safe\n", encoding="utf-8")
            (root / "private.env").write_text("private\n", encoding="utf-8")
            subprocess.run(["git", "add", "safe.txt"], cwd=root, check=True)
            (root / "escape").symlink_to(outside, target_is_directory=True)

            self.assertEqual(
                reconciliation.resolve_tracked_repo_path(root, "safe.txt"),
                (root / "safe.txt").resolve(),
            )
            with self.assertRaises(ValueError):
                reconciliation.resolve_tracked_repo_path(root, "private.env")
            subprocess.run(["git", "add", "private.env"], cwd=root, check=True)
            self.assertEqual(
                reconciliation.resolve_tracked_repo_path(root, "private.env"),
                (root / "private.env").resolve(),
            )
            for path in (
                "../outside/secret",
                "escape/secret",
                "/tmp/secret",
                None,
                7,
                False,
            ):
                with self.subTest(path=path), self.assertRaises(ValueError):
                    reconciliation.resolve_repo_path(root, path)

    def test_canonical_inventory_covers_every_packaged_skill(self) -> None:
        inventory = build_canonical_inventory(REPO_ROOT)
        packaged = list((REPO_ROOT / "skills").glob("*/SKILL.md"))
        self.assertEqual(len(inventory["entries"]), len(packaged))
        self.assertEqual(validate_canonical_inventory(inventory, REPO_ROOT), [])

    def test_canonical_inventory_ignores_untracked_skills_and_rejects_symlinks(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "repo"
            init_test_repo(root)
            (root / "data").mkdir()
            for map_name in (
                "skill-map.json",
                "gbrain-skill-map.json",
                "praneet-skill-map.json",
            ):
                (root / "data" / map_name).write_text(
                    json.dumps({"source": {}, "skills": []}), encoding="utf-8"
                )
            (root / "skills/tracked").mkdir(parents=True)
            (root / "skills/tracked/SKILL.md").write_text(
                "tracked\n", encoding="utf-8"
            )
            (root / "skills/ignored").mkdir(parents=True)
            (root / "skills/ignored/SKILL.md").write_text(
                "ignored private text\n", encoding="utf-8"
            )
            subprocess.run(
                ["git", "add", "skills/tracked/SKILL.md"], cwd=root, check=True
            )

            inventory = build_canonical_inventory(root)

            self.assertEqual(
                [entry["skill_name"] for entry in inventory["entries"]], ["tracked"]
            )

            outside = Path(temp_dir) / "outside.md"
            outside.write_text("outside private text\n", encoding="utf-8")
            (root / "skills/linked").mkdir()
            (root / "skills/linked/SKILL.md").symlink_to(outside)
            subprocess.run(
                ["git", "add", "skills/linked/SKILL.md"], cwd=root, check=True
            )

            with self.assertRaises(ValueError):
                build_canonical_inventory(root)

    def test_tracked_canonical_inventory_is_current(self) -> None:
        inventory = json.loads(
            (REPO_ROOT / "data" / "canonical-skill-inventory.json").read_text(encoding="utf-8")
        )
        self.assertEqual(validate_canonical_inventory(inventory, REPO_ROOT), [])

    def test_alpha_manifest_is_structurally_valid_and_hash_current(self) -> None:
        inventory = json.loads(
            (REPO_ROOT / "data" / "canonical-skill-inventory.json").read_text(encoding="utf-8")
        )
        manifest = json.loads(
            (REPO_ROOT / "data" / "reconciliation-alpha.json").read_text(encoding="utf-8")
        )
        self.assertEqual(validate_reconciliation_manifest(manifest, REPO_ROOT, inventory), [])
        self.assertEqual(len(manifest["records"]), 6)

    def test_alpha_manifest_rejects_unexplained_removal_and_missing_companion(self) -> None:
        inventory = json.loads(
            (REPO_ROOT / "data" / "canonical-skill-inventory.json").read_text(encoding="utf-8")
        )
        manifest = json.loads(
            (REPO_ROOT / "data" / "reconciliation-alpha.json").read_text(encoding="utf-8")
        )
        invalid = copy.deepcopy(manifest)
        invalid["records"][0]["intentional_removals"] = []
        invalid["records"][0]["companion_resources"] = ["missing/example.md"]

        errors = validate_reconciliation_manifest(invalid, REPO_ROOT, inventory)

        self.assertTrue(any("lacks its removal manifest" in error for error in errors))
        self.assertTrue(any("missing companion resource" in error for error in errors))

    def test_beta_manifest_tracks_preserved_resource_and_structured_outcomes(self) -> None:
        inventory = json.loads(
            (REPO_ROOT / "data" / "canonical-skill-inventory.json").read_text(encoding="utf-8")
        )
        manifest = json.loads(
            (REPO_ROOT / "data" / "reconciliation-beta.json").read_text(encoding="utf-8")
        )

        self.assertEqual(validate_reconciliation_manifest(manifest, REPO_ROOT, inventory), [])
        self.assertEqual(len(manifest["records"]), 2)
        self.assertEqual(
            manifest["resource_records"][0]["hashes"]["local_sha256"],
            manifest["resource_records"][0]["hashes"]["current_upstream_sha256"],
        )
        self.assertEqual(manifest["evaluations"][0]["case_count"], 6)
        self.assertTrue(all(manifest["evaluations"][0]["outcomes"].values()))

    def test_beta_manifest_rejects_resource_and_evaluator_drift(self) -> None:
        inventory = json.loads(
            (REPO_ROOT / "data" / "canonical-skill-inventory.json").read_text(encoding="utf-8")
        )
        manifest = json.loads(
            (REPO_ROOT / "data" / "reconciliation-beta.json").read_text(encoding="utf-8")
        )
        invalid = copy.deepcopy(manifest)
        invalid["resource_records"][0]["hashes"]["local_sha256"] = "0" * 64
        invalid["evaluations"][0]["case_count"] = 5
        invalid["evaluations"][0]["outcomes"]["valid_jsonl"] = False

        errors = validate_reconciliation_manifest(invalid, REPO_ROOT, inventory)

        self.assertTrue(any("resource hash drift" in error for error in errors))
        self.assertTrue(any("case count drift" in error for error in errors))
        self.assertTrue(any("outcome drift" in error for error in errors))

    def test_routing_evaluator_reports_malformed_ambiguity_without_crashing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            fixture = Path(temp_dir) / "routing.jsonl"
            fixture.write_text(
                '{"intent":"route this","expected_skill":"brain-taxonomist","ambiguous_with":7}\n',
                encoding="utf-8",
            )

            case_count, outcomes = evaluate_routing_jsonl(fixture, REPO_ROOT)

        self.assertEqual(case_count, 1)
        self.assertFalse(outcomes["valid_jsonl"])

    def test_refresh_updates_local_upstream_resource_and_evaluation_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "skills/local").mkdir(parents=True)
            (root / "skills/local/SKILL.md").write_text("local text\n", encoding="utf-8")
            (root / "skills/remote").mkdir(parents=True)
            (root / "skills/remote/SKILL.md").write_text("shared\nlocal\n", encoding="utf-8")
            (root / "skills/expected").mkdir(parents=True)
            (root / "skills/expected/SKILL.md").write_text("expected\n", encoding="utf-8")
            (root / "skills/fixtures").mkdir(parents=True)
            (root / "skills/fixtures/routing.jsonl").write_text(
                '{"intent":"route","expected_skill":"expected"}\n', encoding="utf-8"
            )
            (root / "skills/resource.txt").write_bytes(b"local resource\n")
            manifest = {
                "sources": {
                    "gstack": {
                        "adopted_commit": "a" * 40,
                        "current_commit": "b" * 40,
                    }
                },
                "records": [
                    {
                        "source_name": "local",
                        "local_path": "skills/local/SKILL.md",
                        "hashes": {},
                        "retention": {},
                    },
                    {
                        "source_name": "gstack",
                        "local_path": "skills/remote/SKILL.md",
                        "upstream_path": "remote/SKILL.md",
                        "hashes": {},
                        "retention": {},
                    },
                ],
                "resource_records": [
                    {
                        "source_name": "gstack",
                        "local_path": "skills/resource.txt",
                        "upstream_path": "resource.txt",
                        "hashes": {},
                    }
                ],
                "evaluations": [
                    {
                        "kind": "routing-jsonl",
                        "fixture_path": "skills/fixtures/routing.jsonl",
                    }
                ],
            }

            def fake_blob_text(repo, commit, path):
                return "shared\n" if commit == "a" * 40 else "shared\ncurrent\n"

            def fake_blob_bytes(repo, commit, path):
                return b"adopted resource\n" if commit == "a" * 40 else b"current resource\n"

            with (
                patch.object(reconciliation, "git_blob_text", side_effect=fake_blob_text),
                patch.object(reconciliation, "git_blob_bytes", side_effect=fake_blob_bytes),
            ):
                refreshed = reconciliation.refresh_reconciliation_manifest(
                    manifest, root, {"gstack": root / "upstream"}
                )

        local_record, remote_record = refreshed["records"]
        self.assertIsNone(local_record["hashes"]["adopted_source_sha256"])
        self.assertEqual(remote_record["retention"]["adopted_source_percent"], 100.0)
        self.assertEqual(remote_record["retention"]["current_upstream_percent"], 50.0)
        self.assertEqual(refreshed["evaluations"][0]["case_count"], 1)
        self.assertTrue(all(refreshed["evaluations"][0]["outcomes"].values()))
        self.assertEqual(
            refreshed["resource_records"][0]["hashes"]["local_sha256"],
            reconciliation.sha256_bytes(b"local resource\n"),
        )

    def test_complete_manifest_covers_every_owned_gstack_and_gbrain_skill(self) -> None:
        inventory = json.loads(
            (REPO_ROOT / "data" / "canonical-skill-inventory.json").read_text(
                encoding="utf-8"
            )
        )
        manifest = json.loads(
            (REPO_ROOT / "data" / "reconciliation-complete.json").read_text(
                encoding="utf-8"
            )
        )

        self.assertEqual(validate_reconciliation_manifest(manifest, REPO_ROOT, inventory), [])
        self.assertEqual(len(manifest["records"]), 108)
        self.assertEqual(len(manifest["alternate_source_records"]), 1)
        self.assertEqual(
            manifest["policy"]["minimum_current_upstream_retention_percent"],
            50.0,
        )
        all_records = [*manifest["records"], *manifest["alternate_source_records"]]
        self.assertEqual(
            Counter(record["decision"] for record in all_records),
            {"adopted": 68, "reviewed-deferred": 41},
        )
        self.assertEqual(
            Counter(record["source_name"] for record in manifest["records"]),
            {"gstack": 55, "gbrain": 53},
        )
        self.assertEqual(
            (
                manifest["alternate_source_records"][0]["canonical_id"],
                manifest["alternate_source_records"][0]["source_name"],
                manifest["alternate_source_records"][0]["decision"],
            ),
            ("skill:skillify", "gstack", "reviewed-deferred"),
        )

    def test_complete_manifest_builds_records_from_pinned_git_blobs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo_root = root / "local"
            empty_hooks = root / "empty-hooks"
            empty_hooks.mkdir()
            (repo_root / "data").mkdir(parents=True)
            (repo_root / "skills/adopted").mkdir(parents=True)
            (repo_root / "skills/deferred").mkdir(parents=True)
            (repo_root / "skills/adopted/SKILL.md").write_text(
                "shared\n", encoding="utf-8"
            )
            (repo_root / "skills/deferred/SKILL.md").write_text(
                "local adaptation\n", encoding="utf-8"
            )

            upstream_roots: dict[str, Path] = {}
            commits: dict[str, tuple[str, str]] = {}
            for source_name, source_path in (
                ("gstack", "adopted/SKILL.md"),
                ("gbrain", "skills/deferred/SKILL.md"),
            ):
                upstream = root / source_name
                init_test_repo(upstream)
                initial_text = (
                    "shared\n" if source_name == "gstack" else "old upstream\n"
                )
                adopted_commit = commit_test_file(
                    upstream, source_path, initial_text, "initial", empty_hooks
                )
                reviewed_commit = adopted_commit
                if source_name == "gbrain":
                    reviewed_commit = commit_test_file(
                        upstream,
                        source_path,
                        "current upstream\n",
                        "current",
                        empty_hooks,
                    )
                upstream_roots[source_name] = upstream
                commits[source_name] = (adopted_commit, reviewed_commit)

            for source_name in ("gstack", "gbrain"):
                adopted_commit, reviewed_commit = commits[source_name]
                map_data = {
                    "source": {
                        "name": source_name,
                        "repo": f"https://example.invalid/{source_name}.git",
                        "commit": adopted_commit,
                        "skill_parity_commit": adopted_commit,
                        "skill_reviewed_commit": reviewed_commit,
                    },
                    "skills": [],
                }
                map_filename = (
                    "skill-map.json"
                    if source_name == "gstack"
                    else "gbrain-skill-map.json"
                )
                (repo_root / "data" / map_filename).write_text(
                    json.dumps(map_data), encoding="utf-8"
                )

            inventory = {
                "entries": [
                    {
                        "canonical_id": "skill:adopted",
                        "source_name": "gstack",
                        "source_slug": "adopted",
                        "source_path": "adopted/SKILL.md",
                        "local_path": "skills/adopted/SKILL.md",
                        "adopted_commit": commits["gstack"][0],
                        "reviewed_commit": commits["gstack"][1],
                        "port_kind": "native",
                        "adaptation_notes": "Preserved portable behavior.",
                    },
                    {
                        "canonical_id": "skill:deferred",
                        "source_name": "gbrain",
                        "source_slug": "deferred",
                        "source_path": "skills/deferred/SKILL.md",
                        "local_path": "skills/deferred/SKILL.md",
                        "adopted_commit": commits["gbrain"][0],
                        "reviewed_commit": commits["gbrain"][1],
                        "port_kind": "adapted",
                        "adaptation_notes": "Retains the portable Codex workflow.",
                    },
                ]
            }

            with (
                patch.object(
                    reconciliation, "build_canonical_inventory", return_value=inventory
                ),
                patch.object(
                    reconciliation,
                    "git_blob_text_batch",
                    wraps=reconciliation.git_blob_text_batch,
                ) as blob_batch,
            ):
                manifest = reconciliation.build_complete_reconciliation_manifest(
                    repo_root, upstream_roots, "2026-08-09"
                )

        adopted, deferred = manifest["records"]
        self.assertEqual(adopted["decision"], "adopted")
        self.assertEqual(adopted["classifications"], ["preserved"])
        self.assertEqual(
            adopted["hashes"]["local_sha256"],
            adopted["hashes"]["current_upstream_sha256"],
        )
        self.assertEqual(deferred["decision"], "reviewed-deferred")
        self.assertEqual(deferred["retention"]["current_upstream_percent"], 0.0)
        self.assertEqual(deferred["adaptation_approval"]["status"], "approved")
        self.assertEqual(blob_batch.call_count, 2)

    def test_complete_manifest_fails_closed_on_false_adoption_and_unapproved_low_retention(self) -> None:
        inventory = json.loads(
            (REPO_ROOT / "data" / "canonical-skill-inventory.json").read_text(
                encoding="utf-8"
            )
        )
        manifest = json.loads(
            (REPO_ROOT / "data" / "reconciliation-complete.json").read_text(
                encoding="utf-8"
            )
        )
        invalid = copy.deepcopy(manifest)
        record = invalid["records"][0]
        record["adopted_commit"] = "1" * 40
        record["classifications"] = ["host-adapted"]
        record.pop("adaptation_approval", None)

        errors = validate_reconciliation_manifest(invalid, REPO_ROOT, inventory)

        self.assertTrue(any("does not pin the reviewed commit" in error for error in errors))
        self.assertTrue(any("lacks an approved adaptation record" in error for error in errors))

    def test_complete_manifest_uses_configured_retention_threshold(self) -> None:
        inventory = json.loads(
            (REPO_ROOT / "data" / "canonical-skill-inventory.json").read_text(
                encoding="utf-8"
            )
        )
        manifest = json.loads(
            (REPO_ROOT / "data" / "reconciliation-complete.json").read_text(
                encoding="utf-8"
            )
        )
        configured = copy.deepcopy(manifest)
        configured["policy"]["minimum_current_upstream_retention_percent"] = 0
        configured["records"][0].pop("adaptation_approval", None)

        errors = validate_reconciliation_manifest(configured, REPO_ROOT, inventory)

        self.assertFalse(any("approved adaptation record" in error for error in errors))

    def test_complete_manifest_rejects_invalid_retention_policy(self) -> None:
        inventory = json.loads(
            (REPO_ROOT / "data" / "canonical-skill-inventory.json").read_text(
                encoding="utf-8"
            )
        )
        manifest = json.loads(
            (REPO_ROOT / "data" / "reconciliation-complete.json").read_text(
                encoding="utf-8"
            )
        )
        invalid = copy.deepcopy(manifest)
        invalid["policy"]["minimum_current_upstream_retention_percent"] = "50"

        errors = validate_reconciliation_manifest(invalid, REPO_ROOT, inventory)

        self.assertTrue(any("retention threshold" in error for error in errors))

    def test_complete_manifest_requires_retention_policy(self) -> None:
        inventory = json.loads(
            (REPO_ROOT / "data" / "canonical-skill-inventory.json").read_text(
                encoding="utf-8"
            )
        )
        manifest = json.loads(
            (REPO_ROOT / "data" / "reconciliation-complete.json").read_text(
                encoding="utf-8"
            )
        )
        invalid = copy.deepcopy(manifest)
        invalid.pop("policy")

        errors = validate_reconciliation_manifest(invalid, REPO_ROOT, inventory)

        self.assertTrue(any("needs a retention policy" in error for error in errors))

    def test_complete_manifest_rejects_malformed_adaptation_approval(self) -> None:
        inventory = json.loads(
            (REPO_ROOT / "data" / "canonical-skill-inventory.json").read_text(
                encoding="utf-8"
            )
        )
        manifest = json.loads(
            (REPO_ROOT / "data" / "reconciliation-complete.json").read_text(
                encoding="utf-8"
            )
        )
        invalid = copy.deepcopy(manifest)
        record = invalid["records"][0]
        self.assertLess(
            record["retention"]["current_upstream_percent"],
            invalid["policy"]["minimum_current_upstream_retention_percent"],
        )
        record["adaptation_approval"] = {"status": "pending", "reason": ""}

        errors = validate_reconciliation_manifest(invalid, REPO_ROOT, inventory)

        self.assertTrue(any("lacks an approved adaptation record" in error for error in errors))

    def test_complete_manifest_rejects_non_object_removal_without_crashing(self) -> None:
        inventory = json.loads(
            (REPO_ROOT / "data" / "canonical-skill-inventory.json").read_text(
                encoding="utf-8"
            )
        )
        manifest = json.loads(
            (REPO_ROOT / "data" / "reconciliation-complete.json").read_text(
                encoding="utf-8"
            )
        )
        invalid = copy.deepcopy(manifest)
        invalid["records"][0]["intentional_removals"] = [None]

        errors = validate_reconciliation_manifest(invalid, REPO_ROOT, inventory)

        self.assertTrue(any("unexplained removal" in error for error in errors))

    def test_complete_manifest_rejects_repository_path_escape(self) -> None:
        inventory = json.loads(
            (REPO_ROOT / "data" / "canonical-skill-inventory.json").read_text(
                encoding="utf-8"
            )
        )
        manifest = json.loads(
            (REPO_ROOT / "data" / "reconciliation-complete.json").read_text(
                encoding="utf-8"
            )
        )
        invalid = copy.deepcopy(manifest)
        invalid["records"][0]["local_path"] = "../private-material"

        errors = validate_reconciliation_manifest(invalid, REPO_ROOT, inventory)

        self.assertTrue(any("canonical local_path" in error for error in errors))

    def test_complete_manifest_requires_duplicate_source_lineage(self) -> None:
        inventory = json.loads(
            (REPO_ROOT / "data" / "canonical-skill-inventory.json").read_text(
                encoding="utf-8"
            )
        )
        manifest = json.loads(
            (REPO_ROOT / "data" / "reconciliation-complete.json").read_text(
                encoding="utf-8"
            )
        )
        invalid = copy.deepcopy(manifest)
        invalid["alternate_source_records"] = []

        errors = validate_reconciliation_manifest(invalid, REPO_ROOT, inventory)

        self.assertTrue(any("missing alternate sources" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
