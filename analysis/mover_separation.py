"""
VOLLEY | Separating the mover from the payload: what standoff buys, and what reeving costs.

Review items 16 and 15.

ITEM 16. The sled carries the Halbach arrays AND the payload. A14 measured 61.081 mT at the
20 mm near face -- 611x a magnetometer's full scale -- and PAYLOAD_ENVIRONMENT concedes two
losses because of it: a payload's magnetometer is unusable inside the deployer, and soft-magnetic
parts leave PERMANENTLY MAGNETISED, which compromises the "never modified" claim (item 9).

If the payload rode AHEAD of the mover instead of on top of it, the standoff is a design
variable rather than a fixed 20 mm. This computes what standoff is needed, and what it costs.

ITEM 15. A tug carrying the magnets, coupled to a separate payload carriage through a cable
and pulley -- EMALS-like, with the tug running the other way. Reeving ratio n means the
carriage moves n times the tug's distance at n times its speed, for n times the force and
n^2 times the tug's reflected inertia. That is the trade.

Provenance: model output. Field from motor_model's own magpylib array.
"""
import json
import math
import os

import numpy as np

import motor_model as mm

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
MAG_FS = 100e-6           # T, attitude-magnetometer full scale, class figure per A14
B_EARTH = 45e-6           # T


def field_at(standoff_m, axis='y'):
    """|B| at `standoff_m` from the array centre, PERPENDICULAR to the array plane.

    motor_model's frame is not the CAD frame: here the gap is along y and the array depth
    along z, so the payload standoff PAYLOAD_ENVIRONMENT calls "z" is this module's +y.
    Probing along +x instead puts the point on the array's own symmetry axis, where
    everything cancels and the result is 1e-17 T of numerical noise -- the same error A2
    band 3 made, and the reason that band is recorded as badly chosen.
    """
    f = mm.build_field()
    p = {'y': [0.0, standoff_m, 0.0], 'x': [standoff_m, 0.0, 0.0]}[axis]
    return float(np.linalg.norm(f.getB([p])[0]))


def standoff_sweep():
    # Longitudinal standoff: the payload ahead of the mover, along the track.
    rows = []
    for mm_off in (20, 50, 100, 150, 200, 251, 300, 400, 500):
        B = field_at(mm_off / 1000.0, 'y')
        rows.append(dict(standoff_mm=mm_off, B_T=B, x_mag_fs=B / MAG_FS,
                         x_earth=B / B_EARTH))
    return rows


def reeving(n_values=(1, 2, 3), m_carriage=2.0, m_pay=4.0, m_tug=9.445,
            v_exit=16.388, L_payload=1.30):
    """Item 15: what a pulley ratio buys and costs.

    Carriage moves n x the tug's distance at n x its speed. Force at the tug is n x the
    carriage force, and the tug's inertia referred to the carriage is m_tug / n^2 ... no:
    referred to the CARRIAGE, a tug moving 1/n as far contributes m_tug/n^2. That is the
    one genuinely favourable term, and it is why reeving is interesting at all.
    """
    out = []
    for n in n_values:
        L_tug = L_payload / n                     # the track only has to be this long
        m_eff = m_pay + m_carriage + m_tug / (n * n)
        # Same commanded force at the tug as today.
        Kt, _ = mm.thrust_constant()
        F_tug = 0.9 * Kt * mm.K_RATED
        F_carriage = F_tug / n                    # force divides as distance multiplies
        a = F_carriage / (m_pay + m_carriage)
        # Energy method on the effective mass, which is the honest way to carry the tug.
        a_eff = F_tug / (n * m_eff)
        v = math.sqrt(2 * a_eff * L_payload)
        out.append(dict(n=n, track_len_m=L_tug, m_eff_kg=m_eff, F_tug_N=F_tug,
                        F_carriage_N=F_carriage, a_g=a_eff / 9.81, v_exit=v,
                        v_tug=v / n))
    return out


if __name__ == '__main__':
    print("ITEM 16 -- field against standoff, perpendicular to the array plane\n")
    print(f"{'standoff':>9s} {'|B|':>12s} {'x mag FS':>10s} {'x Earth':>9s}")
    rows = standoff_sweep()
    for r in rows:
        print(f"{r['standoff_mm']:8d}mm {r['B_T']:11.3e}T {r['x_mag_fs']:10.2f} "
              f"{r['x_earth']:9.2f}")
    under_fs = next((r for r in rows if r['x_mag_fs'] < 1.0), None)
    under_e = next((r for r in rows if r['x_earth'] < 1.0), None)
    print(f"\n  below magnetometer full scale at ~{under_fs['standoff_mm'] if under_fs else '>500'} mm")
    print(f"  below Earth's own field at ~{under_e['standoff_mm'] if under_e else '>500'} mm")

    print("\n\nITEM 15 -- reeving a tug to a separate carriage\n")
    print(f"{'ratio':>6s} {'track m':>9s} {'m_eff kg':>9s} {'F carriage':>11s} "
          f"{'a (g)':>7s} {'v_exit':>8s} {'v_tug':>7s}")
    rv = reeving()
    for r in rv:
        print(f"{r['n']:6d} {r['track_len_m']:9.2f} {r['m_eff_kg']:9.2f} "
              f"{r['F_carriage_N']:10.0f}N {r['a_g']:7.2f} {r['v_exit']:7.2f} "
              f"{r['v_tug']:7.2f}")
    print("\n  Track length is what the ENVELOPE cares about (P9: 1839 mm, 44 % over class).")

    os.makedirs(RESULTS, exist_ok=True)
    json.dump(dict(standoff=rows, reeving=rv, mag_fs_T=MAG_FS, B_earth_T=B_EARTH),
              open(os.path.join(RESULTS, 'mover_separation.json'), 'w'), indent=2)
    print("\n-> results/mover_separation.json")
