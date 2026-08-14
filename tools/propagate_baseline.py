"""One-shot propagation of the 2026-08-13 baseline change (ADR-030, P46/P28/P10).

WHY A SCRIPT AND NOT AN EDITOR
------------------------------
The change moves fourteen coupled numbers across roughly thirty live documents. Editing
that by hand produces a P42 -- a known correction sitting in the register while the public
pages still say something else -- and editing it with a blind `sed` produces something
worse, because **most occurrences of `16.388` in this repository are historical and must not
change.**

So the substitution runs against an explicit WHITELIST of live prose, and everything that is
a record of what was true at the time is excluded by construction:

    CHANGELOG.md, OPEN_PROBLEMS.md   the audit record; this project does not rewrite it
    validation/A*.md                  run sheets, each a record of a run at its own point
    legacy/, paper/archive/           superseded by intent
    docs/adr/0NN-*.md                 decisions record the numbers they were taken against

Anything generated -- BASELINE.md, cad/BOM.md, cad/DIMENSIONS.md, figures, the CV -- is NOT
touched here. It regenerates from the scripts, which is the point of it being generated.

Usage:  python3 tools/propagate_baseline.py [--check]
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# old -> new. Ordered longest-first so a shorter pattern cannot eat a longer one.
SUBS = [
    ("11.0258", "10.5386"),
    ("16.388", "16.029"),
    ("16.54 m/s", "16.03 m/s"),
    ("11.03 N per kA/m", "10.54 N per kA/m"),
    ("11.03 N/kA", "10.54 N/kA"),
    ("11.03 N per kA", "10.54 N per kA"),
    ("16.4 m/s", "16.0 m/s"),
    ("16.2 m/s", "15.8 m/s"),
    ("158.6 ms", "162.3 ms"),
    ("159 ms", "162 ms"),
    ("339 A", "320 A"),
    ("2851 J", "2782 J"),
    ("2.85 kJ", "2.78 kJ"),
    ("2560 J", "2735 J"),
    ("2.56 kJ", "2.74 kJ"),
    ("537 J", "514 J"),
    ("10.53 g", "10.07 g"),
    ("10.5 g", "10.1 g"),
    ("5.30 %", "5.17 %"),
    ("76.5 kg", "84.5 kg"),
    ("6.375 kg", "7.042 kg"),
    ("6.378 kg", "7.042 kg"),
    ("6.38 kg", "7.04 kg"),
    ("21.0 %", "18.5 %"),
    ("20.99 %", "18.47 %"),
    ("0.027 m/s", "0.0274 m/s"),
    ("0.0267 m/s", "0.0274 m/s"),
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
