"""Build a short, standalone report from the captured orbit evidence."""
from pathlib import Path
import json
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Image,PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
ROOT=Path(__file__).resolve().parent

def main():
 styles=getSampleStyleSheet();styles['BodyText'].fontSize=10;styles['BodyText'].leading=14
 styles['Title'].alignment=TA_LEFT
 doc=SimpleDocTemplate(str(ROOT/'ORBIT_EVIDENCE_BRIEF.pdf'),pagesize=(595.28,841.89),leftMargin=42,rightMargin=42,topMargin=42,bottomMargin=42)
 d=json.loads((ROOT/'ORBIT_RESULTS.json').read_text());story=[]
 def para(s,style='BodyText'):story.append(Paragraph(s,styles[style]));story.append(Spacer(1,10))
 para('VOLLEY | Orbital analysis','Title');para('Native solver evidence supplement — 18 October 2026','Heading2')
 para('Purpose: show what commanded relative release inputs change in the orbit, how the numerical implementations compare, and what the archived twelve-orbit campaign does not establish.')
 para('Case definition','Heading2');para('450 km circular reference; 51.6° inclination; 4 kg payload and 300 kg remaining host. At 16.029 m/s relative release, the payload inertial velocity increment is 15.818092105 m/s. The numerical release inputs are prescribed, not measured motor performance.')
 para('Execution record','Heading2');para('Orekit 13.1.6: queued single-release case, plus eight 24-hour central-gravity/J2 histories, repeated with 60 s and 30 s maximum integration steps. GMAT R2026a: repaired queued case plus two fresh one-day histories. Archived GMAT R1: twelve preloaded post-release orbits, 90 days; not a coupled deployment campaign.')
 para('Observed numerical differences','Heading2')
 para(f"Largest Orekit refinement difference: {max(c['max_refinement_position_m']for c in d['cases']):.6g} m. Independent SciPy DOP853 difference: {max(c['max_scipy_position_difference_m']for c in d['cases']):.6g} m. Harmonized-central-constant GMAT comparison: {d['matched_central_gravity']['max_position_difference_m']:.6g} m. J2 setup difference: {d['cross_code'][1]['max_position_difference_m']/1000:.4f} km; not a matched-force validation.")
 para('Interpretation','Heading2');para('No new hardware qualification, provider compatibility, release accuracy, atmospheric lifetime or collision-risk result is established. Thresholds were not preregistered before exploratory runs. The unresolved J2 setup discrepancy remains a follow-up task. Source, CSV histories, manifests and a detailed reader guide accompany this report.')
 for name,title,caption in [
 ('release_history','1 | Release-state consequences','The left panel shows radial excursion; the right is a reference local T-axis projection over one day. The reference axis moves with the no-impulse orbit. Neither panel represents a customer delivery tolerance.'),
 ('solver_comparison','2 | Solver agreement and setup differences','Central gravity constants and output epochs must be reconciled before interpreting a residual. GMAT Earth-fixed degree-2 gravity and fixed-axis Orekit J2 are not identical configurations. The larger J2 discrepancy is retained explicitly.'),
 ('numerical_checks','3 | Numerical sensitivity','Step refinement and a separate implementation test integration consistency under shared physics. They cannot quantify model error from atmosphere, payload contact, control or release dispersion.'),
 ('archived_campaign','4 | Archived campaign and close approach','The RAAN span uses circular angular extent. The five-second close-approach sample is 190.15 m; the hollow inset marker is a 180.29 m straight-line interpolation. There is no demonstrated continuous-clearance bound.')]:
  story.append(PageBreak());para(title,'Title');story.append(Image(str(ROOT/'figures'/f'{name}.png'),width=511,height=209));story.append(Spacer(1,16));para(caption);para('Source and reproducibility','Heading2');para('See validation/orbit_evidence/README.md, ORBIT_RESULTS.json and the accompanying raw histories. Figures are Matplotlib exports of computed native output; they are not application screenshots or flight observations.')
 def footer(canvas,doc):canvas.setFillColor(colors.HexColor('#555555'));canvas.setFont('Helvetica',8);canvas.drawString(42,24,'VOLLEY — computational evidence supplement');canvas.drawRightString(553,24,str(doc.page))
 doc.build(story,onFirstPage=footer,onLaterPages=footer)
 print('Standalone orbit evidence PDF built')
if __name__=='__main__':main()
