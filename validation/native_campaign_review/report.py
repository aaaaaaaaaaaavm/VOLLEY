"""Scientific figures and reader report from native results and explicit budgets."""
from pathlib import Path
import json,math,re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np
H=Path(__file__).resolve().parent;O=H/'full';F=H/'figures';F.mkdir(exist_ok=True)
d=json.loads((O/'SUMMARY.json').read_text());raw=json.loads((O/'RESULTS.json').read_text())
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42,'svg.fonttype':'none','figure.dpi':160})
labels=['4 / spring\n10 kg reserve','4 / VOLLEY input\n10 kg reserve','12 / spring\n20 kg reserve','12 / VOLLEY input\n20 kg reserve']
names=[r['case'] for r in d['nominal_crosschecks']]

def save(fig,stem):
    fig.tight_layout()
    for ext in ['png','svg','pdf']:fig.savefig(F/(stem+'.'+ext),bbox_inches='tight')
    plt.close(fig)

fig,ax=plt.subplots(figsize=(8,3.8));x=np.arange(4)
for offset,key,label,color in [(-.18,'max_payload_position_error_m','Payload at common epoch','#315e7b'),(.18,'max_host_event_position_residual_m','Host event checkpoints + final epoch','#9b672d')]:
    values=[r[key]*1e6 for r in d['nominal_crosschecks']]
    ax.bar(x+offset,values,width=.34,color=color,label=label)
ax.set_xticks(x,labels);ax.set_ylabel('Maximum difference from source [µm]');ax.set_title('Independent nominal propagation and bookkeeping')
ax.legend(fontsize=8,loc='upper left');ax.set_ylim(0,max(max(r['max_host_event_position_residual_m'],r['max_payload_position_error_m'])*1e6 for r in d['nominal_crosschecks'])*1.65)
save(fig,'nominal_consistency')

categories=list(dict.fromkeys(r['category'] for r in d['sensitivity']))
values=np.array([[next(r['position_error_m'] for r in d['sensitivity'] if r['case']==name and r['category']==category) for name in names]for category in categories])
fig,ax=plt.subplots(figsize=(8.4,5.3));im=ax.imshow(values,norm=LogNorm(vmin=.01,vmax=max(1e4,10**math.ceil(math.log10(float(values.max()))))),cmap='cividis',aspect='auto')
ax.set_xticks(range(4),labels);ax.set_yticks(range(len(categories)),categories)
for i in range(values.shape[0]):
    for j in range(values.shape[1]):
        v=values[i,j];label=f'{v/1000:.2g}k' if v>=1000 else f'{v:.2g}'
        ax.text(j,i,label,ha='center',va='center',fontsize=9,color='white' if v<15 else 'black')
ax.set_title('Deterministic command errors at the common assessment epoch')
fig.colorbar(im,ax=ax,label='Maximum payload position error [m]')
save(fig,'control_sensitivity')

fig,axs=plt.subplots(1,2,figsize=(8.8,3.8),sharey=True)
allocation=min(r['linearized_common_release_bias_fraction'] for r in d['accuracy_allocations'] if r['case'] in ['4_volley_3_6_10kg','12_volley_3_6_20kg'] and r['illustrative_position_band_m']==100)
for ax,speed in zip(axs,[3,6]):
    for acceleration,color in [(0,'#315e7b'),(.001,'#6f7e3c'),(.01,'#a45c2b')]:
        rows=[r for r in d['dynamic_metrology'] if r['coasting_entry_speed_m_s']==speed and r['relative_acceleration_bound_m_s2']==acceleration and r['rate_uncertainty_deg_s']==0]
        ax.plot([r['baseline_mm'] for r in rows],[r['relative_exit_speed_bound']*100 for r in rows],'o-',label=f'|a| ≤ {acceleration:g} m/s²',color=color)
    ax.axhline(allocation*100,color='black',ls='--',lw=1,label='100 m / 0.1 m/s common-bias allocation')
    ax.set(xlabel='Photogate baseline [mm]',title=f'Assumed entry speed {speed} m/s');ax.set_yscale('log')
axs[0].set_ylabel('Conditional exit-speed error bound [%]');axs[1].legend(fontsize=7,loc='upper right')
fig.suptitle('Metrology budget: calibration, timing, thermal drift and mean-to-exit speed')
save(fig,'metrology_budget')

fig,ax=plt.subplots(figsize=(7.6,4))
for name,label,color,style in zip(names,['4 spring','4 VOLLEY input','12 spring','12 VOLLEY input'],['#315e7b','#315e7b','#a45c2b','#a45c2b'],['--','-','--','-']):
    rows=[r for r in d['thrust_time'] if r['case']==name]
    ax.plot([r['equivalent_resultant_thrust_N'] for r in rows],[r['thrust_on_before_final_release_s'] for r in rows],marker='o',ls=style,color=color,label=label)
ax.axhline(3600,color='black',ls=':',lw=1,label='3600 s reference release window')
ax.set_xscale('log');ax.set_yscale('log');ax.set(xlabel='Assumed equivalent resultant thrust [N]',ylabel='Summed thrust-on time before final release [s]',title='Necessary time for the frozen control commands')
ax.legend(fontsize=8);save(fig,'thrust_time')

max_nominal=max(r['max_payload_position_error_m'] for r in d['nominal_crosschecks'])
max_refinement=max(r['max_payload_position_change_m'] for r in d['refinement'])
fuel=[(r['case'],r['fuel_used_kg']) for r in d['nominal_crosschecks']]
baseline_table='\n'.join(f"| {r['case'].replace('_',' ')} | {r['fuel_used_kg']:.6f} | {r['max_payload_position_error_m']*1e6:.3f} | {r['final_host_position_error_m']*1e6:.3f} |" for r in d['nominal_crosschecks'])
allocation_table='\n'.join(f"| {r['case'].replace('_',' ')} | {r['linearized_common_release_bias_fraction']*100:.5f}% | {r['linearity_ratio_0p1pct_vs_1pct']:.5f} |" for r in d['accuracy_allocations'] if r['illustrative_position_band_m']==100)
thrust_table='\n'.join(f"| {r['case'].replace('_',' ')} | {r['thrust_on_before_final_release_s']:.1f} | {'Exceeds reference window' if r['violates_3600s_pre_final_release_necessary_time'] else 'Not excluded by total time alone'} |" for r in d['thrust_time'] if r['equivalent_resultant_thrust_N']==5)
text=f'''---
title: "VOLLEY Gen6 — native coupled campaign verification and precision budgets"
date: "19 October 2026 · CNR-01"
geometry: margin=18mm
fontsize: 10pt
mainfont: DejaVu Sans
---

# Purpose and configuration

CNR-01 independently propagates the prescribed host burns and finite-mass releases from the earlier four/twelve-payload construction. It then probes command errors and derives provisional metrology and thrust-time requirements. This is numerical verification and requirements development for a surrogate mission. Motor performance, delivered flight accuracy and hardware compatibility remain unvalidated.

| Input | Declared basis |
|:--|:--|
| Reference orbit | 500 km,97.4°; fixed inertial +Z J2 |
| Gravity | μ =3.986004418×10¹⁴ m³/s²; radius6378137 m; J2 =1.08262668×10⁻³ |
| Manifest | Four: two1U at1.33 kg and two3U at4 kg; twelve: six of each |
| Release schedule | Nominal0–3600 s; common assessment at90000 s |
| Targets | Constructed3–9 m/s prograde increments from reference-host states; not customer target states |
| Release inputs | Spring2.5 m/s; VOLLEY imposed3–6 m/s with host assistance |
| Host | 300 kg dry surrogate; ideal Isp220 s; device proxies16/30 kg per four payloads |
| Reference reserves | 10 kg for both four-release cases;20 kg for both twelve-release cases |

The source control law returns the host to reference positions and restores its final state. The force model is distinct from the earlier450 km,shared-pole GMAT–Orekit benchmark. No Earth-orientation,drag or atmosphere accuracy is inferred from agreement here. The API epoch is a time origin for this time-independent surrogate, not a selected launch date.

# Independent full-sequence calculation

The included event-export derivative retains the earlier source's gravity,targeting,rocket and recoil calculations. It adds explicit burn/release records and omits the later dense-output/clearance-reporting stage. The derivation patch and upstream source identities are included. Recomputed fuel amounts exactly reproduce the archived reference cases in this environment. The twelve-spring case with10 kg reserve still fails at transfer10; its20 kg countercase completes.

Orekit13.1.6 starts from **one initial host state**, propagates between every event, independently applies rocket mass loss and parent/child recoil, and propagates each released payload to the common epoch. It never resets a later host or payload arc to a source sample. The control vectors and targets are shared inputs; the target construction and control optimization are not independently solved. SciPy and Hipparchus both use DOP853, with separate force and bookkeeping implementations.

For a relative release vector u, mass m and pre-release total M, the implementation uses v_child =v_host +(1−m/M)u and v_parent =v_host −(m/M)u. The comoving kinetic-energy identity is ½m(M−m)|u|²/M. Burn mass follows M_after =M_before exp(−|Δv|/(Isp g0)). These are point-mass,ideal-impulse relationships.

{d['native_case_count']} native cases cover five nominal baselines,two step refinements and44 deterministic probes. The four matched comparisons are:

| Case | Native fuel used [kg] | Maximum payload target difference [µm] | Final host difference [µm] |
|:--|--:|--:|--:|
{baseline_table}

The largest nominal payload difference in these matched comparisons is {max_nominal*1e6:.3f} µm. Halving the maximum step from60 to30 s in the two twelve-release comparisons changes payload positions by up to {max_refinement*1e6:.3f} µm. Mass,momentum and comoving-energy residuals are retained in raw output and checked. The numerical consistency threshold is1 cm position and10⁻⁵ m/s velocity; these thresholds are not flight accuracy specifications or rigorous continuous error enclosures.

![Independent nominal calculation; differences reflect shared model inputs](figures/nominal_consistency.png)

# Command-error sensitivity

The probes vary one input at a time: common release-speed bias ±1% and+0.1%; in-plane/out-of-plane direction error ±0.1°; host-burn magnitude bias ±0.1%; and shot latency5/50 ms. Every case uses the original commands,without navigation feedback or retargeting. Delayed shots also delay the following transfer burn,retaining the20 s post-release coast. Assessment remains at the nominal common90000 s epoch.

These are deterministic assumptions rather than measured distributions. The matrix reports the largest payload error across each stated signed probe,not a global uncertainty bound. Source-state differences at shifted intermediate events are not numerical residuals; nominal consistency and perturbed terminal errors are evaluated separately.

![Maximum terminal position errors under explicitly defined probes](figures/control_sensitivity.png)

An illustrative100 m /0.1 m/s full-state box gives the following first-order allocation to a common release bias when **all other errors are set to zero**. It is not a customer requirement. The linearity ratio compares ten times the+0.1% position response with the+1% response; a ratio near one supports the local approximation over those probes.

| Case | Common release-bias allocation | Linearity ratio |
|:--|--:|--:|
{allocation_table}

The10 m /0.01 m/s and1000 m /1 m/s alternatives are in SUMMARY.json. Their purpose is to connect mission targets to actuator and measurement requirements. A controller must estimate the host state,account for actual pointing and manage release velocity. Published model-versus-test error in another deployer is not a measurement of VOLLEY repeatability.

# Velocity measurement budget

For two photogates with baseline L and transit time t,the constant-speed estimate is L/t. The324 static intervals use speeds3/6/9 m/s,baselines50/100/200 mm,calibration bounds5/10/50 µm,individual timestamp bounds0.1/1/10 µs and residual temperature bounds0/0.1/1/10 K. Aluminium-like CTE23×10⁻⁶/K is assumed. Nine m/s remains a study point beyond the first-article objective.

The exact constant-speed interval is (L−δL)/(t+2δt) to (L+δL)/(t−2δt). Temperature drift adds CTE×L×δT to the distance bound. These are prescribed bounds,not statistical standard deviations or actual detector specifications.

A further108 cases include mean-to-exit velocity and frame compensation. With |a_relative|≤a and positive monotonic motion,the transit-time comparison bounds are2L/(v0+√(v0²±2aL)). The difference between mean transit speed and exit speed is bounded by a×t_max/2. A rate-knowledge bound adds δω×r for a0.5 m lever arm. Exact constant-acceleration corner checks exercise the interval arithmetic.

![Conditional measurement/exit-speed budget at3 and6 m/s; dashed allocation consumes the entire illustrative mission budget](figures/metrology_budget.png)

A longer baseline reduces calibration/timestamp contributions but increases the mean-to-exit contribution when relative acceleration is present. The required quiet/coasting measurement zone,baseline thermal calibration,detector response,payload edge geometry,tip-off and frame-rate compensation must be implemented and tested. Post-release measurements support verification and calibration; they cannot correct a passive satellite already released. Closed-loop acceleration and release control require their own sensors and design.

# Necessary thrust-time screen

For an equivalent constant-thrust engine,the nominal impulse fuel amount implies thrust-on time Δm×Isp×g0/F. Twenty cases use0.1/1/5/20/100 N. This is a necessary time calculation for the **frozen reference commands**; it does not integrate finite burns or optimize another spring/VOLLEY policy.

| Case at5 N | Thrust-on time before final release [s] | Total-time screen |
|:--|--:|:--|
{thrust_table}

![Frozen-command thrust-on time; coasting,feeding,slew and safety scheduling need additional allowance](figures/thrust_time.png)

Passing the summed-time screen is insufficient: each finite burn must fit the chronology and avoid incompatible operations. Alternative controls/release epochs can change these demands. A low-thrust failure here does not prove every competent spring-host strategy fails. The device mass proxies still leave VOLLEY heavier despite lower fuel consumption. A selected host,installed system and optimized service comparison remain necessary before a product advantage is claimed.

# Verification status and remaining engineering

| Verified within this study | Still required |
|:--|:--|
| Prescribed full host/release sequence in independent native code | Customer target states and acceptable errors |
| Rocket/recoil/mass/energy identities and step comparison | Finite-burn targeting,attitude/slew and navigation feedback |
| Deterministic terminal-error responses | Calibrated sensor/actuator/error distributions |
| Conditional metrology and total-thrust-time calculations | Actual measurement architecture and source-rated hardware |
| Retained failed low-reserve spring campaign | Body/contact/near-field clearance and fault recovery |

The earlier conditional point-centre clearance screen remains conditional. Numerical agreement at events and the common epoch does not prove the assumed1 cm continuous state-error enclosure,physical separation geometry or conjunction probability. All51 trajectories use imposed release velocities; they do not establish a motor rating.

# Reproduction

1. Inspect the reports,raw event/host/payload CSVs and exact source identities.
2. Run check_capture.py with standard Python for integrity and independent bookkeeping checks.
3. Run download_jars.py to obtain the pinned public Orekit/Hipparchus dependencies; set OREKIT_CLASSPATH to jars/* and use Java21 with its source-file compiler module.
4. Run run_full_campaign.py for the native cases,then summarize.py and report.py for budgets and figures. Install the pinned numerical packages when regenerating the source events with instrument_campaign.py and export_events.py.
5. Compile this Markdown with pandoc and XeLaTeX for the PDF. The manifest records the captured environment and exact inputs/outputs; rerunning does not imply bit-identical PDF metadata.
'''
# Readable SI spacing without changing identifiers,hashes or paths.
for old,new in {'500 km,97.4':'500 km, 97.4','μ =3.':'μ = 3.','radius6378137':'radius 6378137','J2 =1.':'J2 = 1.','two1U at1.33':'two 1U at 1.33','two3U at4':'two 3U at 4','Nominal0–3600':'Nominal 0–3600','at90000':'at 90000','Constructed3–9':'Constructed 3–9','Spring2.5':'Spring 2.5','imposed3–6':'imposed 3–6','Isp220':'Isp 220','proxies16/30':'proxies 16/30',';20 kg':'; 20 kg','earlier450':'earlier 450','with10':'with 10','transfer10':'transfer 10','its20':'its 20','Orekit13.1.6':'Orekit 13.1.6','from60 to30':'from 60 to 30','threshold is1':'threshold is 1','and10⁻⁵':'and 10⁻⁵','and44':'and 44','and+0.1':'and +0.1','latency5/50':'latency 5/50','the20':'the 20','common90000':'common 90000','illustrative100':'illustrative 100','m /0.':'m / 0.','The10':'The 10','and1000':'and 1000','m /1':'m / 1','The324':'The 324','speeds3/6/9':'speeds 3/6/9','baselines50':'baselines 50','bounds5/10/50':'bounds 5/10/50','bounds0.1/1/10':'bounds 0.1/1/10','bounds0/0.1/1/10':'bounds 0/0.1/1/10','CTE23':'CTE 23','further108':'further 108','a0.5':'a 0.5','at3 and6':'at 3 and 6','use0.1':'use 0.1','at5 N':'at 5 N','All51':'All 51','Java21':'Java 21','assumed1 cm':'assumed 1 cm'}.items():text=text.replace(old,new)
text=re.sub(r',(?=[A-Za-z0-9])', ', ', text)
text=re.sub(r';(?=[A-Za-z0-9])', '; ', text)
(H/'README.md').write_text(text)
print('CNR-01 reader report and four scientific figure sets generated')
