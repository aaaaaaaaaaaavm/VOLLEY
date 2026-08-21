"""A35 constraint ledger: the mass that survives deleting every requirement.

WHY THIS EXISTS
---------------
A35 attributed every kilogram of the dry mass to the requirement that causes it, then deleted
requirements in all 64 corners of the six-constraint space. The finding is that 49.23 kg --
58.2 % -- survives every deletion, so there is no architecture that reaches the 2.0 kg per
satellite kill criterion. That is the whole of kill criterion 1's argument and it has only ever
been a sentence.

Draws analysis/results/constraint_ledger.json. Computes nothing.

Run:  python3 analysis/make_ledger_figure.py
"""
import json
import os

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), 'figures')


def main():
    with open(os.path.join(HERE, 'results', 'constraint_ledger.json'), encoding='utf-8') as fh:
        d = json.load(fh)
    dry = d['dry_kg']
    corners = d['corners']
    best = max(corners, key=lambda c: c['removed_kg'])
    survives = dry - best['removed_kg']

    plt.rcParams.update({'font.size': 8, 'figure.dpi': 200, 'savefig.bbox': 'tight'})
    fig, ax = plt.subplots(1, 2, figsize=(9.2, 3.4), gridspec_kw={'wspace': 0.34,
                                                                 'width_ratios': [1.15, 1]})

    # LEFT: what each single requirement is worth on its own.
    sr = d['single_requirement_kg']
    keys = sorted(sr, key=lambda k: -sr[k])
    vals = [sr[k] for k in keys]
    lbl = [f"{k}  {d['constraints'][k]}" for k in keys]
    ax[0].barh(range(len(keys)), vals, color=['#b4451f' if v else '#c9ccd1' for v in vals])
    ax[0].set_yticks(range(len(keys)))
    ax[0].set_yticklabels(lbl, fontsize=7)
    ax[0].invert_yaxis()
    ax[0].set_xlabel('kg removed if this requirement alone is deleted')
    ax[0].set_title('Three of six requirements carry no mass by themselves',
                    loc='left', fontsize=8)
    for i, v in enumerate(vals):
        ax[0].text(v + 0.4, i, f'{v:.2f}', va='center', fontsize=7)
    ax[0].grid(axis='x', alpha=0.25)

    # RIGHT: every corner of the 2^6 space, and the floor none of them reaches.
    rem = np.array([c['removed_kg'] for c in corners])
    left = dry - rem
    ax[1].scatter(np.arange(len(left)), left, s=14, color='#2a6f97', alpha=0.75,
                  label=f'{len(corners)} corners of the 6-constraint space')
    ax[1].axhline(survives, color='#b4451f', lw=1.4,
                  label=f'floor {survives:.2f} kg  ({survives/dry*100:.1f} % of dry)')
    ax[1].axhline(dry, color='k', lw=0.8, ls='--', label=f'dry mass {dry:.2f} kg')
    ax[1].set_xlabel('corner (requirement subset deleted)')
    ax[1].set_ylabel('dry mass remaining  [kg]')
    ax[1].set_title('No subset of deletions reaches 2.0 kg per satellite',
                    loc='left', fontsize=8)
    ax[1].legend(fontsize=7, loc='lower left')
    ax[1].grid(alpha=0.25)

    fig.suptitle('A35  every kilogram attributed to the requirement that causes it',
                 fontsize=9, y=1.03)
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, 'A35_ledger.png')
    fig.savefig(path)
    print(f'dry {dry:.2f} kg, best corner removes {best["removed_kg"]:.2f}, '
          f'floor {survives:.2f} kg = {survives/dry*100:.1f} %')
    print(f'best corner deletes {best["deleted"]}')
    print('wrote', path)


if __name__ == '__main__':
    main()
