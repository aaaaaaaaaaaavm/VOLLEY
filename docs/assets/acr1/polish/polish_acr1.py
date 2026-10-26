"""Restyle accepted ACR1 Blender geometry; no hardware mesh/transform edits.

blender -b -t 4 -P polish_acr1.py -- --source SOURCE.blend --output OUTPUT --preview
"""
from pathlib import Path
import argparse,sys,json,hashlib,math,bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',required=True);p.add_argument('--preview',action='store_true');p.add_argument('--only',default='');p.add_argument('--save-scene',action='store_true');cfg=p.parse_args(args)
source=Path(cfg.source).resolve();out=Path(cfg.output).resolve();out.mkdir(exist_ok=True,parents=True)
source_hash=hashlib.sha256(source.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(source))
original={s.name:s for s in bpy.data.scenes}
# Every hardware object retains its accepted mesh and object transform.
def cad_objects(scene):return [o for o in scene.objects if 'cad_name' in o]
def geometry_hash(ob):
 h=hashlib.sha256()
 for v in ob.data.vertices:h.update((','.join(float(x).hex() for x in v.co)+';').encode())
 for face in ob.data.polygons:h.update((','.join(str(i) for i in face.vertices)+';').encode())
 return h.hexdigest()
source_geometry={o.name:geometry_hash(o) for s in original.values() for o in cad_objects(s)}
colors={'aluminium':(.59,.62,.63,1),'steel':(.26,.30,.32,1),'copper':(.43,.43,.40,1),'ndfeb':(.14,.17,.19,1),'payload':(.70,.73,.72,1),'polymer':(.25,.28,.28,1),'catalog':(.32,.36,.37,1),'insulator':(.57,.59,.55,1)}
accent=(.05,.62,.59,1)
configs=[
 {'id':'assembly_hero','source':'01_assembly_isometric','target':(1.05,0,.35),'direction':(1.1,-1.8,1.0),'width':3.30,'size':(2000,1250),'hide':'none'},
 {'id':'feeder_detail','source':'01_assembly_isometric','target':(.435,-.30,.875),'direction':(-1.0,-1.5,1.8),'width':.82,'size':(1800,1350),'hide':'single_cell'},
 {'id':'sequence_01_home','source':'01_assembly_isometric','target':(.44,0,.50),'direction':(1.4,-2.5,1.2),'width':1.65,'size':(900,1050),'hide':'sequence_focus'},
 {'id':'sequence_02_captured','source':'03_captured_source_level','target':(.44,0,.50),'direction':(1.4,-2.5,1.2),'width':1.65,'size':(900,1050),'hide':'sequence_focus'},
 {'id':'sequence_03_handoff','source':'02_handoff_pallet_locks','target':(.44,0,.50),'direction':(1.4,-2.5,1.2),'width':1.65,'size':(900,1050),'hide':'sequence_focus'},
 {'id':'sequence_04_clear','source':'04_clear_docked','target':(.44,0,.50),'direction':(1.4,-2.5,1.2),'width':1.65,'size':(900,1050),'hide':'sequence_focus'}]
records=[];scenes=[]
for config in configs:
 scene=bpy.data.scenes.new(config['id']);scenes.append(scene);bpy.context.window.scene=scene
 scene.render.engine='BLENDER_WORKBENCH';scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGB';scene.render.film_transparent=False
 scene.render.resolution_x=config['size'][0];scene.render.resolution_y=config['size'][1];scene.render.resolution_percentage=45 if cfg.preview else 100
 scene.world=bpy.data.worlds.new(config['id']+'_world');scene.world.color=(.035,.045,.052)
 shade=scene.display.shading;shade.light='STUDIO';shade.studiolight_rotate_z=.3;shade.studiolight_background_alpha=0
 shade.color_type='OBJECT';shade.background_type='VIEWPORT';shade.background_color=(.035,.045,.052)
 shade.show_shadows=True;shade.show_cavity=True;shade.cavity_type='BOTH';shade.curvature_ridge_factor=1.25;shade.curvature_valley_factor=1.0;shade.cavity_ridge_factor=1.0;shade.cavity_valley_factor=1.0
 shade.show_object_outline=True;shade.object_outline_color=(.12,.15,.17);shade.show_specular_highlight=True
 scene.display.render_aa='16' if cfg.preview else '8';scene.view_settings.view_transform='Standard';scene.view_settings.look='None'
 geometry=bpy.data.collections.new(config['id']+'_accepted_CAD');scene.collection.children.link(geometry)
 hidden=[];shown=[];accented=[];identity=[]
 for src in cad_objects(original[config['source']]):
  ob=src.copy();ob.name=config['id']+'_'+src['cad_name'];geometry.objects.link(ob);ob.hide_render=False;ob.hide_viewport=False
  name=src['cad_name'];ob.color=colors[src['cad_material']]
  active=name in ['Transferred_3U','Captive_payload_pallet'] or name=='Bank_south_L5_Stored_3U' or (name.startswith('Bank_south_L5_') and src['cad_subsystem'] in ['cell_drive','cell_pusher'])
  if active:ob.color=accent;accented.append(name)
  omit=(config['hide']=='single_cell' and (not name.startswith('Bank_south_L5_') or name in ['Bank_south_L5_Stored_3U','Bank_south_L5_Fixed_channel_frame'])) or (config['hide']=='sequence_focus' and ((name.startswith('Bank_') and not name.startswith('Bank_south_L5_')) or name=='Host_mount_ladder'))
  if omit:ob.hide_render=True;hidden.append(name)
  else:shown.append(name)
  require=geometry_hash(ob)==source_geometry[src.name] and ob.matrix_world==src.matrix_world
  if not require:raise RuntimeError('Hardware geometry/transform changed: '+name)
  identity.append({'cad_name':name,'mesh_identity_sha256':source_geometry[src.name]})
 cam_data=bpy.data.cameras.new(config['id']+'_camera');cam_data.type='ORTHO';cam_data.ortho_scale=config['width'];cam_data.clip_start=.01;cam_data.clip_end=100
 cam=bpy.data.objects.new(config['id']+'_camera',cam_data);scene.collection.objects.link(cam);scene.camera=cam
 target=Vector(config['target']);direction=Vector(config['direction']).normalized();cam.location=target+direction*6;cam.rotation_euler=(-direction).to_track_quat('-Z','Y').to_euler()
 scene['configuration']='VOLLEY-G5-ACR1';scene['visual_class']='CAD-derived render; nominal surrogate envelopes; not hardware photography'
 scene['source_state']=config['source'];scene['geometry_edits']='None';scene['hidden_part_count']=len(hidden)
 record={**config,'render_engine':'Blender '+bpy.app.version_string+' Workbench','hardware_objects':len(shown)+len(hidden),'shown_objects':len(shown),'hidden_objects':hidden,'accent_objects':accented,'camera':{'location_m':list(cam.location),'rotation_euler_rad':list(cam.rotation_euler),'orthographic_width_m':cam_data.ortho_scale},'geometry_identities':identity,'geometry_and_transform_checks_pass':True}
 bpy.context.view_layer.update()
 if config['id']=='feeder_detail':
  points={'1':(.216,-.2775,.880),'2':(.216,-.535,.880),'3':(.434,-.346,.880),'4':(.6245,-.27,.880)}
  record['editorial_targets']={key:{'target_m':point,'projected_uv':list(world_to_camera_view(scene,cam,Vector(point)))[:2]} for key,point in points.items()}
 records.append(record)
# Remove source annotations and original scene data from the derivative.
for scene in original.values():bpy.data.scenes.remove(scene)
bpy.ops.outliner.orphans_purge(do_recursive=True)
for scene in scenes:scene.render.filepath='//'+scene.name+'.png'
bpy.context.window.scene=scenes[0]
if not cfg.preview and cfg.save_scene:bpy.ops.wm.save_as_mainfile(filepath=str(out/'VOLLEY_ACR1_polished.blend'),compress=True)
for scene,record in zip(scenes,records):
 if cfg.only and scene.name not in cfg.only.split(','):continue
 imagepath=out/(scene.name+('_preview' if cfg.preview else '')+'.png');scene.render.filepath=str(imagepath)
 bpy.context.window.scene=scene;bpy.ops.render.render(write_still=True)
 record['render_file']=imagepath.name;record['render_sha256']=hashlib.sha256(imagepath.read_bytes()).hexdigest();print('RENDERED',imagepath.name,flush=True)
for scene in scenes:scene.render.filepath='//'+scene.name+'.png'
if not cfg.preview and cfg.save_scene:bpy.ops.wm.save_as_mainfile(filepath=str(out/'VOLLEY_ACR1_polished.blend'),compress=True)
provenance={'configuration':'VOLLEY-G5-ACR1','source_blend_basename':source.name,'source_blend_sha256':source_hash,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'software':bpy.app.version_string,'preview':cfg.preview,'no_geometry_or_transform_edits':True,'views':records}
(out/('PREVIEW_PROVENANCE.json' if cfg.preview else 'POLISH_PROVENANCE.json')).write_text(json.dumps(provenance,indent=2)+'\n')
