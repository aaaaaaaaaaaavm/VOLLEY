"""Fail when the published companion payloads are older than the flagship they claim to reproduce.

WHY THIS EXISTS
---------------
P84, P100, P101 and P102 are the same defect: a value moved and something that restates it did
not. `check_crossrefs.py` catches that between two results FILES. This catches it between two
REPOSITORIES, which is where it had been happening unobserved.

`VOLLEY-paper` and `VOLLEY-thesis` are generated. Their README banner names the flagship commit
they came from -- that provenance was always there and was always correct. What was missing is
that the banner lives in the OTHER repository, so no gate here could read it. On 2026-08-22 the
flagship carried P100's follow-up, P101 and P102 while both companions still published the
pre-correction A38 under a banner naming a commit four behind. Every gate passed.

WHAT IT CHECKS
--------------
1. `tools/companion_export.json` records the commit `export_companion.py` last ran at.
2. If any commit since then has touched a manifest source path, the payloads are stale. That is
   the whole test, and git answers it offline.
3. If the companion working copies are on disk, their README banner commit must equal the
   recorded one. Absent copies are not a pass or a failure -- they are reported as unchecked.

It is deliberately offline. It asks git about this repository and reads files if they happen to
be there; it never reaches the network, because the rest of the gate set does not either.

    python3 tools/check_companions.py
"""
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RECORD = os.path.join(ROOT, "tools", "companion_export.json")
BANNER_RE = re.compile(r"at commit\s*\n?>?\s*`([0-9a-f]{6,40})`")
COMPANIONS = ("VOLLEY-paper", "VOLLEY-thesis")


def _git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True).stdout


def _git_ok(*args):
    """True when git exits zero. For questions answered by status rather than stdout."""
    return subprocess.run(["git", *args], cwd=ROOT,
                          capture_output=True, text=True).returncode == 0


def main():
    if not os.path.exists(RECORD):
        print("companions: NO EXPORT RECORD. Run tools/export_companion.py -- the payloads "
              "cannot be shown to match anything.")
        return 1
    with open(RECORD, encoding="utf-8") as fh:
        rec = json.load(fh)
    commit, sources = rec["flagship_commit"], rec["manifest_sources"]

    # Two questions, and the first one alone is not enough. `cat-file -t` says the object
    # exists in THIS clone, which stays true for a commit that has been amended or rebased
    # away: the object lingers here and was never fetched anywhere else. That is how an
    # unreachable export commit passed locally and failed on a fresh CI clone twice, once
    # as 59b3661 and once immediately after an amend. Reachability from HEAD is the
    # property that actually travels.
    if _git("cat-file", "-t", commit).strip() != "commit":
        print(f"companions: the recorded export commit {commit} is not in this repository's "
              f"history. Re-export.")
        return 1
    if not _git_ok("merge-base", "--is-ancestor", commit, "HEAD"):
        print(f"companions: the recorded export commit {commit} exists as an object but is "
              f"not an ancestor of HEAD, so it was amended or rebased away and no fresh "
              f"clone will have it. Re-export.")
        return 1

    problems = []
    if rec.get("flagship_tree_was_dirty"):
        problems.append("the export ran against a dirty working tree, so the banner commit does "
                        "not describe what was copied. Commit, then re-export")

    since = _git("log", "--oneline", f"{commit}..HEAD", "--", *sources).strip()
    if since:
        n = len(since.splitlines())
        problems.append(f"{n} commit(s) have touched a manifest source since {commit}, so the "
                        f"published payloads are stale:\n      "
                        + "\n      ".join(since.splitlines()[:10]))

    checked, absent = [], []
    for name in COMPANIONS:
        readme = os.path.join(os.path.dirname(ROOT), name, "README.md")
        if not os.path.exists(readme):
            absent.append(name)
            continue
        m = BANNER_RE.search(open(readme, encoding="utf-8").read(8192))
        if not m:
            problems.append(f"{name}: no flagship commit in its README banner")
        elif not (m.group(1).startswith(commit) or commit.startswith(m.group(1))):
            problems.append(f"{name}: banner says {m.group(1)}, export record says {commit}")
        else:
            checked.append(name)

    if problems:
        print(f"companions: {len(problems)} problem(s)\n")
        for p in problems:
            print(f"  {p}")
        print("\n  fix: python3 tools/export_companion.py --out .. && push both companions")
        return 1

    tail = f"{len(checked)} working copy/copies agree" if checked else "no working copies on disk"
    if absent:
        tail += f"; not checked: {', '.join(absent)}"
    print(f"companions: payloads current at flagship {commit}; "
          f"{len(sources)} manifest sources unchanged since; {tail}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
