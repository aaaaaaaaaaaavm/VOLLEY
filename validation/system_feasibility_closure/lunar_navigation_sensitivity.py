"""Parametric lunar release uncertainty in a two-body osculating-orbit model.

This is an uncalibrated sensitivity study. The covariance bands are declared
investigation inputs, not measured navigation or mechanism performance.
Reference-sphere crossing is not a terrain/lifetime or controlled-impact result.
"""
from pathlib import Path
import hashlib,json,math
import numpy as np

H=Path(__file__).resolve().parent
MU=4902800118000.;R=1737400.;ALPHA=300/304
U=-4.569852054443217


def periapsis(states):
    a=np.asarray(states)
    if a.ndim==1:a=a[None,:]
    r=a[:,:3];v=a[:,3:];rr=np.linalg.norm(r,axis=1)
    h=np.cross(r,v);hh=np.sum(h*h,axis=1)
    ev=np.cross(v,h)/MU-r/rr[:,None]
    ecc=np.linalg.norm(ev,axis=1)
    return hh/(MU*(1+ecc))-R


def nominal(apo_km):
    rp=R+100e3;ra=R+apo_km*1e3
    v=math.sqrt(MU*(2/ra-2/(rp+ra)))
    return np.array([ra,0,0,0,v+ALPHA*U,0.])


def jac(state,scale):
    d=np.array([.1,.1,.1,.0001,.0001,.0001])*scale
    return np.array([(periapsis(state+np.eye(6)[i]*d[i])[0]-periapsis(state-np.eye(6)[i]*d[i])[0])/(2*d[i]) for i in range(6)])


def compute(samples=8192):
    bands=[dict(name='tight_study_band',position_1sigma_m=10.,velocity_1sigma_m_s=.01,pointing_1sigma_deg=.01,relative_speed_1sigma_fraction=.001),
      dict(name='middle_study_band',position_1sigma_m=100.,velocity_1sigma_m_s=.1,pointing_1sigma_deg=.1,relative_speed_1sigma_fraction=.01),
      dict(name='wide_study_band',position_1sigma_m=1000.,velocity_1sigma_m_s=1.,pointing_1sigma_deg=1.,relative_speed_1sigma_fraction=.05)]
    rng=np.random.default_rng(20261023)
    z=rng.standard_normal((samples,9))
    results=[];checks=[]
    for apo in (100,1000,10000):
        state=nominal(apo);J=jac(state,1);J2=jac(state,2)
        diff=float(np.linalg.norm(J-J2)/max(np.linalg.norm(J),1))
        assert diff<1e-4
        checks.append(dict(staging_apoapsis_km=apo,jacobian_relative_refinement_difference=diff,pass_1e_minus4=True))
        for b in bands:
            p=b['position_1sigma_m'];vel=b['velocity_1sigma_m_s'];ang=math.radians(b['pointing_1sigma_deg']);us=abs(U)*b['relative_speed_1sigma_fraction']
            # Correlations are explicitly zero; a real delivery covariance may be correlated.
            sigma=np.array([p,p,p,math.sqrt(vel**2+(ALPHA*U*ang)**2),math.sqrt(vel**2+(ALPHA*us)**2),math.sqrt(vel**2+(ALPHA*U*ang)**2)])
            linear_sigma=float(math.sqrt(np.sum((J*sigma)**2)))
            x=np.tile(state,(samples,1))
            x[:,:3]+=z[:,:3]*p
            x[:,3:]+=z[:,3:6]*vel
            yaw=z[:,6]*ang;pitch=z[:,7]*ang;du=z[:,8]*us
            speed=U+du
            direction=np.c_[np.sin(yaw)*np.cos(pitch),np.cos(yaw)*np.cos(pitch),np.sin(pitch)]
            release=ALPHA*speed[:,None]*direction
            x[:,3:]+=release-np.array([0.,ALPHA*U,0.])
            per=periapsis(x)
            stats=[]
            for n in (samples//2,samples):
                q=np.quantile(per[:n],[.00135,.025,.5,.975,.99865])
                stats.append(dict(samples=n,mean_periapsis_altitude_m=float(per[:n].mean()),std_periapsis_altitude_m=float(per[:n].std(ddof=1)),
                    quantiles_m=dict(zip(['0.135pct','2.5pct','50pct','97.5pct','99.865pct'],map(float,q))),
                    sampled_fraction_osculating_periapsis_below_reference_sphere=float(np.mean(per[:n]<0))))
            results.append(dict(staging_apoapsis_km=apo,staging_periapsis_km=100,relative_command_m_s=U,
                nominal_payload_periapsis_altitude_m=float(periapsis(state)[0]),assumed_band=b,
                linearized_periapsis_1sigma_m=linear_sigma,finite_sample=stats,
                caveat='Distribution is conditional on assumed independent Gaussian inputs; no measured reliability or lunar useful lifetime follows.'))
    return dict(study='LNS-01 parametric lunar release navigation sensitivity',source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        model='two-body lunar osculating periapsis at apolune release; no orbit lifetime integration',
        constants=dict(mu_moon_m3_s2=MU,moon_reference_radius_m=R,payload_kg=4.,retained_host_kg=300.),
        assumptions=['independent zero-mean Gaussian errors','declared investigation covariance bands, not supplier/customer/measured data',
          'spherical lunar reference surface, no terrain, lunar harmonics, solar/Earth perturbation, coverage or communications',
          'point release, no finite release interval or payload attitude dynamics'],
        finite_difference_checks=checks,cases=results)


if __name__=='__main__':
    r=compute();(H/'LUNAR_NAVIGATION_SENSITIVITY.json').write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(dict(cases=len(r['cases']),checks=r['finite_difference_checks'])))
