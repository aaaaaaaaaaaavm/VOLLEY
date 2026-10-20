"""Captured-evidence and independent mechanical identities; standard Python."""

from pathlib import Path
import json, hashlib, math

H = Path(__file__).resolve().parent


def load(n):
    return json.loads((H / n).read_text())


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


cad = load("cad/NATIVE_CAD.json")
sweep = load("CONTINUOUS_SWEEPS.json")
step = load("cad/INDEPENDENT_STEP.json")
assert (
    cad["revision"] == "FM-02" and len(cad["poses"]) == 28 and len(cad["motion"]) == 78
)
assert len(sweep["cases"]) == 26 and sweep["total_penetrations"] == 0
for name, digest in sweep["source_sha256"].items():
    assert sha(H / name) == digest, name
for case in cad["poses"]:
    assert not case["invalid_parts"] and not case["penetrations"] and case["step_valid"]
    assert (
        case["step_solids"] == case["component_solids"]
        and abs(case["step_volume_error_mm3"]) < 0.01
    )
    for name, digest in case["files"].items():
        assert sha(H / "cad" / name) == digest, name
assert all(not x["penetrations"] for x in cad["motion"])
assert len(step["cases"]) == 28 and all(x["valid"] for x in step["cases"])
physical = load("PHYSICAL_INTERLOCKS.json")
capture = load("figures/FreeCAD_FM02_transfer.provenance.json")
assert sha(H / capture["source"]) == capture["source_sha256"]
assert sha(H / capture["image"]) == capture["image_sha256"]
drawing = load("drawings/DRAWING_RECORD.json")
assert sha(H / "cad/FM02_3U_transfer.FCStd") == drawing["source_sha256"]
assert (
    physical["verified_rigid_obstructions"] == 22
    and physical["retained_counterexamples"] == 2
)
assert all(x.get("obstruction_mm3", 1) > 0 for x in physical["cases"])
control = load("CONTROLLER_REVIEW.json")
assert (
    control["total_cases"] == 796 and len(control["common_cause_counterexamples"]) == 26
)
drive = load("INTEGRATED_DRIVE.json")
convergence = load("CONVERGENCE.json")
assert len(convergence["cases"]) == 972 and convergence["all_gate_decisions_agree"]
assert convergence["max_801_torque_relative_error"] < 1e-4
assert convergence["max_801_energy_relative_error"] < 1e-4
assert drive["case_count"] == 972 and drive["passes"] == 729
for c in drive["cases"]:
    # Exact quintic peak speed is attained at half-time; acceleration maximum
    # is5.7735*s/T². Grid peaks are checked against the closed-form upper value.
    speed = 1.875 * 0.2 / c["time_s"]
    assert abs(c["peak_speed_m_s"] - speed) < 1e-10
    assert abs(c["peak_motor_rpm"] - speed / 0.002 * 60 * 4.5) < 1e-7
    a = 10 / math.sqrt(3) * 0.2 / c["time_s"] ** 2
    assert 0 <= a - c["peak_acceleration_m_s2"] < 1e-5
    assert (
        abs(
            c["peak_force_N"]
            - (c["resistance_N"] + c["mass_kg"] * c["peak_acceleration_m_s2"])
        )
        < 1e-9
    )
    assert c["input_energy_proxy_J"] >= c["resistance_N"] * 0.2
    assert c["ambient_catalogue_screen_pass"] == (c["time_s"] >= 10)
assert (
    drive["thermal_failure_count"]
    == sum(not x["below_catalogue125C_if_model_holds"] for x in drive["thermal_cases"])
    > 0
)
brake = load("BRAKE_REVIEW.json")
assert len(brake["cases"]) == 576
for c in brake["cases"]:
    k = 2 * math.pi / 0.002
    m = c["moving_kg"] + 4.6e-6 * k * k
    assert abs(m - c["equivalent_kg"]) < 1e-9
    forward = c["persistent_drive_torque_Nm"] * k
    braking = 0.12 * c["assumed_dynamic_torque_factor"] * k
    if braking <= forward:
        assert c["total_runout_mm"] is None
    else:
        v = c["initial_m_s"] + forward / m * c["total_delay_s"]
        coast = (
            c["initial_m_s"] * c["total_delay_s"]
            + 0.5 * forward / m * c["total_delay_s"] ** 2
        )
        stop = 0.5 * m * v * v / (braking - forward)
        assert abs(c["total_runout_mm"] - 1000 * (coast + stop)) < 1e-8
        assert abs(c["brake_work_J"] - braking * stop) < 1e-9
assert brake["no_stop_cases"] == 96 and brake["over_24mm"] == 72
fit = load("FIT_BUDGET.json")
assert len(fit["cases"]) == 324 and fit["nonpositive"] == 115
for c in fit["cases"]:
    loss = (
        c["manufacturing_stack_assumed_mm"]
        + c["alignment_loss_mm"]
        + c["thermal_loss_mm"]
        + c["unpredicted_deflection_band_mm"]
    )
    assert abs(c["residual_mm"] - (c["nominal_gap_mm"] - loss)) < 1e-10
sched = load("SCHEDULE.json")
assert len(sched["cases"]) == 32
for n, h in sched["input_sha256"].items():
    assert sha(H / "inputs" / n) == h, n
assert sum(not x["conditional_fit"] for x in sched["cases"]) == 11
assert all(
    x["conditional_fit"] for x in sched["cases"] if x["policy"] == "faster_auxiliaries"
)
for c in sched["cases"]:
    assert abs(c["margin_s"] - c["available_s"] + c["required_assumed_s"]) < 1e-9
    assert c["zero_force_coast_s"][1] <= c["release_s"] - 10
mass = load("METROLOGY.json")
for c in mass["configurations"]:
    assert (
        abs(
            sum(x["mass_proxy_kg"] for x in c["ledger"])
            - c["total_with_payload_proxy_kg"]
        )
        < 1e-9
    )
    M = c["inertia_with_payload_kg_m2"]
    assert all(M[i][i] > 0 for i in range(3))
    assert all(abs(M[i][j] - M[j][i]) < 1e-10 for i in range(3) for j in range(3))
if (H / "MANIFEST.json").exists():
    for name, digest in load("MANIFEST.json")["files"].items():
        assert sha(H / name) == digest, name
print(
    "PASS FM-02:28 native/STEP poses,26 continuous rigid phases,22 obstruction checks; captured drive,thermal,brake,fit and scheduling identities checked. Failed criteria and unimplemented hardware interfaces remain explicit."
)
