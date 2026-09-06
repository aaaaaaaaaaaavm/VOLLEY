"""A13 correction: transient host motion from internal mass translation.

The first A13 implementation treated peak internal angular momentum as a residual host
rate after the moving mass stopped. That violates angular-momentum conservation in the
ideal rigid-body model it declared. The host counter-rotates while the mass moves, returns
to zero rate when the mass stops, and retains an attitude offset.
"""
import hashlib
import json
import math
import os
import platform
import sys
import numpy as np

import motor_model as mm

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
M_SAT, M_SLED = 4.0, 9.445


def _loaded_kg():
    """The deployer's LOADED mass, because deployer_inertia() is added to the host's.

    The rotating body is the installed deployer with its twelve satellites aboard; only the
    one being indexed, and the sled, move within it. So this is loaded mass, not dry.

    It was the literal 124.5, which was mass_properties' loaded figure BEFORE A46 itemised
    the enclosure on 2026-08-16 -- 8.00 kg of placeholder became 50.04 kg. Read live so it
    cannot go stale again; 124.5 -> 174.6 raises the deployer inertia by 40 %.
    """
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, 'results', 'mass_properties.json'), encoding='utf-8') as fh:
        return json.load(fh)['loaded_kg']


M_DEPLOYER = _loaded_kg()
SLED_TRAVEL, CASSETTE_PITCH = 1.50, 0.104
# DECLARED ASSUMPTION, no derivation: the lever arm from the host centre of mass to the
# deployer's. Named ASSUMED_ARM since A13 was written and never sourced.
ASSUMED_ARM = 0.166
T_INDEX, T_RETURN, N_SHOTS = 4.0, 6.0, 12
V_EXIT = mm.operating_point()['v_exit']    # never a literal; see mm.operating_point
# DECLARED ASSUMPTION, N.m, and it is the one this script should be challenged on: a host
# reaction-control authority. E5 records that NO host control-authority figure exists in this
# project. The ideal endpoint has zero rate, so it needs no control torque to meet band 5.
# The post-move attitude slew still assumes this authority. P94 remains open.
RCS_TORQUE = 0.1
HOST_MASSES = (200.0, 500.0, 1000.0, 2000.0, 5000.0)


def host_inertia(mass):
    scale = (mass / 500.0) ** (1.0 / 3.0)
    radius, length = scale, 2.0 * scale
    return mass * (3 * radius**2 + length**2) / 12.0


def deployer_inertia():
    length, width = 1.839, 0.530
    return M_DEPLOYER * (length**2 + width**2) / 12.0


def move(mass, distance, duration, inertia, n=20001, arm=None):
    """Internal move, checked analytically and by numerical time integration.

    `arm` defaults to ASSUMED_ARM so A13's own results are unchanged. It is a parameter because
    A57 needed a DIFFERENT arm and the first version of that run silently reused this one --
    A13's arm is from a Gen5 host CoM to the deployer's, and a Gen6 payload traverses a tube
    whose offset from the stage CoM A52 already published a requirement on. P100.
    """
    if arm is None:
        arm = ASSUMED_ARM
    time = np.linspace(0.0, duration, n)
    accel = 4.0 * distance / duration**2
    velocity = np.where(time <= duration / 2, accel * time,
                        accel * (duration - time))
    body_rate = -mass * arm * velocity / inertia
    angle_numeric = float(np.trapezoid(body_rate, time))
    angle_exact = -mass * arm * distance / inertia
    return dict(
        peak_linear_momentum_Ns=mass * 2.0 * distance / duration,
        net_internal_momentum_change_Ns=mass * float(velocity[-1] - velocity[0]),
        peak_body_rate_deg_s=math.degrees(float(np.max(np.abs(body_rate)))),
        residual_body_rate_deg_s=math.degrees(abs(float(body_rate[-1]))),
        attitude_offset_deg=math.degrees(angle_exact),
        numerical_offset_deg=math.degrees(angle_numeric),
        integration_error_deg=math.degrees(angle_numeric - angle_exact),
        post_move_slew_min_s=2.0 * math.sqrt(inertia * abs(angle_exact) / RCS_TORQUE))


def sweep():
    rows = []
    i_deployer = deployer_inertia()
    for mass in HOST_MASSES:
        inertia = host_inertia(mass) + i_deployer
        index = move(M_SAT, CASSETTE_PITCH, T_INDEX, inertia)
        returned = move(M_SLED, SLED_TRAVEL, T_RETURN, inertia)
        rows.append(dict(
            host_kg=mass, combined_inertia_kgm2=inertia,
            index=index, sled_return=returned,
            sequential_peak_rate_deg_s=max(index["peak_body_rate_deg_s"],
                                           returned["peak_body_rate_deg_s"]),
            residual_rate_deg_s=max(index["residual_body_rate_deg_s"],
                                    returned["residual_body_rate_deg_s"]),
            worst_case_attitude_offset_deg=(abs(index["attitude_offset_deg"])
                                            + abs(returned["attitude_offset_deg"]))))
    return rows


def evaluate_bands(rows, shot_impulse):
    """Apply A13's original bands to the reported rigid-body quantities.

    Peak internal momentum answers rows 1 and 2. It is not residual host momentum.
    Row 5 only evaluates rate at the stopped endpoint; a nonzero residual cannot be
    assigned a settling time without an attitude controller. Row 6 sums the internal
    momentum change, which establishes neither attitude restoration nor CoM return.
    """
    if not math.isfinite(shot_impulse) or shot_impulse <= 0:
        raise ValueError("shot impulse must be positive and finite")
    row200 = next(r for r in rows if r["host_kg"] == 200.0)
    row500 = next(r for r in rows if r["host_kg"] == 500.0)
    index_pct = 100 * row500["index"]["peak_linear_momentum_Ns"] / shot_impulse
    return_pct = 100 * row500["sled_return"]["peak_linear_momentum_Ns"] / shot_impulse
    rate500 = row500["sequential_peak_rate_deg_s"]
    rate200 = row200["sequential_peak_rate_deg_s"]
    endpoint_rate = row500["residual_rate_deg_s"]
    stopped = math.isfinite(endpoint_rate) and abs(endpoint_rate) < 0.01
    net_index = abs(N_SHOTS * row500["index"]["net_internal_momentum_change_Ns"])
    index_limit = 0.05 * row500["index"]["peak_linear_momentum_Ns"]

    def below(value, limit):
        return math.isfinite(value) and 0 <= value < limit

    return [
        dict(row=1, result_pct=index_pct, verdict="PASS" if below(index_pct, 10) else "FAIL"),
        dict(row=2, result_pct=return_pct, verdict="PASS" if below(return_pct, 20) else "FAIL"),
        dict(row=3, result_deg_s=rate500, verdict="PASS" if below(rate500, 0.05) else "FAIL"),
        dict(row=4, result_deg_s=rate200, verdict="PASS" if below(rate200, 0.2) else "FAIL"),
        dict(row=5, result_s=0.0 if stopped else None,
             verdict=("PASS IN THE IDEAL RIGID-BODY MODEL" if stopped else
                      "VOID; NONZERO ENDPOINT RATE REQUIRES A CONTROLLER")),
        dict(row=6, result_Ns=net_index,
             verdict=("PASS BY THE CLOSED INTERNAL CYCLE" if below(net_index, index_limit)
                      else "FAIL")),
        dict(row=7, result_pct=None, verdict="VOID; NO RCS PROPELLANT MODEL EXISTS")]


def source_hash():
    """Hash canonical LF bytes, independent of checkout line endings."""
    with open(__file__, "rb") as source:
        return hashlib.sha256(source.read().replace(b"\r\n", b"\n")).hexdigest()


def inertia_description():
    return f"{M_DEPLOYER} kg box at the 1.839 x 0.530 m envelope"


def verdict_summary(bands):
    return "; ".join(f"row {b['row']}: {b['verdict']}" for b in bands) + "; cadence conclusion superseded"


def check_result(result):
    """Check verdicts against their recorded inputs and the declared provenance.

    This is an exact consistency check, with no numerical acceptance tolerance.
    It does not independently validate the host inertia or the motion calculation.
    """
    problems = []
    try:
        expected = evaluate_bands(result["host_sweep"], result["shot_impulse_Ns"])
        if result["bands"] != expected:
            problems.append("band verdicts or values disagree with the recorded inputs")
        if result["verdict"] != verdict_summary(expected):
            problems.append("summary verdict disagrees with the recorded inputs")
        if result["software"]["source_sha256"] != source_hash():
            problems.append("result was not produced by the current analysis source")
        if result["assumptions"]["deployer_inertia"] != inertia_description():
            problems.append("inertia description does not use the current loaded mass")
    except (KeyError, TypeError, ValueError, StopIteration):
        problems.append("result is missing or has invalid band inputs")
    return problems


def main():
    path = os.path.join(RESULTS, "attitude_budget.json")
    if "--check" in sys.argv:
        with open(path, encoding="utf-8") as source:
            problems = check_result(json.load(source))
        for problem in problems:
            print(f"A13: {problem}")
        if not problems:
            print("A13: verdicts agree with recorded inputs; source and loaded mass agree")
        return int(bool(problems))

    rows = sweep()
    shot_impulse = M_SAT * V_EXIT
    campaign_impulse = N_SHOTS * shot_impulse
    bands = evaluate_bands(rows, shot_impulse)
    print("A13 corrected rigid-body momentum budget\n")
    print(f"{'host kg':>8} {'I total':>10} {'index peak':>12} {'return peak':>12} "
          f"{'residual':>11} {'offset worst':>13}")
    for row in rows:
        print(f"{row['host_kg']:8.0f} {row['combined_inertia_kgm2']:10.1f} "
              f"{row['index']['peak_body_rate_deg_s']:12.5f} "
              f"{row['sled_return']['peak_body_rate_deg_s']:12.5f} "
              f"{row['residual_rate_deg_s']:11.5f} "
              f"{row['worst_case_attitude_offset_deg']:13.5f}")
    print(f"\nshot impulse {shot_impulse:.3f} N.s; twelve shots {campaign_impulse:.3f} N.s")
    for band in bands:
        print(f"Row {band['row']}: {band['verdict']}")
    print("Structural ringing and the attitude-restoration schedule remain open.")

    # Hash canonical LF bytes so Git checkout line endings cannot change the provenance record.
    result = dict(
        analysis="A13 corrected",
        supersedes="A13 result run 2026-07-31",
        method="angular-momentum conservation with numerical time integration",
        software=dict(python=platform.python_version(), python_license="PSF License",
                      numpy=np.__version__, numpy_license="BSD-3-Clause",
                      source_sha256=source_hash()),
        solver_settings=dict(time_samples=20001, integration="numpy.trapezoid",
                             analytic_cross_check="closed-form triangular profile"),
        assumptions=dict(
            motion="symmetric triangular profile; each mass starts and ends at rest",
            arm_m=ASSUMED_ARM,
            arm_status="assumed; cassette width is not a measured CoM lever arm",
            sequence="index and return are sequential; peak rates are not added",
            deployer_inertia=inertia_description(),
            rigid_body="no structural modes, damping, flexible coupling, or controller"),
        shot_impulse_Ns=shot_impulse, campaign_impulse_Ns=campaign_impulse,
        host_sweep=rows, bands=bands,
        verdict=verdict_summary(bands))
    os.makedirs(RESULTS, exist_ok=True)
    with open(path, "w") as output:
        json.dump(result, output, indent=2)
        output.write("\n")
    print("\n-> results/attitude_budget.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
