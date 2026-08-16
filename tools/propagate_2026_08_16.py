"""One-shot propagation of the 2026-08-16 enclosure buildup (A46, P10 closed).

WHY A SCRIPT AND NOT AN EDITOR
------------------------------
Same reason as tools/propagate_baseline.py, and the same construction. A46 replaced P10's
8.0 kg placeholder with five derived line items totalling 50.04 kg, and the dry mass and
every kg-per-satellite figure move with it.

    dry mass                84.5 -> 126.6 kg
    loaded                 132.5 -> 174.6 kg
    dry per 3U satellite   7.042 -> 10.547 kg
    kill criterion 1       crossed 3.5x -> crossed 5.3x

The whitelist and the exclusions are inherited verbatim: run sheets, the register, the
changelog, the decision log and the ADRs all record what was true when they were written,
and this script does not rewrite them.

Usage:  python3 tools/propagate_2026_08_16.py [--check]
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# old -> new. Ordered longest-first so a shorter pattern cannot eat a longer one.
SUBS = [
    ("84.5 kg / 132.5 kg", "126.6 kg / 174.6 kg"),
    ("84.5 kg", "126.6 kg"),
    ("84.53 kg", "126.56 kg"),
    ("132.5 kg", "174.6 kg"),
    ("7.042 kg", "10.547 kg"),
    ("7.04 kg", "10.55 kg"),
    ("crossed by 3.5", "crossed by 5.3"),
    ("crossed 3.5", "crossed 5.3"),
    ("3.5x at 3U", "5.3x at 3U"),
]

EXCLUDE_DIRS = {".git", "legacy", "paper", "node_modules", "__pycache__",
                os.path.join("docs", "adr"), os.path.join("validation", "gmat")}
# Files that deliberately retain superseded values as history. Substituting into these
# would rewrite the record, which is the one thing this repository does not do.
EXCLUDE_FILES = {
    "CHANGELOG.md",            # the audit record
    "OPEN_PROBLEMS.md",        # every entry states the value that was wrong at the time
    "HISTORY.md",              # "velocity from 20.37 to 16.54" is a historical sentence
    "DECISION_LOG.md",         # decisions record the numbers they were taken against
    "CHANGELOG_CAD.md",        # ditto, for geometry
    "EMOCD_Computation_Results_C1-C10.md",   # a dated record of a computation set
    "RESULTS.md",              # its own header says earlier audit states are retained
}


def targets():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        rel = os.path.relpath(dirpath, ROOT)
        if any(rel == d or rel.startswith(d + os.sep) for d in EXCLUDE_DIRS):
            dirnames[:] = []
            continue
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for fn in filenames:
            if not fn.endswith((".md", ".html")):
                continue
            if fn in EXCLUDE_FILES:
                continue
            # validation run sheets record runs at their own operating point
            if rel.startswith("validation") and re.match(r"A\d+_.*\.md$", fn):
                continue
            yield os.path.join(dirpath, fn)


def main():
    check = "--check" in sys.argv
    touched, hits = [], 0
    for path in targets():
        src = open(path, encoding="utf-8", errors="ignore").read()
        out = src
        for a, b in SUBS:
            out = out.replace(a, b)
        if out != src:
            n = sum(src.count(a) for a, _ in SUBS)
            hits += n
            touched.append((os.path.relpath(path, ROOT), n))
            if not check:
                open(path, "w", encoding="utf-8").write(out)
    verb = "would change" if check else "changed"
    for rel, n in sorted(touched, key=lambda t: -t[1]):
        print(f"  {n:4d}  {rel}")
    print(f"\n{verb} {hits} occurrences across {len(touched)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
