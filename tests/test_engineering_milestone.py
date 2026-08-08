from __future__ import annotations

import importlib.util
from pathlib import Path
import subprocess
import sys
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "check_engineering_milestone.py"
SPEC = importlib.util.spec_from_file_location("check_engineering_milestone", SCRIPT_PATH)
assert SPEC and SPEC.loader
milestone = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = milestone
SPEC.loader.exec_module(milestone)


class EngineeringMilestoneTests(unittest.TestCase):
    def test_default_gate_has_local_checks_and_explicit_skillpack_skip(self) -> None:
        checks = milestone.build_checks(
            False,
            python_executable="python3",
            which=lambda _: None,
        )

        names = [check.name for check in checks]
        self.assertIn("canonical inventory", names)
        self.assertIn("repository registry", names)
        self.assertIn("unit tests", names)
        self.assertIn("public boundary", names)
        self.assertIn("GBrain skillpack", names)
        self.assertFalse(any("upstream drift" in name for name in names))
        skillpack = next(check for check in checks if check.name == "GBrain skillpack")
        self.assertIsNone(skillpack.command)
        self.assertFalse(skillpack.required)
        self.assertIn("unavailable", skillpack.skip_reason)

    def test_upstream_gate_covers_every_tracked_source(self) -> None:
        checks = milestone.build_checks(
            True,
            python_executable="python3",
            which=lambda _: "/usr/local/bin/gbrain",
        )

        upstream_commands = [
            check.command
            for check in checks
            if check.name.endswith("upstream drift")
        ]
        self.assertEqual(len(upstream_commands), len(milestone.UPSTREAM_MAPS))
        self.assertEqual(
            {command[-1] for command in upstream_commands if command},
            set(milestone.UPSTREAM_MAPS),
        )
        skillpack = next(check for check in checks if check.name == "GBrain skillpack")
        self.assertEqual(skillpack.command, ("/usr/local/bin/gbrain", "skillpack-check"))
        self.assertTrue(skillpack.required)

    def test_run_check_preserves_failure_evidence(self) -> None:
        check = milestone.Check("example", ("tool", "arg"))

        def fake_runner(*args, **kwargs):
            return subprocess.CompletedProcess(args[0], 7, stdout="partial\n", stderr="broken\n")

        outcome = milestone.run_check(check, cwd=REPO_ROOT, runner=fake_runner)

        self.assertEqual(outcome.status, "failed")
        self.assertEqual(outcome.returncode, 7)
        self.assertEqual(outcome.stdout, "partial\n")
        self.assertEqual(outcome.stderr, "broken\n")
        self.assertEqual(milestone.failed_required([outcome]), [outcome])

    def test_skipped_optional_check_does_not_fail_gate(self) -> None:
        outcome = milestone.run_check(
            milestone.Check("optional", None, required=False, skip_reason="not installed")
        )

        self.assertEqual(outcome.status, "skipped")
        self.assertEqual(milestone.failed_required([outcome]), [])


if __name__ == "__main__":
    unittest.main()
