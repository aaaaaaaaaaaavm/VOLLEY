"""
VOLLEY | Magazine density: the only lever A35 left on kill criterion 1.

WHY THIS EXISTS
---------------
A35 attributed every kilogram to the requirement causing it and found that 49.23 kg --
58.2 % of dry mass -- survives every deletion of every requirement in all 64 corners.
At twelve satellites that is 4.10 kg each, still twice the criterion. No architecture
change closes it.

The surviving mass is per MACHINE. The one lever that reaches the threshold is the
divisor, and it sits outside the physics: the same mass over more satellites. It has
never been studied. This asks whether it is real.

Bands declared in validation/A36_magazine_density.md at 39c0d21, BEFORE this file existed.

Provenance: model output. Mass attribution is READ from constraint_ledger.py's C6 tagging
rather than restated, so there is one source and not two. Geometry is read from
payload_family.py, which reads cad/parameters.json.
"""
import json
import math
import os

import constraint_ledger as cl
import payload_family as pf

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

N_REF = pf.CASSETTES * pf.SATS_PER_CASSETTE      # the manifest that exists
TARGET_KG = 2.0                                  # kill criterion 1, docs/KILL_CRITERIA.md
SKIN_EXPONENT = 2.0 / 3.0                        # surface of a growing volume; AN ASSUMPTION
CADENCE_S = 1200.0                               # ADR-020

# Declared in the run sheet before this file existed. `skin` is everything whose area grows
# with the magazine; everything not named here is fixed.
SKIN_PREFIXES = ('Panels / closeouts', 'Enclosure / radiator')


def split():
    """Dry mass as (fixed, skin_at_reference, per_satellite).

    Per-satellite items are exactly those A35 tagged as driven by C6 -- the containment.
    Reading the ledger rather than re-listing them means a change to the attribution
    propagates here instead of forking, which is the P53 failure in miniature.
    """
    rows, unattributed = cl.ledger()
    assert not unattributed, unattributed
    per_sat_total = sum(r['kg'] for r in rows
                        if 'C6' in r['full'] or 'C6' in r['partial'])
    skin = sum(r['kg'] for r in rows if r['part'].startswith(SKIN_PREFIXES))
    total = sum(r['kg'] for r in rows)
    return total - per_sat_total - skin, skin, per_sat_total / N_REF


def dry_at(n, fixed, skin_ref, per_sat):
    return fixed + skin_ref * (n / N_REF) ** SKIN_EXPONENT + per_sat * n


def kg_per_sat(n, *args):
    return dry_at(n, *args) / n


def arrangements(n):
    """Every way of splitting n satellites into equal cassettes, with the envelope each gives.

    The cassettes sit TRANSVERSELY to the track, so slots stack along z and cassettes sit
    side by side along y. Neither grows the track axis, which is band 5's whole point.
    """
    out = []
    for cassettes in range(1, n + 1):
        if n % cassettes:
            continue
        per = n // cassettes
        out.append(dict(cassettes=cassettes, per_cassette=per,
                        stack_z_mm=per * pf.PITCH_Z,
                        width_y_mm=cassettes * pf.CASSETTE_WID_Y,
                        length_x_mm=pf.CASSETTE_LEN_X))
    return out


def main():
    fixed, skin_ref, per_sat = split()
    args = (fixed, skin_ref, per_sat)
    track_mm = 1500.0                     # mm, motor_model.TRACK; the track axis

    print(f"mass split at N = {N_REF}:")
    print(f"  fixed              {fixed:7.2f} kg")
    print(f"  magazine skin      {skin_ref:7.2f} kg   (scales as N^{SKIN_EXPONENT:.3f})")
    print(f"  per satellite      {per_sat:7.3f} kg   (A35's C6 containment)")
    print(f"  dry, modelled      {dry_at(N_REF, *args):7.2f} kg")

    print(f"\n{'N':>4s} {'dry kg':>8s} {'kg/sat':>8s} {'stack z':>9s} {'width y':>9s} "
          f"{'campaign h':>11s}")
    curve = []
    for n in (6, 12, 18, 24, 30, 36, 48, 60, 96, 240, 1200):
        best = min((a for a in arrangements(n)
                    if a['stack_z_mm'] <= track_mm and a['width_y_mm'] <= track_mm),
                   key=lambda a: max(a['stack_z_mm'], a['width_y_mm']), default=None)
        row = dict(n=n, dry_kg=dry_at(n, *args), kg_per_sat=kg_per_sat(n, *args),
                   campaign_h=n * CADENCE_S / 3600.0,
                   arrangement=best)
        curve.append(row)
        z = f"{best['stack_z_mm']:.0f}" if best else '--'
        y = f"{best['width_y_mm']:.0f}" if best else '--'
        print(f"{n:4d} {row['dry_kg']:8.2f} {row['kg_per_sat']:8.3f} {z:>9s} {y:>9s} "
              f"{row['campaign_h']:11.1f}")

    # The N -> infinity limit. kg/sat = fixed/N + skin_ref*N^(-1/3)*k + per_sat, and both
    # leading terms vanish, so the limit is the per-satellite containment alone.
    asymptote = per_sat
    n_reaching = next((n for n in range(N_REF, 2001)
                       if kg_per_sat(n, *args) <= TARGET_KG), None)

    ref_kg = next(c['kg_per_satellite'] for c in
                  json.load(open(os.path.join(RESULTS, 'payload_family.json')),
                            )['classes'] if c['tag'] == '3U CubeSat')
    model_ref = kg_per_sat(N_REF, *args)

    a24 = [a for a in arrangements(24)
           if a['stack_z_mm'] <= track_mm and a['width_y_mm'] <= track_mm]
    geometry_ok = all(a['length_x_mm'] <= pf.CASSETTE_LEN_X + 1e-9 for a in arrangements(24))

    print(f"\n  N -> infinity limit        {asymptote:.3f} kg/satellite")
    print(f"  first N at or below {TARGET_KG:.1f} kg   N = {n_reaching}")
    print(f"  reference check            model {model_ref:.3f} against "
          f"payload_family {ref_kg:.3f} kg")
    print(f"  recoil, N = 24             "
          f"{24 * 4.0 * __import__('motor_model').operating_point()['v_exit']:.0f} N.s "
          f"(REPORT: doubles by construction)")

    bands = [
        ('1', 'model reproduces payload_family at N = 12, within 1 %',
         f"{model_ref:.3f} against {ref_kg:.3f} kg",
         abs(model_ref - ref_kg) / ref_kg <= 0.01),
        ('2', 'fixed + skin + N x per-satellite reproduces dry mass, to 0.01 kg',
         f"{dry_at(N_REF, *args):.4f} against {sum(r['kg'] for r in cl.ledger()[0]):.4f}",
         abs(dry_at(N_REF, *args) - sum(r['kg'] for r in cl.ledger()[0])) <= 0.01),
        ('3', f'N -> infinity limit <= {TARGET_KG} kg/satellite',
         f"{asymptote:.3f} kg", asymptote <= TARGET_KG),
        ('4', f'kg/satellite <= {TARGET_KG} at N <= 30',
         f"first at N = {n_reaching}", n_reaching is not None and n_reaching <= 30),
        ('5', 'N = 24 arrangement exists: track axis unchanged, transverse <= track length',
         f"{len(a24)} arrangement(s), best "
         f"{min(max(a['stack_z_mm'], a['width_y_mm']) for a in a24):.0f} mm"
         if a24 else 'none', bool(a24)),
        ('6', 'no arrangement violates the 166 mm section, 104 mm pitch or 340.5 mm cell',
         'cassette length unchanged in every arrangement', geometry_ok),
        ('7', 'N = 24 campaign completes in <= 12 h at the 1200 s cadence',
         f"{24 * CADENCE_S / 3600.0:.1f} h", 24 * CADENCE_S / 3600.0 <= 12.0),
    ]
    print("\nbands:")
    for n, name, detail, ok in bands:
        print(f"  band {n}: {'PASS' if ok else 'FAIL'}  {name}\n            {detail}")

    out = dict(analysis='A36', bands_declared_commit='39c0d21',
               note='reports mass and envelope only; indexing reach, follower travel, '
                    'stack structural depth and doubled ascent loads are NOT priced, and '
                    'every omission makes this optimistic',
               n_reference=N_REF, target_kg=TARGET_KG, skin_exponent=SKIN_EXPONENT,
               fixed_kg=fixed, skin_kg_at_reference=skin_ref, per_satellite_kg=per_sat,
               asymptote_kg_per_satellite=asymptote, first_n_at_target=n_reaching,
               curve=curve,
               bands=[dict(band=n, name=name, detail=d, pass_=ok)
                      for n, name, d, ok in bands])
    os.makedirs(RESULTS, exist_ok=True)
    path = os.path.join(RESULTS, 'magazine_density.json')
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(out, fh, indent=2, default=float)
        fh.write('\n')
    print(f"\nwrote {path}")


if __name__ == '__main__':
    main()
