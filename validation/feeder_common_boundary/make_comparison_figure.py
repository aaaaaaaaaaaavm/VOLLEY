"""Plot measured CAD subtotals and separately listed, unintegrated catalog options."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parent
d=json.loads((R/'release/REVIEW.json').read_text());rows=d['comparison']
names={'lead_screw':'Captive lead screw','spring_dual_gate':'Spring / dual gate','rack_pawl':'Rack / pawl','indexed_drum':'Indexed drum','pantograph':'Pantograph','telescopic':'Nested telescope','belt_shuttle':'Belt shuttle'}
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','savefig.facecolor':'white'})
fig,ax=plt.subplots(figsize=(9.2,4.4));ys=list(range(len(rows)))
a=ax.barh([y-.18 for y in ys],[r['modeled_custom_material_kg']for r in rows],height=.32,color='#245b78',label='Represented CAD material, R1')
b=ax.barh([y+.18 for y in ys],[r['catalog_hardware_option_subtotal_kg']for r in rows],height=.32,facecolor='white',edgecolor='#666666',label='Listed catalog options; unintegrated')
for bars in [a,b]:
 for rect in bars:ax.text(rect.get_width()+.18,rect.get_y()+rect.get_height()/2,f'{rect.get_width():.2f}',va='center',fontsize=9)
ax.set_yticks(ys,[names[r['candidate']]for r in rows]);ax.invert_yaxis();ax.set_xlim(0,24);ax.set_xlabel('Mass subtotal [kg]');ax.xaxis.grid(True,alpha=.16);ax.set_axisbelow(True);fig.legend(handles=[a,b],loc='upper center',bbox_to_anchor=(.5,.95),ncol=2,frameon=False,fontsize=9)
fig.suptitle('Four stored payloads, one common receiver: partial mass accounting',fontsize=12,x=.5,y=.99)
fig.text(.02,.015,'FDR09 / R1 · two 1U + two 3U · complete installed mass, CG and inertia unestablished · no eligible downselect',fontsize=8.5)
fig.tight_layout(rect=(0,.06,1,.89))
for ext in ['png','pdf','svg']:fig.savefig(R/f'comparison_mass.{ext}',dpi=220)
plt.close(fig)
