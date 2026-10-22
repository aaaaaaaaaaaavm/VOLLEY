"""Replot the captured FCE13 values at the intended full-page publication width."""
from pathlib import Path
import json,csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parent
rows=list(csv.DictReader((R/'COMPARISON_TIMESERIES.csv').open()))
summary=json.loads((R/'SUMMARY.json').read_text())
plt.rcParams.update({'font.size':7.5,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42,'svg.fonttype':'none'})
fig,axs=plt.subplots(1,3,figsize=(7.2,2.65),layout='constrained',gridspec_kw={'width_ratios':[1,1,.88]})
t=[float(r['time_s'])for r in rows]
series=[('1U PSOR','#0072B2','1U PSOR'),('3U PSOR','#D55E00','3U PSOR'),('3U BB','#009E73','3U BB'),('3U box core / PSOR','#CC79A7','3U box')]
for name,color,label in series:
 for ax,quantity in zip(axs[:2],['COM_delta_mm','orientation_delta_deg']):ax.plot(t,[float(r[name+' '+quantity])for r in rows],label=label,color=color,lw=.9)
for ax in axs[:2]:
 ax.axhline(.05,color='#333333',ls='--',lw=.8);ax.axvspan(5,10,color='#777777',alpha=.09)
 ax.set_xlim(0,26.5);ax.set_xticks([0,10,20]);ax.set_xlabel('Time [s]');ax.grid(alpha=.16)
axs[0].set_title('A  COM refinement');axs[1].set_title('B  Orientation refinement')
axs[0].set_ylabel('COM difference [mm]');axs[1].set_ylabel('Orientation difference [deg]')
axs[0].legend(loc='upper left',fontsize=6.5,frameon=False,handlelength=1.2)
ids=['P3-250','W3-250','B3-250','B3-125','X3-250','X3-125']
values=[100*summary['completed_native_runs'][i]['solver_metrics']['saturated_steps']/summary['completed_native_runs'][i]['metrics']['steps']for i in ids]
axs[2].bar(range(6),values,color=['#0072B2','#56B4E9','#009E73','#009E73','#CC79A7','#CC79A7'])
axs[2].set_xticks(range(6),['P\n250','W\n250','BB\n250','BB\n125','Box\n250','Box\n125'],fontsize=6.5)
axs[2].set_xlabel('Solver / step [µs]');axs[2].set_ylabel('Full-budget steps [%]');axs[2].set_ylim(0,8)
axs[2].set_title('C  3U iteration budget');axs[2].grid(axis='y',alpha=.16);axs[2].set_axisbelow(True)
for j,v in enumerate(values):axs[2].text(j,v+.15,f'{v:.2f}',ha='center',fontsize=6.5)
for ext in ['png','pdf','svg']:fig.savefig(R/f'convergence_publication.{ext}',dpi=300)
plt.close(fig)
