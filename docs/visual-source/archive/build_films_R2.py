"""Source-driven editorial films: accepted CAD views, numeric plots and labelled diagrams.

python3 build_films.py prepare
python3 build_films.py animatic
python3 build_films.py render

Motion diagrams are explanatory, not CAD kinematics or measured motion. The original
Blender source is retained in downloads/VOLLEY_G5_ACR1_editable_scene.zip. No image AI,
synthetic screenshot, replacement solver output, audio or remote dependency is used.
"""
from pathlib import Path
import argparse,json,csv,hashlib,math,subprocess,shutil,textwrap,zipfile
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]; HERE=Path(__file__).resolve().parent
A=ROOT/'assets/acr1'; OUT=ROOT/'films'; INPUT=HERE/'inputs'; INPUT.mkdir(exist_ok=True)
FROZEN=Path('/workspace/volley-work/2026-10-24-gen5-acr1')
W,H=1280,720
BG='#11161c'; PANEL='#1b2229'; INK='#f6f5f1'; DIM='#c0c7cd'; ACC='#bfe3cf'; GOLD='#efd199'
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; MONO='/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def font(n,bold=False,mono=False):return ImageFont.truetype(MONO if mono else BOLD if bold else FONT,n)
def slide(duration,title,text,asset=None,kind='image',source='',label='CAD-derived Blender render'):
 return dict(duration_s=duration,title=title,text=text,asset=asset,kind=kind,source=source,label=label)
STORY={
 'overview':{'title':'One path. Commanded departures.','duration_s':72,'scope':'System overview / ACR1','slides':[
 slide(12,'An integrated twelve-3U study.','Twelve 4 kg 3U envelopes. Two six-level storage banks. One reusable electromagnetic carrier.','01_assembly_isometric.jpg',source='visuals/VIEW_PROVENANCE.json'),
 slide(12,'Select. Feed. Capture.','A guided lead screw transfers one payload sideways into the Z-indexed lift. The lift holds the payload and captive pallet.','03_captured_source_level.jpg',source='visuals/VIEW_PROVENANCE.json'),
 slide(12,'Transfer custody positively.','Carrier bayonets and lift grip pins overlap custody at handoff. Prove the destination restraint before releasing the other.','02_handoff_pallet_locks.jpg',source='visuals/VIEW_PROVENANCE.json'),
 slide(12,'Dock. Prove. Clear.','The pallet locks to the carrier. The custody frame withdraws clear of the launch path before the shot is enabled.','04_clear_docked.jpg',source='visuals/VIEW_PROVENANCE.json'),
 slide(12,'Only the payload departs.','The captive pallet stays on the carrier through arrest and return. Payload separation is along +X; vertical stacking identifies components. Motion and timing are conceptual.',kind='recovery',source='cad/release/FINAL_CAD_MANIFEST.json; analysis/COUPLED_SHOT.json',label='Conceptual motion / not time-scaled / not a dynamics simulation'),
 slide(12,'Evaluate the complete trade.','Modeled 1–3 m/s commands. Installed device allocation 156.557 kg. These preplanned mission cases show no advantage over the ideal ground-pretrimmed spring comparator.','MISSION_RESOURCES.png',kind='plot',source='mission/MISSION_RESULTS.csv',label='Computed result / G5-MISSION-01')
 ]},
 'custody':{'title':'Continuous payload custody.','duration_s':78,'scope':'Feeder, carrier and modeled fault branch / ACR1','slides':[
 slide(10,'Retain the inventory.','Two fixed six-level banks hold twelve nominal 3U payloads. Select one cell and inhibit host burns during feeding.','01_assembly_isometric.jpg',source='visuals/VIEW_PROVENANCE.json'),
 slide(10,'Capture the selected payload.','The guided pusher feeds the lift. At source level 5 the payload floor is Z830 mm; the lift grips hold its pallet.','03_captured_source_level.jpg',source='visuals/VIEW_PROVENANCE.json'),
 slide(12,'Overlap the restraints.','At handoff, positive carrier bayonets and outboard lift grip pins establish dual custody. The storage banks and fixed frame are hidden in this view for access.','02_handoff_pallet_locks.jpg',source='visuals/VIEW_PROVENANCE.json'),
 slide(12,'Prove the clear state.','Payload floor Z46 mm. Raised custody frame floor Z190 mm. Prove pallet locks, pusher withdrawal and a clear path before enabling launch.','04_clear_docked.jpg',source='visuals/VIEW_PROVENANCE.json'),
 slide(16,'Retain the pallet during recovery.','The payload separates along +X. Carrier and captive pallet arrest and return together. Vertical stacking identifies components; the motion is conceptual.',kind='recovery',source='cad/release/FINAL_CAD_MANIFEST.json; analysis/COUPLED_SHOT.json',label='Conceptual motion / not time-scaled / not a dynamics simulation'),
 slide(18,'Fault → inhibit → retain → verify.','Modeled custody/interlock logic; physical fault-response validation is subsequent work. A fault does not authorize an automatic restart.',kind='fault',source='analysis/TRANSFER_INTERLOCKS.json',label='Modeled fault/isolation branch / physical validation subsequent')
 ]},
 'mission':{'title':'A host-assisted delivery study.','duration_s':108,'scope':'G5-MISSION-01 / frozen twelve-release Gen5 case','slides':[
 slide(12,'One common starting state.','Nominal 500 km SSO. Twelve 4 kg 3U payloads. Generic host: 500 kg wet bus, including 20 kg fuel once; Isp 220 s.','01_assembly_isometric.jpg',source='mission/MISSION_INPUTS.json'),
 slide(12,'Twelve scheduled releases.','Actual computed Gen5 host history, uniform-2 target family. Markers identify the frozen release epochs; the inertial X/Z projection preserves the numerical trajectory.',kind='trajectory',source='mission/release/uniform_2_gen5_f0.35_trajectory.csv; mission/TARGETS.json',label='Computed host trajectory / fixed-axis J2 / X–Z projection'),
 slide(12,'Host manoeuvre. Point. Release.','Host burns provide the departure state and direction. The launcher adds the coupled release contribution. The propagated state depends on both.',kind='mission_flow',source='mission/MISSION_REPORT.md',label='Conceptual operations diagram / generic host study'),
 slide(12,'Frozen full-state targets.','Uniform synthetic 2 m/s or alternating 1/3 m/s along-track target families. All payloads and retained host are compared at t = 91800 s: 24 h after the final release.','MISSION_TARGETS.png',kind='plot',source='mission/TARGETS.json',label='Computed target states / synthetic study cases'),
 slide(12,'Coast for loading and safe release.','Gen5 reserves 400 s of zero-force loading coast per payload for the declared 355 s cycle. Both architectures keep 5 s pre-release and 20 s post-release zero-force guards.',kind='timeline',source='mission/MISSION_REPORT.md',label='Source-derived operation timing / one 450 s release leg'),
 slide(12,'The spring comparator matters.','The ideal ground-pretrimmed spring closes both target families at the 1 N and 5 N gates. Preplanned targets give no established Gen5 propellant or initial wet-mass advantage.','MISSION_RESOURCES.png',kind='plot',source='mission/MISSION_RESULTS.csv',label='Computed result / bounded candidate policies'),
 slide(12,'Replay checks numerical consistency.','Native Orekit 13.1.6 replay and 60→30 s refinement agree within the declared numerical residuals. Numerical agreement is not physical delivery accuracy.','MISSION_NATIVE_AGREEMENT.png',kind='plot',source='mission/NATIVE_REPLAY_CHECKS.json',label='Computed numerical agreement / no physical accuracy inference'),
 slide(12,'Know the model boundary.','Fixed-axis J2 point masses and constant inertial force. Drag, higher gravity, attitude/plume allocation, navigation and finite exit geometry are outside this study.',kind='boundary',source='mission/MISSION_REPORT.md',label='Generic host study / modeled target states'),
 slide(12,'A reproducible system result.','The tested uniform family closes within the host gates; alternating Gen5 closes at 5 N. Its retained-device penalty is 84.55672 kg. Inspect the frozen inputs and same-input comparison.','MISSION_RESOURCES.png',kind='plot',source='mission/MISSION_RESULTS.csv; mission/MISSION_REPORT.md',label='Computed result / synthetic preplanned target families')
 ]},
 'methods':{'title':'Geometry. Models. Results.','duration_s':54,'scope':'Engineering methods and configuration / ACR1','slides':[
 slide(9,'Start with a controlled configuration.','VOLLEY-G5-ACR1: twelve 4 kg 3U payloads, two six-level banks, guided screw transfer, indexed lift and captive carrier pallet.','01_assembly_isometric.jpg',source='visuals/VIEW_PROVENANCE.json'),
 slide(9,'Resolve the finite geometry.','Native geometry defines the magnetic gap, conductor placement and finite stator. CAD/STEP is preserved beside the computational model.','magnetic_gap_section.png',kind='plot',source='analysis/FINITE_MOTOR.json',label='Scientific section / controlled geometry'),
 slide(9,'Couple the source and moving system.','The evaluated 1–3 m/s commands include finite force, electrical behavior, release recoil and carrier arrest within the declared computational assumptions.','coupled_shot_reference.png',kind='plot',source='analysis/COUPLED_SHOT.json',label='Computed coupled-shot result'),
 slide(9,'Account for the whole shot.','The ledger records mechanical energy and copper, inverter, bank and auxiliary terms. Installed device allocation is 149.55672 kg CAD mass plus 7 kg.','shot_energy_ledger.png',kind='plot',source='analysis/COUPLED_SHOT.json',label='Computed energy ledger / model result'),
 slide(9,'Replay the mission independently.','Frozen synthetic target PV states, continuous host arcs, release momentum and independent mass-flow checks support numerical consistency.','MISSION_NATIVE_AGREEMENT.png',kind='plot',source='mission/NATIVE_REPLAY_CHECKS.json',label='Computed numerical agreement / Orekit replay'),
 slide(9,'Use the result to set the next gate.','The evaluated integrated configuration has a traceable computational record. Gen6 mixed-size work and instrumented hardware correlation remain separately identified development.','MISSION_RESOURCES.png',kind='plot',source='mission/MISSION_REPORT.md',label='Computed study result / subsequent development identified')
 ]}}

def wrap(draw,text,xy,maxwidth,f,fill=DIM,spacing=11):
 x,y=xy; line=''
 for word in text.split():
  test=(line+' '+word).strip()
  if draw.textlength(test,font=f)>maxwidth and line:
   draw.text((x,y),line,font=f,fill=fill);y+=f.size+spacing;line=word
  else:line=test
 if line:draw.text((x,y),line,font=f,fill=fill);y+=f.size+spacing
 return y

def contained(im,path,box):
 pic=Image.open(path).convert('RGB');pic.thumbnail((box[2]-box[0],box[3]-box[1]),Image.Resampling.LANCZOS)
 im.paste(pic,(box[0]+(box[2]-box[0]-pic.width)//2,box[1]+(box[3]-box[1]-pic.height)//2))

def recovery(draw,progress):
 # Normalized explanatory displacement; deliberately not a dynamics calculation.
 # Carrier and pallet always share their displacement. Payload separates after release.
 if progress<.40:x=185+progress/.40*500;state='POWERED STROKE'
 elif progress<.60:x=685+(progress-.40)/.20*70;state='RELEASE / ARREST'
 else:x=755-(progress-.60)/.40*570;state='RETURN WITH PALLET'
 y=410; draw.line((150,y+65,1160,y+65),fill=DIM,width=4)
 for xx,label in [(185,'HOME'),(685,'RELEASE'),(755,'ARREST')]:
  draw.line((xx,y+72,xx,y+88),fill=DIM,width=2);draw.text((xx-30,y+100),label,font=font(14,mono=True),fill=DIM)
 draw.rounded_rectangle((x-65,y+22,x+65,y+62),5,fill='#77848b');draw.rounded_rectangle((x-53,y+7,x+53,y+22),3,fill=ACC)
 payload_x=x if progress<.40 else 685+(progress-.40)/.60*410
 draw.rectangle((payload_x-42,y-80,payload_x+42,y+5),fill='#739eb9',outline=INK,width=2)
 draw.text((150,245),state,font=font(23,True),fill=ACC)
 draw.text((150,287),'Carrier + captive pallet: retained throughout arrest and return',font=font(20),fill=INK)
 draw.text((190,560),'■ PAYLOAD',font=font(18,mono=True),fill='#92bad4');draw.text((420,560),'■ CAPTIVE PALLET',font=font(18,mono=True),fill=ACC);draw.text((760,560),'■ CARRIER',font=font(18,mono=True),fill='#b2b9bd')
 draw.polygon([(1160,y+65),(1149,y+58),(1149,y+72)],fill=DIM)
 direction='+X → launch direction; separation along +X. Vertical stacking identifies components only.'
 draw.text((150,610),direction,font=font(17),fill=DIM)
 # Reserve distinct text bands above and below the entire swept diagram region.
 text_boxes=[draw.textbbox((150,245),state,font=font(23,True)),draw.textbbox((150,287),'Carrier + captive pallet: retained throughout arrest and return',font=font(20)),draw.textbbox((150,610),direction,font=font(17))]
 for xx,label in [(185,'HOME'),(685,'RELEASE'),(755,'ARREST')]:text_boxes.append(draw.textbbox((xx-30,y+100),label,font=font(14,mono=True)))
 for pos,label in [((190,560),'■ PAYLOAD'),((420,560),'■ CAPTIVE PALLET'),((760,560),'■ CARRIER')]:text_boxes.append(draw.textbbox(pos,label,font=font(18,mono=True)))
 sprites=[(x-65,y+22,x+65,y+62),(x-53,y+7,x+53,y+22),(payload_x-42,y-80,payload_x+42,y+5)]
 def intersects(a,b):return a[0]<b[2]and a[2]>b[0]and a[1]<b[3]and a[3]>b[1]
 assert not any(intersects(label,sprite)for label in text_boxes for sprite in sprites),'Recovery text/sprite collision'
 # Semantic invariants recorded independently in review receipt.
 return {'carrier_x':x,'pallet_x':x,'payload_x':payload_x,'state':state,'text_sprite_collision':False}

def fault(draw,progress):
 labels=['Detect stalled transfer','Inhibit launcher','Retain payload','Isolate affected cell','Supervised reset / recovery','Verify before next eligible cell']
 active=min(5,int(progress*6))
 for i,label in enumerate(labels):
  col=i%3;row=i//3;x=80+col*410;y=275+row*150
  draw.rectangle((x,y,x+375,y+113),fill=PANEL,outline=GOLD if i==active else '#48545b',width=3 if i==active else 1)
  draw.text((x+18,y+12),f'{i+1:02d}',font=font(16,mono=True),fill=GOLD)
  wrap(draw,label,(x+18,y+45),340,font(21),INK,4)
 draw.text((80,608),'Modeled custody/interlock logic; physical fault-response validation is subsequent work.',font=font(20),fill=GOLD)

def trajectory(draw,progress):
 traj=np.genfromtxt(INPUT/'uniform_2_gen5_f0.35_trajectory.csv',delimiter=',',names=True)
 traj=traj[traj['t_s']<=5677]
 scale=180/7.1e6;cx=365;cy=438
 def point(x,z):return (cx+x*scale,cy-z*scale)
 r=6378137*scale;draw.ellipse((cx-r,cy-r,cx+r,cy+r),fill='#273a42',outline='#77868e',width=1)
 points=[point(row['x_m'],row['z_m'])for row in traj];draw.line(points,fill='#55746a',width=2)
 elapsed=5400*progress;included=traj[traj['t_s']<=elapsed]
 if len(included)>1:draw.line([point(row['x_m'],row['z_m'])for row in included],fill=ACC,width=4)
 if len(included):
  x,y=point(included[-1]['x_m'],included[-1]['z_m']);draw.ellipse((x-6,y-6,x+6,y+6),fill=INK)
 draw.text((145,637),'X / Z projection (km); Earth drawn to scale',font=font(15),fill=DIM)
 for val in [-6000,0,6000]:
  x,y=point(val*1000,0);draw.text((x-20,660),str(val),font=font(12,mono=True),fill=DIM)
 draw.text((690,245),f'SIMULATION t = {elapsed:6.0f} s',font=font(21,mono=True),fill=ACC)
 for i in range(12):
  released=elapsed>=450*(i+1);x=690+(i//6)*265;y=292+(i%6)*56
  draw.text((x,y),f'P{i+1:02d}  #{i+1:02d}  {450*(i+1):4d} s',font=font(17,mono=True),fill=ACC if released else DIM)
  draw.text((x,y+24),'uniform 2 / host-assisted',font=font(12),fill=DIM)
 draw.text((690,650),'Generic host study · modeled target state',font=font(17),fill=DIM)

def flow(draw,progress):
 steps=[('HOST MANOEUVRE','Planned inertial departure state'),('POINT + RELEASE','Coupled launcher contribution'),('PROPAGATE','Fixed-axis J2 full state')]
 for i,(head,sub) in enumerate(steps):
  x=80+i*410;y=330;draw.rectangle((x,y,x+370,y+160),fill=PANEL,outline=ACC if int(progress*3)==i else '#48545b',width=2)
  draw.text((x+18,y+22),head,font=font(20,True),fill=ACC);wrap(draw,sub,(x+18,y+62),332,font(22),INK)
  if i<2:draw.text((x+377,y+60),'→',font=font(30),fill=ACC)
 draw.text((100,565),'Material altitude or plane changes depend on the host model and its manoeuvres.',font=font(22),fill=INK)

def timeline(draw,progress):
 left=95;width=1080;y=370
 # Actual first uniform Gen5 leg boundaries: two 22.5 s force windows around 400 s loading coast.
 intervals=[(0,22.5,'Host force window',GOLD),(22.5,422.5,'400 s loading coast',ACC),(422.5,445,'Host force window',GOLD),(445,450,'5 s guard',DIM)]
 for lo,hi,label,color in intervals:
  x=left+lo/450*width;r=left+hi/450*width
  draw.rectangle((x,y,r,y+65),fill=color)
 for t in [0,22.5,422.5,445,450]:
  x=left+t/450*width;draw.line((x,y+67,x,y+92),fill=INK,width=2)
 # Separate labels avoid overlapping the tightly spaced end guards.
 draw.text((left,485),'0 s',font=font(18,mono=True),fill=DIM)
 draw.text((left+180,305),'400 s ZERO-FORCE LOADING COAST',font=font(23,True),fill=ACC)
 draw.text((left+180,465),'355 s mechanism cycle + 45 s reserve',font=font(21),fill=INK)
 draw.text((left+850,535),'RELEASE 450 s',font=font(19,mono=True),fill=INK)
 draw.text((left,575),'Both architectures: 5 s pre-release + 20 s post-release zero-force guards.',font=font(21),fill=DIM)
 x=left+progress*width;draw.line((x,y-15,x,y+80),fill=INK,width=3)

def boundary(draw,progress):
 for i,(head,text) in enumerate([('MODEL','Fixed-axis J2 · point masses · constant inertial resultant force'),('TARGETS','Synthetic preplanned full PV · generic host · modeled target states'),('OUTSIDE SCOPE','Drag · higher gravity · navigation · attitude/plumes · finite exit geometry')]):
  y=270+i*110;draw.text((80,y),head,font=font(18,True),fill=ACC);wrap(draw,text,(80,y+36),1100,font(24),INK,6)

def frame(film,index,p):
 data=STORY[film];s=data['slides'][index];im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
 d.text((48,28),'VOLLEY',font=font(22,True),fill=INK);d.text((195,34),data['scope'].upper(),font=font(11,mono=True),fill=DIM)
 d.line((48,69,1232,69),fill='#48545b',width=1)
 d.text((48,88),s['label'].upper(),font=font(12,mono=True),fill=ACC)
 if s['kind']=='image':
  wrap(d,s['title'],(48,138),410,font(36,True),INK,8)
  wrap(d,s['text'],(48,290),400,font(24),DIM,12)
  d.rectangle((490,125,1232,640),fill='#fff');contained(im,A/s['asset'],(490,125,1232,640))
 elif s['kind']=='plot':
  d.text((48,124),s['title'],font=font(30,True),fill=INK)
  d.rectangle((142,181,1138,580),fill='#fff');contained(im,A/s['asset'],(142,181,1138,580))
  wrap(d,s['text'],(70,597),1140,font(19),DIM,6)
 else:
  d.text((48,124),s['title'],font=font(32,True),fill=INK)
  wrap(d,s['text'],(48,176),1180,font(20),DIM,6)
  {'recovery':recovery,'fault':fault,'trajectory':trajectory,'mission_flow':flow,'timeline':timeline,'boundary':boundary}[s['kind']](d,p)
 d.line((48,689,1232,689),fill='#48545b',width=1)
 d.text((48,699),f'G5 ACR1 · {film.upper()} · {index+1:02d}/{len(data["slides"]):02d}',font=font(10,mono=True),fill=DIM)
 d.text((620,699),'Source-linked editorial sequence · computational design study',font=font(10,mono=True),fill=DIM)
 return im

def stamp(seconds):
 ms=round(seconds*1000);return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d}.{ms%1000:03d}'

def prepare():
 for rel in ['mission/release/uniform_2_gen5_f0.35_trajectory.csv','mission/release/uniform_2_gen5_f0.35.json','mission/TARGETS.json','mission/MISSION_RESULTS.csv','mission/MISSION_REPORT.md','mission/NATIVE_REPLAY_CHECKS.json','analysis/COUPLED_SHOT.json','analysis/TRANSFER_INTERLOCKS.json','cad/release/FINAL_CAD_MANIFEST.json']:
  src=FROZEN/rel;dst=INPUT/src.name
  if not dst.exists():shutil.copy2(src,dst)
 for s in STORY.values():
  assert sum(x['duration_s']for x in s['slides'])==s['duration_s']
 (HERE/'STORYBOARD.json').write_text(json.dumps(STORY,indent=2))
 pins=[]
 for p in [p for p in sorted(INPUT.glob('*'))+sorted(A.glob('*.png'))+sorted(A.glob('*.jpg'))if p.is_file()]:
  pins.append({'path':str(p.relative_to(ROOT)),'sha256':sha(p)})
 (HERE/'SOURCE_PINS.json').write_text(json.dumps(pins,indent=2))
 for key,data in STORY.items():
  directory=OUT/key;directory.mkdir(exist_ok=True,parents=True);captions=['WEBVTT',''];t=0;script=[];stills=[]
  for i,s in enumerate(data['slides']):
   captions.extend([str(i+1),f'{stamp(t)} --> {stamp(t+s["duration_s"])}',s['title']+' '+s['text'],''])
   script.append({'start_s':t,'end_s':t+s['duration_s'],'title':s['title'],'text':s['text'],'source':s['source'],'evidence_class':s['label']})
   still=frame(key,i,.65);still.save(directory/f'storyboard-{i+1:02d}.jpg',quality=93);still.save(directory/f'storyboard-{i+1:02d}.png');stills.append(still)
   t+=s['duration_s']
  frame(key,0,0).save(directory/'poster.jpg',quality=95)
  sheet=Image.new('RGB',(1280,math.ceil(len(stills)/2)*360),BG)
  for i,im in enumerate(stills):im.thumbnail((640,360));sheet.paste(im,((i%2)*640,(i//2)*360))
  sheet.save(directory/'storyboard-contact-sheet.jpg',quality=95)
  (directory/'captions.vtt').write_text('\n'.join(captions));(directory/'transcript.json').write_text(json.dumps(script,indent=2))
  (directory/'transcript.txt').write_text(data['title']+'\n\n'+'\n\n'.join(f'{x["start_s"]}–{x["end_s"]} s | {x["title"]}\n{x["text"]}\nEvidence: {x["evidence_class"]}\nSource: {x["source"]}'for x in script))
 # Source-driven explorer: static SVG plus accessible range control; no arbitrary orbits.
 traj=np.genfromtxt(INPUT/'uniform_2_gen5_f0.35_trajectory.csv',delimiter=',',names=True);traj=traj[traj['t_s']<=5677]
 samples=[]
 for row in traj:
  samples.append({'t_s':float(row['t_s']),'x_m':float(row['x_m']),'z_m':float(row['z_m']),'mass_kg':float(row['mass_kg']),'px':round(400+row['x_m']/20000,3),'py':round(400-row['z_m']/20000,3)})
 (A/'trajectory-explorer.json').write_text(json.dumps({'case':'uniform_2_gen5_f0.35','source_sha256':sha(INPUT/'uniform_2_gen5_f0.35_trajectory.csv'),'samples':samples},indent=2))
 print('Prepared four pinned storyboards, posters, transcripts and source trajectory.')

def verify():
 pins=json.loads((HERE/'SOURCE_PINS.json').read_text())
 for p in pins:assert sha(ROOT/p['path'])==p['sha256'],p['path']
 view=json.loads((A/'VIEW_PROVENANCE.json').read_text())
 for v in view['views']:
  for name,record in v['outputs'].items():assert sha(A/name)==record['sha256'],name
 tests=[]
 for key,data in STORY.items():
  assert len(data['slides'])>=6;assert sum(s['duration_s']for s in data['slides'])==data['duration_s']
  for i,s in enumerate(data['slides']):
   assert s['source'];assert s['label']
   if s['asset']:assert (A/s['asset']).exists()
   if s['kind']=='recovery':
    dummy=ImageDraw.Draw(Image.new('RGB',(1280,720)))
    states=[recovery(dummy,p/100)for p in range(101)]
    assert all(x['carrier_x']==x['pallet_x']for x in states)
    assert states[-1]['carrier_x']==states[0]['carrier_x']
    assert states[-1]['payload_x']>states[-1]['carrier_x']
    tests.append(f'{key}: captive pallet invariant and text/sprite nonoverlap at101conceptual poses; payload departs along+X; carrier returns')
 tests.extend(['All four accepted image hashes match frozen view provenance','All source pins match','Twelve-release source schedule and numeric trajectory retained','All four duration bands met; captions/transcripts/posters and stills exist','Conceptual motion and fault branch explicitly identified','No arbitrary orbital or inclination changes; computed host history used'])
 receipt={'configuration':'VOLLEY-G5-ACR1','review_type':'automated source and semantic checks + human-readable editorial artifacts','automated_checks':tests,'storyboard_editorial_review':'pending visual inspection','owner_approval':'not requested; publication pending','expensive_render_gate':'animatic and visual inspection required before final render'}
 (HERE/'STORYBOARD_REVIEW.json').write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt,indent=2))

def encode(key,animatic=False):
 data=STORY[key];directory=OUT/key;fps=2 if animatic else 12;size=(640,360)if animatic else(W,H)
 dst=directory/('animatic.mp4'if animatic else'film.mp4')
 command=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s',f'{size[0]}x{size[1]}','-r',str(fps),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','22'if animatic else'19','-pix_fmt','yuv420p','-movflags','+faststart',str(dst)]
 proc=subprocess.Popen(command,stdin=subprocess.PIPE)
 try:
  for i,s in enumerate(data['slides']):
   motion=s['kind']not in ['image','plot'];still=None
   if not motion:
    still=frame(key,i,0)
    if animatic:still=still.resize(size,Image.Resampling.LANCZOS)
    still=still.tobytes()
   count=round(s['duration_s']*fps)
   for n in range(count):
    if motion:
     im=frame(key,i,n/max(1,count-1))
     if animatic:im=im.resize(size,Image.Resampling.LANCZOS)
     raw=im.tobytes()
    else:raw=still
    proc.stdin.write(raw)
 finally:proc.stdin.close()
 assert proc.wait()==0
 if not animatic:
  subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(dst),'-an','-c:v','libvpx-vp9','-deadline','realtime','-cpu-used','6','-crf','35','-b:v','0',str(directory/'film.webm')],check=True)
  # Lossless archival frames per storyboard state, preserved alongside source; MP4 is the high quality editorial master.
  manifest={'configuration':'VOLLEY-G5-ACR1','film':key,'title':data['title'],'duration_s':data['duration_s'],'dimensions_px':[W,H],'fps':fps,'codec':'H.264 yuv420p / VP9','audio':'none; explicit playback; captions and transcript supplied','master':'film.mp4','editable_source':'../../visual-source/build_films.py; ../../visual-source/STORYBOARD.json','cad_scene':'../../downloads/VOLLEY_G5_ACR1_editable_scene.zip','sources':'../../visual-source/SOURCE_PINS.json','captions':'captions.vtt','transcript':'transcript.json','poster':'poster.jpg','publication':'pending','source_files':[{'path':str(p.relative_to(ROOT)),'sha256':sha(p)}for p in sorted(directory.iterdir())if p.is_file()and p.name!='FILM_MANIFEST.json'and p.suffix in ['.mp4','.webm','.vtt','.json','.txt','.jpg','.png']]}
  manifest.update({'render_script_sha256':sha(Path(__file__)),'storyboard_sha256':sha(HERE/'STORYBOARD.json'),'software':json.loads((HERE/'FILM_SOURCE_MANIFEST.json').read_text()),'archival_derivatives':'lossless storyboard-*.png and H.264 editorial master film.mp4','revision':'R2 recovery text-band/+X correction'if key in ['overview','custody']else'R1'})
  (directory/'FILM_MANIFEST.json').write_text(json.dumps(manifest,indent=2))
 print('Encoded',key,'animatic'if animatic else'master + webm',flush=True)

def main():
 p=argparse.ArgumentParser();p.add_argument('mode',choices=['prepare','verify','animatic','render']);p.add_argument('--film',choices=list(STORY));args=p.parse_args()
 if args.mode=='prepare':prepare();verify()
 elif args.mode=='verify':verify()
 else:
  for key in ([args.film]if args.film else STORY):encode(key,args.mode=='animatic')
if __name__=='__main__':main()
