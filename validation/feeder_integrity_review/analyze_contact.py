"""Assess captured native cases; completion never substitutes for acceptance."""
from pathlib import Path
import csv, json, math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

H = Path(__file__).resolve().parent
C = H / 'contact/campaign'
runs = json.loads((C / 'RUNS.json').read_text())['cases']
rows = []
traces = {}
for r in runs:
    with (C / (r['case_id'] + '.csv')).open() as f:
        a = np.genfromtxt(f, delimiter=',', names=True)
    a = np.atleast_1d(a)
    traces[r['case_id']] = a
    last = a[-1]
    m = r['native_metrics']
    p = [float(last[k])*1000 for k in ['payload_x_m', 'payload_y_m', 'payload_z_m']]
    v = [float(last[k]) for k in ['vx_m_s', 'vy_m_s', 'vz_m_s']]
    recomputed = None
    if abs(float(last['time_s']) - m['final_time_s']) < 1e-8:
        recomputed = [r['mass_kg'] * v[k] - m['contact_impulse_N_s'][k] + (r['mass_kg'] * r['gravity_m_s2'] * m['final_time_s'] if k == 2 else 0) for k in range(3)]
        assert max(abs(x) for x in recomputed) < 1e-7, r['case_id']
    rows.append({'case_id': r['case_id'], 'size': r['size'], 'label': r['label'],
                 'dt_s': r['dt_s'], 'iterations': r['iterations'], 'exit_code': r['exit_code'],
                 'time_s': float(last['time_s']), 'native_stop_time_s': m['final_time_s'], 'final_CG_mm': p,
                 'final_speed_m_s': math.sqrt(sum(x*x for x in v)),
                 'final_spin_rad_s': math.sqrt(sum(float(last[k])**2 for k in ['wx_rad_s','wy_rad_s','wz_rad_s'])),
                 'peak_resultant_contact_N': m['maximum_resultant_contact_force_N'],
                 'positive_mechanical_work_J': m['positive_mechanical_motor_work_J'],
                 'native_momentum_residual_N_s': m['payload_momentum_balance_residual_N_s'],
                 'independent_momentum_residual_N_s': recomputed})

refinements = []
for size in ['1U','3U']:
    group = [r for r in rows if r['size'] == size and r['label'] == 'time_refinement']
    fine = min(group, key=lambda r:r['dt_s'])
    for r in group:
        a = traces[r['case_id']]; b = traces[fine['case_id']]
        assert len(a) == len(b) and np.max(abs(a['time_s']-b['time_s'])) < 1e-8
        delta = np.column_stack([a[k]-b[k] for k in ['payload_x_m','payload_y_m','payload_z_m']])*1000
        refinements.append({'case_id':r['case_id'], 'reference_case':fine['case_id'], 'dt_s':r['dt_s'],
                            'final_CG_difference_mm':float(np.linalg.norm(delta[-1])),
                            'maximum_sampled_CG_difference_mm':float(np.linalg.norm(delta,axis=1).max())})

spots = json.loads((H/'DYNAMIC_BREP_SPOTS.json').read_text())
positive = [{'case_id':r['case_id'], **q} for r in spots['cases'] for q in r['checks'] if q['payload_fork_intersection_mm3'] > 1e-5]
assessment = {'revision':'FCE08','cases':rows,'time_refinement':refinements,
              'engineering_acceptance':'not_established',
              'positive_BRep_spot_count':len(positive),
              'maximum_spot_intersection_mm3':max(q['payload_fork_intersection_mm3'] for q in positive),
              'interpretation':'Nominal sequence completion and near-zero momentum residual verify execution/bookkeeping only. Time/iteration sensitivity and actual B-rep overlaps prevent contact-load, precision and dynamic clearance acceptance. Rigid bodies, ideal guide joints and unmeasured contact/actuation laws require further model development and physical correlation.'}
(H/'CONTACT_ASSESSMENT.json').write_text(json.dumps(assessment,indent=2)+'\n')
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42,'svg.fonttype':'none','svg.hashsalt':'VOLLEY-FCE08','savefig.facecolor':'white'})
fig,axs=plt.subplots(1,2,figsize=(6.8,2.8))
for size,color in [('1U','#285875'),('3U','#9a5636')]:
    rr=[r for r in rows if r['size']==size and r['label']=='time_refinement']
    axs[0].plot([r['dt_s']*1e6 for r in rr],[r['peak_resultant_contact_N'] for r in rr],'o-',color=color,label=size,ms=4)
    qq=[r for r in refinements if r['case_id'] in {q['case_id'] for q in rr}]
    axs[1].plot([r['dt_s']*1e6 for r in qq],[r['final_CG_difference_mm'] for r in qq],'o-',color=color,label=size,ms=4)
axs[0].set(xlabel='Integration step [µs]',ylabel='Peak resultant contact force [N]',title='a) Peak force is step-sensitive')
axs[1].set(xlabel='Integration step [µs]',ylabel='Final CG difference from 125 µs [mm]',title='b) Reference is a numerical case')
for ax in axs:ax.set_xticks([125,250,500]);ax.legend(frameon=False,fontsize=8)
fig.tight_layout()
for ext in ['png','svg','pdf']:fig.savefig(H/'figures'/('contact_refinement.'+ext),dpi=300)
plt.close(fig)

lines=['# Native contact assessment: FCE08','',
       'The twelve captured cases are numerical studies, not hardware release tests. **Engineering acceptance is not established.** Nominal sequence completion is separated from contact, clearance and accuracy acceptance.','',
       '## Captured results','',
       '| Case | Payload / variation | Step [µs] | Exit | Last CSV sample [s] | Peak resultant contact [N] | Positive mechanical work [J] |',
       '|:--|:--|--:|--:|--:|--:|--:|']
for r in rows:lines.append(f"| {r['case_id']} | {r['size']} / {r['label'].replace('_',' ')} | {r['dt_s']*1e6:g} | {r['exit_code']} | {r['time_s']:.3f} | {r['peak_resultant_contact_N']:.3f} | {r['positive_mechanical_work_J']:.5f} |")
lines += ['', 'Exit 0 denotes the programmed sequence endpoint; 11 denotes a commanded abort and 10 a numerical/domain rejection. These codes do not measure reliability. Mechanical work omits electrical losses, static holding power and actual actuator ratings.', '',
          '## Numerical review','',
          'The nominal 1U and 3U cases complete transfer, capture and fork withdrawal. Peak contact forces increase substantially as the integration step is reduced. Doubling the iteration cap also changes the final 3U pose. The study therefore does not establish a converged force history or delivery-accuracy range. The 125 µs trace is a comparison reference, not an exact solution.', '',
          '![Time-step sensitivity of native contact forces and final positions. Nonconverged peaks must not be used as hardware design loads.](figures/contact_refinement.png)','',
          f"Independent exact-solid spot checks retain {len(positive)} positive payload/fork intersections; the largest checked intersection volume is {assessment['maximum_spot_intersection_mm3']:.3f} mm³. This is a volume, not a penetration depth. These actual solver-transformed B-reps contradict a zero-dynamic-interference claim even where reported triangle-contact distances are small. The discrete spot checks do not cover all components or continuous time.", '',
          'For cases whose final CSV sample coincides with the final physics step, momentum balance recomputed from CSV velocity and native contact impulse agrees within the stated numerical tolerance. A truncated abort CSV does not support that independent endpoint check; its native every-step residual is retained separately. Balance validates bookkeeping under the rigid model; it does not validate collision geometry, contact law, constraints or force predictions.', '',
          'The gravity case is a rigid-body sensitivity and does not include the elastic tine deflection calculated separately in FLR02. The jam and stuck-pin cases are deliberately injected faults; their results do not demonstrate safe power-loss containment, redundant sensing or recovery. Ideal state measurements and force cutoffs have no selected physical implementation.', '',
          '## Disposition','',
          'Use the campaign to diagnose contact representation, numerical sensitivity and missing interfaces. Do not use it to accept loaded clearance, contact loads, tip-off, repeatability, a source-rated actuator or flight reliability. Further work requires controlled surface/contact refinement, time/iteration studies with specified convergence criteria, actual joint compliance/friction, complete restraint/release geometry and physical correlation.', '']
(H/'CONTACT_REVIEW.md').write_text('\n'.join(lines))
print('Native contact assessed:',len(rows),'cases; engineering acceptance not established; B-rep positive spots',len(positive))
