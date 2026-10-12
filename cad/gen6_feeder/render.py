#!/usr/bin/env python3
"""Create labeled Blender images of FreeCAD-derived one-cell state geometry."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import bpy
from mathutils import Vector

HERE = Path(__file__).resolve().parent
MESH = Path("/tmp/volley_gen6_feeder_meshes")
MANIFEST = json.loads((MESH / "manifest.json").read_text())

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def material(name, color, metallic=0.0):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.use_nodes = True
    node = m.node_tree.nodes.get("Principled BSDF")
    node.inputs["Base Color"].default_value = (*color, 1)
    node.inputs["Metallic"].default_value = metallic
    node.inputs["Roughness"].default_value = 0.4
    node.inputs["Emission Color"].default_value = (*color, 1)
    node.inputs["Emission Strength"].default_value = 0.45
    return m

def label(camera, body, x, y, size, mat):
    curve = bpy.data.curves.new("label", "FONT")
    curve.body = body
    curve.size = size
    obj = bpy.data.objects.new("label", curve)
    bpy.context.collection.objects.link(obj)
    obj.parent = camera
    obj.location = (x, y, -100)
    curve.materials.append(mat)

def role(name):
    if name.startswith("Passive_"): return "payload"
    if name.startswith("Captured_"): return "pusher"
    if name.startswith("Cassette_Gate"): return "gate"
    if name.startswith("Cradle_Left"): return "gate"
    if name.endswith("Floor") or name.startswith("Transfer_"): return "floor"
    return "structure"

def render(state):
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    palette = {
        "payload": material("inert 3U envelope", (0.10, 0.76, 0.64), 0.15),
        "pusher": material("captured pusher proxy", (0.22, 0.52, 0.9), 0.45),
        "gate": material("moving barrier proxy", (0.95, 0.58, 0.20), 0.35),
        "floor": material("transfer support proxy", (0.35, 0.53, 0.67), 0.5),
        "structure": material("unrated structure", (0.58, 0.69, 0.78), 0.5),
    }
    for item in MANIFEST["states"][state]["parts"]:
        path = MESH / item["obj"]
        if sha(path) != item["sha256"]:
            raise RuntimeError("CAD mesh hash mismatch")
        before = set(bpy.data.objects)
        bpy.ops.wm.obj_import(filepath=str(path), forward_axis="Y", up_axis="Z")
        imported = [o for o in bpy.data.objects if o not in before and o.type == "MESH"]
        if len(imported) != 1:
            raise RuntimeError("unexpected mesh object count")
        obj = imported[0]
        obj.name = item["name"]
        corners = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
        bounds = [min(p.x for p in corners), max(p.x for p in corners),
                  min(p.y for p in corners), max(p.y for p in corners),
                  min(p.z for p in corners), max(p.z for p in corners)]
        if any(abs(a-b) > 0.05 for a,b in zip(bounds, item["bounds_mm"])):
            raise RuntimeError(f"FreeCAD/Blender bounds mismatch: {obj.name}")
        obj.data.materials.append(palette[role(obj.name)])
    bpy.ops.object.camera_add(location=(850, -700, 650))
    camera = bpy.context.object
    target = Vector((340, -110, 85))
    camera.rotation_euler = (target-camera.location).to_track_quat("-Z", "Y").to_euler()
    camera.data.type = "ORTHO"
    camera.data.ortho_scale = 1050
    camera.data.clip_end = 10000
    bpy.context.scene.camera = camera
    bpy.ops.object.light_add(type="AREA", location=(250, -500, 850))
    bpy.context.object.data.energy = 80000
    bpy.context.object.data.size = 800
    world = bpy.data.worlds.new("studio")
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.018, 0.04, 0.07, 1)
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.9
    bpy.context.scene.world = world
    white = material("white text", (0.96, 0.98, 1.0))
    label(camera, "GEN6 / ONE-CELL FEED STUDY / " + state.replace("_", " ").upper(), -485, 280, 22, white)
    label(camera, "FREECAD NATIVE + STEP VOLUME CHECK / BLENDER RENDER", -485, 250, 13, white)
    label(camera, "INERT 3U ENVELOPE / NO RATED RESTRAINT OR POWER-LOSS CONTAINMENT", -485, -275, 13, white)
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE_NEXT"
    scene.eevee.taa_render_samples = 16
    scene.render.resolution_x = 1600
    scene.render.resolution_y = 900
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "JPEG"
    scene.render.image_settings.quality = 90
    scene.render.filepath = str(HERE / "release" / f"Gen6_Feed_{state}_STEP_derived.jpg")
    scene.view_settings.view_transform = "AgX"
    bpy.ops.render.render(write_still=True)

for name in MANIFEST["states"]:
    render(name)
