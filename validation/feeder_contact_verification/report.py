"""Produce the source-linked FCE12 numerical-method report."""
from pathlib import Path
import json
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,Image,PageBreak
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.units import mm
H=Path(__file__).resolve().parent;O=H;d=json.loads((O/'RESULTS.json').read_text())
styles=getSampleStyleSheet();styles.add(ParagraphStyle('Body',parent=styles['BodyText'],fontName='Helvetica',fontSize=9.5,leading=13,spaceAfter=7));styles['Title'].fontSize=22;styles['Title'].leading=26
story=[]
def clean(s):
    substitutions={
      'imposed10µm–1mm':'imposed 10 µm–1 mm','error4.28nm':'error 4.28 nm','within1e-6':'within 1e-6',
      'reach26.5s':'reach 26.5 s','at11s':'at 11 s','after1µmYtranslation':'after 1 µm Y translation',
      'Provisional50µm/0.05deg':'Provisional 50 µm / 0.05 deg','cells:64':'cells: 64',
      '12mm':'12 mm','14mm':'14 mm','8mm':'8 mm','5µm':'5 µm','The1ms':'The 1 ms',
      'by1000':'by 1000','by10⁶':'by 10⁶','Figure1':'Figure 1','Figure2':'Figure 2','Figure3':'Figure 3',
      'Step[µs]':'Step [µs]','Work[J]':'Work [J]','4000iterations':'4000 iterations',
      'friction0':'friction 0','6kg,1g':'6 kg, 1 g','Exit0':'Exit 0','identifies a commanded':'identifies a commanded',
      ';11 identifies':'; 11 identifies','The6kg':'The 6 kg','for1U and3U':'for 1U and 3U',
      '250→125µs':'250 → 125 µs','The125µs':'The 125 µs','provisional0.05mm':'provisional 0.05 mm',
      'cover12':'cover 12','Two3U500µs':'Two 3U 500 µs','maximum0.000124mm³':'maximum 0.000124 mm³',
      'by1µm inY':'by 1 µm in Y','84selected':'84 selected','[−12,L+12]mm':'[−12, L+12] mm',
      '[14,128]mm':'[14, 128] mm','[−500,500]mm':'[−500, 500] mm',
    }
    for a,b in substitutions.items():s=s.replace(a,b)
    import re
    return re.sub(r'(?<=\d)(mm|deg|%)', r' \1', s)
def P(s,style='Body'):story.append(Paragraph(clean(s),styles[style]))
def T(rows,widths):
    t=Table([[Paragraph(clean(str(x)),styles['Body']) for x in row] for row in rows],colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e8eef2')),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,0),.6,colors.HexColor('#657585')),('LINEBELOW',(0,1),(-1,-1),.25,colors.HexColor('#cbd4dc')),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5)]));story.append(t);story.append(Spacer(1,8))
def fig(name,caption):
    story.append(Image(str(O/'figures'/name),width=174*mm,height=70.6*mm));P(caption)
def page(canvas,doc):
    canvas.setFont('Helvetica',8);canvas.setFillColor(colors.HexColor('#4b5563'));canvas.drawString(18*mm,12*mm,'VOLLEY / FCE12 / 21 October 2026');canvas.drawRightString(192*mm,12*mm,str(doc.page))
P('Feeder contact verification','Title');P('FCE12 • Native numerical method and transfer-subcycle results','Heading2')
P('Configuration: unchanged FM06-R1 reference geometry. Native solver: Project Chrono 10.0.0, rigid nonsmooth contact, Bullet collision and PSOR. Internal units are kg, mm and s; published trajectories, loads and work are converted to SI.')
P('Study question','Heading2');P('Does the collision representation resolve the actual CAD contact geometry at the relevant scale, and which transfer results remain sensitive to numerical settings? The study separates analytical calibration, geometric resolution and dynamic convergence.')
T([['Check','Outcome'],['Planar contact calibration','Both sizes detect imposed10µm–1mm overlaps; largest checked reported-gap error4.28nm. General curved-surface accuracy is not inferred.'],['Unit conversion','No-contact controller replay agrees within1e-6 in checked SI outputs.'],['Native case matrix','Ten nominal/friction/gravity cases reach26.5s; injected jam and stuck-pin cases abort at11s.'],['Full native-solid pose audit','84 targeted poses; two residual intersections admit a nonintersecting pose after1µmYtranslation.'],['Final-pose and force refinement','Provisional50µm/0.05deg final-pose screen is not met. Impulsive contact peaks are not design loads.']],[48*mm,126*mm])
P('These are computational method results. The sequence begins with the storage gate open and ends after capture and fork withdrawal. Full launch/empty return/reset, installed actuation and physical correlation are separate requirements. No feeder architecture is selected by this study.')
story.append(PageBreak())
P('1. Geometry and unit scaling','Heading1')
P('The native payload is partitioned into nine convex solids with disjoint interiors and exact B-rep union equivalence. The rounded rail and recessed-panel geometry is retained. Each mechanism is partitioned into orthogonal native material cells:64 boxes per payload size within the guarded contact domain. Full original body mass, centre of gravity and inertia are retained. Nonplanar retained mechanism material is rejected rather than approximated by a box.')
P('The payload domain is X=[−12,L+12]mm and Z=[14,128]mm; Y coverage is [−500,500]mm. Initial receiver material below14mm is retained down to8mm to cover its12mm upward stroke. Leaving the X/Z domain rejects the dynamics. The independent audit uses the complete original B-reps, including material outside the collision domain.')
T([['Quantity','Native unit','Conversion to SI'],['Position / velocity','mm / mm·s⁻¹','divide by1000'],['Mass','kg','unchanged'],['Inertia','kg·mm²','divide by10⁶'],['Force / impulse','mN / mN·s','divide by1000'],['Mechanical work','µJ','divide by10⁶'],['Angle / angular velocity','rad / rad·s⁻¹','unchanged']],[54*mm,55*mm,65*mm])
P('The assumed collision envelope is5µm, safe margin zero. The same physical numerical settings are converted consistently: gravity, actuator limits, guide resistance, penetration recovery speed and inertia. The1ms controller period and dimensionless contact coefficients are unchanged. The no-contact unit-invariance check isolates conversion correctness from collision behavior.')
fig('contact_calibration.png','Figure1. Analytical planar-gap controls and replayed fixed poses. The planar controls compare native coordinate scales. The replay uses actual captured FCE08 poses with the same material geometry; negative gap denotes detected penetration. Missing contacts are omitted from the plotted gap series.')
story.append(PageBreak())
P('2. Native case matrix','Heading1')
rows=[['Case','Payload / condition','Step[µs]','Exit','Work[J]']]
for r in d['cases']:
    condition={'time_refinement':'step refinement','iteration_refinement':'4000iterations','friction_sensitivity':f"friction{r['mu']:g}",'rigid_ground_adverse_mass':'6kg,1g rigid','deliberate_jam':'injected jam','deliberate_stuck_pin':'injected stuck pin'}[r['label']]
    rows.append([r['case_id'].replace('FCE12-',''),r['size']+' / '+condition,f"{r['dt_s']*1e6:g}",str(r['exit_code']),f"{r['positive_motor_work_J']:.5f}"])
T(rows,[17*mm,83*mm,25*mm,17*mm,32*mm])
P('Exit0 identifies the programmed endpoint;11 identifies a commanded abort. Exit codes do not measure physical reliability. Mechanical work excludes motor/inverter losses, static holding power and the installed energy source. The6kg gravity case is rigid and does not include elastic tine/root/frame deflection.')
fig('transfer_refinement.png','Figure2. Native transfer/capture/withdrawal histories for1U and3U at three integration steps. Similar travel histories do not establish agreement in final six-degree-of-freedom state.')
story.append(PageBreak())
P('3. Numerical sensitivity and geometric resolution','Heading1')
T([['Payload','250→125µs COM change','Orientation change','Work relative change']]+[[r['size'],f"{r['last_step_COM_difference_mm']:.6f}mm",f"{r['last_step_orientation_difference_deg']:.6f}deg",f"{100*r['last_step_work_relative_difference']:.6f}%"] for r in d['convergence']],[27*mm,53*mm,47*mm,47*mm])
fig('numerical_sensitivity.png','Figure3. Final-pose and rigid-contact peak sensitivity. The125µs trace is a numerical comparison reference. The provisional0.05mm screen is not met; the peak contact values are not accepted structural loads.')
P('Independent native-solid checks cover12 targeted times in each of seven nominal/iteration cases, including the earlier transfer-interference times. Two3U500µs poses retain positive material intersections: maximum0.000124mm³. Their original positions remain in NATIVE_POSE_AUDIT.json. A separate check translates the payload by1µm inY and verifies zero positive intersections with all original components. This establishes a nearby nonintersecting pose for those residuals; it does not modify the trajectories or prove continuous nonpenetration.')
P('The planar calibration and sampled full-solid checks support this collision representation at the declared numerical scale. Final-state sensitivity remains relevant because the modeled payload is loosely retained rather than correlated against a measured preloaded contact system. Precision, force ratings and wear/reliability require further contact/joint evidence.')
story.append(PageBreak())
P('4. Traceability and engineering boundary','Heading1')
P('Frozen campaign records retain exact command arguments, source/executable identities, solver outputs, CSV histories, metrics and hashes. The exact executed source is preserved under captured/. Formatted root sources are verified to have equivalent non-comment tokens. CMake builds the readable sources; a replay writes a separate output directory. MANIFEST.json identifies every distributed file.')
P('Independent checks','Heading2')
for s in ['Native B-rep volume equivalence and disjoint payload-cell interiors.','Exact orthogonal mechanism-cell volume identities and guarded-domain definition.','Fourteen analytical planar-gap controls; no-contact SI unit invariance.','Twelve native dynamic cases and seven full native-solid pose reconstructions.','84selected poses and explicit residual-resolution checks.','Separate timestep, iteration, friction, gravity and injected-fault outcomes.']:P('• '+s)
P('Engineering interpretation','Heading2')
P('This work closes a numerical representation question for the stated subcycle. It does not close source-rated actuation, joint flexibility, actual friction/compliance, payload interface approval, a complete release/reset mechanism, multi-cell installed integration or a seven-architecture downselect. Receiver and tine finite-element results belong to their separately stated fixtures. No physical prototype, measured precision, qualification or flight acceptance is represented.')
P('All source files, local replay commands, scientific figures and machine-readable criteria are included with the report. Historical FCE08 and intermediate diagnostic results remain separately traceable; they are not relabeled as accepted current performance.')
doc=SimpleDocTemplate(str(O/'FEEDER_CONTACT_VERIFICATION.pdf'),pagesize=(210*mm,297*mm),leftMargin=18*mm,rightMargin=18*mm,topMargin=18*mm,bottomMargin=20*mm,title='VOLLEY feeder contact verification — FCE12',author='VOLLEY computational study')
doc.build(story,onFirstPage=page,onLaterPages=page)
print('Built',O/'FEEDER_CONTACT_VERIFICATION.pdf')
