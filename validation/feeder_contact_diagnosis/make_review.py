"""Produce review artifacts from completed native records without rerunning dynamics."""
from pathlib import Path
import csv,datetime,hashlib,json,math,os,re
os.environ.setdefault("MPLCONFIGDIR",str(Path(__file__).resolve().parent/".mpl-cache"))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
H=Path(__file__).resolve().parent
C=json.loads((H/'COMPARISONS.json').read_text());comparisons=C['comparisons']
D={tuple(r['pair']):r for r in comparisons}
ids=['P3-250','W3-250','B3-250','B3-125','X3-250','X3-125']
records={i:json.loads((H/'runs'/(i+'.record.json')).read_text()) for i in ids}
for i,r in records.items():
 assert r['exit_code']==0 and abs(r['metrics']['final_time_s']-26.5)<1e-6
 assert not r['metrics']['sequence_aborted'] and not r['metrics']['outside_domain_or_nonfinite']
labels=[('FCE12 1U PSOR',('FCE12-02','FCE12-03')),('FCE12 3U PSOR',('FCE12-05','FCE12-06')),('3U PSOR 2k → 4k',('FCE12-05','FCE12-07')),('3U cold → warm PSOR',('P3-250','W3-250')),('3U BB 250 → 125 µs',('B3-250','B3-125')),('3U box core 250 → 125 µs',('X3-250','X3-125')),('3U mesh → box core at125 µs',('FCE12-06','X3-125'))]
summary={'revision':'FCE13 targeted diagnosis of FCE12','generated_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'decision':'FAIL: final-state convergence remains unestablished; no numerical correction adopted','applicability':'FM06-R1 transfer/capture/withdraw numerical subcycle only; no FM07-R6 validation; no feeder selection; no outside expert review','criteria_unchanged':C['criteria'],'observed_sensitivities':[],'completed_native_runs':{i:{'wall_s':r['wall_s'],'metrics':r['metrics'],'solver_metrics':r['solver_metrics'],'source_sha256':r['source_sha256'],'executable_sha256':r['executable_sha256']} for i,r in records.items()},'partial_APGD_attempts':[json.loads((H/'runs'/(i+'.aborted.json')).read_text()) for i in ['A3-250','A3-125']],'certified_true_solution_error_bound':None,'boundary':'Measured differences are sensitivities, not an upper bound on true discretization or physical error.'}
for label,pair in labels:
 r=D[pair];s=r['stages'][-1]
 summary['observed_sensitivities'].append({'label':label,'pair':list(pair),'COM_delta_mm':s['COM_delta_mm'],'orientation_delta_deg':s['angle_delta_deg'],'COM_pass':r['final_COM_target_pass'],'orientation_pass':r['final_angle_target_pass'],'net_contact_impulse_delta_N_s':r['integrated_impulse_delta_norm_N_s'],'positive_motor_work_relative_delta':r['positive_work_relative_difference'],'final_speeds_mm_s':[r['a_final_speed_mm_s'],r['b_final_speed_mm_s']]})
(H/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
plot_pairs=[('1U PSOR','baseline/FCE12-02.csv','baseline/FCE12-03.csv','#0072B2'),('3U PSOR','baseline/FCE12-05.csv','baseline/FCE12-06.csv','#D55E00'),('3U BB','runs/B3-250.csv','runs/B3-125.csv','#009E73'),('3U box core / PSOR','runs/X3-250.csv','runs/X3-125.csv','#CC79A7')]
series=[]
for label,ap,bp,color in plot_pairs:
 a=list(csv.DictReader((H/ap).open()));b=list(csv.DictReader((H/bp).open()));assert len(a)==len(b)
 A=np.array([[float(r[k]) for k in ['payload_x_m','payload_y_m','payload_z_m']] for r in a]);B=np.array([[float(r[k]) for k in ['payload_x_m','payload_y_m','payload_z_m']] for r in b]);qa=np.array([[float(r[k]) for k in ['qw','qx','qy','qz']] for r in a]);qb=np.array([[float(r[k]) for k in ['qw','qx','qy','qz']] for r in b]);dp=np.linalg.norm(A-B,axis=1)*1000;dot=np.abs(np.einsum('ij,ij->i',qa,qb))/(np.linalg.norm(qa,axis=1)*np.linalg.norm(qb,axis=1));dq=np.degrees(2*np.arccos(np.clip(dot,0,1)));t=np.array([float(r['time_s']) for r in a]);series.append((label,t,dp,dq,color))
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42,'svg.fonttype':'none'})
fig,axs=plt.subplots(1,3,figsize=(12.5,3.8),layout='constrained',gridspec_kw={'width_ratios':[1,1,.82]})
for label,t,dp,dq,color in series:
 axs[0].plot(t,dp,label=label,color=color,lw=1);axs[1].plot(t,dq,color=color,lw=1)
for ax in axs[:2]:
 ax.axhline(.05,color='#333333',ls='--',lw=1);ax.axvspan(5,10,color='#777777',alpha=.09);ax.set_xlim(0,26.5);ax.set_xlabel('Time [s]');ax.grid(True,alpha=.18)
names=['PSOR\n250','warm\n250','BB\n250','BB\n125','box core\n250','box core\n125'];fractions=[100*records[i]['solver_metrics']['saturated_steps']/records[i]['metrics']['steps'] for i in ids];axs[2].bar(range(6),fractions,color=['#0072B2','#56B4E9','#009E73','#009E73','#CC79A7','#CC79A7']);axs[2].set_xticks(range(6),names,fontsize=6.4);axs[2].set_ylabel('Steps using full 2,000-iteration budget [%]');axs[2].set_title('3U solver budget use (step in µs)');axs[2].set_ylim(0,max(fractions)*1.24);axs[2].grid(axis='y',alpha=.18)
for j,value in enumerate(fractions):axs[2].text(j,value+.11,f'{value:.2f}',ha='center',fontsize=7)
axs[0].set_ylabel('COM difference [mm]');axs[1].set_ylabel('Orientation difference [deg]');axs[0].set_title('250 → 125 µs, common physical endpoint');axs[1].set_title('Dashed: unchanged 0.05 acceptance screens');axs[0].legend(fontsize=7.4,loc='upper left');fig.suptitle('FCE13 / FM06-R1: final-state convergence remains unestablished',fontsize=11)
for ext in ['png','pdf','svg']:fig.savefig(H/('convergence_diagnosis.'+ext),dpi=190)
plt.close(fig)
with (H/'COMPARISON_TIMESERIES.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['time_s']+[label+' '+quantity for label,*_ in series for quantity in ['COM_delta_mm','orientation_delta_deg']]);
 for j in range(len(series[0][1])):w.writerow([series[0][1][j]]+[value for _,t,dp,dq,_ in series for value in [dp[j],dq[j]]])
report=[]
report.append('FCE13 targeted contact-convergence diagnosis — 22 October 2026\n\nDecision: the existing 0.05 mm COM and 0.05° orientation criteria remain FAILED. No solver or representation correction is qualified for adoption. The original FCE12 failure is preserved. All results apply to FM06-R1 only; they do not validate FM07-R6, rate rigid-contact forces, select a feeder, or constitute outside expert review.\n')
report.append('The six new completed native Chrono10/Bullet runs reached the same26.5s endpoint without domain exit or sequence abort. Zero gravity, restitution0, assumed friction0.1, payload mass4kg,1ms sampled PD control, ideal prismatic guides and actuator caps remain as in FCE12. The exact box-core variant changes collision representation only; all masses, inertias, dimensions, eight rail cells and physical inputs remain fixed.\n')
report.append('| Comparison | Final COM Δ [mm] | Final angle Δ [deg] | Net impulse Δ [N s] | Positive work Δ [%] |\n|---|---:|---:|---:|---:|')
for r in summary['observed_sensitivities']:report.append(f"| {r['label']} | {r['COM_delta_mm']:.6f} | {r['orientation_delta_deg']:.6f} | {r['net_contact_impulse_delta_N_s']:.6g} | {100*r['positive_motor_work_relative_delta']:.6f} |")
report.append('\nAll listed endpoint comparisons fail at least one retained pose criterion; all listed work differences are below the existing1% work screen. Small work differences do not establish pose or load convergence. Net contact impulse is integrated at every native step, but it includes cancellation; no impulse acceptance limit was invented. It is not an integrated absolute load or force rating.\n')
report.append('The instrumented250µs PSOR baseline CSV is byte-identical to FCE12-05. It uses all2,000 iterations in1,936 of106,000 steps and reaches a maximum native reported error0.654381 versus its1e-7 stopping tolerance. Of46 sampled full-budget solves,45 occur during5–10s feed deceleration. At10s the original3U timestep pair already differs1.549519mm/.853163°. Ideal guide constraints remain present; original baseline fork off-axis drift is subnanometre. The measured sensitivity begins before receiver capture.\n')
report.append('Warm starting still uses the full budget during2,444 steps and changes final pose1.736801mm/.497359°. Native BB uses its full2,000-iteration budget during7,028/106,000 and4,424/212,000 steps. Its250→125µs result still fails1.926456mm/.120098°. PSOR GetError measures its reported normal/joint violation and omits tangent components from that stopping statistic. BB exposes an absolute projected-gradient norm while stopping on its norm relative to the initial gradient. These errors have different meanings; full-budget counts do not prove every final iteration missed tolerance. Neither solver establishes every solve as converged here.\n')
report.append('Representation is a demonstrated sensitivity: core00 is exactly an8-vertex,12-triangle box. CORE_BOX_EQUIVALENCE.json verifies all corners, face planes and volume. At250µs, replacing it with a native box gives a byte-identical full CSV. At125µs, that equivalent representation changes final pose0.755420mm/.603748°. Its own timestep pair fails0.716162mm/.564333°. This demonstrates sensitivity to contact manifold representation with unchanged input geometry. It does not establish an upper error bound or isolate a unique root cause. The original planar gap controls detect all imposed10/100/500/1,000µm overlaps with worst error4.273nm and correctly reject10/100µm separated controls. Those controls do not certify moving or rotated contact manifolds.\n')
report.append('Friction remains an uncalibrated physical assumption. Existing500µs3U sensitivities atµ=0 andµ=.3 change final pose0.839301mm/.736022° and0.877083mm/.213657° fromµ=.1. They are sensitivities, not nominal corrections. Under the unchanged undamped zero-g model, FCE12 final speeds at250/125µs are0.187322/.007801mm/s(1U) and0.091251/.114192mm/s(3U). Continuing residual motion makes endpoint phase relevant; no damping or settling time was added to force a pass. Stage velocities and vector impulse differences are in COMPARISONS.json.\n')
report.append('The unpreconditioned APGD pair was terminated as a bounded pilot after an observed91s: last complete CSV times were.85s and.34s, far short of26.5s. Its partial outputs, commands and source identities are retained and excluded from convergence results.\n')
report.append('| Completed native run | Change from FCE12 | Wall time [s] | Full-budget steps |\n|---|---|---:|---:|')
for i in ids:
 r=records[i];note={'P3-250':'instrumentation only','W3-250':'warm start','B3-250':'native BB,250µs','B3-125':'native BB,125µs','X3-250':'exact box core,250µs','X3-125':'exact box core,125µs'}[i];report.append(f"| {i} | {note} | {r['wall_s']:.3f} | {r['solver_metrics']['saturated_steps']} |")
report.append('\nThe observed pose discrepancies measure sensitivity to the tested alternatives; they are not certified bounds on the exact solution. No true-solution error bound is established. The blocking criterion remains a common-endpoint refinement pair satisfying both0.05mm and0.05° after contact representation and solver errors are controlled. Rigid NSC peaks remain unrated. Geometry/contact applicability, physical correlation, full release/reset and installed actuation remain outside this contact subcycle.\n')
report.append('Files: SUMMARY.json gives the decision and numbers; COMPARISONS.json gives stage pose/velocity and impulse/work differences; SOLVER_PHASES.json gives sampled solve diagnostics; runs/*.record.json contains exact native commands, settings, wall times and output hashes; runs/*.solver.csv and*.solver.json preserve diagnostics; BASELINE_HASHES.json preserves original source/results/geometry hashes; references/SOURCES.json identifies the inspected native solver/collision sources. baseline/PROTOCOL.json preserves the unchanged criteria. See REPRODUCE.md for exact commands.\n')
report_text='\n\n'.join(report)+'\n'
for word in ['same','of','all','versus','during','At','by','than','in','after','below','all','assumed','mass','friction','restitution','gravity','during','only','original','existing','box','core','coefficient','instrumented','both','its','a','an','from','and','error','pose','fails','differs','imposed','reject','at','Existing','are','observed','were','Of','solves','full','under','result','times','Its']:
 report_text=re.sub(r'\b'+word+r'(?=[0-9]|\.[0-9])',word+' ',report_text)
report_text=report_text.replace('µs3U','µs 3U').replace('atµ','at µ').replace('fromµ','from µ').replace('andµ','and µ').replace('s(1U)','s (1U)').replace('s(3U)','s (3U)')
report_text=re.sub(r'(?<=\d)(µs|mm|nm|kg|ms|µm|s)(?=[\s,.;:/()°]|$)',r' \1',report_text)
report_text=report_text.replace('Chrono10','Chrono 10').replace('2,000-iteration','2,000 iteration').replace('250µs','250 µs').replace('125µs','125 µs').replace('500µs','500 µs').replace('1e-7','1e-7')
report_text=re.sub(r'(?m)^(\|[^\n]+\|)\n\n(?=\|)',r'\1\n',report_text)
report_text=re.sub(r' *→ *',' → ',report_text)
report_text=re.sub(r',(?=\d{1,2}\b)',', ',report_text)
report_text=re.sub(r'(?<![\dA-Za-z])\.(?=\d)','0.',report_text)
report_text=report_text.replace('BB,250','BB, 250').replace('BB,125','BB, 125').replace('core,250','core, 250').replace('core,125','core, 125')
(H/'REPORT.md').write_text(report_text)
print(json.dumps({'decision':summary['decision'],'completed_runs':len(records),'comparison_rows':len(summary['observed_sensitivities']),'plot':'convergence_diagnosis.pdf'},indent=2))
