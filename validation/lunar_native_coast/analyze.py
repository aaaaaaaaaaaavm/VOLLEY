"""Summarize actual native output; do not infer terrain clearance or mission lifetime."""
from pathlib import Path
import csv
import gzip
import datetime as dt
import hashlib
import io
import json
import os

ROOT = Path(__file__).resolve().parent
os.environ['MPLCONFIGDIR'] = str(ROOT / 'source/mpl-cache')
os.environ['XDG_CACHE_HOME'] = str(ROOT / 'source/cache')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

RADIUS, MU = 1737.4, 4902.79996708864
COLUMNS = ['elapsed_s', 'x_km', 'y_km', 'z_km', 'vx_km_s', 'vy_km_s', 'vz_km_s',
           'radius_km', 'sma_km', 'eccentricity', 'osculating_periapsis_radius_km',
           'osculating_apoapsis_radius_km']


def read_checkpoints(path):
    rows = []
    for line in path.read_text().splitlines():
        fields = line.split(',')
        if len(fields) != len(COLUMNS):
            continue
        try:
            rows.append([float(x) for x in fields])
        except ValueError:
            continue
    return np.array(rows, dtype=float).reshape((-1, len(COLUMNS)))


def clean_native_samples(data):
    # Check actual time ordering. If a rewind/duplicate occurs, retain the final branch.
    # Report the removal count; do not assume that the native subscriber rewinds.
    keep = np.ones(len(data), dtype=bool)
    for index in np.flatnonzero(np.diff(data[:, 0]) < -1e-7) + 1:
        keep[:index] &= data[:index, 0] < data[index, 0] - 1e-7
    cleaned = data[keep]
    unique = np.r_[np.diff(cleaned[:, 0]) > 1e-7, True]
    cleaned = cleaned[unique]
    return cleaned, len(data) - len(cleaned)


results, samples = [], {}
cases = json.loads((ROOT / 'CASES.json').read_text())
for case in cases:
    name = case['name']
    execution = ROOT / 'runs' / (name + '_execution.json')
    if not execution.exists():
        results.append({**case, 'termination': 'execution_not_finished_at_analysis'})
        continue
    result = json.loads(execution.read_text())
    path = ROOT / 'runs' / (name + '.csv')
    if not path.exists() and path.with_suffix('.csv.gz').exists():
        path = path.with_suffix('.csv.gz')
    if not path.exists() or path.stat().st_size < 300:
        results.append({**result, 'termination': 'no_usable_history'})
        continue
    content = gzip.decompress(path.read_bytes()) if path.suffix == '.gz' else path.read_bytes()
    complete_bytes = content[:content.rfind(b'\n')+1]
    raw = np.loadtxt(io.BytesIO(complete_bytes), delimiter=',', skiprows=1, ndmin=2)
    if raw.shape[1] != len(COLUMNS) or not np.all(np.isfinite(raw)):
        results.append({**result, 'termination': 'unusable_or_nonfinite_native_history',
                        'raw_history_sha256': hashlib.sha256(content).hexdigest()})
        continue
    data, removed = clean_native_samples(raw)
    checkpoints = read_checkpoints(ROOT / 'runs' / (name + '_checkpoints.csv'))
    t, r, v = data[:, 0], data[:, 1:4], data[:, 4:7]
    radius = np.linalg.norm(r, axis=1)
    derived_ecc = np.linalg.norm(np.cross(v, np.cross(r, v)) / MU - r / radius[:, None], axis=1)
    final_time = float(checkpoints[-1, 0] if len(checkpoints) else t[-1])
    target_s = case['requested_days'][-1] * 86400
    completed = result['native_completion_message'] and result['exit_code'] == 0
    if completed and abs(final_time - target_s) < .001:
        termination = 'requested_horizon_reached'
    elif completed and len(checkpoints) and abs(checkpoints[-1, 7] - RADIUS) < .001:
        termination = 'native_spherical_radius_stop'
    elif result['execution_status'].startswith('timeout'):
        termination = 'wall_limit_timeout'
    else:
        termination = 'native_failure_or_incomplete'
    result.update({'termination': termination, 'final_elapsed_days': final_time / 86400,
                   'raw_sample_count': len(raw), 'final_branch_sample_count': len(data),
                   'incomplete_trailing_native_bytes_excluded': len(content) - len(complete_bytes),
                   'rewound_or_duplicate_samples_removed': removed,
                   'max_final_branch_sample_interval_s': float(np.max(np.diff(t))),
                   'sampled_min_spherical_altitude_km': float(np.min(data[:, 7]) - RADIUS),
                   'sampled_max_spherical_altitude_km': float(np.max(data[:, 7]) - RADIUS),
                   'minimum_osculating_periapsis_altitude_km': float(np.min(data[:, 10]) - RADIUS),
                   'eccentricity_range': [float(np.min(data[:, 9])), float(np.max(data[:, 9]))],
                   'all_output_values_finite': bool(np.all(np.isfinite(data))),
                   'radius_reconstruction_max_abs_km': float(np.max(np.abs(radius - data[:, 7]))),
                   'eccentricity_reconstruction_max_abs': float(np.max(np.abs(derived_ecc - data[:, 9]))),
                   'raw_history_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                   'checkpoints': [], 'completed_horizons': []})
    for requested_day, row in zip(case['requested_days'], checkpoints):
        reached = bool(abs(row[0] - requested_day * 86400) < .001)
        upto = data[t <= row[0] + .001]
        record = {'requested_day': requested_day, 'reached': reached,
                  **dict(zip(COLUMNS, map(float, row))),
                  'sampled_min_altitude_to_checkpoint_km': float(np.min(upto[:, 7]) - RADIUS)}
        result['checkpoints'].append(record)
        if reached:
            result['completed_horizons'].append(requested_day)
    with (ROOT / 'runs' / (name + '_canonical_checkpoints.csv')).open('w') as stream:
        writer = csv.writer(stream); writer.writerow(COLUMNS); writer.writerows(checkpoints)
    samples[name] = data
    results.append(result)

by_name = {r['name']: r for r in results}
comparisons = []
for apo in (100, 1000, 10000):
    base = f'p100_a{apo}'
    pairs = [('max_step_120_vs_60_s', base + '_d20_s120', base + '_d20_s60'),
             ('degree20_vs_degree40', base + '_d20_s120', base + '_d40_s120'),
             ('degree40_vs_degree80', base + '_d40_s120', base + '_d80_s120_30d'),
             ('GRGM900C_vs_LP165P_degree20', base + '_d20_s120', base + '_lp165p_d20_s120_30d')]
    for kind, left, right in pairs:
        a, b = by_name[left], by_name[right]
        for ca in a.get('checkpoints', []):
            for cb in b.get('checkpoints', []):
                if ca['requested_day'] != cb['requested_day'] or not ca['reached'] or not cb['reached']:
                    continue
                ra = np.array([ca[x] for x in COLUMNS[1:4]])
                rb = np.array([cb[x] for x in COLUMNS[1:4]])
                va = np.array([ca[x] for x in COLUMNS[4:7]])
                vb = np.array([cb[x] for x in COLUMNS[4:7]])
                comparisons.append({'kind': kind, 'apogee_altitude_km': apo, 'day': ca['requested_day'],
                                    'left': left, 'right': right,
                                    'checkpoint_epoch_difference_s': ca['elapsed_s'] - cb['elapsed_s'],
                                    'position_difference_m': float(np.linalg.norm(ra-rb) * 1000),
                                    'velocity_difference_mm_s': float(np.linalg.norm(va-vb) * 1e6),
                                    'eccentricity_difference': abs(ca['eccentricity'] - cb['eccentricity'])})

summary = {'study': 'BB52 C3 provisional native lunar coast / gravity / step screen',
           'analyzed_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
           'classification': 'Native computed propagation; sampled radius/eccentricity and root-located spherical stop. No terrain or lifetime qualification.',
           'sampling': 'Native GMAT subscriber samples; actual nonmonotonic/duplicate epochs are counted and filtered if present. Untouched native output is retained. Minimum radius is sampled; spherical stop is root-located.',
           'reference_radius_km': RADIUS, 'reference_mu_km3_s2': MU,
           'cases': results, 'comparisons': comparisons}
(ROOT / 'RESULTS.json').write_text(json.dumps(summary, indent=2, allow_nan=False) + '\n')
with (ROOT / 'COMPARISONS.csv').open('w') as stream:
    if comparisons:
        writer = csv.DictWriter(stream, fieldnames=list(comparisons[0])); writer.writeheader(); writer.writerows(comparisons)

plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10, 'axes.titlesize': 11,
                     'axes.spines.top': False, 'axes.spines.right': False, 'svg.fonttype': 'none',
                     'svg.hashsalt': 'lunar-native-20261023', 'pdf.fonttype': 42, 'savefig.dpi': 300})


def save(fig, stem, caption):
    fig.text(.02, .018, caption, fontsize=9, va='bottom')
    for ext in ('svg', 'pdf', 'png'):
        metadata = {'Date': None} if ext == 'svg' else {'CreationDate': None, 'ModDate': None} if ext == 'pdf' else None
        fig.savefig(ROOT / 'figures' / (stem + '.' + ext), dpi=300, metadata=metadata)
    plt.close(fig)


colours = ['#0072b2', '#d55e00', '#009e73', '#6f4c9b']
fig, axes = plt.subplots(3, 1, figsize=(7.1, 7.8))
variants = [('_d20_s120', 'GRGM 20/20', '-'), ('_d40_s120', 'GRGM 40/40', '--'),
            ('_d80_s120_30d', 'GRGM 80/80 (30 d)', ':'), ('_i0_d20_s120', 'GRGM 20/20, i=0°', '-.')]
for index, (apo, ax) in enumerate(zip((100, 1000, 10000), axes)):
    for (suffix, label, style), colour in zip(variants, colours):
        name = f'p100_a{apo}' + suffix
        if name not in samples:
            continue
        data = samples[name]; low = np.minimum.accumulate(data[:, 7] - RADIUS)
        ax.plot(data[:, 0] / 86400, low, color=colour, ls=style, label=label, lw=1.3)
    ax.axhline(0, color='.4', lw=.7)
    ax.set(title=f'{chr(97+index)}  Initial 100 × {apo} km orbit', ylabel='Minimum sampled\naltitude to date (km)', xlim=(0, 180))
    ax.grid(alpha=.2)
axes[-1].set_xlabel('Elapsed time (days)')
fig.legend(*axes[0].get_legend_handles_labels(), loc='upper center', ncol=2, frameon=False, fontsize=9)
fig.subplots_adjust(left=.16, right=.98, bottom=.17, top=.89, hspace=.48)
save(fig, 'lunar_sampled_altitude',
     'GMAT R2026a; DE421; Earth/Sun point masses; MOON_PA gravity; max step 120 s.\n'
     'Radius minus 1737.4 km sphere; cumulative sampled minima, not continuous terrain clearance.\n'
     'Reference i=90° in MJ2000Eq unless labelled 0°; no stationkeeping. 23 Oct 2026.')

fig, axes = plt.subplots(3, 1, figsize=(7.1, 7.8))
for ax, kind, title in zip(axes, ['max_step_120_vs_60_s', 'degree20_vs_degree40', 'degree40_vs_degree80'],
                           ['a  Maximum step: 120 s versus 60 s at 20/20',
                            'b  Gravity degree/order: 20/20 versus 40/40',
                            'c  Gravity degree/order: 40/40 versus 80/80']):
    for apo, colour, marker in zip((100, 1000, 10000), colours, ['o', 's', '^']):
        rows = sorted([x for x in comparisons if x['kind'] == kind and x['apogee_altitude_km'] == apo], key=lambda x:x['day'])
        if rows:
            ax.plot([x['day'] for x in rows], [x['position_difference_m'] for x in rows],
                    color=colour, marker=marker, label=f'100 × {apo} km')
    ax.set(title=title, xlabel='Common checkpoint (days)', ylabel='Position difference (m)', yscale='log')
    ax.grid(alpha=.2)
fig.legend(*axes[0].get_legend_handles_labels(), loc='upper center', ncol=3, frameon=False, fontsize=9)
fig.subplots_adjust(left=.16, right=.98, bottom=.17, top=.89, hspace=.62)
save(fig, 'lunar_refinement',
     'Common-epoch native states; logarithmic difference axis; completed requested checkpoints only.\n'
     'Step changes test numerical sensitivity; degree changes test gravity-model sensitivity.\n'
     'No precision acceptance criterion or physical convergence is established. 23 Oct 2026.')

print('Analyzed', sum('final_elapsed_days' in r for r in results), 'of', len(cases), 'native attempts')
for r in results:
    print(r['name'], r['termination'], round(r.get('final_elapsed_days', 0), 4),
          'd; min alt km', round(r.get('sampled_min_spherical_altitude_km', 0), 5),
          'horizons', r.get('completed_horizons', []))
