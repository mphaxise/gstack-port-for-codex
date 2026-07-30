from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = (
    REPO_ROOT
    / "skills"
    / "prescriptive-opencode-delegation"
    / "scripts"
)
sys.path.insert(0, str(SCRIPT_DIR))

from validate_commission import validate  # noqa: E402


def valid_commission() -> str:
    lines = [
        "# Commission: deterministic demo",
        "",
        "## Objective",
        "Create one deterministic output.",
        "",
        "## Model and effort",
        "- Model: `provider/model`",
        "- Reasoning: `medium`",
        "",
        "## Ownership and boundaries",
        "Read only:",
        "- `input.md`",
        "Create or edit only:",
        "- `output.md`",
        "Do not use Git, install packages, start servers, or deploy.",
        "",
        "## Allowed inputs",
        "Use the supplied fixture.",
        "",
        "## Required output",
        "Write `output.md`.",
        "",
        "## Implementation contract",
        "1. Preserve the schema.",
        "2. Keep the output deterministic.",
        "",
        "## Acceptance checks",
        "Run only the supplied validator.",
        "",
        "## Failure handoff",
        "Report the failing command and safest next action.",
        "Do not widen scope.",
        "",
        "## Stop condition",
        "Stop after the validator passes.",
    ]
    lines.extend(f"Contract detail {index}." for index in range(1, 8))
    return "\n".join(lines) + "\n"


class CommissionValidatorTests(unittest.TestCase):
    def test_accepts_complete_commission(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "commission.md"
            path.write_text(valid_commission(), encoding="utf-8")

            self.assertEqual(validate(path), [])

    def test_rejects_placeholder_and_missing_boundary(self) -> None:
        text = valid_commission().replace("Do not widen scope.\n", "")
        text += "[exact output path]\n"

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "commission.md"
            path.write_text(text, encoding="utf-8")
            errors = validate(path)

        self.assertIn("missing boundary phrase: Do not widen scope", errors)
        self.assertIn("unresolved placeholder: [exact output path]", errors)


if __name__ == "__main__":
    unittest.main()
