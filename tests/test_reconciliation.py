from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from gstack_port_for_codex.reconciliation import (  # noqa: E402
    build_canonical_inventory,
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


if __name__ == "__main__":
    unittest.main()
