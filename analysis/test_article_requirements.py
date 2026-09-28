"""P92-S6: reproducible MC-L2 component loads; no hardware release."""
import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from mission_cartridges import size, evaluate, M, P
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analysis/results/test_article_requirements.json'


def build():
    source=size(2.,.08); n=source['nominal']; corners=source['corners']
    k,c,L=n['stiffness_N_m'],n['charge_m'],n['stroke_m']
    worst_load=max(r['peak_latch_N'] for r in corners)
    worst_energy=max(r['catcher_net_absorption_J'] for r in corners)
    springs=[]
    for d,index in itertools.product((.0015,.002,.0025,.003,.0035),(6,8,10,12)):
        D=index*d; na=79e9*d**4/(8*D**3*(k/2)); nt=na+2
        solid=nt*d; free=solid+1.15*(c+.0005)
        pitch=(free-2*d)/na
        wire=na*math.hypot(math.pi*D,pitch)+2*math.pi*D
        mass=2*7850*math.pi*d*d/4*wire
        wahl=(4*index-1)/(4*index-4)+.615/index
        stress=wahl*8*(worst_load/2)*D/(math.pi*d**3)
        reasons=[]
        if na<3: reasons.append('TOO_FEW_ACTIVE_TURNS')
        if D+d>.05: reasons.append('OUTER_DIAMETER')
        if free>.25: reasons.append('FREE_LENGTH')
        springs.append(dict(wire_mm=d*1000,index=index,mean_diameter_mm=D*1000,
            active_turns=na,total_turns=nt,outer_diameter_mm=(D+d)*1000,
            solid_mm=solid*1000,free_mm=free*1000,charged_length_mm=(free-c)*1000,
            solid_reserve_mm=(free-c-.0005-solid)*1000,pitch_mm=pitch*1000,
            helix_angle_deg=math.degrees(math.atan(pitch/(math.pi*D))),
            slenderness=free/D,pair_wire_mass_kg=mass,peak_shear_MPa=stress/1e6,
            inverse_rate_N_m=2*79e9*d**4/(8*D**3*na),
            geometry_survivor=not reasons,rejections=reasons,
            strength_status='UNKNOWN_MATERIAL_AND_DWELL',buckling_status='GUIDE_REQUIRED_UNVERIFIED'))
    survivors=[(i,s) for i,s in enumerate(springs) if s['geometry_survivor']]
    selected=min(survivors,key=lambda pair:pair[1]['pair_wire_mass_kg'])[0] if survivors else None
    catch=[]; allocation=1.5*worst_energy; stroke=.020
    for law in ('constant','linear'):
        peak=allocation/stroke*(1 if law=='constant' else 2)
        for i,r in enumerate(corners):
            mu=P*r['base_kg']/(P+r['base_kg'])
            speed=math.sqrt(2*r['catcher_kinetic_J']/mu)
            def absorb(x): return peak if law=='constant' else peak*x/stroke
            def rhs(t,y):
                return [y[1],(r['stiffness_N_m']*(r['charge_m']-L-y[0])-r['friction_N']-absorb(y[0]))/mu]
            def stopped(t,y): return y[1]
            stopped.terminal=True; stopped.direction=-1
            sol=solve_ivp(rhs,(0,.2),(0,speed),events=stopped,method='DOP853',rtol=1e-11,atol=1e-13)
            if not len(sol.t_events[0]): raise ValueError('CATCH_NOT_STOPPED')
            x=float(sol.y_events[0][0][0])
            drive=r['stiffness_N_m']*((r['charge_m']-L)*x-x*x/2)-r['friction_N']*x
            absorbed=peak*x if law=='constant' else peak*x*x/(2*stroke)
            residual=abs(absorbed-drive-r['catcher_kinetic_J'])
            catch.append(dict(corner=i,law=law,stroke_m=x,time_s=float(sol.t_events[0][0]),
                absorber_peak_N=absorb(x),energy_residual_J=residual,within_envelope=x<=stroke,
                warning='Requires anti-rebound latch; ideal force law is not a selected damper'))
    charger=[dict(lead_mm=lead*1000,efficiency=eta,torque_N_m=worst_load*lead/(2*math.pi*eta),
                  charge_time_s=(c+.0005)/lead,axial_load_N=worst_load)
             for lead,eta in itertools.product((.001,.002,.004),(.2,.4,.6))]
    fixed_speed=math.sqrt(2*n['work_J']/(M+P))
    uncertainty=2*6*math.sqrt((.0001/.1)**2+(.00001/(.1/6))**2)
    # Keep a failed measurement-range requirement visible: do not shrink it to the nominal speed.
    checks=dict(spring_inverse=max(abs(s['inverse_rate_N_m']/k-1) for s in springs)<=1e-12,
        catch_energy=max(r['energy_residual_J'] for r in catch)<=1e-6,
        catch_stroke=all(r['within_envelope'] for r in catch),
        finite_base_limit=abs(evaluate(k,L,c,B=1e12)['final_speed_m_s']-fixed_speed)<=1e-6,
        torque_monotonic=all(charger[i+3]['torque_N_m']>charger[i]['torque_N_m'] for i in range(6)),
        geometric_reserve=all(s['solid_reserve_mm']>0 for s in springs),
        cases=len(springs)==20 and len(catch)==162 and len(charger)==9)
    paths=['analysis/test_article_requirements.py','analysis/mission_cartridges.py',
           'validation/P92_S6_test_article.md','analysis/results/mission_cartridges.json']
    return dict(study='P92-S6',nominal=n,flight_corners=corners,spring_candidates=springs,
        selected_geometry_index=selected,catch_cases=catch,charger_cases=charger,
        load_envelope=dict(latch_N=worst_load,catch_absorption_J=worst_energy,
            catch_planning_energy_J=allocation,constant_absorber_N=allocation/stroke,
            linear_absorber_full_stroke_peak_N=2*allocation/stroke,
            charge_energy_J=max(r['stored_J'] for r in corners),
            peak_g=max(r['peak_g'] for r in corners)),
        bench=dict(fixed_base_speed_m_s=fixed_speed,finite_host_nominal_speed_m_s=2.,
            velocity_range_m_s=6.,expanded_velocity_uncertainty_at_range_m_s=uncertainty,
            uncertainty_target_pass=uncertainty<=.01,
            required_spacing_standard_uncertainty_m=math.sqrt((.01/(2*6))**2-(.00001/(.1/6))**2)*.1,
            shot_count=20,model_error_limit_m_s=.10,sample_std_limit_m_s=.03,
            actual_tests_completed=0),verification=checks,
        source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths})


def report(d):
    e=d['load_envelope'];b=d['bench'];s=d['spring_candidates'][d['selected_geometry_index']]
    return f'''# MC-L2 component requirements — P92-S6

Adityavardhan Mishra · 25 September 2026

This is an analytical procurement and coupon-planning package. No part has been
purchased, certified, strength-approved or tested. MC-L2 remains an 80 mm stroke,
4 kg payload, 0.25 kg pusher candidate. Every original S5 corner is retained.

| Derived requirement | Value | Disposition |
|---|---:|---|
| Maximum sampled latch load | {e['latch_N']:.3f} N | Unfactored working load; stress/contact review open |
| Maximum stored energy | {e['charge_energy_J']:.4f} J | Containment and charging review input |
| Maximum sampled initial acceleration | {e['peak_g']:.4f} g | Same analytical S5 model |
| Maximum pusher catch absorption | {e['catch_absorption_J']:.4f} J | Includes continued spring drive |
| Catch planning energy | {e['catch_planning_energy_J']:.4f} J | Explicit 1.5x allocation, not proof certification |
| Constant absorber force | {e['constant_absorber_N']:.3f} N | Ideal assumed law |
| Linear absorber full-stroke peak | {e['linear_absorber_full_stroke_peak_N']:.3f} N | Ideal assumed law; 20 mm envelope |
| Fixed-base bench nominal speed | {b['fixed_base_speed_m_s']:.6f} m/s | Compare bench measurements to this model |
| Finite-host final relative speed | 2.000000 m/s | Includes host recoil and pusher capture |

Twenty spring geometries were screened, with all rejected candidates in the JSON.
The lowest wire-mass geometric survivor uses two springs: {s['wire_mm']:.2f} mm
wire, {s['mean_diameter_mm']:.2f} mm mean diameter, {s['active_turns']:.3f} active
turns each, {s['solid_mm']:.3f} mm solid height and {s['free_mm']:.3f} mm free
length. Pair wire mass is {s['pair_wire_mass_kg']:.5f} kg and calculated maximum
Wahl shear stress is {s['peak_shear_MPa']:.1f} MPa. **This is not a strength pass
or supplier selection.** Fractional active turns require manufacturer interpretation.
Guide friction, pitch effects, fatigue, stress relaxation, end seating, tolerances
and material allowables remain open. Free-length/diameter ratio is {s['slenderness']:.2f};
positive guidance is mandatory. Wire mass omits guides and seats. The spring's
distributed moving mass is absent from S5 and needs dynamic calibration.

Rate per spring is Gd⁴/(8D³Na), solid height is (Na+2)d, and free length includes
1.15 times maximum charge travel above solid. Wahl factor is
(4C−1)/(4C−4)+0.615/C. Material modulus/density are illustrative assumptions.
A supplier must return certified material, rate tolerances, set/dwell data and
force-versus-length measurements. Manufacturer reference:
[Lee Spring compression design](https://www.leespring.com/learn-about-compression-springs).

The 162 catch integrations stop inside the envelope and close energy. They do
not establish rebound performance: the spring still pushes after the ideal stop.
An anti-rebound lock must capture and retain the pusher. Shock response depends
on the real force law and compliance. Nine charger lead/efficiency cases retain
load, torque and time. Torque excludes guide losses beyond the stated efficiency,
acceleration and gearbox starting behavior; the screw must disengage before release.

**Measurement requirement failed at full instrument range.** With 0.10 mm standard
gate-spacing uncertainty and 10 µs standard interval uncertainty, expanded speed
uncertainty at 6 m/s is {b['expanded_velocity_uncertainty_at_range_m_s']:.5f} m/s,
above 0.01 m/s. Keep that failure. At the same interval uncertainty, gate spacing
must be known to at most {b['required_spacing_standard_uncertainty_m']*1000:.4f} mm
standard uncertainty, or redesign gate spacing/timing and review the budget.
No experimental result exists; the planned 20-shot acceptance remains unexecuted.

[Criteria](../validation/P92_S6_test_article.md) ·
[All numerical cases](../analysis/results/test_article_requirements.json) ·
[Bench procedure](MC_L2_BENCH_PROCEDURE.md) · [Component ledger](MC_L2_COMPONENT_LEDGER.csv)
'''

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args();d=build()
    doc=ROOT/'docs/MC_L2_COMPONENT_REQUIREMENTS.md'
    if a.check:
        from campaign_allocation import numerical_match
        assert numerical_match(json.loads(OUT.read_text()),d) and doc.read_text()==report(d),'stale P92-S6 output'
    else:
        OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n');doc.write_text(report(d))
    print(json.dumps(dict(verification=d['verification'],loads=d['load_envelope'],bench=d['bench']),indent=2))
    assert all(d['verification'].values())
