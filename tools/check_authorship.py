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


def identities():
    """(sha, subject, author, committer) for every commit reachable from HEAD."""
    out = subprocess.run(
        ["git", "log", "--format=%H%x1f%s%x1f%an <%ae>%x1f%cn <%ce>", "HEAD"],
        capture_output=True, text=True, check=True).stdout
    for line in out.splitlines():
        if line:
            yield line.split("\x1f")


def main():
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
