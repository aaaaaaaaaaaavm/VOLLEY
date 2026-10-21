"""Quantitative review of contact calibration, refinement and exact-solid checks."""
from pathlib import Path
import csv,hashlib,json,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

H=Path(__file__).resolve().parent;F=H/'figures';F.mkdir(exist_ok=True)
runs=json.loads((H/'campaign_mm/RUNS.json').read_text())['cases']
def table(p):return list(csv.DictReader(p.open()))
def qangle(a,b):
    qa=np.array([float(a[k]) for k in ['qw','qx','qy','qz']]);qb=np.array([float(b[k]) for k in ['qw','qx','qy','qz']]);return math.degrees(2*math.acos(min(1,abs(np.dot(qa,qb)/(np.linalg.norm(qa)*np.linalg.norm(qb))))))
summary=[]
for r in runs:
    rows=table(H/'campaign_mm'/(r['case_id']+'.csv'));last=rows[-1]
    summary.append({**{k:r[k] for k in ['case_id','size','mass_kg','dt_s','label','exit_code','mu','g','iterations']},'last_csv_s':float(last['time_s']),'final_COM_mm':[float(last[k])*1000 for k in ['payload_x_m','payload_y_m','payload_z_m']],'positive_motor_work_J':r['metrics']['positive_mechanical_motor_work_J'],'peak_resultant_contact_N':r['metrics']['maximum_resultant_contact_force_N'],'peak_pair_contact_N':r['metrics']['maximum_pair_contact_force_N'],'minimum_reported_contact_um':r['metrics']['minimum_reported_contact_distance_m']*1e6})
convergence=[]
for size in ['1U','3U']:
    selected=[r for r in runs if r['size']==size and r['label']=='time_refinement'];a,b=selected[1:]
    ra=table(H/'campaign_mm'/(a['case_id']+'.csv'))[-1];rb=table(H/'campaign_mm'/(b['case_id']+'.csv'))[-1]
    delta=np.array([float(ra[k])-float(rb[k]) for k in ['payload_x_m','payload_y_m','payload_z_m']])*1000
    convergence.append({'size':size,'last_step_COM_difference_mm':float(np.linalg.norm(delta)),'last_step_orientation_difference_deg':qangle(ra,rb),'last_step_work_relative_difference':abs(a['metrics']['positive_mechanical_motor_work_J']/b['metrics']['positive_mechanical_motor_work_J']-1),'COM_target_pass':bool(np.linalg.norm(delta)<=.05),'orientation_target_pass':bool(qangle(ra,rb)<=.05)})
calibration=[]
for size in ['1U','3U']:
    for units in ['m','mm']:
        path=H/f'calibration_{size}.csv' if units=='m' else H/f'calibration_mm_{size}.csv';rows=table(path)
        overlaps=[r for r in rows if float(r['imposed_gap_m'])<0 and int(r['contacts'])]
        misses=[float(r['imposed_gap_m']) for r in rows if float(r['imposed_gap_m'])<0 and not int(r['contacts'])]
        calibration.append({'size':size,'internal_length':units,'maximum_detected_gap_error_um':max(abs(float(r['error_from_analytical_gap_m']))*1e6 for r in overlaps),'missed_negative_gap_m':misses,'false_negative_gap_control':len(misses)>0})
audit=json.loads((H/'NATIVE_POSE_AUDIT.json').read_text());positive=[(c['case_id'],r) for c in audit['cases'] for r in c['checks'] if r['positive_pairs']]
result={'revision':'FCE12','cases':summary,'convergence':convergence,'calibration':calibration,'geometry_audit':{'cases':len(audit['cases']),'sampled_poses':sum(len(c['checks']) for c in audit['cases']),'positive_poses':len(positive),'maximum_pair_intersection_mm3':max((p['intersection_mm3'] for _,r in positive for p in r['positive_pairs']),default=0),'residual_resolution':json.loads((H/'POSE_RESOLUTION.json').read_text())},'acceptance':{'analytical_planar_gap_controls':'pass for millimetre internal coordinates, SI output; largest checked error below5nm','discrete_geometric_resolution':'all84sampled poses are nonintersecting or within a verified1um nonintersecting pose; not continuous loaded clearance','final_pose_refinement':'not established under provisional50um/0.05deg screen','contact_force_rating':'not established; rigid NSC contact peaks remain timestep dependent','complete_feeder':'not established; full release/reset, actual actuation and installed architecture remain separate'},'scope':'Gate-already-open transfer/capture/withdraw subcycle with ideal joints and state feedback; unchanged FM06-R1 material geometry and assumed contact/actuator parameters. No physical correlation.'}
(H/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.labelsize':10,'svg.fonttype':'none','pdf.fonttype':42})
colors=['#0072B2','#D55E00','#009E73']
fig,axes=plt.subplots(1,2,figsize=(9,3.65),layout='constrained')
for size,style in [('1U','-'),('3U','--')]:
    for units,color in [('m',colors[1]),('mm',colors[0])]:
        path=H/f'calibration_{size}.csv' if units=='m' else H/f'calibration_mm_{size}.csv'
        rows=[r for r in table(path) if float(r['imposed_gap_m'])<0 and int(r['contacts'])]
        axes[0].plot([-float(r['imposed_gap_m'])*1e6 for r in rows],[abs(float(r['error_from_analytical_gap_m']))*1e6 for r in rows],style+'o',ms=4,color=color,label=f'{size}; internal {units}')
axes[0].set(xscale='log',yscale='log',xlabel='Imposed planar overlap [µm]',ylabel='Absolute reported-gap error [µm]',title='Analytical contact controls');axes[0].legend(fontsize=8)
for filename,label,color in [('mesh_replay.csv','Connected triangles',colors[1]),('volumes_replay.csv','CAD-cell support',colors[0])]:
    rows=table(H/filename);axes[1].plot([float(r['time_s']) for r in rows],[float(r['min_distance_m'])*1000 if int(r['contact_count']) else np.nan for r in rows],'-o',color=color,label=label,ms=4)
axes[1].axhline(0,color='#777777',lw=.8);axes[1].set(xlabel='Replayed FCE08 time [s]',ylabel='Minimum reported gap [mm]',title='Fixed-pose representation check');axes[1].legend(fontsize=8)
for ax in axes:ax.grid(True,alpha=.18)
for ext in ['png','svg','pdf']:fig.savefig(F/('contact_calibration.'+ext),dpi=220)
plt.close(fig)
fig,axes=plt.subplots(1,2,figsize=(9,3.65),layout='constrained')
for si,size in enumerate(['1U','3U']):
    selected=[r for r in runs if r['size']==size and r['label']=='time_refinement']
    for i,r in enumerate(selected):
        rows=table(H/'campaign_mm'/(r['case_id']+'.csv'));axes[si].plot([float(x['time_s']) for x in rows],[float(x['payload_y_m'])*1000 for x in rows],color=colors[i],lw=1,label=f"{r['dt_s']*1e6:g} µs")
    axes[si].set(xlabel='Time [s]',ylabel='Payload centre Y [mm]',title=f'{size} transfer, capture and withdrawal');axes[si].legend(fontsize=8);axes[si].grid(True,alpha=.18)
for ext in ['png','svg','pdf']:fig.savefig(F/('transfer_refinement.'+ext),dpi=220)
plt.close(fig)
fig,axes=plt.subplots(1,2,figsize=(9,3.65),layout='constrained')
for si,size in enumerate(['1U','3U']):
    selected=[r for r in summary if r['size']==size and r['label']=='time_refinement'];ref=np.array(selected[-1]['final_COM_mm'])
    axes[0].plot([r['dt_s']*1e6 for r in selected],[np.linalg.norm(np.array(r['final_COM_mm'])-ref) for r in selected],'-o',color=colors[si],label=size)
    axes[1].plot([r['dt_s']*1e6 for r in selected],[r['peak_resultant_contact_N'] for r in selected],'-o',color=colors[si],label=size)
axes[0].axhline(.05,color='#777777',ls=':',label='Provisional 0.05 mm screen');axes[0].set(xlabel='Integration step [µs]',ylabel='Final COM difference from 125 µs [mm]',title='Final-pose numerical sensitivity')
axes[1].set(xlabel='Integration step [µs]',ylabel='Peak resultant contact [N]',title='Rigid-contact peak sensitivity')
for ax in axes:ax.legend(fontsize=8);ax.grid(True,alpha=.18)
for ext in ['png','svg','pdf']:fig.savefig(F/('numerical_sensitivity.'+ext),dpi=220)
plt.close(fig)
print(json.dumps({'cases':len(summary),'poses':result['geometry_audit']['sampled_poses'],'convergence':convergence,'calibration':calibration},indent=2))
