"""Fail when any commit in this repository is authored by someone other than its author.

WHY THIS EXISTS
---------------
This repository states in `README.md`, in `CITATION.cff` and on every companion front page that
the work is Adityavardhan Mishra's. Nothing checked it. On 2026-08-31 a sibling repository was
found carrying a commit written under a different identity entirely -- not a co-author, not a
collaborator, but a machine account that the working container sets as its DEFAULT git identity.
This repository escaped only because its clone happened to carry a local `user.name` override,
which is luck rather than a control.

A single-author claim that nothing enforces is the same class of defect as a band that nothing
computes. `check_bands.py` exists because a verdict nobody evaluates is not a verdict; this
exists because a provenance claim nobody checks is not provenance.

WHY IT REFUSES A SHALLOW CLONE
------------------------------
On 2026-09-14 this gate reported "52 commits, every author and committer is the repository's
own" in a working container whose clone was shallow. The repository had 412. It passed, and it
passed for the wrong reason -- the claim it prints is about EVERY commit, and on a truncated
history it cannot make that claim about the ones it cannot see. A gate that quietly checks a
subset is worse than one that refuses, because it reads as a clean result.

CI fetches full history for `check_companions`, so it is unaffected. A local clone is fixed with
`git fetch --unshallow`.

WHAT IT CHECKS
--------------
Every commit reachable from HEAD must carry an author AND a committer drawn from ALLOWED. Both
are checked: an identity can be laundered through either field, and the committer is the one a
casual `git log` does not show.

The allowed set is deliberately tiny and spelled out here rather than read from `git config`,
because the configuration is exactly what failed. Adding an entry to it is a visible diff.

    python3 tools/check_authorship.py
"""
import subprocess
import sys

ALLOWED = {
    "Adityavardhan Mishra <adityavardhanmishr@gmail.com>",
    "Adityavardhan Mishra <87394853+aaaaaaaaaaaavm@users.noreply.github.com>",
}


def is_shallow():
    out = subprocess.run(["git", "rev-parse", "--is-shallow-repository"],
                         capture_output=True, text=True, check=True).stdout.strip()
    return out == "true"


def identities():
    """(sha, subject, author, committer) for every commit reachable from HEAD."""
    out = subprocess.run(
        ["git", "log", "--format=%H%x1f%s%x1f%an <%ae>%x1f%cn <%ce>", "HEAD"],
        capture_output=True, text=True, check=True).stdout
    for line in out.splitlines():
        if line:
            yield line.split("\x1f")


def main():
    if is_shallow():
        seen = sum(1 for _ in identities())
        print("authorship: REFUSED -- this clone is shallow")
        print(f"  {seen} commits are reachable here, and the rest of the history is not.")
        print("  This gate asserts something about EVERY commit, so on a truncated history it")
        print("  cannot make the claim at all. Passing would read as a clean result.")
        print("\n  Fix with:  git fetch --unshallow")
        return 1

    bad = []
    total = 0
    for sha, subject, author, committer in identities():
        total += 1
        if author not in ALLOWED:
            bad.append((sha, subject, "author", author))
        if committer not in ALLOWED:
            bad.append((sha, subject, "committer", committer))

    if bad:
        print(f"authorship: {len(bad)} identity problem(s) across {total} commits\n")
        for sha, subject, field, who in bad:
            print(f"  {sha[:9]}  {field:9s} {who}")
            print(f"             {subject[:78]}")
        print("\n  Every commit must carry one of:")
        for a in sorted(ALLOWED):
            print(f"    {a}")
        print("\n  If this fires on a fresh clone, check `git config user.email` before")
        print("  committing anything: the container default is not this repository's author.")
        return 1

    print(f"authorship: {total} commits, every author and committer is the repository's own")
    return 0


if __name__ == "__main__":
    sys.exit(main())
