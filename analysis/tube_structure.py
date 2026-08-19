"""A59: the Gen6 drive tube as a beam, a column and a pressure vessel.

Bands declared in validation/A59_tube_structure.md at 6ff6dd5, BEFORE this file existed.

WHY THIS EXISTS
---------------
ADR-034 took the stroke from 2.18 m to 8.0 m and nothing structural was checked. A49 costed the
tube as "a plain cylinder at one wall thickness, no bending, no alignment tolerance, no dynamic
seal behaviour" and added that every omission flatters a long tube. build_gen6.py says in its own
docstring that the 1.0 mm wall "is set by handling and by carrying A38's 201.7 N cradle preload --
neither of which is modelled here."

So the wall thickness was chosen by two criteria nobody computed, on a tube that is now 8.0 m long
at 17.805 mm outside diameter. An aspect ratio of 449:1.

THREE THINGS AT ONCE
--------------------
    pressure vessel   hoop stress at the charge pressure     -- the only one precharged.py sizes
    beam              sag under handling and ascent load, and a bending mode
    column            the shot's axial reaction p0*A runs back through it

The design variable is SUPPORT SPACING, and each of the three demands a different one. This sweeps
it and reports what every criterion asks for.

THE MATERIAL IS NOT STATED ANYWHERE IN THIS REPOSITORY
------------------------------------------------------
A49 computes tube_kg at 2700 kg/m3. precharged.py sizes the chamber at 7800 with a 500 MPa
allowable. Nothing says which the tube is. Both are computed here; band 9 reports the difference
rather than resolving it by preference.

Geometry and the charge pressure are read from cad/parameters.json, not restated -- P84 is the
defect that comes from doing otherwise.

Run:  python3 analysis/tube_structure.py
"""
import json
import math
import os

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
PARAMS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                      'cad', 'parameters.json')

G = 9.81
SIGMA_ALLOW, SAFETY = 500e6, 2.0        # precharged.py
G_ASCENT = 25.0                         # sizing.py::retention_gate
TARGET_HZ = 70.0                        # sizing.py::track_first_mode
LAM2_PINNED, LAM2_FIXED = 9.87, 22.37   # sizing.py::track_first_mode

MATERIALS = {'aluminium': dict(E=69e9, rho=2700.0),    # sizing.py E_al, A49 RHO_AL
             'steel': dict(E=200e9, rho=7800.0)}       # precharged.py::chamber_kg

SPANS_M = (8.0, 6.0, 4.0, 3.0, 2.5, 2.0, 1.5, 1.25, 1.0, 0.8)


def geometry():
    """Bore, wall, stroke and charge pressure, read from the parameter file."""
    with open(PARAMS, encoding='utf-8') as f:
        g = json.load(f)['groups']
    d, s = g['gen6_drive'], g['gen6_store']
    bore, wall = d['bore_mm'] / 1e3, d['tube_wall_mm'] / 1e3
    r_o, r_i = bore / 2 + wall, bore / 2
    return dict(bore=bore, wall=wall, L=d['stroke_mm'] / 1e3, r_o=r_o, r_i=r_i,
                I=math.pi * (r_o ** 4 - r_i ** 4) / 4.0,
                A_metal=math.pi * (r_o ** 2 - r_i ** 2),
                A_bore=math.pi * r_i ** 2,
                p0=s['charge_pressure_bar'] * 1e5)


def hoop_stress(p0, r_i, wall):
    """Thin-wall hoop. The tube's only sized criterion until this run."""
    return p0 * r_i / wall


def first_mode(span, E, I, mu, lam2=LAM2_FIXED):
    return lam2 / (2.0 * math.pi * span ** 2) * math.sqrt(E * I / mu)


def euler_buckling(span, E, I, k=1.0):
    """Pinned-pinned between supports: the conservative end, and the honest one for a
    clamp that is not a moment connection."""
    return math.pi ** 2 * E * I / (k * span) ** 2


def udl_sag(span, w, E, I):
    """Fixed-fixed uniformly loaded, mid-span deflection. wL^4/384EI."""
    return w * span ** 4 / (384.0 * E * I)


def udl_bending_stress(span, w, r_o, I):
    """Fixed-fixed UDL: the maximum moment is at the supports, wL^2/12."""
    return (w * span ** 2 / 12.0) * r_o / I


def support_mass_kg(r_o):
    """Declared in the run sheet before this file existed, so it cannot be tuned afterwards.

    A split ring clamp of 3 mm wall and 12 mm width, a 40 x 12 x 3 mm standoff bracket to the
    rail, and two fasteners at 2 g. Aluminium. An estimate, and said to be one.
    """
    rho_al = MATERIALS['aluminium']['rho']
    ring_ro, ring_w, ring_t = r_o + 3e-3, 12e-3, 3e-3
    ring = math.pi * (ring_ro ** 2 - r_o ** 2) * ring_w * rho_al
    bracket = 40e-3 * 12e-3 * 3e-3 * rho_al
    return ring + bracket + 2 * 2e-3


def sweep(geo, mat):
    E, rho = mat['E'], mat['rho']
    mu = rho * geo['A_metal']
    rows = []
    for span in SPANS_M:
        w_1g = mu * G
        w_25g = mu * G_ASCENT * G
        rows.append(dict(
            span_m=span,
            f1_Hz=first_mode(span, E, geo['I'], mu),
            f1_pinned_Hz=first_mode(span, E, geo['I'], mu, LAM2_PINNED),
            P_cr_N=euler_buckling(span, E, geo['I']),
            sag_1g_mm=udl_sag(span, w_1g, E, geo['I']) * 1e3,
            sag_25g_mm=udl_sag(span, w_25g, E, geo['I']) * 1e3,
            bend_25g_MPa=udl_bending_stress(span, w_25g, geo['r_o'], geo['I']) / 1e6,
            n_supports=max(0, math.ceil(geo['L'] / span) - 1)))
    return rows, mu


def required_span(rows, key, limit, greater=True):
    """Loosest span in the sweep that still satisfies the criterion. None if none does."""
    ok = [r for r in rows if (r[key] >= limit if greater else r[key] <= limit)]
    return max((r['span_m'] for r in ok), default=None)


def main():
    geo = geometry()
    p_axial = geo['p0'] * geo['A_bore']
    hoop = hoop_stress(geo['p0'], geo['r_i'], geo['wall'])
    allow = SIGMA_ALLOW / SAFETY

    print(f"A59 drive tube structure. bore {geo['bore']*1e3:.3f} mm, wall {geo['wall']*1e3:.1f} mm, "
          f"L {geo['L']:.1f} m, OD {geo['r_o']*2e3:.3f} mm")
    print(f"  aspect ratio {geo['L']/(geo['r_o']*2):.0f}:1, second moment {geo['I']*1e12:.2f} mm^4")
    print(f"  charge {geo['p0']/1e5:.4f} bar -> axial reaction p0*A = {p_axial:.2f} N")
    print(f"  hoop {hoop/1e6:.2f} MPa against {allow/1e6:.0f} MPa allowable "
          f"({allow/hoop:.1f}x margin)\n")

    out_mats = {}
    for name, mat in MATERIALS.items():
        rows, mu = sweep(geo, mat)
        tube_kg = mu * geo['L']
        print(f"  {name}: {mu:.4f} kg/m, tube {tube_kg:.3f} kg over {geo['L']:.1f} m")
        print(f"  {'span':>6}{'supports':>10}{'f1 Hz':>10}{'P_cr N':>10}"
              f"{'sag 1g mm':>12}{'sag 25g mm':>12}{'bend 25g MPa':>14}")
        for r in rows:
            print(f"  {r['span_m']:6.2f}{r['n_supports']:10d}{r['f1_Hz']:10.2f}"
                  f"{r['P_cr_N']:10.1f}{r['sag_1g_mm']:12.3f}{r['sag_25g_mm']:12.2f}"
                  f"{r['bend_25g_MPa']:14.2f}")
        out_mats[name] = dict(rows=rows, mu_kg_m=mu, tube_kg=tube_kg)
        print()

    al = out_mats['aluminium']
    rows = al['rows']
    unsupported = next(r for r in rows if r['span_m'] == geo['L'])

    # the spacing each criterion demands, aluminium
    span_mode = required_span(rows, 'f1_Hz', TARGET_HZ)
    span_buckle = required_span(rows, 'P_cr_N', p_axial * SAFETY)
    span_bend = required_span(rows, 'bend_25g_MPa', allow / 1e6, greater=False)
    span_sag = required_span(rows, 'sag_1g_mm', 0.10 * geo['bore'] * 1e3, greater=False)
    governing = min(s for s in (span_mode, span_buckle, span_bend) if s is not None)
    sel = next(r for r in rows if r['span_m'] == governing)

    per_support = support_mass_kg(geo['r_o'])
    sup_total = per_support * sel['n_supports']

    print(f"  spacing demanded by each criterion:")
    print(f"    first mode >= {TARGET_HZ:.0f} Hz          {span_mode} m")
    print(f"    buckling with SF {SAFETY:.0f}            {span_buckle} m")
    print(f"    bending at {G_ASCENT:.0f} g              {span_bend} m")
    print(f"    1 g sag <= 10 % of bore       {span_sag} m")
    print(f"  governing (bands 2, 3, 7): {governing} m -> {sel['n_supports']} intermediate supports")
    print(f"  support {per_support*1e3:.1f} g each, {sup_total*1e3:.1f} g total")
    print(f"  tube + supports: aluminium {al['tube_kg']+sup_total:.3f} kg, "
          f"steel {out_mats['steel']['tube_kg']+sup_total:.3f} kg\n")

    bands = [
        ('1', f'hoop stress within {allow/1e6:.0f} MPa',
         f'{hoop/1e6:.2f} MPa, {allow/hoop:.1f}x margin', hoop <= allow),
        ('2', f'unsupported 8.0 m first mode >= {TARGET_HZ:.0f} Hz',
         f"{unsupported['f1_Hz']:.2f} Hz", unsupported['f1_Hz'] >= TARGET_HZ),
        ('3', f'unsupported Euler load > p0*A with SF {SAFETY:.0f}',
         f"{unsupported['P_cr_N']:.1f} N against {p_axial*SAFETY:.1f} N required",
         unsupported['P_cr_N'] > p_axial * SAFETY),
        ('4', 'governing support spacing >= 2.0 m',
         f'{governing} m, {sel["n_supports"]} supports', governing >= 2.0),
        ('5', 'total support mass <= 0.5 kg',
         f'{sup_total:.3f} kg', sup_total <= 0.5),
        ('6', 'tube + supports <= 2.0 kg (A49 band 7)',
         f"aluminium {al['tube_kg']+sup_total:.3f} kg, steel {out_mats['steel']['tube_kg']+sup_total:.3f} kg",
         al['tube_kg'] + sup_total <= 2.0),
        ('7', f'bending stress at {G_ASCENT:.0f} g within {allow/1e6:.0f} MPa at the selected spacing',
         f"{sel['bend_25g_MPa']:.2f} MPa", sel['bend_25g_MPa'] <= allow / 1e6),
        ('8', '1 g sag over the selected spacing <= 10 % of bore',
         f"{sel['sag_1g_mm']:.3f} mm against {0.10*geo['bore']*1e3:.3f} mm",
         sel['sag_1g_mm'] <= 0.10 * geo['bore'] * 1e3),
        ('9', 'REPORT: aluminium against steel',
         f"tube {al['tube_kg']:.3f} vs {out_mats['steel']['tube_kg']:.3f} kg; "
         f"unsupported mode {unsupported['f1_Hz']:.2f} vs "
         f"{next(r for r in out_mats['steel']['rows'] if r['span_m'] == geo['L'])['f1_Hz']:.2f} Hz",
         None),
    ]

    print('bands:')
    npass = 0
    for n, band, value, ok in bands:
        mark = 'REPORT' if ok is None else ('PASS' if ok else 'FAIL')
        npass += 1 if ok else 0
        print(f'  {n}  {mark:6} {band}\n        {value}')

    out = dict(analysis='A59', bands_declared_commit='6ff6dd5',
               geometry={k: v for k, v in geo.items()},
               aspect_ratio=geo['L'] / (geo['r_o'] * 2),
               axial_reaction_N=p_axial, hoop_stress_Pa=hoop, allowable_Pa=allow,
               materials=out_mats,
               spacing_demanded=dict(first_mode_m=span_mode, buckling_m=span_buckle,
                                     bending_25g_m=span_bend, sag_1g_m=span_sag),
               governing_span_m=governing, n_supports=sel['n_supports'],
               support_kg_each=per_support, support_kg_total=sup_total,
               tube_plus_supports_kg=dict(
                   aluminium=al['tube_kg'] + sup_total,
                   steel=out_mats['steel']['tube_kg'] + sup_total),
               bands=[dict(n=n, band=b, value=v, verdict=('REPORT' if o is None else
                                                          ('PASS' if o else 'FAIL')))
                      for n, b, v, o in bands])
    path = os.path.join(RESULTS, 'tube_structure.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, default=float)
        f.write('\n')
    print(f'\nwrote {path}')


if __name__ == '__main__':
    main()
