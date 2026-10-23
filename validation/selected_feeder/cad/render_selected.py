"""Render identified native FM08-R3 meshes in Blender Workbench.

Run blender -b --factory-startup -P render_selected.py -- <CAD-package-root>
No mechanical geometry is introduced by the renderer. Output images depict
prescribed nominal states and do not establish dynamic or hardware performance.
"""
from pathlib import Path
import bpy,sys,json,hashlib,math
from mathutils import Vector
H=Path(sys.argv[sys.argv.index('--')+1]).resolve()
manifest=H/'release/GEOMETRY_REPORT.json'
D=json.loads(manifest.read_text());O=H/'figures';O.mkdir(exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.context.preferences.filepaths.save_version=0
s=bpy.context.scene;s.render.engine='BLENDER_WORKBENCH';s.render.threads_mode='FIXED';s.render.threads=2
s.render.resolution_x=1800;s.render.resolution_y=1100;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG'
s.display.shading.light='STUDIO';s.display.shading.studiolight_rotate_z=.4;s.display.shading.color_type='MATERIAL'
s.display.shading.show_shadows=True;s.display.shading.show_cavity=True;s.display.shading.cavity_type='BOTH'
s.display.shading.show_object_outline=True;s.display.shading.object_outline_color=(.12,.15,.18)
s.display.shading.background_type='WORLD';s.world=bpy.data.worlds.new('Technical white');s.world.color=(1,1,1)
s.view_settings.view_transform='Standard';s.view_settings.exposure=0
mats={}
for n,c in [('frame',(.64,.68,.71,1)),('payload',(.10,.30,.43,1)),('restraint',(.78,.40,.12,1)),('steel',(.28,.32,.35,1)),('envelope',(.33,.45,.47,1))]:
 m=bpy.data.materials.new(n);m.diffuse_color=c;mats[n]=m
bpy.ops.object.camera_add(location=(1.9,-2.5,2.1));cam=bpy.context.object;target=Vector((.65,.05,.08))
cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=2.25;cam.data.clip_end=100;s.camera=cam
records=[]
poses=[]
for cap in D['captures']:
 phase=Path(cap['native']).stem.replace('FM08_R3_four_cell_','')
 if phase=='1U_seated' or ('--stowed-only' in sys.argv and phase!='stowed'):continue
 poses.append({'phase':phase,'source':cap['native'],'sha256':hashlib.sha256((H/'release'/cap['native']).read_bytes()).hexdigest(),'objfile':Path(cap['native']).stem+'.obj'})
for record in poses:
 objs=[]
 objpath=H/'release/obj'/record['objfile']
 vertices=[];groups=[];name=None;faces=[]
 for line in objpath.read_text().splitlines():
  a=line.split()
  if not a:continue
  if a[0]=='o':
   if name is not None:groups.append((name,faces))
   name=' '.join(a[1:]);faces=[]
  elif a[0]=='v':vertices.append(tuple(float(v)*.001 for v in a[1:4]))
  elif a[0]=='f':faces.append(tuple(int(v.split('/')[0])-1 for v in a[1:]))
 if name is not None:groups.append((name,faces))
 for name,globalfaces in groups:
  used=sorted(set(i for face in globalfaces for i in face));remap={old:i for i,old in enumerate(used)}
  verts=[vertices[i] for i in used];faces=[tuple(remap[i] for i in face) for face in globalfaces]
  mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update()
  ob=bpy.data.objects.new(name,mesh);s.collection.objects.link(ob);objs.append(ob)
  n=name.lower();mat='payload' if 'payload' in n else 'restraint' if any(t in n for t in ['gate','barrier','retainer','latch','clutch']) else 'steel' if any(t in n for t in ['screw','shaft','pin','rack','bearing']) else 'envelope' if any(t in n for t in ['motor','controller','brake']) else 'frame'
  ob.data.materials.append(mats[mat])
 phase=record.get('phase',record.get('state','state'))
 cam.location=Vector((1.9,-2.5,2.1));cam.rotation_euler=(Vector((.65,.05,.08))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=2.25
 s.render.filepath=str(O/('FM08_'+phase+'.png'));bpy.ops.render.render(write_still=True)
 if phase in ['stowed','stored']:
  bpy.ops.wm.save_as_mainfile(filepath=str(O/'FM08_technical_scene.blend'))
 records.append({'phase':phase,'source':record.get('source'),'source_sha256':record.get('sha256'),'image':Path(s.render.filepath).name,'sha256':hashlib.sha256(Path(s.render.filepath).read_bytes()).hexdigest()})
 cam.location=Vector((1.2,-1.3,2.4));cam.rotation_euler=(Vector((.42,.1,.08))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=1.1
 s.render.filepath=str(O/('FM08_detail_'+phase+'.png'));bpy.ops.render.render(write_still=True)
 records.append({'phase':phase,'view':'Detail crop; neighbouring structures may be truncated','source':record.get('source'),'source_sha256':record.get('sha256'),'image':Path(s.render.filepath).name,'sha256':hashlib.sha256(Path(s.render.filepath).read_bytes()).hexdigest()})
 for ob in objs:bpy.data.objects.remove(ob,do_unlink=True)
(O/'BLENDER_PROVENANCE.json').write_text(json.dumps({'revision':'FM08-R3','software':'Blender '+bpy.app.version_string,'engine':'Workbench','mesh_manifest_sha256':hashlib.sha256(manifest.read_bytes()).hexdigest(),'render_source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'evidence_class':'Technical renders of actual native CAD; nominal prescribed states. No geometry invented, hardware photograph, GUI capture or dynamics rating.','renders':records},indent=2)+'\n')
