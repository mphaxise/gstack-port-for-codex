from __future__ import annotations

from pathlib import Path
import sys
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from gstack_port_for_codex.upstream_drift import (  # noqa: E402
    build_drift_report,
    classify_changed_paths,
    format_drift_report,
    parse_github_repo,
)


class UpstreamDriftTests(unittest.TestCase):
    def setUp(self) -> None:
        self.skill_map = {
            "source": {
                "repo": "https://github.com/garrytan/gstack",
                "commit": "abc123",
            },
            "skills": [
                {"upstream_slug": "review"},
                {"upstream_slug": "browse"},
            ],
        }

    def test_parse_github_repo_strips_git_suffix(self) -> None:
        owner, repo = parse_github_repo("https://github.com/garrytan/gstack.git")
        self.assertEqual((owner, repo), ("garrytan", "gstack"))

    def test_classify_changed_paths_groups_skill_and_shared_paths(self) -> None:
        classified = classify_changed_paths(
            [
                "review/SKILL.md",
                "browse/src/cli.ts",
                "README.md",
                "scripts/skill-check.ts",
                "misc/unknown.txt",
            ],
            self.skill_map,
        )

        self.assertEqual(classified["skills"]["review"], ["review/SKILL.md"])
        self.assertEqual(classified["skills"]["browse"], ["browse/src/cli.ts"])
        self.assertEqual(classified["shared"], ["README.md", "scripts/skill-check.ts"])
        self.assertEqual(classified["unmatched"], ["misc/unknown.txt"])

    def test_format_drift_report_handles_no_drift(self) -> None:
        report = build_drift_report(
            self.skill_map,
            {"full_name": "garrytan/gstack", "default_branch": "main"},
            {"sha": "abc123", "html_url": "https://example.com/commit/abc123"},
            {
                "html_url": "https://example.com/compare",
                "status": "identical",
                "ahead_by": 0,
                "behind_by": 0,
                "total_commits": 0,
                "files": [],
            },
        )

        text = format_drift_report(report)
        self.assertIn("No upstream drift detected.", text)

    def test_format_drift_report_lists_impacted_skills(self) -> None:
        report = build_drift_report(
            self.skill_map,
            {"full_name": "garrytan/gstack", "default_branch": "main"},
            {"sha": "def456", "html_url": "https://example.com/commit/def456"},
            {
                "html_url": "https://example.com/compare",
                "status": "ahead",
                "ahead_by": 2,
                "behind_by": 0,
                "total_commits": 2,
                "files": [
                    {"filename": "review/SKILL.md"},
                    {"filename": "browse/src/cli.ts"},
                    {"filename": "README.md"},
                ],
            },
        )

        text = format_drift_report(report)
        self.assertIn("Commits since pin: 2", text)
        self.assertIn("- review (1 files)", text)
        self.assertIn("- browse (1 files)", text)
        self.assertIn("Shared upstream paths:", text)


if __name__ == "__main__":
    unittest.main()
