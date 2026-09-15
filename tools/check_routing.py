"""Fail when the public workstream routing misquotes the register it routes.

WHY THIS EXISTS
---------------
On 2026-09-15 `docs/workstreams/ENGINEERING_CLOSURE.md` shipped with seven native register
titles corrupted. The owner column had been filled by substituting the private stream letters
for public names, and the substitution also replaced sentence-initial words inside the QUOTED
titles:

    An acceptance band ...        ->  Redesignn acceptance band ...
    At femtosat scale ...         ->  Redesignt femtosat scale ...
    ADR-032's first falsifier ... ->  RedesignDR-032's first falsifier ...

Nothing caught it. `check_public.py` compares counts, `check_links.py` compares link targets,
and `make_bsx_review.py` GENERATES its table from the register so it cannot drift. This routing
table is hand-maintained and quotes the register verbatim, which is precisely the arrangement
that needs a comparison.

WHAT IT CHECKS
--------------
For every row of the routing table: the ID exists in `OPEN_PROBLEMS.md`, the native title matches
that entry's heading EXACTLY, and each ID is routed once. It does not check the owner column --
that is a human assignment with no authority in the register, and inventing one here would be a
gate asserting something it cannot know.

    python3 tools/check_routing.py
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTER = os.path.join(ROOT, "OPEN_PROBLEMS.md")
ROUTES = [os.path.join(ROOT, "docs", "workstreams", "ENGINEERING_CLOSURE.md")]

ROW = re.compile(r"^\|\s*([PE]\d+)\s*\|([^|]*)\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$", re.M)
HEADING = re.compile(r"^###\s+([PE]\d+)\.\s+(.+?)\s*$", re.M)


def register_titles():
    with open(REGISTER, encoding="utf-8") as fh:
        return {m.group(1): m.group(2) for m in HEADING.finditer(fh.read())}


def main():
    titles = register_titles()
    problems = []
    routed_total = 0

    for path in ROUTES:
        rel = os.path.relpath(path, ROOT)
        if not os.path.exists(path):
            problems.append(f"{rel}: missing")
            continue
        with open(path, encoding="utf-8") as fh:
            rows = ROW.findall(fh.read())
        seen = {}
        for ident, _owner, title, _next_step in rows:
            seen[ident] = seen.get(ident, 0) + 1
            routed_total += 1
            if ident not in titles:
                problems.append(f"{rel}: {ident} is routed but is not in the register")
                continue
            if title != titles[ident]:
                problems.append(f"{rel}: {ident} title does not match the register")
                problems.append(f"    register: {titles[ident][:96]}")
                problems.append(f"    routing:  {title[:96]}")
        for ident, n in sorted(seen.items()):
            if n > 1:
                problems.append(f"{rel}: {ident} is routed {n} times")

    if problems:
        print(f"routing: {len(problems)} problem(s)\n")
        for p in problems:
            print("  " + p)
        print("\n  The register is the authority. Restore the quoted title from OPEN_PROBLEMS.md,")
        print("  and never fix a routing table with a substitution that can reach inside a quote.")
        return 1

    print(f"routing: {routed_total} routed entries, every quoted title matches the register")
    return 0


if __name__ == "__main__":
    sys.exit(main())
