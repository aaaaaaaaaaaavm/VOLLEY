"""Render actual FM06 CAD meshes with Blender Cycles. No synthetic mechanism."""
from pathlib import Path
import sys,json,hashlib,math
import bpy
from mathutils import Vector
H=Path(__file__).resolve().parent;source=H/'render_meshes/MESHES.json';D=json.loads(source.read_text());O=H/'figures'
bpy.ops.wm.read_factory_settings(use_empty=True)
scene=bpy.context.scene;scene.render.engine='BLENDER_WORKBENCH';scene.render.threads_mode='FIXED';scene.render.threads=1;scene.display.shading.light='STUDIO';scene.display.shading.studiolight_rotate_z=.4;scene.display.shading.color_type='MATERIAL';scene.display.shading.show_shadows=True;scene.display.shading.show_cavity=True;scene.display.shading.cavity_type='BOTH';scene.display.shading.show_object_outline=True;scene.display.shading.object_outline_color=(.08,.10,.12)
scene.render.resolution_x=1400;scene.render.resolution_y=1000;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.world=bpy.data.worlds.new('White studio');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.93,.95,.97,1);scene.world.node_tree.nodes['Background'].inputs[1].default_value=.45;scene.view_settings.exposure=0;scene.view_settings.view_transform='Standard';scene.display.shading.background_type='WORLD';scene.world.color=(1,1,1)
mats={}
for name,color,metal in [('frame',(.55,.59,.63,1),.35),('payload',(.10,.27,.40,1),.2),('restraint',(.75,.38,.10,1),.3),('steel',(.25,.28,.31,1),.5)]:
 m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=color;p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=.5;mats[name]=m
bpy.ops.object.camera_add(location=(.85,-.95,.78));cam=bpy.context.object;target=Vector((.18,-.08,.025));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=.91;scene.camera=cam
for loc,power,size in [((.1,-.3,1.2),45,1),((-.6,.2,.8),25,.8)]:
 bpy.ops.object.light_add(type='AREA',location=loc);light=bpy.context.object;light.data.energy=power;light.data.shape='DISK';light.data.size=size;light.rotation_euler=(target-light.location).to_track_quat('-Z','Y').to_euler()
records=[]
for record in D['poses']:
 objs=[]
 for row in record['parts']:
  p=H/'render_meshes'/row['file'];assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'];verts=[];faces=[]
  for line in p.read_text().splitlines():
   a=line.split()
   if a[0]=='v':verts.append(tuple(map(float,a[1:])))
   elif a[0]=='f':faces.append(tuple(int(v)-1 for v in a[1:]))
  mesh=bpy.data.meshes.new(row['name']);mesh.from_pydata(verts,[],faces);mesh.update();ob=bpy.data.objects.new(row['name'],mesh);scene.collection.objects.link(ob);objs.append(ob)
  name=row['name'];mat='payload' if name=='payload' else ('restraint' if any(s in name for s in ['gate','front','entry']) else ('steel' if any(s in name for s in ['pin','shoe','guide','shaft','screw']) else 'frame'));ob.data.materials.append(mats[mat])
 scene.render.filepath=str(O/('FM06_Technical_'+record['phase']+'.png'));bpy.ops.render.render(write_still=True)
 records.append({'phase':record['phase'],'source':record['source'],'source_sha256':record['sha256'],'image':Path(scene.render.filepath).name,'sha256':hashlib.sha256(Path(scene.render.filepath).read_bytes()).hexdigest()})
 for ob in objs:bpy.data.objects.remove(ob,do_unlink=True)
(O/'BLENDER_PROVENANCE.json').write_text(json.dumps({'software':'Blender '+bpy.app.version_string,'engine':'Blender Workbench technical rendering','tessellation_source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'evidence_class':'Rendered actual CAD geometry; nominal prescribed states. Not hardware photographs, solver screenshots, motion/contact/strength/qualification evidence.','renders':records},indent=2)+'\n')
