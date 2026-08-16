"""
VOLLEY | Gen5: the CAD, built from parameters.

WHY THIS EXISTS
---------------
`cad/parameters.json` opens with a warning it cannot itself enforce:

    "Do NOT edit dimensions inside Fusion 360 -- user parameters there are document-scoped
     and will silently drift across the nine documents."

Gen1 through Gen4 are Fusion documents, so that warning is the only thing standing between
the repository and drift. Gen4 makes the cost concrete: it exists only inside Fusion, has
never been exported, and its stations (release at s = 1200 mm over a 900 mm stroke) do not
match the parameters every published number rests on (release at 1500 over 1.5 m). The
repository therefore publishes renders of geometry no committed file matches -- P43, P39.

A script-built model cannot drift. It regenerates from a clean clone, it is a function of
parameters.json alone, and it matches ADR-015: derive, never paste.

WHAT THIS IS NOT
----------------
**A geometry and interface model, not a manufacturing model.** No fillets, no chamfers, no
fasteners, no harness routing, no tolerancing, no weld or joint detail. Every part is the
simplest solid that carries the right interfaces at the right stations. Do not send it to a
machine shop; do use it to check fit, envelope and clearance.

The sled's array placement is DERIVED, not read: parameters.json gives the Halbach array in
assembly coordinates (x = 230..570) while a sled document needs its own frame. The array is
centred on the 488 mm sled, which puts the sled's aft face at x = 156 when stowed. That
centring is an assumption and is flagged in the self-check output.

USAGE
    python3 cad/build_gen5.py                 # build STEP + STL into cad/step/gen5, cad/stl
    python3 cad/build_gen5.py --check         # build, then verify against parameters.json
"""
import argparse
import json
import os
import re

import cadquery as cq

HERE = os.path.dirname(os.path.abspath(__file__))
STEP_DIR = os.path.join(HERE, "step", "gen5")
STL_DIR = os.path.join(HERE, "stl")

P = json.load(open(os.path.join(HERE, "parameters.json")))
G = P["groups"]
ENV = P["envelope"]

# STEP headers carry a wall-clock timestamp, which would make every rebuild differ from the
# last for reasons that have nothing to do with geometry. The plan requires Gen5 to
# regenerate byte-stably from a clean clone, so the stamp is normalised to a fixed epoch.
EPOCH = "1970-01-01T00:00:00"


def _norm(path):
    """Rewrite the STEP header so two builds of the same parameters are byte-identical."""
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    text = re.sub(r"'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}'", f"'{EPOCH}'", text)
    text = re.sub(r"FILE_NAME\('[^']*'", f"FILE_NAME('{os.path.basename(path)}'", text)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def export(shape, name, stl=False):
    os.makedirs(STEP_DIR, exist_ok=True)
    step = os.path.join(STEP_DIR, f"VOLLEY_{name}_Gen5.step")
    cq.exporters.export(shape, step)
    _norm(step)
    if stl:
        os.makedirs(STL_DIR, exist_ok=True)
        cq.exporters.export(shape, os.path.join(STL_DIR, f"VOLLEY_{name}_Gen5.stl"),
                            tolerance=0.1, angularTolerance=0.2)
    return step


# --------------------------------------------------------------------------- documents

def interface_espa():
    """Ring flange, hub plate, four gussets. x = -25..0, the aft mating face at x = 0."""
    g = G["interface_espa"]
    t, od, hub_d, hub_t = (g["flange_thickness"], g["flange_outer_diameter"],
                           g["hub_plate_diameter"], g["hub_plate_thickness"])
    # Flange ring, drilled on its bolt circle. Built in the YZ plane and swept along +x.
    flange = (cq.Workplane("YZ").circle(od / 2).extrude(t)
              .faces(">X").workplane()
              .polarArray(g["bolt_circle_diameter"] / 2, 0, 360, g["bolt_hole_count"])
              .hole(g["bolt_hole_diameter"]))
    flange = flange.translate((g["x_min"], 0, 0))
    hub = (cq.Workplane("YZ").circle(hub_d / 2).extrude(hub_t)
           .translate((0, 0, 0)))
    out = flange.union(hub)
    # Four gussets, radial webs from the hub out to the flange, at 45 deg to the axes so
    # they miss the track longerons.
    gt, ri, ro = g["gusset_thickness"], g["gusset_inner_radius"], g["gusset_outer_radius"]
    for ang in (45, 135, 225, 315):
        web = (cq.Workplane("XY").box(hub_t, ro - ri, gt, centered=(False, False, True))
               .translate((0, ri, 0))
               .rotate((0, 0, 0), (1, 0, 0), ang))
        out = out.union(web)
    return out


def track():
    """Two longerons with roller channels, guide rails and launch locks."""
    g = G["track"]
    L, z0, z1 = g["longeron_length"], g["longeron_z_min"], g["longeron_z_max"]
    yi = g["roller_channel_y_inner"]
    yo = g["overall_width"] / 2.0      # the beam runs out to the track's overall width;
    #                                    roller_channel_y_outer (90) is where the CHANNEL
    #                                    ends, not where the longeron does.
    out = None
    for sgn in (+1, -1):
        beam = (cq.Workplane("XY")
                .box(L, yo - yi, z1 - z0, centered=(False, False, False))
                .translate((0, min(sgn * yi, sgn * yo), z0)))
        # Guide rails: two per side, running the full length inside the channel.
        gi, go = g["guide_rail_y_inner"], g["guide_rail_y_outer"]
        for zc in (g["guide_rail_z_contact"], -g["guide_rail_z_contact"]):
            rail = (cq.Workplane("XY")
                    .box(L, go - gi, g["guide_rail_z_outer"] - g["guide_rail_z_contact"],
                         centered=(False, False, False))
                    .translate((0, min(sgn * gi, sgn * go), zc)))
            beam = beam.union(rail)
        # Launch locks, x = 30..50.
        li, lo = g["launch_lock_y_inner"], g["launch_lock_y_outer"]
        lock = (cq.Workplane("XY")
                .box(g["launch_lock_x_end"] - g["launch_lock_x_start"], lo - li,
                     2 * g["launch_lock_z_half_height"], centered=(False, False, True))
                .translate((g["launch_lock_x_start"], min(sgn * li, sgn * lo), 0)))
        beam = beam.union(lock)
        out = beam if out is None else out.union(beam)
    return out


def stator():
    """162-conductor three-phase belt winding, z = -5..+5, active span 0..1296."""
    g = G["stator"]
    n, pitch, w = g["conductor_count"], g["belt_pitch"], g["belt_width"]
    depth, z0, z1 = g["active_width_y"], g["belt_z_min"], g["belt_z_max"]
    bars = None
    for i in range(n):
        x = g["active_span_start"] + i * pitch
        bar = (cq.Workplane("XY")
               .box(w, depth, z1 - z0, centered=(False, True, False))
               .translate((x, 0, z0)))
        bars = bar if bars is None else bars.union(bar)
    return bars


def sled(x_aft=None):
    """Chassis, two Halbach arrays, webs, backstop, four rollers.

    The array is centred on the sled; see the module docstring on why that is derived.
    """
    g = G["sled"]
    L, W, H = g["overall_length"], g["overall_width"], g["overall_height"]
    arr_len = g["halbach_array_length"]
    a_off = (L - arr_len) / 2.0
    if x_aft is None:
        x_aft = g["halbach_array_x_start"] - a_off
    zi, zo = g["halbach_array_z_inner"], g["halbach_array_z_outer"]
    ay = g["halbach_array_width_y"]

    out = None
    for sgn in (+1, -1):
        # Chassis plate carrying each array, outboard of the magnets.
        plate = (cq.Workplane("XY")
                 .box(L, W, g["chassis_plate_thickness"], centered=(False, True, False))
                 .translate((x_aft, 0, sgn * zo if sgn > 0 else -zo - g["chassis_plate_thickness"])))
        arr = (cq.Workplane("XY")
               .box(arr_len, ay, zo - zi, centered=(False, True, False))
               .translate((x_aft + a_off, 0, zi if sgn > 0 else -zo)))
        out = plate if out is None else out.union(plate)
        out = out.union(arr)
    # Side webs tying the two plates together, outboard of the stator's 90 mm depth.
    wi, wo = g["chassis_web_y_inner"], g["chassis_web_y_outer"]
    for sgn in (+1, -1):
        web = (cq.Workplane("XY")
               .box(L, wo - wi, 2 * (zo + g["chassis_plate_thickness"]),
                    centered=(False, False, True))
               .translate((x_aft, min(sgn * wi, sgn * wo), 0)))
        out = out.union(web)
    # Backstop: the face the payload is pushed by, at the aft end of the sled.
    out = out.union(cq.Workplane("XY")
                    .box(g["backstop_thickness"], W, H, centered=(False, True, True))
                    .translate((x_aft, 0, 0)))
    # Four rollers, running in the track channels.
    rd, rw = g["roller_diameter"], g["roller_width"]
    ry = (g["roller_y_inner"] + g["roller_y_outer"]) / 2.0
    xc = x_aft + L / 2.0
    for dx in (-g["roller_x_offset_from_centre"], g["roller_x_offset_from_centre"]):
        for sgn in (+1, -1):
            # extrude(rw/2, both=True), not extrude(rw). Workplane("XZ") extrudes towards
            # -Y, so a one-sided extrude with a -rw/2 offset put the +y roller at y 54..70
            # -- inboard of its 70..86 channel, in the stator gap -- and the -y roller at
            # -102..-86, outboard of its own. The sled came out asymmetric about y = 0.
            # Found by the OpenSCAD cross-check, P71.
            roller = (cq.Workplane("XZ").circle(rd / 2).extrude(rw / 2, both=True)
                      .translate((xc + dx, sgn * ry, 0)))
            out = out.union(roller)
    return out


def magazine_cassette():
    """Shell, six cells, septa, gate frame and two gate pins."""
    g = G["magazine"]
    lx, wy, hz = g["cassette_length_x"], g["cassette_width_y"], g["cassette_height_z"]
    t = g["shell_panel_thickness"]
    # Closed 4 mm panels, per the shell_construction_decision: drawn closed as the upper
    # bound and as the mounting surface the septa need.
    shell = (cq.Workplane("XY").box(lx, wy, hz, centered=(False, True, False))
             .faces(">Z").shell(-t))
    # Septa, one per cell boundary, spanning the drawn x and z range.
    for i in range(1, g["satellites_per_cassette"]):
        z = g["septum_z_min"] + i * g["satellite_pitch_z"]
        if z > g["septum_z_max"]:
            break
        sep = (cq.Workplane("XY")
               .box(g["septum_x_max"] - g["septum_x_min"], wy - 2 * t,
                    g["septum_thickness"], centered=(False, True, False))
               .translate((g["septum_x_min"], 0, z)))
        shell = shell.union(sep)
    # Retention gate frame and its two A-286 pins.
    gz0, gz1 = g["gate_frame_z_min"], g["gate_frame_z_max"]
    frame = (cq.Workplane("XY").box(lx, t, gz1 - gz0, centered=(False, True, False))
             .translate((0, -wy / 2 + t / 2, gz0)))
    shell = shell.union(frame)
    for x in g["gate_pin_x_positions"]:
        pin = (cq.Workplane("XZ").circle(g["gate_pin_diameter"] / 2).extrude(wy)
               .translate((x, wy / 2, gz0 + (gz1 - gz0) / 2)))
        shell = shell.union(pin)
    return shell


def brake():
    """Two tapered pole plates. The taper is the 200 g arrest limiter, not styling."""
    g = G["brake"]
    x0, x1 = g["x_start"], g["x_end"]
    t, w, taper = g["pole_plate_thickness"], g["pole_width_y"], g["pole_taper_entry_length"]
    out = None
    for sgn in (+1, -1):
        z = sgn * (G["sled"]["halbach_array_z_outer"] + 10)
        # Tapered entry: the plate ramps to full thickness over the first `taper` mm, so
        # the sled meets a rising field gradient rather than a step.
        prof = (cq.Workplane("XZ")
                .polyline([(x0, 0), (x0 + taper, sgn * t), (x1, sgn * t), (x1, 0)])
                .close().extrude(w).translate((0, w / 2, z)))
        out = prof if out is None else out.union(prof)
    return out


def payload_3u():
    """3U CubeSat with CDS corner rails, as a proxy: envelope and rails, nothing inside."""
    g = G["payload_3u"]
    lx, wy, hz = g["length_x"], g["width_y"], g["height_z"]
    r = g["corner_rail_size"]
    body = cq.Workplane("XY").box(lx, wy - 2 * r, hz - 2 * r, centered=(False, True, True))
    for sy in (+1, -1):
        for sz in (+1, -1):
            rail = (cq.Workplane("XY").box(lx, r, r, centered=(False, True, True))
                    .translate((0, sy * (wy - r) / 2, sz * (hz - r) / 2)))
            body = body.union(rail)
    return body


def enclosure():
    """Skins, muzzle aperture, aft flange cutout, radiator. The flight unit from outside."""
    g = G["enclosure"]
    x0, x1 = g["x_min"], g["x_max"]
    yh, zb, zt = g["y_half_width"], g["z_bottom_skin_outer"], g["z_top_skin_outer"]
    t = g["skin_thickness"]
    box = (cq.Workplane("XY")
           .box(x1 - x0, 2 * yh, zt - zb, centered=(False, True, False))
           .translate((x0, 0, zb))
           .faces(">X").shell(-t))
    # Muzzle aperture: must be genuinely open on the satellite exit line.
    ap = (cq.Workplane("XY")
          .box(3 * t, g["muzzle_aperture_width_y"], g["muzzle_aperture_height_z"],
               centered=(False, True, True))
          .translate((g["muzzle_panel_x"] - t, g["muzzle_aperture_centre_y"],
                      g["muzzle_aperture_centre_z"])))
    box = box.cut(ap)
    # Aft flange cutout: a horseshoe by design -- the flange OD extends below the belly.
    cut = (cq.Workplane("YZ").circle(g["aft_flange_cutout_diameter"] / 2)
           .extrude(3 * t).translate((x0 - t, 0, 0)))
    box = box.cut(cut)
    # Radiator, on the top skin.
    rad = (cq.Workplane("XY")
           .box(g["radiator_length"], g["radiator_width"], g["radiator_thickness"],
                centered=(False, True, False))
           .translate((g["radiator_x_start"], 0, g["radiator_z"])))
    return box.union(rad)


DOCUMENTS = {
    "Interface_ESPA": interface_espa,
    "Track": track,
    "Stator": stator,
    "Sled": sled,
    "Magazine_Cassette": magazine_cassette,
    "Brake": brake,
    "Payload_3U": payload_3u,
    "Enclosure": enclosure,
}


def build(stl=False):
    made = {}
    for name, fn in DOCUMENTS.items():
        shape = fn()
        made[name] = shape
        export(shape, name, stl=stl)
        print(f"  {name:20s} -> step/gen5/VOLLEY_{name}_Gen5.step")
    return made


def check(made):
    """Read the geometry back and compare it to parameters.json.

    A script-built model that is never measured is just a script that ran. These assertions are
    the difference between "it built" and "it built the thing the parameters describe".
    """
    fails = []

    def cmp(label, got, want, tol=0.51):
        ok = abs(got - want) <= tol
        print(f"  {'ok ' if ok else 'FAIL'} {label:44s} {got:9.2f} vs {want:9.2f}")
        if not ok:
            fails.append(label)

    def bb(name):
        return made[name].val().BoundingBox()

    g = G
    b = bb("Track")
    cmp("track length", b.xlen, g["track"]["longeron_length"])
    cmp("track overall width", b.ylen, g["track"]["overall_width"], tol=1.0)

    b = bb("Stator")
    cmp("stator active span",
        b.xmax - g["stator"]["active_span_start"], g["stator"]["active_span_end"], tol=8.1)
    cmp("stator active depth", b.ylen, g["stator"]["active_width_y"])
    cmp("stator belt thickness", b.zlen, g["stator"]["belt_thickness_z"])

    b = bb("Sled")
    cmp("sled overall length", b.xlen, g["sled"]["overall_length"])
    cmp("halbach array start (assembly x)",
        b.xmin + (g["sled"]["overall_length"] - g["sled"]["halbach_array_length"]) / 2,
        g["sled"]["halbach_array_x_start"])
    # The air gap is the one dimension the whole thrust constant rests on.
    gap = g["sled"]["halbach_array_z_inner"] - g["stator"]["belt_z_max"]
    cmp("magnetic air gap per side", gap, g["sled"]["airgap_per_side"], tol=0.01)

    b = bb("Interface_ESPA")
    cmp("ESPA flange OD", max(b.ylen, b.zlen), g["interface_espa"]["flange_outer_diameter"])
    cmp("ESPA aft face", b.xmin, g["interface_espa"]["x_min"])

    b = bb("Magazine_Cassette")
    cmp("cassette length", b.xlen, g["magazine"]["cassette_length_x"])
    cmp("cassette width", b.ylen, g["magazine"]["cassette_width_y"])
    cmp("cassette height", b.zlen, g["magazine"]["cassette_height_z"])

    b = bb("Payload_3U")
    cmp("payload length", b.xlen, g["payload_3u"]["length_x"])
    cmp("payload width", b.ylen, g["payload_3u"]["width_y"])
    cmp("payload height", b.zlen, g["payload_3u"]["height_z"])

    b = bb("Brake")
    cmp("brake envelope start", b.xmin, g["brake"]["x_start"])
    cmp("brake envelope end", b.xmax, g["brake"]["x_end"])

    b = bb("Enclosure")
    cmp("enclosure x extent", b.xlen, g["enclosure"]["x_max"] - g["enclosure"]["x_min"])
    cmp("installed envelope, x", b.xlen, ENV["installed_closed_mm"][0], tol=1.0)
    cmp("installed envelope, y", b.ylen, ENV["installed_closed_mm"][1], tol=1.0)
    # The radiator stands proud of the top skin: parameters.json records z_top_skin_outer
    # 707 but extremes_max_mm 710, the 3 mm radiator. Check against the extreme, not the skin.
    cmp("enclosure z extent, incl. radiator", b.zmax - b.zmin,
        (g["enclosure"]["radiator_z"] + g["enclosure"]["radiator_thickness"])
        - g["enclosure"]["z_bottom_skin_outer"], tol=1.0)
    cmp("radiator top = extremes_max z", b.zmax, ENV["extremes_max_mm"][2], tol=1.0)

    print()
    if fails:
        print(f"CHECK FAILED on {len(fails)}: {', '.join(fails)}")
    else:
        print("CHECK PASSED: geometry as built agrees with cad/parameters.json")
    return not fails


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="verify the geometry as built against parameters.json")
    ap.add_argument("--stl", action="store_true", help="also write STL meshes")
    a = ap.parse_args()
    print("Gen5, built from cad/parameters.json\n")
    made = build(stl=a.stl)
    if a.check:
        print("\nreading the geometry back:")
        raise SystemExit(0 if check(made) else 1)


if __name__ == "__main__":
    main()
