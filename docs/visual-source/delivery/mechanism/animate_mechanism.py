"""Build/render a CAD-derived VOLLEY operating-sequence animation in Blender.

blender -b -t 4 -P animate_mechanism.py -- --source SOURCE.blend --out OUT --build
blender -b OUT/VOLLEY_ACR1_operating_cycle.blend -t 4 -s 1 -e 1680 -a

Motion is a rigid-part editorial illustration of the source operating sequence.
Display times are edited; this script does not calculate contact dynamics.
"""
import argparse,sys,math,json,hashlib,time
from pathlib import Path
import bpy
from mathutils import Vector,Matrix

ap=argparse.ArgumentParser();ap.add_argument('--source',required=True);ap.add_argument('--out',required=True);ap.add_argument('--build',action='store_true');ap.add_argument('--preview',action='store_true')
args=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);out=Path(args.out).resolve();out.mkdir(parents=True,exist_ok=True)
source=Path(args.source).resolve();bpy.ops.wm.open_mainfile(filepath=str(source))
src=bpy.data.scenes['03_captured_source_level'];scene=bpy.data.scenes.new('ACR1_OPERATING_CYCLE');bpy.context.window.scene=scene
scene.render.engine='BLENDER_WORKBENCH';scene.render.resolution_x=1280;scene.render.resolution_y=720;scene.render.resolution_percentage=100
scene.render.fps=24;scene.frame_start=1;scene.frame_end=1680
scene.render.image_settings.file_format='JPEG';scene.render.image_settings.color_mode='RGB';scene.render.image_settings.quality=94
scene.render.filepath=str(out/'frames')+'/';(out/'frames').mkdir(exist_ok=True)
scene.world=bpy.data.worlds.new('Studio');scene.world.color=(.0056,.008,.0116)
s=scene.display.shading;s.light='STUDIO';s.color_type='OBJECT';s.background_type='VIEWPORT';s.background_color=(.0056,.0080,.0116);s.show_shadows=False;s.show_cavity=True;s.cavity_type='WORLD';s.curvature_ridge_factor=1.15;s.curvature_valley_factor=1.0;s.show_object_outline=True;s.object_outline_color=(.10,.14,.16);s.show_specular_highlight=True
scene.display.render_aa='FXAA';scene.view_settings.view_transform='Standard';scene.view_settings.look='None'
colors={'aluminium':(.59,.62,.63,1),'steel':(.26,.30,.32,1),'copper':(.43,.43,.40,1),'ndfeb':(.14,.17,.19,1),'payload':(.70,.73,.72,1),'polymer':(.25,.28,.28,1),'catalog':(.32,.36,.37,1),'insulator':(.57,.59,.55,1)}
accent=(.05,.62,.59,1)
objects={};identities=[]
for ob in list(src.objects):
 if 'cad_name' not in ob:continue
 copy=ob.copy();copy.animation_data_clear();copy.name='MOVIE_'+ob['cad_name'];scene.collection.objects.link(copy);copy.hide_render=False
 copy.color=colors[ob['cad_material']];objects[ob['cad_name']]=copy
 if ob['cad_name']=='Transferred_3U' or ob['cad_name']=='Captive_payload_pallet' or ob['cad_name'].startswith('Bank_south_L5_')and ob['cad_subsystem'] in ['cell_pusher','cell_drive']:copy.color=accent
 h=hashlib.sha256()
 for v in ob.data.vertices:h.update((','.join(float(x).hex() for x in v.co)+';').encode())
 for face in ob.data.polygons:h.update((','.join(str(i) for i in face.vertices)+';').encode())
 identities.append({'cad_name':ob['cad_name'],'source_mesh_sha256':h.hexdigest(),'subsystem':ob['cad_subsystem'],'source_state':'03_captured_source_level'})
assert len(objects)==387
for old in list(bpy.data.scenes):
 if old!=scene:bpy.data.scenes.remove(old)
bpy.ops.outliner.orphans_purge(do_recursive=True)
camera_data=bpy.data.cameras.new('Editorial_camera');camera_data.type='ORTHO';camera_data.clip_start=.01;camera_data.clip_end=100
camera=bpy.data.objects.new('Editorial_camera',camera_data);scene.collection.objects.link(camera);scene.camera=camera

def ramp(t,a,b):return min(1.,max(0.,(t-a)/(b-a)))
def ease(t,a,b):
 x=ramp(t,a,b);return x*x*(3-2*x)
def translate(x=0,y=0,z=0):return Matrix.Translation((x,y,z))
def rot_z(theta,x,y):return translate(x,y,0)@Matrix.Rotation(theta,4,'Z')@translate(-x,-y,0)

def state(t):
 # Retrieve the empty pallet, index to the cell, receive, lower, dock and launch.
 floor=.190-.144*ease(t,4,7)+.784*ease(t,10,16)-.784*ease(t,30,38)+.144*ease(t,44,46)
 feed=ease(t,18,25);retract=ease(t,27,30)
 # Open/close events are ordered to keep positive custody.
 grip=(1-ease(t,7,8))+ease(t,42,43)
 lock_rotation=1-ease(t,8,9)+ease(t,39,40)
 lock_height=1-ease(t,9,10)+ease(t,38,39)
 pallet_floor=.046+.784*ease(t,10,16)-.784*ease(t,30,38)
 incoming_keeper=1-ease(t,25,26)+ease(t,43,44)
 other_keeper=1-ease(t,14,15)+ease(t,43,44)
 storage_gate=ease(t,16,17)*(1-ease(t,26,27))
 cap_closed=ease(t,40,41);cap_pin=ease(t,41,42)
 if t<49:carrier=0.
 elif t<54:carrier=1.3*ramp(t,49,54)**2
 elif t<58:
  x=ramp(t,54,58);carrier=1.3+.21*(2*x-x*x)
 else:carrier=1.51*(1-ease(t,58,65))
 payload_x=carrier if t<=54 else 1.3+2.2*ramp(t,54,58)+2.2*ramp(t,58,70)
 payload_floor=.830-.784*ease(t,30,38)
 fore_open=min(1.,max(0.,(carrier-1.245)/.05)) if t<58 else 1-ramp(t,58,59)
 return dict(floor=floor,feed=feed,retract=retract,grip=grip,lock_rotation=lock_rotation,lock_height=lock_height,pallet_floor=pallet_floor,incoming_keeper=incoming_keeper,other_keeper=other_keeper,storage_gate=storage_gate,cap_closed=cap_closed,cap_pin=cap_pin,carrier=carrier,payload_x=payload_x,payload_floor=payload_floor,fore_open=fore_open)

def set_pose(t,keyframe=False):
 a=state(t);focus=4<=t<46
 for name,ob in objects.items():
  group=ob['cad_subsystem'];mat=Matrix.Identity(4)
  if group in ['cradle','cradle_catalog','cradle_grip','cradle_keeper']:mat=translate(z=a['floor']-.830)
  if group=='cradle_grip':mat=translate(y=-.026*a['grip'],z=a['floor']-.830)
  if group=='cradle_keeper':
   opened=a['incoming_keeper'] if name.endswith('_-1') else a['other_keeper']
   mat=translate(z=a['floor']-.830+.110*opened)
  if name.startswith('Bank_south_L5_'):
   if group=='cell_pusher':mat=translate(y=-.250+.250*a['feed']-.250*a['retract'])
   if group=='cell_gate':
    side=-1 if '_keeper_-1_' in name else 1
    mat=translate(x=-side*.04*(1-a['storage_gate']))
  if name=='Captive_payload_pallet':mat=translate(x=a['carrier'],z=a['pallet_floor']-.830)
  if name=='Transferred_3U':mat=translate(x=a['payload_x'],y=-.250*(1-a['feed']),z=a['payload_floor']-.830)
  if group.startswith('sled'):
   mat=translate(x=a['carrier'])
   if name.startswith('Pallet_bayonet_lock_'):
    x=.200+float(name.rsplit('_',1)[1])/1000
    mat=translate(x=a['carrier'],z=.012*a['lock_height'])@rot_z(math.pi/2*a['lock_rotation'],x,-.09)
   elif name.startswith('Sled_cap_')and group=='sled_gate':
    side=int(name.rsplit('_',1)[1]);mat=translate(x=a['carrier'],y=-side*.05*a['cap_closed'])
   elif group=='sled_latch_pin':mat=translate(x=a['carrier'],z=.026*a['cap_pin'])
   elif name.startswith('Sled_fore_keeper_'):
    side=int(name.rsplit('_',1)[1]);mat=translate(x=a['carrier'],y=side*.012*a['fore_open'])
   if name=='Captive_payload_pallet':mat=translate(x=a['carrier'],z=a['pallet_floor']-.830)
  ob.matrix_world=mat
  # A documented cutaway removes unselected banks and fixed support frame only in detail shots.
  hide=focus and ((name.startswith('Bank_')and not name.startswith('Bank_south_L5_'))or group in ['bank_mount']or name=='Host_mount_ladder')
  hide=hide or group=='sled_latch_spring'
  ob.hide_render=hide
  if keyframe:
   moving=group in ['cradle','cradle_catalog','cradle_grip','cradle_keeper']or group.startswith('sled')or name in ['Transferred_3U','Captive_payload_pallet']or(name.startswith('Bank_south_L5_')and group in ['cell_pusher','cell_gate'])
   if moving:
    ob.keyframe_insert('location')
    if name.startswith('Pallet_bayonet_lock_'):ob.keyframe_insert('rotation_euler')
   if f in [1,96,97,1104,1105]:ob.keyframe_insert('hide_render')
 if t<4 or t>=65:target=(.99,0,.37);direction=(1.0,-1.8,1.0);width=3.55
 elif t<16:target=(.43,-.04,a['floor']+.13);direction=(1.0,-1.8,1.0);width=1.70
 elif t<30:target=(.435,-.10,.89);direction=(1.0,-1.8,1.2);width=1.24
 elif t<38:target=(.435,0,a['floor']+.13);direction=(1.1,-1.8,.9);width=1.55
 elif t<46:target=(.435,0,.18);direction=(1.1,-1.8,1.2);width=1.35
 else:target=(1.18,0,.18);direction=(.65,-1.8,1.4);width=3.65
 d=Vector(direction).normalized();camera.location=Vector(target)+d*6;camera.rotation_euler=(-d).to_track_quat('-Z','Y').to_euler();camera_data.ortho_scale=width
 if keyframe:camera.keyframe_insert('location');camera.keyframe_insert('rotation_euler');camera_data.keyframe_insert('ortho_scale')
 return a

checks=[]
for f in range(1,1681):
 t=(f-1)/24;scene.frame_set(f);a=set_pose(t,keyframe=args.build)
 # Path/custody invariants for this animation, independent of visual rendering.
 checks.append({'frame':f,'carrier_pallet_x_equal':abs(objects['Captive_payload_pallet'].location.x-a['carrier'])<1e-7,'payload_transfers_only_at_source_height':not(0<a['feed']<1)or abs(a['floor']-.830)<1e-7,'launch_only_with_clear_lift':a['carrier']==0 or a['floor']>=.190-1e-7,'unselected_inventory_static':all(o.location.length<1e-7 for n,o in objects.items()if n.startswith('Bank_')and not n.startswith('Bank_south_L5_'))})
assert all(all(v for k,v in q.items()if k!='frame')for q in checks)
if args.build:
 next_payload=objects['Bank_south_L4_Stored_3U']
 for frame,color in [(1,colors['payload']),(1560,colors['payload']),(1561,accent),(1680,accent)]:
  next_payload.color=color;next_payload.keyframe_insert('color',frame=frame)
 for ob in list(objects.values())+[camera,camera_data]:
  if ob.animation_data and ob.animation_data.action:
   for fc in ob.animation_data.action.fcurves:
    for point in fc.keyframe_points:point.interpolation='LINEAR' if fc.data_path!='hide_render' else 'CONSTANT'
 scene['configuration']='VOLLEY-G5-ACR1';scene['animation_class']='CAD-derived rigid-part editorial operating sequence; edited timing; no measured/contact dynamics claim'
 scene['source_blend_sha256']=hashlib.sha256(source.read_bytes()).hexdigest()
 scene.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(out/'VOLLEY_ACR1_operating_cycle.blend'),compress=True)
 prov={'configuration':'VOLLEY-G5-ACR1','duration_s':70,'fps':24,'frames':1680,'render_size':[1280,720],'source_blend_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'source_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'geometry_objects':len(objects),'all_source_meshes_preserved':True,'display_timing':'Edited; feeder/lift time compression and launch slow motion, not simulation time','detail_visibility':'Other banks, bank mounts and host mounting ladder hidden during details; nominal spring reference envelopes omitted throughout','not_shown':'Real host mounts, sensing electronics and payload details beyond accepted envelope; purchased thread/spring detail','animation_invariants':{'sampled_frames':len(checks),'all_pass':True,'checks':list(checks[0])[1:]},'source_meshes':identities}
 (out/'ANIMATION_PROVENANCE.json').write_text(json.dumps(prov,indent=2)+'\n')
 (out/'ANIMATION_PATH_CHECKS.json').write_text(json.dumps(checks,indent=2)+'\n')
if args.preview:
 for t in [1,8,16,21.5,27,34,40,45,52,56,62,68]:
  frame=round(t*24)+1;scene.frame_set(frame);set_pose(t);scene.render.filepath=str(out/f'preview-{frame:04d}.jpg');bpy.ops.render.render(write_still=True)
