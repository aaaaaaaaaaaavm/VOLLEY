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

WHY THE COMPARISON IS NUMERICAL AND NOT BYTE-FOR-BYTE
-----------------------------------------------------
It was byte-for-byte until 2026-08-26, and that was wrong in a way nothing local could
show. The comparison passed on the machine the results were committed from and failed on
a GitHub runner, on `run_a69.py` and `run_a70.py`: both solve eigenvalue and linear
systems through numpy, and the last bits of a float depend on the BLAS the interpreter
was built against. Byte identity of floating-point JSON across two machines was never an
achievable property, and the gate had only ever been run on one.

So values are compared numerically, at RTOL below, and everything non-numeric is still
compared exactly. That is not a weakening. The defect this gate exists to catch is a
committed result that no longer matches its generator, and P110's was a factor of 15.6;
a tolerance of 1e-9 catches that and every defect of its kind, while tolerating the 1e-16
that separates one BLAS from another.

WHAT IS AND IS NOT CHECKED
--------------------------
Only analyses that are cheap AND deterministic. A run with a Monte Carlo, a long integration or a
solver sweep is excluded by name with the reason, because re-running it on every commit would cost
more than it protects -- but an excluded run is listed, so the exclusion is visible rather than
implicit.

    python3 tools/check_results_fresh.py
"""
import json
import os
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
]

# Relative tolerance for numeric leaves. Tight enough that any real staleness fails, loose
# enough that two BLAS implementations agree. See the module docstring.
RTOL = 1e-9
ATOL = 1e-12

# Excluded, by name and with the reason. An exclusion that is not written down is a gap.
EXCLUDED = [
    ("analysis/run_a67.py", "guided_contact.json",
     "a 288-sample Sobol design over a fixed-step integration; tens of minutes"),
    ("analysis/run_a68.py", "contact_laws.json",
     "45 impact integrations at 2e-8 s plus a root-find per restitution; tens of minutes"),
    ("analysis/motor_model.py", "motor_results.json",
     "guarded by make_baseline.py --check, which compares 23 values against live script output"),
]


def differing(a, b, path=""):
    """Paths at which two parsed JSON values disagree beyond RTOL/ATOL."""
    if isinstance(a, dict) and isinstance(b, dict):
        out = []
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                out.append(path + "/" + str(k))
            else:
                out += differing(a[k], b[k], path + "/" + str(k))
        return out
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            return [path + f" (length {len(a)} against {len(b)})"]
        out = []
        for i, (x, y) in enumerate(zip(a, b)):
            out += differing(x, y, path + f"[{i}]")
        return out
    if isinstance(a, bool) or isinstance(b, bool):
        return [] if a is b else [path]
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        if a == b:
            return []
        scale = max(abs(a), abs(b))
        return [] if abs(a - b) <= max(ATOL, RTOL * scale) else [path + f" ({a} against {b})"]
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
            if new != old:
                try:
                    moved = differing(json.loads(old), json.loads(new))
                except Exception:
                    moved = ["<unparseable>"]
                if moved:
                    problems.append(f"{name}: committed result differs from what {script} "
                                    f"produces now, beyond {RTOL:g} relative. Moved: "
                                    f"{', '.join(moved[:6])}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    if problems:
        print(f"results freshness: {len(problems)} problem(s)\n")
        for p in problems:
            print(f"  {p}")
        print("\n  fix: re-run the script and commit its output, or find why it moved")
        return 1
    print(f"results freshness: {len(FRESH)} results reproduce to {RTOL:g} relative; "
          f"{len(EXCLUDED)} runs excluded by name with reasons")
    return 0


if __name__ == "__main__":
    sys.exit(main())
