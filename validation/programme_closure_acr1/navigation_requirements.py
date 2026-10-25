"""Inverse lunar release covariance requirements for a declared study accuracy.

Distinct from LNS-01: uses current study's +3m/s,100x1000km surrogate and
solves speed accuracy required by a1km3sigma osculating-perilune band.
"""
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import brentq
from scipy.special import ndtri
from scipy.stats import qmc

from lunar_native import HERE, sha


def orbit_outputs(states,mu,radius):
    r=states[:,:3];v=states[:,3:]
    rn=np.linalg.norm(r,axis=1);h=np.cross(r,v)
    e=np.linalg.norm(np.cross(v,h)/mu-r/rn[:,None],axis=1)
    energy=np.sum(v*v,axis=1)/2-mu/rn
    a=-mu/(2*energy)
    # Angle relative to nominal orbital plane; h points +Y for x-z polar case.
    normal=np.array([0,-1,0]);hunit=h/np.linalg.norm(h,axis=1)[:,None]
    plane=np.arctan2(np.linalg.norm(np.cross(hunit,normal),axis=1),hunit@normal)
    return np.stack([a*(1-e)-radius,plane],axis=1)


def main():
    c=json.loads((HERE/'study_inputs.json').read_text())['lunar'];n=c['navigation']
    mu=c['mu_moon_km3_s2']*1e9;radius=c['reference_radius_km']*1000
    ra=radius+n['case_apolune_km']*1000;rp=radius+c['staging_perilune_km']*1000
    v=math.sqrt(mu*(2/ra-2/(ra+rp)));alpha=c['retained_host_kg']/(c['retained_host_kg']+c['payload_kg'])
    u=n['relative_command_m_s'];nominal=np.array([ra,0,0,0,0,v+alpha*u])
    # Positive x at apolune,+z velocity gives nominal h=-Y.
    nominal_output=orbit_outputs(nominal[None,:],mu,radius)[0]
    def states(errors,speed_sigma,pointing_sigma_deg=None):
        state=np.tile(nominal,(len(errors),1))
        state[:,:3]+=errors[:,:3]*n['position_1sigma_m']
        state[:,3:]+=errors[:,3:6]*n['velocity_1sigma_m_s']
        pointing_band=n['pointing_1sigma_deg'] if pointing_sigma_deg is None else pointing_sigma_deg
        yaw=errors[:,6]*math.radians(pointing_band)
        pitch=errors[:,7]*math.radians(pointing_band)
        release=(u+errors[:,8]*speed_sigma)*alpha
        dirs=np.stack([np.sin(pitch),np.cos(pitch)*np.sin(yaw),np.cos(pitch)*np.cos(yaw)],axis=1)
        state[:,3:]+=dirs*release[:,None]-np.array([0,0,alpha*u])
        return state
    # Independent symmetric differences for first-order periapsis Jacobian.
    def jac(step):
        basis=np.eye(9)*step
        plus=orbit_outputs(states(basis,1),mu,radius)[:,0]
        minus=orbit_outputs(states(-basis,1),mu,radius)[:,0]
        return (plus-minus)/(2*step)
    j=jac(0.01);jfine=jac(0.005)
    # Jacobian input9 is1m/s speed error; all remaining errors use fixed bands.
    nav_variance=np.dot(j[:8],j[:8]);budget=(n['study_perilune_error_3sigma_m']/3)**2-nav_variance
    speed_sigma=math.sqrt(budget)/abs(j[8]) if budget>0 else 0
    # Independent fixed-seed scrambled Sobol normal draws. Keep4K/16K results
    # to expose finite-sample tail variation; no measured success probability.
    z=ndtri(qmc.Sobol(9,scramble=True,seed=n['seed']).random_base2(n['sample_power']))
    def quantile_halfwidth(sigma):
        out=orbit_outputs(states(z,sigma),mu,radius)[:,0]-nominal_output[0]
        q=np.quantile(out,[0.00135,0.99865]);return max(abs(q))
    mc_sigma=brentq(lambda sig:quantile_halfwidth(sig)-n['study_perilune_error_3sigma_m'],0,1)
    # Solve the angular budget independently while holding the calibrated speed
    # error fixed. Large pointing errors also change along-track energy, so these
    # two independently saturated budgets must not be combined as a joint pass.
    def plane_quantile(pointing):
        out=orbit_outputs(states(z,mc_sigma,pointing),mu,radius)
        return float(np.quantile(out[:,1],.9973))
    mc_pointing=brentq(lambda deg:plane_quantile(deg)-n['study_plane_error_3sigma_rad'],0,90)
    # Conservative single-axis first-order plane requirement after accounting
    # for independent host nav position/normal velocity; pointing is not a
    # validated mechanical accuracy and the final MC uses the declared0.1deg.
    plane_nav_sigma=math.sqrt((n['velocity_1sigma_m_s']/(v+alpha*u))**2+(n['position_1sigma_m']/ra)**2)
    remaining=(n['study_plane_error_3sigma_rad']/3)**2-plane_nav_sigma**2
    pointing_sigma=math.sqrt(remaining)*(v+alpha*u)/(alpha*u) if remaining>0 else 0
    records=[]
    for size in [4096,len(z)]:
        outputs=orbit_outputs(states(z[:size],mc_sigma),mu,radius)
        peri_error=outputs[:,0]-nominal_output[0]
        records.append(dict(samples=size,perilune_error_mean_m=float(np.mean(peri_error)),
                            perilune_error_std_m=float(np.std(peri_error,ddof=1)),
                            perilune_error_quantiles_m=np.quantile(peri_error,[.00135,.5,.99865]).tolist(),
                            plane_error_99p73pct_rad=float(np.quantile(outputs[:,1],.9973)),
                            minimum_osculating_perilune_altitude_m=float(np.min(outputs[:,0]))))
    result=dict(study='PCS-LUNAR-COVARIANCE-01',source_sha256=sha(__file__),inputs_sha256=sha(HERE/'study_inputs.json'),
                requirements=n,nominal_osculating_perilune_altitude_m=float(nominal_output[0]),
                assumed_independent_normal_inputs=True,
                finite_difference_relative_refinement=float(np.linalg.norm(j-jfine)/np.linalg.norm(jfine)),
                linear_speed_1sigma_requirement_m_s=speed_sigma,
                finite_sample_speed_1sigma_requirement_m_s=mc_sigma,
                finite_sample_speed_3sigma_requirement_m_s=3*mc_sigma,
                necessary_command_increment_if_uniform_quantization_alone_m_s=math.sqrt(12)*mc_sigma,
                linear_single_axis_pointing_1sigma_budget_deg=math.degrees(pointing_sigma),
                finite_sample_pointing_1sigma_budget_deg=mc_pointing,
                finite_sample_pointing_3sigma_budget_deg=3*mc_pointing,
                saturated_pointing_band_plane_99p73pct_rad=plane_quantile(mc_pointing),
                monte_carlo=records,
                interpretation='Study targets, not customer requirements. Increment is an upper necessary bound if quantization alone uses the entire speed budget; shared error allocation requires finer increments. Speed/pointing limits are independently saturated and cannot be combined as a joint accuracy guarantee; joint MC uses fixed0.1deg pointing.',
                limits='Two-body osculating-element covariance at release; no perturbed30day covariance/terrain/contact or measured accuracy. Native nominal lifetime results remain separate.')
    (HERE/'NAVIGATION_REQUIREMENTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['finite_difference_relative_refinement','finite_sample_speed_3sigma_requirement_m_s','linear_single_axis_pointing_1sigma_budget_deg']},indent=2))


if __name__=='__main__':main()
