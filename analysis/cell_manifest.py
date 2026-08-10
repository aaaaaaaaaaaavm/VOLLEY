"""
VOLLEY | The fixed-cell manifest: the payload ladder as a design rather than a volume ratio.

WHY THIS EXISTS
---------------
`payload_family.py` answers "how much room is there" with a volume ratio calibrated so the 3U
case returns the twelve the machine is laid out for. It is careful to say what it is not:

    "No cassette, cradle or gate exists for any class except 3U ... The counts below say how
     much room there is, not that anything has been designed to use it."

So the ladder that currently answers KILL_CRITERIA threat 1 -- 1U at 1.913 kg per satellite
against a ~2 kg threshold -- is arithmetic. This script tests an actual architecture instead.

THE FIXED CELL
--------------
One cell geometry, sized to the 3U slot the machine already has: 340.5 mm along x, 100 x 100 in
section, on the existing 104 mm pitch, twelve cells across two cassettes. Smaller classes fly in
INSERTS -- transverse dividers subdividing a cell along x, using the cell's own walls in y and z.
One pitch, one gate, one cradle, one qualification campaign. Mixing at ground integration.

The cost, stated because it is the whole trade: velocity is programmable per CELL, not per
satellite. At 3U, cell = satellite and nothing is lost. Below 3U it is a real reduction, and it
creates a problem the machine does not have today -- satellites sharing a cell leave on the same
shot at the same velocity, so they never separate from each other.

Bands declared in validation/A24_fixed_cell_manifest.md at 5fdc978, BEFORE this file existed.

Provenance: model output, not independently re-derived.
"""
import json
import math
import os

import motor_model as mm
import payload_family as pf

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

# --- the cell, from cad/parameters.json groups.magazine ------------------------
CELL_LEN_X = 340.5              # mm, the 3U slot length
CELL_SEC_Y = 100.0              # mm, section. Set by the 166 mm cassette width less structure
CELL_SEC_Z = 100.0              # mm, section. Set by the 104 mm stack pitch less the septum
CELLS_TOTAL = 12                # 6 per cassette x 2

DIVIDER_MM = 1.5                # insert divider wall, transverse, between units along x
DEPLOYER_DRY_KG = pf.DEPLOYER_DRY_KG

# --- intra-cell separation ------------------------------------------------------
SEP_TARGET_M = 10.0             # m, the separation to open
SEP_TIME_S = 120.0              # s, within which to open it
V_EXIT_3U = 16.388              # m/s, the frozen baseline shot


def fit_in_cell(box):
    """How many of `box` fit in one cell, and in which orientation.

    Tries every axis permutation. The cell's y and z are hard limits set by existing
    structure -- the cassette width and the stack pitch -- so a class larger than the
    section in two axes cannot be accommodated at all, whatever its volume says. Dividers
    are charged along x only: the insert subdivides the cell lengthwise and uses the cell's
    own walls in section, which is the point of a fixed cell.
    """
    best = None
    for perm in ((0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)):
        lx, ly, lz = box[perm[0]], box[perm[1]], box[perm[2]]
        ny = int(CELL_SEC_Y // ly)
        nz = int(CELL_SEC_Z // lz)
        if ny < 1 or nz < 1:
            continue
        # n units along x need (n-1) dividers between them.
        nx = 0
        while (nx + 1) * lx + nx * DIVIDER_MM <= CELL_LEN_X:
            nx += 1
        if nx < 1:
            continue
        n = nx * ny * nz
        if best is None or n > best['n_per_cell']:
            best = dict(n_per_cell=n, nx=nx, ny=ny, nz=nz,
                        oriented_mm=[lx, ly, lz])
    return best


def separation_differential(n_per_cell):
    """Differential velocity to open SEP_TARGET_M between cell-mates within SEP_TIME_S.

    Satellites sharing a cell exit nose-to-tail on the same shot at the same commanded
    velocity, so their designed differential is ZERO and the gap between them never grows.
    The worst pair is the two furthest apart in the release order, which must open the full
    target between them; adjacent pairs open proportionally less.
    """
    if n_per_cell < 2:
        return None
    return SEP_TARGET_M / SEP_TIME_S


def shim_mechanism(n_per_cell, m_sat):
    """A momentum-neutral intra-cell shim, and what it does to the cell's mean velocity.

    The mechanism has to push cell-mates apart WITHOUT pushing on the sled: anything
    reacting into the sled perturbs the primary shot, and v_exit is a frozen baseline
    value. A compressed shim between adjacent units is internal to the cell, so the
    cell's total momentum is unchanged and the MEAN exit velocity is unchanged to first
    order -- the shim redistributes velocity within the cell rather than adding any.

    Returned: the per-unit velocity spread the shim must produce, and the change in the
    cell's mean, which for an internal mechanism is identically zero. The residual is the
    second-order term from the shim's own mass leaving with one side, carried explicitly
    rather than assumed away.
    """
    if n_per_cell < 2:
        return None
    dv = separation_differential(n_per_cell)
    # Symmetric split about the mean: the trailing unit slows by dv/2, the leading gains dv/2,
    # for a two-unit cell. For n units the spread is dv across the train.
    spread = dv
    m_shim = 0.010          # kg, a 10 g compressed shim per interface -- an assumption, flagged
    # Second-order: the shim mass departs with one side, shifting the cell's mean by the
    # momentum it carries divided by the cell's total payload mass.
    m_cell = n_per_cell * m_sat
    dv_mean = (m_shim * (n_per_cell - 1) * spread / 2.0) / m_cell if m_cell else 0.0
    return dict(spread_m_s=spread, shim_kg=m_shim,
                mean_shift_m_s=dv_mean,
                mean_shift_pct=100.0 * dv_mean / V_EXIT_3U)


def manifest():
    volumetric = {r['tag']: r['n_per_load'] for r in pf.family()['classes']}
    rows = []
    for tag, m_sat, box, note in pf.CLASSES:
        fit = fit_in_cell(box)
        if fit is None:
            rows.append(dict(tag=tag, mass_kg=m_sat, box_mm=list(box),
                             accommodated=False,
                             reason=f"exceeds the {CELL_SEC_Y:g} x {CELL_SEC_Z:g} mm cell "
                                    f"section in two axes; the section is fixed by the "
                                    f"cassette width and the stack pitch",
                             n_per_cell=0, cells_per_sat=None, n_per_load=0,
                             kg_per_satellite=None,
                             volumetric_n=volumetric.get(tag),
                             sep=None, shim=None, note=note))
            continue
        n_cell = fit['n_per_cell']
        n_load = n_cell * CELLS_TOTAL
        rows.append(dict(
            tag=tag, mass_kg=m_sat, box_mm=list(box), accommodated=True,
            n_per_cell=n_cell, cells_per_sat=round(1.0 / n_cell, 4),
            arrangement=f"{fit['nx']} x {fit['ny']} x {fit['nz']}",
            oriented_mm=fit['oriented_mm'],
            n_per_load=n_load,
            kg_per_satellite=round(DEPLOYER_DRY_KG / n_load, 3),
            volumetric_n=volumetric.get(tag),
            sep=separation_differential(n_cell),
            shim=shim_mechanism(n_cell, m_sat),
            note=note))
    return rows


def multi_cell(box):
    """Classes larger than one cell: how many whole cells they consume, or a refusal.

    A class is never allowed to consume a fractional cell. If it does not fit the section in
    any orientation even when stacked across adjacent cells in z, it is NOT ACCOMMODATED --
    the cassette is 166 mm wide, so there is no second cell in y to grow into.
    """
    for perm in ((0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)):
        lx, ly, lz = box[perm[0]], box[perm[1]], box[perm[2]]
        if lx > CELL_LEN_X or ly > CELL_SEC_Y:
            continue                     # y cannot grow: no second cell sideways
        cells_z = math.ceil(lz / CELL_SEC_Z)
        if cells_z >= 1:
            return dict(cells=cells_z, oriented_mm=[lx, ly, lz])
    return None


def bands(rows):
    out = []

    # Band 1: reproduces the machine that exists.
    ref = next(r for r in rows if r['tag'] == '3U CubeSat')
    b1 = (ref['n_per_load'] == 12
          and abs(ref['kg_per_satellite'] - 6.375) / 6.375 <= 0.01)
    out.append(('1', 'cell model reproduces the 3U machine',
                f"{ref['n_per_load']} per load, {ref['kg_per_satellite']} kg/sat "
                f"(against 12 and 6.375)", b1))

    # Band 2: never more optimistic than the free volume ratio.
    worse = [r['tag'] for r in rows
             if r['accommodated'] and r['volumetric_n'] is not None
             and r['n_per_load'] > r['volumetric_n']]
    out.append(('2', 'designed cell never beats the volume ratio',
                'all classes at or below' if not worse else f"EXCEEDS on {', '.join(worse)}",
                not worse))

    # Band 3: does a designed ladder close threat 1?
    cand = ['ThinSat', 'PocketQube 1P', 'PocketQube 3P', 'TubeSat', '1U CubeSat']
    crossed = [(r['tag'], r['kg_per_satellite']) for r in rows
               if r['tag'] in cand and r['accommodated']
               and r['kg_per_satellite'] is not None and r['kg_per_satellite'] <= 2.0]
    out.append(('3', 'a designed class closes kill criterion 1 (<= 2.0 kg/sat)',
                ', '.join(f"{t} {v}" for t, v in crossed) if crossed
                else 'NO class crosses 2.0 kg',
                bool(crossed)))

    # Band 4: whole cells only, honest refusals.
    frac = [r['tag'] for r in rows
            if r['accommodated'] and r['n_per_cell'] < 1]
    refused = [r['tag'] for r in rows if not r['accommodated']]
    out.append(('4', 'whole cells only, refusals printed as refusals',
                f"{len(refused)} refused ({', '.join(refused) or 'none'}), "
                f"0 fractional" if not frac else f"FRACTIONAL on {', '.join(frac)}",
                not frac))

    # Band 5: cell-mates can separate at <= 1 % of exit velocity.
    lim = 0.01 * V_EXIT_3U
    shared = [r for r in rows if r['accommodated'] and r['n_per_cell'] > 1]
    over = [r['tag'] for r in shared if r['sep'] > lim]
    out.append(('5', f'intra-cell differential <= 1 % of v_exit ({lim:.3f} m/s)',
                f"{len(shared)} classes share cells, required {shared[0]['sep']:.4f} m/s"
                if shared else 'no class shares a cell',
                not over))

    # Band 6: the mechanism does not corrupt the shot.
    lim6 = 0.005 * V_EXIT_3U
    bad = [r['tag'] for r in shared if r['shim']['mean_shift_m_s'] > lim6]
    worst = max((r['shim']['mean_shift_m_s'] for r in shared), default=0.0)
    out.append(('6', f'mechanism shifts cell mean by <= 0.5 % ({lim6:.3f} m/s)',
                f"worst {worst:.2e} m/s", not bad))
    return out


if __name__ == '__main__':
    rows = manifest()
    print(f"fixed cell: {CELL_LEN_X:g} x {CELL_SEC_Y:g} x {CELL_SEC_Z:g} mm, "
          f"{CELLS_TOTAL} cells, {DIVIDER_MM:g} mm dividers along x\n")
    print(f"{'class':22s} {'per cell':>9s} {'per load':>9s} {'vol.':>6s} "
          f"{'kg/sat':>8s}  arrangement")
    for r in rows:
        if not r['accommodated']:
            print(f"{r['tag']:22s} {'--':>9s} {'NOT ACCOMMODATED':>9s}")
            continue
        print(f"{r['tag']:22s} {r['n_per_cell']:9d} {r['n_per_load']:9d} "
              f"{r['volumetric_n']:6d} {r['kg_per_satellite']:8.3f}  {r['arrangement']}")

    print("\nlarger than one cell:")
    for tag, _m, box, _n in pf.CLASSES:
        if tag not in ('6U CubeSat', '12U CubeSat'):
            continue
        mc = multi_cell(box)
        if mc is None:
            print(f"  {tag:20s} NOT ACCOMMODATED -- exceeds the cell section in y, and the "
                  f"cassette has no second cell sideways")
        else:
            n = CELLS_TOTAL // mc['cells']
            print(f"  {tag:20s} {mc['cells']} whole cells -> {n} per load, "
                  f"{DEPLOYER_DRY_KG / n:.3f} kg/sat")

    print("\nbands:")
    res = bands(rows)
    for num, name, detail, ok in res:
        print(f"  band {num}: {'PASS' if ok else 'FAIL'}  {name}\n            {detail}")

    os.makedirs(RESULTS, exist_ok=True)
    payload = dict(
        cell_mm=[CELL_LEN_X, CELL_SEC_Y, CELL_SEC_Z], cells_total=CELLS_TOTAL,
        divider_mm=DIVIDER_MM, deployer_dry_kg=DEPLOYER_DRY_KG,
        sep_target_m=SEP_TARGET_M, sep_time_s=SEP_TIME_S,
        classes=rows,
        bands=[dict(band=n, name=nm, detail=d, pass_=ok) for n, nm, d, ok in res])
    json.dump(payload, open(os.path.join(RESULTS, 'cell_manifest.json'), 'w'), indent=2)
    print("\n-> results/cell_manifest.json")
