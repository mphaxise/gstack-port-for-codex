from __future__ import annotations

from pathlib import Path
import sys
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from gstack_port_for_codex.registry import (  # noqa: E402
    format_capability_status_table,
    extract_frontmatter_keys,
    format_status_table,
    load_skill_map,
    skill_source_commit,
    validate_repo,
    validate_capability_map,
    validate_skill_map,
)


class RegistryTests(unittest.TestCase):
    def test_extract_frontmatter_keys_reads_name_and_description(self) -> None:
        text = (
            "---\n"
            "name: demo-skill\n"
            "description: A short description.\n"
            "---\n"
            "\n"
            "# Demo\n"
        )

        self.assertEqual(
            extract_frontmatter_keys(text),
            {"name": "demo-skill", "description": "A short description."},
        )

    def test_validate_skill_map_rejects_duplicate_codex_slug(self) -> None:
        data = {
            "source": {
                "name": "gstack",
                "repo": "https://example.com",
                "license": "MIT",
                "commit": "abc123",
            },
            "skills": [
                {
                    "upstream_slug": "one",
                    "codex_slug": "shared",
                    "status": "planned",
                    "port_kind": "native",
                    "summary": "first",
                    "notes": "first notes",
                    "source_files": ["one/SKILL.md"],
                },
                {
                    "upstream_slug": "two",
                    "codex_slug": "shared",
                    "status": "planned",
                    "port_kind": "native",
                    "summary": "second",
                    "notes": "second notes",
                    "source_files": ["two/SKILL.md"],
                },
            ],
        }

        errors = validate_skill_map(data)
        self.assertTrue(any("Duplicate codex slug: shared." == error for error in errors))

    def test_skill_source_commit_uses_parity_boundary_then_explicit_override(self) -> None:
        skill_map = {
            "source": {"commit": "baseline", "skill_parity_commit": "parity123"},
        }

        self.assertEqual(skill_source_commit(skill_map, {}), "parity123")
        self.assertEqual(
            skill_source_commit(skill_map, {"source_commit": "override456"}),
            "override456",
        )

    def test_validate_repo_passes_for_current_checkout(self) -> None:
        self.assertEqual(validate_repo(REPO_ROOT), [])

    def test_impeccable_capability_map_is_valid_and_complete(self) -> None:
        capability_map = load_skill_map(REPO_ROOT / "data" / "impeccable-capability-map.json")

        self.assertEqual(validate_capability_map(capability_map), [])
        self.assertEqual(capability_map["source"]["name"], "impeccable")
        self.assertEqual(len(capability_map["capabilities"]), 27)
        capability_ids = {capability["id"] for capability in capability_map["capabilities"]}
        for capability_id in (
            "core-guidance",
            "craft",
            "init",
            "critique",
            "audit",
            "live",
            "detector-and-hooks",
            "behavior-tests",
        ):
            self.assertIn(capability_id, capability_ids)

    def test_capability_status_table_reports_integration_mode(self) -> None:
        capability_map = load_skill_map(REPO_ROOT / "data" / "impeccable-capability-map.json")
        table = format_capability_status_table(capability_map)

        self.assertIn("core-guidance", table)
        self.assertIn("codex-adapted", table)
        self.assertIn("external-runtime", table)

    def test_status_table_mentions_reference_port(self) -> None:
        skill_map = load_skill_map(REPO_ROOT / "data" / "skill-map.json")
        table = format_status_table(skill_map)

        self.assertIn("plan-ceo-review", table)
        self.assertIn("ported", table)
        self.assertIn("runtime-aware", table)
        self.assertIn("Source", table)

    def test_current_gstack_ports_count(self) -> None:
        skill_map = load_skill_map(REPO_ROOT / "data" / "skill-map.json")
        ported = [skill["codex_slug"] for skill in skill_map["skills"] if skill["status"] == "ported"]

        self.assertEqual(len(ported), 56)
        for slug in (
            "gstack",
            "office-hours",
            "autoplan",
            "diagram",
            "spec",
            "setup-gbrain",
            "sync-gbrain",
            "context-save",
            "context-restore",
            "document-generate",
            "benchmark-models",
            "ios-qa",
            "landing-report",
            "make-pdf",
            "scrape",
            "skillify",
            "plan-design-review",
            "devex-review",
            "document-release",
            "cso",
            "open-gstack-browser",
            "connect-chrome",
            "plan-tune",
        ):
            self.assertIn(slug, ported)

    def test_current_gbrain_surface_is_ported(self) -> None:
        skill_map = load_skill_map(REPO_ROOT / "data" / "gbrain-skill-map.json")
        ported = [skill for skill in skill_map["skills"] if skill["status"] == "ported"]

        self.assertEqual(len(skill_map["skills"]), 53)
        self.assertEqual(len(ported), 53)
        for slug in (
            "capture",
            "gbrain-advisor",
            "gbrain-upgrade",
            "idea-lineage",
            "schema-unify",
            "skill-optimizer",
            "brain-taxonomist",
            "schema-author",
            "frontmatter-guard",
            "article-enrichment",
            "concept-synthesis",
            "perplexity-research",
            "minion-orchestrator",
            "skillpack-check",
            "voice-note-ingest",
        ):
            self.assertIn(slug, [skill["codex_slug"] for skill in ported])

    def test_praneet_extension_layer_is_registered(self) -> None:
        skill_map = load_skill_map(REPO_ROOT / "data" / "praneet-skill-map.json")
        ported = [skill for skill in skill_map["skills"] if skill["status"] == "ported"]

        self.assertEqual(len(ported), 7)
        self.assertEqual(
            sorted(skill["codex_slug"] for skill in ported),
            [
                "accessibility-review",
                "design-leadership-review",
                "market-map",
                "outcome-memory",
                "research-synthesis",
                "responsible-design-review",
                "startup-memo",
            ],
        )
        self.assertTrue(all(skill["port_kind"] == "hand-port-enhanced" for skill in ported))


if __name__ == "__main__":
    unittest.main()
