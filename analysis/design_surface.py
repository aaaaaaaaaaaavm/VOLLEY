"""
VOLLEY | The velocity, acceleration and stroke surface.

WHY THIS EXISTS
---------------
Asked directly: make Gen6 best on velocity, on acceleration and on power. Best at everything is
not available. A point that DOMINATES the current one on several axes may be, and the record
contains a lever nobody has pulled: A37 swept stage length at a fixed 25 g and let velocity
rise, and never asked the inverse. A spent upper stage is 8 m long, so stroke is the one
variable this architecture can spend freely.

TWO THINGS THAT MAKE IT NON-OBVIOUS
-----------------------------------
Peak acceleration is p0*A/m and contains no L. Lengthening the tube does not soften the shot at
all; it lets the expansion continue after the peak has happened. To reduce g you must drop the
charge pressure, and then you need stroke to buy the velocity back.

Work from a fixed charge RISES with stroke, because the constant-pressure ceiling p0*A*L grows
linearly. More stroke means more work out of the same gas -- an efficiency term, not only a
performance one.

Bands declared in validation/A49_design_surface.md at HEAD, BEFORE this file existed.

Provenance: model output. Ideal gas, closed adiabatic expansion, Coulomb friction constant over
the stroke, tube as a plain cylinder at one wall thickness, no bending, no alignment tolerance
and no dynamic seal behaviour. Every omission flatters a long tube.
"""
import json
import math
import os

import precharged as pc

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

V_CHAMBER = 2.0e-3
RHO_AL = 2700.0
WALL_M = pc.BORE and 1.0e-3
FRICTION_N = 83.40371375447981        # A41 band 8's allowance, carried unchanged
PV_OVER_W = pc.PV_OVER_W
RHO_STORE = pc.RHO_STORE
N = pc.N_MANIFEST
ADDED_BASE_KG = 11.452976             # A37
TARGET_KG = 2.0

STROKES = (1.3, 2.18, 3.0, 4.0, 5.0, 6.0, 8.0)
PRESSURES_BAR = (10, 15, 18, 20, 25, 30, 40, 50, 60)
GEN6 = dict(L=2.18, p0_bar=50.0)


def work(p0, L, v0=V_CHAMBER):
    r = v0 / (v0 + pc.AREA * L)
    return p0 * v0 / (pc.GAMMA - 1.0) * (1.0 - r ** (pc.GAMMA - 1.0))


def ceiling(p0, L):
    return p0 * pc.AREA * L


def point(p0, L):
    """One (charge pressure, stroke) point, with everything that scales with either."""
    w = work(p0, L)
    w_fric = FRICTION_N * L
    w_net = w - w_fric
    v = math.sqrt(2.0 * max(w_net, 0.0) / pc.M_PAY)
    a_peak = p0 * pc.AREA / pc.M_PAY / 9.81
    gas = p0 * V_CHAMBER / (pc.R_GAS * pc.T0)
    tube = math.pi * ((pc.BORE / 2 + WALL_M * 1e3 / 1e3 * 1e3 / 1e3) ** 2) * 0  # placeholder
    r_in = pc.BORE / 2.0
    r_out = r_in + WALL_M
    tube = math.pi * (r_out ** 2 - r_in ** 2) * L * RHO_AL
    return dict(p0_bar=p0 / 1e5, L=L, work_J=w, friction_J=w_fric, work_net_J=w_net,
                v_exit=v, a_peak_g=a_peak, gas_kg=gas, tube_kg=tube,
                ceiling_J=ceiling(p0, L), ceiling_frac=w / ceiling(p0, L),
                friction_frac=w_fric / w)


def p_for_v(target_v, L, lo=1e5, hi=300e5):
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if point(mid, L)['v_exit'] < target_v:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def dominates(a, b):
    """a beats b on velocity, peak g and gas -- all three, none worse."""
    return (a['v_exit'] >= b['v_exit'] and a['a_peak_g'] <= b['a_peak_g']
            and a['gas_kg'] <= b['gas_kg']
            and (a['v_exit'] > b['v_exit'] or a['a_peak_g'] < b['a_peak_g']
                 or a['gas_kg'] < b['gas_kg']))


def main():
    base = point(GEN6['p0_bar'] * 1e5, GEN6['L'])
    print(f"Gen6 today: {base['v_exit']:.3f} m/s, {base['a_peak_g']:.2f} g peak, "
          f"{base['gas_kg']*1e3:.1f} g gas, {base['work_J']:.1f} J\n")

    # band 2, 3, 4: what stroke alone does at fixed pressure
    print(f"at a fixed 50 bar charge:")
    print(f"{'L m':>6s} {'work J':>9s} {'v m/s':>7s} {'a_pk g':>8s} {'gas g':>7s} "
          f"{'ceil %':>7s} {'fric %':>7s} {'tube kg':>8s}")
    fixed_p = []
    for L in STROKES:
        q = point(50e5, L)
        fixed_p.append(q)
        print(f"{L:6.2f} {q['work_J']:9.1f} {q['v_exit']:7.2f} {q['a_peak_g']:8.2f} "
              f"{q['gas_kg']*1e3:7.1f} {q['ceiling_frac']*100:7.1f} "
              f"{q['friction_frac']*100:7.2f} {q['tube_kg']:8.3f}")

    # the inverse A37 never asked: hold velocity, let stroke buy the g down
    print(f"\nholding {base['v_exit']:.3f} m/s and spending stroke on gentleness:")
    print(f"{'L m':>6s} {'p0 bar':>8s} {'a_pk g':>8s} {'gas g':>7s} {'vs Gen6 gas':>12s} "
          f"{'tube kg':>8s}")
    held = []
    for L in STROKES:
        p0 = p_for_v(base['v_exit'], L)
        q = point(p0, L)
        held.append(q)
        print(f"{L:6.2f} {q['p0_bar']:8.2f} {q['a_peak_g']:8.2f} {q['gas_kg']*1e3:7.1f} "
              f"{(q['gas_kg']/base['gas_kg']-1)*100:11.1f}% {q['tube_kg']:8.3f}")

    # band 5 and 9: the full surface, and what dominates today's point
    surface = [point(p * 1e5, L) for L in STROKES for p in PRESSURES_BAR]
    doms = [q for q in surface if dominates(q, base)]
    pareto = [q for q in surface
              if not any(dominates(o, q) for o in surface)]
    pareto.sort(key=lambda q: -q['v_exit'])

    print(f"\n{len(doms)} of {len(surface)} surface points dominate Gen6 on all three axes")
    if doms:
        best = max(doms, key=lambda q: q['v_exit'] / max(q['a_peak_g'], 1e-9))
        store = (pc.CHAMBER_KG if hasattr(pc, 'CHAMBER_KG') else 0.936) + best['tube_kg']
        print(f"  best velocity-per-g among them: {best['L']:.2f} m at "
              f"{best['p0_bar']:.1f} bar -> {best['v_exit']:.2f} m/s, "
              f"{best['a_peak_g']:.2f} g, {best['gas_kg']*1e3:.1f} g gas")

    print(f"\nPareto front ({len(pareto)} points), velocity-first:")
    print(f"{'L m':>6s} {'p0 bar':>8s} {'v m/s':>7s} {'a_pk g':>8s} {'gas g':>7s}")
    for q in pareto[:14]:
        print(f"{q['L']:6.2f} {q['p0_bar']:8.1f} {q['v_exit']:7.2f} {q['a_peak_g']:8.2f} "
              f"{q['gas_kg']*1e3:7.1f}")

    # the recommended point: same velocity as today, on the longest stage A37 lists
    rec = point(p_for_v(base['v_exit'], 8.0), 8.0)
    gas_saved = (1 - rec['gas_kg'] / base['gas_kg']) * 100
    # store scales with gas: reservoir sized on usable gas, chamber unchanged
    store_scale = rec['gas_kg'] / base['gas_kg']
    store_today = 5.38                      # A43's design store
    store_rec = 0.936 + (store_today - 0.936) * store_scale + rec['tube_kg']
    per_sat = (ADDED_BASE_KG + store_rec) / N

    a_dev = max(abs(q['a_peak_g'] - fixed_p[0]['a_peak_g']) for q in fixed_p)
    gas_dev = max(abs(q['gas_kg'] - fixed_p[0]['gas_kg']) for q in fixed_p)
    fr = [q['friction_frac'] for q in fixed_p]

    bands = [
        ('1', "L=2.18 m, 50 bar reproduces A41's 30.535 m/s and 1864.8 J within 0.1 %",
         f"{base['v_exit']:.3f} m/s, {base['work_J']:.1f} J",
         abs(base['v_exit'] - 30.535) / 30.535 <= 1e-3
         and abs(base['work_J'] - 1864.8) / 1864.8 <= 1e-3),
        ('2', 'work from a fixed charge is monotonically increasing in stroke',
         f"{fixed_p[0]['work_J']:.1f} -> {fixed_p[-1]['work_J']:.1f} J",
         all(a['work_J'] < b['work_J'] for a, b in zip(fixed_p, fixed_p[1:]))),
        ('3', 'peak acceleration is independent of stroke within 0.1 %',
         f"max deviation {a_dev:.6f} g", a_dev / fixed_p[0]['a_peak_g'] <= 1e-3),
        ('4', 'gas per shot is unchanged across the stroke sweep within 0.1 %',
         f"max deviation {gas_dev*1e6:.3f} mg",
         gas_dev / fixed_p[0]['gas_kg'] <= 1e-3),
        ('5', 'a point exists beating Gen6 on velocity, peak g and gas at once',
         f"{len(doms)} such points", bool(doms)),
        ('6', 'friction fraction varies by <= 2 percentage points across the stroke sweep',
         f"{min(fr)*100:.2f} % to {max(fr)*100:.2f} %", (max(fr) - min(fr)) * 100 <= 2.0),
        ('7', 'tube mass at 8.0 m <= 2.0 kg',
         f"{point(50e5, 8.0)['tube_kg']:.3f} kg", point(50e5, 8.0)['tube_kg'] <= 2.0),
        ('8', f'added mass per satellite at the recommended point <= {TARGET_KG} kg',
         f"{per_sat:.3f} kg", per_sat <= TARGET_KG),
        ('9', 'the Pareto front is published rather than a single point',
         f"{len(pareto)} points reported", len(pareto) > 1),
    ]
    print()
    for n, text, got, ok in bands:
        print(f"  {n}  {'PASS' if ok else 'FAIL'}  {text}: {got}")

    print(f"\nrecommended: {rec['L']:.1f} m at {rec['p0_bar']:.2f} bar -> "
          f"{rec['v_exit']:.3f} m/s at {rec['a_peak_g']:.2f} g peak, "
          f"{rec['gas_kg']*1e3:.1f} g gas ({gas_saved:.1f} % less), "
          f"store ~{store_rec:.2f} kg, {per_sat:.3f} kg/satellite")

    out = dict(analysis='A49', bands_declared_commit='HEAD~1',
               note='ideal gas, closed adiabatic expansion, Coulomb friction constant over the '
                    'stroke, tube as a plain cylinder at one wall thickness, no bending, no '
                    'alignment tolerance, no dynamic seal behaviour. Every omission flatters a '
                    'long tube. Store mass at the recommended point is scaled from A43 by gas '
                    'ratio and is an ESTIMATE, not a sized store.',
               gen6_today=base, fixed_pressure_sweep=fixed_p, held_velocity_sweep=held,
               pareto=pareto, dominating_count=len(doms), surface_size=len(surface),
               recommended=rec, recommended_store_kg=store_rec,
               recommended_per_satellite_kg=per_sat, gas_saved_pct=gas_saved,
               bands=[dict(n=n, band=t, got=g, passed=bool(o)) for n, t, g, o in bands])
    with open(os.path.join(RESULTS, 'design_surface.json'), 'w') as f:
        json.dump(out, f, indent=2)
        f.write('\n')


if __name__ == '__main__':
    main()
