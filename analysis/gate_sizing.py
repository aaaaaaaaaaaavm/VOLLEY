"""A22: resize the retention gates against the case that actually governs them.

Bands declared in validation/A22_gate_resize.md at bc113e6, before this file existed.

THE DEFECT
----------
sizing.py::retention_gate() sizes against a QUASI-STATIC 25 g ascent load of 5.89 kN. A18 band 9
showed the governing case is random vibration through the track's 109 Hz mode: 11.7 kN at Q=10
and 20.2 kN at Q=30 against an 18.2 kN capacity. The pins are not necessarily undersized; the
load case was.

Sizes against Q = 30, the conservative end. Q is unmeasured (STRUCTURAL_GAP), and A19 found it
is the only assumed input that moves a margin of safety through zero, so sizing at the optimistic
end would be the same error in a new place.

Run:  python3 analysis/gate_sizing.py
"""
import json
import math
import os

import phase1_closeout as pc
import sizing

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

G = 9.80665
TAU_ULT = 537e6 * 0.6           # A-286 shear ~0.6 x tensile. Class assumption, not a datasheet.
RHO_A286 = 8030.0               # kg/m^3
DESIGN_FACTOR = 1.4             # same factor sizing.py already applies
Q_DESIGN = 30.0
Q_RANGE = (10.0, 15.0, 20.0, 30.0)

# Allowed design space, bounded in the run sheet.
PIN_DIAS = (0.006, 0.007, 0.008, 0.009, 0.010)
PIN_COUNTS = (2, 3, 4)
RESTRAINTS = (1, 2)             # gates per cassette; 2 splits the stack mass
MOS_TARGET = 0.20
MASS_BUDGET_KG = 0.40           # per cassette, band 3

STACK_KG = 24.0                 # six 3U per cassette
PIN_LENGTH = 0.020              # m, through the gate frame -- for the mass delta only


def miles_load_N(stack_kg, Q, f_n=None):
    """3-sigma random-vibration load. Same relation phase1_closeout.e10 uses."""
    if f_n is None:
        f_n = sizing.track_first_mode()['fixed_fixed_Hz']
    g_rms = math.sqrt(math.pi / 2 * f_n * Q * pc.GEVS_ASD)
    return stack_kg * 3 * g_rms * G


def capacity_N(n_pins, d):
    return n_pins * (math.pi * (d / 2) ** 2) * TAU_ULT


def pin_mass_kg(n_pins, d, n_gates):
    return n_gates * n_pins * math.pi * (d / 2) ** 2 * PIN_LENGTH * RHO_A286


def bearing_capacity_N(n_pins, d, t_frame=0.004, sigma_bearing=1.5 * 537e6):
    """Bearing on the gate frame boss. Band 6: is pin shear really what governs?"""
    return n_pins * d * t_frame * sigma_bearing


def main():
    f_n = sizing.track_first_mode()['fixed_fixed_Hz']

    # --- band 1: reproduce A18 band 9 --------------------------------------
    a18_rows, _cap = pc.e10()
    a18 = {r['Q']: r['load_N'] for r in a18_rows}
    repro = {Q: miles_load_N(STACK_KG, Q, f_n) for Q in (10.0, 20.0, 30.0)}
    band1_err = {Q: abs(repro[Q] - a18[Q]) / a18[Q] for Q in repro if Q in a18}
    band1_pass = all(e <= 0.02 for e in band1_err.values())

    # --- the design space ---------------------------------------------------
    baseline_cap = capacity_N(2, 0.006)
    candidates = []
    for n_gates in RESTRAINTS:
        stack_per_gate = STACK_KG / n_gates
        load30 = miles_load_N(stack_per_gate, Q_DESIGN, f_n)
        for n in PIN_COUNTS:
            for d in PIN_DIAS:
                cap = capacity_N(n, d)
                mos30 = cap / (DESIGN_FACTOR * load30) - 1.0
                mos_all = {Q: cap / (DESIGN_FACTOR * miles_load_N(stack_per_gate, Q, f_n)) - 1.0
                           for Q in Q_RANGE}
                # band 4: the original quasi-static case must not regress
                f_static = stack_per_gate * 25.0 * G
                mos_static = cap / (DESIGN_FACTOR * f_static) - 1.0
                dm = pin_mass_kg(n, d, n_gates) - pin_mass_kg(2, 0.006, 1)
                candidates.append(dict(
                    n_gates=n_gates, n_pins=n, pin_dia_mm=d * 1e3,
                    stack_per_gate_kg=stack_per_gate,
                    load_Q30_kN=load30 / 1e3, capacity_kN=cap / 1e3,
                    mos_Q30=mos30, mos_by_Q=mos_all, mos_static=mos_static,
                    added_mass_kg=dm,
                    bearing_kN=bearing_capacity_N(n, d) / 1e3,
                    shear_governs=cap <= bearing_capacity_N(n, d),
                    passes=(mos30 >= MOS_TARGET and min(mos_all.values()) >= 0.0
                            and mos_static >= 1.2 and dm <= MASS_BUDGET_KG)))

    passing = [c for c in candidates if c['passes']]
    # Minimum change: fewest gates, then fewest pins, then smallest diameter.
    chosen = min(passing, key=lambda c: (c['n_gates'], c['n_pins'], c['pin_dia_mm'])) \
        if passing else None

    bands = {
        '1_reproduces_a18': dict(errors_pct={k: v * 100 for k, v in band1_err.items()},
                                 band='within 2 %', passed=band1_pass),
        '2_design_exists': dict(n_passing=len(passing), band='at least one',
                                passed=bool(passing)),
        '3_added_mass': dict(value_kg=chosen['added_mass_kg'] if chosen else None,
                             band=f'<= {MASS_BUDGET_KG} kg per cassette',
                             passed=bool(chosen and chosen['added_mass_kg'] <= MASS_BUDGET_KG)),
        '4_static_not_regressed': dict(value=chosen['mos_static'] if chosen else None,
                                       band='MoS >= 1.2',
                                       passed=bool(chosen and chosen['mos_static'] >= 1.2)),
        '5_positive_across_Q': dict(
            value=min(chosen['mos_by_Q'].values()) if chosen else None,
            band='MoS >= 0 for Q = 10..30',
            passed=bool(chosen and min(chosen['mos_by_Q'].values()) >= 0.0)),
        '6_shear_governs': dict(
            shear_kN=chosen['capacity_kN'] if chosen else None,
            bearing_kN=chosen['bearing_kN'] if chosen else None,
            governs='pin shear' if (chosen and chosen['shear_governs']) else 'bearing',
            band='REPORT', verdict='REPORT'),
    }

    print(f"A22 gate resize. Track mode {f_n:.0f} Hz, GEVS {pc.GEVS_ASD} g^2/Hz, "
          f"design factor {DESIGN_FACTOR}, sizing at Q = {Q_DESIGN:.0f}\n")
    print("  band 1, against A18 band 9:")
    for Q in sorted(repro):
        print(f"    Q={Q:4.0f}  this {repro[Q]/1e3:6.2f} kN   A18 {a18[Q]/1e3:6.2f} kN   "
              f"err {band1_err[Q]*100:.3f} %")
    print(f"\n  baseline 2 x D6 capacity {baseline_cap/1e3:.1f} kN, "
          f"load at Q=30 {miles_load_N(STACK_KG, 30.0, f_n)/1e3:.1f} kN, "
          f"MoS {baseline_cap/(DESIGN_FACTOR*miles_load_N(STACK_KG,30.0,f_n))-1:+.2f}")

    print(f"\n  {len(passing)} of {len(candidates)} candidates pass all constraints")
    if chosen:
        c = chosen
        print(f"\n  MINIMUM CHANGE: {c['n_gates']} gate(s) per cassette, "
              f"{c['n_pins']} x D{c['pin_dia_mm']:.0f} pins")
        print(f"    stack per gate {c['stack_per_gate_kg']:.1f} kg, "
              f"load at Q=30 {c['load_Q30_kN']:.2f} kN, capacity {c['capacity_kN']:.1f} kN")
        print(f"    MoS at Q=30 {c['mos_Q30']:+.2f}, across Q=10..30 "
              f"{min(c['mos_by_Q'].values()):+.2f} to {max(c['mos_by_Q'].values()):+.2f}")
        print(f"    quasi-static MoS {c['mos_static']:+.2f}, added mass "
              f"{c['added_mass_kg']*1e3:+.0f} g, governs: "
              f"{'pin shear' if c['shear_governs'] else 'BEARING'}")

    print("\nbands:")
    for k, v in bands.items():
        mark = v.get('passed')
        print(f"  {k:26} {'PASS' if mark else ('REPORT' if mark is None else 'FAIL')}")

    out = dict(analysis='A22', bands_declared_commit='bc113e6',
               sized_at_Q=Q_DESIGN, design_factor=DESIGN_FACTOR, track_mode_Hz=f_n,
               baseline=dict(n_pins=2, pin_dia_mm=6.0, capacity_kN=baseline_cap / 1e3),
               chosen=chosen, n_passing=len(passing), candidates=candidates, bands=bands)
    path = os.path.join(RESULTS, 'gate_sizing.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, default=float)
        f.write('\n')
    print(f"\nwrote {path}")


if __name__ == '__main__':
    main()
