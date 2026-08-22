"""A57: attitude rate and packaging on the stage, for Gen6.

WHAT THIS ANSWERS
-----------------
The two `NEEDS SOURCE` rows in docs/KILL_CRITERIA.md -- row 2 (envelope) and row 5 (attitude rate
at firing). Both were quantified for Gen5 and neither was recomputed after ADR-032 changed the
architecture.

Gen6 deleted the mover and kept the problem. What translates internally is no longer a 9.445 kg
sled over 1.50 m; it is the 4 kg payload over 8.0 m, on a vehicle an order of magnitude heavier.
Displacement up 5.3x, moving mass down 2.4x, and nobody had multiplied those together.

THE MODEL IS A13'S, DELIBERATELY
--------------------------------
`attitude_budget.move()` is imported rather than reimplemented. It is the corrected A13 model --
the host counter-rotates while the mass moves, returns to zero rate when it stops, and retains an
attitude offset -- and reimplementing it here would create a second copy to keep in step (P19,
P58, P61 are all that failure). Band 1 re-verifies conservation through the import.

BAND 5 REFUSES TO ANSWER, AND THAT IS THE POINT
-----------------------------------------------
A13 band 5 passed by comparing its result against a host reaction-control authority of 0.1 N.m
that E5 records does not exist. The calculation was right and the reference was invented, which is
P94. This script therefore reports the momentum the host must absorb and REFUSES to divide it by
anything. `attitude_budget.RCS_TORQUE` is never read here -- there is an assertion that says so --
so a future edit cannot quietly reintroduce the comparison.

Bands declared in validation/A57_stage_attitude_packaging.md before this file existed.
Provenance: model output. Rigid-body, ideal, no flexibility, no slosh, no control system.
Host mass is parametric across E5's range because no candidate stage publishes one.
"""
import ast
import hashlib
import json
import math
import os
import platform

import attitude_budget as ab
import motor_model as mm

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results")

# E5: no candidate stage publishes a mass. The range is the band's, not a choice.
HOST_MASSES = (300.0, 500.0, 700.0, 900.0)
N_SHOTS = 12
WHEEL_N_M_S = 15.0          # A52's wheel, reused so the two attitude runs are comparable


def _a52_saturating_offset_m():
    """A52's interface requirement: the thrust line must pass this close to the host CoM.

    The first run of this script used attitude_budget.ASSUMED_ARM = 0.166 m -- A13's arm from a
    GEN5 host centre of mass to the DEPLOYER's, inherited without asking whether it describes a
    Gen6 geometry. It does not. For a payload traversing the drive tube, the arm that matters is
    the perpendicular distance from the host CoM to the line of travel, and A52 already published
    a requirement on exactly that: 10.65 mm.

    166 mm is 15.6x A52's requirement. A design meeting its own stated interface has the smaller
    arm, so the first run was conservative by that factor in every attitude figure. Read live
    from A52 rather than restated. P100.
    """
    with open(os.path.join(RESULTS, "gen6_recoil.json"), encoding="utf-8") as fh:
        return json.load(fh)["saturating_offset_mm"] / 1000.0
G = 9.80665


def _params():
    with open(os.path.join(os.path.dirname(HERE), "cad", "parameters.json"), encoding="utf-8") as fh:
        return json.load(fh)["groups"]


def _stage_inertia(mass, length_m):
    """A slender stage about a transverse axis through its centre.

    A13 used a stubby cylinder scaled from 500 kg because a Gen5 host was a satellite bus. A
    Gen6 host is the stage itself and its length is the rail: 8 m of tube, not a 2 m bus. Using
    A13's aspect ratio here would understate the inertia and flatter every offset below.
    """
    radius = 0.9                     # DECLARED: a large upper stage's radius, E5 has no source
    return mass * (3.0 * radius ** 2 + length_m ** 2) / 12.0


def run():
    p = _params()
    drive = p["gen6_drive"]
    stroke = drive["stroke_mm"] / 1000.0
    rail_as_drawn = 8.2                       # ADR-034
    usable = 8.0                              # A37's usable acceleration length
    v_free = drive["exit_velocity_m_s_zero_friction"]
    m_sat = ab.M_SAT                      # the 3U reference, imported not restated
    a_g = drive["acceleration_g"]

    # duration of the stroke at constant acceleration: v = a t, s = v t / 2
    t_stroke = 2.0 * stroke / v_free

    # The arm is swept rather than assumed. Its two ends are the only two the repository has:
    # A52's published alignment requirement, and the arm A13 inherited from Gen5.
    arm_required = _a52_saturating_offset_m()
    arm_inherited = ab.ASSUMED_ARM
    arm = arm_required          # the design meeting its own interface requirement

    rows = []
    for host in HOST_MASSES:
        inertia = _stage_inertia(host, rail_as_drawn)
        shot = ab.move(m_sat, stroke, t_stroke, inertia, arm=arm)
        rows.append(dict(
            host_kg=host,
            inertia_kgm2=round(inertia, 2),
            stroke_duration_ms=round(t_stroke * 1000.0, 2),
            peak_body_rate_deg_s=round(shot["peak_body_rate_deg_s"], 6),
            residual_body_rate_deg_s=shot["residual_body_rate_deg_s"],
            offset_per_shot_deg=round(abs(shot["attitude_offset_deg"]), 6),
            offset_campaign_deg=round(abs(shot["attitude_offset_deg"]) * N_SHOTS, 6),
            angular_momentum_Ns_m=round(m_sat * arm * v_free, 4),
        ))

    light = rows[0]

    # --- Gen5 comparison at the same host mass, using A13's own geometry (band 4) ---
    gen5_inertia = _stage_inertia(HOST_MASSES[0], rail_as_drawn) + ab.deployer_inertia()
    gen5 = ab.move(ab.M_SLED, ab.SLED_TRAVEL, ab.T_RETURN, gen5_inertia, arm=arm_inherited)
    gen5_offset = abs(gen5["attitude_offset_deg"])

    # --- packaging (bands 6, 7, 8) ---
    #
    # The overrun is END HARDWARE, not stroke. ADR-034: "8.0 m of stroke plus end hardware makes
    # the rail 8.2 m". The stroke already equals the usable length exactly, so the contingency
    # bands 7 and 8 price is the one ADR-034 names: if the end hardware cannot live outside the
    # usable acceleration length, the STROKE gives up that 200 mm.
    #
    # The first version of this function cut the stroke to `usable` -- which is what the stroke
    # already was -- so bands 7 and 8 passed at a 0.0 % loss and an unchanged acceleration. A band
    # that passes by identity has not been tested. Corrected 2026-08-22, before the run was
    # recorded; the bands themselves are unchanged.
    end_hardware = rail_as_drawn - stroke
    overrun_mm = (rail_as_drawn - usable) * 1000.0
    stroke_fitted = usable - end_hardware
    v_fitted = v_free * math.sqrt(stroke_fitted / stroke)   # v ~ sqrt(L) at fixed acceleration
    v_loss_pct = 100.0 * (v_free - v_fitted) / v_free
    # at fixed shot energy the acceleration rises as the stroke shortens
    a_fitted_g = a_g * (stroke / stroke_fitted)

    # --- band 5: momentum only. No authority, no margin. ---
    momentum_per_shot = m_sat * arm * v_free
    momentum_campaign = momentum_per_shot * N_SHOTS
    momentum_sweep = [
        dict(arm_mm=round(a * 1000.0, 4), per_shot_Nms=round(m_sat * a * v_free, 4),
             campaign_Nms=round(m_sat * a * v_free * N_SHOTS, 4), source=src)
        for a, src in ((arm_required, "A52 band 4, the published alignment requirement"),
                       (arm_inherited, "A13's Gen5 arm, inherited by the first run of this "
                                       "script and not applicable to a Gen6 geometry (P100)"))]

    bands = [
        dict(band=1, question="host rate returns to zero", limit="<= 1e-9 deg/s",
             value=max(r["residual_body_rate_deg_s"] for r in rows),
             verdict="PASS" if max(r["residual_body_rate_deg_s"] for r in rows) <= 1e-9 else "FAIL"),
        dict(band=2, question="attitude offset per shot, lightest host", limit="<= 2.0 deg",
             value=light["offset_per_shot_deg"],
             verdict="PASS" if light["offset_per_shot_deg"] <= 2.0 else "FAIL"),
        dict(band=3, question="campaign offset, twelve shots, lightest host", limit="<= 15 deg",
             value=light["offset_campaign_deg"],
             verdict="PASS" if light["offset_campaign_deg"] <= 15.0 else "FAIL"),
        dict(band=4, question="Gen6 against Gen5 offset per shot, same host",
             limit="REPORT, no pass/fail",
             value=round(light["offset_per_shot_deg"] / gen5_offset, 4),
             gen5_offset_deg=round(gen5_offset, 4), verdict="REPORT"),
        dict(band=5, question="momentum the host must absorb",
             limit="REPORT in N.m.s; NO comparison against any control authority (E5, P94)",
             per_shot_Nms=round(momentum_per_shot, 4),
             campaign_Nms=round(momentum_campaign, 4),
             authority_comparison="NOT COMPUTED -- no host control authority exists in this "
                                  "project (E5). A13 band 5 passed against an invented one (P94) "
                                  "and this band exists so that cannot recur. The band forbids a "
                                  "margin, so A52's declared wheel is NOT reported in this band; "
                                  "see findings.wheel_observation, which is outside the bands",
             verdict="REPORT"),
        dict(band=6, question="rail as drawn fits A37's usable acceleration length",
             limit="overrun <= 0 mm", value=round(overrun_mm, 1),
             verdict="PASS" if overrun_mm <= 0.0 else "FAIL"),
        dict(band=7, question="exit-velocity cost of cutting the stroke to fit",
             limit="<= 2 % of zero-friction v_exit", value=round(v_loss_pct, 4),
             v_fitted_m_s=round(v_fitted, 4), stroke_fitted_m=round(stroke_fitted, 4),
             end_hardware_m=round(end_hardware, 4),
             verdict="PASS" if v_loss_pct <= 2.0 else "FAIL"),
        dict(band=8, question="payload acceleration at the fitted stroke",
             limit="<= 25 g (this design's own ceiling, P98)", value=round(a_fitted_g, 4),
             verdict="PASS" if a_fitted_g <= 25.0 else "FAIL"),
    ]

    # Band 5 is a promise about this file, so it is enforced in this file. It parses its own
    # source and looks for an attribute ACCESS, not for the word: a string search trips on the
    # docstring that forbids it, and on the check itself. This is the check A13 did not have.
    forbidden = "RCS" + "_TORQUE"
    tree = ast.parse(open(__file__, encoding="utf-8").read())
    assert not [n for n in ast.walk(tree)
                if isinstance(n, ast.Attribute) and n.attr == forbidden], \
        "band 5: this script must not read a host control authority (E5, P94)"

    return dict(
        analysis="A57",
        bands_declared_in="validation/A57_stage_attitude_packaging.md",
        note="rigid-body, ideal. No flexibility, slosh or control system. Host mass parametric "
             "across E5's range because no candidate stage publishes one. Nothing measured.",
        inputs=dict(payload_kg=m_sat, stroke_m=stroke, rail_as_drawn_m=rail_as_drawn,
                    usable_m=usable, v_exit_zero_friction_m_s=v_free,
                    lever_arm_m=arm,
                    lever_arm_source="A52 band 4, saturating_offset_mm, read live from "
                                     "gen6_recoil.json -- the published alignment requirement",
                    lever_arm_inherited_m=arm_inherited,
                    lever_arm_inherited_note="A13's Gen5 arm. Used by the first run of this "
                                             "script and 15.6x the requirement above. P100",
                    stage_radius_m=0.9, shots=N_SHOTS),
        momentum_sweep=momentum_sweep,
        rows=rows, bands=bands,
        findings=dict(
            wheel_observation=dict(
                outside_bands=True,
                why="Band 5 forbids any comparison against an assumed control authority, and it "
                    "is not widened here. This is recorded as a finding instead, because "
                    "suppressing it would be the opposite failure to P94's.",
                momentum_per_shot_Nms=round(momentum_per_shot, 4),
                a52_declared_wheel_Nms=WHEEL_N_M_S,
                a52_wheel_status="DECLARED ASSUMPTION in A52, not a host property. E5 stands.",
                observation="The per-shot angular momentum exceeds the wheel A52 declared. On "
                            "that assumed wheel the campaign cannot be flown without desaturating "
                            "between shots, which no ConOps in this repository describes.",
                what_it_is_not="This is NOT a finding about any real stage. It is a finding about "
                               "A52's assumed wheel, and it would change entirely on a real one."),
            band4_direction=dict(
                gen6_over_gen5=round(light["offset_per_shot_deg"] / gen5_offset, 4),
                why="Gen6 moves 2.4x less mass 5.3x further on a longer, more slender body. The "
                    "displacement wins: the offset per shot is larger, not smaller.")),
        software=dict(python=platform.python_version(),
                      source_sha256=hashlib.sha256(
                          open(__file__, "rb").read()).hexdigest()))


def main():
    out = run()
    with open(os.path.join(RESULTS, "stage_attitude.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    print("A57: attitude rate and packaging on the stage")
    for r in out["rows"]:
        print(f"  host {r['host_kg']:>6.0f} kg | offset/shot {r['offset_per_shot_deg']:>7.4f} deg"
              f" | campaign {r['offset_campaign_deg']:>8.4f} deg"
              f" | peak rate {r['peak_body_rate_deg_s']:>8.5f} deg/s")
    print()
    for b in out["bands"]:
        v = b.get("value", b.get("per_shot_Nms"))
        print(f"  band {b['band']}  {b['verdict']:<6}  {b['question'][:52]:<52} {v}")


if __name__ == "__main__":
    main()
