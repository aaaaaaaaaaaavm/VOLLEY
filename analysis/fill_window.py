"""
VOLLEY | The fill window, and the gas a bottle cannot give back.

WHY THIS EXISTS
---------------
ADR-032's replacement falsifier, written when A41 closed P63: a 2 L chamber cannot be filled
to 50 bar inside the inter-shot window. A41 specified the store and never checked that the
store can be reloaded.

And a second question A41 did not ask, found while scoping this one. A41 sized the reservoir
by dividing total charge by storage pressure -- 6 L at 200 bar for twelve 100 bar.L charges.
That assumes the bottle can be drawn to ZERO. It cannot: below the charge pressure it can no
longer fill the chamber, so only the gas between 200 and 50 bar is usable, three quarters of
it.

Bands declared in validation/A42_fill_window.md at 9c5c6e2, BEFORE this file existed. Band 3
is declared at A41's 6 L rather than at the 8 L the scoping arithmetic gives, because a band
restated to match a number already computed tests nothing.

Provenance: model output. Choked isentropic flow, ideal gas, adiabatic reservoir. No line
losses, valve dynamics, heat of compression or reservoir cooling across a sequence.
"""
import json
import math
import os

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

GAMMA, R_GAS, T0, CD = 1.4, 296.8, 300.0, 0.8
RHO_STORE = 235.0
P_STORE = 200e5

# A42's OWN declared point, frozen, so its run sheet stays reproducible.
P_CHARGE_A42, V_CHAMBER_A42 = 50e5, 2.0e-3


def design_point():
    """Charge pressure and chamber volume, read from cad/parameters.json.

    Second instance of P84. The first repair covered precharged.py and stopped there, while
    this module -- which feeds A42, A43 and A45 -- went on declaring 50 bar. The hole P84
    described was never that one constant was stale; it was that nothing compares the
    parameter file against the analysis. ADR-015: derive, never paste.
    """
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        'cad', 'parameters.json')
    with open(path, encoding='utf-8') as f:
        s = json.load(f)['groups']['gen6_store']
    return s['charge_pressure_bar'] * 1e5, s['chamber_volume_l'] / 1e3


P_CHARGE, V_CHAMBER = design_point()
V_RES_A41 = 6.0e-3
N_MANIFEST = 12
WINDOW_S = 10.0                       # 4 s index + 6 s return, already in the cadence
CADENCE_S = 1200.0                    # ADR-020
PV_OVER_W = 15000.0
CHAMBER_KG = 0.3382                   # A41's 2 L chamber
HARDWARE_KG = 1.5                     # A39's allowance, carried unchanged
ADDED_BASE_KG = 11.45                 # A37 and A36
BUDGET_KG, TARGET_KG = 12.55, 2.0

FLUX = math.sqrt(GAMMA / (R_GAS * T0)) * \
    (2.0 / (GAMMA + 1.0)) ** ((GAMMA + 1.0) / (2.0 * (GAMMA - 1.0)))
CRIT = (2.0 / (GAMMA + 1.0)) ** (GAMMA / (GAMMA - 1.0))


def fill(p_res0, v_res, orifice_m2, dt=1e-4):
    """Fill the chamber from p_res0 to the charge pressure. Returns time, or None."""
    m_res = p_res0 * v_res / (R_GAS * T0)
    m_ch, t = 0.0, 0.0
    p_res, p_ch = p_res0, 0.0
    while p_ch < P_CHARGE and t < 1e4:
        if p_res <= p_ch:
            return None, p_res                       # bottle cannot push any further
        ratio = p_ch / p_res
        if ratio <= CRIT:
            flow = CD * orifice_m2 * p_res * FLUX
        else:
            flow = CD * orifice_m2 * math.sqrt(
                2.0 * GAMMA / (GAMMA - 1.0) * p_res * (p_res / (R_GAS * T0))
                * max(ratio ** (2.0 / GAMMA) - ratio ** ((GAMMA + 1.0) / GAMMA), 0.0))
        step = min(flow * dt, m_res)
        m_res -= step
        m_ch += step
        p_res = p_res0 * (m_res / (p_res0 * v_res / (R_GAS * T0))) ** GAMMA
        p_ch = m_ch * R_GAS * T0 / V_CHAMBER
        t += dt
        if m_res <= 0.0:
            return None, p_res
    return t, p_res


def sequence(v_res, orifice_m2):
    """Twelve fills off one bottle. Returns per-shot time and the shot it fails on."""
    p, out, failed = P_STORE, [], None
    for i in range(N_MANIFEST):
        t, p_end = fill(p, v_res, orifice_m2)
        out.append(dict(shot=i + 1, p_res_bar=p / 1e5,
                        fill_s=t, p_res_end_bar=p_end / 1e5))
        if t is None:
            failed = i + 1
            break
        p = p_end
    return out, failed


def store_kg(v_res):
    return (CHAMBER_KG + P_STORE * v_res / (PV_OVER_W * 9.81)
            + v_res * RHO_STORE + HARDWARE_KG)


def main():
    m_charge = P_CHARGE * V_CHAMBER / (R_GAS * T0)
    print(f"charge: {m_charge*1e3:.1f} g of nitrogen into {V_CHAMBER*1e3:.0f} L at "
          f"{P_CHARGE/1e5:.0f} bar\n")

    print(f"{'orifice mm':>11s} {'first fill s':>13s}")
    orifice = None
    for d_mm in (0.5, 1.0, 2.0, 3.0):
        a = math.pi * (d_mm / 2e3) ** 2
        t, _ = fill(P_STORE, V_RES_A41, a)
        print(f"{d_mm:11.1f} {t if t else float('nan'):13.2f}")
        if orifice is None and t is not None and t <= WINDOW_S:
            orifice, orifice_mm = a, d_mm

    seq6, failed6 = sequence(V_RES_A41, orifice)
    print(f"\nA41's {V_RES_A41*1e3:.0f} L bottle, {orifice_mm:.1f} mm orifice:")
    for r in seq6:
        t = f"{r['fill_s']:.2f} s" if r['fill_s'] else "CANNOT FILL"
        print(f"  shot {r['shot']:2d}  from {r['p_res_bar']:6.1f} bar  {t}")
    if failed6:
        print(f"  -> fails on shot {failed6}")

    # the reservoir that does deliver twelve, found by search rather than asserted
    v_needed = V_RES_A41
    while v_needed < 40e-3:
        _, f = sequence(v_needed, orifice)
        if f is None:
            break
        v_needed += 0.25e-3
    seqN, _ = sequence(v_needed, orifice)
    print(f"\nreservoir that delivers twelve: {v_needed*1e3:.2f} L "
          f"(store {store_kg(v_needed):.2f} kg, was {store_kg(V_RES_A41):.2f})")
    print(f"  last fill {seqN[-1]['fill_s']:.2f} s from "
          f"{seqN[-1]['p_res_bar']:.1f} bar")

    added = ADDED_BASE_KG + store_kg(v_needed)
    bands = [
        ('1', f'first charge fills in <= {WINDOW_S:.0f} s',
         f"{seq6[0]['fill_s']:.2f} s at {orifice_mm:.1f} mm",
         seq6[0]['fill_s'] is not None and seq6[0]['fill_s'] <= WINDOW_S),
        ('2', 'fill orifice <= 5 mm', f"{orifice_mm:.1f} mm", orifice_mm <= 5.0),
        ('3', "A41's 6 L reservoir delivers twelve full charges",
         "fails on shot %s" % failed6 if failed6 else "all twelve", failed6 is None),
        ('4', f'twelfth charge fills in <= 60 s, inside the {CADENCE_S:.0f} s cadence',
         f"{seqN[-1]['fill_s']:.2f} s", seqN[-1]['fill_s'] is not None
         and seqN[-1]['fill_s'] <= 60.0),
        ('5', f'store with the required reservoir <= {BUDGET_KG:.2f} kg',
         f"{store_kg(v_needed):.2f} kg at {v_needed*1e3:.2f} L",
         store_kg(v_needed) <= BUDGET_KG),
        ('6', f'added mass per satellite <= {TARGET_KG:.1f} kg',
         f"{added/N_MANIFEST:.3f} kg", added / N_MANIFEST <= TARGET_KG),
    ]
    print("\nbands:")
    for n, name, detail, ok in bands:
        print(f"  band {n}: {'PASS' if ok else 'FAIL'}  {name}\n            {detail}")

    out = dict(analysis='A42', bands_declared_commit='9c5c6e2',
               note='choked isentropic flow, ideal gas, adiabatic reservoir. No line losses, '
                    'valve dynamics, heat of compression, reservoir cooling across a sequence, '
                    'or gas recovery from the fired chamber.',
               charge_kg=m_charge, orifice_mm=orifice_mm,
               reservoir_a41_l=V_RES_A41 * 1e3, reservoir_required_l=v_needed * 1e3,
               store_a41_kg=store_kg(V_RES_A41), store_required_kg=store_kg(v_needed),
               added_kg_per_satellite=added / N_MANIFEST,
               sequence_a41=seq6, sequence_required=seqN, failed_on_shot=failed6,
               bands=[dict(band=n, name=nm, detail=d, pass_=ok)
                      for n, nm, d, ok in bands])
    os.makedirs(RESULTS, exist_ok=True)
    path = os.path.join(RESULTS, 'fill_window.json')
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(out, fh, indent=2, default=float)
        fh.write('\n')
    print(f"\nwrote {path}")


if __name__ == '__main__':
    main()
