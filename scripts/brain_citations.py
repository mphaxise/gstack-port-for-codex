#!/usr/bin/env python3

from collections import Counter
from pathlib import Path
import argparse
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from gstack_port_for_codex.brain import (  # noqa: E402
    CITATION_RE,
    DEFAULT_BRAIN_ROOT,
    audit_citations,
    iter_brain_pages,
    rewrite_citation_markup,
)


def count_citations() -> int:
    total = 0
    for page in iter_brain_pages(REPO_ROOT / DEFAULT_BRAIN_ROOT):
        total += len(CITATION_RE.findall(page.body))
    return total


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit and normalize citation formatting in the local Codex brain.")
    parser.add_argument("--fix", action="store_true", help="Normalize malformed citation markup before reporting")
    parser.add_argument("--verbose", action="store_true", help="Print each remaining citation issue")
    args = parser.parse_args()

    brain_root = REPO_ROOT / DEFAULT_BRAIN_ROOT
    issues_before = audit_citations(brain_root)
    fixes = 0
    if args.fix:
        for page in iter_brain_pages(brain_root):
            fixes += rewrite_citation_markup(page.path)

    issues_after = audit_citations(brain_root)
    kinds = Counter(issue.issue for issue in issues_after)

    print("Citation Audit Report")
    print("=====================")
    print(f"Pages scanned: {len(iter_brain_pages(brain_root))}")
    print(f"Citations found: {count_citations()}")
    print(f"Issues fixed: {max(0, len(issues_before) - len(issues_after)) + fixes}")
    print(f"Remaining gaps: {len(issues_after)}")

    if args.verbose and issues_after:
        print("")
        for issue in issues_after:
            print(f"- {issue.path}:{issue.line_number} [{issue.issue}] {issue.line}")

    return 0 if not kinds else 1


if __name__ == "__main__":
    raise SystemExit(main())
