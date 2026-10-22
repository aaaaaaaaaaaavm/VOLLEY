"""Reproduce the captured ideal lunar/separation bounds from public inputs only.

No orbit integration, provider retrieval, hardware selection or task-status logic.
Archived source files in inputs are read for identity checks, never executed.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import os

ROOT = Path(__file__).resolve().parent
INPUTS = ROOT / "inputs"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def build():
    """The same arithmetic and numerical checks used for the captured results."""
    I = INPUTS
    s1 = json.loads((I / "lunar_release_scaling.json").read_text())
    s2 = json.loads((I / "lunar_visual_design.json").read_text())
    assert len(s1['release_cases'])==126 and len(s1['scaling_cases'])==42 and len(s2['releases'])==42 and len(s2['budgets'])==18
    assert s1['verification']['passed'] and all(s2['checks'].values())
    MU=s1['inputs']['lunar_mu_m3_s2'];R=s1['inputs']['lunar_radius_m'];ME=s1['inputs']['earth_mu_m3_s2'];RE=s1['inputs']['earth_radius_m'];DIST=s1['inputs']['reference_distance_m'];G0=9.80665
    M=float(s2['assumptions']['host_kg']);m=float(s2['assumptions']['payload_kg']);alpha=M/(M+m);U=max(r['relative_speed_m_s'] for r in s1['release_cases']);required_u=1000.
    assert MU==s2['assumptions']['mu_moon_km3s2']*1e9 and R==s2['assumptions']['moon_radius_km']*1000
    provenance=[]
    for path,digest in s1['source_sha256'].items():
     p=I/Path(path).name;provenance.append({'study':'C0-S1','source':path,'stored_sha256':digest,'current_sha256':sha(p),'matches':sha(p)==digest})
    for path,key in [('analysis/lunar_visual_design.py','analysis_sha256'),('validation/C0_S2_lunar_visual_design.md','criteria_sha256')]:
     p=I/Path(path).name;provenance.append({'study':'C0-S2','source':path,'stored_sha256':s2['sources'][key],'current_sha256':sha(p),'matches':sha(p)==s2['sources'][key]})
    # Reconstruct stored S1 apsides algebraically. Do not repeat its Cartesian ODE checks.
    def elements(radius,speed):
     energy=speed**2/2-MU/radius;h=radius*speed;e=abs(radius*speed**2/MU-1);rp=h*h/MU/(1+e)
     a=-MU/(2*energy) if energy else None
     return {'specific_energy_J_kg':energy,'bound':energy<0,'periapsis_altitude_km':(rp-R)/1000,'apoapsis_altitude_km':(a*(1+e)-R)/1000 if energy<0 else None}
    apsis_errors=[];momentum_errors=[]
    for c in s1['release_cases']:
     rp=R+c['staging_periapsis_km']*1000;ra=R+c['staging_apoapsis_km']*1000;a=(rp+ra)/2;r=rp if c['release_at']=='periapsis' else ra;v=math.sqrt(MU*(2/r-1/a));mp=c['payload_kg'];mh=c['retained_host_kg'];u=c['relative_speed_m_s'];dp=mh/(mp+mh)*u;dh=-mp/(mp+mh)*u
     momentum_errors.append(abs(mp*dp+mh*dh))
     for role,dv in [('payload',dp),('host',dh)]:
      result=elements(r,v+dv)
      for k in ['periapsis_altitude_km','apoapsis_altitude_km']:apsis_errors.append(abs(result[k]-c[role][k])*1000)
    # Connect the same ideal transfer algebraically; the source's encounter limits remain.
    r0=RE+300000.;at=(r0+DIST)/2;vt=math.sqrt(ME*(2/r0-1/at));vleo=math.sqrt(ME/r0);va_transfer=math.sqrt(ME*(2/DIST-1/at));vmoon=math.sqrt(ME/DIST);vinf=vmoon-va_transfer;departure=vt-vleo
    transfer_errors=[abs(departure-s2['transfer']['departure_kms']*1000),abs(vinf-s2['transfer']['arrival_vinf_kms']*1000)]
    disposal=[];capture=[];release_margin=[]
    for staging in s2['staging']:
     ha=staging['apo_km'];rp=R+100000.;ra=R+ha*1000.;a=(rp+ra)/2;vp=math.sqrt(MU*(2/rp-1/a));va=math.sqrt(MU*(2/ra-1/a));vc=math.sqrt(MU/rp);vin=math.sqrt(vinf*vinf+2*MU/rp)
     capture.append({'staging_apo_km':ha,'capture_m_s':vin-vp,'later_circularization_m_s':vp-vc,'capture_plus_circularization_m_s':vin-vc,'stored_capture_error_m_s':abs(vin-vp-staging['capture_kms']*1000),'stored_circularization_error_m_s':abs(vp-vc-staging['circularize_kms']*1000)})
     vgrazing=math.sqrt(2*MU*R/(ra*(ra+R)));dv_grazing=va-vgrazing;dv_escape=math.sqrt(2*MU/rp)-vp
     disposal.append({'staging_apo_km':ha,'retrograde_at_apo_to_reference_sphere_grazing_m_s':dv_grazing,'prograde_at_peri_to_zero_escape_energy_m_s':dv_escape,'assumed_200m_s_allowance_minus_ideal_escape_m_s':200-dv_escape,'interpretation':'reference-sphere grazing/zero-energy escape thresholds only; not controlled disposal, Earth return, stable high-lunar orbit or terrain/epoch solution'})
     ucrit=(vgrazing-va)/alpha;vnom=va-alpha*U;enom=elements(ra,vnom);derivative=alpha*4*MU*ra*ra*vnom/(2*MU-ra*vnom*vnom)**2/1000
     release_margin.append({'staging_apo_km':ha,'release_at':'apoapsis','nominal_relative_command_m_s':-U,'nominal_periapsis_altitude_km':enom['periapsis_altitude_km'],'relative_command_for_reference_sphere_grazing_m_s':ucrit,'remaining_adverse_command_margin_m_s':-U-ucrit,'local_periapsis_sensitivity_km_per_m_s':derivative,'interpretation':'deterministic tangential one-variable screen; no navigation, pointing or stochastic/3sigma requirement is supplied'})
    # Lower bounds for the declared 4kg/300kg two-body, massless-pusher screen.
    energy=.5*m*M/(m+M)*required_u**2;oldenergy=.5*m*M/(m+M)*U**2
    acceleration=[{'payload_acceleration_study_g':g,'constant_force_relative_stroke_m':alpha*required_u**2/(2*g*G0),'zero_end_preload_linear_spring_relative_stroke_m':alpha*required_u**2/(g*G0),'payload_force_at_study_acceleration_N':m*g*G0} for g in [3.,10.,25.]]
    lengths=[(.08,'historical MC-L2 working-stroke reference; C0-S2 criteria; retired bank architecture'),(.25,'reference_architecture.py compact-stroke study screen'),(1.3,'historical Gen5 acceleration zone; EMOCD_Computation_Results_C1-C10.md'),(1.5,'optimistic entire historical Gen5 track, including coast/trim')]
    compact=[{'relative_stroke_m':s,'source_context':label,'minimum_peak_payload_acceleration_g':alpha*required_u**2/(2*s*G0),'max_relative_speed_at_25g_m_s':math.sqrt(2*25*G0*s/alpha)} for s,label in lengths]
    vc=math.sqrt(MU/(R+100000.));high_release=[]
    for sign in [-1,1]:high_release.append({'relative_speed_m_s':sign*required_u,'payload_delta_v_m_s':sign*alpha*required_u,**elements(R+100000.,vc+sign*alpha*required_u)})
    # Translation-only campaign: mass changes after each shot; bound coherent recoil.
    campaign=[]
    for n in [1,4,12]:
     contributions=[m*U/(M+m*k) for k in range(1,n+1)];total_energy=sum(.5*m*(M+m*(k-1))/(M+m*k)*required_u**2 for k in range(1,n+1))
     campaign.append({'payload_count':n,'payload_kg_each':m,'retained_non_payload_kg':M,'initial_carried_mass_kg':M+n*m,'max_coherent_recoil_magnitude_at_U_m_s':sum(contributions),'no_release_recoil_m_s':0.,'ideal_added_energy_at_1000m_s_J':total_energy,'scope':'algebraic translation-only bound; no burns, attitude/inertia, optimized order, navigation, thermal services or actual campaign feasibility'})
    mass_boundary=[];rocket_errors=[]
    for b in s2['budgets']:
     ratio=b['leo_wet_if_self_departure_kg']/b['arrival_wet_kg'];expected=math.exp(departure/(G0*b['isp_s']));rocket_errors.append(abs(ratio/expected-1))
     if b['apo_km']==100:mass_boundary.append({**b,'self_departure_to_launcher_departure_wet_mass_ratio':ratio})
    checks={'S1_case_counts':len(s1['release_cases'])==126 and len(s1['scaling_cases'])==42,'S1_sources_and_criteria_hash_match':all(p['matches'] for p in provenance if p['study']=='C0-S1'),'S1_stored_apsides_reconstructed_within_original_1mm_band':max(apsis_errors)<=1e-3,'momentum_within_original_1e_minus8_band':max(momentum_errors)<=1e-8,'connected_ideal_transfer_reconstructed_within_1e_minus6_m_s':max(transfer_errors)<=1e-6,'S2_capture_identity_and_stored_values_within_original_1e_minus6_m_s_band':max(abs(c['capture_plus_circularization_m_s']-(s2['staging'][0]['capture_kms']*1000)) for c in capture)<=1e-6 and max(c['stored_capture_error_m_s'] for c in capture)<=1e-6 and max(c['stored_circularization_error_m_s'] for c in capture)<=1e-6,'rocket_boundary_identity_within_original_1e_minus12_relative_band':max(rocket_errors)<=1e-12,'constant_force_work_identity_1e_minus12_relative':all(abs(m*x['payload_acceleration_study_g']*G0*x['constant_force_relative_stroke_m']/energy-1)<1e-12 for x in acceleration),'sphere_grazing_reconstruction_1mm':all(abs(elements(R+x['staging_apo_km']*1000,math.sqrt(MU*(2/(R+x['staging_apo_km']*1000)-2/(2*R+100000+x['staging_apo_km']*1000)))-x['retrograde_at_apo_to_reference_sphere_grazing_m_s'])['periapsis_altitude_km'])<=1e-6 for x in disposal)}
    assert all(checks.values()),checks

    return {
        "study": "BB52 analytical lunar and high-speed feasibility bounds",
        "scope": "Ideal surrogate-case bounds only; no lifetime, provider, hardware or flight qualification",
        "source_sha256": sha(Path(__file__)),
        "source_provenance": provenance,
        "inputs": {
            "payload_kg": m, "retained_host_kg": M, "g0_m_s2": G0,
            "legacy_relative_speed_m_s": U, "required_speed_investigation_m_s": required_u,
            "mu_moon_m3_s2": MU, "moon_reference_radius_m": R,
            "basis": "GM/radii/scenarios reused from C0-S1/C0-S2; 25g is a historical study ceiling, not a payload rating; 1000m/s is a declared investigation point"
        },
        "checks": checks,
        "residuals": {
            "max_stored_S1_apsis_error_m": max(apsis_errors),
            "max_momentum_residual_kg_m_s": max(momentum_errors),
            "max_transfer_reconstruction_error_m_s": max(transfer_errors),
            "max_boundary_rocket_relative_error": max(rocket_errors)
        },
        "B1_capture_and_carrier_boundary": {"transfer": s2["transfer"], "capture": capture, "circular_target_mass_cases": mass_boundary},
        "B2_engine_only_disposal_thresholds": disposal,
        "B3_tangential_release_margin": release_margin,
        "B3_low_circular_1000m_s_cases": high_release,
        "B4_translation_only_campaign_bound": campaign,
        "B5_high_speed": {
            "ideal_added_relative_energy_J": energy,
            "legacy_speed_ideal_relative_energy_J": oldenergy,
            "energy_ratio_to_legacy_speed": energy / oldenergy,
            "stroke_at_acceleration_screens": acceleration,
            "compact_stroke_screens": compact,
            "bus_energy_boundary": "E_bus >= E_relative/eta for efficiency0<eta<=1, with pusher/friction/charging/catcher burden extra. No efficiency, power availability or installed energy store is supplied."
        },
        "unresolved_provenance": "The supplied current C0-S2 criteria hash differs from its original result's recorded criteria hash. The mismatch is retained; no stored hash or numerical threshold has been replaced."
    }

def make_figure(data, output_dir):
    """Recreate the captured plot from the same calculated values."""
    os.environ.setdefault("MPLCONFIGDIR", str(output_dir / ".mpl-cache"))
    M = data["inputs"]["retained_host_kg"]
    m = data["inputs"]["payload_kg"]
    G0 = data["inputs"]["g0_m_s2"]
    alpha = M / (M + m)
    capture = data["B1_capture_and_carrier_boundary"]["capture"]
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    speeds=[10**(3*j/149) for j in range(150)]
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42,'svg.fonttype':'none'})
    fig,axs=plt.subplots(1,2,figsize=(10.6,3.8),layout='constrained')
    for g,color in [(3,'#0072B2'),(10,'#D55E00'),(25,'#009E73')]:axs[0].loglog(speeds,[alpha*u*u/(2*g*G0) for u in speeds],label=f'{g} g study screen',color=color)
    for length,label in [(.08,'0.08 m historical cell'),(.25,'0.25 m compact screen'),(1.3,'1.3 m Gen5 acceleration zone')]:axs[0].axhline(length,color='#777777',lw=.7,ls=':');axs[0].text(1.12,length*1.08,label,fontsize=6.7,color='#444444')
    axs[0].axvline(1000,color='#333333',lw=.7,ls='--');axs[0].set(xlabel='Required relative speed [m/s]',ylabel='Ideal minimum relative stroke [m]',title='Constant force, 4 kg payload / 300 kg host');axs[0].legend(loc='upper left',fontsize=7.3);axs[0].grid(True,which='both',alpha=.16)
    x=range(3);cap=[c['capture_m_s'] for c in capture];circ=[c['later_circularization_m_s'] for c in capture]
    axs[1].bar(x,cap,color='#D55E00',label='Capture into staging orbit');axs[1].bar(x,circ,bottom=cap,color='#009E73',label='Later circularization at 100 km');axs[1].set_xticks(list(x),['100 × 100','100 × 1,000','100 × 10,000']);axs[1].set(xlabel='Initial lunar staging altitudes [km]',ylabel='Ideal carrier impulse [m/s]',title='Same final circular orbit: 821.239 m/s in each case');axs[1].legend(loc='upper center',fontsize=7.2);axs[1].set_ylim(0,1020);axs[1].grid(axis='y',alpha=.16)
    fig.suptitle('BB52: conditional feasibility bounds; no lifetime, provider or hardware closure',fontsize=11)
    for ext in ['png','pdf','svg']:fig.savefig(output_dir/('feasibility_bounds.'+ext),dpi=190)
    plt.close(fig)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, help="Write recalculated JSON and figures here; otherwise print JSON only")
    args = parser.parse_args()
    data = build()
    if args.output_dir:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        (args.output_dir / "NUMERICAL_BOUNDS.json").write_text(json.dumps(data, indent=2) + "\n")
        make_figure(data, args.output_dir)
    else:
        print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()
