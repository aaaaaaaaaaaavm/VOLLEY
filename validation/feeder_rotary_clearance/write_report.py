"""Build the compact engineering note and figures from captured numeric results."""
from pathlib import Path
import hashlib,json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,Image

H=Path(__file__).resolve().parent
d=json.loads((H/'CONTINUOUS_ROTARY_CLEARANCE.json').read_text())
x=json.loads((H/'DELTA_AND_EXPORT.json').read_text())
s=json.loads((H/'INDEPENDENT_STEP.json').read_text())
assert d['all_passed'] and len(d['cases'])==4 and len(s['cases'])==10
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,
                     'axes.spines.right':False,'svg.fonttype':'none','savefig.dpi':180})
fig,ax=plt.subplots(1,2,figsize=(9,3.1),layout='constrained')
for key,col,label in [('r5_gap_mm','#6b7280','R5'),('r6_gap_mm','#1f5e89','R6 candidate')]:
    q=[r for r in x['contact_comparison'] if r['size']=='1U' and r['angle_deg']<=1]
    ax[0].plot([r['angle_deg'] for r in q],[r[key] for r in q],'o-',color=col,ms=3,label=label)
ax[0].set(xlabel='Gate opening angle (deg)',ylabel='Door-to-sled distance (mm)',title='A  Near-closed native distances')
ax[0].legend(frameon=False,fontsize=8)
labels=[c['payload']+' '+c['direction'] for c in d['cases']]
values=[c['minimum_guarded_lower_bound_mm']*1000 for c in d['cases']]
ax[1].bar(range(4),values,color='#1f5e89',width=.6)
ax[1].set(xticks=range(4),xticklabels=labels,ylabel='Conservative bound (micrometres)',title='B  Complete 0–90 deg interval screen',ylim=(0,max(values)*1.3))
ax[1].tick_params(axis='x',labelsize=8)
for i,v in enumerate(values):ax[1].text(i,v+.3,f'{v:.3f}',ha='center',fontsize=8)
for a in ax:a.grid(axis='y',color='#d9dde1',lw=.5);a.set_axisbelow(True)
F=H/'figures';F.mkdir(exist_ok=True)
for ext in ['png','svg']:fig.savefig(F/('rotary_clearance.'+ext))
plt.close(fig)
method='A rigid rotation through at most half an angular interval moves any gate point by no more than 2 R sin(w/4), where R bounds its radius and w is the full interval width in radians. Native midpoint distance minus this displacement and a 0.00001 mm numerical guard gives the interval lower bound. Adaptive bisection covers every angle for every stationary obstacle. The source-verified coaxial hinge uses rotational invariance. This is a numerical nominal-geometry screen, not a manufacturing tolerance or a formally certified kernel error bound.'
minimum=min(c['minimum_guarded_lower_bound_mm'] for c in d['cases'])
body=f'''# Feeder exit-gate rotary clearance — FM07-R6 candidate

## Engineering result

The R5 gate panel shares a zero-clearance surface with the sled deck at the checked near-closed angles (0–0.5 degrees). Native intersection volume at those samples is zero: this is surface contact, not a demonstrated volumetric collision. The panel's lower edge is raised from z=22.00 to z=22.25 mm and its height reduced from 18.00 to 17.75 mm; its upper edge, hinge, locks and other components remain unchanged.

The R6 candidate passes all four nominal continuous rotary screens: opening and closing, 1U and 3U. The smallest guarded conservative lower bound is **{minimum:.9f} mm** across those angle intervals. It is a computed conservative bound, not a measured or qualified clearance. Eight full native assemblies and two individual gate STEP files passed separate CadQuery readback.

## Method

{method}

## Change verification

The source change is restricted to the gate panel's lower edge/height and revision label. Eight exported states verify that the new gate remains one valid solid, removes 41 mm³ and adds no material outside R5. All other components match R5, and all component pairs have no detected volumetric penetration at those states. Under the unchanged rigid motions, a material subset cannot introduce a new intersection with previously nonintersecting geometry. This inherits only the prior nominal nonpenetration evidence; it does not establish loaded clearance or contact dynamics.

At an assumed steel density of 7850 kg/m³, the material change is a reduction of 0.32185 g per gate. This is a material delta, not an installed-system mass.

## Interpretation and remaining work

The nominal gate/deck rubbing contact is removed in this separate candidate revision. Tolerance stacks, thermal expansion, joint compliance, actuation loads, stress, wear, power-off behavior and multi-cell integration still require their existing checks. FM06/FCE12 contact results do not validate the R6 assembly. No feeder downselect or D27 acceptance follows from this result. R5 and the evaluated Gen5 record remain preserved.

## Evidence and reproduction

- [Captured intervals](CONTINUOUS_ROTARY_CLEARANCE.json) and [checker](check_rotary.py).
- [Native change audit and exports](DELTA_AND_EXPORT.json), [CAD and STEP](cad/), [independent readback](INDEPENDENT_STEP.json).
- [Native-distance and interval figure](figures/rotary_clearance.svg).
- [Preserved R5 evidence](reference_r5/) and [R5 source](reference_r5/mechanism.py).
- FreeCAD runtime: run check_rotary.py and export_delta.py; CadQuery runtime: run readback_step.py. Run write_report.py after the capture and STEP checks. check_capture.py verifies the packaged identities without rerunning CAD.

Figure evidence class: computed native-geometry results. Source: DELTA_AND_EXPORT.json and CONTINUOUS_ROTARY_CLEARANCE.json; configuration FM07-R6-CANDIDATE. No physical measurements.
'''
(H/'README.md').write_text(body)
styles=getSampleStyleSheet();styles['BodyText'].fontSize=9;styles['BodyText'].leading=12
parts=[Paragraph('Feeder exit-gate rotary clearance',styles['Title']),Paragraph('FM07-R6 candidate · nominal rigid-geometry engineering note',styles['Heading2'])]
for title,text in [('Result',body.split('## Engineering result\n\n')[1].split('\n\n## Method')[0]),('Method',method),('Change and applicability',body.split('## Change verification\n\n')[1].split('\n\n## Evidence')[0])]:
    parts.append(Paragraph(title,styles['Heading2']))
    for para in text.split('\n\n'):
        if para.startswith('## '):continue
        parts.extend([Paragraph(para.replace('**',''),styles['BodyText']),Spacer(1,2*mm)])
parts.insert(5,Image(str(F/'rotary_clearance.png'),width=175*mm,height=60.3*mm))
parts.append(Paragraph('Source: DELTA_AND_EXPORT.json; CONTINUOUS_ROTARY_CLEARANCE.json; INDEPENDENT_STEP.json. Numeric guard is a declared computation parameter, not a qualified physical tolerance.',styles['BodyText']))
doc=SimpleDocTemplate(str(H/'FEEDER_ROTARY_CLEARANCE.pdf'),pagesize=(210*mm,297*mm),leftMargin=17*mm,rightMargin=17*mm,topMargin=16*mm,bottomMargin=16*mm,title='VOLLEY feeder rotary-clearance study',author='Adityavardhan Mishra')
doc.build(parts)
print('Report, PNG/SVG and README built from verified records.')
