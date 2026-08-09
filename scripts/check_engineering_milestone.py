#!/usr/bin/env python3
"""Run the engineering milestone acceptance ladder from one entry point."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
from typing import Callable


REPO_ROOT = Path(__file__).resolve().parents[1]
UPSTREAM_MAPS = ("gstack", "gbrain", "praneet", "impeccable")


@dataclass(frozen=True)
class Check:
    name: str
    command: tuple[str, ...] | None
    required: bool = True
    skip_reason: str | None = None


@dataclass(frozen=True)
class Outcome:
    name: str
    status: str
    command: tuple[str, ...] | None
    required: bool
    returncode: int | None
    stdout: str
    stderr: str
    reason: str | None = None


def build_checks(
    include_upstream: bool,
    *,
    gstack_repo: Path | None = None,
    gbrain_repo: Path | None = None,
    python_executable: str = sys.executable,
    which: Callable[[str], str | None] = shutil.which,
) -> list[Check]:
    if (gstack_repo is None) != (gbrain_repo is None):
        raise ValueError("Provide both GStack and GBrain repositories for reconciliation verification.")

    checks = [
        Check(
            "canonical inventory",
            (python_executable, "scripts/build_skill_inventory.py", "--check"),
        ),
        Check("repository registry", (python_executable, "scripts/validate_repo.py")),
        Check(
            "unit tests",
            (python_executable, "-m", "unittest", "discover", "-s", "tests"),
        ),
        Check("installer smoke", (python_executable, "scripts/smoke_install.py")),
        Check("public boundary", (python_executable, "scripts/check_public_boundary.py")),
        Check("brain health", (python_executable, "scripts/brain_doctor.py")),
        Check(
            "Python compilation",
            (python_executable, "-m", "compileall", "-q", "scripts", "src", "tests"),
        ),
        Check("unstaged diff formatting", ("git", "diff", "--check")),
        Check("staged diff formatting", ("git", "diff", "--cached", "--check")),
    ]

    if gstack_repo is not None and gbrain_repo is not None:
        checks.append(
            Check(
                "complete reconciliation integrity",
                (
                    python_executable,
                    "scripts/build_complete_reconciliation.py",
                    "--gstack-repo",
                    str(gstack_repo),
                    "--gbrain-repo",
                    str(gbrain_repo),
                    "--check",
                ),
            )
        )

    gbrain_executable = which("gbrain")
    if gbrain_executable:
        checks.append(Check("GBrain skillpack", (gbrain_executable, "skillpack-check")))
    else:
        checks.append(
            Check(
                "GBrain skillpack",
                None,
                required=False,
                skip_reason="gbrain CLI unavailable; repository checks are the local fallback",
            )
        )

    if include_upstream:
        checks.extend(
            Check(
                f"{source} upstream drift",
                (python_executable, "scripts/check_upstream_drift.py", "--map", source),
            )
            for source in UPSTREAM_MAPS
        )

    return checks


def run_check(
    check: Check,
    *,
    cwd: Path = REPO_ROOT,
    runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
) -> Outcome:
    if check.command is None:
        return Outcome(
            name=check.name,
            status="skipped",
            command=None,
            required=check.required,
            returncode=None,
            stdout="",
            stderr="",
            reason=check.skip_reason,
        )

    try:
        completed = runner(
            check.command,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError as error:
        return Outcome(
            name=check.name,
            status="failed",
            command=check.command,
            required=check.required,
            returncode=None,
            stdout="",
            stderr="",
            reason=str(error),
        )

    return Outcome(
        name=check.name,
        status="passed" if completed.returncode == 0 else "failed",
        command=check.command,
        required=check.required,
        returncode=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
    )


def run_checks(checks: list[Check], *, cwd: Path = REPO_ROOT) -> list[Outcome]:
    return [run_check(check, cwd=cwd) for check in checks]


def failed_required(outcomes: list[Outcome]) -> list[Outcome]:
    return [outcome for outcome in outcomes if outcome.required and outcome.status != "passed"]


def print_human(outcomes: list[Outcome]) -> None:
    for outcome in outcomes:
        label = outcome.status.upper()
        command = f" ({shlex.join(outcome.command)})" if outcome.command else ""
        print(f"[{label}] {outcome.name}{command}")
        if outcome.reason:
            print(outcome.reason)
        if outcome.stdout.strip():
            print(outcome.stdout.rstrip())
        if outcome.stderr.strip():
            print(outcome.stderr.rstrip())

    passed = sum(outcome.status == "passed" for outcome in outcomes)
    skipped = sum(outcome.status == "skipped" for outcome in outcomes)
    failed = sum(outcome.status == "failed" for outcome in outcomes)
    print(f"Engineering milestone alpha: {passed} passed, {skipped} skipped, {failed} failed.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--upstream",
        action="store_true",
        help="Include network-backed drift checks for every tracked public upstream",
    )
    parser.add_argument("--json", action="store_true", help="Print structured results")
    parser.add_argument(
        "--gstack-repo",
        type=Path,
        help="Local GStack Git checkout used to verify pinned reconciliation blobs",
    )
    parser.add_argument(
        "--gbrain-repo",
        type=Path,
        help="Local GBrain Git checkout used to verify pinned reconciliation blobs",
    )
    args = parser.parse_args()

    if (args.gstack_repo is None) != (args.gbrain_repo is None):
        parser.error("--gstack-repo and --gbrain-repo must be provided together")

    outcomes = run_checks(
        build_checks(
            args.upstream,
            gstack_repo=args.gstack_repo,
            gbrain_repo=args.gbrain_repo,
        )
    )
    if args.json:
        print(json.dumps([asdict(outcome) for outcome in outcomes], indent=2))
    else:
        print_human(outcomes)
    return 1 if failed_required(outcomes) else 0


if __name__ == "__main__":
    raise SystemExit(main())
