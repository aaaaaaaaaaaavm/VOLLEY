"""P92-S5: distinct mission-sized cartridges under unchanged reference limits."""
import argparse,csv,hashlib,io,itertools,json,math
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
ROOT=Path(__file__).resolve().parents[1]
RESULT=ROOT/'analysis/results/mission_cartridges.json'
DOC=ROOT/'docs/MISSION_CARTRIDGES.md'
CSV=ROOT/'cad/current_cell/MISSION_CARTRIDGES.csv'
M,P,G=4.,.25,9.80665


def evaluate(k,L,c,B=300.,f=2.):
    A=M+P;mu=A*B/(A+B)
    initial=k*c;end=k*(c-L)-f;work=k*(c*L-L*L/2)-f*L
    reasons=[]
    if end<=0:reasons.append('CONTACT_NOT_POSITIVE_AT_EXIT')
    if work<=0:reasons.append('NO_POSITIVE_EXIT_WORK')
    if (initial-f)/A/G>10:reasons.append('PEAK_ACCELERATION')
    if c>.320+1e-12:reasons.append('CHARGE_TRAVEL')
    limit=json.loads((ROOT/'analysis/results/reference_cell_mechanics.json').read_text())['cases'][88]['peak_latch_force_n']
    if initial>limit+1e-9:reasons.append('REFERENCE_LATCH_LOAD')
    v=math.sqrt(2*work/mu) if work>0 else None
    speed=v*B/(B+P) if v is not None else None
    q=B/(A+B)*v if v is not None else None
    host=-A/(A+B)*v if v is not None else None
    retained=(B*host+P*q)/(B+P) if v is not None else None
    catcher=.5*(P*B/(P+B))*v*v if v is not None else None
    d=.020
    spring_catch=k*((c-L)*d-d*d/2)
    return dict(stiffness_N_m=k,stroke_m=L,charge_m=c,base_kg=B,friction_N=f,
        peak_latch_N=initial,net_end_N=end,peak_g=(initial-f)/A/G,work_J=work,
        final_speed_m_s=speed,stored_J=.5*k*c*c,accepted=not reasons,rejections=reasons,
        momentum_residual_kg_m_s=abs(M*q+(B+P)*retained) if q is not None else None,
        catcher_kinetic_J=catcher,catcher_continued_spring_work_J=spring_catch,
        catcher_net_absorption_J=catcher+spring_catch-f*d if catcher is not None else None,
        catcher_model_valid=bool(c-L>=d and k*(c-L-d)>f),
        catcher_note='20 mm continued-contact catch; invalid if spring unloads or net drive reverses')


def size(speed,L):
    B=300.;mu=(M+P)*B/(M+P+B);c=L/.75
    v=speed*(B+P)/B;k=(.5*mu*v*v+2*L)/(L*(c-L/2))
    nominal=evaluate(k,L,c)
    corners=[evaluate(k*a,L,c+b,B,f) for a,b,B,f in itertools.product(
        (.95,1,1.05),(-.0005,0,.0005),(100,300,1000),(0,2,5))]
    return dict(requested_speed_m_s=speed,nominal=nominal,corners=corners,
        all_corners_pass=all(r['accepted'] for r in corners),
        minimum_speed_m_s=min(r['final_speed_m_s'] for r in corners if r['final_speed_m_s'] is not None),
        maximum_speed_m_s=max(r['final_speed_m_s'] for r in corners if r['final_speed_m_s'] is not None))


def integrated_speed(r):
    A=M+P;B=r['base_kg'];mu=A*B/(A+B)
    def rhs(t,y):return [y[1],(r['stiffness_N_m']*(r['charge_m']-y[0])-r['friction_N'])/mu]
    def exit(t,y):return y[0]-r['stroke_m']
    exit.terminal=True;exit.direction=1
    s=solve_ivp(rhs,[0,10],[0,0],events=exit,rtol=1e-11,atol=1e-13,method='DOP853')
    if not len(s.t_events[0]):raise ValueError('NO_EXIT')
    return float(s.y_events[0][0][1])*B/(B+P)


def build():
    rows=[size(u,L) for u,L in itertools.product((.5,1,2,3,5),(.020,.040,.080,.120,.240))]
    selected=[]
    for u in (.5,1,2,3,5):
        good=[(i,r) for i,r in enumerate(rows) if r['requested_speed_m_s']==u and r['all_corners_pass']]
        winner=min(good,key=lambda x:(x[1]['nominal']['stroke_m'],x[1]['nominal']['stored_J'])) if good else None
        selected.append(dict(speed_m_s=u,candidate_index=winner[0] if winner else None,
            status='SAMPLED_LAYOUT_CANDIDATE' if winner else 'NO_CANDIDATE_WITHIN_FROZEN_LIMITS'))
    errors=[abs(integrated_speed(rows[x['candidate_index']]['nominal'])-x['speed_m_s']) for x in selected if x['candidate_index'] is not None]
    checks=dict(inverse=max(abs(r['nominal']['final_speed_m_s']-r['requested_speed_m_s']) for r in rows)<1e-8,
        integrated=max(errors)<1e-7,momentum=max(r['momentum_residual_kg_m_s'] or 0 for x in rows for r in x['corners'])<=1e-8,
        contact_failure=not evaluate(100,.02,.025,f=100)['accepted'],case_count=len(rows)==25 and all(len(x['corners'])==81 for x in rows))
    paths=['analysis/mission_cartridges.py','validation/P92_S5_mission_cartridges.md','analysis/results/reference_cell_mechanics.json']
    return dict(study='P92-S5',cases=rows,selected=selected,verification=checks,
        integrated_errors_m_s=errors,source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths})


def report(d):
    lines=['# Mission-sized mechanical cartridges','','Adityavardhan Mishra · 17 September 2026','',
        'I size separate cartridges and retain the original charge, latch and acceleration limits. These are nominal force-law targets for CAD, not selected springs. A corner pass covers sampled contact/load conditions; it does not establish release-speed accuracy.','',
        '| Target (m/s) | Stroke (mm) | Stiffness (N/m) | Charge (mm) | Peak latch (N) | Speed range across corners (m/s) |','|---:|---:|---:|---:|---:|---|']
    for s in d['selected']:
        if s['candidate_index'] is None:lines.append(f"| {s['speed_m_s']:g} | — | — | — | — | no candidate within frozen limits |")
        else:
            r=d['cases'][s['candidate_index']];n=r['nominal']
            lines.append(f"| {s['speed_m_s']:g} | {n['stroke_m']*1000:g} | {n['stiffness_N_m']:.3f} | {n['charge_m']*1000:.3f} | {n['peak_latch_N']:.3f} | {r['minimum_speed_m_s']:.4f}–{r['maximum_speed_m_s']:.4f} |")
    lines+=['','For moving payload+pusher mass A=m+p and retained base B, the internal reduced mass is μ=AB/(A+B). After an ideal inelastic pusher catch, the final payload/retained-host relative speed is B/(B+p)√(2W/μ). Spring work W=k(cL−L²/2)−fL. The initial spring force is kc and the net endpoint force is k(c−L)−f. The latter must remain positive.','',
        'The shortest cartridge is not automatically the smallest installed assembly. Spring solid height/free length, guidance, latch, charger and tolerances still require geometry and component evidence. At low authority the friction and charge errors consume a large fraction of useful energy. Measure these before promising a mission tolerance.','',
        'The JSON retains the 20 mm catcher accounting and marks when continued spring contact over that entire catcher stroke is invalid. Low-stroke cartridges need a separately designed shorter catch or a disengaged spring; never reuse the MC-A1 catcher number.','',
        f"Verification: {'PASS' if all(d['verification'].values()) else 'FAIL'}. Twenty-five designs, 81 corners each; rejected designs retained.",'',
        '[Criteria](../validation/P92_S5_mission_cartridges.md) · [Results](../analysis/results/mission_cartridges.json) · [CAD force-law ledger](../cad/current_cell/MISSION_CARTRIDGES.csv)','']
    return '\n'.join(lines)


def ledger(d):
    out=io.StringIO();w=csv.writer(out,lineterminator='\n');w.writerow(['target_m_s','stroke_mm','stiffness_N_m','charge_mm','latch_N','status'])
    for s in d['selected']:
        n=d['cases'][s['candidate_index']]['nominal'] if s['candidate_index'] is not None else None
        w.writerow([s['speed_m_s'],n['stroke_m']*1000 if n else '',n['stiffness_N_m'] if n else '',n['charge_m']*1000 if n else '',n['peak_latch_N'] if n else '',s['status']])
    return out.getvalue()

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--check',action='store_true');args=a.parse_args();d=build()
    if args.check:
        from campaign_allocation import numerical_match
        assert numerical_match(json.loads(RESULT.read_text()),d) and DOC.read_text()==report(d) and CSV.read_text()==ledger(d),'stale outputs'
    else:
        RESULT.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n');DOC.write_text(report(d));CSV.write_text(ledger(d))
    print(d['selected']);print(d['verification']);assert all(d['verification'].values())
