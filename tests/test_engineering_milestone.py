from __future__ import annotations

from contextlib import redirect_stdout
import importlib.util
import io
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch


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

    def test_checkout_backed_gate_verifies_complete_reconciliation(self) -> None:
        checks = milestone.build_checks(
            False,
            gstack_repo=Path("/tmp/gstack"),
            gbrain_repo=Path("/tmp/gbrain"),
            python_executable="python3",
            which=lambda _: None,
        )

        reconciliation = next(
            check for check in checks if check.name == "complete reconciliation integrity"
        )
        self.assertEqual(
            reconciliation.command,
            (
                "python3",
                "scripts/build_complete_reconciliation.py",
                "--gstack-repo",
                "/tmp/gstack",
                "--gbrain-repo",
                "/tmp/gbrain",
                "--check",
            ),
        )

    def test_checkout_backed_gate_requires_both_repositories(self) -> None:
        with self.assertRaisesRegex(ValueError, "both GStack and GBrain"):
            milestone.build_checks(False, gstack_repo=Path("/tmp/gstack"))

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

    def test_run_check_preserves_os_error(self) -> None:
        check = milestone.Check("missing", ("missing-tool",))

        def failing_runner(*args, **kwargs):
            raise OSError("tool missing")

        outcome = milestone.run_check(check, cwd=REPO_ROOT, runner=failing_runner)

        self.assertEqual(outcome.status, "failed")
        self.assertIsNone(outcome.returncode)
        self.assertEqual(outcome.reason, "tool missing")

    def test_run_checks_preserves_order(self) -> None:
        checks = [
            milestone.Check("first", (sys.executable, "-c", "print('one')")),
            milestone.Check("second", None, required=False, skip_reason="optional"),
        ]

        outcomes = milestone.run_checks(checks, cwd=REPO_ROOT)

        self.assertEqual([outcome.name for outcome in outcomes], ["first", "second"])
        self.assertEqual(outcomes[0].status, "passed")
        self.assertEqual(outcomes[1].status, "skipped")

    def test_print_human_includes_evidence_and_summary(self) -> None:
        outcomes = [
            milestone.Outcome(
                "passed check", "passed", ("tool", "arg"), True, 0, "output\n", ""
            ),
            milestone.Outcome(
                "optional check", "skipped", None, False, None, "", "", "not installed"
            ),
            milestone.Outcome(
                "failed check", "failed", ("bad-tool",), True, 3, "", "broken\n"
            ),
        ]

        with redirect_stdout(io.StringIO()) as output:
            milestone.print_human(outcomes)

        rendered = output.getvalue()
        self.assertIn("[PASSED] passed check (tool arg)", rendered)
        self.assertIn("not installed", rendered)
        self.assertIn("broken", rendered)
        self.assertIn("1 passed, 1 skipped, 1 failed", rendered)

    def test_main_supports_json_and_failure_exit(self) -> None:
        outcomes = [
            milestone.Outcome(
                "failed check", "failed", ("bad-tool",), True, 3, "", "broken\n"
            )
        ]
        with (
            patch.object(sys, "argv", ["check_engineering_milestone.py", "--upstream", "--json"]),
            patch.object(milestone, "build_checks", return_value=[]) as build_checks,
            patch.object(milestone, "run_checks", return_value=outcomes),
            redirect_stdout(io.StringIO()) as output,
        ):
            self.assertEqual(milestone.main(), 1)

        build_checks.assert_called_once_with(
            True,
            gstack_repo=None,
            gbrain_repo=None,
        )
        rendered = output.getvalue()
        self.assertIn('"status": "failed"', rendered)
        self.assertIn('"bad-tool"', rendered)


if __name__ == "__main__":
    unittest.main()
