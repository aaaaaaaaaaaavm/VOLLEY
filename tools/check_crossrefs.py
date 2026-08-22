"""Fail when two committed files disagree about the same physical quantity.

WHY THIS EXISTS
---------------
Seven register entries in ten days were the same defect wearing different clothes:

    P83   the trim authority was sized at a friction share the design point had left behind
    P84   ADR-034 moved parameters.json and the documents, and left the scripts at the old point
    P96   the manuscript argued from a number its own table had already replaced
    P97   ADR-030 shortened the regenerative section and the recovery figure never moved with it
    P100  A57 used a lever arm 15.6x the interface requirement A52 had published six days earlier
    P101  the payload ladder D2 turns on divided a dry mass three corrections out of date
    P102  the only Gen6 tip-off run stayed at a stroke ADR-034 had already replaced

**Every one of them is two files disagreeing about a shared quantity**, and every existing gate
passed while they were true. `make_baseline.py --check` guards the twenty-three values BASELINE.md
publishes. `check_public.py` guards the prose. Neither looks at whether two *results* files agree
with each other, which is where these actually live.

A60 -- a second CAD implementation -- was the planned answer, and it is the wrong shape for this.
A second implementation catches geometry errors, like P71's rollers outside their channels. It
catches none of the five above.

WHAT A CROSS-REFERENCE IS
-------------------------
A quantity that two files both state, where one of them is the source and the other should agree.
Each is declared below with both paths, a tolerance, and **why they must agree** -- because a pair
that must NOT agree is the more common mistake. `gen6_seal.friction_max_N` is 17.8 N and
`seal_class.specification.trim_unnecessary.friction_N` is 22.29 N, and they are supposed to
differ: ADR-036 names them as two ends of a decision. That pair is not in this file, and the
reason it is not is written down.

Tolerances are per-reference and generous where a file legitimately rounds. The point is to catch
15.6x, not 0.03 %.

    python3 tools/check_crossrefs.py
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(ROOT, "analysis", "results")


def _load(name):
    if name == "parameters":
        with open(os.path.join(ROOT, "cad", "parameters.json"), encoding="utf-8") as fh:
            return json.load(fh)["groups"]
    with open(os.path.join(RESULTS, name + ".json"), encoding="utf-8") as fh:
        return json.load(fh)


def _dig(doc, path):
    """Walk a dotted path. A segment of the form key=value selects from a list."""
    cur = doc
    for seg in path.split("."):
        if "=" in seg:
            key, val = seg.split("=", 1)
            cur = next(item for item in cur if str(item.get(key)) == val)
        elif seg.isdigit():
            cur = cur[int(seg)]
        else:
            cur = cur[seg]
    return cur


# (label, source file, source path, consumer file, consumer path, scale, tol %, why)
REFS = [
    ("Gen5 dry mass",
     "mass_properties", "dry_kg", "payload_family", "deployer_dry_kg", 1.0, 0.5,
     "the family table divides this by the manifest; A46 moved it once and the table did not"),
    ("Gen5 dry mass, ledger",
     "mass_properties", "dry_kg", "constraint_ledger", "dry_kg", 1.0, 0.5,
     "A35's shares are percentages of this. P73 and P95 are both this pair disagreeing"),
    ("Gen5 exit velocity",
     "motor_results", "shot.v_exit", "payload_family", "classes.tag=3U CubeSat.v_exit", 1.0, 0.5,
     "P96: the manuscript's prose and its own table forked on exactly this"),
    ("mass per 3U satellite",
     "payload_family", "classes.tag=3U CubeSat.kg_per_satellite",
     "comparators", "kg_per_3U_volley", 1.0, 0.5,
     "P69's ratio is built on it; A21 quoted 6.375 for four days after A46"),
    ("sled energy to the brake",
     "motor_results", "regen.KE_to_brake", "sizing", "energy_closure.KE_to_brake_J", 1.0, 0.5,
     "P97: the closure and the regen block disagreed for eight days"),
    ("energy recovered per shot",
     "motor_results", "regen.E_recovered", "sizing", "energy_closure.regen_recovered_J", 1.0, 0.5,
     "P97 again, and this is the half that was quoted on the front page"),
    ("Gen6 stroke",
     "parameters", "gen6_drive.stroke_mm", "stage_attitude", "inputs.stroke_m", 1000.0, 0.5,
     "P84: ADR-034 moved the stroke and left the scripts behind"),
    ("Gen6 exit velocity, zero friction",
     "parameters", "gen6_drive.exit_velocity_m_s_zero_friction",
     "stage_attitude", "inputs.v_exit_zero_friction_m_s", 1.0, 0.5,
     "the same propagation as the stroke, one field along"),
    ("Gen6 design-point acceleration",
     "parameters", "gen6_drive.acceleration_g", "tipoff_gen6", "design_point.a_g", 1.0, 0.5,
     "P102. A38 is the only run that takes tip-off to Gen6 and it held 25 g as a module constant "
     "while ADR-034 moved the design point. Every cradle figure it publishes scales with this"),
    ("Gen6 design-point stroke, tip-off",
     "parameters", "gen6_drive.stroke_mm", "tipoff_gen6", "design_point.stroke_m", 1000.0, 0.5,
     "P102, the other half. 2.18 m was A37's window and the stroke is now the stage's whole "
     "usable length; the powered time every settling band is measured against descends from it"),
    ("Gen5 dry mass, designed cell",
     "mass_properties", "dry_kg", "cell_manifest", "deployer_dry_kg", 1.0, 0.5,
     "P101. The designed-cell ladder is this number over the manifest count, and it is the table "
     "decision D2 turns on. It sat at 84.5 kg for six days after A46 published 126.6, and the "
     "document quoting it sat at 76.5"),
    ("mass per 3U satellite, volumetric against designed",
     "payload_family", "classes.tag=3U CubeSat.kg_per_satellite",
     "cell_manifest", "classes.tag=3U CubeSat.kg_per_satellite", 1.0, 0.5,
     "P101. At 3U a designed cell holds exactly one satellite, so the two ladders MUST return the "
     "same rung. When they do not, one of them was not re-run"),
    ("thrust-line lever arm",
     "gen6_recoil", "saturating_offset_mm", "stage_attitude", "inputs.lever_arm_m", 1000.0, 1.0,
     "P100. A52 published an alignment REQUIREMENT and A57 modelled the disturbance it causes; "
     "an attitude run must use the arm the interface requires, not one inherited from Gen5"),
]

# Pairs deliberately NOT checked, because they are supposed to differ. Recording them here is
# the point: the next person to notice the difference finds the reason instead of 'fixing' it.
NOT_REFS = [
    ("gen6_seal.friction_max_N (17.8 N) vs seal_class.trim_unnecessary.friction_N (22.29 N)",
     "ADR-036 names both as the two ends of one decision: at or below 17.8 N the trim stator is "
     "unnecessary AND the seal survives its own heat; above 22.3 N the stator is needed. P67 "
     "measures which side. Making them agree would delete the decision"),
    ("gen6_drive.exit_velocity_m_s_zero_friction (34.28) vs _at_friction_allowance (29.01)",
     "A ceiling and a floor. P67 says both are real and neither should appear alone"),
]


def main():
    problems = []
    for label, sf, sp, cf, cp, scale, tol, why in REFS:
        try:
            a = float(_dig(_load(sf), sp))
            b = float(_dig(_load(cf), cp)) * scale
        except (KeyError, StopIteration, IndexError, FileNotFoundError) as exc:
            problems.append(f"{label}: cannot read the pair ({exc!r}). A cross-reference whose "
                            f"path has moved is a defect, not a skip")
            continue
        drift = abs(a - b) / max(abs(a), 1e-12) * 100.0
        if drift > tol:
            problems.append(
                f"{label}: {sf}.{sp} = {a:g} but {cf}.{cp} = {b:g}  ({drift:.2f} % apart, "
                f"tolerance {tol} %)\n      why they must agree: {why}")

    if problems:
        print(f"cross-references: {len(problems)} disagreement(s)\n")
        for p in problems:
            print("  " + p)
        return 1
    print(f"cross-references: {len(REFS)} pairs agree; "
          f"{len(NOT_REFS)} pairs deliberately excluded and documented")
    return 0


if __name__ == "__main__":
    sys.exit(main())
