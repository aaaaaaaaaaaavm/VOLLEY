"""C0-S1: ideal lunar release authority and payload-size requirements screen."""
import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'analysis/results/lunar_release_scaling.json'
DOC = ROOT/'docs/LUNAR_RELEASE_SCREEN.md'
MU = 4902.800118e9
R = 1737400.
ME = 398600.435507e9
RE = 6378137.
G = 9.80665
U = 4.569852054443217
STAGING = [(100.,100.),(100.,1000.),(100.,10000.)]


def elements(r, v):
    energy = v*v/2-MU/r
    h = r*v
    # Stable at the circular limit; general vector eccentricity reduces to this.
    e = abs(r*v*v/MU-1)
    bound = energy < 0
    a = -MU/(2*energy) if energy != 0 else None
    rp = h*h/MU/(1+e)
    ra = a*(1+e) if bound else None
    return dict(energy_j_kg=energy, angular_momentum_m2_s=h, eccentricity=e,
                semimajor_m=a, periapsis_altitude_km=(rp-R)/1000,
                apoapsis_altitude_km=(ra-R)/1000 if bound else None,
                period_s=2*math.pi*math.sqrt(a**3/MU) if bound else None,
                bound=bound, above_reference_surface=rp>R)


def split(m, host, u):
    if m <= 0 or host <= 0: raise ValueError('positive masses required')
    return host/(m+host)*u, -m/(m+host)*u


def fraction(dv, isp):
    if dv < 0 or isp <= 0: raise ValueError('nonnegative dv and positive Isp required')
    return -math.expm1(-dv/(G*isp))


def propagate(r, v, dt, tight=False):
    def rhs(t,y):
        rr=math.hypot(y[0],y[1]); return [y[2],y[3],-MU*y[0]/rr**3,-MU*y[1]/rr**3]
    result=solve_ivp(rhs,[0,dt],[r,0,0,v],method='DOP853',rtol=3e-14 if tight else 2e-12,
                     atol=1e-9 if tight else 1e-7)
    if not result.success: raise RuntimeError(result.message)
    return result.y[:,-1]


def build():
    cases=[]; momentum=[]; speed=[]; energy=[]; zero=[]; apses=[]
    for (hp,ha),at,host,u in itertools.product(STAGING,['periapsis','apoapsis'],[100.,300.,1000.],[-U,-2.,-.5,0.,.5,2.,U]):
        rp,ra=R+hp*1000,R+ha*1000; a=(rp+ra)/2
        r=rp if at=='periapsis' else ra; v=math.sqrt(MU*(2/r-1/a))
        dp,dh=split(4.,host,u); pe=elements(r,v+dp); he=elements(r,v+dh)
        momentum.append(abs(4*dp+host*dh)); speed.append(abs(dp-dh-u))
        energy.append(abs(.5*4*(v+dp)**2+.5*host*(v+dh)**2-.5*(host+4)*v*v-.5*4*host/(host+4)*u*u))
        base=elements(r,v)
        apses.extend([abs(base['periapsis_altitude_km']-hp)*1000,abs(base['apoapsis_altitude_km']-ha)*1000])
        if u==0: zero.extend([abs(pe['periapsis_altitude_km']-hp)*1000,abs(pe['apoapsis_altitude_km']-ha)*1000])
        cases.append(dict(staging_periapsis_km=hp,staging_apoapsis_km=ha,release_at=at,
                          retained_host_kg=host,payload_kg=4.,relative_speed_m_s=u,
                          payload_impulse_m_s=dp,host_impulse_m_s=dh,payload=pe,host=he))
    sizes=[]; work=[]
    for m,host,u in itertools.product([1.,4.,12.,25.,50.,100.,250.],[300.,1000.],[.5,2.,U]):
        dp,dh=split(m,host,u); bounds=[]
        for g in [3.,10.]:
            s=u*u/(2*g*G); spring=2*s
            e=.5*m*u*u
            work.extend([abs(m*g*G*s-e)/e,abs(.5*m*g*G*spring-e)/e])
            bounds.append(dict(study_acceleration_g=g,constant_force_stroke_m=s,
                               zero_preload_linear_spring_stroke_m=spring,peak_payload_force_n=m*g*G))
        sizes.append(dict(payload_kg=m,retained_host_kg=host,relative_speed_m_s=u,
                          payload_impulse_m_s=dp,host_impulse_m_s=dh,
                          separation_momentum_kg_m_s=m*dp,ideal_relative_energy_j=.5*m*host/(m+host)*u*u,
                          fixed_frame_payload_energy_j=.5*m*u*u,fixed_frame_bounds=bounds))
    r0=RE+300000; at=(r0+384400000)/2
    tli=math.sqrt(ME*(2/r0-1/at))-math.sqrt(ME/r0)
    captures=[]
    for (hp,ha),vinf in itertools.product(STAGING,[800.,1000.]):
        rp,ra=R+hp*1000,R+ha*1000; a=(rp+ra)/2
        vin=math.sqrt(vinf*vinf+2*MU/rp); target=math.sqrt(MU*(2/rp-1/a)); dv=vin-target
        circularize=target-math.sqrt(MU/rp)
        captures.append(dict(staging_periapsis_km=hp,staging_apoapsis_km=ha,
                             assumed_arrival_vinf_m_s=vinf,capture_dv_m_s=dv,
                             subsequent_circularization_dv_m_s=circularize,
                             fractions=[dict(assumed_isp_s=isp,capture_only=fraction(dv,isp),
                                             earth_departure_plus_capture_plus_assumed_200_m_s=fraction(tli+dv+200,isp)) for isp in [220.,320.]]))
    independent=[]
    rp,ra=R+100000,R+1000000; v=math.sqrt(MU*(2/rp-2/(rp+ra)))
    for u in [-U,0,U]:
        dp,_=split(4,300,u); actual=v+dp; e=elements(rp,actual); other=R+1000*e['apoapsis_altitude_km']
        expected=np.array([-other,0,0,-rp*actual/other])
        coarse=propagate(rp,actual,e['period_s']/2); fine=propagate(rp,actual,e['period_s']/2,True)
        independent.append(dict(relative_speed_m_s=u,position_error_m=float(np.linalg.norm(coarse[:2]-expected[:2])),
                                velocity_error_m_s=float(np.linalg.norm(coarse[2:]-expected[2:])),
                                tightened_position_change_m=float(np.linalg.norm(fine[:2]-coarse[:2])),
                                tightened_velocity_change_m_s=float(np.linalg.norm(fine[2:]-coarse[2:]))))
    rejected=False
    try: split(0,300,U)
    except ValueError: rejected=True
    negative=False
    try: fraction(-1,220)
    except ValueError: negative=True
    checks=dict(case_counts=len(cases)==126 and len(sizes)==42,
                momentum=max(momentum)<=1e-8,relative_speed=max(speed)<=1e-10,
                kinetic_energy=max(energy)<=1e-5,zero_release=max(zero)<=1e-3,
                apsidal_reconstruction=max(apses)<=1e-3,
                independent_propagation=all(c['position_error_m']<=.1 and c['velocity_error_m_s']<=1e-4 for c in independent),
                tighter_propagation=all(c['tightened_position_change_m']<.01 and c['tightened_velocity_change_m_s']<1e-5 for c in independent),
                work_identity=max(work)<=1e-12,invalid_mass_rejected=rejected,
                rocket_equation_limits=negative and fraction(0,220)==0 and 0<fraction(100,220)<1,
                capture_energy_sign=all(c['capture_dv_m_s']>0 for c in captures))
    paths=['analysis/lunar_release_scaling.py','validation/C0_S1_lunar_release_scaling.md']
    return dict(study='C0-S1',evidence='IDEAL_TWO_BODY_REQUIREMENTS_SCREEN_NOT_LIFETIME_OR_HARDWARE',
                inputs=dict(lunar_mu_m3_s2=MU,lunar_radius_m=R,earth_mu_m3_s2=ME,earth_radius_m=RE,reference_distance_m=384400000.),
                source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},
                release_cases=cases,scaling_cases=sizes,earth_departure_dv_m_s=tli,capture_scenarios=captures,
                verification=dict(checks=checks,passed=all(checks.values()),max_momentum_residual= max(momentum),
                                  max_energy_residual_j=max(energy),independent=independent))


def report(d):
    lines=['# Lunar release authority and payload-size screen','',
           'Generated from `analysis/lunar_release_scaling.py`. **Concept requirements only: no lifetime, selected carrier or flight performance is established.**','',
           '126 finite-host release cases and 42 payload-size cases are retained. Negative signed speed means repointing the carrier. It does not mean firing backwards through the same cell.','',
           '## Lunar geometry: 4 kg payload, 300 kg retained host','',
           '| Staging altitudes (km) | Release apsis | Relative speed (m/s) | Payload perilune (km) | Payload apolune (km) | Host recoil (m/s) |',
           '|---|---|---:|---:|---:|---:|']
    for c in d['release_cases']:
        if c['retained_host_kg']==300 and c['relative_speed_m_s'] in [-U,0,U]:
            p=c['payload']; lines.append(f"| {c['staging_periapsis_km']:g} x {c['staging_apoapsis_km']:g} | {c['release_at']} | {c['relative_speed_m_s']:.6f} | {p['periapsis_altitude_km']:.3f} | {p['apoapsis_altitude_km']:.3f} | {c['host_impulse_m_s']:.6f} |")
    lines+=['','Releasing near perilune principally changes apolune in this collinear screen; near apolune it principally changes perilune. A small perilune margin is sensitive to the sign and error of an apolune release. These geometric ellipses are not demonstrated frozen lunar orbits.','',
            '## Carrier responsibility','',f"Ideal impulsive Earth departure from 300 km circular altitude: **{d['earth_departure_dv_m_s']:.1f} m/s** to a geocentric ellipse reaching the reference lunar distance. It is not a lunar encounter solution. The separately assumed arrival speeds below are not predictions of that Earth ellipse.",'',
            '| Staging altitudes (km) | Assumed arrival v-infinity (m/s) | Capture impulse (m/s) | Later circularization at 100 km (m/s) |','|---|---:|---:|---:|']
    for c in d['capture_scenarios']:
        lines.append(f"| {c['staging_periapsis_km']:g} x {c['staging_apoapsis_km']:g} | {c['assumed_arrival_vinf_m_s']:g} | {c['capture_dv_m_s']:.1f} | {c['subsequent_circularization_dv_m_s']:.1f} |")
    lines+=['','Capture and orbit reshaping are carrier burns. A few m/s release cannot turn the high ellipse into the 100 km circular orbit. The carrier must first approach the payload’s useful orbit. Progressive burns need a finite-thrust trajectory, restart/endurance and loss budget; subdividing an impulse is not equivalent automatically.','',
            'The JSON includes rocket-equation fractions at assumed 220/320 s Isp and a separately assumed 200 m/s allowance. That allowance is not an end-of-life solution. No provider, engine, tank, dry mass or leftover propellant is credited.','',
            '## Size scaling at the current study speed','',
            '| Payload (kg) | Retained host (kg) | Relative speed (m/s) | Ideal relative energy (J) | Host recoil (m/s) | Fixed-frame peak force at 3 g (N) |','|---:|---:|---:|---:|---:|---:|']
    for c in d['scaling_cases']:
        if c['retained_host_kg']==300 and c['relative_speed_m_s']==U:
            lines.append(f"| {c['payload_kg']:g} | 300 | {U:.6f} | {c['ideal_relative_energy_j']:.2f} | {c['host_impulse_m_s']:.4f} | {c['fixed_frame_bounds'][0]['peak_payload_force_n']:.2f} |")
    lines+=['','The finite-host energy omits the retained pusher, friction, spring preload and conversion losses. Fixed-frame stroke bounds use the relative speed as the large-host limit: constant force u²/(2a), zero-end-preload linear spring u²/a. Neither is a component selection. Large satellites require attachment-ring/pallet load paths and synchronized force application, not enlarged CubeSat rails.','',
            '## Verification','', '| Check | Result |','|---|---|']
    lines += [f"| {k} | {'PASS' if v else 'FAIL'} |" for k,v in sorted(d['verification']['checks'].items())]
    lines += ['','Independent Cartesian propagation checks three opposite-apsis states, including extreme releases; tighter reruns and energy/momentum/work limits are retained in JSON. Physical stability and useful lifetime remain untested.','',
              '[Predeclared criteria](../validation/C0_S1_lunar_release_scaling.md) · [Full results](../analysis/results/lunar_release_scaling.json) · [Lunar programme](LUNAR_VOLLEY_CONCEPT.md)','',
              'Sources: [JPL astrodynamic parameters](https://ssd.jpl.nasa.gov/astro_par.html), [NASA Moon facts](https://science.nasa.gov/moon/facts/). Radii and scenario choices are declared assumptions in the run sheet.','']
    return '\n'.join(lines)


def matches(a,b):
    if type(a)!=type(b): return False
    if isinstance(a,dict): return a.keys()==b.keys() and all(matches(a[k],b[k]) for k in a)
    if isinstance(a,list): return len(a)==len(b) and all(matches(x,y) for x,y in zip(a,b))
    if isinstance(a,float): return math.isfinite(a) and math.isfinite(b) and math.isclose(a,b,rel_tol=1e-9,abs_tol=1e-7)
    return a==b


def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');args=p.parse_args();d=build()
    if args.check:
        old=json.loads(OUT.read_text())
        if old['inputs']!=d['inputs'] or old['source_sha256']!=d['source_sha256'] or not matches(old,d) or DOC.read_text()!=report(old):
            raise SystemExit('C0-S1 outputs stale')
    else:
        OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n'); DOC.write_text(report(d))
    if not d['verification']['passed']: raise SystemExit('C0-S1 failed; retain and diagnose')
    print('C0-S1: 126 release / 42 scaling cases; verification PASS; lifetime and hardware remain open')

if __name__=='__main__':main()
