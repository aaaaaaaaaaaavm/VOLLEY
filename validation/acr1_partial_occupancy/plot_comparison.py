"""Plot selected host propellant at the declared 5 N authority."""
import csv
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

H = Path(__file__).resolve().parent
plt.style.use(H.parents[1]/'tools/scientific.mplstyle')
rows = list(csv.DictReader((H/'technical/SELECTED_MISSION_OUTCOMES.csv').open()))
fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.5), sharey=True)
series = [('gen5', 'ACR1', '#0072b2', 'o'),
          ('spring_fixed2', 'Fixed 2 m/s spring', '#d55e00', '^'),
          ('spring_pretrim', 'Ideal ground-pretrim spring', '#555555', 's')]
for ax, family, title, letter in zip(axes, ['uniform_2', 'alternating_1_3'],
    ['Uniform 2 m/s target family', 'Alternating 1 / 3 m/s family'], ['(a)', '(b)']):
    for architecture, label, colour, marker in series:
        y = []
        for n in [2, 4, 12]:
            key = family if n == 12 else f'n{n}_{family}'
            row = next(r for r in rows if r['family'] == key
                       and float(r['force_authority_N']) == 5
                       and r['architecture'] == architecture)
            y.append(float(row['fuel_used_kg']) if row['fuel_used_kg'] else np.nan)
        ax.plot([2, 4, 12], y, color=colour, marker=marker, label=label,
                linewidth=1.3, markersize=4)
    ax.set_title(f'{letter} {title}', loc='left', fontsize=9.5)
    ax.set_xlabel('Deployed payload count')
    ax.set_xticks([2, 4, 12]); ax.set_xlim(1.3, 12.7)
    ax.set_yscale('log'); ax.set_ylim(.005, 5)
    ax.grid(axis='y', which='major', alpha=.5)
axes[0].set_ylabel('Host propellant consumed (kg)')
axes[1].annotate('Fixed spring: no tested pass at 12', xy=(12, .009),
                 xytext=(4, .0065), fontsize=7.7, color='#a74400')
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=3, frameon=False,
           fontsize=8, bbox_to_anchor=(.5, .005))
fig.subplots_adjust(left=.10, right=.98, top=.87, bottom=.24, wspace=.17)
fig.suptitle('Partial-occupancy comparison · allocated host force ≤ 5 N', fontsize=11, y=.99)
out = H/'figures'; out.mkdir(exist_ok=True)
for suffix in ['png', 'svg', 'pdf']:
    metadata = {'Creator': 'Matplotlib; plot_comparison.py'} if suffix != 'png' else {'Software': 'Matplotlib; plot_comparison.py'}
    if suffix == 'pdf': metadata.update(CreationDate=None, ModDate=None)
    fig.savefig(out/f'partial_occupancy_propellant.{suffix}', metadata=metadata, dpi=300)
plt.close(fig)
