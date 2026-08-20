"""A64: the pulse store, priced against pulsed-power capacitor technology.

Bands declared in validation/A64_pulse_store_technology.md at HEAD~1, BEFORE this file existed.

WHY THIS EXISTS
---------------
A54 priced the trim store as an EDLC bank at 23.44-37.36 kg and left one route open, stated as a
required number rather than a comparison it could not honestly make: any store fitting inside the
1.2328 kg section must deliver 23.20 kW/kg, and NEEDS SOURCE for a film or pulse capacitor.

That source now exists: published pulsed-power literature gives millisecond-discharge capacitor
energy densities of 1.9-2.68 J/cm3 at roughly unit density, with metallised polypropylene
construction and extended-foil or bifilar electrodes for very low ESR and ESL.

THE FORM A54'S CORRECTION ESTABLISHED
-------------------------------------
    m >= 0.5 * (ESR x C) * P / (f * specific_energy)

with the bus voltage cancelling exactly. A technology change enters through two terms only:
ESR x C, and specific energy. Film moves the first by orders of magnitude, which should flip the
store from power-limited to energy-limited.

No product, series or supplier is named. The switch and the conductors are still unpriced, so
every mass here remains a LOWER BOUND.

Run:  python3 analysis/pulse_store_tech.py
"""
import json
import math
import os

import pulse_chain as pcx

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

LOSS_FRAC = 0.10
SPEC_E_PULSE = (2000.0, 2680.0)          # J/kg, published pulsed-power range
SPEC_E_EDLC = 0.5 * 5.94 * 96.0 ** 2 / 6.50
ESR_C_FILM = (1e-6, 1e-5, 1e-4, 1e-3)    # s, swept; typical metallised PP is nearer 1e-7
ESR_C_EDLC = (pcx.ESR_C_LO, pcx.ESR_C_HI)
PER_SAT_BASE = 1.296
SECTION_KG = 1.2328
N_MANIFEST = 12


def store_kg(esr_c, peak_W, delivered_J, spec_e, f=LOSS_FRAC):
    """The store must hold enough to SOURCE the power and enough to DELIVER the energy.

    Power term: E >= 0.5 * (ESR x C) * P / f, from A54's correction. Voltage cancels.
    Energy term: E >= the energy actually delivered.
    Whichever binds sets the mass.
    """
    e_power = 0.5 * esr_c * peak_W / f
    e_needed = max(e_power, delivered_J)
    return dict(esr_c_s=esr_c, spec_e_J_kg=spec_e, e_power_J=e_power,
                e_binding_J=e_needed, limited_by='power' if e_power > delivered_J else 'energy',
                mass_kg=e_needed / spec_e,
                specific_power_W_kg=peak_W / (e_needed / spec_e),
                over_delivered=e_needed / delivered_J)


def main():
    req = pcx.requirement()
    P, E = req['peak_W'], req['energy_J']
    print(f"A64 pulse store technology. {E:.2f} J at {P:.0f} W, into a {SECTION_KG:.4f} kg section\n")

    edlc = [store_kg(c, P, E, SPEC_E_EDLC) for c in ESR_C_EDLC]
    print(f"  EDLC, for the check against A54: "
          f"{edlc[0]['mass_kg']:.2f}-{edlc[1]['mass_kg']:.2f} kg "
          f"({edlc[0]['limited_by']}-limited, {edlc[0]['over_delivered']:.0f}x over-delivered)\n")

    print(f"  {'ESRxC s':>10}{'spec E':>9}{'E power J':>12}{'binds':>9}"
          f"{'store kg':>10}{'kW/kg':>9}{'x over':>9}")
    rows = []
    for c in ESR_C_FILM:
        for se in SPEC_E_PULSE:
            r = store_kg(c, P, E, se)
            rows.append(r)
            print(f"  {c:10.0e}{se:9.0f}{r['e_power_J']:12.3f}{r['limited_by']:>9}"
                  f"{r['mass_kg']:10.4f}{r['specific_power_W_kg']/1e3:9.1f}"
                  f"{r['over_delivered']:9.2f}")

    worst = max(rows, key=lambda r: r['mass_kg'])
    typical = store_kg(1e-6, P, E, SPEC_E_PULSE[0])
    per_sat = PER_SAT_BASE + (SECTION_KG + worst['mass_kg']) / N_MANIFEST

    print(f"\n  worst corner  {worst['esr_c_s']:.0e} s at {worst['spec_e_J_kg']:.0f} J/kg: "
          f"{worst['mass_kg']:.4f} kg, {worst['limited_by']}-limited")
    print(f"  typical       {typical['esr_c_s']:.0e} s at {typical['spec_e_J_kg']:.0f} J/kg: "
          f"{typical['mass_kg']:.4f} kg, {typical['limited_by']}-limited")
    print(f"  against A54's EDLC {edlc[0]['mass_kg']:.2f}-{edlc[1]['mass_kg']:.2f} kg "
          f"-> {edlc[1]['mass_kg']/worst['mass_kg']:.0f}x lighter at the worst corner")
    print(f"  added mass per satellite, section + worst store: {per_sat:.4f} kg")

    bands = [
        ('1', "reproduces A54's EDLC 23.44-37.36 kg within 1 %",
         f"{edlc[0]['mass_kg']:.2f}-{edlc[1]['mass_kg']:.2f} kg",
         abs(edlc[0]['mass_kg'] - 23.44) / 23.44 <= 0.01
         and abs(edlc[1]['mass_kg'] - 37.36) / 37.36 <= 0.01),
        ('2', 'at the worst ESRxC the power-driven energy is <= 10x the delivered',
         f"{worst['e_power_J']:.2f} J against {E:.2f} J delivered",
         worst['e_power_J'] <= 10.0 * E),
        ('3', f'store at the worst corner <= the {SECTION_KG:.4f} kg section',
         f"{worst['mass_kg']:.4f} kg", worst['mass_kg'] <= SECTION_KG),
        ('4', 'store at the typical corner <= 0.25 kg',
         f"{typical['mass_kg']:.4f} kg", typical['mass_kg'] <= 0.25),
        ('5', 'added mass per satellite <= 2.0 kg',
         f"{per_sat:.4f} kg", per_sat <= 2.0),
        ('6', "specific power exceeds A54's required 23.20 kW/kg",
         f"{worst['specific_power_W_kg']/1e3:.1f} kW/kg at the worst corner",
         worst['specific_power_W_kg'] >= 23200.0),
        ('7', 'REPORT: store against ESRxC and specific energy',
         f"{len(rows)} points, {min(r['mass_kg'] for r in rows):.4f} to "
         f"{worst['mass_kg']:.4f} kg", None),
    ]
    print('\nbands:')
    for n, band, value, ok in bands:
        mark = 'REPORT' if ok is None else ('PASS' if ok else 'FAIL')
        print(f'  {n}  {mark:6} {band}\n        {value}')

    out = dict(analysis='A64', bands_declared_commit='HEAD~1',
               note='Specific energy 2000-2680 J/kg is a published pulsed-power TECHNOLOGY CLASS '
                    'range, not a product. ESR x C for film is SWEPT conservatively; typical '
                    'metallised polypropylene is nearer 1e-7 s. The switch and the conductors are '
                    'still unpriced, so every mass here is a LOWER BOUND. Derating, voltage '
                    'reversal and life are not modelled. No product, series or supplier is named.',
               requirement=req, edlc=edlc, film=rows,
               worst=worst, typical=typical, added_mass_per_satellite_kg=per_sat,
               bands=[dict(n=n, band=b, value=v,
                           verdict=('REPORT' if o is None else ('PASS' if o else 'FAIL')))
                      for n, b, v, o in bands])
    path = os.path.join(RESULTS, 'pulse_store_tech.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, default=float)
        f.write('\n')
    print(f'\nwrote {path}')


if __name__ == '__main__':
    main()
