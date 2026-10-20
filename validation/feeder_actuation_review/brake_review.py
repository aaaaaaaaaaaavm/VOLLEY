"""Source-backed candidate brake with explicitly unvalidated transient bands.

The source's armature time is NOT treated as a complete application stopping
time. Dynamic torque is varied as a hypothesis; no manufacturer dynamic torque
rating, flight suitability, or stop qualification is inferred from static torque.
"""

from pathlib import Path
import math, json, itertools

H = Path(__file__).parent
lead = 0.002
k = 2 * math.pi / lead
rows = []
# J includes3242rotor, BXW01rotor and an explicit shaft/coupling allowance.
J = 3e-6 + 0.6e-6 + 1e-6
for m, v, delay, factor, drive in itertools.product(
    [2.83, 5.5, 7.5],
    [0.02, 0.0266666666667, 0.04, 0.08],
    [0.008, 0.02, 0.05, 0.1],
    [0.5, 0.75, 1],
    [0, 0.02, 0.05, 0.1],
):
    equivalent = m + J * k * k
    forward = drive * k
    accel = forward / equivalent
    vd = v + accel * delay
    coast = v * delay + 0.5 * accel * delay**2
    brake = 0.12 * factor * k
    net = brake - forward
    if net > 0:
        stop = equivalent * vd * vd / (2 * net)
        tstop = equivalent * vd / net
        work = brake * stop
        runout = coast + stop
    else:
        stop = tstop = work = runout = None
    rows.append(
        dict(
            moving_kg=m,
            initial_m_s=v,
            total_delay_s=delay,
            assumed_dynamic_torque_factor=factor,
            persistent_drive_torque_Nm=drive,
            equivalent_kg=equivalent,
            velocity_at_engagement_m_s=vd,
            coast_mm=coast * 1000,
            stopping_distance_mm=None if stop is None else stop * 1000,
            total_runout_mm=None if runout is None else runout * 1000,
            stop_time_after_engagement_s=tstop,
            brake_work_J=work,
            inside_24mm_if_model_holds=runout is not None and runout <= 0.024,
        )
    )
nom = [
    r
    for r in rows
    if r["persistent_drive_torque_Nm"] == 0 and r["initial_m_s"] <= 0.026666666667
]
review = dict(
    revision="BRK-01",
    brake_candidate="BXW-01-10L,24V option",
    static_torque_Nm=0.12,
    source_rotor_inertia_kg_m2=0.6e-6,
    source_mass_kg=0.2,
    source_coil_W=5,
    source_max_rpm=5000,
    source_allowable_braking_power_W=2.5,
    source_total_work_J=1.5e6,
    source_armature_deceleration_time_s=0.008,
    source_temperature_C=[-10, 40],
    source="https://www.mikipulley.co.jp/en/electromagnetic-clutches-brakes/offbrakes/braking/bxw-l",
    rejected="BXR-020-10LE is holding-only per its instruction manual; not a dynamic stop selection.",
    inertia_assumptions_kg_m2={
        "motor": 3e-6,
        "brake": 0.6e-6,
        "shaft_coupling_allowance": 1e-6,
    },
    case_count=len(rows),
    no_stop_cases=sum(x["total_runout_mm"] is None for x in rows),
    over_24mm=sum(
        x["total_runout_mm"] is not None and x["total_runout_mm"] > 24 for x in rows
    ),
    slow_zero_drive_max_runout_mm=max(x["total_runout_mm"] for x in nom),
    cases=rows,
    boundary="Direct-drive frictionless transmission is assumed for energy mapping; no additional friction credit. Assumed torque rise/delay/torque factors are not measured or supplier guarantees. Brake is not integrated into CAD. Persistent powered drive, broken coupling, nut failure, loss of guide support and actual latch impact need separate containment.",
)
(H / "BRAKE_REVIEW.json").write_text(json.dumps(review, indent=2) + "\n")
print(
    len(rows),
    "stop sensitivities;",
    review["no_stop_cases"],
    "no-stop;",
    review["over_24mm"],
    "over24mm; slow/no-drive max",
    review["slow_zero_drive_max_runout_mm"],
)
