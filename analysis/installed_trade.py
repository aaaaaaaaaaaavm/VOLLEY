"""N6: matched installed-mass sensitivity, not measured system benefit."""
import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analysis/results/installed_trade.json'
G=9.80665

def masses(increment,avoided,isp,common):
    ve=G*isp
    return 348*math.exp((common+avoided)/ve),(348+increment)*math.exp(common/ve)

def build():
    rows=[]
    for cell,shared,dv,isp,common in itertools.product((0,.25,.5,1,2),(0,2,5,10),(0,5,20,50,100),(60,220,320),(0,100,500)):
        increment=12*cell+shared; conventional,new=masses(increment,dv,isp,common)
        threshold=G*isp*math.log1p(increment/348)
        rows.append(dict(cell_increment_kg=cell,shared_increment_kg=shared,increment_kg=increment,
            avoided_dv_m_s=dv,isp_s=isp,common_dv_m_s=common,
            baseline_wet_kg=conventional,cell_wet_kg=new,net_wet_saving_kg=conventional-new,
            break_even_avoided_dv_m_s=threshold,positive_benefit=conventional>new))
    residual=max(abs(a-b) for r in rows for a,b in [masses(r['increment_kg'],r['break_even_avoided_dv_m_s'],r['isp_s'],r['common_dv_m_s'])])
    checks=dict(break_even=residual<=1e-8,zero=masses(0,0,220,100)[0]-masses(0,0,220,100)[1]==0,
        monotonic=all(masses(1,dv,isp,common)[1]>masses(0,dv,isp,common)[1] for dv,isp,common in itertools.product((0,100),(60,320),(0,500))),
        count=len(rows)==900,negative_retained=any(r['net_wet_saving_kg']<0 for r in rows))
    paths=['analysis/installed_trade.py','validation/N6_installed_trade.md']
    return dict(study='N6',cases=rows,verification=checks,break_even_residual_kg=residual,
        source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths})

def report(d):
    lines=['# Installed-system break-even — N6','','Adityavardhan Mishra · 25 September 2026','',
        'This is a 900-case sensitivity, not a completed installed mass estimate or proof of product advantage. Twelve identical 4 kg propulsionless payloads and a 300 kg retained baseline (including the conventional deployer) define both sides. All candidate increments are assumed differences above that baseline. Extra cell structure, controls, harness, launch restraint and host modifications must fit inside the stated increment; they are never implicitly free.','',
        'Baseline wet mass = 348 exp((common Δv + avoided Δv)/(g₀Isp)); candidate wet mass = (348 + ΔM) exp(common Δv/(g₀Isp)). This places all burns before release and carries all payload mass throughout. It cannot represent a sequential manifest with evolving mass. The exact break-even avoided Δv is g₀Isp ln(1+ΔM/348). A saved release impulse is not automatically avoided host Δv.','',
        '| Increment per cell (kg) | Shared increment (kg) | Total increment (kg) | Break-even at 60 s (m/s) | At 220 s | At 320 s |',
        '|---:|---:|---:|---:|---:|---:|']
    for cell,shared in ((.25,2),(.5,5),(1,5),(2,10)):
        inc=12*cell+shared;values=[G*i*math.log1p(inc/348) for i in (60,220,320)]
        lines.append(f'| {cell:g} | {shared:g} | {inc:g} | '+ ' | '.join(f'{x:.2f}' for x in values)+' |')
    lines+=['','Higher-Isp hosts save less propellant per avoided m/s, so more avoided Δv is needed to repay added dry mass. Common host burns multiply both wet masses: they increase the magnitude of the gain or loss but do not change this simplified break-even threshold. Negative and zero-benefit cases remain in the JSON.','',
        'The release cells must demonstrate an actual matched-mission maneuver saving before any row becomes an evidenced benefit. No supplier cost, launch price, mission success probability or complete installed mass is inferred. Independent-cell jam isolation can limit the number mechanically stranded, but cannot supply a reliability probability.','',
        '[Criteria](../validation/N6_installed_trade.md) · [All cases](../analysis/results/installed_trade.json) · [Accounting ledger](INSTALLED_ACCOUNTING.csv)','']
    return '\n'.join(lines)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args();d=build();doc=ROOT/'docs/INSTALLED_TRADE.md'
    if a.check:
        from campaign_allocation import numerical_match
        assert numerical_match(json.loads(OUT.read_text()),d) and doc.read_text()==report(d),'stale N6 output'
    else: OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n');doc.write_text(report(d))
    print(d['verification']);assert all(d['verification'].values())
