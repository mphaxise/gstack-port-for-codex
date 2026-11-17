#!/bin/sh
set -eu

# Design Ledger supplies a fresh git archive. The milestone checks use the
# index for package membership, ignore rules, and staged diff checks.
test -n "${DESIGN_LEDGER_COMMIT:-}"
test ! -e .git
git init -q --template=
git add -f -- .
git -c user.name=Verifier -c user.email=verify@localhost -c commit.gpgSign=false \
    commit --quiet -m "Isolated verification snapshot"
exec python3 scripts/check_engineering_milestone.py
