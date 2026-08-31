"""Re-run the cheap deterministic analyses and require byte-identical results.

WHY THIS EXISTS
---------------
P110 corrected A70's markdown and left `analysis/results/guided_contact_derived.json` holding the
superseded numbers -- including the 37.33 um figure the correction withdrew -- and the companion
export shipped that stale JSON to a public repository. The run sheet said one thing, the generator
another, and the committed result a third. Every other gate passed.

check_crossrefs.py compares two results files to each other. check_companions.py compares the
payload to the flagship. Nothing compared a results file to the script that claims to produce it.
This does.

WHY THE COMPARISON IS NUMERICAL, AND WHY THE TOLERANCE IS PER FILE
------------------------------------------------------------------
It was byte-for-byte until 2026-08-26, and that was wrong in a way nothing local could
show. The comparison passed on the machine the results were committed from and failed on
a GitHub runner, on `run_a69.py` and `run_a70.py`. Byte identity of floating-point JSON
across two machines was never an achievable property, and the gate had only ever run on
one machine.

The first diagnosis of that failure was wrong and is withdrawn. It read the disagreement
as ordinary last-bit BLAS sensitivity in A69 -- measured at 3e-9 locally -- amplified into
A70 by the cancellation in a three-point sagitta. The amplification is a real property of a
sagitta, but it was not what happened: when the runner reported field by field, the fields
that moved were A69's own, by 8.5e-4, and A70's sagittas moved LESS than their input, not
33,000 times more.

What was actually happening is P115. `beam()` held its rigid supports with a diagonal
penalty of 1e8 times the element stiffness, which put the assembled 1602-DOF system at a
condition number of 8.6e15 against a double-precision epsilon of 2.2e-16. Nothing survives
that along the worst direction. Only the cases with a PRESCRIBED support offset moved,
because only those put the penalty into the right-hand side as well, and those are exactly
the fields the runner named. The supports are now imposed by eliminating the constrained
rows, cond 4.1e9, and the two answers differ by 8.5e-4 -- which was the penalty solve's
error, not this one's.

Perturbing every entry of the matrix and the right-hand side by one ulp and re-solving,
which is roughly what a different summation order does, moves the reported quantities by:

  penalty supports, as committed before 2026-08-26      4.3e-3
  eliminated supports, as now                           4.4e-8

The observed cross-machine disagreement, 8.5e-4, sits inside the first and far outside the
second. Both files therefore carry 1e-7, measured rather than fitted, and the rest of the
set stays at 1e-9.

This is not a widened band. The gate still catches staleness by seven orders of magnitude:
P110's defect, the one this gate exists for, was a factor of 15.6.

Three leaves in that file still could not hold 1e-7, and they are named individually rather
than by loosening the file. The free-free first mode comes out of a generalised eigenproblem
and moves by 2.0e-6 under the same perturbation; band 3 tests it against A59's 1.67 Hz at 5 %.
The two `err_pct` fields are the solver's residuals against closed forms, 3.4e-7 and 2.3e-6
PERCENT, which is a difference of two numbers agreeing to fifteen digits: there are no
significant figures in them to reproduce, so they carry an absolute tolerance instead, five
orders below the 0.5 % band that tests them.

Nine injected faults were used on this arrangement, including one that returns the SECOND
elastic mode in place of the first.

WHAT IS AND IS NOT CHECKED
--------------------------
The committed file is restored after every comparison, pass or fail. A checker that leaves
its own output behind is a generator, and CI's later `git diff --exit-code` then fails on a
file this gate wrote.

Only analyses that are cheap AND deterministic. A run with a Monte Carlo, a long integration or a
solver sweep is excluded by name with the reason, because re-running it on every commit would cost
more than it protects -- but an excluded run is listed, so the exclusion is visible rather than
implicit.

    python3 tools/check_results_fresh.py
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(ROOT, "analysis", "results")

# (script, results file) -- cheap and deterministic, re-run every time.
FRESH = [
    ("analysis/run_a70.py", "guided_contact_derived.json"),
    ("analysis/run_a69.py", "tube_centreline.json"),
    ("analysis/cell_manifest.py", "cell_manifest.json"),
    ("analysis/payload_family.py", "payload_family.json"),
    ("analysis/mass_properties.py", "mass_properties.json"),
    ("analysis/host_reference.py", "host_reference.json"),
    ("analysis/tube_shielding.py", "tube_shielding.json"),
]

# Relative tolerance for numeric leaves, per file, each with the reason it is what it is.
# A tolerance without a reason beside it is a widened band. See the module docstring.
RTOL_DEFAULT = 1e-9
ATOL = 1e-12
RTOL = {
    "tube_centreline.json":
        (1e-7, "a constrained linear solve at cond 4.1e9; a one-ulp perturbation of the "
               "system moves the reported peaks by 4.4e-8"),
    "guided_contact_derived.json":
        (1e-7, "the same centreline, read as three-point sagittas; same perturbation, 4.7e-8"),
}

# Three leaves inside tube_centreline.json cannot hold the file's tolerance, each for a reason
# that is about the quantity rather than about the gate. Named individually so the rest of the
# file stays at 1e-7.
FIELD = {
    "tube_centreline.json:/free_free_f1_Hz":
        ("rel", 1e-5, "a generalised eigenproblem through scipy at cond(M) 2.0e6, with the two "
                      "rigid-body modes six orders below the first elastic one; a one-ulp "
                      "perturbation moves it by 2.0e-6"),
    "tube_centreline.json:/simple_span/err_pct":
        ("abs", 1e-5, "the solver's residual against a closed form, in percent, and it is 3.4e-7 "
                      "-- a difference of two numbers that agree to fifteen digits, so it has no "
                      "significant figures to reproduce. Band 1 tests it at 0.5 %"),
    "tube_centreline.json:/imposed_curvature_check/err_pct":
        ("abs", 1e-5, "the same residual for the imposed-curvature case, 2.3e-6 percent, and the "
                      "same reason. Band 1 tests it at 0.5 %"),
}

# Excluded, by name and with the reason. An exclusion that is not written down is a gap.
EXCLUDED = [
    ("analysis/run_a67.py", "guided_contact.json",
     "a 288-sample Sobol design over a fixed-step integration; tens of minutes"),
    ("analysis/run_a68.py", "contact_laws.json",
     "45 impact integrations at 2e-8 s plus a root-find per restitution; tens of minutes"),
    ("analysis/motor_model.py", "motor_results.json",
     "guarded by make_baseline.py --check, which compares 23 values against live script output"),
    ("analysis/tube_requirement.py", "tube_requirement.json",
     "twelve nested root-finds, each one an inversion of array_drag's own root-find over the "
     "shot integration; several minutes"),
    ("analysis/trim_secondary.py", "trim_secondary.json",
     "a magpylib field solve over 720 CylinderSegment sources at five magnet depths, plus a "
     "large-radius limit case and a sector-convergence sweep; about ten minutes"),
    ("analysis/array_drag.py", "array_drag.json",
     "a root-find over a 2000-step integration, twice per field, over six fields and four "
     "sensitivity corners, plus a second root-find over the conductance; 44 s"),
]


_NUM = re.compile(r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?')


def _close(a, b, rtol):
    if a == b:
        return True
    return abs(a - b) <= max(ATOL, rtol * max(abs(a), abs(b)))


def _strings_agree(a, b, rtol):
    """True if two strings differ only in embedded numbers, within tolerance.

    Run sheets embed computed values in prose, so a band's `detail` line moves when the
    number in it moves. Comparing those exactly would reimpose byte identity through the
    back door, and ignoring them would stop checking the text.
    """
    if _NUM.sub("#", a) != _NUM.sub("#", b):
        return False
    for x, y in zip(_NUM.findall(a), _NUM.findall(b)):
        try:
            if not _close(float(x), float(y), rtol):
                return False
        except ValueError:
            return False
    return True


def differing(a, b, path="", rtol=RTOL_DEFAULT, name=""):
    """Paths at which two parsed JSON values disagree beyond the file's tolerance."""
    if isinstance(a, dict) and isinstance(b, dict):
        out = []
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                out.append(path + "/" + str(k))
            else:
                out += differing(a[k], b[k], path + "/" + str(k), rtol, name)
        return out
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            return [path + f" (length {len(a)} against {len(b)})"]
        out = []
        for i, (x, y) in enumerate(zip(a, b)):
            out += differing(x, y, path + f"[{i}]", rtol, name)
        return out
    if isinstance(a, bool) or isinstance(b, bool):
        return [] if a is b else [path]
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        kind, tol, _why = FIELD.get(f"{name}:{path}", ("rel", rtol, ""))
        ok = abs(a - b) <= tol if kind == "abs" else _close(a, b, tol)
        return [] if ok else [path + f" ({a} against {b})"]
    if isinstance(a, str) and isinstance(b, str):
        return [] if a == b or _strings_agree(a, b, rtol) else [path]
    return [] if a == b else [path]


def main():
    tmp = tempfile.mkdtemp(prefix="volley-fresh-")
    problems = []
    try:
        for script, name in FRESH:
            live = os.path.join(RESULTS, name)
            if not os.path.exists(live):
                problems.append(f"{name}: missing; {script} has never been run")
                continue
            backup = os.path.join(tmp, name)
            shutil.copy(live, backup)
            r = subprocess.run([sys.executable, os.path.join(ROOT, script)],
                               cwd=ROOT, capture_output=True, text=True)
            if r.returncode != 0:
                shutil.copy(backup, live)
                problems.append(f"{script}: exited {r.returncode}. "
                                f"{r.stderr.strip().splitlines()[-1] if r.stderr.strip() else ''}")
                continue
            with open(live, encoding="utf-8") as fh:
                new = fh.read()
            with open(backup, encoding="utf-8") as fh:
                old = fh.read()
            # Put the committed file back whatever the verdict. This gate re-runs a script to
            # look at its output, and a checker that leaves its own output in the working tree
            # is a generator. On one machine the two are byte-identical and nothing shows; on
            # another the difference is real and the next step to run `git diff --exit-code`
            # fails on a file this gate wrote, not on anything that drifted.
            shutil.copy(backup, live)
            if new != old:
                rtol = RTOL.get(name, (RTOL_DEFAULT, ""))[0]
                try:
                    moved = differing(json.loads(old), json.loads(new), rtol=rtol, name=name)
                except Exception:
                    moved = ["<unparseable>"]
                if moved:
                    problems.append(f"{name}: committed result differs from what {script} "
                                    f"produces now, beyond {rtol:g} relative. Moved: "
                                    f"{', '.join(moved[:6])}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    if problems:
        print(f"results freshness: {len(problems)} problem(s)\n")
        for p in problems:
            print(f"  {p}")
        print("\n  fix: re-run the script and commit its output, or find why it moved")
        return 1
    print(f"results freshness: {len(FRESH)} results reproduce, {len(RTOL)} at a declared "
          f"per-file tolerance and {len(FIELD)} fields at their own, the rest at "
          f"{RTOL_DEFAULT:g}; {len(EXCLUDED)} runs excluded by name with reasons")
    return 0


if __name__ == "__main__":
    sys.exit(main())
