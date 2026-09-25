"""C0-S2 ideal connected lunar budget and release geometry. Adityavardhan Mishra."""
from pathlib import Path
import hashlib,json,math
import numpy as np
from scipy.integrate import solve_ivp
ROOT=Path(__file__).resolve().parents[1]
MU=4902.800118; ME=398600.435507; R=1737.4; RE=6378.137; D=384400.; G0=9.80665

def elements(r,v):
    r=np.array(r,dtype=float); v=np.array(v,dtype=float)
    energy=np.dot(v,v)/2-MU/np.linalg.norm(r)
    h=r[0]*v[1]-r[1]*v[0]
    a=-MU/(2*energy); ev=((np.dot(v,v)-MU/np.linalg.norm(r))*r-np.dot(r,v)*v)/MU
    e=float(np.linalg.norm(ev))
    return dict(a_km=float(a),e=e,peri_km=float(a*(1-e)-R),apo_km=float(a*(1+e)-R),period_s=float(2*math.pi*math.sqrt(a**3/MU)),omega_rad=float(math.atan2(ev[1],ev[0])) if e>1e-12 else 0.)

def rhs(t,y):
    return np.r_[y[2:],-MU*y[:2]/np.linalg.norm(y[:2])**3]

def run():
    rp=RE+300; at=(rp+D)/2
    ve=math.sqrt(ME/rp); vt=math.sqrt(ME*(2/rp-1/at))
    va=math.sqrt(ME*(2/D-1/at)); vm=math.sqrt(ME/D); vi=vm-va
    departure=vt-ve; tof=math.pi*math.sqrt(at**3/ME)
    transfer=dict(departure_kms=departure,arrival_vinf_kms=vi,transfer_apogee_speed_kms=va,moon_speed_kms=vm,time_days=tof/86400,required_moon_initial_phase_deg=180-math.degrees(vm/D*tof),model='Ideal coplanar tangential patched conics; no finite SOI or epoch targeting')
    cases=[]; budgets=[]; staging=[]; momentum=[]; zero=[]; closure=[]; rocket=[]
    for ha in [100,1000,10000]:
        lo=R+100; hi=R+ha; a=(lo+hi)/2
        vp=math.sqrt(MU*(2/lo-1/a)); capture=math.sqrt(vi**2+2*MU/lo)-vp
        circ=vp-math.sqrt(MU/lo); direct=math.sqrt(vi**2+2*MU/lo)-math.sqrt(MU/lo)
        closure.append(abs(capture+circ-direct))
        staging.append(dict(apo_km=ha,capture_kms=capture,circularize_kms=circ,period_h=2*math.pi*math.sqrt(a**3/MU)/3600))
        for isp in [220,320]:
            for n in [1,4,12]:
                final=300+4*n; dv=(capture+.2)*1000
                arrival=final*math.exp(dv/(G0*isp)); leo=arrival*math.exp(departure*1000/(G0*isp))
                rocket.append(abs(G0*isp*math.log(arrival/final)-dv)/dv)
                budgets.append(dict(apo_km=ha,isp_s=isp,payload_count=n,dry_plus_payload_kg=final,arrival_wet_kg=arrival,arrival_propellant_kg=arrival-final,leo_wet_if_self_departure_kg=leo,leo_propellant_if_self_departure_kg=leo-final,reserve_allowance_ms=200))
        for apsis in ['perilune','apolune']:
            x=lo if apsis=='perilune' else -hi
            vy=math.sqrt(MU*(2/abs(x)-1/a))*(1 if x>0 else -1)
            for u in [-3,-2,-.5,0,.5,2,3]:
                dp=300/304*u; dh=-4/304*u; sign=1 if x>0 else -1
                p=elements([x,0],[0,vy+sign*dp/1000]); h=elements([x,0],[0,vy+sign*dh/1000])
                momentum.append(abs(4*dp+300*dh))
                if u==0: zero.extend([abs(p['peri_km']-100)*1000,abs(p['apo_km']-ha)*1000])
                cases.append(dict(staging_apo_km=ha,apsis=apsis,u_ms=u,payload_dv_ms=dp,host_dv_ms=dh,payload=p,host=h,bound_above_sphere=p['peri_km']>0))
    nominal=next(c for c in cases if c['staging_apo_km']==1000 and c['apsis']=='perilune' and c['u_ms']==2)
    a=(2*R+1100)/2; vp=math.sqrt(MU*(2/(R+100)-1/a))+nominal['payload_dv_ms']/1000
    y0=[R+100,0,0,vp]; half=nominal['payload']['period_s']/2
    s=solve_ivp(rhs,[0,half],y0,method='DOP853',rtol=1e-11,atol=1e-12)
    tight=solve_ivp(rhs,[0,half],y0,method='DOP853',rtol=2e-13,atol=1e-14)
    endpoint=np.linalg.norm(s.y[:2,-1]-[-R-nominal['payload']['apo_km'],0])*1000
    tighten=np.linalg.norm(s.y[:2,-1]-tight.y[:2,-1])*1000
    t=np.linspace(0,2*math.pi*math.sqrt(a**3/MU),401)
    y=solve_ivp(rhs,[0,t[-1]],y0,t_eval=t,method='DOP853',rtol=1e-11,atol=1e-12).y
    energy=(y[2:]**2).sum(axis=0)/2-MU/np.linalg.norm(y[:2],axis=0)
    drift=float(np.max(abs((energy-energy[0])/energy[0])))
    checks=dict(case_count=len(cases)==42,budget_count=len(budgets)==18,momentum=max(momentum)<=1e-8,zero=max(zero)<=1e-3,capture_identity=max(closure)<=1e-9,rocket_identity=max(rocket)<=1e-12,half_period=endpoint<=.1,tolerance=tighten<=.01,energy=drift<=1e-9,finite=all(np.isfinite([departure,vi,tof,endpoint,tighten,drift])))
    result=dict(study='C0-S2',sources={'analysis_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'criteria_sha256':hashlib.sha256((ROOT/'validation/C0_S2_lunar_visual_design.md').read_bytes()).hexdigest()},assumptions=dict(mu_moon_km3s2=MU,mu_earth_km3s2=ME,moon_radius_km=R,earth_radius_km=RE,distance_km=D,payload_kg=4,host_kg=300),transfer=transfer,staging=staging,budgets=budgets,releases=cases,trace=dict(t_s=t.tolist(),xy_km=y[:2].T.tolist()),checks=checks,residuals=dict(momentum_kgms=max(momentum),zero_m=max(zero),capture_kms=max(closure),rocket_relative=max(rocket),half_period_m=endpoint,tolerance_m=tighten,energy_relative=drift),disposition='IDEAL_SCREEN_ONLY; lifetime, encounter targeting, finite burns and disposal remain open')
    out=ROOT/'analysis/results/lunar_visual_design.json';out.write_text(json.dumps(result,indent=2)+'\n')
    if not all(checks.values()):
        archive=ROOT/'validation/failures/C0_S2';archive.mkdir(parents=True,exist_ok=True)
        (archive/'original_result.json').write_bytes(out.read_bytes());(archive/'original_source.py').write_bytes(Path(__file__).read_bytes())
        raise SystemExit('FAIL: '+str(checks))
    print(json.dumps(dict(checks=checks,transfer=transfer,residuals=result['residuals']),indent=2))
if __name__=='__main__':run()
