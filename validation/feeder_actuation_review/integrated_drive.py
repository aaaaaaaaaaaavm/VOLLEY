"""IDR-01 ambient catalogue screen of an integrated32L ball-screw candidate.

Maximum catalogue efficiency is not a guaranteed minimum. Lower efficiencies,
drag, added shaft inertia and thermal mounting are explicit sensitivity inputs.
"""

from pathlib import Path
import json, math, itertools
import numpy as np
from scipy.linalg import expm

H = Path(__file__).parent
lead = 0.002
ratio = 4.5
motor = dict(
    voltage=24,
    rated_torque=0.0418,
    no_load_rpm=5600,
    slope=20.4,
    kT=0.0414,
    I0=0.089,
    J=3e-6,
)
extra_J = (0.5 * (7850 * math.pi * 0.005**2 * 0.1) * 0.005**2) / ratio**2
J = motor["J"] + 630e-9 + extra_J
rows = []
for mass, T, R, eg, es, drag in itertools.product(
    [2.83, 5.5, 7.5],
    [5, 10, 15, 20],
    [5, 20, 50],
    [0.65, 0.8, 0.92],
    [0.65, 0.8, 0.9],
    [0, 0.005, 0.015],
):
    t = np.linspace(0, T, 801)
    tau = t / T
    v = 0.2 / T * (30 * tau**2 - 60 * tau**3 + 30 * tau**4)
    acc = 0.2 / T**2 * (60 * tau - 180 * tau**2 + 120 * tau**3)
    F = R + mass * acc
    alpha = acc * 2 * math.pi / lead * ratio
    torque = (
        F * lead / (2 * math.pi * ratio * eg * es) + drag / (ratio * eg) + J * alpha
    )
    rpm = v * 60 / lead * ratio
    current = np.abs(torque) / motor["kT"] + motor["I0"]
    available = motor["no_load_rpm"] - motor["slope"] * 1000 * np.abs(torque)
    passed = bool(
        max(abs(torque)) <= motor["rated_torque"]
        and np.all(rpm <= available)
        and max(F) < 354
        and max(rpm) < 8000
        and max(F * v) < 50
    )
    rows.append(
        dict(
            mass_kg=mass,
            time_s=T,
            resistance_N=R,
            gear_efficiency_assumed=eg,
            screw_efficiency_assumed=es,
            output_drag_Nm=drag,
            motion="Quintic rest-to-rest;801 samples",
            peak_speed_m_s=float(max(v)),
            peak_acceleration_m_s2=float(max(abs(acc))),
            peak_motor_rpm=float(max(rpm)),
            peak_motor_torque_Nm=float(max(abs(torque))),
            peak_equivalent_current_A=float(max(current)),
            input_energy_proxy_J=float(np.trapezoid(24 * current, t)),
            peak_force_N=float(max(F)),
            ambient_catalogue_screen_pass=passed,
        )
    )


# Matrix-exponential two-node thermal sensitivity. Parameters reconstructed from
# catalogue thermal resistances/time constants are not a correlated motor model.
def thermal(power, ambient, Rh, shots, T, dwell):
    Rw = 2.3
    Cw = 13 / Rw
    Ch = 880 / 11.6
    A = np.array(
        [[-1 / (Rw * Cw), 1 / (Rw * Cw)], [1 / (Rw * Ch), -(1 / Rw + 1 / Rh) / Ch]]
    )
    B = np.array([1 / Cw, 0.0])
    u = np.zeros(2)
    peak = ambient
    trace = []
    clock = 0

    def arc(dt, P):
        nonlocal u, peak, clock
        for tt in np.linspace(0, dt, 41)[1:]:
            E = expm(A * tt)
            q = E @ u + np.linalg.solve(A, (E - np.eye(2)) @ B) * P
            peak = max(peak, ambient + q[0])
            trace.append([clock + tt, ambient + q[0], ambient + q[1]])
        E = expm(A * dt)
        u = E @ u + np.linalg.solve(A, (E - np.eye(2)) @ B) * P
        clock += dt

    for i in range(shots):
        arc(2 * T, power)  # loaded return is conservatively assumed equal to feed
        arc(dwell, 0)
    return float(peak), trace


worst = max(
    [r for r in rows if r["ambient_catalogue_screen_pass"] and r["time_s"] == 20],
    key=lambda r: r["peak_equivalent_current_A"],
)
thermal_rows = []
for ambient, Rh, shots, dwell in itertools.product(
    [20, 60, 80], [11.6, 50, 100], [4, 12], [30, 120, 600]
):
    power = 24 * worst["peak_equivalent_current_A"]
    peak, trace = thermal(power, ambient, Rh, shots, 20, dwell)
    thermal_rows.append(
        dict(
            ambient_C=ambient,
            housing_to_sink_assumed_K_W=Rh,
            shots=shots,
            feed_and_return_s=40,
            dwell_s=dwell,
            input_power_proxy_all_at_winding_W=power,
            peak_winding_C=peak,
            below_catalogue125C_if_model_holds=peak <= 125,
        )
    )
_, trace = thermal(24 * worst["peak_equivalent_current_A"], 60, 50, 12, 20, 120)
r = dict(
    revision="IDR-01",
    candidate="32L...SB4.5:1,10x2,300mm screw +3242...024BX4;MC5005S CO ground controller",
    reference="https://www.faulhaber.com/fileadmin/Import/Media/EN_32L_SB_FMM.pdf",
    catalogue_domain="22C standard200mm source;300mm is an available length option requiring revised inertia/buckling and supplier confirmation. Vacuum options alter ratings and are not selected.",
    ratio_nominal=ratio,
    travel_screen_mm={
        "selected_screw_length": 300,
        "nut_envelope_length": 35.5,
        "root_and_end_allowances_each": 15,
        "nominal_available": 234.5,
        "required": 200,
    },
    source_force_N=354,
    source_max_input_rpm=8000,
    source_gear_efficiency_max=0.92,
    source_screw_efficiency_max=0.9,
    source_standard_actuator_mass_kg=0.220,
    source_standard_input_inertia_kg_m2=630e-9,
    added100mm_major_cylinder_inertia_at_input_kg_m2=extra_J,
    total_rotating_input_inertia_kg_m2=J,
    source_temperature_C=[-20, 80],
    controller=dict(
        part="MC5005S CO",
        supply_V=[12, 50],
        continuous_A=5,
        peak_A=15,
        mass_kg=0.230,
        source="https://www.faulhaber.com/fileadmin/Import/Media/EN_MC5005S_DFF.pdf",
        notestablished="Equivalent DCcurrent is not a verified phase/PWM limit, thermal mount, wiring design or closed-loop commissioning.",
    ),
    cases=rows,
    case_count=len(rows),
    passes=sum(x["ambient_catalogue_screen_pass"] for x in rows),
    thermal_cases=thermal_rows,
    thermal_failure_count=sum(
        not x["below_catalogue125C_if_model_holds"] for x in thermal_rows
    ),
    thermal_trace=trace,
    thermal_boundary="All modeled electrical input proxy is deposited at winding; actual input, current convention, PWM losses and correlated two-node parameters are unverified. Catalogue thermal constants refer to its test mounting;50/100K/W are assumed sensitivities. Brake,controller,gear heating and radiation are not coupled.125C is winding ceiling;hardware ambient limits are separate.",
    boundary="Ground component feasibility screen, not a selected space actuator or completed installed feeder. No magnetic/thermal vacuum qualification, brake mounting or real load-path verification.",
)
(H / "INTEGRATED_DRIVE.json").write_text(json.dumps(r, indent=2) + "\n")
print(
    len(rows),
    "integrated-drive cases;",
    r["passes"],
    "ambient screens;",
    len(thermal_rows),
    "thermal sensitivities;",
    r["thermal_failure_count"],
    "above winding ceiling",
)
