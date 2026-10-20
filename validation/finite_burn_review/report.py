"""Scientific plots and report from captured finite-force/native results."""
from pathlib import Path
import json,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
H=Path(__file__).resolve().parent;F=H/'figures';F.mkdir(exist_ok=True)
S=json.loads((H/'SUMMARY.json').read_text())
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,'axes.spines.right':False,
                     'pdf.fonttype':42,'svg.fonttype':'none','figure.dpi':160,'savefig.dpi':300})
cases=['4_spring_10kg','4_volley_3_6_10kg','12_spring_20kg','12_volley_3_6_20kg']
labels=['4 / spring','4 / VOLLEY input','12 / spring','12 / VOLLEY input']
colors=['#355f7c','#ae6b30']
def save(fig,name):
    fig.tight_layout()
    for ext in ['svg','pdf','png']:fig.savefig(F/(name+'.'+ext),bbox_inches='tight')
    plt.close(fig)
def nominal(case):return next(r for r in S['solutions'] if r['case']==case and r['fraction']==.35 and r['max_step_s']==60 and r['initial_fuel_kg'] in [10,20])

fig,axs=plt.subplots(2,1,figsize=(7.1,5.1),sharex=True)
for case,label,color,ls in zip(cases,labels,[colors[0],colors[1],colors[0],colors[1]],['--','--','-','-']):
    vals=[r for r in S['solutions'] if r['case']==case and r['max_step_s']==60 and r['initial_fuel_kg'] in [10,20]]
    vals.sort(key=lambda r:r['fraction'])
    axs[0].plot([100*r['fraction'] for r in vals],[r['peak_force_N'] for r in vals],marker='o',color=color,ls=ls,label=label)
    axs[1].plot([100*r['fraction'] for r in vals],[r['fuel_used_kg'] for r in vals],marker='o',color=color,ls=ls)
axs[0].axhline(20,color='black',ls=':',lw=1,label='20 N illustrative resultant limit')
axs[1].axhline(20,color='black',ls=':',lw=1,label='12-release reserve: 20 kg')
axs[1].axhline(10,color='grey',ls=':',lw=1,label='4-release reserve: 10 kg')
axs[0].set(ylabel='Peak resultant thrust [N]',ylim=(0,55),title='Finite-force scheduling on shared full-state targets')
axs[1].set(xlabel='Each force-window duration / available leg [%]',ylabel='Total propellant used [kg]',ylim=(0,30))
axs[0].legend(fontsize=7,ncol=2);axs[1].legend(fontsize=7,loc='upper left')
save(fig,'force_fuel_trade')

fig,axs=plt.subplots(2,1,figsize=(7.1,4.9),sharex=True)
for case,color in zip(['12_spring_20kg','12_volley_3_6_20kg'],colors):
    r=json.loads((H/'release'/nominal(case)['file']).read_text())
    for idx,e in enumerate(r['events']):
        if e['kind']=='arc':
            force=np.linalg.norm(e['force_N']);a,b=e['start_s'],e['end_s']
            axs[0].plot([a,b],[force,force],color=color,lw=1.5,label=case.split('_')[1] if idx==0 else None)
    traj=np.loadtxt(H/'release'/(nominal(case)['stem']+'_trajectory.csv'),delimiter=',',skiprows=1)
    payload=np.array([sum(e['payload_mass_kg'] for e in r['events'] if e['kind']=='shot' and e['start_s']<=t) for t in traj[:,0]])
    # Mass immediately before/after a shot is discontinuous; draw fuel at arc endpoints.
    nowfuel=0.;tt=[-900];ff=[0.]
    for e in r['events']:
        if e['kind']=='arc':nowfuel+=e['before'][6]-e['after'][6]
        tt.append(e['end_s']);ff.append(nowfuel)
    axs[1].plot(tt,ff,color=color,label=case.split('_')[1])
axs[0].axhline(20,color='black',ls=':',lw=1);axs[1].axhline(20,color='black',ls=':',lw=1)
axs[0].set(ylabel='Resultant thrust magnitude [N]',title='Twelve releases: explicit preparation, force windows and recovery')
axs[1].set(xlabel='Time relative to first release [s]',ylabel='Propellant consumed [kg]',xlim=(-950,4250))
axs[0].legend(fontsize=8);save(fig,'twelve_chronology')

fig,ax=plt.subplots(figsize=(7.1,3.5));x=np.arange(4)
nr=[next(r for r in S['native'] if r['name']==nominal(c)['stem']) for c in cases]
ax.bar(x-.17,[r['max_payload_target_position_error_m']*1e6 for r in nr],.32,label='Payload target at common epoch',color=colors[0])
ax.bar(x+.17,[r['max_host_position_difference_m']*1e6 for r in nr],.32,label='Host checkpoints vs Python',color=colors[1])
ax.set_xticks(x,labels);ax.set(ylabel='Maximum numerical difference [µm]',title='Independent native finite-force propagation')
ax.legend(fontsize=7);ax.set_ylim(0,max(r['max_payload_target_position_error_m']*1e6 for r in nr)*1.4)
save(fig,'native_consistency')

cats=['force ±0.1%','release speed ±0.1%','initial inertial X ±10 m'];mat=[]
for key in ['force','shot','dx']:
    vals=[]
    for case in cases:
        z=[r for r in S['native'] if r['category']=='deterministic_sensitivity' and r['name'].startswith(case+'_') and r[key]!=(0 if key=='dx' else 1)]
        vals.append(max(r['max_payload_target_position_error_m'] for r in z))
    mat.append(vals)
mat=np.array(mat);fig,ax=plt.subplots(figsize=(7.1,3.2));im=ax.imshow(mat,cmap='cividis',norm=LogNorm(vmin=1,vmax=10**math.ceil(math.log10(mat.max()))),aspect='auto')
ax.set_xticks(range(4),labels);ax.set_yticks(range(3),cats)
for i in range(3):
    for j in range(4):ax.text(j,i,f'{mat[i,j]:.0f}',ha='center',va='center',color='white' if mat[i,j]<100 else 'black',fontsize=8)
fig.colorbar(im,ax=ax,label='Maximum terminal position error [m]')
ax.set_title('Frozen commands: deterministic error probes, no feedback')
save(fig,'finite_control_sensitivity')

fig,ax=plt.subplots(figsize=(7.1,3.4))
for case,label,col,ls in zip(cases,labels,[colors[0],colors[1],colors[0],colors[1]],['--','--','-','-']):
    slew=nominal(case)['slew_requirements']
    ax.plot([r['end_s'] for r in slew],[r['mean_rate_deg_s'] for r in slew],marker='o',markersize=3,color=col,ls=ls,label=label)
ax.set(xlabel='Start of next thrust window [s]',ylabel='Average direction slew needed [°/s]',title='Single fixed-thruster interpretation: coast-only force-vector reversals',ylim=(0,10))
ax.legend(fontsize=7,ncol=2);save(fig,'slew_requirements')

baseline='\n'.join(f"| {label} | {nominal(c)['peak_force_N']:.2f} | {nominal(c)['fuel_used_kg']:.3f} | {'Pass' if nominal(c)['feasible_in_declared_model'] else 'Fail'} |" for c,label in zip(cases,labels))
fair=[r for r in S['solutions'] if r['initial_fuel_kg']==30]
fairtable='\n'.join(f"| {r['case'].split('_')[1]} | {r['peak_force_N']:.2f} | {r['fuel_used_kg']:.3f} | {r['fuel_remaining_kg']:.3f} |" for r in fair)
mx=max(r['max_payload_target_position_error_m'] for r in S['native'] if r['category']=='nominal')
ref=max(r['payload_position_change_m'] for r in S['refinement'])
text=rf'''---
title: "VOLLEY Gen6 — finite-force campaign study"
date: "20 October 2026 · FBR-01"
geometry: margin=18mm
fontsize: 10pt
mainfont: DejaVu Sans
---

# Scope and principal finding

FBR-01 replaces the archived instantaneous host-burn sequence with targeted, finite-duration constant-inertial-force windows and continuous propellant consumption. It is a point-mass control feasibility study, separately versioned from the evaluated Gen5. The release inputs remain imposed: 2.5 m/s for spring and 3–6 m/s for VOLLEY. No selected motor, host propulsion system, flight pointing capability or physical release is established.

For the declared 35%/35% two-window policy, both four-release comparisons meet the illustrative 20 N / 10 kg fuel screen. The twelve-release VOLLEY-input case meets the 20 N / 20 kg screen; the corresponding spring case fails both. A common 30 kg reserve and 100 N limit permits **both** twelve-release policies in the translational model. This rules out a claim that a competent spring/host service cannot perform the constructed mission.

Whole-host slews would need approximately 9°/s mean force-vector reversal in some 20 s gaps for a single fixed thruster. No host is selected with this capability. Opposed thrusters or another force allocation could avoid whole-body reversals, but that requires an actual propulsion, attitude, plume and mass architecture. The model therefore does not close operational host compatibility.

# Requirements and common boundary

The reference is 500 km altitude, 97.4° inclination, Earth-centred inertial Cartesian axes, with a fixed inertial +Z J2 axis. Constants are μ = 3.986004418×10¹⁴ m³/s², equatorial radius 6378137 m and J2 = 1.08262668×10⁻³. This explicitly simplified force model omits drag, higher-order gravity, Sun/Moon perturbations and Earth-orientation effects. The arbitrary epoch is 29 September 2026 00:00:00 TAI; no geographic service window is claimed.

Four releases alternate 1.33 kg 1U and 4 kg 3U surrogates; twelve use six of each. Releases span 0–3600 s. Every payload is assessed at the same 90000 s epoch, 24 h after the final nominal release. Targets and release vectors are preserved byte-for-byte from the archived matched study; reverse propagation supplies the desired release states. Target construction is therefore shared evidence, not an independently optimized customer mission.

Host dry mass is 300 kg, with device mass proxies 16 kg spring or 30 kg VOLLEY per four cells. Initial fuel is 10 kg for four and 20 kg for twelve, with an additional matched 30 kg twelve-release countercase. These are study assumptions, not measured installed hardware. Specific impulse is a constant 220 s for both.

# Finite-force formulation

During a force window, the integrated state is (r, v, M):

$$\dot{{\mathbf r}}=\mathbf v,\qquad \dot{{\mathbf v}}=\mathbf a_{{J2}}(\mathbf r)+\mathbf F/M,\qquad \dot M=-\|\mathbf F\|/(I_{{sp}}g_0).$$

Each leg has two independently constant inertial force vectors. Each force window occupies a declared fraction f of the leg; the intervening zero-force coast occupies 1−2f. Six force components are solved for the six endpoint constraints using nonlinear shooting. Controls are solved without hard thrust saturation and then screened against the declared limits. This is one constructed policy, not a globally optimal solution or a proof of infeasibility for other schedules.

The first preparatory leg starts at −900 s on the reference orbit; its fuel and thrust are counted. Every release is followed by a 20 s zero-force guard. The final host recovery ends at 4200 s; the host then coasts to the same 90000 s epoch. No velocity reset, instantaneous preburn or later host-state reset is used between finite arcs. Preparation before the first release is an explicit additional operational allowance.

At a point-centre release of mass m and prescribed relative velocity u, child velocity is v + (1−m/M)u and parent velocity is v − (m/M)u. The parent loses the payload mass. The targeter includes endpoint mass in this recoil relation. This instantaneous release boundary does not model the contact interval or the physical launcher body.

# Results and retained failures

| Case | Peak resultant [N] | Total fuel [kg] | Declared thrust/fuel screen |
|:--|--:|--:|:--|
{baseline}

The twelve-spring 20 kg formal solution exhausts its reserve at 3509.06 s, before the final release. Later portions are retained **only as mathematical diagnostics**; the complete prescribed campaign is infeasible under that resource budget. Nominal endpoint agreement must not be used to claim operation after fuel exhaustion.

![Finite-window force/fuel trade; each point is a separately retargeted solution. Horizontal lines are illustrative resource limits, not provider ratings.](figures/force_fuel_trade.png)

The 18 targeted solutions include f = 0.20, 0.35 and 0.45 for four common comparisons, four 30 s step retargets, and two common 30 kg reserve cases. Shorter force windows reduce propellant in this family but increase peak resultant force. The retained 20% twelve-VOLLEY case needs 26.12 N and therefore fails the 20 N screen; selecting only the favorable 35% case would conceal this dependence.

![Twelve-release chronology for f = 0.35, including counted preparation, zero-force intervals and host recovery. The spring trace after fuel exhaustion is diagnostic.](figures/twelve_chronology.png)

The matched 30 kg reserve comparison at a common 100 N illustrative limit is:

| Twelve-release input | Peak force [N] | Fuel used [kg] | Fuel remaining [kg] |
|:--|--:|--:|--:|
{fairtable}

VOLLEY's additional device proxy is 42 kg for twelve cells. Its propellant saving in the common 30 kg countercase is {fair[0]['fuel_used_kg']-fair[1]['fuel_used_kg']:.3f} kg. The added proxy mass exceeds that saving by {42-(fair[0]['fuel_used_kg']-fair[1]['fuel_used_kg']):.3f} kg. This is a resource comparison, not an optimized installed mass or a priced service-value calculation. Precision, throughput, host wear and customer delivery requirements remain unmeasured.

# Independent native replay and numerical sensitivity

SciPy DOP853 integrates and targets the Python model. A separately written Java implementation uses Orekit 13.1.6, Hipparchus 4.0.3, NumericalPropagator, J2OnlyPerturbation and a custom ForceModel with an integrated mass derivative. It starts once at −900 s and follows the captured finite force/release sequence without later state resets or access to the Python targeter. Both solvers use DOP853; the shared integration family and common targets limit independence.

Forty-six actual native runs comprise 18 nominal/revised solutions, four same-command 60-to-30 s refinements, and 24 deterministic error probes. Across all 18 nominal replays, the largest payload terminal difference from the archived target is {mx*1e6:.2f} µm. The largest payload change in the eight numerical refinements is {ref*1e6:.2f} µm. The retained capture check applies 1 cm / 10⁻⁵ m/s numerical tolerances, mass-flow/recoil identities and exact file hashes. These are numerical consistency checks, not flight accuracy or a rigorous continuous error enclosure.

![Native Orekit finite-force consistency for the four common 35% policies. Numerical differences share the same target and simplified physical model.](figures/native_consistency.png)

The 24 probes apply common force magnitude ±0.1%, imposed release speed ±0.1%, or initial inertial X displacement ±10 m, one source at a time. No feedback or retargeting follows the perturbation. Results are deterministic sensitivities, not probability distributions or simultaneous uncertainty bounds.

![Common-epoch errors under frozen commands. Values give maximum payload position error across both signed probes.](figures/finite_control_sensitivity.png)

# Host pointing and force allocation

For a single fixed thruster, changing the thrust direction entails rotating the vehicle. The angle between consecutive nonzero force vectors divided by the intervening zero-force time gives a **necessary average direction slew**, with instantaneous acceleration/deceleration and no settling allowance. It excludes payload release alignment and any pointing-knowledge error. The highest averages are 8.78–9.00°/s for the four primary comparisons.

![Required average direction slew if one fixed thruster supplies the resultant. Opposed thrusters may change this requirement; their hardware and plume geometry are not included.](figures/slew_requirements.png)

A slew-rate limit below these values rejects this specific single-thruster interpretation. Multi-axis or opposed thrusters may produce a different resultant without rotating the host through every reversal; they add valves, propellant/pressurant plumbing, dry mass, plume exclusions, thermal limits and fault allocation. Either route needs a controlled host design before it can close an engineering gate.

# Disposition

Finite-duration translational targeting and continuous mass consumption have now been run and independently replayed for the declared policy family. The older summed-thrust-time calculation remains a necessary screen for its frozen impulse schedule, not the result of this new retargeted policy.

Still open are actual host thrust/attitude allocation and slew dynamics; finite release-body and plume clearance; navigation feedback and covariance; drag and higher-fidelity environment; actual installed mass, power and thermal control; motor/circuit ratings and measured release precision; selected customer targets; and the feeder/retention hardware. No product, flight readiness, calibrated precision or globally superior service is concluded.

# Reproduction and source record

1. Verify MANIFEST.json and run check_capture.py using standard Python.
2. Install requirements-python.txt; use target.py and run_matrix.py for the captured target family, then export.py.
3. Run download_jars.py for the exact SHA-256-locked public dependencies. Set OREKIT_CLASSPATH to jars/*, use Java 21 with its compiler module, and run run_native.py.
4. Run summarize.py and report.py. Compile README.md using Pandoc/XeLaTeX for the report PDF.

Native CSVs and logs are genuine software outputs; scientific plots are derived from those outputs and are not application screenshots. No software interface is synthesized. Source identities identify the archived targets. Rebuilding a PDF can change its metadata, so the manifest records the reviewed captured bytes.

Primary software references: [Orekit ForceModel API](https://www.orekit.org/static/apidocs/org/orekit/forces/ForceModel.html), [Orekit J2OnlyPerturbation API](https://www.orekit.org/static/apidocs/org/orekit/forces/gravity/J2OnlyPerturbation.html), and [SciPy solve_ivp](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html). Dependency versions and hashes are separately pinned in SOFTWARE_LOCK.json.
'''
(H/'README.md').write_text(text)
print('FBR-01 report and five vector/raster figure sets generated')
