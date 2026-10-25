"""Create figures and comparison tables from completed native records."""
from pathlib import Path
import os
os.environ.setdefault('MPLCONFIGDIR','/tmp/acr1-release-matplotlib')
import csv,json,math,hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE=Path(__file__).resolve().parent
a=json.loads((HERE/'CAMPAIGN.json').read_text());runs=a['completed_records']
good=[r for r in runs if r.get('status')!='RUN_FAILED']
def csvwrite(path,rows):
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def qangle(a,b):return math.degrees(2*math.acos(min(1,abs(float(np.dot(a,b))))))
base=[r for r in good if r['solver']=='Newton' and r['iterations']==100 and r['direct_stiffness_s_minus2']==1e6 and r['direct_damping_s_minus1']==2000 and r['representation']=='box']
comp=[]
for case in sorted({r['case']['id'] for r in base}):
    group=sorted([r for r in base if r['case']['id']==case],key=lambda r:-r['dt_s'])
    for x,y in zip(group,group[1:]):
        dp=float(np.linalg.norm(np.array(y['payload_final_position_m'])-x['payload_final_position_m']))
        da=qangle(x['payload_final_quaternion_wxyz'],y['payload_final_quaternion_wxyz'])
        comp.append({'case':case,'coarse_dt_us':x['dt_s']*1e6,'fine_dt_us':y['dt_s']*1e6,'COM_difference_mm':dp*1000,'orientation_difference_deg':da,'speed_vector_difference_m_s':float(np.linalg.norm(np.array(y['payload_final_velocity_m_s'])-x['payload_final_velocity_m_s'])),'omega_vector_difference_deg_s':float(np.linalg.norm(np.array(y['payload_final_omega_deg_s'])-x['payload_final_omega_deg_s'])),'within_inherited_0p05mm_0p05deg_reference':dp<=.00005 and da<=.05})
csvwrite(HERE/'REFINEMENT.csv',comp)
summaryrows=[]
for r in good:
    summaryrows.append({'case':r['case']['id'],'dt_us':r['dt_s']*1e6,'solver':r['solver'],'iterations':r['iterations'],'stiffness_s_minus2':r['direct_stiffness_s_minus2'],'damping_s_minus1':r['direct_damping_s_minus1'],'representation':r['representation'],'vx_m_s':r['payload_final_velocity_m_s'][0],'vx_minus_source_m_s':r['payload_inertial_kick_difference_m_s'],'omega_norm_deg_s':float(np.linalg.norm(r['payload_final_omega_deg_s'])),'orientation_change_deg':r['orientation_change_deg'],'rear_last_s':r['rear_contact_last_s'],'post_source_release_absolute_impulse_Ns':sum(r['post_source_release_absolute_impulse_by_group_Ns'].values()),'final_aft_relative_carrier_m':r['final_payload_aft_relative_carrier_m'],'fully_beyond_0p5145m_carrier_envelope':r['final_payload_aft_relative_carrier_m']>.5145,'maximum_numerical_overlap_um':r['max_overlap_m']*1e6,'total_x_momentum_residual_Ns':r['conservation']['total_x_momentum_residual_kg_m_s'],'solver_max_iterations':r['solver_max_iterations_used'],'full_iteration_budget_steps':r['solver_full_budget_steps'],'native_warnings':sum(r['native_warning_increments'])})
csvwrite(HERE/'RESULTS.csv',summaryrows)
comparisons=[]
for r in good:
    if r in base:continue
    reference=next((q for q in base if q['case']['id']==r['case']['id'] and abs(q['dt_s']-r['dt_s'])<1e-12),None)
    if reference:
        comparisons.append({'case':r['case']['id'],'variant':f'{r["solver"]}/{r["iterations"]}/{r["representation"]}/k={r["direct_stiffness_s_minus2"]}/b={r["direct_damping_s_minus1"]}','COM_difference_mm':1000*float(np.linalg.norm(np.array(r['payload_final_position_m'])-reference['payload_final_position_m'])),'orientation_difference_deg':qangle(r['payload_final_quaternion_wxyz'],reference['payload_final_quaternion_wxyz']),'velocity_difference_m_s':float(np.linalg.norm(np.array(r['payload_final_velocity_m_s'])-reference['payload_final_velocity_m_s']))})
csvwrite(HERE/'SOLVER_AND_CONTACT_SENSITIVITY.csv',comparisons)
physical=[]
for r in base:
    if abs(r['dt_s']-25e-6)<1e-12:physical.append(r)
result={'configuration_id':'VOLLEY-G5-ACR1','native_engine':'MuJoCo3.3.7','planned_runs':a['planned_runs'],'completed_runs':len(good),'failed_runs':[r for r in runs if r.get('status')=='RUN_FAILED'],'refinement_pairs':comp,'solver_contact_comparisons':comparisons,'full_P3_BB_criterion_complete':False,'numerical_scope':'Local six-DOF surrogate release/contact replay with finite X translation;not physical repeatability or full source/host/mechanism closure','maximum_total_x_momentum_residual_Ns':max(abs(r['conservation']['total_x_momentum_residual_kg_m_s']) for r in good),'maximum_payload_linear_impulse_residual_Ns':max(float(np.linalg.norm(r['conservation']['payload_linear_impulse_residual_Ns'])) for r in good),'maximum_payload_angular_impulse_residual_Nms':max(float(np.linalg.norm(r['conservation']['payload_angular_impulse_residual_Nms'])) for r in good),'maximum_contact_vs_generalized_force_error_N':max(r['conservation']['native_generalized_vs_contact_force_max_N'] for r in good),'maximum_native_iterations':max(r['solver_max_iterations_used'] for r in good),'full_budget_steps':sum(r['solver_full_budget_steps'] for r in good),'native_warning_increments':sum(sum(r['native_warning_increments']) for r in good),'aligned_25us':next(r for r in base if r['case']['id']=='aligned' and abs(r['dt_s']-25e-6)<1e-12),'half_keeper_25us':next(r for r in base if r['case']['id']=='half_keeper' and abs(r['dt_s']-25e-6)<1e-12),'no_contact_control_25us':next(r for r in base if r['case']['id']=='freeflight' and abs(r['dt_s']-25e-6)<1e-12),'physics_parameter_interpretation':'Contact stiffness,damping and friction are unmeasured sensitivity values;native contact-force peaks unrated.'}
(HERE/'SUMMARY.json').write_text(json.dumps(result,indent=2)+'\n')

plt.rcParams.update({'font.size':10,'axes.grid':True,'grid.alpha':.25})
fig,axs=plt.subplots(1,2,figsize=(11,4.2))
for case in sorted({c['case'] for c in comp}):
    cs=[c for c in comp if c['case']==case]
    if case=='freeflight':continue
    axs[0].plot([c['fine_dt_us'] for c in cs],[max(c['COM_difference_mm']*1000,1e-8) for c in cs],'o-',label=case)
    axs[1].plot([c['fine_dt_us'] for c in cs],[max(c['orientation_difference_deg'],1e-10) for c in cs],'o-')
axs[0].axhline(50,color='k',ls='--',lw=.8);axs[1].axhline(.05,color='k',ls='--',lw=.8)
for ax in axs:ax.set_xscale('log');ax.set_yscale('log');ax.set_xlabel('Fine time step (µs)')
axs[0].set_ylabel('Common-endpoint COM difference (µm)');axs[1].set_ylabel('Orientation difference (deg)')
axs[0].legend(fontsize=7,ncol=2);fig.suptitle('ACR1 native contact refinement — dashed lines are inherited numerical reference screens')
fig.tight_layout();fig.savefig(HERE/'REFINEMENT.png',dpi=180);fig.savefig(HERE/'REFINEMENT.pdf');plt.close(fig)

fig,axs=plt.subplots(2,1,figsize=(10,7),sharex=True)
names=['aligned','yaw','pitch','one_rear_pad','half_keeper']
for name in names:
    path=next((HERE/'runs').glob(f'{name}_25us_Newton100_k1e+06_b2000_box.csv'))
    dat=np.genfromtxt(path,delimiter=',',names=True)
    r=next(r for r in physical if r['case']['id']==name)
    t=dat['time_s']-r['source_release_s']
    axs[0].plot(t*1000,dat['vx_m_s'],label=name)
    norm=np.sqrt(dat['wx_deg_s']**2+dat['wy_deg_s']**2+dat['wz_deg_s']**2)
    axs[1].plot(t*1000,norm,label=name)
axs[0].set_ylabel('Payload inertial X speed (m/s)');axs[1].set_ylabel('Angular-speed magnitude (deg/s)');axs[1].set_xlabel('Time from 1D source unload (ms)')
axs[0].legend(ncol=3,fontsize=8);fig.suptitle('Computed local departure histories — unmeasured contact-model parameters')
fig.tight_layout();fig.savefig(HERE/'DEPARTURE_HISTORIES.png',dpi=180);fig.savefig(HERE/'DEPARTURE_HISTORIES.pdf');plt.close(fig)

# Visual capture from the native XML collision surfaces and final native poses.
# This is a plotted collision proxy, not a full CAD or hardware rendering.
import xml.etree.ElementTree as ET
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
def rotation(q):
    w,x,y,z=q
    return np.array([[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w)],[2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w)],[2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y)]])
signs=np.array([[-1,-1,-1],[-1,-1,1],[-1,1,-1],[-1,1,1],[1,-1,-1],[1,-1,1],[1,1,-1],[1,1,1]])
faces=[[0,1,3,2],[4,5,7,6],[0,1,5,4],[2,3,7,6],[0,2,6,4],[1,3,7,5]]
fig=plt.figure(figsize=(12,5))
for panel,name in enumerate(['aligned','half_keeper']):
    ax=fig.add_subplot(1,2,panel+1,projection='3d')
    path=next((HERE/'runs').glob(f'{name}_25us_Newton100_k1e+06_b2000_box.xml'))
    tree=ET.parse(path)
    for g in tree.findall('.//body[@name="carrier"]/geom'):
        mid=np.fromstring(g.attrib['pos'],sep=' ');half=np.fromstring(g.attrib['size'],sep=' ')
        vertices=mid+signs*half
        mesh=Poly3DCollection([vertices[f] for f in faces],alpha=.12,facecolor='#536d7a',edgecolor='#536d7a',linewidth=.25)
        ax.add_collection3d(mesh)
    r=next(r for r in physical if r['case']['id']==name)
    R=rotation(r['payload_final_quaternion_wxyz'])
    ext=np.abs(R)@np.array([.17025,.05,.05])
    payload_mid=np.array([r['final_payload_aft_relative_carrier_m']+ext[0],r['payload_final_position_m'][1],r['payload_final_position_m'][2]])
    vertices=(signs*np.array([.17025,.05,.05]))@R.T+payload_mid
    mesh=Poly3DCollection([vertices[f] for f in faces],alpha=.65,facecolor='#247b9d',edgecolor='#0d3f59',linewidth=.5)
    ax.add_collection3d(mesh)
    ax.set_xlim(-.04,1.3);ax.set_ylim(-.17,.17);ax.set_zlim(-.04,.2)
    ax.set_box_aspect((3.2,1,1));ax.view_init(elev=25,azim=-65)
    ax.set_xlabel('X from carrier aft (m)');ax.set_ylabel('Y (m)');ax.set_zlabel('Z (m)')
    ax.set_title(f'{name}: final native pose\n{r["tend_s"]-r["source_release_s"]:.3f} s after source unload')
fig.suptitle('CAD-derived collision-surface proxy and native final payload poses')
fig.tight_layout();fig.savefig(HERE/'NATIVE_POSE_CAPTURE.png',dpi=180);plt.close(fig)

paths=[p for p in HERE.rglob('*') if p.is_file() and p.name!='MANIFEST.json' and '__pycache__' not in str(p) and p.suffix not in ['.pyc']]
manifest={'configuration_id':'VOLLEY-G5-ACR1','review_date_utc':'2026-10-25','public_distribution':'Project source/results/plots only;runtime engine remains outside repository','files':[{'path':str(p.relative_to(HERE)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(paths)]}
(HERE/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['completed_runs','planned_runs','maximum_total_x_momentum_residual_Ns','maximum_payload_linear_impulse_residual_Ns','maximum_payload_angular_impulse_residual_Nms','maximum_contact_vs_generalized_force_error_N','maximum_native_iterations','full_budget_steps','native_warning_increments']},indent=2))
