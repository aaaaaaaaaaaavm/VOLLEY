"""Exploratory Gen5 shot with finite-array force and the historical bank model.

The P118 force map sets ideal phase at each x at the old sheet-current limit.
This script couples that position-dependent force to mover motion, copper heat,
capacitor droop and ESR using the same assumed electrical parameters as the old
periodic shot. It is not a winding/inverter implementation or a motor rating.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import motor_model as mm

ROOT = Path(__file__).resolve().parents[1]
FORCE = ROOT / "analysis/results/gen5_finite_force_map.json"
OUT = ROOT / "analysis/results/gen5_finite_coupled_shot.json"
FIG = ROOT / "figures/gen5_finite_coupled_shot.png"
REPORT = ROOT / "validation/P120_gen5_finite_coupled_shot.md"


def run(force_x, force_y, active_length_m: float, dt: float, keep_trace=False):
    moving_mass = mm.M_SAT + mm.M_SLED
    j_copper = 0.9 * mm.K_RATED / (mm.WIND_THICK * mm.FILL)
    copper_volume = active_length_m * mm.DEPTH * mm.WIND_THICK * mm.FILL
    copper_power = mm.RHO_CU * j_copper**2 * copper_volume
    x = v = t = drawn = copper = esr = auxiliary = converter = work = 0.0
    voltage = mm.V0
    peak_current = peak_power = peak_accel = 0.0
    trace = []
    while x < mm.ACCEL_ZONE:
        force = float(np.interp(x, force_x, force_y))
        v_next = v + force / moving_mass * dt
        x_next = x + v_next * dt
        power_mechanical = force * v_next
        power_terminal = power_mechanical / mm.CONV_EFF + copper_power + mm.P_AUX
        disc = voltage**2 - 4 * mm.R_ESR * power_terminal
        if disc <= 0 or voltage <= 40:
            raise RuntimeError(f"assumed bank infeasible at x={x:.4f} m, V={voltage:.2f} V")
        current = (voltage - math.sqrt(disc)) / (2 * mm.R_ESR)
        drawn += voltage * current * dt
        esr += current**2 * mm.R_ESR * dt
        copper += copper_power * dt
        auxiliary += mm.P_AUX * dt
        converter += power_mechanical * (1 / mm.CONV_EFF - 1) * dt
        work += force * (x_next - x)
        voltage -= current * dt / mm.C_BANK
        x, v, t = x_next, v_next, t + dt
        peak_current = max(peak_current, current)
        peak_power = max(peak_power, power_terminal)
        peak_accel = max(peak_accel, force / moving_mass)
        if keep_trace and len(trace) % 20 == 0:
            trace.append([t, x, v, force, voltage, current, power_terminal])
        elif keep_trace:
            # Keep a compact deterministic sample without changing the dynamics.
            trace.append(None)
        if t > 5:
            raise RuntimeError("shot did not leave the acceleration zone within 5 s")
    if keep_trace:
        trace = [row for row in trace if row is not None]
    kinetic = 0.5 * moving_mass * v**2
    return dict(active_copper_length_m=active_length_m, time_step_s=dt,
                duration_s=t, exit_speed_m_s=v, exit_position_m=x,
                peak_acceleration_g=peak_accel / 9.80665,
                voltage_end_V=voltage, peak_bank_current_A=peak_current,
                peak_terminal_power_W=peak_power, gross_capacitor_draw_J=drawn,
                copper_J=copper, bank_esr_J=esr, converter_J=converter,
                auxiliary_J=auxiliary, mechanical_work_J=work,
                mover_kinetic_J=kinetic,
                numerical_work_minus_kinetic_J=work-kinetic,
                energy_ledger_residual_J=drawn-work-converter-copper-esr-auxiliary,
                trace=trace)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    force_raw = FORCE.read_bytes()
    mapped = json.loads(force_raw)
    xs = np.asarray(mapped["positions_m"])
    fs = np.asarray(mapped["forces_N"])
    branches = []
    for name, length in (("full_stator_energized_historical_assumption", 1.3),
                         ("mover_length_energized_unselected_branch", 0.34)):
        coarse = run(xs, fs, length, 1e-4, keep_trace=True)
        fine = run(xs, fs, length, 5e-5)
        fine.pop("trace")
        branches.append(dict(name=name, result=coarse, half_step=fine,
                             speed_time_step_change_m_s=abs(coarse["exit_speed_m_s"]-fine["exit_speed_m_s"]),
                             draw_time_step_change_J=abs(coarse["gross_capacitor_draw_J"]-fine["gross_capacitor_draw_J"])))
    result = dict(status="EXPLORATORY_IDEAL_PHASE_FINITE_FORCE_COUPLED_TO_ASSUMED_BANK",
                  method="P118 finite force interpolated in a forward-time mover/capacitor/ESR model",
                  force_source_sha256=hashlib.sha256(force_raw).hexdigest(),
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  software_versions=dict(python=platform.python_version(), numpy=np.__version__),
                  source_assumptions=dict(capacitance_F=mm.C_BANK, initial_voltage_V=mm.V0,
                                          bank_esr_ohm=mm.R_ESR, converter_efficiency=mm.CONV_EFF,
                                          auxiliary_power_W=mm.P_AUX,
                                          sheet_current_A_per_m=0.9*mm.K_RATED,
                                          moving_mass_kg=mm.M_SAT+mm.M_SLED),
                  caveats=["Phase optimized independently at each position; inverter commutation and voltage limits omitted",
                           "P118 force uses the analytic cuboid field; no independent 3-D full-depth force FEM",
                           "Both copper lengths are assumptions; actual segmented winding and source components are unselected",
                           "No friction, payload contact, host motion, arrest/regeneration or thermal derating"],
                  branches=branches)
    rendered = json.dumps(result, indent=2) + "\n"
    full, short = (b["result"] for b in branches)
    report = "\n".join([
        "# P120 — finite-force shot with assumed bank and copper branches", "",
        "**Exploratory coupled model, not a selected motor rating or flight-power design.**", "",
        "P118's position-dependent ideal-phase force replaces the constant historical",
        "force in a mover/capacitor/ESR time integration. Both branches retain the old",
        "assumed 96 V, 6 F, 12 mΩ source, 95% converter, 200 W auxiliaries and 0.9×140 kA/m",
        "sheet current. One branch energizes the full 1.3 m winding as the historical shot",
        "does; the other uses a hypothetical 0.34 m active copper length. Neither branch",
        "specifies real switching, device ratings, selected cells or winding segmentation.", "",
        "| Assumed energized length | Exit speed | Gross capacitor draw | Copper heat | Peak bank current | Time |", "|:--|--:|--:|--:|--:|--:|",
        *[f"| {b['result']['active_copper_length_m']:.2f} m | {b['result']['exit_speed_m_s']:.3f} m/s | {b['result']['gross_capacitor_draw_J']:.1f} J | {b['result']['copper_J']:.1f} J | {b['result']['peak_bank_current_A']:.1f} A | {1000*b['result']['duration_s']:.1f} ms |" for b in branches],
        "",
        f"The full-winding branch ends at {full['voltage_end_V']:.2f} V and its bank energy",
        f"ledger residual is {full['energy_ledger_residual_J']:.5f} J. Halving the time step",
        f"changes its speed by {branches[0]['speed_time_step_change_m_s']:.4f} m/s and gross",
        f"draw by {branches[0]['draw_time_step_change_J']:.2f} J. The electrical result is",
        "conditional on a bank and converter with no supplier-backed implementation.", "",
        "![Finite-force bank and speed histories](../figures/gen5_finite_coupled_shot.png)", "",
        "The old 16.029 m/s, 2.782 kJ, 47 J regeneration, brake duty and 0.0274 m/s",
        "dispersion must not be reused as outputs of this finite-force run. This model does",
        "not calculate the release-contact state, new brake entry or mission closure.", "",
        "Reproduce with `python analysis/gen5_finite_coupled_shot.py`; run with",
        "`--check` to compare the report and JSON to a fresh calculation.", "",
    ])
    if args.check:
        fresh = OUT.exists() and OUT.read_text() == rendered and REPORT.exists() and REPORT.read_text() == report
        print("P120 current" if fresh else "P120 STALE")
        return 0 if fresh else 1
    OUT.write_text(rendered)
    REPORT.write_text(report)
    trace = np.asarray(full["trace"])
    fig, axes = plt.subplots(3, 1, figsize=(8.8, 6.2), sharex=True, dpi=150)
    axes[0].plot(trace[:, 0]*1000, trace[:, 2], color="#147a8c")
    axes[0].set_ylabel("Speed (m/s)")
    axes[1].plot(trace[:, 0]*1000, trace[:, 3], color="#bf6744")
    axes[1].set_ylabel("Ideal force (N)")
    axes[2].plot(trace[:, 0]*1000, trace[:, 4], color="#355f80", label="Capacitor voltage")
    axes[2].set_ylabel("Voltage (V)")
    axes[2].set_xlabel("Time from shot start (ms)")
    for ax in axes:
        ax.grid(alpha=0.2)
    fig.suptitle("Gen5 finite-force shot under historical bank assumptions", fontweight="bold")
    fig.tight_layout()
    fig.savefig(FIG)
    plt.close(fig)
    print(f"full winding: {full['exit_speed_m_s']:.3f} m/s, {full['gross_capacitor_draw_J']:.1f} J; "
          f"short hypothetical copper: {short['gross_capacitor_draw_J']:.1f} J")


if __name__ == "__main__":
    raise SystemExit(main())
