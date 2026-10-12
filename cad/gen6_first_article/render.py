#!/usr/bin/env python3
"""Render labeled Blender review images from FreeCAD native geometry tessellation.

Run: blender -b --factory-startup -P cad/gen6_first_article/render.py
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parent
MESH = Path("/tmp/volley_gen6_go2_meshes")
MANIFEST = json.loads((MESH / "manifest.json").read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def material(name,color,metal=0.0):
    m=bpy.data.materials.new(name)
    m.diffuse_color=(*color,1)
    m.use_nodes=True
    node=m.node_tree.nodes.get("Principled BSDF")
    node.inputs["Base Color"].default_value=(*color,1)
    node.inputs["Metallic"].default_value=metal
    node.inputs["Roughness"].default_value=0.38
    # Physical scene dimensions are millimetres; a controlled emissive fill
    # keeps review colors legible without changing the imported geometry.
    node.inputs["Emission Color"].default_value=(*color,1)
    node.inputs["Emission Strength"].default_value=0.65
    return m


def role(name):
    if name.startswith("Passive_"):return "payload"
    if name.startswith(("Carrier_Al", "Carrier_Pusher")):return "carrier"
    if name.startswith("PM_"):return "magnet"
    if name.startswith("Copper_"):return "plate"
    if name.startswith("Primary_"):return "drive"
    if name.startswith("Carrier_Brake_"):return "brake"
    if name.startswith("Guide_"):return "guide"
    if name.startswith("Support_"):return "support"
    return "frame"


def text_label(camera,text,x,y,size,mat):
    curve=bpy.data.curves.new(text[:15],"FONT")
    curve.body=text
    curve.size=size
    obj=bpy.data.objects.new(text[:15],curve)
    bpy.context.collection.objects.link(obj)
    obj.parent=camera
    obj.location=(x,y,-100)
    curve.materials.append(mat)


def render(kind):
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    palette={
        "payload":material("inert 3U surrogate",(0.10,0.65,0.62),0.2),
        "carrier":material("captured carrier",(0.13,0.43,0.80),0.65),
        "magnet":material("magnet envelope",(0.91,0.58,0.18),0.4),
        "plate":material("conductive plate envelope",(0.91,0.40,0.17),0.55),
        "drive":material("unrated primary envelope",(0.75,0.31,0.18),0.4),
        "brake":material("unrated brake envelope",(0.87,0.61,0.16),0.2),
        "guide":material("guide",(0.68,0.75,0.80),0.65),
        "support":material("support lips",(0.39,0.55,0.65),0.6),
        "frame":material("ladder frame",(0.34,0.43,0.54),0.7),
    }
    for item in MANIFEST["candidates"][kind]["parts"]:
        path=MESH/item["obj"]
        if sha(path)!=item["sha256"]:raise RuntimeError("render mesh hash mismatch")
        before=set(bpy.data.objects)
        bpy.ops.wm.obj_import(filepath=str(path),forward_axis="Y",up_axis="Z")
        imported=[o for o in bpy.data.objects if o not in before and o.type=="MESH"]
        if len(imported)!=1:raise RuntimeError(f"unexpected OBJ objects {item['name']}")
        obj=imported[0]
        obj.name=item["name"]
        corners=[obj.matrix_world @ Vector(c) for c in obj.bound_box]
        bounds=[min(p.x for p in corners),max(p.x for p in corners),
                min(p.y for p in corners),max(p.y for p in corners),
                min(p.z for p in corners),max(p.z for p in corners)]
        if any(abs(a-b)>0.05 for a,b in zip(bounds,item["bounds_mm"])):
            raise RuntimeError(f"FreeCAD/Blender bound mismatch {item['name']}: {bounds}")
        obj.data.materials.append(palette[role(item["name"])])
        for face in obj.data.polygons:face.use_smooth=False
    bpy.ops.object.camera_add(location=(2450,-1850,1100))
    camera=bpy.context.object
    target=Vector((900,0,95))
    camera.rotation_euler=(target-camera.location).to_track_quat("-Z","Y").to_euler()
    camera.data.type="ORTHO"
    camera.data.ortho_scale=2350
    camera.data.clip_end=10000
    bpy.context.scene.camera=camera
    bpy.ops.object.light_add(type="AREA",location=(800,-500,1450))
    bpy.context.object.data.energy=250000
    bpy.context.object.data.shape="DISK"
    bpy.context.object.data.size=1800
    bpy.ops.object.light_add(type="AREA",location=(1500,850,900))
    bpy.context.object.data.energy=100000
    bpy.context.object.data.size=1200
    world=bpy.data.worlds.new("deep background")
    world.use_nodes=True
    world.node_tree.nodes["Background"].inputs["Color"].default_value=(0.014,0.033,0.053,1)
    world.node_tree.nodes["Background"].inputs["Strength"].default_value=0.9
    bpy.context.scene.world=world
    white=material("annotations",(0.95,0.97,0.99))
    muted=material("annotation detail",(0.58,0.70,0.79))
    for label_mat in (white,muted):
        bsdf=label_mat.node_tree.nodes.get("Principled BSDF")
        bsdf.inputs["Emission Color"].default_value=label_mat.diffuse_color
        bsdf.inputs["Emission Strength"].default_value=1.5
    title="GEN6 / CANDIDATE A · PM CARRIER" if kind=="A" else "GEN6 / CANDIDATE B · CONDUCTIVE PLATE"
    text_label(camera,title,-1090,560,56,white)
    text_label(camera,"FREECAD NATIVE → STEP → BLENDER MESH REVIEW",-1090,505,27,muted)
    text_label(camera,"4 KG 3U INERT SURROGATE  |  1.3 M STROKE  |  UNRATED DRIVE + BRAKE",-1090,-585,28,white)
    text_label(camera,"ENVELOPE STUDY · NO MOTOR, CONTACT, TOLERANCE OR FLIGHT APPROVAL",-1090,-635,24,muted)
    scene=bpy.context.scene
    scene.render.engine="BLENDER_EEVEE_NEXT"
    scene.eevee.taa_render_samples=16
    scene.render.resolution_x=1600
    scene.render.resolution_y=900
    scene.render.resolution_percentage=100
    scene.render.image_settings.file_format="JPEG"
    scene.render.image_settings.quality=92
    scene.render.filepath=str(ROOT/"release"/f"Gen6_G1_{kind}_STEP_derived.jpg")
    scene.view_settings.view_transform="AgX"
    bpy.ops.render.render(write_still=True)


for candidate in ("A","B"):
    render(candidate)
