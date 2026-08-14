"""A19: rank the assumed inputs by how much each moves the answer.

Bands declared in validation/A19_sensitivity_ranking.md at 03628da, before this file existed.

WHAT THIS IS NOT
----------------
It ranks assumptions. It does not make any of them less assumed. Every input here is unmeasured
before this runs and unmeasured after it, and E4 is unaffected. The output is a measurement
priority list, not new precision.

The project already has a Monte Carlo, and it measures DISPERSION -- how much v_exit scatters
given sensor noise. That is a different question from which of the numbers nobody has measured
would change the result if it turned out to be wrong.

METHOD
------
For each input i and output y, with nominal x0 and declared range [lo, hi]:

    swing      = (max(y) - min(y)) / y(x0)   over {lo, x0, hi}   -- GLOBAL, primary key
    elasticity = (dy/y) / (dx/x) at x0, central difference +/-5% -- LOCAL, range-independent

Ranking by a global measure alone confounds "this matters" with "I drew a wide range for it".
Ranking by a local measure alone misses saturation. Both are reported and bands 1 and 2 check
that they agree.

PROVENANCE
----------
Every input is patched on the module that OWNS it and the real pipeline is re-run. Nothing is
restated here: BR and R_ESR patch motor_model and go through thrust_constant/shot/regen_brake,
the packing efficiency patches payload_family's calibrated value, and the binding outputs call
phase1_closeout's own e10/e19/e20/e26 and astro's lifetime.

Run:  python3 analysis/sensitivity_ranking.py
"""
import json
import math
import os

import numpy as np

import astro
import motor_model as mm
import payload_family
import phase1_closeout as pc

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

OUTPUTS = ('v_exit', 'eff_net_pct', 'kg_per_satellite')
PERTURB = 0.05          # +/-5 % for the local elasticity

# (key, label, nominal, lo, hi, range provenance) -- the table declared in the run sheet.
INPUTS = [
    ('BR', 'magnet remanence', 1.32, 1.25, 1.40, 'assumed; CAD states no grade'),
    ('B_POLE', 'brake pole field', 0.50, 0.30, 0.70, "A18 sweep; unstated in CAD, B-4 bounds it"),
    ('Q', 'structural Q', 20.0, 10.0, 30.0, 'A18 sweep; never measured (STRUCTURAL_GAP)'),
    ('EPS', 'fin emissivity', 0.50, 0.05, 0.90, 'A18 sweep; surface finish unspecified'),
    ('H_CONT', 'contact conductance', 500.0, 100.0, 5000.0, 'A18 sweep; joint unspecified'),
    ('R_ESR', 'bank ESR', 0.012, 0.006, 0.065, 'nominal unsourced (E17); ceiling from A10'),
    ('BC', 'ballistic coefficient', 61.0, 40.0, 90.0, 'A5 sweep'),
    ('PACK', 'packing efficiency', None, 0.40, 0.60, 'calibrated to the 3U layout'),
    ('RHO_MAG_E', 'magnet resistivity', 1.4e-6, 1.2e-6, 1.6e-6, 'assumed; grade unstated'),
]

# Declared in the run sheet BEFORE the run: which inputs have no model path to which output.
# Band 3 requires these to return exactly 0.0, not merely small.
NO_PATH = {
    'v_exit': ('B_POLE', 'Q', 'EPS', 'H_CONT', 'BC', 'PACK', 'RHO_MAG_E'),
    'eff_net_pct': ('B_POLE', 'Q', 'EPS', 'H_CONT', 'BC', 'PACK', 'RHO_MAG_E'),
    'kg_per_satellite': ('BR', 'B_POLE', 'Q', 'EPS', 'H_CONT', 'R_ESR', 'BC', 'RHO_MAG_E'),
}


def _pack_nominal():
    return payload_family._pack_efficiency()


def motor_chain():
    """The real pipeline: Kt -> shot -> regen -> net efficiency. Same order as motor_model.main."""
    Kt, _ripple = mm.thrust_constant()
    s = mm.shot(Kt)
    rg = mm.regen_brake(Kt, s['v_exit'], mm.V0 * (1 - s['sag_pct'] / 100))
    net = s['E_drawn'] - rg['E_recovered']
    return s['v_exit'], s['KE_payload'] / net * 100.0


def kg_per_sat(pack_eff):
    """3U kg per satellite at a given packing efficiency. n is an int(), so this is a STEP
    function -- a small change in packing moves nothing until a slot appears or disappears."""
    box = next(b for tag, _m, b, _n in payload_family.CLASSES if tag == '3U CubeSat')
    n = int(payload_family.BAY_MM3 / (box[0] * box[1] * box[2]) * pack_eff)
    return payload_family.DEPLOYER_DRY_KG / n if n else float('nan')


def evaluate(key, value):
    """Return the three ranked outputs with `key` set to `value`. Everything else nominal."""
    if key == 'BR':
        old = mm.BR
        mm.BR = value
        try:
            v, e = motor_chain()
        finally:
            mm.BR = old
        return dict(v_exit=v, eff_net_pct=e, kg_per_satellite=kg_per_sat(_pack_nominal()))
    if key == 'R_ESR':
        old = mm.R_ESR
        mm.R_ESR = value
        try:
            v, e = motor_chain()
        finally:
            mm.R_ESR = old
        return dict(v_exit=v, eff_net_pct=e, kg_per_satellite=kg_per_sat(_pack_nominal()))
    if key == 'PACK':
        v, e = NOMINAL_MOTOR
        return dict(v_exit=v, eff_net_pct=e, kg_per_satellite=kg_per_sat(value))
    # Every remaining input has no declared path to the three ranked outputs.
    v, e = NOMINAL_MOTOR
    return dict(v_exit=v, eff_net_pct=e, kg_per_satellite=kg_per_sat(_pack_nominal()))


def binding_output(key, value):
    """The quantity each input actually governs, for inputs with no path to the ranked three.

    Calls A18's own functions rather than restating their physics.
    """
    if key == 'B_POLE':
        old = pc.B_POLE_SWEEP
        pc.B_POLE_SWEEP = (value,)
        try:
            rows, _ok = pc.e20(14.1, 934.7)
        finally:
            pc.B_POLE_SWEEP = old
        return 'brake stop distance', rows[0]['stop_dist_m'], 'm'
    if key == 'Q':
        old = pc.Q_SWEEP
        pc.Q_SWEEP = (value,)
        try:
            rows, _cap = pc.e10()
        finally:
            pc.Q_SWEEP = old
        return 'gate margin of safety', rows[0]['MoS'], '-'
    if key in ('EPS', 'H_CONT'):
        # NOT the peak. The fin's peak temperature is set entirely by the first shot's
        # adiabatic rise q_shot/C, which neither emissivity nor contact conductance touches,
        # so reporting the peak here returns an identical number at both ends of the range
        # and looks like a broken sweep. What these two actually govern is how completely
        # the fin decays between shots, which is the residual after the campaign.
        old_e, old_h = pc.EPS_SWEEP, pc.H_SWEEP
        pc.EPS_SWEEP = (value,) if key == 'EPS' else (0.50,)
        pc.H_SWEEP = (value,) if key == 'H_CONT' else (500.0,)
        try:
            rows = pc.e26(934.7 / 12)
        finally:
            pc.EPS_SWEEP, pc.H_SWEEP = old_e, old_h
        return 'fin residual above ambient after 12 shots', rows[0]['final_K'] - pc.T_ENV, 'K'
    if key == 'BC':
        return 'unboosted lifetime', astro.lifetime(astro.RE + 450e3, 0.0, BC=value), 'yr'
    if key == 'RHO_MAG_E':
        old = pc.SIG_NDFEB
        pc.SIG_NDFEB = 1.0 / value
        try:
            r = pc.e19(mm.operating_point()['v_exit'])
        finally:
            pc.SIG_NDFEB = old
        return 'magnet eddy rise per shot', r['dT_per_shot_K'], 'K'
    return None, None, None


def sweep(scale=1.0):
    """Swing and elasticity for every input. `scale` shrinks each range about its nominal,
    so scale=0.5 is band 5's halved-range test."""
    rows = []
    for key, label, nom, lo, hi, prov in INPUTS:
        x0 = _pack_nominal() if key == 'PACK' else nom
        lo_s = x0 + (lo - x0) * scale
        hi_s = x0 + (hi - x0) * scale

        at = {p: evaluate(key, p) for p in (lo_s, x0, hi_s)}
        base = at[x0]

        swing, elast = {}, {}
        for out in OUTPUTS:
            vals = [at[p][out] for p in (lo_s, x0, hi_s)]
            swing[out] = (max(vals) - min(vals)) / abs(base[out]) if base[out] else 0.0

            yp = evaluate(key, x0 * (1 + PERTURB))[out]
            ym = evaluate(key, x0 * (1 - PERTURB))[out]
            elast[out] = ((yp - ym) / base[out]) / (2 * PERTURB) if base[out] else 0.0

        rows.append(dict(key=key, label=label, nominal=x0, lo=lo_s, hi=hi_s,
                         provenance=prov, swing=swing, elasticity=elast))
    return rows


def rank(rows, out, metric):
    """Inputs ordered by |metric| on one output, descending."""
    return [r['key'] for r in sorted(rows, key=lambda r: -abs(r[metric][out]))]


def main():
    global NOMINAL_MOTOR
    NOMINAL_MOTOR = motor_chain()
    print(f"nominal: v_exit {NOMINAL_MOTOR[0]:.3f} m/s, eff_net {NOMINAL_MOTOR[1]:.2f} %, "
          f"kg/sat {kg_per_sat(_pack_nominal()):.3f}\n")

    full = sweep(1.0)
    half = sweep(0.5)

    # --- bands ---------------------------------------------------------------
    bands = {}

    # 1 and 2: swing versus elasticity, leader and top three
    b1, b2 = {}, {}
    for out in OUTPUTS:
        rs, re_ = rank(full, out, 'swing'), rank(full, out, 'elasticity')
        b1[out] = dict(swing=rs[0], elasticity=re_[0], agree=rs[0] == re_[0])
        b2[out] = dict(swing=rs[:3], elasticity=re_[:3], agree=set(rs[:3]) == set(re_[:3]))
    bands['1_leader_agrees'] = dict(per_output=b1, passed=all(v['agree'] for v in b1.values()))
    bands['2_top3_agrees'] = dict(per_output=b2, passed=all(v['agree'] for v in b2.values()))

    # 3: declared no-path entries must be exactly zero
    viol = [(r['key'], out, r['swing'][out], r['elasticity'][out])
            for r in full for out in OUTPUTS if r['key'] in NO_PATH[out]
            and (r['swing'][out] != 0.0 or r['elasticity'][out] != 0.0)]
    bands['3_declared_zeros'] = dict(violations=viol, passed=not viol)

    # 4: something must move v_exit by >= 1 %
    max_v = max(r['swing']['v_exit'] for r in full)
    leader_v = max(full, key=lambda r: r['swing']['v_exit'])['key']
    bands['4_v_exit_moves'] = dict(max_swing_pct=max_v * 100, by=leader_v,
                                   passed=max_v >= 0.01)

    # 5: rank order under halved ranges, top three per output
    b5 = {}
    for out in OUTPUTS:
        a, b = rank(full, out, 'swing')[:3], rank(half, out, 'swing')[:3]
        b5[out] = dict(full=a, halved=b, unchanged=a == b)
    bands['5_rank_stable_halved'] = dict(per_output=b5,
                                         passed=all(v['unchanged'] for v in b5.values()))

    # 6: provenance of each leader -- report, VOID-able
    b6 = {}
    for out in OUTPUTS:
        lead = rank(full, out, 'swing')[0]
        prov = next(r['provenance'] for r in full if r['key'] == lead)
        b6[out] = dict(leader=lead, provenance=prov,
                       unsourced=('assumed' in prov or 'unsourced' in prov))
    bands['6_leader_provenance'] = dict(per_output=b6, verdict='REPORT')

    # --- binding outputs -----------------------------------------------------
    binding = []
    for key, label, nom, lo, hi, _prov in INPUTS:
        if key in ('BR', 'R_ESR', 'PACK'):
            continue
        name, y_lo, unit = binding_output(key, lo)
        _n, y_hi, _u = binding_output(key, hi)
        _n, y_0, _u = binding_output(key, nom)
        binding.append(dict(key=key, label=label, quantity=name, unit=unit,
                            at_lo=y_lo, at_nominal=y_0, at_hi=y_hi,
                            swing=(abs(y_hi - y_lo) / abs(y_0)) if y_0 else None))

    res = dict(analysis='A19', bands_declared_commit='03628da',
               framing='ranks assumptions; does not make any of them less assumed',
               nominal=dict(v_exit=NOMINAL_MOTOR[0], eff_net_pct=NOMINAL_MOTOR[1],
                            kg_per_satellite=kg_per_sat(_pack_nominal())),
               perturbation=PERTURB, inputs=full, halved_ranges=half,
               bands=bands, binding_outputs=binding)

    # --- report --------------------------------------------------------------
    print(f"{'input':24}" + ''.join(f"{o[:14]:>16}" for o in OUTPUTS))
    print(f"{'':24}" + ''.join(f"{'swing %':>16}" for _ in OUTPUTS))
    for r in sorted(full, key=lambda r: -max(r['swing'][o] for o in OUTPUTS)):
        print(f"  {r['label']:22}" + ''.join(f"{r['swing'][o]*100:16.3f}" for o in OUTPUTS))

    print(f"\n{'input':24}" + ''.join(f"{'elasticity':>16}" for _ in OUTPUTS))
    for r in sorted(full, key=lambda r: -max(abs(r['elasticity'][o]) for o in OUTPUTS)):
        print(f"  {r['label']:22}" + ''.join(f"{r['elasticity'][o]:16.4f}" for o in OUTPUTS))

    print("\nbinding outputs, for the inputs with no path to the ranked three:")
    for b in binding:
        print(f"  {b['label']:22} {b['quantity']:28} "
              f"{b['at_lo']:9.3f} -> {b['at_hi']:9.3f} {b['unit']}")

    print("\nbands:")
    for k, v in bands.items():
        mark = v.get('passed')
        print(f"  {k:26} {'PASS' if mark else ('REPORT' if mark is None else 'FAIL')}")
    if viol:
        print("  band 3 violations:", viol)
    for out in OUTPUTS:
        print(f"    {out:18} leader {b1[out]['swing']:12} "
              f"top3 {b5[out]['full']} halved {b5[out]['halved']}")

    path = os.path.join(RESULTS, 'sensitivity_ranking.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(res, f, indent=2, default=float)
        f.write('\n')
    print(f"\nwrote {path}")


if __name__ == '__main__':
    main()
