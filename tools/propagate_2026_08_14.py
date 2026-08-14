"""One-shot propagation of the 2026-08-14 consistency sweep (P53).

WHY A SECOND SCRIPT AND NOT AN EDIT TO THE FIRST
------------------------------------------------
`propagate_baseline.py` is the record of what the 2026-08-13 change moved. Rewriting its
SUBS table to cover a later change would destroy that record and make the earlier
propagation unreproducible. Each propagation gets its own script, kept afterwards.

WHAT THIS ONE CARRIES
---------------------
P53 found eight analysis scripts and one mass constant still running at the superseded
operating point. Re-running them moved eight published quantities. This walks the same
whitelist of live prose that the first script did, with the same exclusions, and applies
only patterns long enough to be unambiguous.

WHAT IT DELIBERATELY DOES NOT CARRY
-----------------------------------
The bare string `7.5x` appears in two unrelated roles -- the lifetime-extension ratio
against the fastest spring (now 7.33) and the cold-gas mass loss at 3U (now 8.28). A
substitution cannot tell them apart, so both are left to a hand pass. Getting that wrong
would put the wrong claim in the front door, which is worse than leaving it stale.

Usage:  python3 tools/propagate_2026_08_14.py [--check]
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# old -> new. Ordered longest-first so a shorter pattern cannot eat a longer one.
SUBS = [
    # exit velocity, the two-decimal rounded form the first propagation never saw
    ("16.39 m/s", "16.03 m/s"),
    # force ripple, moved by the depth-resolved integral
    ("±0.99 %", "±1.01 %"),
    ("+/-0.99 %", "+/-1.01 %"),
    # orbital lifetime
    ("x1.62", "x1.60"),
    ("×1.62", "×1.60"),
    ("1.62x", "1.60x"),
    ("+61.8 %", "+60.2 %"),
    ("61.8 %", "60.2 %"),
    # ratios against the fastest published spring
    ("7.52×", "7.33×"),
    ("7.52x", "7.33x"),
    ("6.6×", "6.4×"),
    ("6.6x", "6.4x"),
    ("6.56×", "6.41×"),
    # recoil and campaign impulse
    ("65.6 N·s", "64.1 N·s"),
    ("65.6 N.s", "64.1 N.s"),
    ("0.787 kN·s", "0.769 kN·s"),
    # loaded mass, stale since the dry mass moved
    ("124.5 kg", "132.5 kg"),
]

EXCLUDE_DIRS = {".git", "legacy", "paper", "node_modules", "__pycache__",
                os.path.join("docs", "adr"), os.path.join("validation", "gmat")}
EXCLUDE_FILES = {
    "CHANGELOG.md",
    "OPEN_PROBLEMS.md",
    "HISTORY.md",
    "DECISION_LOG.md",
    "CHANGELOG_CAD.md",
    "EMOCD_Computation_Results_C1-C10.md",
    "RESULTS.md",
    # Generated. It regenerates from the scripts, which is the point of it being generated,
    # and writing into it would only make make_baseline.py --check disagree with itself.
    "BASELINE.md",
    # Its every occurrence is a dated narrative of what the value used to be. Line 261 already
    # reads "16.03 m/s (before the quadrature correction)", so substituting 16.39 -> 16.03
    # would produce two identical rows describing opposite points in time.
    "DESIGN_OPTIONS_exit_velocity.md",
}
# Same reason, but the file name is not unique enough to exclude by basename alone.
EXCLUDE_PATHS = {os.path.join("cad", "README.md")}


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
            if os.path.normpath(os.path.join(rel, fn)) in EXCLUDE_PATHS:
                continue
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
    print(f"{verb} {hits} occurrence(s) across {len(touched)} file(s)")


if __name__ == "__main__":
    main()
