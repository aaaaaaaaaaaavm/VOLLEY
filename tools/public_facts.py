"""Derive every number a public page is allowed to quote, from the files that own it.

WHY THIS EXISTS
---------------
Twelve public surfaces have independently retold this programme's headline numbers, by hand, and
every rollup change since 2026-08-13 has been chased across them one at a time and missed some:
A46 was found in eight places over five days (P93, P95, P96), ADR-030's shortened regenerative
section in seven (P97), and the acceleration ceiling's withdrawn basis in nine (P98). The register
counts alone have been wrong on the front page three times.

The cause is not carelessness. It is that a README is prose, and no gate reads prose.

This module does not hold a single number of its own. It reads them from the results and record
files that already own them, and `check_public.py` verifies the public pages against what it
returns. Adding a number here without a source is a defect in this file.

Run it to see the current values:  python3 tools/public_facts.py
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _j(*parts):
    with open(os.path.join(ROOT, *parts)) as fh:
        return json.load(fh)


def facts():
    """Every value a public surface may quote, with the file each is read from."""
    motor = _j('analysis', 'results', 'motor_results.json')
    astro = _j('analysis', 'results', 'astro_results.json')
    mass = _j('analysis', 'results', 'mass_properties.json')
    fam = _j('analysis', 'results', 'payload_family.json')
    comp = _j('analysis', 'results', 'comparators.json')
    reg = _j('analysis', 'results', 'register_status.json')
    siz = _j('analysis', 'results', 'sizing.json')
    cost = _j('analysis', 'results', 'cost.json')
    three_u = next(c for c in fam['classes'] if c['tag'] == '3U CubeSat')

    val = {
        # --- register, the count that has gone stale most often ---
        'register_total': reg['total'],
        'register_live': reg['live'],
        'register_corrected': reg['corrected'],
        'register_closed': reg['closed'],
        # --- Gen5 operating point ---
        'kt': motor['Kt_N_per_kA'] * 1000.0,
        'ripple_pct': motor['ripple_pct'],
        'v_exit': motor['shot']['v_exit'],
        'a_g': motor['shot']['a_g'],
        'pulse_ms': motor['shot']['t_ms'],
        'i_peak': motor['shot']['I_peak'],
        'e_gross_J': motor['shot']['E_drawn'],
        'e_net_J': motor['E_drawn_net_J'],
        'e_recovered_J': motor['regen']['E_recovered'],
        'regen_section_mm': motor['regen']['s_m'] * 1000.0,
        'ke_to_brake_J': motor['regen']['KE_to_brake'],
        'eff_net_pct': motor['eff_net_pct'],
        'dispersion_3sigma': motor['closed_loop_3sigma'],
        # --- mass ---
        'dry_kg': mass['dry_kg'],
        'loaded_kg': mass['loaded_kg'],
        'kg_per_3U': three_u['kg_per_satellite'],
        # --- astro ---
        'lifetime_mult': astro['lifetime']['mean']['multiplier'],
        'lifetime_ratio_vs_spring': comp['ratio_vs_fastest_spring'],
        'velocity_ratio': comp['velocity_ratio'],
        'ext_volley_pct': comp['lifetime_extensions']['volley'] * 100.0,
        'ext_spring_fast_pct': comp['lifetime_extensions']['spring_fast'] * 100.0,
        'recoil_Ns': astro['recoil_Ns_per_shot'],
        'realign_days': astro['conjunction']['realign_days'],
        # --- comparators, including the two withdrawn claims ---
        'kg_per_3U_dispenser': comp['kg_per_3U_dispenser'],
        'dispenser_ratio': comp['kg_per_3U_volley'] / comp['kg_per_3U_dispenser'],
        'coldgas_ratio': comp['coldgas_loss_ratio'],
        'phase_timing_s': comp['release_timing']['seconds_to_30deg_by_timing'],
        'da_commanded_m': comp['release_timing']['da_commanded_m'],
        # --- structure and cost ---
        'track_mode_Hz': siz['track_mode']['fixed_fixed_Hz'],
        'cost_INR': cost['total_INR'],
    }

    # Run sheets are files, not a JSON field. Count them the way a reader would.
    vdir = os.path.join(ROOT, 'validation')
    sheets = [f for f in os.listdir(vdir) if re.match(r'^A\d+.*\.md$', f)]
    nums = sorted({int(re.match(r'^A(\d+)', f).group(1)) for f in sheets})
    val['run_sheet_files'] = len(sheets)
    val['run_sheet_distinct'] = len(nums)
    val['run_sheet_high'] = max(nums)
    val['run_sheets_missing'] = [n for n in range(1, max(nums) + 1) if n not in nums]

    src = {
        'register_*': 'analysis/results/register_status.json',
        'kt / ripple / v_exit / a_g / pulse / current / energy / efficiency / dispersion':
            'analysis/results/motor_results.json',
        'dry_kg / loaded_kg': 'analysis/results/mass_properties.json',
        'kg_per_3U': 'analysis/results/payload_family.json',
        'lifetime / recoil / realign': 'analysis/results/astro_results.json',
        'dispenser_ratio / coldgas_ratio / phase_timing / da_commanded':
            'analysis/results/comparators.json',
        'track_mode_Hz': 'analysis/results/sizing.json',
        'cost_INR': 'analysis/results/cost.json',
        'run_sheet_*': 'validation/A*.md, counted',
    }
    return val, src


if __name__ == '__main__':
    v, s = facts()
    w = max(len(k) for k in v)
    for k in v:
        print(f'  {k:<{w}}  {v[k]}')
    print('\nsources')
    for k in s:
        print(f'  {k}\n      {s[k]}')
