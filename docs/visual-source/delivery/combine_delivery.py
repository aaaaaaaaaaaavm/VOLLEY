"""Assemble verified mechanism, principle-comparison and orbital chapters."""
from pathlib import Path
import json,subprocess,re,hashlib
R=Path(__file__).resolve().parent
parts=[(R/'mechanism/mechanism.mp4',70),(R/'comparison/comparison.mp4',20),(R/'orbit/VOLLEY_orbit_comparison_100s.mp4',100)]
for p,dur in parts:assert p.is_file(),p
def probe(p):
 d=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)],text=True));v=next(s for s in d['streams']if s['codec_type']=='video');return d,v
media=[]
for p,dur in parts:
 d,v=probe(p);assert v['width']==1280 and v['height']==720 and v['avg_frame_rate']=='24/1';assert int(v['nb_frames'])==dur*24
 media.append({'path':str(p.relative_to(R)),'duration_s':dur,'frames':int(v['nb_frames']),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
# Relative file names avoid shell evaluation and preserve a portable concat list.
(R/'concat.txt').write_text('\n'.join("file '"+str(p.relative_to(R))+"'"for p,d in parts)+'\n')
subprocess.run(['ffmpeg','-y','-v','error','-f','concat','-safe','1','-i',str(R/'concat.txt'),'-c','copy','-movflags','+faststart',str(R/'VOLLEY_from_cassette_to_orbit.mp4')],check=True)
def seconds(t):
 h,m,s=t.split(':');return int(h)*3600+int(m)*60+float(s)
def stamp(t):return f'{int(t//3600):02d}:{int(t%3600//60):02d}:{t%60:06.3f}'
subs=[]
for p,offset in [(R/'mechanism/captions.vtt',0),(R/'comparison/captions.vtt',70),(R/'orbit/ENGLISH.vtt',90)]:
 text=p.read_text();blocks=re.split(r'\n\s*\n',text.strip())
 for block in blocks:
  lines=block.splitlines();i=next((i for i,x in enumerate(lines)if'-->'in x),None)
  if i is None:continue
  a,b=lines[i].split('-->');a=seconds(a.strip());b=seconds(b.strip());subs.append((a+offset,b+offset,'\n'.join(lines[i+1:])))
assert subs[0][0]==0 and abs(subs[-1][1]-190)<.01
assert all(0<=a<b<=190 for a,b,t in subs)
(R/'captions.vtt').write_text('WEBVTT\n\n'+'\n\n'.join(f'{stamp(a)} --> {stamp(b)}\n{t}'for a,b,t in subs)+'\n')
(R/'TRANSCRIPT.md').write_text('# VOLLEY: from cassette to orbit\n\nFull film:3min10s. 1280×720,24fps; English on-screen explanation and optional closed captions; no audio.\n\n'+ '\n\n'.join(f'## {stamp(a)}–{stamp(b)}\n\n{t}'for a,b,t in subs)+'\n')
full=R/'VOLLEY_from_cassette_to_orbit.mp4';d,v=probe(full);assert int(v['nb_frames'])==4560 and abs(float(d['format']['duration'])-190)<.01
decode=subprocess.run(['ffmpeg','-v','error','-i',str(full),'-f','null','-'],capture_output=True,text=True);assert decode.returncode==0 and not decode.stderr,decode.stderr
report={'film':'VOLLEY from cassette to orbit','duration_s':190,'width':v['width'],'height':v['height'],'fps':v['avg_frame_rate'],'frames':int(v['nb_frames']),'audio':False,'full_decode_pass':True,'caption_cues':len(subs),'caption_end_s':subs[-1][1],'chapters':media,'source_scope':'CAD-derived edited mechanism motion; original principle schematics; invariant-checked planar two-body orbital illustrations','current_command_points_m_s':[1,2,3],'historical_periodic_model_example_m_s':16.029,'future_kinematic_examples_m_s':[1000,3500],'claims':'Future and historical speeds are not current ACR1 ratings; same-host preset-spring comparator preserved','sha256':hashlib.sha256(full.read_bytes()).hexdigest(),'bytes':full.stat().st_size}
(R/'FINAL_DELIVERY_CHECKS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
