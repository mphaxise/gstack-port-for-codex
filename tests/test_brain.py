from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from gstack_port_for_codex.brain import (  # noqa: E402
    add_backlink,
    audit_citations,
    brain_stats,
    ensure_brain_root,
    make_page_path,
    parse_brain_page,
    render_page,
    rewrite_citation_markup,
    search_brain,
    slugify,
    upsert_page,
    validate_brain,
)


class BrainTests(unittest.TestCase):
    def test_slugify_normalizes_words(self) -> None:
        self.assertEqual(slugify("Jane Doe, PhD"), "jane-doe-phd")

    def test_search_brain_finds_matching_page(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            brain_root = Path(tmp) / "brain"
            ensure_brain_root(brain_root)
            page_path = make_page_path(brain_root, "people", "Jane Doe")
            page_path.write_text(
                render_page(
                    "Jane Doe",
                    "person",
                    "Jane Doe leads Example Labs and works on applied AI.",
                    ["- 2026-04-16: Mentioned in planning notes."],
                    tags=["ai"],
                ),
                encoding="utf-8",
            )

            hits = search_brain(brain_root, "Jane AI", limit=5)
            self.assertEqual(len(hits), 1)
            self.assertEqual(hits[0].title, "Jane Doe")

    def test_brain_stats_counts_pages(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            brain_root = Path(tmp) / "brain"
            ensure_brain_root(brain_root)
            page_path = make_page_path(brain_root, "concepts", "Founder Mode")
            page_path.write_text(
                render_page(
                    "Founder Mode",
                    "concept",
                    "Founder Mode is a management posture.",
                    ["- 2026-04-16: Added example."],
                ),
                encoding="utf-8",
            )

            stats = brain_stats(brain_root)
            self.assertEqual(stats["page_count"], 1)
            self.assertEqual(stats["categories"], {"concepts": 1})

    def test_validate_brain_flags_missing_type(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            brain_root = Path(tmp) / "brain"
            ensure_brain_root(brain_root)
            page_path = brain_root / "people" / "untitled.md"
            page_path.write_text("---\ntitle: Test\n---\n\nBody\n", encoding="utf-8")

            errors = validate_brain(brain_root)
            self.assertTrue(any("missing frontmatter type" in error for error in errors))

    def test_upsert_page_merges_compiled_truth_and_timeline(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            brain_root = Path(tmp) / "brain"
            ensure_brain_root(brain_root)
            upsert_page(
                brain_root,
                "people",
                "Jane Doe",
                "Jane Doe builds Example Labs. [Source: notes, 2026-04-16]",
                timeline_entries=["- 2026-04-16: Added profile. [Source: notes, 2026-04-16]"],
                tags=["founder"],
            )
            path = upsert_page(
                brain_root,
                "people",
                "Jane Doe",
                "She also writes about applied AI. [Source: memo, 2026-04-17]",
                timeline_entries=["- 2026-04-17: Added writing context. [Source: memo, 2026-04-17]"],
                tags=["ai"],
            )

            page = parse_brain_page(path)
            self.assertIn("Example Labs", page.compiled_truth)
            self.assertIn("applied AI", page.compiled_truth)
            self.assertIn("2026-04-16", page.timeline)
            self.assertIn("2026-04-17", page.timeline)
            self.assertIn("founder", page.frontmatter["tags"])
            self.assertIn("ai", page.frontmatter["tags"])

    def test_add_backlink_appends_reference_entry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            brain_root = Path(tmp) / "brain"
            ensure_brain_root(brain_root)
            target = upsert_page(
                brain_root,
                "people",
                "Jane Doe",
                "Jane Doe is a founder. [Source: notes, 2026-04-16]",
                timeline_entries=["- 2026-04-16: Created page. [Source: notes, 2026-04-16]"],
            )
            source = upsert_page(
                brain_root,
                "meetings",
                "Team Sync",
                "Discussed roadmap. [Source: meeting, 2026-04-16]",
                timeline_entries=["- 2026-04-16: Meeting held. [Source: meeting, 2026-04-16]"],
            )

            changed = add_backlink(target, source, "2026-04-16", "discussed during roadmap review")
            page = parse_brain_page(target)

            self.assertTrue(changed)
            self.assertIn("Referenced in [Team Sync]", page.timeline)
            self.assertIn("../meetings/team-sync.md", page.timeline)

    def test_audit_citations_distinguishes_missing_and_malformed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            brain_root = Path(tmp) / "brain"
            ensure_brain_root(brain_root)
            path = brain_root / "concepts" / "founder-mode.md"
            path.write_text(
                render_page(
                    "Founder Mode",
                    "concept",
                    "\n".join(
                        (
                            "Founder Mode is a useful operating stance. [source: memo, 2026-04-16]",
                            "It gets stronger when paired with clear ownership.",
                        )
                    ),
                    ["- 2026-04-16: Added concept page. [Source: memo, 2026-04-16]"],
                ),
                encoding="utf-8",
            )

            issues_before = audit_citations(brain_root)
            self.assertEqual(sorted(issue.issue for issue in issues_before), ["malformed-citation", "missing-citation"])

            rewrite_citation_markup(path)
            issues_after = audit_citations(brain_root)
            self.assertEqual([issue.issue for issue in issues_after], ["missing-citation"])


if __name__ == "__main__":
    unittest.main()
