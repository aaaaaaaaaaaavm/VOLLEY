#!/usr/bin/env python3
"""Make figures and a bounded scientific report from actual SD01 capture files."""
from pathlib import Path
import hashlib,json,os,subprocess
os.environ.setdefault('MPLCONFIGDIR','/tmp/volley-sd-mpl');os.environ.setdefault('XDG_CACHE_HOME','/tmp/volley-sd-cache')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
H=Path(__file__).resolve().parent;R=H.parents[1];O=H/'figures';O.mkdir(exist_ok=True)
m=json.loads((H/'MODAL_RESULTS.json').read_text());d=json.loads((H/'RESPONSE_RESULTS.json').read_text());n=json.loads((H/'CURRENT_NORMAL_FORCE.json').read_text());b=np.load(H/'MODAL_BASIS.npz');c=np.load(H/'RESPONSE_CURVES.npz');plt.style.use(H/'scientific.mplstyle')
figures=[]
def save(fig,name,caption):
 fig.tight_layout();files={}
 for suffix in ['png','pdf','svg']:
  p=O/f'{name}.{suffix}';fig.savefig(p,dpi=260);files[p.relative_to(H).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
 plt.close(fig);figures.append({'id':name,'caption':caption,'evidence_class':'Model output from captured native modes and declared forcing; not hardware or GUI evidence','exports':files})
fig,ax=plt.subplots(1,2,figsize=(10.2,3.7));freq=np.array(m['elastic_frequencies_Hz']);ax[0].plot(np.arange(1,41),freq,'o-',ms=3);ax[0].set(xlabel='Elastic mode index (six rigid modes excluded)',ylabel='Bare chassis frequency (Hz)',title='Native CalculiX 2.23, actual C3D10 chassis')
mode=int(np.argmax(np.max(np.abs(b['D_paired']),axis=0)*np.abs(b['G_normal_per_N'])/b['omega_rad_s']**2));xy=b['query_xy_mm'];shape=b['D_paired'][:,mode];p=ax[1].tricontourf(xy[:,0],xy[:,1],shape/np.max(np.abs(shape)),levels=np.linspace(-1,1,21),cmap='coolwarm');fig.colorbar(p,ax=ax[1],label='Normalized differential face mode shape');ax[1].set(xlabel='Source X (mm)',ylabel='Source Y (mm)',title=f'Native mode{int(b["mode_numbers"][mode])}: {freq[mode]:.3f}Hz; arbitrary display scale');save(fig,'SD01_modes','Forty actual free-free elastic modes. The face map is a numerical native modal field, normalized for display; no physical amplitude is implied.')
fig,ax=plt.subplots(3,1,figsize=(9.8,7),sharex=True);ax[0].plot(c['time_s'],c['axial_force_N'],label='Reconstructed source axial force');ax[0].plot(c['time_s'],c['normal_ripple_N'],label='Declared 5% normal ripple sensitivity',alpha=.8);ax[0].set(ylabel='Force (N)',title='Principal 3 m/s finite-shot sensitivity; 0.5% damping, uniform loaded-mass scale');ax[0].legend();ax[1].plot(c['time_s'],c['paired_closure_increment_bound_mm'],label='Modal triangle bound over sampled faces');ax[1].plot(c['time_s'],c['control_point_incremental_closure_mm'],label='Actual control-point peak');ax[1].axhline(d['available_paired_budget_before_dynamic_mm'],ls='--',color='black',label='Remaining paired budget before dynamics');ax[1].set(ylabel='Incremental paired closure (mm)');ax[1].legend();ax[2].plot(c['time_s'],c['conditional_paired_remaining_mm']);ax[2].axhline(0,color='black',ls='--');ax[2].set(xlabel='Time (s)',ylabel='Conditional paired margin (mm)');save(fig,'SD01_finite_response','Finite acceleration/release/brake history with explicit normal ripple. Paired margin retains original static/thermal/tolerance allocations and an additional modal residual reserve; individual centring/stator dynamics remain conditional.')
fig,ax=plt.subplots(figsize=(9.8,3.8));ax.semilogy(c['frequency_Hz'],c['transfer_mm_per_N_bound']);ax.set(xlabel='Harmonic excitation frequency (Hz)',ylabel='Paired compliance bound (mm/N)',title='Steady dwell sensitivity: uniform loaded-mass scale, 0.5% damping');ax.grid(True,which='both',alpha=.3);save(fig,'SD01_harmonic_limit','A sustained harmonic is separate from the finite chirp. Resonance gives a source-dependent normal-force design limit; the assumed damping and actual assembly spectrum are unmeasured.')
records=n['records'];labels=[f"{r['displacement_m']*1000:g}mm\n"+('FE current'if'FE-current'in r['method']else'refined'if'refined'in r['method']else'uniform')for r in records];ideal=[abs(r['ideal_max_thrust_phase_opposed_normal_N'])for r in records];anyphase=[r['opposed_normal_envelope_at_supported_current_N']for r in records];err5=[r['phase_error_brackets']['5']['max_abs_opposed_normal_N']for r in records];err15=[r['phase_error_brackets']['15']['max_abs_opposed_normal_N']for r in records];limit=min(x['normal_ripple_limit_N']for x in d['harmonic_design_limits']);fig,ax=plt.subplots(figsize=(10,4.2));x=np.arange(len(records));ax.semilogy(x,ideal,'o-',label='Ideal maximum-thrust phase (absolute)');ax.semilogy(x,err5,'s-',label='±5° phase sensitivity');ax.semilogy(x,err15,'^-',label='±15° phase sensitivity');ax.semilogy(x,anyphase,'x--',label='Any balanced electrical phase');ax.axhline(limit,color='black',ls=':',label=f'Continuous resonant screen: {limit:.2f}N');ax.set_xticks(x,labels);ax.set(ylabel='Modeled opposed normal reaction (N)',title=f'Representative current/PM reaction at supported maximum {n["supported_max_phase_current_A"]:.3f}A');ax.legend(ncol=2);save(fig,'SD01_current_normal','Per-array reciprocal J×B force with PM top/bottom fields separated. Representative source stations only; DC pinch is excluded from these alternating current-force curves.')
worst=min(d['finite_cases'],key=lambda q:q['paired_remaining_budget_mm']);fine=d['response_convergence'][-1];fine_margin=d['available_paired_budget_before_dynamic_mm']-fine['paired_closure_bound_mm'];critical=min(d['harmonic_design_limits'],key=lambda q:q['normal_ripple_limit_N']);representative_max=max(anyphase);ideal_max=max(ideal);phase5max=max(err5);phase15max=max(err15);theta=np.linspace(0,np.pi/2,18001);Cphase=[]
for rec in records:
 coeff=np.array(rec['per_array_per_phase_field_XYZ_N_per_A']);phasors=np.exp(1j*np.array([0,-2*np.pi/3,2*np.pi/3]));Cx=coeff[:,:,0].sum(axis=0)@phasors;Cp=((coeff[0,:,1]-coeff[1,:,1])/2)@phasors;opt=np.pi/2-np.angle(Cx);Cphase.append(np.maximum(abs(np.imag(np.exp(1j*(opt+theta))*Cp)),abs(np.imag(np.exp(1j*(opt-theta))*Cp)))*n['supported_max_phase_current_A'])
envelope=np.max(Cphase,axis=0);allow=np.max(theta[envelope<=critical['normal_ripple_limit_N']])*180/np.pi
comparison={'representative_ideal_phase_max_absolute_normal_N':ideal_max,'representative_5deg_phase_error_normal_N':phase5max,'representative_15deg_phase_error_normal_N':phase15max,'representative_arbitrary_phase_normal_N':representative_max,'minimum_continuous_harmonic_normal_limit_N':critical['normal_ripple_limit_N'],'conditional_station_based_phase_error_limit_deg':float(allow),'fine_step_finite_paired_margin_mm':float(fine_margin),'limit_boundary':'Conditional numerical design screen over tested stations and 1–500Hz, not a certified global phase/error/ripple allowance.'}
original_vector_reference=json.loads((R/'validation/acr1/analysis/CURRENT_FIELD_FORCE.json').read_text())
fe=next(r for r in records if 'FE-current' in r['method']);refined=next(r for r in records if 'refined' in r['method'])
assert abs(fe['axial_amplitude_N_per_peak_A']-original_vector_reference['force_amplitude_N_per_peak_phase_A'])<1e-10
comparison['frozen_scalar_X_reproduction_absolute_error_N_per_A']=abs(fe['axial_amplitude_N_per_peak_A']-original_vector_reference['force_amplitude_N_per_peak_phase_A'])
comparison['FE_vs_refined_uniform_normal_relative_difference']=abs(fe['opposed_normal_envelope_at_supported_current_N']-refined['opposed_normal_envelope_at_supported_current_N'])/refined['opposed_normal_envelope_at_supported_current_N']
(H/'PHYSICS_LIMIT_COMPARISON.json').write_text(json.dumps(comparison,indent=2)+'\n')
rows='\n'.join(f"| {r['displacement_m']*1000:.0f} | {r['method']} | {abs(r['ideal_max_thrust_phase_opposed_normal_N']):.4f} | {r['phase_error_brackets']['5']['max_abs_opposed_normal_N']:.3f} | {r['phase_error_brackets']['15']['max_abs_opposed_normal_N']:.3f} | {r['opposed_normal_envelope_at_supported_current_N']:.3f} |"for r in records)
report=f'''# ACR1 structural dynamics and conditional airgap screen

**Study SD01; 25 October 2026. Separate follow-on evidence.** Frozen ACR1 geometry, original static/ED1 captures and report operating-point identities remain unchanged. This study supplies genuine native modal extraction and bounded numerical forcing/airgap decisions; it does not qualify the complete installed assembly.

## Result and design decision

The actual connected chassis mesh yields six numerical rigid modes and **40 elastic modes from {freq[0]:.4f} to {freq[-1]:.3f} Hz**. All **54 finite principal-3 m/s sensitivity cases** retain positive conditional paired clearance. The adverse 50 µs refinement has **{fine['paired_closure_bound_mm']:.6f} mm** incremental paired closure bound and **{fine_margin:.6f} mm** paired budget remaining. This relies on the original guide/flatness/assembly/thermal allocations and stationary-stator/centring boundary.

A continuous resonant load is an adverse case: with assumed 0.5% damping the conservative modeled normal-force limit is **{critical['normal_ripple_limit_N']:.3f} N** (about **{critical['allowable_normal_ripple_fraction_for_existing_budget']*100:.3f}%** of DC pinch). A sustained 5% harmonic exceeds this conditional budget. It must not be confused with a brief swept passage in the finite shot.

The representative current/PM calculation gives ideal maximum-thrust-phase opposed normal reaction at most **{ideal_max:.3f} N**, including sampled arrest positions. At the supported current maximum, the representative ±5° and ±15° phase sensitivities reach **{phase5max:.3f} N** and **{phase15max:.3f} N**. The arbitrary balanced-phase envelope reaches **{representative_max:.3f} N**. The corresponding station-based continuous-resonance phase-error screen is approximately **±{allow:.2f} degrees**. This is a conditional design requirement, not demonstrated controller accuracy or a global force-map bound.

## Actual native model and scope

The input reuses all **112,519 nodes and 62,198 C3D10 elements** from accepted chassis deck SHA256 `e62f404781d0ad7e43897daa2e98c3af21eabb639ecfd435ac51b0db1b8d9255`, itself tied to the final connected-chassis BRep. E = 70,000 MPa and Poisson ratio 0.33 remain source assumptions. Added density is 2700 kg/m³ (2.7e-9 tonne/mm³) from the frozen material class. The bare represented chassis mass is **{m['bare_chassis_mass_kg']:.6f} kg**.

The original six scalar static gauge constraints are removed for true free-free modes. The six near-zero rigid modes have squared angular frequencies below 0.001 rad²/s² in magnitude; small negative numerical rigid values are not elastic buckling modes. Elastic participation factors in rigid translation/rotation are near zero. Native output is mass normalized. The final native run also prints stresses at **{m['stress_monitor_points']} integration points**, including the element incident to the actual accepted static stress hotspot. Original source deck/mesh/geometry are not edited.

Separate magnets, bonds, pallet, payload, rollers, joints, stator and host mounts are not meshed here. Uniform-density sensitivities scale the bare mass to the retained-sled and retained-sled-plus 4 kg totals; they are not real discrete attachment modes or a bound over arbitrary mass distributions. No provider mount approval is implied.

![Actual native modal spectrum and differential face mode](figures/SD01_modes.png)

## Forcing, DC preload and finite response

The source **3010.480631N per array** is permanent-magnet mutual attraction. The two PM arrays move together, so this is treated as DC preload, never a full 3 kN oscillatory excitation. The accepted 130% static closure and existing material/thermal/tolerance allocations remain in the budget.

The axial history is reconstructed from the captured principal 3 m/s phase-current trace and finite-force/arrest coefficients. The original saved trace is sampled every 2 ms; reconstructed transitions do not resolve switching or uncaptured current transients. Longitudinal force is distributed uniformly over the two existing magnet patches for this elasticity screen. Free-body rigid acceleration is excluded from paired elastic closure.

Normal sensitivity fractions are 0.1%, 1% and 5% of DC, multiplied by the normalized source force envelope and sin(2pi*x/pitch), with actual source x(t), 8 mm stator pitch and48 mm magnetic wavelength. These are deliberately declared sensitivities, not calibrated ripple. Damping ratios are 0.5%, 2% and 5%. The nominal body, uniformly mass-scaled retained sled and uniformly mass-scaled loaded sled give54 finite cases.

A 500 N/mm rank-one opposing-gap stiffness sensitivity uses the energy-conjugate normal modal force. It is rounded above the largest recorded field-gap secant (about 485 N/mm over the source 0–0.8 mm per-face samples), rather than asserted as a certified derivative bound. Native mechanical geometric-prestress stiffness is not included. The reduced stiffness remains positive for the declared cases.

The modal response uses an exact state transition for each linearly interpolated force increment. A triangle bound covers the union of accepted face nodes and2mm grid; actual control-point histories are retained separately. Static FEM residual is reserved explicitly rather than silently replacing the accepted static solution with a truncated modal approximation.

![Finite principal-shot response and conditional paired clearance](figures/SD01_finite_response.png)

## Current-induced normal reaction from source physics

Each PM array is handled separately. Magnetostatic reciprocity gives reaction on that array as minus the volume integral of JcrossB from its field on the winding. This avoids hiding opposed pinch through cancellation of the total winding normal force. Field coordinates are right-handed Xtravel,Ygap,Zdepth, with CADX=Xfield,CADZ=Yfield,CADY=-Zfield. Common-mode normal force is reported separately in the JSON.

Actual connected DC FE-current distributions for phaseA(h2mm),B(h3mm),C(h3mm) are integrated at650mm. Other representatives use the exact source active-bar and end-return quadrature, including two arrest-region stations; one interior station is refined. The supported18-case maximum phase current is **{n['supported_max_phase_current_A']:.6f}A**. Maximum-thrust electrical phase matches the ideal phase convention of the frozen averaged motor model.

| Stroke mm | Numerical method | Ideal phase abs N | ±5deg N | ±15deg N | Any balanced phase N |
|:--|:--|--:|--:|--:|--:|
{rows}

The actual FE-current interior normal envelope differs from refined uniform quadrature by about 0.067%. That checks this representative implementation; it does not independently validate the shared cuboid field or a full commutation/stroke/brake map. AC skin/proximity, induced fields, steel perturbations, detailed cables and actual controller errors remain outside the model.

![Representative normal reaction compared with the continuous-resonance design screen](figures/SD01_current_normal.png)

## Stress, convergence and required limits

The actual accepted native **nodal extrapolated DC vonMises maximum is {m['accepted_static_nodal_von_Mises_max_MPa']:.6f}MPa**, at the declared web hotspot. Recovered static and modal C3D10 integration-point stresses share the same consistent strain tensor; modal recovery matches native printed stresses within **{100*m['C3D10_stress_recovery_max_relative_component_error']:.3f}%** relative component error. The adverse finite monitor bound is **{worst['monitor_combined_DC1p3_vonMises_bound_MPa']:.3f}MPa**, including130% monitored DC stress. This bounds the declared monitored integration points, not a global dynamic peak. No alloy/temper, yield, fatigue or measured strength limit is invented.

Static paired closure with 10/20/40 elastic modes is0.00553/0.24771/0.29100mm versus accepted0.28598mm. The40-mode maximum spatial residual is0.008468 mm; a 1.3-scaled0.011008 mm reserve is included. The adverse30-to40-mode finite closure-bound change is about 0.0065%;100-to50 µs refinement changes the adverse bound by about 0.266%. Source-trace2ms sampling remains a separate input limitation.

This is one actual accepted mesh with positive element Jacobians, not modal/stress mesh qualification. Full assembly/stator/mount modes, joint/contact damping, manufactured tolerances, a denser current-normal force map and calibrated phase/ripple histories remain required before a physical operating rating. The conditional individual-face residual assumes the original centring allocation; positive paired clearance alone does not prove both actual installed gaps.

![Sustained harmonic sensitivity; a separate load-duration case](figures/SD01_harmonic_limit.png)

**Required design controls:** retain a verified normal-force spectrum/phase-error bound below the applicable resonant limit or introduce demonstrated damping/stiffness/operating exclusions; validate the actual attachment/stator spectrum and individual gaps; keep stress/yield acceptance separate until real material specifications and loads are assigned. The present results support the declared computational reference and identify explicit adverse limits. They do not broaden the original averaged1–3 m/s evidence into hardware qualification.

## Source and reproduction record

`MODAL_INPUT.json`, `runs/free_free/modal.inp`, native `modal.dat` and `SOLVER_STDOUT.txt` identify the genuine run. `MODAL_BASIS.npz` retains patch modes and148 monitored stress fields. `RESPONSE_RESULTS.json`, `FINITE_CASES.csv`, `RESPONSE_CURVES.npz`, `SOURCE_SHOT_FORCE.csv` and `CURRENT_NORMAL_FORCE.json` provide inputs, limits and raw reduced-model results. No vendor PDF is redistributed.

CalculiX2.23 manual sections6.9,7.52,7.63,7.87 and7.88 document mass normalization, frequency extraction, printed stress and modal response conventions (publisher: https://www.dhondt.de/ccx_2.23.pdf). Actual numerical outputs remain the run evidence; a prepared input or manual citation alone is not execution proof.
'''
(H/'STRUCTURAL_DYNAMICS_REPORT.md').write_text(report)
subprocess.run(['pandoc','STRUCTURAL_DYNAMICS_REPORT.md','--pdf-engine=xelatex','-V','papersize:a4','-V','geometry:margin=19mm','-V','mainfont=DejaVu Sans','-V','fontsize=10pt','-o','STRUCTURAL_DYNAMICS_REPORT.pdf'],cwd=H,check=True,capture_output=True)
(H/'FIGURE_MANIFEST.json').write_text(json.dumps({'configuration_id':'VOLLEY-G5-ACR1','study':'SD01','sources':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in [H/'MODAL_RESULTS.json',H/'MODAL_BASIS.npz',H/'RESPONSE_RESULTS.json',H/'RESPONSE_CURVES.npz',H/'CURRENT_NORMAL_FORCE.json',H/'make_report.py']},'figures':figures},indent=2)+'\n')
print(json.dumps(comparison,indent=2))
