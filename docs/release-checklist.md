# Release Checklist

Use this checklist before creating a tag or GitHub release.

1. Confirm the target commit contains no private operating material,
   credentials, generated brain content, or machine-specific paths.
2. Run `python3 scripts/check_engineering_milestone.py`.
3. Review the changelog, license notices, README installation path, and
   upstream freshness record.
4. Run `python3 scripts/check_engineering_milestone.py --upstream` when network
   access is available. Record a network limitation explicitly when it is
   unavailable.
5. Review the final diff from a clean checkout and confirm the intended tag or
   release notes.
6. Create the tag and GitHub release only after the owner authorizes external
   publication.
