from __future__ import annotations

from pathlib import Path
import sys
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from record_skill_review import record_review  # noqa: E402


class RecordSkillReviewTests(unittest.TestCase):
    def test_review_boundary_does_not_advance_deferred_skill_source(self) -> None:
        data = {
            "source": {"commit": "baseline", "skill_parity_commit": "adopted"},
            "skills": [
                {"upstream_slug": "accepted"},
                {"upstream_slug": "deferred", "source_commit": "older"},
            ],
        }

        refreshed = record_review(
            data, "reviewed", ["accepted"], reviewed_at="2026-08-08"
        )

        self.assertEqual(refreshed["source"]["skill_reviewed_commit"], "reviewed")
        self.assertEqual(refreshed["source"]["latest_checked_at"], "2026-08-08")
        self.assertEqual(refreshed["skills"][0]["source_commit"], "reviewed")
        self.assertEqual(refreshed["skills"][1]["source_commit"], "older")

    def test_unknown_adopted_slug_fails_closed(self) -> None:
        data = {"source": {}, "skills": [{"upstream_slug": "known"}]}

        with self.assertRaisesRegex(ValueError, "Unknown upstream skill"):
            record_review(data, "reviewed", ["missing"])


if __name__ == "__main__":
    unittest.main()
