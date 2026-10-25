"""Scientific figures from captured solver outputs; no synthetic result curves."""
import json,hashlib
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
P=Path(__file__).resolve().parent

def read(s):return json.loads((P/s).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 plt.style.use(P/'scientific.mplstyle');out=P/'figures';out.mkdir(exist_ok=True);inventory=[]
 def save(fig,name,inputs,description):
  fig.tight_layout()
  for ext in ['png','pdf','svg']:fig.savefig(out/(name+'.'+ext),dpi=220)
  plt.close(fig);inventory.append(dict(figure=name,description=description,source_script='make_figures.py',source_sha256=sha(Path(__file__)),inputs=[dict(path=s,sha256=sha(P/s)) for s in inputs],files=[f'figures/{name}.{ext}' for ext in ['png','pdf','svg']]))
 a=read('THERMAL_RESULTS.json');b=read('THERMAL_CORRECTIONS.json');n=read('NUMERICAL_VERIFICATION.json');v=read('DERATED_SOURCE_RESULTS.json')
 ref=read('results/reference_1mps.json');hot=read('results/hot_1mps.json');corr=next(r for r in b['corrected86p4V_cases'] if r['context']=='bounded_contact_corner' and r['command_m_s']==3);der=next(r for r in b['derated78p4V_cases'] if r['context']=='bounded_contact_corner' and r['command_m_s']==3)
 fig,axs=plt.subplots(2,2,figsize=(10,6.5),sharex=True)
 for ax,r,title,limit in zip(axs.flat,[ref,hot,corr,der],['Reference, 86.4 V; 1 m/s','Hot baseline, 86.4 V; 1 m/s','Hot contact corner +3 W/K, 86.4 V; 3 m/s','Hot contact corner, 78.4 V; 3 m/s'],[65,65,65,85]):
  h=np.array(r['history']);t=h[:,0]/60
  for idx,label in [(6,'Source cells'),(1,'Copper bulk'),(4,'Magnets'),(5,'Pallet')]:ax.plot(t,h[:,idx+1]-273.15,label=label)
  ax.axhline(limit,c='k',ls='--',lw=1,label=f'Cell catalogue {limit}°C');ax.axvline(90,c='.4',ls=':',lw=.8);ax.set(title=title,ylabel='Temperature (°C)');ax.grid(alpha=.2)
 axs[1,0].set_xlabel('Campaign time (min)');axs[1,1].set_xlabel('Campaign time (min)');axs[0,0].legend(fontsize=8,ncol=2)
 save(fig,'duty_temperatures',['results/reference_1mps.json','results/hot_1mps.json','THERMAL_CORRECTIONS.json'],'Actual24-node histories; release campaign ends90min, followed byoneorbit. Each source limit applies only tosourcecells,not othermaterials.')
 fig,ax=plt.subplots(figsize=(7,4.4))
 for context,label in [('reference_hot','Reference contacts'),('bounded_contact_corner','Adverse contact corner')]:
  points={}
  for r in b['evaluation_receipts']:
   if r['context']==context and r['host_interface_C']==50 and r['variant']=='86.4V':points[r['direct_source_host_G_W_K']]=max(points.get(r['direct_source_host_G_W_K'],-1e9),r['cell_max_C'])
  xy=sorted((g,t) for g,t in points.items() if g<=4);ax.plot(*np.array(xy).T,'o-',ms=3,label=label)
 ax.axhline(65,c='k',ls='--',label='65°C catalogue band');ax.axhline(60,c='.4',ls=':',label='60°C monitoring allocation');ax.axvline(3,c='C2',ls='--',lw=1)
 refined=next(r for r in n['rows'] if r['case']=='corrected86p4V_cases');ax.plot(3,refined['result']['temperature_max_C'][6],'*',ms=12,c='C3',label='8192 rays / 5 s corner')
 ax.set(xlabel='Direct source plate to regulated host conductance (W/K)',ylabel='Maximum source-cell temperature (°C)',title='Hot environment; regulated host interface 50°C');ax.grid(alpha=.2);ax.legend(fontsize=8)
 save(fig,'conductance_correction',['THERMAL_CORRECTIONS.json','NUMERICAL_VERIFICATION.json'],'Actual bounded solver trials andrefinement; interpolated lines join sampled evaluations anddo notextend thetested envelope.')
 groups={}
 for r in a['uncertainty']:
  if r['sample'] not in groups or groups[r['sample']]['temperature_max_C'][6]<r['temperature_max_C'][6]:groups[r['sample']]=r
 rs=list(groups.values());temp=np.array([r['temperature_max_C'][6] for r in rs]);opt=np.array([r['environment']['optical_fraction'] for r in rs]);host=np.array([r['environment']['host_interface_C'] for r in rs])
 keys=[k for k,vv in read('THERMAL_INPUTS.json')['uncertainty'].items() if isinstance(vv,list)];s=[]
 for k in keys:
  values=[r['environment'].get(k,r['parameters'].get(k)) for r in rs];rho=float(spearmanr(values,temp).statistic);s.append((k,rho))
 s=sorted(s,key=lambda x:abs(x[1]),reverse=True)[:8]
 fig,(ax,ax2)=plt.subplots(1,2,figsize=(10,4.3),gridspec_kw={'width_ratios':[1,1.2]})
 sc=ax.scatter(opt,temp,c=host,s=24,cmap='viridis');ax.scatter(0,hot['temperature_max_C'][6],marker='X',s=70,c='C3',label='Deterministic hot corner');ax.axhline(65,c='k',ls='--');ax.set(xlabel='Optical finish interpolation (0 bright; 1 dark)',ylabel='Maximum source-cell temperature (°C)',title='64 input sets; maximum of1/3 m/s');ax.legend(fontsize=8);fig.colorbar(sc,ax=ax,label='Host interface (°C)')
 ax2.barh([k.replace('_',' ') for k,rho in s][::-1],[rho for k,rho in s][::-1]);ax2.set(xlabel='Sample Spearman rank association',title='Sensitivity within declared input bands',xlim=(-1,1));ax2.grid(axis='x',alpha=.2)
 save(fig,'uncertainty_sensitivity',['THERMAL_RESULTS.json','THERMAL_INPUTS.json'],'Latin-hypercube64designpoints,not a probability orreliability claim. The sampledset missesthe deterministichotcorner. Association isnot causalvariance decomposition; unusedcase-to-sinkparameter hasno networkeffect.')
 old=read('inputs/COUPLED_SHOT.json')['cases'];fig,(ax,ax2)=plt.subplots(1,2,figsize=(10,4.3));markers={3e-6:'o',20e-6:'s',100e-6:'^'}
 for adverse in [False,True]:
  for L in markers:
   rows=[r for r in v['cases'] if r['adverse']==adverse and r['inductance_H']==L];ax.plot([r['target_m_s'] for r in rows],[r['maximum_cell_terminal_or_internal_V'] for r in rows],marker=markers[L],ls='--' if adverse else '-',label=f'{L*1e6:g} µH, '+('adverse' if adverse else 'nominal'))
 ax.axhline(2.5,c='k',ls='--',label='85°C catalogue maximum');ax.axhline(2.47,c='.4',ls=':',label='Regen command ceiling');ax.set(xlabel='Commanded payload speed (m/s)',ylabel='Maximum cell-equivalent voltage (V)',ylim=(2.44,2.51),xticks=[1,2,3]);ax.legend(fontsize=7,ncol=2)
 width=.32;bottoms=np.zeros((2,2));x=np.arange(2)
 for key,label in [('copper_J','Copper'),('inverter_J','Inverter'),('bank_J','Source ESR'),('auxiliary_J','Auxiliary')]:
  for j,(cases,offset,hatch) in enumerate([(old,-width/2,''),(v['cases'],width/2,'//')]):
   heights=[next(r for r in cases if r['target_m_s']==u and r['adverse'] and r['inductance_H']==3e-6)['energy_ledger'][key] for u in [1,3]]
   ax2.bar(x+offset,heights,width,bottom=bottoms[j],label=label if j==0 else None,hatch=hatch);bottoms[j]+=heights
 ax2.set(xticks=x,xticklabels=['1 m/s','3 m/s'],ylabel='Actual shot heat ledger (J)',title='86.4 V (left), 78.4 V (hatched right)');ax2.legend(fontsize=8)
 save(fig,'derated_source',['DERATED_SOURCE_RESULTS.json','inputs/COUPLED_SHOT.json'],'All18unchanged-production cases; exact actual heatledgers used inhot thermalvariant. The30mV/cell margin is a controlallocation requiring32-group sensing andphysical transient verification.')
 (P/'FIGURE_SOURCE_INVENTORY.json').write_text(json.dumps(inventory,indent=2)+'\n');(P/'SENSITIVITY_SUMMARY.json').write_text(json.dumps(dict(sample_sets=len(rs),max_sample_cell_C=float(temp.max()),deterministic_hot_cell_C=hot['temperature_max_C'][6],rank_associations=[dict(parameter=k,rho=r) for k,r in s]),indent=2)+'\n')
if __name__=='__main__':main()
