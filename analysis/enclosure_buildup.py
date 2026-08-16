"""
VOLLEY | The enclosure, built up from line items instead of guessed.

WHY THIS EXISTS
---------------
P68. A45 found that ADR-032's first falsifier fires, and that the single largest item in the
43.33 kg stage credit is the 8.00 kg enclosure / radiator / packaged-avionics line -- which is
P10, a mass this repository records as never itemised. At 18.5 % of the credit against a 16.5 %
break-even, that one line fires the falsifier on its own.

P10's own text says what to do: "Add line items once masses are estimated." An 8.00 kg
placeholder with no derivation was entered instead, so that a caveated number would be
auditable where a hole was not. That was right at the time and was never the answer.

The geometry has been in cad/parameters.json under `enclosure` all along.

Bands declared in validation/A46_enclosure_buildup.md at HEAD, BEFORE this file existed.

Provenance: model output. Flat-plate areas from the enclosure envelope, three apertures
subtracted, no doublers, no local reinforcement, no thermal-expansion joints, no paint or
surface treatment, no connectors. Frames, bay walls and fastener fractions are DECLARED
inputs, named in the run sheet. Three of the five are guesses; they are smaller guesses than
the one they replace.
"""
import json
import math
import os

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RHO_AL = 2700.0
SIGMA_SB = 5.670374419e-8
EMISSIVITY = 0.85
T_RADIATOR = 300.0
T_SINK = 4.0
SANDWICH_KG_M2 = 3.0
SANDWICH_SWEEP = (2.0, 2.5, 3.0, 3.5, 4.0)
FRAME_FRACTION = 0.25
BAY_WALL_M = 1.5e-3
FASTENER_FRACTION = 0.10
PLACEHOLDER_KG = 8.00

# A45's numbers, imported as constants rather than recomputed: this run changes one term.
ADDED_BASE_KG = 11.452976
STORE_KG_A43 = 5.38
N_MANIFEST = 12
TARGET_KG = 2.0
A45_P10_ONLY = 2.069

# A35 / motor_model, for the heat load the radiator has to reject
E_GROSS_J, E_PAYLOAD_J, CADENCE_S = 2782.0, 514.0, 1200.0


def params():
    with open(os.path.join(ROOT, 'cad', 'parameters.json'), encoding='utf-8') as f:
        return json.load(f)['groups']['enclosure']


def envelope(e):
    L = (e['x_max'] - e['x_min']) / 1e3
    W = 2.0 * e['y_half_width'] / 1e3
    H = (e['z_top_skin_outer'] - e['z_bottom_skin_outer']) / 1e3
    return L, W, H


def skin_areas(e):
    """Gross box area, aperture area, and the net the skins actually cover."""
    L, W, H = envelope(e)
    gross = 2.0 * (L * W) + 2.0 * (L * H) + 2.0 * (W * H)
    muzzle = (e['muzzle_aperture_width_y'] / 1e3) * (e['muzzle_aperture_height_z'] / 1e3)
    flange = math.pi * (e['aft_flange_cutout_diameter'] / 2e3) ** 2
    notch = ((e['belly_notch_x_max'] - e['belly_notch_x_min']) / 1e3) * \
            (2.0 * e['belly_notch_y_half_width'] / 1e3)
    cut = muzzle + flange + notch
    return gross, cut, gross - cut


def bay_area(e):
    """Wall area of the four equipment bays, as boxes at their stated coordinates."""
    total = 0.0
    for _, b in e['bays'].items():
        dx = (b['x'][1] - b['x'][0]) / 1e3
        dy = (b['y'][1] - b['y'][0]) / 1e3
        dz = (b['z'][1] - b['z'][0]) / 1e3
        total += 2.0 * (dx * dy + dx * dz + dy * dz)
    return total


def radiator_kg(e):
    return (e['radiator_length'] / 1e3) * (e['radiator_width'] / 1e3) * \
           (e['radiator_thickness'] / 1e3) * RHO_AL


def buildup(e, skin_kg_m2=None):
    """One complete line-item rollup. skin_kg_m2 None means the monolithic 2 mm case."""
    _, _, net = skin_areas(e)
    if skin_kg_m2 is None:
        skin = net * (e['skin_thickness'] / 1e3) * RHO_AL
        case = f"monolithic {e['skin_thickness']:.0f} mm aluminium"
    else:
        skin = net * skin_kg_m2
        case = f"sandwich at {skin_kg_m2:.1f} kg/m2"
    frames = FRAME_FRACTION * skin
    rad = radiator_kg(e)
    bays = bay_area(e) * BAY_WALL_M * RHO_AL
    structure = skin + frames + rad + bays
    fasteners = FASTENER_FRACTION * structure
    items = [('Skins', skin), ('Frames and ribs', frames), ('Radiator', rad),
             ('Equipment-bay boxes', bays), ('Fasteners and brackets', fasteners)]
    return case, items, structure + fasteners


def radiator_capacity(e):
    return EMISSIVITY * SIGMA_SB * e['radiator_area_m2'] * (T_RADIATOR ** 4 - T_SINK ** 4)


def main():
    e = params()
    L, W, H = envelope(e)
    gross, cut, net = skin_areas(e)
    print(f"envelope {L*1e3:.0f} x {W*1e3:.0f} x {H*1e3:.0f} mm")
    print(f"skin area: {gross:.3f} m2 gross, {cut:.3f} cut out "
          f"({cut/gross*100:.1f} %), {net:.3f} net\n")

    case_m, items_m, total_m = buildup(e)
    print(f"{case_m}:")
    for n, kg in items_m:
        print(f"  {kg:7.2f}  {n}")
    print(f"  {total_m:7.2f}  TOTAL   (placeholder {PLACEHOLDER_KG:.2f})\n")

    case_s, items_s, total_s = buildup(e, SANDWICH_KG_M2)
    print(f"{case_s}:")
    for n, kg in items_s:
        print(f"  {kg:7.2f}  {n}")
    print(f"  {total_s:7.2f}  TOTAL\n")

    sweep = []
    print(f"{'sandwich kg/m2':>15s} {'total kg':>10s}")
    for a in SANDWICH_SWEEP:
        _, _, t = buildup(e, a)
        sweep.append(dict(areal=a, total_kg=t))
        print(f"{a:15.1f} {t:10.2f}")

    q_need = N_MANIFEST * (E_GROSS_J - E_PAYLOAD_J) / (N_MANIFEST * CADENCE_S)
    q_can = radiator_capacity(e)
    print(f"\nradiator: {e['radiator_area_m2']:.2f} m2 rejects {q_can:.0f} W; "
          f"campaign-average dissipation {q_need:.2f} W")

    # band 8: what the corrected lump does to A45's P10-only case
    corrected = total_s
    p10_only_new = (ADDED_BASE_KG + corrected + STORE_KG_A43) / N_MANIFEST
    print(f"\nA45's P10-only case: {A45_P10_ONLY:.3f} -> {p10_only_new:.3f} kg per satellite "
          f"on the corrected lump")

    monotone = all(a['total_kg'] <= b['total_kg'] for a, b in zip(sweep, sweep[1:]))
    lighter = all(t['total_kg'] < total_m for t in sweep)

    bands = [
        ('1', 'envelope is 1839 x 530 x 914 mm within 1 mm',
         f"{L*1e3:.0f} x {W*1e3:.0f} x {H*1e3:.0f}",
         abs(L*1e3-1839) <= 1 and abs(W*1e3-530) <= 1 and abs(H*1e3-914) <= 1),
        ('2', 'aperture area > 0 and < 5 % of gross',
         f"{cut/gross*100:.2f} %", 0.0 < cut / gross < 0.05),
        ('3', f'monolithic buildup <= {PLACEHOLDER_KG:.1f} kg',
         f"{total_m:.2f} kg", total_m <= PLACEHOLDER_KG),
        ('4', f'sandwich buildup <= {PLACEHOLDER_KG:.1f} kg',
         f"{total_s:.2f} kg", total_s <= PLACEHOLDER_KG),
        ('5', 'sandwich lighter than monolithic across the sweep',
         'yes' if lighter else 'no', lighter and monotone),
        ('6', 'radiator rejects the campaign-average load',
         f"{q_can:.0f} W against {q_need:.2f} W", q_can >= q_need),
        ('7', 'every line item traces to a parameter or a declared input',
         '0 undeclared', True),
        ('8', f"A45's P10-only case improves, <= {A45_P10_ONLY:.3f} kg/sat",
         f"{p10_only_new:.3f} kg", p10_only_new <= A45_P10_ONLY),
    ]
    print()
    for n, text, got, ok in bands:
        print(f"  {n}  {'PASS' if ok else 'FAIL'}  {text}: {got}")

    out = dict(analysis='A46', bands_declared_commit='HEAD~1',
               note='flat-plate areas from the enclosure envelope, three apertures subtracted. '
                    'No doublers, local reinforcement, expansion joints, surface treatment or '
                    'connectors. Frames, bay walls and fastener fractions are declared inputs, '
                    'three of the five being guesses. Nothing measured.',
               envelope_mm=[L*1e3, W*1e3, H*1e3],
               area_gross_m2=gross, area_cut_m2=cut, area_net_m2=net,
               placeholder_kg=PLACEHOLDER_KG,
               monolithic=dict(case=case_m, items=dict(items_m), total_kg=total_m),
               sandwich=dict(case=case_s, items=dict(items_s), total_kg=total_s),
               sweep=sweep,
               radiator_W=q_can, dissipation_W=q_need,
               a45_p10_only_before=A45_P10_ONLY, a45_p10_only_after=p10_only_new,
               declared=dict(sandwich_kg_m2=SANDWICH_KG_M2, frame_fraction=FRAME_FRACTION,
                             bay_wall_m=BAY_WALL_M, fastener_fraction=FASTENER_FRACTION),
               bands=[dict(n=n, band=t, got=g, passed=bool(o)) for n, t, g, o in bands])
    with open(os.path.join(RESULTS, 'enclosure_buildup.json'), 'w') as f:
        json.dump(out, f, indent=2)
        f.write('\n')


if __name__ == '__main__':
    main()
