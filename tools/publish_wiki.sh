#!/usr/bin/env bash
#
# Publish wiki/Home.md to the GitHub wiki.
#
# WHY THIS SCRIPT EXISTS
# ----------------------
# `wiki/Home.md` in this repository is the MAINTAINED SOURCE. The live wiki is a separate
# git repository -- VOLLEY.wiki.git -- that nothing here writes to, and there was no note
# anywhere saying so.
#
# The result was predictable and it happened: on 2026-08-14 the source had been corrected
# four times while the live page had not been touched since 2026-07-30. It still named the
# project "emocd", still quoted a 20.37 m/s headline from before the CAD sled
# reconciliation, still reported a x1.62 lifetime multiplier from before the depth-resolved
# thrust constant, and still made a phase-spacing claim withdrawn as P56.
#
# Every propagation tool in this repository walks tracked files. The wiki is tracked, so it
# was corrected; it is also PUBLISHED SOMEWHERE ELSE, and no check can see across that
# boundary. This is the same class as P58, where two authored manuscripts in two
# repositories forked, and P61, where a run sheet drifted from its own script.
#
# It cannot run in an environment whose git proxy has not been granted the .wiki
# repository -- GitHub does not expose wiki content through its API, so there is no
# fallback. Run it where you have ordinary push credentials.
#
# Usage:  tools/publish_wiki.sh [--dry-run]
set -euo pipefail

OWNER=aaaaaaaaaaaavm
REPO=VOLLEY
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/wiki/Home.md"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

[ -f "$SRC" ] || { echo "missing $SRC" >&2; exit 1; }

git clone --quiet "https://github.com/$OWNER/$REPO.wiki.git" "$WORK/wiki"
cp "$SRC" "$WORK/wiki/Home.md"

cd "$WORK/wiki"
if git diff --quiet; then
    echo "live wiki already matches wiki/Home.md; nothing to publish"
    exit 0
fi

echo "--- what would change on the live wiki ---"
git --no-pager diff --stat

if [ "${1:-}" = "--dry-run" ]; then
    echo "dry run; not committing"
    exit 0
fi

git add Home.md
git commit --quiet -m "Publish the maintained landing page from the repository

wiki/Home.md in the VOLLEY repository is the source. This is a copy of it at
$(cd "$ROOT" && git rev-parse --short HEAD)."
git push --quiet origin master
echo "published from $(cd "$ROOT" && git rev-parse --short HEAD)"
