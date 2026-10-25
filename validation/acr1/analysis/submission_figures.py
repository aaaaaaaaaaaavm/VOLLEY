"""Publication figures from the frozen coupled-shot result; no new simulation."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1];O=R/'figures';O.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'legend.frameon':False,'savefig.facecolor':'white'})
d=json.loads((R/'analysis/COUPLED_SHOT.json').read_text());c=next(v for v in d['cases'] if v['target_m_s']==3 and not v['adverse'] and abs(v['inductance_H']-20e-6)<1e-12)
a=np.array([v[:7]for v in c['trace']],float)
fig,axs=plt.subplots(3,1,figsize=(7.3,6.8),sharex=True,layout='constrained')
for ax,cols,labels,ylabel in [(axs[0],[2],['Relative carrier speed'],'Speed (m/s)'),(axs[1],[3],['Signed current amplitude'],'Current (A)'),(axs[2],[4,5],['Internal capacitor voltage','Terminal voltage'],'Voltage (V)')]:
 for j,col in enumerate(cols):ax.plot(a[:,0],a[:,col],label=labels[j],lw=1.5,color=['#164c70','#ac6535'][j])
 ax.axvline(c['release']['time_s'],color='#666666',lw=.8,ls='--');ax.set_ylabel(ylabel);ax.grid(alpha=.16);ax.legend(fontsize=8,loc='best')
axs[-1].set_xlabel('Time from shot command (s)');fig.suptitle('3 m/s reference shot — nominal source, 20 µH',fontsize=12)
for ext in ['png','pdf']:fig.savefig(O/f'coupled_shot_reference.{ext}',dpi=200,bbox_inches='tight')
plt.close(fig)
e=c['energy_ledger'];labels=['Mechanical','Copper','Inverter','Bank ESR','Auxiliary'];vals=[e[k]for k in ['mechanical_J','copper_J','inverter_J','bank_J','auxiliary_J']]
fig,ax=plt.subplots(figsize=(7.3,3.4),layout='constrained');y=np.arange(len(vals));ax.barh(y,vals,color=['#164c70','#ac6535','#71828e','#aab5bc','#cbd0d4']);ax.set_yticks(y,labels);ax.invert_yaxis();ax.set_xlabel('Net shot energy contribution (J)');ax.set_xlim(0,190);ax.grid(axis='x',alpha=.15);ax.set_axisbelow(True)
for i,v in enumerate(vals):ax.text(v+2,i,f'{v:.2f}',va='center',fontsize=9)
ax.set_title(f'Source draw: {c["cap_draw_J"]:.2f} J — same reference shot',loc='left',fontsize=12)
for ext in ['png','pdf']:fig.savefig(O/f'shot_energy_ledger.{ext}',dpi=200,bbox_inches='tight')
plt.close(fig)
print('Created coupled trace and energy PNG/PDF pairs.')
