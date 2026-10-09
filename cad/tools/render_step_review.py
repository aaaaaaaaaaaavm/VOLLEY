"""Render labeled JPEG review views from FreeCAD-tessellated STEP solids.

    /usr/bin/python3 cad/tools/export_step_view_meshes.py
    blender -b --factory-startup -P cad/tools/render_step_review.py -- \
        --mesh-manifest /tmp/volley-step-review-meshes/meshes.json

Blender adds lighting, materials, a floor and camera labels. It does not add
mechanical parts or alter the STEP-derived part geometry. Hidden enclosures and
cropped views are identified in each image's label and provenance record.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "cad/renders/step_review"

VIEWS = [
    dict(file="gen5_reference_open.jpg", config="gen5_reference", title="GEN5 / REFERENCE ASSEMBLY",
         status="STEP-DERIVED CAD  |  ENCLOSURE HIDDEN  |  SIDE-FED FIT FAILS",
         camera=(2650, -2450, 1600), target=(900, 0, 220), scale=3600,
         omit=("Enclosure",), meaning="Reference placement; track/cassette solids intersect."),
    dict(file="gen5_reference_closed.jpg", config="gen5_reference", title="GEN5 / CLOSED ENVELOPE",
         status="STEP-DERIVED CAD  |  REFERENCE ONLY  |  INTERNAL CLASH NOT VISIBLE",
         camera=(3100, -2900, 1750), target=(900, 0, 225), scale=3600,
         omit=(), meaning="External envelope view; the concealed side-fed fit failure remains."),
    dict(file="gen5_fit_plan.jpg", config="gen5_reference", title="GEN5 / SIDE-FED TOP VIEW",
         status="STEP-DERIVED CAD  |  ENCLOSURE + PAYLOADS HIDDEN  |  11 MM SHORTFALL",
         camera=(900, 0, 3000), target=(900, 0, 170), scale=2420,
         omit=("Enclosure", "Payload"), meaning="Top view of reference track and cassette placement; 11 mm width shortfall is from the exact-solid CAD audit."),
    dict(file="gen5_drive_detail.jpg", config="gen5_reference", title="GEN5 / DRIVE GEOMETRY",
         status="STEP-DERIVED CAD CROP  |  WINDING, CONTROL + HARDWARE UNSELECTED",
         camera=(1050, -1120, 780), target=(530, 0, 0), scale=1100,
         only=("Track", "Stator", "Sled"), meaning="Cropped visualization of the reference track, stator and sled; no switching or release-contact mechanism shown."),
    dict(file="r1_candidate_open.jpg", config="r1_candidate", title="R1 / FEEDER GEOMETRY CANDIDATE",
         status="STEP-DERIVED CAD  |  ENCLOSURE HIDDEN  |  ACTUATION UNDESIGNED",
         camera=(2650, -2550, 1650), target=(900, 0, 220), scale=3700,
         omit=("Wide_Enclosure_R1",), meaning="Separate widened 570 mm enclosure candidate; path screen only, not selected Gen5 hardware."),
    dict(file="r1_candidate_plan.jpg", config="r1_candidate", title="R1 / TOP VIEW",
         status="STEP-DERIVED CAD  |  ENCLOSURE + PAYLOADS HIDDEN  |  UNSELECTED",
         camera=(900, 0, 3000), target=(900, 0, 170), scale=2480,
         omit=("Wide_Enclosure_R1", "Payload"), meaning="Separate R1 candidate top view; scripted route clears but actuator, retention, tolerance and mass remain open."),
]

COLORS = {
    "Interface_ESPA": ((0.38, 0.60, 0.67, 1), 0.46, 0.38),
    "Track": ((0.70, 0.75, 0.79, 1), 0.68, 0.36),
    "Stator": ((0.85, 0.35, 0.17, 1), 0.55, 0.29),
    "Sled": ((0.19, 0.68, 0.79, 1), 0.51, 0.28),
    "Brake": ((0.91, 0.65, 0.23, 1), 0.56, 0.34),
    "Magazine": ((0.52, 0.59, 0.66, 1), 0.48, 0.42),
    "Open_Cassette": ((0.52, 0.59, 0.66, 1), 0.48, 0.42),
    "Payload": ((0.27, 0.80, 0.63, 1), 0.10, 0.39),
    "Enclosure": ((0.32, 0.44, 0.55, 1), 0.52, 0.46),
    "Wide_Enclosure": ((0.34, 0.48, 0.57, 1), 0.52, 0.46),
    "Lift_Guides": ((0.73, 0.56, 0.30, 1), 0.55, 0.35),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def material(name: str, color: tuple, metallic: float = 0.0, roughness: float = 0.5):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = color
    mat.use_nodes = True
    shader = mat.node_tree.nodes.get("Principled BSDF")
    shader.inputs["Base Color"].default_value = color
    shader.inputs["Metallic"].default_value = metallic
    shader.inputs["Roughness"].default_value = roughness
    return mat


def emission(name: str, color: tuple):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    output = nodes.new("ShaderNodeOutputMaterial")
    glow = nodes.new("ShaderNodeEmission")
    glow.inputs["Color"].default_value = color
    glow.inputs["Strength"].default_value = 1.0
    mat.node_tree.links.new(glow.outputs[0], output.inputs["Surface"])
    return mat


def clear() -> None:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for collection in (bpy.data.materials, bpy.data.meshes, bpy.data.cameras, bpy.data.lights):
        for block in list(collection):
            collection.remove(block)


def matches(instance: str, prefixes: tuple) -> bool:
    return any(instance.startswith(prefix) for prefix in prefixes)


def add_text(camera, body: str, x: float, y: float, size: float, mat) -> None:
    curve = bpy.data.curves.new(body[:16], type="FONT")
    curve.body = body
    curve.size = size
    curve.extrude = 0
    object_ = bpy.data.objects.new(body[:16], curve)
    bpy.context.collection.objects.link(object_)
    object_.parent = camera
    object_.location = (x, y, -150)
    object_.data.materials.append(mat)


def build(view: dict, manifest: dict, mesh_root: Path, engine: str, samples: int) -> dict:
    clear()
    technical_plan = "plan" in view["file"]
    entries = manifest["configurations"][view["config"]]["parts"]
    selected = []
    for item in entries:
        name = item["instance"]
        if matches(name, view.get("omit", ())) or ("only" in view and not matches(name, view["only"])):
            continue
        source = mesh_root / item["obj_file"]
        if sha256(source) != item["obj_sha256"]:
            raise RuntimeError(f"mesh changed after FreeCAD export: {source}")
        before = set(bpy.data.objects)
        # FreeCAD's OBJ writer emits Z-up coordinates. Blender's OBJ importer
        # otherwise assumes Y-up and rotates the complete assembly.
        bpy.ops.wm.obj_import(filepath=str(source), forward_axis="Y", up_axis="Z")
        added = [obj for obj in bpy.data.objects if obj not in before and obj.type == "MESH"]
        if len(added) != 1:
            raise RuntimeError(f"expected one mesh for {name}, got {len(added)}")
        obj = added[0]
        corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
        actual = [min(point.x for point in corners), max(point.x for point in corners),
                  min(point.y for point in corners), max(point.y for point in corners),
                  min(point.z for point in corners), max(point.z for point in corners)]
        expected = item["placed_bounds_mm"]
        if any(abs(a - e) > 1.5 for a, e in zip(actual, expected)):
            raise RuntimeError(f"Blender OBJ axes disagree with FreeCAD STEP bounds for {name}: {actual} vs {expected}")
        obj.name = name
        role = next((key for key in COLORS if name.startswith(key)), "Track")
        color, metal, rough = COLORS[role]
        obj.data.materials.clear()
        obj.data.materials.append(emission(name, color) if technical_plan
                                  else material(name, color, metal, rough))
        selected.append(name)

    if not technical_plan:
        bpy.ops.mesh.primitive_cube_add(size=1, location=(900, 0, -292))
        floor = bpy.context.object
        floor.name = "Presentation floor — not CAD"
        floor.scale = (4300, 2300, 55)
        floor.data.materials.append(material("Floor", (0.025, 0.052, 0.076, 1), 0.0, 0.77))
    world = bpy.data.worlds.new("Studio world")
    bpy.context.scene.world = world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.025, 0.045, 0.07, 1)
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.65
    for label, rotation, power, tint in (() if technical_plan else (
        ("Key", (math.radians(38), 0, math.radians(30)), 3.0, (0.80, 0.90, 1.0)),
        ("Fill", (math.radians(58), 0, math.radians(-115)), 1.8, (0.53, 0.75, 1.0)),
        ("Rim", (math.radians(32), 0, math.radians(165)), 2.4, (1.0, 0.72, 0.46)),
    )):
        bpy.ops.object.light_add(type="SUN", rotation=rotation)
        light = bpy.context.object
        light.name = label
        light.data.energy = power
        light.data.color = tint
        light.data.angle = math.radians(5)
    bpy.ops.object.camera_add(location=view["camera"])
    camera = bpy.context.object
    camera.name = "Review camera"
    direction = Vector(view["target"]) - camera.location
    camera.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    camera.data.type = "ORTHO"
    camera.data.ortho_scale = view["scale"]
    camera.data.clip_start = 1
    camera.data.clip_end = 100000
    scene = bpy.context.scene
    scene.camera = camera
    aspect = scene.render.resolution_x / scene.render.resolution_y
    half_height = view["scale"] / (2 * aspect)
    left = -view["scale"] / 2 + view["scale"] * 0.055
    bpy.ops.mesh.primitive_plane_add(size=2)
    banner = bpy.context.object
    banner.name = "Evidence label plate — not CAD"
    banner.parent = camera
    banner.location = (0, -half_height + view["scale"] * 0.048, -160)
    banner.scale = (view["scale"] / 2, view["scale"] * 0.054, 1)
    banner.data.materials.append(emission("Label plate", (0.025, 0.055, 0.075, 1)))
    add_text(camera, view["title"], left, half_height - view["scale"] * 0.06, view["scale"] * 0.023,
             emission("Label white", (0.91, 0.96, 0.99, 1)))
    add_text(camera, view["status"], left, -half_height + view["scale"] * 0.05, view["scale"] * 0.015,
             emission("Limit teal", (0.44, 0.85, 0.84, 1)))
    scene.render.engine = engine
    if engine == "CYCLES":
        scene.cycles.device = "CPU"
        scene.cycles.samples = 1 if technical_plan else samples
        # The packaged headless Blender build has no OpenImageDenoise support.
        scene.cycles.use_denoising = False
    scene.render.resolution_x = 1800
    scene.render.resolution_y = 1012
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "JPEG"
    scene.render.image_settings.quality = 94
    scene.render.image_settings.color_mode = "RGB"
    scene.render.film_transparent = False
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = "AgX - Medium High Contrast"
    OUTPUT.mkdir(parents=True, exist_ok=True)
    target = OUTPUT / view["file"]
    scene.render.filepath = str(target)
    bpy.ops.render.render(write_still=True)
    return {"file": str(target.relative_to(ROOT)), "sha256": sha256(target),
            "configuration": view["config"], "included_instances": selected,
            "omitted_instance_prefixes": list(view.get("omit", ())),
            "only_instance_prefixes": list(view.get("only", ())),
            "meaning_and_limit": view["meaning"], "title_on_image": view["title"],
            "status_on_image": view["status"]}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mesh-manifest", type=Path, required=True)
    parser.add_argument("--view", help="render only one named JPEG while checking the layout")
    parser.add_argument("--engine", choices=("CYCLES", "BLENDER_EEVEE_NEXT"), default="CYCLES")
    parser.add_argument("--samples", type=int, default=64)
    args = parser.parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])
    mesh_path = args.mesh_manifest.resolve()
    manifest = json.loads(mesh_path.read_text())
    views = [v for v in VIEWS if not args.view or v["file"] == args.view]
    if not views:
        parser.error("view name not found")
    output = [build(view, manifest, mesh_path.parent, args.engine, args.samples) for view in views]
    if not args.view:
        provenance = {"evidence_class": "STEP-derived FreeCAD/Blender visualization, not measured hardware",
                      "exporter": "cad/tools/export_step_view_meshes.py",
                      "renderer": "cad/tools/render_step_review.py",
                      "blender_engine": args.engine, "cycles_samples": args.samples if args.engine == "CYCLES" else None,
                      "freecad_source": {key: {"native_document": value["native_document"],
                                                "native_document_sha256": value["native_document_sha256"],
                                                "source_steps": sorted({p["source_step"]: p["source_step_sha256"]
                                                                        for p in value["parts"]}.items())}
                                         for key, value in manifest["configurations"].items()},
                      "views": output}
        (OUTPUT / "PROVENANCE.json").write_text(json.dumps(provenance, indent=2) + "\n")
    elif (OUTPUT / "PROVENANCE.json").is_file():
        saved = OUTPUT / "PROVENANCE.json"
        provenance = json.loads(saved.read_text())
        provenance["views"] = [output[0] if item["file"] == output[0]["file"] else item
                               for item in provenance["views"]]
        saved.write_text(json.dumps(provenance, indent=2) + "\n")
    for entry in output:
        print(f"wrote {entry['file']} ({len(entry['included_instances'])} STEP instances)", flush=True)


if __name__ == "__main__":
    main()
