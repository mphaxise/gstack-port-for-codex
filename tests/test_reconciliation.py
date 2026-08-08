from __future__ import annotations

import copy
from collections import Counter
import json
from pathlib import Path
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from gstack_port_for_codex.reconciliation import (  # noqa: E402
    build_canonical_inventory,
    evaluate_routing_jsonl,
    normalized_line_retention,
    validate_canonical_inventory,
    validate_reconciliation_manifest,
)


class ReconciliationTests(unittest.TestCase):
    def test_line_retention_uses_nonblank_multiset_overlap(self) -> None:
        source = "one\ntwo\ntwo\n\nthree\n"
        target = "two\ntwo\nfour\n"
        self.assertEqual(normalized_line_retention(source, target), 50.0)

    def test_canonical_inventory_covers_every_packaged_skill(self) -> None:
        inventory = build_canonical_inventory(REPO_ROOT)
        packaged = list((REPO_ROOT / "skills").glob("*/SKILL.md"))
        self.assertEqual(len(inventory["entries"]), len(packaged))
        self.assertEqual(validate_canonical_inventory(inventory, REPO_ROOT), [])

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

    def test_complete_manifest_fails_closed_on_false_adoption_and_low_retention(self) -> None:
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
        record["intentional_removals"] = []

        errors = validate_reconciliation_manifest(invalid, REPO_ROOT, inventory)

        self.assertTrue(any("does not pin the reviewed commit" in error for error in errors))
        self.assertTrue(any("lacks removal evidence" in error for error in errors))

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
