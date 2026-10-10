"""P125: conditional quasi-steady voltage/current screen of the P118 force map.

This is deliberately a *screen*, not a selected winding or drive simulation.
The R, L and reference current come from the superseded periodic winding model.
The finite-force map determines a local force constant. A balanced three-phase
q-axis power identity gives E_peak=F*v/(1.5*I_peak); winding voltage is bounded
by sqrt((E+RI)^2+(omega*L*I)^2) <= Vdc/sqrt(3). No phase transient, contact,
segmentation, supplier rating, or temperature dependence is modeled.
"""
from __future__ import annotations

import argparse
import bisect
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORCE = ROOT / "analysis/results/gen5_finite_force_map.json"
DRIVE = ROOT / "analysis/results/drive_electrical.json"
RESULT = ROOT / "analysis/results/gen5_voltage_limited_screen.json"
REPORT = ROOT / "validation/P125_gen5_voltage_limited_screen.md"
FIGURE = ROOT / "figures/gen5_voltage_limited_screen.svg"
MASS = 13.445
STROKE = 1.30
V0 = 96.0
CAP_F = 6.0
ESR = .012
EFF = .95
AUX_W = 200.0
PITCH = .048


def force_at(x, xs, fs):
    j = bisect.bisect_left(xs, x)
    if j <= 0:
        return fs[0]
    if j >= len(xs):
        return fs[-1]
    a = (x-xs[j-1])/(xs[j]-xs[j-1])
    return fs[j-1] + a*(fs[j]-fs[j-1])


def simulate(xs, fs, i_ref, resistance, inductance, current_limit,
             source_voltage=V0, step=.0001, trace=False):
    x = v = t = w_mech = w_cu = w_esr = w_aux = w_conv = 0.0
    vc = source_voltage
    records = []
    voltage_limited = 0
    peak_i = peak_bank_i = peak_accel = 0.0
    while x < STROKE:
        f_ref = max(0.0, force_at(x, xs, fs))
        kt = f_ref / i_ref
        # Force and back-EMF use one power-consistent three-phase convention.
        ke = kt / 1.5
        omega = 2 * math.pi * v / PITCH
        vmax = vc / math.sqrt(3)
        lo, hi = 0.0, current_limit
        for _ in range(26):
            mid = (lo + hi) / 2
            required = math.hypot(ke * v + resistance * mid,
                                  omega * inductance * mid)
            if required <= vmax:
                lo = mid
            else:
                hi = mid
        current = lo
        if current < current_limit - .001:
            voltage_limited += 1
        force = kt * current
        vn = v + force / MASS * step
        xn = x + vn * step
        copper_power = 1.5 * resistance * current**2
        mechanical_power = force * vn
        dc_terminal = (mechanical_power + copper_power) / EFF + AUX_W
        discriminant = vc**2 - 4 * ESR * dc_terminal
        if discriminant <= 0:
            return {"status": "SOURCE_ESR_POWER_LIMIT", "position_m": x}
        ibank = 2 * dc_terminal / (vc + math.sqrt(discriminant))
        w_mech += force * (xn - x)
        w_cu += copper_power * step
        w_esr += ibank**2 * ESR * step
        w_aux += AUX_W * step
        w_conv += (mechanical_power + copper_power) * (1 / EFF - 1) * step
        vc -= ibank * step / CAP_F
        if trace and len(records) % 20 == 0:
            records.append([t, x, v, force, current, vc,
                            math.hypot(ke * v + resistance * current,
                                       omega * inductance * current), vmax])
        elif trace:
            records.append(None)
        x, v, t = xn, vn, t + step
        peak_i = max(peak_i, current)
        peak_bank_i = max(peak_bank_i, ibank)
        peak_accel = max(peak_accel, force / MASS)
        if t > 5:
            return {"status": "STALLED", "position_m": x}
    drawn = .5 * CAP_F * (source_voltage**2 - vc**2)
    return dict(status="COMPLETED_CONDITIONAL_SCREEN", speed_m_s=v,
                duration_s=t, end_voltage_V=vc, cap_draw_J=drawn,
                mechanical_J=w_mech, copper_J=w_cu, bank_esr_J=w_esr,
                auxiliary_J=w_aux, converter_J=w_conv,
                ledger_residual_J=drawn-w_mech-w_cu-w_esr-w_aux-w_conv,
                peak_phase_current_A=peak_i, peak_bank_current_A=peak_bank_i,
                peak_acceleration_g=peak_accel / 9.80665,
                voltage_limited_fraction=voltage_limited / round(t / step),
                trace=[p for p in records if p is not None] if trace else [])


def make_svg(cases):
    vals = [(k, v["speed_m_s"]) for k, v in cases.items()]
    width, height = 800, 340
    bars = []
    for i, (name, speed) in enumerate(vals):
        y = 58 + i * 54
        w = 500 * speed / 13
        color = "#13859d" if name == "reference_unselected" else "#b86b4a"
        bars.append(f'<text x="22" y="{y+18}" font-size="14">{name.replace("_", " ")}</text>'
                    f'<rect x="245" y="{y}" width="{w:.1f}" height="24" fill="{color}"/>'
                    f'<text x="{255+w:.1f}" y="{y+18}" font-size="14">{speed:.3f} m/s</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">'
            '<rect width="100%" height="100%" fill="#f6f9fb"/>'
            '<text x="22" y="32" font-size="20" font-weight="bold">P125 · conditional voltage-limited screen</text>'
            + "".join(bars) +
            '<text x="22" y="325" font-size="12">Unselected R/L/current and ideal phase; no rated Gen5 speed</text></svg>\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    raw_force, raw_drive = FORCE.read_bytes(), DRIVE.read_bytes()
    fm, drive = json.loads(raw_force), json.loads(raw_drive)
    xs, fs = fm["positions_m"], fm["forces_N"]
    i_ref = drive["phase_current_peak_A"]
    r, l = drive["phase_resistance_ohm"], drive["phase_inductance_H"]
    variants = {
        "reference_unselected": (r, l, i_ref, V0),
        "twice_resistance": (2*r, l, i_ref, V0),
        "twice_inductance": (r, 2*l, i_ref, V0),
        "half_current_limit": (r, l, i_ref/2, V0),
        "half_source_voltage": (r, l, i_ref, V0/2),
    }
    cases = {name: simulate(xs, fs, i_ref, *p) for name, p in variants.items()}
    if any(v["status"] != "COMPLETED_CONDITIONAL_SCREEN" for v in cases.values()):
        raise RuntimeError("at least one surrogate case did not complete")
    refinements = {dt: simulate(xs, fs, i_ref, r, l, i_ref, V0, dt)["speed_m_s"]
                   for dt in (.0002, .00005)}
    data = dict(evidence_class="CONDITIONAL_QUASI_STEADY_SCREEN_NOT_SELECTED_DRIVE_OR_RATED_SPEED",
                sources_sha256={"force_map": hashlib.sha256(raw_force).hexdigest(),
                                "historical_drive": hashlib.sha256(raw_drive).hexdigest(),
                                "source": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
                assumptions=dict(phase_peak_current_A=i_ref, phase_resistance_ohm=r,
                                 phase_inductance_H=l, pitch_m=PITCH, source_initial_V=V0,
                                 capacitance_F=CAP_F, bank_esr_ohm=ESR, converter_efficiency=EFF,
                                 auxiliary_W=AUX_W, mass_kg=MASS,
                                 phase_voltage_limit="Vdc/sqrt(3), ideal space-vector modulation",
                                 source_of_R_L_I="historical periodic winding model, not selected hardware",
                                 omitted=["transient switched currents and commutation error",
                                          "thermal rise and derating", "iron and saturation",
                                          "feed/contact/recoil/brake", "supplier cell and switch ratings"]),
                variants={name: dict(R_ohm=p[0], L_H=p[1], I_limit_A=p[2], source_initial_V=p[3])
                          for name,p in variants.items()},
                cases=cases, time_step_refinement=refinements,
                speed_step_change_m_s=max(abs(cases["reference_unselected"]["speed_m_s"]-x)
                                          for x in refinements.values()))
    svg = make_svg(cases)
    rows = [f"| {name.replace('_',' ')} | {v['speed_m_s']:.3f} | {v['cap_draw_J']:.0f} | {100*v['voltage_limited_fraction']:.1f}% |"
            for name,v in cases.items()]
    report = "\n".join([
        "# P125 — voltage and current feasibility screen", "",
        "**Conditional numerical screen, not a selected motor, rated speed or hardware validation.**", "",
        "P118's position force map is scaled by phase current. A balanced three-phase",
        "power identity gives `E_peak = Fv/(1.5 I_peak)`. At each time step the model",
        "caps the current where `sqrt((E+RI)^2+(ωLI)^2)` reaches `Vdc/√3`, and",
        "integrates capacitor droop and ESR. The resistance, inductance and peak current",
        "come from the historical periodic-winding calculation; they are **not selected parts**.",
        "Ideal space-vector modulation and instantaneous q-axis current are assumed.", "",
        "| Surrogate case | Exit speed (m/s) | Cap draw (J) | Steps voltage limited |",
        "|:--|--:|--:|--:|", *rows, "",
        f"Reference step refinement (0.2–0.05 ms) changes exit speed by at most {data['speed_step_change_m_s']:.4f} m/s.",
        f"Reference energy-ledger residual is {cases['reference_unselected']['ledger_residual_J']:.4f} J.",
        "This step check does not cover force-map interpolation, winding tolerance or source uncertainty.", "",
        "![P125 conditional voltage screen](../figures/gen5_voltage_limited_screen.svg)", "",
        "The decisive motor gate remains open: select and document a winding, switching",
        "stage and pulse source, then run switched-current and thermal cases against",
        "their data-sheet limits. Voltage-limited speed here is an engineering sensitivity",
        "to *assumed* components. No release speed or command precision is established.", "",
        "Reproduce with `python3 analysis/gen5_voltage_limited_screen.py`; `--check`",
        "compares the committed JSON, report and SVG byte for byte.", "",
    ])
    rendered = json.dumps(data, indent=2) + "\n"
    if args.check:
        ok = all((p.exists() and p.read_text() == s) for p,s in
                 ((RESULT,rendered),(REPORT,report),(FIGURE,svg)))
        print("P125 current" if ok else "P125 STALE")
        return 0 if ok else 1
    RESULT.write_text(rendered)
    REPORT.write_text(report)
    FIGURE.write_text(svg)
    print({k: round(v["speed_m_s"],3) for k,v in cases.items()})


if __name__ == "__main__":
    raise SystemExit(main())
