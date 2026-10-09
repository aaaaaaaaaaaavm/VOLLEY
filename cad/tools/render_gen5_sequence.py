"""Render a STEP-derived, conceptual Gen5 operations sequence in Blender.

FreeCAD first tessellates the checked source-linked STEP solids with
cad/tools/export_step_view_meshes.py. This Blender script rechecks mesh hashes
and source bounds, then animates the intent only: feed, handoff, acceleration,
and payload continuation after sled arrest. These motions are not a clearance,
contact, timing, or hardware validation. The reference side-fed assembly fails
its own static fit check. One near cassette shell and the enclosure are hidden.

Example:
  blender -b --factory-startup -P cad/tools/render_gen5_sequence.py -- \
    --mesh-manifest /tmp/volley-step-review-meshes/meshes.json --preview
  blender -b --factory-startup -P cad/tools/render_gen5_sequence.py -- \
    --mesh-manifest /tmp/volley-step-review-meshes/meshes.json
"""
from __future__ import annotations
import argparse
import hashlib
import json
import sys
from pathlib import Path
import bpy
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'cad/renders/sequence'
FRAME_DIR=Path('/tmp/volley-gen5-sequence-frames')
COLORS={'Interface':(.50,.70,.77,1),'Track':(.72,.79,.86,1),'Stator':(.91,.37,.18,1),
        'Sled':(.14,.80,.88,1),'Brake':(.97,.75,.29,1),'Magazine':(.54,.65,.76,1),
        'Payload':(.30,.82,.63,1)}

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def text(body, camera, x,y,size,color):
    curve=bpy.data.curves.new(body[:24],'FONT');curve.body=body;curve.size=size
    ob=bpy.data.objects.new(body[:24],curve);bpy.context.collection.objects.link(ob)
    ob.parent=camera;ob.location=(x,y,-155);ob.color=color
    return ob

def make_scene(manifest, mesh_root):
    parts=manifest['configurations']['gen5_reference']['parts']
    objects={}
    for item in parts:
        name=item['instance']
        if name in ('Enclosure','Magazine_S'):continue
        source=mesh_root/item['obj_file']
        if sha(source)!=item['obj_sha256']:raise RuntimeError('STEP display mesh changed: '+str(source))
        before=set(bpy.data.objects)
        bpy.ops.wm.obj_import(filepath=str(source),forward_axis='Y',up_axis='Z')
        added=[o for o in bpy.data.objects if o not in before and o.type=='MESH']
        if len(added)!=1:raise RuntimeError(f'{name}: expected one imported mesh')
        obj=added[0];obj.name=name
        bounds=[obj.matrix_world@Vector(c) for c in obj.bound_box]
        actual=[min(p.x for p in bounds),max(p.x for p in bounds),min(p.y for p in bounds),max(p.y for p in bounds),min(p.z for p in bounds),max(p.z for p in bounds)]
        if any(abs(a-b)>1.5 for a,b in zip(actual,item['placed_bounds_mm'])):
            raise RuntimeError(f'{name}: display axes disagree with STEP bounds: {actual}')
        role=next((k for k in COLORS if name.startswith(k)),'Track')
        obj.color=(1.0,.84,.27,1) if name=='Payload_S01' else COLORS[role]
        objects[name]=obj
    scene=bpy.context.scene
    bpy.ops.object.camera_add(location=(2700,-2850,1770))
    camera=bpy.context.object;camera.name='Operations review camera'
    target=Vector((1000,0,360));camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler()
    camera.data.type='ORTHO';camera.data.ortho_scale=3550;camera.data.clip_end=100000
    scene.camera=camera
    scene.render.engine='BLENDER_WORKBENCH'
    scene.display.shading.light='STUDIO'
    scene.display.shading.color_type='OBJECT'
    scene.display.shading.background_type='WORLD'
    scene.world.color=(.014,.038,.072)
    scene.display.shading.show_cavity=True
    scene.display.shading.cavity_type='BOTH'
    scene.display.shading.curvature_ridge_factor=1.2
    scene.display.shading.curvature_valley_factor=1.0
    scene.render.resolution_x=1600;scene.render.resolution_y=900;scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGB'
    scene.render.film_transparent=False
    scene.render.fps=16;scene.frame_start=1;scene.frame_end=128
    scene.camera.data.lens=50
    text('VOLLEY  /  GEN5 INTENDED OPERATIONS',camera,-1560,820,89,(.94,.98,1,1))
    text('STEP GEOMETRY  |  ENCLOSURE + NEAR CASSETTE SHELL HIDDEN',camera,-1560,710,48,(.45,.84,.90,1))
    labels=['01  LOAD','02  HANDOFF','03  ACCELERATE','04  DEPART']
    positions=[-1550,-760,40,840]
    for label,x in zip(labels,positions):text(label,camera,x,-790,60,(.85,.95,1,1))
    text('CONCEPT MOTION ONLY  /  REFERENCE FIT FAILS  /  FEED, CONTACT + BRAKE UNVERIFIED',camera,-1560,-945,43,(1,.66,.38,1))
    bpy.ops.mesh.primitive_cube_add(size=1);indicator=bpy.context.object;indicator.name='Stage marker, not CAD'
    indicator.parent=camera;indicator.color=(.17,.95,.83,1);indicator.scale=(570,9,2)
    for frame,x in ((1,-1260),(32,-470),(65,330),(105,1120),(128,1120)):
        indicator.location=(x,-855,-153);indicator.keyframe_insert(data_path='location',frame=frame)
    for fcurve in indicator.animation_data.action.fcurves:
        for kp in fcurve.keyframe_points:kp.interpolation='CONSTANT'
    payload=objects['Payload_S01'];sled=objects['Sled']
    for frame,x,y in ((1,0,0),(25,0,0),(55,0,180),(60,0,180),(104,1000,180),(116,1260,180),(128,1440,180)):
        payload.location=(x,y,0);payload.keyframe_insert(data_path='location',frame=frame)
    for frame,x in ((1,0),(60,0),(104,1000),(128,1000)):
        sled.location.x=x;sled.keyframe_insert(data_path='location',frame=frame)
    for o in (payload,sled):
        for fcurve in o.animation_data.action.fcurves:
            for kp in fcurve.keyframe_points:kp.interpolation='LINEAR'
    return scene,objects

def render_frame(scene,frame,path):
    scene.frame_set(frame);scene.render.filepath=str(path)
    bpy.ops.render.render(write_still=True)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--mesh-manifest',type=Path,required=True)
    parser.add_argument('--preview',action='store_true')
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    manifest=json.loads(args.mesh_manifest.read_text());scene,objects=make_scene(manifest,args.mesh_manifest.parent)
    OUT.mkdir(parents=True,exist_ok=True);FRAME_DIR.mkdir(parents=True,exist_ok=True)
    if args.preview:
        render_frame(scene,1,OUT/'preview.png');print('preview',OUT/'preview.png');return
    for frame in range(1,129):render_frame(scene,frame,FRAME_DIR/f'frame_{frame:04d}.png')
    for number,frame in enumerate((12,57,83,123),1):
        source=FRAME_DIR/f'frame_{frame:04d}.png'
        target=OUT/f'step_{number:02d}.png';target.write_bytes(source.read_bytes())
    record={'evidence_class':'STEP-derived Blender animation of intended operations; no moving-clearance, release-contact, electrical, brake, or hardware validation',
            'source_mesh_manifest_sha256':sha(args.mesh_manifest),'native_freecad_document':'cad/native/Gen5_Review.FCStd',
            'native_freecad_sha256':sha(ROOT/'cad/native/Gen5_Review.FCStd'),
            'reference_fit':'FAIL: 11 mm transverse shortfall and 32915 mm3 track/cassette overlap per side',
            'hidden':['Enclosure','Magazine_S'],'animated':['Payload_S01','Sled'],
            'stage_frames':[12,57,83,123],'frames':128,'fps':16}
    (OUT/'PROVENANCE.json').write_text(json.dumps(record,indent=2)+'\n')
    print('rendered 128 STEP-derived conceptual frames')
if __name__=='__main__':main()
