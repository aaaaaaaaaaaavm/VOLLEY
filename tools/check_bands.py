"""Find acceptance-band verdicts that are assigned rather than computed.

WHY THIS EXISTS
---------------
P110. A69 band 4 -- "a continuous centreline is returned and exported" -- was implemented as
`b4 = True`. It was the one band that would have caught a thermal construction that kinked a
continuous tube at every support, and it was the one band that was not computed. A70 band 6 was
`b6 = True` with the dynamics disabled, so it recorded a PASS on an energy balance nothing had
evaluated.

Every repository gate passed while both were true. The gates check that the record is consistent;
they cannot check that a model is right. This is the narrow part that CAN be automated: a verdict
that is a literal is not a verdict.

WHAT IT ALLOWS
--------------
A band may legitimately be report-only -- "report the trend", "name the dominant input" -- and
those must not be outlawed. What is not allowed is a report-only criterion counted in a
"six of seven passed" verification tally without being declared as such.

So a literal verdict must be declared in ALLOW below, naming the file, the variable and why.

    python3 tools/check_bands.py
"""
import ast
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCAN = ("analysis", "cad", "tools")

# (file, variable, reason). Each line is a claim that a human read it.
ALLOW = [
    ("analysis/run_a69.py", "b6",
     "report-only by declaration: A69 band 6 asks for the pressure-induced bore growth to be "
     "REPORTED against the clearance, and the figure is computed and printed. It has no "
     "threshold and is recorded as report-only, not as verification"),
    ("analysis/run_a69.py", "b8",
     "report-only by declaration: A69 band 8 asks that the contributions be reported separately "
     "and ranked, and the ranking is computed from the cases. No threshold exists to compute"),
]


def literal_verdicts(path):
    """Assignments of a bare True/False to a band-verdict-looking name."""
    try:
        tree = ast.parse(open(path, encoding="utf-8").read())
    except SyntaxError:
        return []
    out = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        if not (isinstance(node.value, ast.Constant) and node.value.value in (True, False)):
            continue
        for t in node.targets:
            if isinstance(t, ast.Name) and (
                    t.id.startswith("b") and t.id[1:].isdigit()
                    or t.id.startswith("band") and t.id[4:].isdigit()
                    or t.id in ("passed", "ok", "verdict")):
                out.append((t.id, node.lineno))
    return out


def main():
    allowed = {(f, v) for f, v, _ in ALLOW}
    problems = []
    checked = 0
    for sub in SCAN:
        for dirpath, _dirs, files in os.walk(os.path.join(ROOT, sub)):
            for f in files:
                if not f.endswith(".py"):
                    continue
                full = os.path.join(dirpath, f)
                rel = os.path.relpath(full, ROOT)
                checked += 1
                for name, line in literal_verdicts(full):
                    if (rel, name) not in allowed:
                        problems.append(f"{rel}:{line}: `{name}` is assigned a literal. A band "
                                        f"verdict must be COMPUTED, or declared report-only in "
                                        f"tools/check_bands.py's ALLOW list with a reason")
    if problems:
        print(f"bands: {len(problems)} problem(s)\n")
        for p in problems:
            print(f"  {p}")
        return 1
    print(f"bands: {checked} scripts scanned, no uncomputed band verdicts; "
          f"{len(ALLOW)} declared report-only or not-evaluable")
    return 0


if __name__ == "__main__":
    sys.exit(main())
