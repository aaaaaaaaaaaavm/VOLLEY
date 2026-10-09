"""Unselected R1 side-feed/lift packaging candidate; does not change Gen5 baseline.

Builds actual STEP solids and exact-solid motion screens for twelve 3U envelope
proxies. It establishes a clear geometric route after widening the enclosure;
it does not design actuation, launch retention or a qualified payload interface.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import cadquery as cq
import numpy as np

import build_gen5 as bg

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "step/feeder_candidate_r1"
RESULT = ROOT / "FEEDER_CANDIDATE_R1.json"
REPORT = ROOT / "FEEDER_CANDIDATE_R1.md"
PARAM = json.loads((ROOT / "parameters.json").read_text())["groups"]
ENCLOSURE_WIDTH = 570.0  # mm, selected only for the R1 screen
TRACK_CLEARANCE = 5.0   # mm per cassette at the track sides


def export(shape, name):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"VOLLEY_{name}_R1.step"
    cq.exporters.export(shape, str(path))
    text = path.read_text()
    text = re.sub(r"'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}'", "'1970-01-01T00:00:00'", text)
    text = re.sub(r"FILE_NAME\('[^']*'", f"FILE_NAME('{path.name}'", text)
    path.write_text(text)
    readback = cq.importers.importStep(str(path))
    if not readback.val().isValid() or abs(readback.val().Volume() - shape.val().Volume()) > .01:
        raise RuntimeError(f"invalid STEP round-trip: {path.name}")
    return path


def open_cassette(inner_side: int):
    """Six fixed cells with inner side apertures, no flight retention gate."""
    g = PARAM["magazine"]
    length, width, height = g["cassette_length_x"], g["cassette_width_y"], g["cassette_height_z"]
    skin = g["shell_panel_thickness"]
    box = cq.Workplane("XY").box(length, width, height, centered=(False, True, False)).faces(">Z").shell(-skin)
    for i in range(1, 6):
        # Leave clearance above the lower payload and below the upper one.
        z = g["septum_z_min"] + i * g["satellite_pitch_z"] - 2.5
        shelf = (cq.Workplane("XY").box(350, width - 2 * skin, g["septum_thickness"],
                                         centered=(False, True, False)).translate((25, 0, z)))
        box = box.union(shelf)
    y_cut = -84 if inner_side < 0 else 77
    for i in range(6):
        z = g["septum_z_min"] + i * g["satellite_pitch_z"]
        aperture = (cq.Workplane("XY").box(347, 7, 104, centered=(False, False, False))
                    .translate((17, y_cut, z - 2)))
        box = box.cut(aperture)
    return box


def guides():
    """Central vertical lift guide envelope outside the 3U x/y sweep."""
    out = None
    for x in (205, 565):
        for y in (-60, 55):
            post = cq.Workplane("XY").box(10, 5, 630, centered=(False, False, False)).translate((x, y, 22))
            out = post if out is None else out.union(post)
    return out


def wide_enclosure():
    prior = bg.G["enclosure"]["y_half_width"]
    try:
        bg.G["enclosure"]["y_half_width"] = ENCLOSURE_WIDTH / 2
        return bg.enclosure()
    finally:
        bg.G["enclosure"]["y_half_width"] = prior


def possible_intersection(a, b):
    aa, bb = a.val().BoundingBox(), b.val().BoundingBox()
    return (aa.xmin < bb.xmax and bb.xmin < aa.xmax and aa.ymin < bb.ymax and bb.ymin < aa.ymax
            and aa.zmin < bb.zmax and bb.zmin < aa.zmax)


def overlap(a, b):
    return a.intersect(b).val().Volume() if possible_intersection(a, b) else 0.0


def envelope(x0, x1, y0, y1, z0, z1):
    return (cq.Workplane("XY").box(x1-x0, y1-y0, z1-z0,
                                    centered=(False, False, False)).translate((x0, y0, z0)))


def build():
    g = PARAM
    track = cq.importers.importStep(str(ROOT / "step/gen5/VOLLEY_Track_Gen5.step"))
    stator = cq.importers.importStep(str(ROOT / "step/gen5/VOLLEY_Stator_Gen5.step"))
    sled = cq.importers.importStep(str(ROOT / "step/gen5/VOLLEY_Sled_Gen5.step"))
    payload = cq.importers.importStep(str(ROOT / "step/gen5/VOLLEY_Payload_3U_Gen5.step"))
    old_enclosure = cq.importers.importStep(str(ROOT / "step/gen5/VOLLEY_Enclosure_Gen5.step"))
    enclosure = wide_enclosure()
    lift = guides()
    cassette = {1: open_cassette(-1), -1: open_cassette(1)}
    y_abs = g["track"]["overall_width"] / 2 + TRACK_CLEARANCE + g["magazine"]["cassette_width_y"] / 2
    cas = {side: cassette[side].translate((200, side * y_abs, 0)) for side in (1, -1)}
    internal_half = ENCLOSURE_WIDTH / 2 - g["enclosure"]["skin_thickness"]
    static = dict(track_cassette_mm3={str(side): overlap(track, cas[side]) for side in (1, -1)},
                  cassette_enclosure_mm3={str(side): overlap(cas[side], enclosure) for side in (1, -1)},
                  track_lift_mm3=overlap(track, lift), sled_lift_mm3=overlap(sled, lift),
                  cassette_outer_clearance_mm=internal_half - (y_abs + g["magazine"]["cassette_width_y"] / 2))
    routes = []
    for side in (1, -1):
        for i in range(6):
            z0 = g["magazine"]["septum_z_min"] + i * g["magazine"]["satellite_pitch_z"]
            samples = []
            for y in np.linspace(side * y_abs, 0, 9):
                samples.append((float(y), float(z0)))
            for z in np.linspace(z0, g["magazine"]["septum_z_min"], max(2, i * 4 + 1))[1:]:
                samples.append((0.0, float(z)))
            worst = dict(cassette=0.0, opposite_cassette=0.0, track=0.0, stator=0.0,
                         sled=0.0, enclosure=0.0, lift=0.0)
            stationary_parts = (("cassette", cas[side]), ("opposite_cassette", cas[-side]),
                                ("track", track), ("stator", stator), ("sled", sled),
                                ("enclosure", enclosure), ("lift", lift))
            for y, z in samples:
                pose = payload.translate((220, y, z + 50))
                for name, stationary in stationary_parts:
                    worst[name] = max(worst[name], overlap(pose, stationary))
            horizontal = envelope(220, 560.5, min(0,side*y_abs)-50,
                                  max(0,side*y_abs)+50, z0, z0+100)
            vertical = envelope(220, 560.5, -50, 50,
                                g["magazine"]["septum_z_min"], z0+100)
            swept = {name: max(overlap(horizontal, part), overlap(vertical, part))
                     for name, part in stationary_parts}
            routes.append(dict(side="P" if side == 1 else "S", cell=i+1,
                               source_center_y_mm=side * y_abs, source_bottom_z_mm=z0,
                               horizontal_then_vertical_samples=len(samples), maximum_intersection_mm3=worst,
                               conservative_swept_envelope_intersection_mm3=swept,
                               clear=all(v < .01 for v in worst.values()) and all(v < .01 for v in swept.values())))
    files = {}
    for name, shape in (("Wide_Enclosure", enclosure), ("Open_Cassette_P", cassette[1]),
                        ("Open_Cassette_S", cassette[-1]), ("Lift_Guides", lift)):
        p = export(shape, name)
        files[p.name] = hashlib.sha256(p.read_bytes()).hexdigest()
    asm = cq.Assembly(name="VOLLEY_R1_UNSELECTED_FEEDER_GEOMETRY")
    for name in ("Interface_ESPA", "Track", "Stator", "Sled", "Brake"):
        asm.add(cq.importers.importStep(str(ROOT / f"step/gen5/VOLLEY_{name}_Gen5.step")), name=name)
    asm.add(enclosure, name="Wide_Enclosure_R1")
    asm.add(lift, name="Lift_Guides_R1")
    for side in (1, -1):
        label = "P" if side == 1 else "S"
        asm.add(cas[side], name=f"Open_Cassette_{label}_R1")
        for i in range(6):
            z = g["magazine"]["septum_z_min"] + i * g["magazine"]["satellite_pitch_z"] + 50
            asm.add(payload.translate((220, side * y_abs, z)), name=f"Payload_{label}{i+1:02d}")
    assembly = OUT / "VOLLEY_Feeder_Assembly_R1.step"
    asm.save(str(assembly), exportType="STEP")
    text = assembly.read_text()
    text = re.sub(r"'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}'", "'1970-01-01T00:00:00'", text)
    text = re.sub(r"FILE_NAME\('[^']*'", f"FILE_NAME('{assembly.name}'", text)
    assembly.write_text(text)
    valid = cq.importers.importStep(str(assembly)).val().isValid()
    files[assembly.name] = hashlib.sha256(assembly.read_bytes()).hexdigest()
    mass_proxy = (enclosure.val().Volume() - old_enclosure.val().Volume()) * 2.7e-6
    d = dict(status="UNSELECTED_R1_GEOMETRY_SCREEN_NOT_FLIGHT_DESIGN", parameter_sha256=hashlib.sha256((ROOT / "parameters.json").read_bytes()).hexdigest(),
             external_width_mm=ENCLOSURE_WIDTH, previous_width_mm=530, internal_width_mm=2*internal_half,
             cassette_centers_y_mm=[-y_abs,y_abs], cassette_to_track_clearance_mm=TRACK_CLEARANCE,
             static=static, routes=routes, all_routes_clear=all(r["clear"] for r in routes),
             enclosure_added_skin_mass_proxy_kg=mass_proxy,
             step_files_sha256=files, step_assembly_readback_valid=valid,
             unresolved=["no actuator, lift carriage or motor package", "no launch retention gate or load path",
                         "no fastener/harness/thermal/tolerance clearance", "no provider ICD or named payload",
                         "larger enclosure invalidates Gen5 mass, structural and host envelopes",
             "rigid swept-envelope screen excludes dynamics, elastic deflection and fault cases"])
    return d


def main():
    d = build()
    RESULT.write_text(json.dumps(d, indent=2) + "\n")
    fails = [r for r in d["routes"] if not r["clear"]]
    REPORT.write_text("\n".join([
        "# R1 feeder geometry candidate — unselected", "",
        "**This is a separate geometry experiment, not a change to the evaluated Gen5 inputs or an accepted feeder.**",
        "It retains the eight Gen5 source parts except the enclosure and cassettes, which are modeled",
        "as new STEP parts. The 3U proxies translate from six side cells into a central vertical",
        "lift corridor, then descend to the first release height. The supports are conceptual guides;",
        "actuation and launch retention are not designed.", "",
        f"External width grows from 530 to {ENCLOSURE_WIDTH:.0f} mm, giving",
        f"{d['static']['cassette_outer_clearance_mm']:.1f} mm cassette-to-inner-skin clearance",
        f"and {TRACK_CLEARANCE:.1f} mm cassette-to-track clearance per side.",
        f"Exact static track/cassette overlap is {d['static']['track_cassette_mm3']} mm³.",
        f"The simple aluminium-skin mass increment is {d['enclosure_added_skin_mass_proxy_kg']:.2f} kg,",
        "not a revised installed-system mass. The new enclosure also changes host accommodation.", "",
        f"Sampled routes clear: {len(d['routes'])-len(fails)} / {len(d['routes'])}.",
        "Each axis-aligned horizontal and vertical translation also clears a conservative full",
        "340.5 × 100 × 100 mm swept box against the listed fixed parts. This does not include",
        "tolerances, the moving lift/gripper, dynamics, cycle life, safety or launch loads.", "",
        "![R1 geometry section](../figures/gen5_feeder_candidate_r1.png)", "",
        "This is a parameter-derived section, not a CAD GUI or solver screenshot. The native",
        "FreeCAD review document is `cad/native/Feeder_Candidate_R1.FCStd`; its 21 named",
        "instances and FreeCAD-exported assembly STEP have read-back and interference results in",
        "`cad/FREECAD_FEEDER_R1.json`. Imported B-reps have no native feature histories.", "",
        "## Open design gates", "", *[f"- {x}" for x in d["unresolved"]], "",
        "The STEP part and assembly exports, hashes and every collision result are in",
        "`cad/FEEDER_CANDIDATE_R1.json`. The source is `cad/build_feeder_candidate_r1.py`.", "",
    ]))
    print(f"R1 candidate: {len(d['routes'])-len(fails)}/{len(d['routes'])} routes clear; static overlaps {d['static']['track_cassette_mm3']}; assembly STEP valid={d['step_assembly_readback_valid']}")


if __name__ == "__main__":
    main()
