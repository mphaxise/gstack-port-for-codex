from __future__ import annotations

from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
DESIGN_QUALITY_ROOT = REPO_ROOT / "skills" / "design-quality"


class DesignQualityTests(unittest.TestCase):
    def test_bridge_has_required_references(self) -> None:
        required = (
            DESIGN_QUALITY_ROOT / "SKILL.md",
            DESIGN_QUALITY_ROOT / "references" / "project-context.md",
            DESIGN_QUALITY_ROOT / "references" / "quality-gates.md",
            DESIGN_QUALITY_ROOT / "references" / "impeccable-runtime.md",
            DESIGN_QUALITY_ROOT / "references" / "critique-contract.md",
        )

        self.assertTrue(all(path.exists() for path in required))

    def test_runtime_reference_uses_no_install_and_forbids_implicit_install(self) -> None:
        runtime_reference = (
            DESIGN_QUALITY_ROOT / "references" / "impeccable-runtime.md"
        ).read_text(encoding="utf-8")
        skill_text = (DESIGN_QUALITY_ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("npx --no-install impeccable", runtime_reference)
        self.assertIn("Never install or update Impeccable implicitly", skill_text)
        self.assertNotIn("npx impeccable install", runtime_reference)

    def test_critique_contract_preserves_codex_subagent_permission_boundary(self) -> None:
        critique_contract = (
            DESIGN_QUALITY_ROOT / "references" / "critique-contract.md"
        ).read_text(encoding="utf-8")

        self.assertIn("only when the user has authorized delegation", critique_contract)
        self.assertIn("run the two passes sequentially", critique_contract)


if __name__ == "__main__":
    unittest.main()
