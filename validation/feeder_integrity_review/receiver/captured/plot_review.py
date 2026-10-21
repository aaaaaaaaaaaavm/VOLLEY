"""Scientific exports of captured receiver geometry and native fixture results.

No synthetic application UI, experimental data or confidence intervals.
"""
from pathlib import Path
import json,csv,hashlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
H=Path(__file__).resolve().parent;O=H/'figures';O.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,'axes.spines.right':False,'axes.linewidth':.7,'lines.linewidth':1.3,'svg.hashsalt':'VOLLEY-FLR01','svg.fonttype':'none','pdf.fonttype':42,'ps.fonttype':42,'savefig.facecolor':'white'})
labels=['FM02','FM03','FM06'];colors={'FM02':'#6d7780','FM03':'#215c85','FM06':'#985b32'}
results={n:json.loads((H/'fea'/n/'CHECKED_RESULTS.json').read_text()) for n in labels}
def finest(rev,size,pattern):
 return max([r for r in results[rev]['native_cases'] if r['case'].startswith(size+'_') and r['case'].endswith('/'+pattern)],key=lambda r:r['mesh']['C3D10_elements'])
def save(fig,name):
 fig.tight_layout()
 for ext in ['png','svg','pdf']:fig.savefig(O/(name+'.'+ext),dpi=300,metadata={'Creator':'VOLLEY scientific plotting source'} if ext=='pdf' else None)
 plt.close(fig)
# A compact single-column figure uses identical axes and an explicit unit load.
fig,axs=plt.subplots(1,2,figsize=(6.4,2.7))
for ax,size in zip(axs,['1U','3U']):
 for i,rev in enumerate(labels):
  vals=[finest(rev,size,p)['loaded_face_mean_displacement_mm'] for p in ['split','one_dog']]
  ax.plot([0,1],vals,'o-',color=colors[rev],label=rev,ms=4)
  for x,y in enumerate(vals if rev!='FM03' else []):ax.annotate(f'{y:.3f}',(x,y),xytext=(5,5),textcoords='offset points',fontsize=8)
 ax.set_yscale('log');ax.set_ylim(.02,3);ax.set_xticks([0,1],['Shared','One dog']);ax.set_title(size+' · 1,000 N reference');ax.set_ylabel('Mean loaded-face displacement [mm]');ax.grid(axis='y',color='.9',lw=.5);ax.legend(frameon=False,fontsize=8)
save(fig,'component_compliance')
fig,axs=plt.subplots(2,2,figsize=(6.4,4.5))
for i,size in enumerate(['1U','3U']):
 for j,pattern in enumerate(['split','one_dog']):
  ax=axs[i,j]
  for rev in labels:
   rr=sorted([r for r in results[rev]['native_cases'] if r['case'].startswith(size+'_') and r['case'].endswith('/'+pattern)],key=lambda r:r['mesh']['C3D10_elements'])
   ax.plot([r['mesh']['C3D10_elements'] for r in rr],[r['loaded_face_mean_displacement_mm'] for r in rr],'o-',ms=3,color=colors[rev],label=rev)
  ax.set_yscale('log');ax.set_xlabel('C3D10 elements [count]');ax.set_ylabel('Mean displacement [mm]');ax.set_title(size+' / '+pattern.replace('_',' '));ax.grid(axis='y',color='.9',lw=.5);ax.legend(frameon=False,fontsize=8);ax.ticklabel_format(axis='x',style='sci',scilimits=(0,0))
save(fig,'mesh_convergence')
sections=json.loads((H/'SECTIONS.json').read_text());fig,axs=plt.subplots(1,3,figsize=(6.8,4.0))
for ax,record in zip(axs,sections):
 rev=record['revision']
 for edge in record['YZ_curves_mm']:ax.plot([p[0] for p in edge],[p[1] for p in edge],color=colors[rev],lw=1)
 z=-10 if rev=='FM02' else 0
 ax.add_patch(Circle((-10,z),1.65,fill=False,ec='#a24a23',lw=1.3))
 ax.annotate('Clamped bore\nin component fixture',xy=(-10,z),xytext=(-23,-24),fontsize=8,arrowprops={'arrowstyle':'-','lw':.7})
 ax.annotate('',xy=(-.5,26),xytext=(7,26),arrowprops={'arrowstyle':'->','lw':.9});ax.text(3.5,29,'−Y force',ha='center',va='bottom',fontsize=8)
 ax.set_aspect('equal');ax.set_xlim(-25,11);ax.set_ylim(-65,36);ax.set_xlabel('Y [mm]');ax.set_ylabel('Z [mm]');ax.set_title(rev+' · actual CAD section')
save(fig,'receiver_section')
# All numerical cases are tabulated without treating them as physical trials.
rows=[]
for rev,d in results.items():
 for r in d['native_cases']:
  rows.append({'revision':rev,'case':r['case'],'elements':r['mesh']['C3D10_elements'],'h_max_mm':r['mesh']['h_max_mm'],'mean_displacement_mm_at_1000N':r['loaded_face_mean_displacement_mm'],'maximum_Y_mm_at_1000N':r['max_abs_Y_mm_at_1000N'],'maximum_vm_MPa_at_1000N':r['max_vm_MPa_at_1000N'],'force_balance_error':r['force_balance_relative_error'],'moment_balance_error':r['moment_balance_relative_error']})
with (H/'COMPONENT_CASES.csv').open('w',newline='') as f:
 writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
summary={}
for size in ['1U','3U']:
 a=finest('FM02',size,'one_dog');b=finest('FM06',size,'one_dog')
 summary[size]={'baseline_case':a['case'],'revised_case':b['case'],'baseline_max_Y_mm':a['max_abs_Y_mm_at_1000N'],'revised_max_Y_mm':b['max_abs_Y_mm_at_1000N'],'baseline_mean_face_mm':a['loaded_face_mean_displacement_mm'],'revised_mean_face_mm':b['loaded_face_mean_displacement_mm'],'mean_fixture_displacement_reduction_fraction':1-b['loaded_face_mean_displacement_mm']/a['loaded_face_mean_displacement_mm']}
(H/'COMPONENT_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n');print(summary)
