"""Source-pinned planar two-body illustrations; no current hardware speed extension."""
import argparse,hashlib,json,math
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
H=Path(__file__).resolve().parent
MU=3.986004418e14;RE=6378137.;R=RE+600000.;VC=math.sqrt(MU/R)
SOURCES={
 'current_source':'validation/acr1/analysis/COUPLED_SHOT.json',
 'mission_mapping':'validation/acr1/mission/MISSION_INPUTS.json',
 'mission_methods':'validation/acr1/mission/MISSION_REPORT.md',
 'reference_cards':'validation/reference_interfaces_acr1/SOURCE_CARDS.json',
 'historical_speed':'README_PRE_ACR1_2026-10-23.md',
}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def analytic(t,u):
    v=VC+u;energy=v*v/2-MU/R;a=-MU/(2*energy);e=abs(R*v*v/MU-1)
    if energy<0:
        n=math.sqrt(MU/a**3);M=n*t;E=M.copy()
        for _ in range(12):E-=(E-e*np.sin(E)-M)/(1-e*np.cos(E))
        den=1-e*np.cos(E)
        return np.array([a*(np.cos(E)-e),a*np.sqrt(1-e*e)*np.sin(E),-a*n*np.sin(E)/den,a*n*np.sqrt(1-e*e)*np.cos(E)/den]).T
    n=math.sqrt(MU/(-a)**3);M=n*t;F=np.arcsinh(M/e)
    for _ in range(20):F-=(e*np.sinh(F)-F-M)/(e*np.cosh(F)-1)
    den=e*np.cosh(F)-1
    return np.array([a*(np.cosh(F)-e),-a*np.sqrt(e*e-1)*np.sinh(F),a*n*np.sinh(F)/den,-a*n*np.sqrt(e*e-1)*np.cosh(F)/den]).T
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--source-root',type=Path,required=True);args=parser.parse_args()
    repo=args.source_root;pins=[]
    for key,rel in SOURCES.items():
        p=repo/rel;pins.append(dict(id=key,path=rel,sha256=sha(p),commit='ca67ea95bf5729aa293da3728f79e23d79da9262',
            url='https://github.com/aaaaaaaaaaaavm/VOLLEY/blob/ca67ea95bf5729aa293da3728f79e23d79da9262/'+rel))
    mi=json.loads((repo/SOURCES['mission_mapping']).read_text())
    current=next(x for x in mi['critical_recoil_mapping_reference_checks'] if x['command_m_s']==3)
    current['modeled_release_m_s']=current.pop('measured_release_m_s')
    kick=current['inertial_payload_kick_m_s'];spring_mass=620.;payload=4.
    spring_kick=(1-payload/spring_mass)*1.
    preset_relative=kick/(1-payload/spring_mass)
    inputs=[('chief',0.,'unreleased circular chief'),('illustrative_low',.2,'illustrative inertial kick; outside current evaluated range'),
        ('spring1',spring_kick,'representative 1 m/s relative spring, not universal P-POD rating'),
        ('current3',kick,'source-coupled modeled ACR1 3 m/s command; finite-host mapping'),
        ('preset_match',kick,'ideal ground-preset spring matched to current inertial kick'),
        ('historical16',16.029,'historical periodic-field speed used only as kinematic input; not current rating'),
        ('future1000',1000.,'future 1 km/s inertial kinematic scenario; not achieved hardware'),
        ('future3500',3500.,'future 3.5 km/s inertial kinematic scenario; not achieved hardware')]
    times=np.linspace(0,86400,5761);states={};results=[];checks=[]
    for ident,u,meaning in inputs:
        v=VC+u
        def rhs(t,s):
            r=math.hypot(s[0],s[1]);return [s[2],s[3],-MU*s[0]/r**3,-MU*s[1]/r**3]
        solution=solve_ivp(rhs,(0,86400),[R,0,0,v],method='DOP853',rtol=2e-12,atol=1e-8,max_step=45,dense_output=True)
        assert solution.success
        sampled=solution.sol(times).T;states[ident]=sampled
        energy=v*v/2-MU/R;angular=R*v;a=-MU/(2*energy);ecc=abs(R*v*v/MU-1)
        perigee=angular**2/(MU*(1+ecc))-RE;apogee=a*(1+ecc)-RE if energy<0 else None
        period=2*np.pi*math.sqrt(a**3/MU) if energy<0 else None
        e=.5*np.sum(sampled[:,2:]**2,axis=1)-MU/np.linalg.norm(sampled[:,:2],axis=1)
        h=sampled[:,0]*sampled[:,3]-sampled[:,1]*sampled[:,2]
        independent=analytic(times,u)
        pdiff=float(np.max(np.linalg.norm(sampled[:,:2]-independent[:,:2],axis=1)))
        ediff=float(np.max(np.abs((e-energy)/energy)));hdiff=float(np.max(np.abs((h-angular)/angular)))
        assert ediff<1e-9 and hdiff<1e-9 and pdiff<.1,(ident,ediff,hdiff,pdiff)
        angle=math.atan2(sampled[-1,1],sampled[-1,0]);chief=math.sqrt(MU/R**3)*86400
        phase=math.degrees(math.atan2(math.sin(angle-chief),math.cos(angle-chief)))
        circularize=math.sqrt(MU/(RE+apogee))-angular/(RE+apogee) if apogee is not None else None
        results.append(dict(id=ident,inertial_kick_m_s=u,meaning=meaning,perigee_altitude_km=perigee/1000,
            apogee_altitude_km=None if apogee is None else apogee/1000,period_minutes=None if period is None else period/60,
            phase_24h_wrapped_deg=phase,specific_energy_J_kg=energy,specific_angular_momentum_m2_s=angular,
            semimajor_axis_m=a,eccentricity=ecc,extra_prograde_burn_at_apogee_to_circularize_m_s=circularize,
            final_state_SI=sampled[-1].tolist(),orbit_type='ellipse' if energy<0 else 'hyperbola'))
        checks.append(dict(id=ident,max_relative_energy_change=ediff,max_relative_angular_momentum_change=hdiff,
            independent_analytic_max_position_difference_m=pdiff,passed=True))
    r1=RE+500000.;r2=R;a=(r1+r2)/2
    dv1=math.sqrt(MU*(2/r1-1/a))-math.sqrt(MU/r1)
    dv2=math.sqrt(MU/r2)-math.sqrt(MU*(2/r2-1/a));transfer=math.pi*math.sqrt(a**3/MU)
    transfer_t=np.linspace(0,transfer,961)
    v1=math.sqrt(MU/r1)+dv1
    def rhs(t,s):
        r=math.hypot(s[0],s[1]);return [s[2],s[3],-MU*s[0]/r**3,-MU*s[1]/r**3]
    tr=solve_ivp(rhs,(0,transfer),[r1,0,0,v1],method='DOP853',rtol=2e-12,atol=1e-8,max_step=30,dense_output=True).sol(transfer_t).T
    assert abs(np.linalg.norm(tr[-1,:2])-r2)<.01
    assert abs(np.linalg.norm(tr[-1,2:])+dv2-math.sqrt(MU/r2))<1e-6
    assert abs(next(r for r in results if r['id']=='chief')['apogee_altitude_km']-600)<1e-8
    assert np.max(np.abs(states['current3']-states['preset_match']))==0
    assert dv1>0 and dv2>0 and next(r for r in results if r['id']=='future3500')['specific_energy_J_kg']>0
    np.savez_compressed(H/'TRAJECTORIES.npz',times_s=times,transfer_times_s=transfer_t,transfer_states=tr,**states)
    output=dict(study='FILM-PLANAR-ILLUSTRATION-01',constants=dict(mu_Earth_m3_s2=MU,reference_radius_m=RE),
        initial_altitude_km=600,host_transfer=dict(initial_altitude_km=500,target_circular_altitude_km=600,first_burn_m_s=dv1,
            second_circularizing_burn_m_s=dv2,total_m_s=dv1+dv2,coast_seconds=transfer,
            assumptions='Ideal impulsive coplanar Hohmann; generic restart-capable maneuverable host; no selected rocket/provider'),
        current_command_mapping=current,spring_example=dict(relative_speed_m_s=1,inertial_kick_m_s=spring_kick,host_plus_device_plus_payload_mass_kg=620,
            disclaimer='Representative passive P-POD-style example; neither universal product rating nor measured capability'),
        ideal_preset_spring=dict(relative_speed_m_s=preset_relative,inertial_kick_m_s=kick,
            reduced_mass_energy_J=.5*payload*(spring_mass-payload)/spring_mass*preset_relative**2,
            assumption='Ground-set ideal energy benchmark; no catalog product with this energy is selected'),
        cases=results,checks=checks,all_checks_passed=True,source_pins=pins,
        display_conventions=dict(phase='Signed Earth-centered azimuth relative to unburned circular chief after24h,wrapped to±180deg; not target accuracy',
            orbit_view='Same-plane physical position ratios, planet reference sphere; tiny offsets also shown in explicit radial/co-rotating zooms',
            future='Independent kinematic scenes, never attached to current rail'),
        limitations=['No plane-change maneuver','No navigation-accuracy claim','No terrain/drag/J2/third-body modeling','No hardware capability beyond source-supported1–3m/s commands'])
    (H/'PHYSICS_RESULTS.json').write_text(json.dumps(output,indent=2)+'\n')
    print('PASS:8 state propagations;independent elliptic/hyperbolic Kepler agreement;energy/angular momentum;zero-kick;matched preset;Hohmann arrival/circularization;escape-energy limit.')
if __name__=='__main__':main()
