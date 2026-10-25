"""Blender orthographic scientific views of the frozen native CAD tessellations."""
from pathlib import Path
import bpy,json,hashlib,math
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
HERE=Path(__file__).resolve().parent
OUT=HERE/'renders';OUT.mkdir(exist_ok=True)
WIDTH,HEIGHT=2800,2100
COLORS={'aluminium':(.62,.65,.67,1),'steel':(.29,.32,.35,1),'copper':(.66,.36,.19,1),'ndfeb':(.19,.22,.25,1),'payload':(.22,.43,.63,1),'polymer':(.42,.45,.44,1),'catalog':(.35,.38,.41,1),'insulator':(.79,.81,.77,1)}
bpy.ops.wm.read_factory_settings(use_empty=True)
materials={}
for name,color in {**COLORS,'annotation_text':(.035,.045,.06,1),'annotation_white':(4,4,4,1)}.items():
 material=bpy.data.materials.new(name);material.diffuse_color=color;material.use_nodes=False;materials[name]=material
font_path=Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf');font=bpy.data.fonts.load(str(font_path))if font_path.exists()else bpy.data.fonts.get('Bfont')
configs=[
 {'id':'01_assembly_isometric','state':'home','title':'VOLLEY G5 ACR1 - integrated assembly','subtitle':'Home pose | 12 installed 3U storage cells | one retained carrier pallet','direction':(1.0,-1.0,1.0),'fit':'all','scale_bar_m':.5,'labels':[
  {'text':'12 installed storage cells','uv':(.055,.80),'target':(.434,-.250,.490)},
  {'text':'Carrier and captive pallet','uv':(.055,.26),'target':(.434,0,.041)},
  {'text':'Fixed stator and 2250 mm guide track','uv':(.55,.27),'target':(1.60,0,0)}]},
 {'id':'02_handoff_pallet_locks','state':'handoff','title':'Handoff - captive pallet and positive lock interfaces','subtitle':'Dual custody: carrier bayonets and outboard lift grip pins engaged','direction':(.75,-1.8,.78),'target':(.445,-.025,.085),'ortho_scale':.50,'hide_banks':True,'scale_bar_m':.1,'labels':[
  {'text':'Rear keyed bayonet lock','uv':(.045,.23),'target':(.240,-.090,.0455)},
  {'text':'Forward keyed bayonet lock','uv':(.57,.21),'target':(.668,-.090,.0455)},
  {'text':'Outboard lift grip (engaged)','uv':(.61,.73),'target':(.7045,0,.041)},
  {'text':'Four feet: Z30 to Z38','uv':(.045,.36),'target':(.338,-.046,.034)},
  {'text':'3U payload envelope','uv':(.045,.78),'target':(.434,0,.110)}]},
 {'id':'03_captured_source_level','state':'captured','title':'Captured transfer - source level 5, payload floor Z830','subtitle':'Payload and pallet held by the lift | carrier pallet locks open','direction':(1.1,-1.65,.9),'fit':'module','scale_bar_m':.25,'labels':[
  {'text':'Captured 3U payload','uv':(.055,.81),'target':(.434,0,.880)},
  {'text':'Pallet carried by lift grips','uv':(.57,.67),'target':(.434,0,.825)},
  {'text':'Source cell: south bank, level 5','uv':(.055,.59),'target':(.605,-.150,.935)}]},
 {'id':'04_clear_docked','state':'clear','title':'Clear / docked - pallet retained on the carrier','subtitle':'Lift and custody frame at Z190 | payload floor remains Z46','direction':(2.8,-.65,.75),'target':(.445,0,.240),'ortho_scale':.80,'scale_bar_m':.10,'labels':[
  {'text':'Raised custody frame (floor Z190)','uv':(.055,.66),'target':(.605,-.046,.250)},
  {'text':'Payload on locked pallet','uv':(.055,.32),'target':(.6045,0,.096)},
  {'text':'Pallet stays with the carrier','uv':(.56,.24),'target':(.7145,0,.045)}]}
]
def add_mesh(scene,name,vertices,faces,material,collection):
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(vertices,[],faces);mesh.update()
 ob=bpy.data.objects.new(name,mesh);collection.objects.link(ob);ob.data.materials.append(material);return ob

def set_camera(scene,config,objects):
 camera_data=bpy.data.cameras.new(config['id']+'_camera');camera_data.type='ORTHO';camera_data.clip_start=.01;camera_data.clip_end=100
 cam=bpy.data.objects.new(config['id']+'_camera',camera_data);scene.collection.objects.link(cam);scene.camera=cam
 direction=Vector(config['direction']).normalized();rotation=(-direction).to_track_quat('-Z','Y');cam.rotation_euler=rotation.to_euler()
 right=rotation@Vector((1,0,0));up=rotation@Vector((0,1,0));aspect=WIDTH/HEIGHT
 if config.get('fit'):
  selected=objects if config['fit']=='all'else[o for o in objects if o['cad_name'].startswith(('Bank_','Lift_','Cradle_','Transferred_','Sled_','Captive_','Pallet_','Magnet_'))]
  corners=[o.matrix_world@Vector(c)for o in selected for c in o.bound_box]
  low=Vector([min(v[i]for v in corners)for i in range(3)]);high=Vector([max(v[i]for v in corners)for i in range(3)]);target=(low+high)/2
  xp=[(v-target).dot(right)for v in corners];yp=[(v-target).dot(up)for v in corners]
  target+=right*((max(xp)+min(xp))/2)+up*((max(yp)+min(yp))/2)
  scale=max((max(yp)-min(yp))/.74,(max(xp)-min(xp))/(aspect*.88))
 else:target=Vector(config['target']);scale=config['ortho_scale']
 cam.location=target+direction*6;camera_data.ortho_scale=scale*aspect;cam['frame_height_m']=scale
 return cam

def plane_point(cam,u,v,distance=.3):
 h=cam['frame_height_m'];w=h*WIDTH/HEIGHT
 return cam.location+cam.rotation_euler.to_quaternion()@Vector(((u-.5)*w,(v-.5)*h,-distance))

def add_text(scene,collection,cam,text,u,v,size=.013,background=False,align='LEFT'):
 data=bpy.data.curves.new('Annotation '+text,'FONT');data.body=text;data.size=cam['frame_height_m']*size;data.align_x=align;data.align_y='CENTER';data.font=font
 ob=bpy.data.objects.new('Annotation '+text,data);collection.objects.link(ob);ob.location=plane_point(cam,u,v);ob.rotation_euler=cam.rotation_euler;ob.data.materials.append(materials['annotation_text'])
 if background:
  bpy.context.view_layer.update();width=max(v[0]for v in ob.bound_box)-min(v[0]for v in ob.bound_box);pad=cam['frame_height_m']*.005;height=cam['frame_height_m']*size*1.35
  center=plane_point(cam,u,v,.304)+cam.rotation_euler.to_quaternion()@Vector((width/2 if align=='LEFT'else 0,0,0))
  verts=[(-width/2-pad,-height/2,0),(width/2+pad,-height/2,0),(width/2+pad,height/2,0),(-width/2-pad,height/2,0)]
  panel=add_mesh(scene,'Annotation background',verts,[(0,1,2,3)],materials['annotation_white'],collection);panel.location=center;panel.rotation_euler=cam.rotation_euler
 return ob

def add_line(scene,collection,cam,uvs,name='Annotation leader'):
 data=bpy.data.curves.new(name,'CURVE');data.dimensions='3D';data.bevel_depth=cam['frame_height_m']/HEIGHT*.65;data.bevel_resolution=0
 spline=data.splines.new('POLY');spline.points.add(len(uvs)-1)
 for point,(u,v)in zip(spline.points,uvs):point.co=(*plane_point(cam,u,v,.295 if name.startswith('View-plane')else .306),1)
 ob=bpy.data.objects.new(name,data);collection.objects.link(ob);ob.data.materials.append(materials['annotation_text']);return ob

records=[]
for i,config in enumerate(configs):
 scene=bpy.context.scene if i==0 else bpy.data.scenes.new(config['id']);scene.name=config['id'];bpy.context.window.scene=scene
 scene.render.engine='BLENDER_WORKBENCH';scene.render.resolution_x=WIDTH;scene.render.resolution_y=HEIGHT;scene.render.resolution_percentage=100
 scene.render.image_settings.color_mode='RGB';scene.render.film_transparent=False;scene.render.image_settings.compression=20
 scene.world=bpy.data.worlds.new(config['id']+'_world');scene.world.color=(1,1,1)
 shading=scene.display.shading;shading.light='STUDIO';shading.color_type='MATERIAL';shading.background_type='VIEWPORT';shading.background_color=(1,1,1)
 shading.show_shadows=False;shading.show_cavity=False;shading.cavity_type='BOTH';shading.curvature_ridge_factor=1.15;shading.curvature_valley_factor=1.05;shading.cavity_ridge_factor=1.15;shading.cavity_valley_factor=1.05;shading.show_object_outline=True;shading.object_outline_color=(.10,.12,.14)
 if hasattr(shading,'show_specular_highlight'):shading.show_specular_highlight=False
 scene.display.render_aa='16';scene.view_settings.view_transform='Standard';scene.view_settings.look='None'
 geometry=bpy.data.collections.new(config['id']+' - native CAD geometry');scene.collection.children.link(geometry)
 annotations=bpy.data.collections.new(config['id']+' - annotations, not hardware');scene.collection.children.link(annotations)
 path=HERE/'meshes'/(config['state']+'.json');data=json.loads(path.read_text());objects=[];hidden=[]
 for item in data['objects']:
  ob=add_mesh(scene,item['name'],item['vertices_m'],item['triangles'],materials[item['material']],geometry)
  ob['cad_name']=item['name'];ob['cad_material']=item['material'];ob['cad_subsystem']=item['subsystem'];ob['geometry_provenance']='Frozen FreeCAD tessellation;no geometry edits'
  if config.get('hide_banks')and(item['name'].startswith('Bank_')or item['name']in ['Host_mount_ladder','Lift_connected_fixed_frame']):ob.hide_render=True;hidden.append(item['name'])
  objects.append(ob)
 bpy.context.view_layer.update();cam=set_camera(scene,config,objects);bpy.context.view_layer.update()
 # Opaque white caption margins are display graphics, not CAD geometry.
 for low,high in [(0,.115),(.905,1)]:
  corners=[plane_point(cam,u,v,.302)for u,v in [(0,low),(1,low),(1,high),(0,high)]]
  add_mesh(scene,'Caption margin (display only)',corners,[(0,1,2,3)],materials['annotation_white'],annotations)
 add_text(scene,annotations,cam,config['title'],.035,.962,size=.036)
 add_text(scene,annotations,cam,config['subtitle'],.035,.930,size=.018)
 label_records=[]
 for label in config['labels']:
  projected=world_to_camera_view(scene,cam,Vector(label['target']));u,v=label['uv'];target_uv=(float(projected.x),float(projected.y))
  add_line(scene,annotations,cam,[(u,v),target_uv]);add_text(scene,annotations,cam,label['text'],u,v,size=.024,background=True)
  label_records.append({**label,'target_projected_uv':target_uv})
 footer='Detail: storage banks, host ladder and fixed lift frame hidden'if hidden else'All CAD parts present; view framing may crop distant geometry'
 add_text(scene,annotations,cam,footer,.035,.064,size=.014)
 add_text(scene,annotations,cam,'Orthographic | payloads are nominal 3U envelopes | visualization mesh: 0.3 mm',.035,.040,size=.014)
 bar=config['scale_bar_m'];h=cam['frame_height_m'];w=h*WIDTH/HEIGHT;u0=.77;v=.085;u1=u0+bar/w
 add_line(scene,annotations,cam,[(u0,v),(u1,v)],'View-plane scale bar')
 for u in [u0,u1]:add_line(scene,annotations,cam,[(u,v-.003),(u,v+.003)],'View-plane scale tick')
 add_text(scene,annotations,cam,f'{bar*1000:g} mm (view plane)',(u0+u1)/2,.062,size=.016,align='CENTER')
 record={'view_id':config['id'],'state':config['state'],'render_engine':'Blender Workbench 4.3.2','projection':'ORTHOGRAPHIC','resolution_px':[WIDTH,HEIGHT],'source_mesh_file':str(path),'source_mesh_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'native_provenance':data['provenance'],'camera':{'location_m':list(cam.location),'rotation_euler_rad':list(cam.rotation_euler),'ortho_scale_m':cam.data.ortho_scale,'frame_height_m':cam['frame_height_m']},'CAD_object_count':len(objects),'rendered_CAD_object_count':len(objects)-len(hidden),'hidden_CAD_objects':hidden,'hidden_parts_disclosure':footer,'annotation_targets_m':label_records,'fabricated_geometry':'None. Text, leader lines, scale bar, and annotation backing panels are separate display-only objects.'}
 records.append(record)
 print('SCENE_READY',config['id'],len(objects),len(hidden),flush=True)
# Pack the annotation font and retain all four editable scenes in one native source.
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'VOLLEY_G5_ACR1_scientific_views.blend'))
for config,record in zip(configs,records):
 scene=bpy.data.scenes[config['id']];bpy.context.window.scene=scene
 png=OUT/(config['id']+'.png');jpg=OUT/(config['id']+'.jpg')
 scene.render.image_settings.file_format='PNG';scene.render.filepath=str(png);bpy.ops.render.render(write_still=True,scene=scene.name)
 scene.render.image_settings.file_format='JPEG';scene.render.image_settings.quality=95;bpy.data.images['Render Result'].save_render(str(jpg),scene=scene)
 scene.render.image_settings.file_format='PNG';scene.render.filepath=str(png)
 record['outputs']={p.name:{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}for p in [png,jpg]}
 (OUT/(config['id']+'_provenance.json')).write_text(json.dumps(record,indent=2)+'\n')
 print('RENDERED',config['id'],flush=True)
bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'VOLLEY_G5_ACR1_scientific_views.blend'))
(HERE/'VIEW_PROVENANCE.json').write_text(json.dumps({'configuration_id':'VOLLEY-G5-ACR1','render_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'blend_file':str(HERE/'VOLLEY_G5_ACR1_scientific_views.blend'),'blend_sha256':hashlib.sha256((HERE/'VOLLEY_G5_ACR1_scientific_views.blend').read_bytes()).hexdigest(),'views':records},indent=2)+'\n')
print('ALL_VIEWS_COMPLETE',flush=True)
