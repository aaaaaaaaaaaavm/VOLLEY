"""Check that every built artifact is newer than the source it was built from.

WHY THIS EXISTS
---------------
Every other guard here compares an artifact to a *script*: make_baseline.py --check compares
BASELINE.md to the JSON, _check_operating_point() compares two modules, check_links.py compares
links to files. Nothing compared a built file to the thing it was built from.

So on 2026-07-30 paper.tex was corrected twice, for the bank ESR and for a retracted
coilgun-efficiency claim, and the PDF was not rebuilt. The published PDF -- the artifact linked
from the Pages site and shipped inside VOLLEY-paper -- went on printing 2.80 kJ, 20 % efficiency
and the retracted figure, for as long as nobody thought to look. This is that check.

WHY MTIMES WOULD NOT WORK
-------------------------
Git does not record modification times. A fresh clone writes every file at checkout time, so
mtime comparisons are meaningless the moment anyone clones: they would either all pass or all
fail depending on checkout order, and neither answer means anything.

The commit in which each path last changed is the durable fact. `git log -1 --format=%ct -- path`
gives it, and it is identical in every clone. That is what this compares.

USAGE
    python3 tools/check_artifacts.py
Exits non-zero if any artifact is older than its source.
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (artifact, [sources]) -- the artifact must not predate any of its sources.
#
# REGENERATORS. Commit time is a proxy for currency and it is a lossy one: a source can change
# in a way the artifact does not depend on, and the artifact then stays byte-identical and
# permanently "stale". That is not hypothetical -- cad/parameters.json gained gen6_drive and
# gen6_store on 2026-08-14, and Gen5's STEP was reported stale against it while regenerating
# BYTE-IDENTICALLY. A false positive in a check is a defect in the check.
#
# Where an artifact can be rebuilt cheaply and deterministically, name the command. A pair that
# looks stale by time is then REBUILT and compared: if nothing changes, it was current and the
# timestamp was lying. Artifacts with no regenerator fall back to the time comparison.
REGENERATORS = {
    "cad/step/gen5/VOLLEY_Track_Gen5.step": ["python3", "cad/build_gen5.py"],
    "cad/step/gen6/VOLLEY_Drive_Tube_Gen6.step": ["python3", "cad/build_gen6.py"],
}

PAIRS = [
    # The manuscript, the .cls, the built PDF and the CV moved to VOLLEY-paper on
    # 2026-08-13 (ADR-028). They are authored there and are not artifacts of this
    # repository any more, so nothing here can or should guard them.
    # The public Pages site. It served pre-quadrature numbers -- 11.22 N/kA.m, 16.54 m/s,
    # 76.9 kg -- from 2026-08-03 until 2026-08-10, because nothing compared it to the
    # operating point it quotes. That is P42, and this pair is the fix: the site is an
    # artifact of the results, exactly like BASELINE.md and the paper.
    ("docs/index.html", ["analysis/results/motor_results.json",
                         "analysis/results/mass_properties.json",
                         "analysis/results/astro_results.json"]),
    # The CAD package a modeller reads instead of the JSON. Both are built by
    # cad/tools/make_cad_package.py, so a dimension changed in parameters.json without a
    # regenerate leaves them quoting geometry the machine no longer has -- the same shape
    # of defect as P42, aimed at whoever is cutting metal.
    # Checked through the build stamp rather than the .md files, for the same reason the
    # figures are (see below). BOM.md quotes only part of parameters.json, so a change to
    # a group it does not cite leaves it correctly byte-identical and permanently "stale".
    ("cad/BUILD.json", ["cad/parameters.json", "analysis/mass_properties.py",
                        "cad/tools/make_cad_package.py"]),
    # Gen5 is built from parameters.json by cad/build_gen5.py. Guarding one STEP is
    # enough: they are all written by the same call, so any of them being older than the
    # parameter file means the whole generation is.
    ("cad/step/gen5/VOLLEY_Track_Gen5.step", ["cad/parameters.json", "cad/build_gen5.py"]),
    # Gen6 is built the same way, from the same parameter file, by cad/build_gen6.py.
    # Guarding one STEP guards the set: they are written in a single pass or not at all.
    ("cad/step/gen6/VOLLEY_Drive_Tube_Gen6.step",
     ["cad/parameters.json", "cad/build_gen6.py"]),
    ("docs/BASELINE.md", ["analysis/results/motor_results.json",
                          "analysis/results/sizing.json",
                          "analysis/results/astro_results.json",
                          "tools/make_baseline.py"]),
    # The figures are checked through their build stamp, not through the PNGs. A rebuild
    # whose output happens to be byte-identical leaves nothing in git, so commit times
    # cannot distinguish "not rebuilt" from "rebuilt, unchanged" -- and F01 hit exactly
    # that on 2026-07-31, when the shot was untouched but the figure script was not.
    # tools/make_figures.py writes BUILD.json with the operating point it drew from, so the
    # stamp moves whenever the figures are actually regenerated.
    ("figures/BUILD.json", ["analysis/results/motor_results.json",
                            "tools/make_figures.py"]),
    ("figures/BUILD_anim.json", ["analysis/results/motor_results.json",
                                 "tools/make_animation.py"]),
]


def last_commit_time(path):
    """Unix time of the commit that last touched `path`, or None if never committed."""
    out = subprocess.run(
        ["git", "-C", ROOT, "log", "-1", "--format=%ct", "--", path],
        capture_output=True, text=True).stdout.strip()
    return int(out) if out else None


def _regenerates_identically(artifact):
    """Rebuild `artifact` and report whether it came back unchanged.

    Returns False when there is no regenerator, when the build fails, or when the file
    genuinely moved -- all three mean the time comparison should stand.
    """
    cmd = REGENERATORS.get(artifact)
    if not cmd:
        return False
    path = os.path.join(ROOT, artifact)
    try:
        with open(path, "rb") as fh:
            before = fh.read()
        r = subprocess.run(cmd, cwd=ROOT, capture_output=True, timeout=900)
        if r.returncode != 0:
            return False
        with open(path, "rb") as fh:
            return fh.read() == before
    except Exception:
        return False


def main():
    dirty = subprocess.run(["git", "-C", ROOT, "status", "--porcelain"],
                           capture_output=True, text=True).stdout.strip()
    if dirty:
        print("note: working tree is dirty, so this compares committed state only.\n")

    stale, missing, proven, ok = [], [], [], 0
    for artifact, sources in PAIRS:
        if not os.path.exists(os.path.join(ROOT, artifact)):
            missing.append(artifact)
            continue
        a_time = last_commit_time(artifact)
        if a_time is None:
            missing.append(f"{artifact} (never committed)")
            continue
        for src in sources:
            s_time = last_commit_time(src)
            if s_time is None:
                continue
            if a_time < s_time:
                behind = (s_time - a_time) / 3600.0
                if _regenerates_identically(artifact):
                    proven.append((artifact, src))
                else:
                    stale.append((artifact, src, behind))
        ok += 1

    for artifact, src in proven:
        print(f"CURRENT  {artifact}")
        print(f"         older than {src} by commit time, but rebuilds byte-identically")

    for artifact, src, behind in stale:
        print(f"STALE  {artifact}")
        print(f"       built before {src}, which changed {behind:.1f} h later")
        print(f"       rebuild it, or the published artifact contradicts its own source")
    for m in missing:
        print(f"MISSING  {m}")

    if not stale and not missing:
        print(f"artifacts: {ok} checked, all newer than their sources")
        return 0
    print(f"\n{len(stale)} stale, {len(missing)} missing, of {len(PAIRS)} checked")
    return 1


if __name__ == "__main__":
    sys.exit(main())
