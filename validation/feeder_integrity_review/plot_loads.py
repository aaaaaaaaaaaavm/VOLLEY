"""Source-identified scientific diagrams. No generated experimental data or GUI."""
from pathlib import Path
import json,math,hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
H=Path(__file__).resolve().parent;O=H/'figures';O.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42,'svg.fonttype':'none','savefig.facecolor':'white','svg.hashsalt':'VOLLEY-FM04'})
def save(fig,n,jpg=False):
 fig.tight_layout()
 for ext in ['png','svg','pdf']+(['jpg'] if jpg else []):fig.savefig(O/(n+'.'+ext),dpi=240,bbox_inches='tight')
 plt.close(fig)
R=json.loads((H/'tine/SUMMARY.json').read_text());rr=R['native_cases']
fig,axs=plt.subplots(1,2,figsize=(6.7,2.8));ax=axs[0]
ax.plot([r['elements'] for r in rr],[r['loaded_mean_Z_mm_per_N']*1e3 for r in rr],'o-',color='#285875',label='Native C3D10 fixture',ms=4);ax.axhline(R['Euler_Bernoulli_compliance_mm_per_N']*1e3,color='#8a5636',ls='--',lw=1,label='Euler–Bernoulli');ax.set(xlabel='C3D10 elements [count]',ylabel='End compliance [µm/N]',title='a) Mesh refinement');ax.ticklabel_format(axis='x',style='sci',scilimits=(0,0));ax.legend(frameon=False,fontsize=7)
ax=axs[1]
for share,ls,label in [(.5,'-','Equal load sharing'),(1.,'--','All load on one tine')]:
 rows=[r for r in R['linear_scaled_sensitivity_cases'] if r['payload_kg']==6 and r['fraction_on_one_tine']==share];ax.plot([r['acceleration_g'] for r in rows],[r['max_Z_linear_fixture_mm'] for r in rows],marker='o',ms=3,ls=ls,color='#285875',label=label)
ax.axhline(.6,color='#a13d35',ls=':',label='Nominal slot clearance');ax.set(xlabel='Assumed acceleration [g]',ylabel='Linear fixture displacement [mm]',title='b) 6 kg sensitivity');ax.legend(frameon=False,fontsize=7)
save(fig,'tine_fixture')
R=json.loads((H/'GUIDE_PLAY.json').read_text());fig,axs=plt.subplots(1,2,figsize=(6.7,2.6))
for rev,c in [('FM03','#737d84'),('FM04','#285875')]:
 r=[r for r in R['cases'] if r['revision']==rev and r['direction']==-1];axs[0].plot([t['radial_pin_clearance_mm'] for t in r],[abs(t['dog_corner_Y_excursion_mm']) for t in r],'o-',color=c,label=rev,ms=4);axs[1].plot([t['radial_pin_clearance_mm'] for t in r],[abs(t['theta_deg']) for t in r],'o-',color=c,label=rev,ms=4)
axs[0].set(xlabel='Assumed radial pin clearance [mm]',ylabel='Rigid dog corner excursion [mm]',title='a) Clearance take-up');axs[1].set(xlabel='Assumed radial pin clearance [mm]',ylabel='Maximum rigid rocking [degree]',title='b) Finite guide overlap')
for ax in axs:ax.legend(frameon=False,fontsize=8)
save(fig,'receiver_rigid_play')
print('Tine and rigid-play scientific figures from captured results')
