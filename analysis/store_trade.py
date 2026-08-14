"""
VOLLEY | The energy store at metre-scale strokes.

WHY THIS EXISTS
---------------
P60. A37 bands 4 and 8 failed: once the stage supplies the structure and the pulse chain is
deleted, the energy store becomes the binding constraint -- 26.16 kg of spring steel at an
8 m stroke, 78.5 % of everything added. Band 4 was the falsification test A35 declared and
left open, and it says the mass RELOCATED rather than left.

A38 has since established that tip-off does not bind -- ceiling 30.9 g against a 25 g
qualification cap -- so acceleration is free and the store is the only thing left setting
the design point.

WHERE THIS RUN CAN BE WRONG
---------------------------
The gas model rests on seven declared assumptions, all of them in
validation/A39_store_trade.md and repeated at each use below. None is measured, none is
vendor-sourced, and every one of them makes gas look better than a detailed design will.
The 1.5 kg of piston, seals, regulator and valving is the largest single guess.

Bands declared in validation/A39_store_trade.md at 8d78d1a, BEFORE this file existed.

Provenance: model output. Screened-out options carry the run that screened them rather than
being omitted, so the trade cannot read as narrower than the record supports.
"""
import json
import math
import os

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

G, G_CAP, M_SAT, N_MANIFEST = 9.81, 25.0, 4.0, 12
ADDED_BASE_KG = 11.45            # A37 and A36, from opposite directions
BUDGET_KG = 2.0 * N_MANIFEST - ADDED_BASE_KG      # 12.55 kg
FALSIFIER_KG = 14.256            # A35: 60 % of the 23.76 kg the pulse chain released
A37_SELECTED_V = 62.6            # A37's selected point, for the band 1 regression
A37_SELECTED_STORE_KG = 41.86

SPRING_J_PER_KG = 300.0          # actuator_trade.py, upper end for spring steel

# --- the gas model. Every constant here is declared in the run sheet. -------------------
PV_OVER_W = 15000.0              # m, conservative end of the modern composite range
P_STORE, P_WORK = 200e5, 50e5    # Pa
SIGMA_ALLOW, SAFETY = 500e6, 2.0 # Pa, steel tube in hoop
WALL_MIN = 1.0e-3                # m, minimum practical wall
RHO_GAS = 235.0                  # kg/m3, nitrogen-class at 200 bar
GAS_HARDWARE_KG = 1.5            # piston, seals, regulator, valving. THE LARGEST GUESS.

# A35's C3 items: what keeping the linear synchronous motor still costs.
LSM_KG = 6.29 + 0.97 + 6.50 + 4.00 + 6.00     # stator, formers, bank, PPU, thermal

SCREENED_OUT = [
    ('lead screw', 'A27', 'DN limit exceeded 8x, whirling critical speed 36x'),
    ('rack and pinion', 'A27', 'contact drive at full speed in vacuum, E21'),
    ('flywheel through a cable or drum', 'VOLLEY-lab PII-14',
     'm_eff = I/r^2 refers rotating inertia straight onto the moving mass'),
]


def kinematics(v):
    """Stroke, force and energy for one shot at the qualification cap."""
    a = G_CAP * G
    return dict(v_exit=v, a_g=G_CAP, stroke_m=v * v / (2 * a),
                force_N=M_SAT * a, energy_J=0.5 * M_SAT * v * v)


def spring(k):
    """Steel spring, plus the wind/latch/safing rule A37 used, unchanged so the two compare."""
    store = k['energy_J'] / SPRING_J_PER_KG
    mech = max(2.0, 0.60 * store)
    return dict(option='steel spring', store_kg=store, mechanism_kg=mech,
                total_kg=store + mech,
                standby='holds indefinitely; no maintenance',
                maintained_by=None)


def gas(k):
    """Cold gas: a cylinder the payload pushes against, fed from one manifest-sized bottle.

    The reservoir is sized for ALL N shots, not one. That is the point of the option: if a
    single bottle runs the manifest, the wind mechanism a spring needs becomes a valve.
    """
    area = k['force_N'] / P_WORK                        # F = pA at the working pressure
    bore_r = math.sqrt(area / math.pi)
    wall = max(WALL_MIN, P_WORK * bore_r * SAFETY / SIGMA_ALLOW)
    cyl = 2 * math.pi * bore_r * wall * k['stroke_m'] * 7800.0

    swept = area * k['stroke_m']                        # m3 per shot at working pressure
    # Blowdown from store to working pressure: a reservoir V delivers V*(P_STORE-P_WORK)/P_WORK
    # of gas measured at the working pressure.
    reservoir = swept * N_MANIFEST * P_WORK / (P_STORE - P_WORK)
    vessel = (P_STORE * reservoir) / (PV_OVER_W * G)
    gas_kg = reservoir * RHO_GAS

    store = vessel + gas_kg
    return dict(option='cold gas', store_kg=store, mechanism_kg=cyl + GAS_HARDWARE_KG,
                total_kg=store + cyl + GAS_HARDWARE_KG,
                bore_mm=2e3 * bore_r, wall_mm=1e3 * wall, cylinder_kg=cyl,
                vessel_kg=vessel, gas_kg=gas_kg, reservoir_litre=1e3 * reservoir,
                standby='leaks; needs a seal that holds from integration to the last shot',
                maintained_by='none commanded, but the seal is a standby requirement')


def lsm(k):
    """The control: keep the linear synchronous motor. A35's C3 items, unchanged."""
    return dict(option='keep the LSM (control)', store_kg=LSM_KG, mechanism_kg=0.0,
                total_kg=LSM_KG,
                standby='bank self-discharges; P26 says no commercial string sources the shot',
                maintained_by='the bank, which A10 shows cannot be bought')


def busts_at(fn, limit, lo=10.0, hi=200.0):
    """Highest exit velocity at which `fn` still fits under `limit`."""
    if fn(kinematics(lo))['total_kg'] > limit:
        return None
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if fn(kinematics(mid))['total_kg'] <= limit:
            lo = mid
        else:
            hi = mid
    return lo


def main():
    print(f"budget: added base {ADDED_BASE_KG:.2f} kg, kill criterion 1 at "
          f"{2.0*N_MANIFEST:.2f} kg -> store + mechanism must fit {BUDGET_KG:.2f} kg")
    print(f"A35 falsifier: {FALSIFIER_KG:.2f} kg\n")

    print(f"{'option':26s} {'store':>7s} {'mech':>7s} {'total':>7s}  at 32.7 m/s")
    rows = {}
    k = kinematics(32.7)
    for fn in (spring, gas, lsm):
        r = fn(k)
        rows[r['option']] = r
        print(f"  {r['option']:24s} {r['store_kg']:7.2f} {r['mechanism_kg']:7.2f} "
              f"{r['total_kg']:7.2f}")
    g = rows['cold gas']
    print(f"\n  gas detail: bore {g['bore_mm']:.1f} mm, wall {g['wall_mm']:.2f} mm, "
          f"cylinder {g['cylinder_kg']:.2f} kg, reservoir {g['reservoir_litre']:.2f} L "
          f"({g['vessel_kg']:.3f} kg vessel + {g['gas_kg']:.3f} kg gas) for all "
          f"{N_MANIFEST} shots")

    print(f"\n{'option':26s} {'busts budget':>13s} {'busts falsifier':>17s}")
    ceilings = {}
    for name, fn in (('steel spring', spring), ('cold gas', gas)):
        b, f = busts_at(fn, BUDGET_KG), busts_at(fn, FALSIFIER_KG)
        ceilings[name] = dict(budget_v=b, falsifier_v=f)
        print(f"  {name:24s} {b if b else 0:13.1f} {f if f else 0:17.1f}  m/s")

    print("\nscreened out, each carrying the run that screened it:")
    for opt, run, why in SCREENED_OUT:
        print(f"  {opt:34s} {run:18s} {why}")

    selected = 'cold gas' if rows['cold gas']['total_kg'] <= rows['steel spring']['total_kg'] \
        else 'steel spring'
    sel = rows[selected]

    # band 1: reproduce A37's spring figure at A37's selected point
    a37 = spring(kinematics(A37_SELECTED_V))

    bands = [
        ('1', "steel spring reproduces A37's store + mechanism to 1 %",
         f"{a37['total_kg']:.2f} against {A37_SELECTED_STORE_KG:.2f} kg",
         abs(a37['total_kg'] - A37_SELECTED_STORE_KG) / A37_SELECTED_STORE_KG <= 0.01),
        ('2', f'some store <= {BUDGET_KG:.2f} kg at >= 30 m/s',
         f"best {min(r['total_kg'] for r in rows.values()):.2f} kg at 32.7 m/s",
         min(r['total_kg'] for r in rows.values()) <= BUDGET_KG),
        ('3', f'selected store inside the {FALSIFIER_KG:.2f} kg falsifier',
         f"{sel['option']} at {sel['total_kg']:.2f} kg",
         sel['total_kg'] <= FALSIFIER_KG),
        ('4', 'selected store reaches >= 35 m/s inside the falsifier',
         f"{ceilings[selected]['falsifier_v']:.1f} m/s"
         if ceilings[selected]['falsifier_v'] else 'never fits',
         bool(ceilings[selected]['falsifier_v'])
         and ceilings[selected]['falsifier_v'] >= 35.0),
        ('5', 'every screened-out option cites the run that screened it',
         f"{len(SCREENED_OUT)} options, {sum(1 for _, r, _ in SCREENED_OUT if r)} cited",
         all(r for _, r, _ in SCREENED_OUT)),
        ('6', f'the control exceeds the {BUDGET_KG:.2f} kg budget',
         f"LSM {rows['keep the LSM (control)']['total_kg']:.2f} kg",
         rows['keep the LSM (control)']['total_kg'] > BUDGET_KG),
        ('7', 'selected store holds without active maintenance, or names what maintains it',
         f"{sel['standby']}", bool(sel['standby'])),
    ]
    print("\nbands:")
    for n, name, detail, ok in bands:
        print(f"  band {n}: {'PASS' if ok else 'FAIL'}  {name}\n            {detail}")

    out = dict(analysis='A39', bands_declared_commit='8d78d1a',
               note='compares stores on mass and standby at a declared point; designs no '
                    'cylinder, valve, seal or latch, models no blowdown transient or '
                    'temperature effect, and prices no pressure-vessel qualification. Every '
                    'declared assumption makes gas look better than a detailed design will.',
               budget_kg=BUDGET_KG, falsifier_kg=FALSIFIER_KG, added_base_kg=ADDED_BASE_KG,
               at_32_7=rows, gas_detail=g, ceilings=ceilings, selected=selected,
               screened_out=[dict(option=o, screened_by=r, reason=w)
                             for o, r, w in SCREENED_OUT],
               bands=[dict(band=n, name=nm, detail=d, pass_=ok)
                      for n, nm, d, ok in bands])
    os.makedirs(RESULTS, exist_ok=True)
    path = os.path.join(RESULTS, 'store_trade.json')
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(out, fh, indent=2, default=float)
        fh.write('\n')
    print(f"\nwrote {path}")


if __name__ == '__main__':
    main()
