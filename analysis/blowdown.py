"""
VOLLEY | The blowdown transient: does the gas arrive in time, and can velocity be commanded?

WHY THIS EXISTS
---------------
P60, and A39's own closing sentence: gas removes a mass problem and introduces a fluid-system
problem, and A39 sized the first and not the second. It chose gas on a quasi-static argument
-- swept volume times working pressure equals the energy needed -- and never asked whether the
gas can ARRIVE in time. Filling 0.428 litres in a 133 ms stroke is roughly 3 L/s.

Nothing about Gen6's geometry can be drawn until this closes. The bore, the reservoir and the
valve are the first three dimensions in cad/parameters.json.

AND A SECOND QUESTION A39 COULD NOT ASK
---------------------------------------
A falling reservoir means every shot is different, against a project whose whole proposition
is a velocity commanded per satellite. The candidate mechanism is VALVE CUT-OFF: open, close
at a commanded time, coast the rest of the stroke. Velocity becomes a function of timing
rather than of pressure -- a digital quantity, and the same trick the linear motor played
with current.

Bands declared in validation/A40_blowdown_transient.md at 0d05ea2, BEFORE this file existed.

Provenance: model output. Isentropic choked flow, ideal gas, adiabatic reservoir and cylinder.
No line losses, no wall heat transfer, no seal friction, no valve dynamics beyond the declared
ramp. Every one of those omissions makes this optimistic.
"""
import json
import math
import os

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

# Gas: nitrogen
GAMMA, R_GAS, T0 = 1.4, 296.8, 300.0
CD = 0.8                              # orifice discharge coefficient
CRIT = (2.0 / (GAMMA + 1.0)) ** (GAMMA / (GAMMA - 1.0))     # 0.528

# Geometry, from A39
BORE = 0.015805366135494582
AREA = math.pi * (BORE / 2.0) ** 2
STROKE = 2.18
P_STORE, P_WORK = 200e5, 50e5
RESERVOIR = 1.7108640e-3              # m3
M_PAY = 4.0
G = 9.81
G_CAP = 25.0
DEAD_VOLUME = AREA * 0.010            # 10 mm of cylinder behind the piston at rest
P_AMBIENT = 0.0                       # vacuum
VALVE_RAMP_S = 2e-3                   # orifice opens linearly over 2 ms


def mdot(p_up, rho_up, p_dn, area):
    """Isentropic mass flow through `area` from (p_up, rho_up) to p_dn. Choked below CRIT."""
    if area <= 0.0 or p_up <= p_dn:
        return 0.0
    ratio = max(p_dn / p_up, 1e-12)
    if ratio <= CRIT:
        flux = math.sqrt(GAMMA * p_up * rho_up) * \
            (2.0 / (GAMMA + 1.0)) ** ((GAMMA + 1.0) / (2.0 * (GAMMA - 1.0)))
    else:
        flux = math.sqrt(2.0 * GAMMA / (GAMMA - 1.0) * p_up * rho_up
                         * (ratio ** (2.0 / GAMMA) - ratio ** ((GAMMA + 1.0) / GAMMA)))
    return CD * area * flux


def shot(orifice_m2, p_res0, cutoff_s=None, dt=2e-7, v_cap=None):
    """One shot. Returns exit state, peak acceleration and gas consumed.

    Reservoir expands adiabatically; the cylinder is filled adiabatically while the piston
    does work on the payload. `cutoff_s` closes the orifice at that time -- the payload then
    coasts on the gas already admitted, which keeps pushing as it expands.
    """
    rho_res = p_res0 / (R_GAS * T0)
    m_res = rho_res * RESERVOIR
    p_res = p_res0

    m_cyl, x, v, t = 0.0, 0.0, 0.0, 0.0
    p_cyl = P_AMBIENT
    a_peak = 0.0
    while x < STROKE and t < 2.0:
        vol = DEAD_VOLUME + AREA * x
        open_frac = 0.0 if (cutoff_s is not None and t >= cutoff_s) \
            else min(1.0, t / VALVE_RAMP_S)
        flow = mdot(p_res, m_res / RESERVOIR, p_cyl, orifice_m2 * open_frac)

        # reservoir: adiabatic expansion of the gas that stays behind
        m_res_new = m_res - flow * dt
        if m_res_new <= 0.0:
            m_res_new, flow = 0.0, m_res / dt
        p_res = p_res0 * (m_res_new / (rho_res * RESERVOIR)) ** GAMMA
        m_res = m_res_new

        # cylinder: energy added by inflow, minus work done on the piston
        m_cyl += flow * dt
        if m_cyl <= 0.0:
            p_cyl = P_AMBIENT
        else:
            # adiabatic with mass addition at reservoir stagnation enthalpy
            p_cyl = p_cyl + (GAMMA * R_GAS * T0 * flow / vol
                             - GAMMA * p_cyl * AREA * v / vol) * dt
            p_cyl = max(p_cyl, 0.0)

        a = p_cyl * AREA / M_PAY
        a_peak = max(a_peak, a)
        v += a * dt
        x += v * dt
        t += dt
        if v_cap and v > v_cap:
            break
    return dict(v_exit=v, t_s=t, x_m=x, a_peak_g=a_peak / G,
                gas_used_kg=rho_res * RESERVOIR - m_res,
                p_res_end=p_res)


def bisect_orifice(target_g=G_CAP, lo=1e-7, hi=1e-4):
    """Largest orifice whose peak acceleration stays inside the qualification cap."""
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if shot(mid, P_STORE)['a_peak_g'] <= target_g:
            lo = mid
        else:
            hi = mid
    return lo


def main():
    # band 1: open the orifice wide and the transient must contain the quasi-static answer
    quasi = shot(100e-6, P_STORE)

    orifice = bisect_orifice()
    d_mm = 2e3 * math.sqrt(orifice / math.pi)
    nominal = shot(orifice, P_STORE)

    print(f"orifice sized on the {G_CAP:.0f} g cap: {orifice*1e6:.3f} mm2, "
          f"{d_mm:.2f} mm diameter")
    print(f"  shot 1   v {nominal['v_exit']:6.2f} m/s   peak {nominal['a_peak_g']:5.2f} g   "
          f"t {nominal['t_s']*1e3:6.1f} ms   gas {nominal['gas_used_kg']*1e3:6.2f} g")

    # band 5: twelve shots in sequence off one bottle
    p, seq = P_STORE, []
    for i in range(12):
        s = shot(orifice, p)
        seq.append(dict(shot=i + 1, p_res_bar=p / 1e5, v_exit=s['v_exit'],
                        a_peak_g=s['a_peak_g'], gas_used_g=s['gas_used_kg'] * 1e3))
        p = s['p_res_end']
    print(f"\n{'shot':>4s} {'p_res bar':>10s} {'v m/s':>8s} {'peak g':>7s} {'gas g':>7s}")
    for r in (seq[0], seq[5], seq[10], seq[11]):
        print(f"{r['shot']:4d} {r['p_res_bar']:10.1f} {r['v_exit']:8.2f} "
              f"{r['a_peak_g']:7.2f} {r['gas_used_g']:7.2f}")
    droop = seq[-1]['v_exit'] / seq[0]['v_exit']

    # band 6: is velocity commandable by valve cut-off?
    print("\ncommanding velocity by valve cut-off:")
    cut = []
    for ms in (2, 3, 4, 5, 6, 8, 10, 15, 20, 40, None):
        s = shot(orifice, P_STORE, cutoff_s=None if ms is None else ms * 1e-3)
        cut.append(dict(cutoff_ms=ms, v_exit=s['v_exit'], a_peak_g=s['a_peak_g']))
        print(f"  cut at {str(ms)+' ms' if ms else 'never ':>8s}  v {s['v_exit']:6.2f} m/s")
    finite = [c for c in cut if c['cutoff_ms']]
    monotonic = all(finite[i]['v_exit'] <= finite[i + 1]['v_exit'] + 1e-9
                    for i in range(len(finite) - 1))
    span_lo, span_hi = finite[0]['v_exit'], finite[-1]['v_exit']

    # band 7: sensitivity to a 1 ms timing error at a mid-range cut-off
    base_ms = 6
    v0 = shot(orifice, P_STORE, cutoff_s=base_ms * 1e-3)['v_exit']
    vp = shot(orifice, P_STORE, cutoff_s=(base_ms + 1) * 1e-3)['v_exit']
    vm = shot(orifice, P_STORE, cutoff_s=(base_ms - 1) * 1e-3)['v_exit']
    timing_pct = max(abs(vp - v0), abs(vm - v0)) / v0 * 100.0
    print(f"\n  +/-1 ms at a {base_ms} ms cut-off ({v0:.2f} m/s): "
          f"{timing_pct:.2f} % velocity error")

    a39_swept_kg = (P_WORK / (R_GAS * T0)) * AREA * STROKE
    bands = [
        ('1', 'wide orifice reproduces A39 32.7 m/s within 2 %',
         f"{quasi['v_exit']:.2f} m/s", abs(quasi['v_exit'] - 32.7) / 32.7 <= 0.02),
        ('2', f'peak acceleration <= {G_CAP:.0f} g',
         f"{nominal['a_peak_g']:.2f} g", nominal['a_peak_g'] <= G_CAP + 1e-6),
        ('3', 'shot 1 exit velocity >= 30 m/s',
         f"{seq[0]['v_exit']:.2f} m/s", seq[0]['v_exit'] >= 30.0),
        ('4', 'orifice diameter <= 10 mm', f"{d_mm:.2f} mm", d_mm <= 10.0),
        ('5', 'shot 12 reaches >= 95 % of shot 1',
         f"{droop*100:.1f} % ({seq[-1]['v_exit']:.2f} against {seq[0]['v_exit']:.2f} m/s)",
         droop >= 0.95),
        ('6', 'cut-off spans 20 -> 30 m/s monotonically',
         f"{span_lo:.1f} -> {span_hi:.1f} m/s, monotonic {monotonic}",
         monotonic and span_lo <= 20.0 and span_hi >= 30.0),
        ('7', '+/-1 ms timing error gives <= 1 % velocity error',
         f"{timing_pct:.2f} %", timing_pct <= 1.0),
        ('8', "gas per shot within 20 % of A39's swept-volume figure",
         f"{nominal['gas_used_kg']*1e3:.2f} g against {a39_swept_kg*1e3:.2f} g",
         abs(nominal['gas_used_kg'] - a39_swept_kg) / a39_swept_kg <= 0.20),
    ]
    print("\nbands:")
    for n, name, detail, ok in bands:
        print(f"  band {n}: {'PASS' if ok else 'FAIL'}  {name}\n            {detail}")

    out = dict(analysis='A40', bands_declared_commit='0d05ea2',
               note='isentropic choked flow, ideal gas, adiabatic. No line losses, wall heat '
                    'transfer, seal friction or valve dynamics beyond a 2 ms ramp; every '
                    'omission makes this optimistic. Designs no valve, seal or manifold and '
                    'does not check A34 release residual.',
               bore_m=BORE, area_m2=AREA, stroke_m=STROKE, reservoir_m3=RESERVOIR,
               p_store_Pa=P_STORE, orifice_m2=orifice, orifice_mm=d_mm,
               quasi_static=quasi, nominal=nominal, sequence=seq,
               droop_shot12_over_shot1=droop, cutoff_sweep=cut,
               timing_sensitivity_pct_per_ms=timing_pct,
               bands=[dict(band=n, name=nm, detail=d, pass_=ok)
                      for n, nm, d, ok in bands])
    os.makedirs(RESULTS, exist_ok=True)
    path = os.path.join(RESULTS, 'blowdown.json')
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(out, fh, indent=2, default=float)
        fh.write('\n')
    print(f"\nwrote {path}")


if __name__ == '__main__':
    main()
