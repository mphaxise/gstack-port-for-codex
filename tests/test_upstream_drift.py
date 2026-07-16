from __future__ import annotations

from pathlib import Path
from unittest.mock import patch
import sys
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from gstack_port_for_codex.upstream_drift import (  # noqa: E402
    build_drift_report,
    classify_changed_paths,
    classify_skill_changes_by_source,
    format_drift_report,
    github_token_from_env,
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
                {"upstream_slug": "query"},
            ],
        }

    def test_parse_github_repo_strips_git_suffix(self) -> None:
        owner, repo = parse_github_repo("https://github.com/garrytan/gstack.git")
        self.assertEqual((owner, repo), ("garrytan", "gstack"))

    @patch.dict("os.environ", {"GITHUB_TOKEN": "env-token"}, clear=True)
    def test_github_token_prefers_environment(self) -> None:
        self.assertEqual(github_token_from_env(), "env-token")

    @patch.dict("os.environ", {}, clear=True)
    @patch("gstack_port_for_codex.upstream_drift.shutil.which", return_value="/usr/bin/gh")
    @patch("gstack_port_for_codex.upstream_drift.subprocess.run")
    def test_github_token_falls_back_to_authenticated_gh(self, run, _which) -> None:
        run.return_value.returncode = 0
        run.return_value.stdout = "gh-token\n"

        self.assertEqual(github_token_from_env(), "gh-token")
        run.assert_called_once_with(
            ["gh", "auth", "token"],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_classify_changed_paths_groups_skill_and_shared_paths(self) -> None:
        classified = classify_changed_paths(
            [
                "review/SKILL.md",
                "browse/src/cli.ts",
                "skills/query/SKILL.md",
                "README.md",
                "scripts/skill-check.ts",
                "misc/unknown.txt",
            ],
            self.skill_map,
        )

        self.assertEqual(classified["skills"]["review"], ["review/SKILL.md"])
        self.assertEqual(classified["skills"]["browse"], ["browse/src/cli.ts"])
        self.assertEqual(classified["skills"]["query"], ["skills/query/SKILL.md"])
        self.assertEqual(classified["shared"], ["README.md", "scripts/skill-check.ts"])
        self.assertEqual(classified["unmatched"], ["misc/unknown.txt"])

    def test_classify_changed_paths_supports_explicit_capability_paths(self) -> None:
        capability_map = {
            "source": {"repo": "https://github.com/pbakaus/impeccable", "commit": "abc123"},
            "capabilities": [
                {
                    "id": "critique",
                    "upstream_paths": ["skill/reference/critique.md"],
                },
                {
                    "id": "live",
                    "upstream_paths": ["skill/reference/live.md", "skill/scripts/live*"],
                },
                {
                    "id": "detector",
                    "upstream_paths": ["cli/engine/"],
                },
            ],
        }

        classified = classify_changed_paths(
            [
                "skill/reference/critique.md",
                "skill/scripts/live-server.mjs",
                "cli/engine/registry/antipatterns.mjs",
                "site/pages/index.astro",
            ],
            capability_map,
        )

        self.assertEqual(classified["skills"]["critique"], ["skill/reference/critique.md"])
        self.assertEqual(classified["skills"]["live"], ["skill/scripts/live-server.mjs"])
        self.assertEqual(
            classified["skills"]["detector"],
            ["cli/engine/registry/antipatterns.mjs"],
        )
        self.assertEqual(classified["unmatched"], ["site/pages/index.astro"])

    def test_classify_skill_changes_uses_each_skill_source_commit(self) -> None:
        self.skill_map["skills"][1]["source_commit"] = "newer-browse"
        changes, sources = classify_skill_changes_by_source(
            self.skill_map,
            {
                "abc123": {"files": [{"filename": "browse/src/old.ts"}]},
                "newer-browse": {
                    "files": [
                        {"filename": "browse/src/current.ts"},
                        {"filename": "review/SKILL.md"},
                    ]
                },
            },
        )

        self.assertEqual(changes, {"browse": ["browse/src/current.ts"]})
        self.assertEqual(sources, {"browse": "newer-browse"})

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
