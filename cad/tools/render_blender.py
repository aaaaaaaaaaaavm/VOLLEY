"""Render the Gen5 STL set with Blender. Run headless:

    blender -b -P cad/tools/render_blender.py -- [--samples N] [--quick]

WHY THIS EXISTS
---------------
OpenSCAD's preview renderer is flat-shaded, single-colour and unlit, which is fine for a
geometry check and useless for looking at. This takes the same committed meshes and renders
them with materials and lighting so the mechanism can actually be read.

IT ADDS NO GEOMETRY. Both Gen5 models are geometry-and-interface models: no fillets, no
fasteners, no harness routing, no tolerancing, and parameters.json carries no tolerances to
give them. A renderer cannot show detail the model does not have, and this one does not try.
"""
import math
import os
import sys

import bpy

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STL = os.path.join(ROOT, "cad", "stl")
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
GEN = (argv[argv.index("--gen") + 1] if "--gen" in argv else "gen5")
OUT = os.path.join(ROOT, "cad", "renders", GEN)
SAMPLES = int(argv[argv.index("--samples") + 1]) if "--samples" in argv else 96
QUICK = "--quick" in argv

# name -> (stl file, base colour RGB, metallic, roughness)
PARTS = {
    "Interface_ESPA":    ("VOLLEY_Interface_ESPA_Gen5.stl",    (0.62, 0.64, 0.67), 1.0, 0.42),
    "Track":             ("VOLLEY_Track_Gen5.stl",             (0.55, 0.57, 0.60), 1.0, 0.48),
    "Stator":            ("VOLLEY_Stator_Gen5.stl",            (0.72, 0.34, 0.16), 1.0, 0.30),
    "Sled":              ("VOLLEY_Sled_Gen5.stl",              (0.70, 0.72, 0.75), 1.0, 0.28),
    "Magazine_Cassette": ("VOLLEY_Magazine_Cassette_Gen5.stl", (0.50, 0.52, 0.56), 1.0, 0.52),
    "Brake":             ("VOLLEY_Brake_Gen5.stl",             (0.26, 0.27, 0.30), 1.0, 0.35),
    "Payload_3U":        ("VOLLEY_Payload_3U_Gen5.stl",        (0.16, 0.30, 0.22), 0.2, 0.60),
    "Enclosure":         ("VOLLEY_Enclosure_Gen5.stl",         (0.74, 0.75, 0.77), 0.6, 0.38),
}

MECHANISM = ["Interface_ESPA", "Track", "Stator", "Sled", "Magazine_Cassette", "Brake"]

VIEWS = [
    # name, visible parts, camera location, look-at, lens
    ("hero_open",   MECHANISM,              (-1500, -2400, 1250), (900, 0, 60),  50),
    ("three_quarter", MECHANISM,            (2900, -2100, 1100),  (950, 0, 40),  55),
    ("side",        MECHANISM,              (900, -3600, 260),    (900, 0, 120), 60),
    ("breech",      MECHANISM,              (-1350, -900, 620),   (250, 0, 60),  50),
    ("sled_detail", ["Sled", "Track", "Stator"], (-350, -1500, 780), (420, 0, 0), 55),
    ("closed",      list(PARTS),            (-1700, -2800, 1500), (900, 0, 250), 50),
    # Exploded. Offsets are presentation only -- they displace the STLs the other views
    # import at their assembled positions, and nothing downstream reads them.
    # The drive stack taken apart, in the order it assembles: track, stator, sled, payload.
    # The ESPA ring, cassette and brake are left out deliberately -- they sit beside the
    # stack rather than in it, and including them reads as scattered parts, not an explode.
    ("exploded", [("Track", (0, 0, 0)),
                  ("Stator", (0, 0, 300)),
                  ("Sled", (0, 0, 620)),
                  ("Payload_3U", (0, 0, 900))],
     (-1350, -2500, 1500), (830, 0, 430), 52),
]


# Gen6: ADR-032. No mover, no stator, no bank, no brake. A rail a spent stage provides,
# a pre-charged chamber, and a carriage that is not recovered.
PARTS_GEN6 = {
    "Stage_Rail":        ("VOLLEY_Stage_Rail_Gen6.stl",        (0.48, 0.50, 0.54), 1.0, 0.55),
    "Drive_Tube":        ("VOLLEY_Drive_Tube_Gen6.stl",         (0.66, 0.68, 0.72), 1.0, 0.34),
    "Trim_Stator":       ("VOLLEY_Trim_Stator_Gen6.stl",        (0.72, 0.34, 0.16), 1.0, 0.30),
    "Carriage":          ("VOLLEY_Carriage_Gen6.stl",           (0.72, 0.74, 0.77), 1.0, 0.26),
    "Chamber":           ("VOLLEY_Chamber_Gen6.stl",            (0.55, 0.32, 0.20), 1.0, 0.32),
    "Reservoir":         ("VOLLEY_Reservoir_Gen6.stl",          (0.30, 0.42, 0.52), 1.0, 0.30),
    "Magazine_Cassette": ("VOLLEY_Magazine_Cassette_Gen6.stl",  (0.50, 0.52, 0.56), 1.0, 0.52),
}

# ADR-034 took the stroke from 2.18 m to 8.0 m, so the assembly spans x -190..8100 and the
# framing that suited a 2.18 m machine puts it off both edges. These distances are set from the
# 8.2 m extent: a 50 mm lens on a 36 mm sensor needs about 11.4 m of standoff to contain it.
# The aspect ratio is roughly 42:1 and the renders look like it. That is the machine.
VIEWS_GEN6 = [
    ("hero_open", list(PARTS_GEN6), (-3400, -8800, 3300), (3350, 0, -320), 50),
    ("three_quarter", list(PARTS_GEN6), (12000, -10000, 4000), (4000, 0, 0), 55),
    ("side", list(PARTS_GEN6), (4000, -16000, 700), (4000, 0, 0), 60),
    ("store", ["Chamber", "Reservoir", "Drive_Tube"], (-900, -1700, 700), (250, 0, 0), 55),
]

GEN3 = {"Assembly": ("EMOCD_Assembly_Gen3.stl", (0.60, 0.62, 0.66), 1.0, 0.40)}
VIEWS_GEN3 = [
    ("hero_open", ["Assembly"], (-1500, -2400, 1250), (900, 0, 60), 50),
    ("three_quarter", ["Assembly"], (2900, -2100, 1100), (950, 0, 40), 55),
]

GROUND_SIZE, GROUND_AT = 9000, (900, 0, -300)

if GEN == "gen6":
    PARTS, VIEWS, MECHANISM = PARTS_GEN6, VIEWS_GEN6, list(PARTS_GEN6)
    GROUND_SIZE, GROUND_AT = 26000, (4000, 0, -400)
elif GEN == "gen3":
    PARTS, VIEWS, MECHANISM = GEN3, VIEWS_GEN3, list(GEN3)


def clear():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
    for block in (bpy.data.meshes, bpy.data.materials, bpy.data.lights, bpy.data.cameras):
        for b in list(block):
            block.remove(b)


def import_stl(path):
    before = set(bpy.data.objects)
    if hasattr(bpy.ops.wm, "stl_import"):
        bpy.ops.wm.stl_import(filepath=path)
    else:
        bpy.ops.import_mesh.stl(filepath=path)
    return list(set(bpy.data.objects) - before)


def material(name, rgb, metallic, rough):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1.0)
    b.inputs["Metallic"].default_value = metallic
    b.inputs["Roughness"].default_value = rough
    return m


def look_at(obj, target):
    import mathutils
    d = mathutils.Vector(target) - obj.location
    obj.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()


def build_scene(parts):
    """Import each named part.

    A parts entry is either a name, or a (name, (dx, dy, dz)) pair that displaces the part
    from its assembled position. A bare name means zero offset, so every view written before
    exploded views existed behaves exactly as it did.
    """
    clear()
    for entry in parts:
        name, offset = entry if isinstance(entry, tuple) else (entry, (0.0, 0.0, 0.0))
        fn, rgb, met, rough = PARTS[name]
        p = os.path.join(STL, fn)
        if not os.path.exists(p):
            continue
        mat = material(name, rgb, met, rough)
        for o in import_stl(p):
            o.name = name
            o.location = (o.location[0] + offset[0],
                          o.location[1] + offset[1],
                          o.location[2] + offset[2])
            o.data.materials.clear()
            o.data.materials.append(mat)
            o.data.use_auto_smooth = False
            for poly in o.data.polygons:
                poly.use_smooth = False

    # A floor, kept small enough to read as a plinth rather than a horizon. It has to track
    # the machine's length: at Gen6's 8.2 m the old 9000-unit plinth ended under the midpoint.
    bpy.ops.mesh.primitive_plane_add(size=GROUND_SIZE, location=GROUND_AT)
    ground = bpy.context.object
    ground.data.materials.append(material("Ground", (0.32, 0.33, 0.35), 0.0, 0.9))

    # World: a bright neutral dome, so metal has something to reflect. This is most of
    # the light in the scene; the suns below only shape it.
    w = bpy.data.worlds.new("W")
    bpy.context.scene.world = w
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = (0.42, 0.45, 0.50, 1)
    w.node_tree.nodes["Background"].inputs[1].default_value = 1.0

    # SUN lamps, not area lamps. A sun's irradiance does not fall off with distance, which
    # matters here because the scene is 1800 units across and an inverse-square area light
    # placed to frame it arrives essentially black.
    for rot, energy, name in (
        ((math.radians(52), 0, math.radians(38)), 4.0, "key"),
        ((math.radians(64), 0, math.radians(-115)), 1.6, "fill"),
        ((math.radians(28), 0, math.radians(190)), 2.2, "rim"),
    ):
        bpy.ops.object.light_add(type="SUN", rotation=rot)
        L = bpy.context.object
        L.name = name
        L.data.energy = energy
        L.data.angle = math.radians(6)


def render(view):
    name, parts, cam_loc, target, lens = view
    build_scene(parts)
    bpy.ops.object.camera_add(location=cam_loc)
    cam = bpy.context.object
    cam.data.lens = lens
    # The machine is ~1800 units long and framed from 2-4000 away. Blender's default
    # clip_end is 100, which puts the whole scene behind the far plane and renders a
    # frame of pure world background -- which looks exactly like a lighting failure.
    cam.data.clip_start = 10.0
    cam.data.clip_end = 200000.0
    look_at(cam, target)
    sc = bpy.context.scene
    sc.camera = cam
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = 48 if QUICK else SAMPLES
    sc.cycles.use_denoising = False
    sc.cycles.max_bounces = 4
    sc.render.resolution_x = 1000 if QUICK else 1600
    sc.render.resolution_y = 640 if QUICK else 1000
    sc.render.film_transparent = False
    sc.view_settings.look = "AgX - Medium High Contrast"
    os.makedirs(OUT, exist_ok=True)
    sc.render.filepath = os.path.join(OUT, name + ".png")
    bpy.context.view_layer.update()
    import mathutils
    from bpy_extras.object_utils import world_to_camera_view
    meshes = [o for o in bpy.data.objects if o.type == "MESH" and o.name != "Plane"]
    pts = [o.matrix_world @ mathutils.Vector(c) for o in meshes for c in o.bound_box]
    if pts:
        n = [world_to_camera_view(sc, cam, q) for q in pts]
        print(f"  [{name}] {len(meshes)} meshes, ndc x "
              f"{min(q.x for q in n):.2f}..{max(q.x for q in n):.2f} y "
              f"{min(q.y for q in n):.2f}..{max(q.y for q in n):.2f} depth "
              f"{min(q.z for q in n):.0f}..{max(q.z for q in n):.0f}")
    else:
        print(f"  [{name}] NO MESHES IN SCENE")
    bpy.ops.render.render(write_still=True)
    print(f"  wrote {name}.png")


for v in VIEWS:
    render(v)
print("done")
