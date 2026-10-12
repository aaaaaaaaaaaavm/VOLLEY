#!/usr/bin/env python3
"""Build two native FreeCAD Gen6 first-article envelope candidates and STEP sets.

Run: PYTHONPATH=/usr/lib/freecad-python3/lib /usr/bin/python3 cad/gen6_first_article/build.py

The boxes are editable FreeCAD Part primitives, with assembly groups and STEP
exports. Drive, brake, restraint and payload contact are envelope placeholders.
Their solid volume is intentionally excluded from the partial material mass.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import FreeCAD as App
import Part

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
PARAMETERS = HERE / "parameters.json"
OUT = HERE / "release"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def box(doc, group, name, length, width, height, origin, material=None, role="solid"):
    obj = doc.addObject("Part::Box", name)
    obj.Label = name.replace("_", " ")
    obj.Length = length
    obj.Width = width
    obj.Height = height
    obj.Placement.Base = App.Vector(*origin)
    obj.addProperty("App::PropertyString", "EvidenceRole", "VOLLEY")
    obj.EvidenceRole = role
    obj.addProperty("App::PropertyString", "MaterialProxy", "VOLLEY")
    obj.MaterialProxy = material or "UNRATED_ENVELOPE"
    group.addObject(obj)
    return obj


def geometry(doc, kind, p):
    fixed = doc.addObject("App::Part", "FixedStructure")
    mover = doc.addObject("App::Part", "CapturedCarrier")
    spacecraft = doc.addObject("App::Part", "SpacecraftSurrogate")
    conceptual = doc.addObject("App::Part", "UnratedEnvelopes")
    al = "aluminium_proxy"
    # Open ladder frame; the host mounting plate and fasteners are unresolved.
    parts = []
    for side, y in (("Left", -80), ("Right", 60)):
        parts.append(box(doc, fixed, f"Frame_{side}", 1800, 20, 18, (0, y, 0), al))
    for i, x in enumerate((0, 400, 800, 1200, 1600, 1780)):
        parts.append(box(doc, fixed, f"Crossmember_{i+1}", 20, 120, 18, (x, -60, 0), al))
    length = p["guide_end"] - p["guide_start"]
    # 110 mm nominal corridor around 100 mm payload; lips touch its lower face.
    half = p["guide_inner_half_width"]
    for side, y in (("Left", -half-10), ("Right", half)):
        parts.append(box(doc, fixed, f"Guide_{side}", length, 10, 52,
                         (p["guide_start"], y, 18), al))
    for side, y in (("Left", -half), ("Right", 45)):
        parts.append(box(doc, fixed, f"Support_Lip_{side}", length, half-45, 8,
                         (p["guide_start"], y, 40), al, "CONTACT_SURFACE_PROXY"))
    carrier = box(doc, mover, "Carrier_Al_Chassis", 60, 80, 18, (100, -40, 30), al)
    pusher = box(doc, mover, "Carrier_Pusher_Face", 10, 88, 90, (160, -44, 48), al,
                 "CONTACT_FACE_PROXY")
    if kind == "A":
        secondary = box(doc, mover, "PM_Armature_Proxy", 40, 80, 4,
                        (110, -40, 26), "ndfeb_proxy", "MAGNET_ENVELOPE_NOT_ARRAY_DESIGN")
    else:
        secondary = box(doc, mover, "Copper_Armature_Proxy", 40, 80, 4,
                        (110, -40, 26), "copper_proxy", "PLATE_ENVELOPE_NOT_INDUCTION_DESIGN")
    payload = box(doc, spacecraft, "Passive_3U_Dummy_Envelope", p["payload_length_3u"],
                  100, 100, (170, -50, 48), None, "4_KG_ASSIGNED_INERT_SURROGATE")
    stator = box(doc, conceptual, "Primary_Drive_Envelope", 1300, 80, 6,
                 (150, -40, 18), None, "NO_WINDING_OR_MASS_RATING")
    brake = box(doc, conceptual, "Carrier_Brake_Envelope", 200, 80, 6,
                (1450, -40, 18), None, "NO_BRAKE_FORCE_OR_HEAT_RATING")
    doc.recompute()
    objects = parts + [carrier, pusher, secondary, payload, stator, brake]
    if any(obj.Shape.isNull() or not obj.Shape.isValid() for obj in objects):
        raise AssertionError("invalid FreeCAD solid")
    return fixed, mover, spacecraft, conceptual, objects


def metrics(kind, p, objects):
    fixed = [obj for obj in objects if obj.Name.startswith(("Frame_", "Crossmember_", "Guide_", "Support_Lip_"))]
    moving = [obj for obj in objects if obj.Name.startswith(("Carrier_", "PM_Armature", "Copper_Armature"))
              and obj.Name != "Carrier_Brake_Envelope"]
    payload = next(obj for obj in objects if obj.Name.startswith("Passive_3U"))
    stator = next(obj for obj in objects if obj.Name == "Primary_Drive_Envelope")
    brake = next(obj for obj in objects if obj.Name == "Carrier_Brake_Envelope")
    static = fixed + [stator, brake]
    sampled = []
    for offset in (0, 325, 650, 975, 1300):
        bodies = []
        for obj in moving + [payload]:
            moved = obj.Shape.copy()
            moved.translate(App.Vector(offset, 0, 0))
            bodies.append((obj.Name, moved))
        maximum = 0.0
        for name, shape in bodies:
            for obstacle in static:
                maximum = max(maximum, shape.common(obstacle.Shape).Volume)
        # Face-to-face pusher contact may have zero intersection volume.
        carrier_payload = max(bodies[i][1].common(bodies[-1][1]).Volume
                              for i in range(len(bodies)-1))
        maximum = max(maximum, carrier_payload)
        sampled.append(dict(stroke_offset_mm=offset, maximum_solid_intersection_mm3=maximum))
    if any(row["maximum_solid_intersection_mm3"] > 1e-5 for row in sampled):
        raise AssertionError(f"{kind}: scripted path has solid interference")
    densities = p["materials_density_kg_mm3"]
    rows = []
    for obj in fixed + moving:
        rows.append(dict(part=obj.Name, material_proxy=obj.MaterialProxy,
                         volume_mm3=obj.Shape.Volume,
                         mass_kg=obj.Shape.Volume * densities[obj.MaterialProxy]))
    partial_mass = sum(row["mass_kg"] for row in rows)
    mover_mass = sum(row["mass_kg"] for row in rows if row["part"] in [x.Name for x in moving])
    return dict(candidate=kind, source_status="PARAMETRIC_FREECAD_ENVELOPE_NOT_DESIGN_RELEASE",
                cross_section=dict(payload_width_mm=p["payload_width"],
                                   guide_inner_width_mm=2*p["guide_inner_half_width"],
                                   nominal_each_side_gap_mm=p["guide_inner_half_width"]-p["payload_width"]/2,
                                   armature_to_primary_vertical_gap_mm=2),
                motion=dict(stroke_mm=1300, sampled_solid_intersections=sampled,
                            contact_dynamics_and_thermal_deflection="UNMODELED"),
                partial_material_mass=dict(fixed_and_carrier_kg=partial_mass,
                                           captured_carrier_kg=mover_mass,
                                           parts=rows,
                                           excluded="payload 4 kg; all primary windings, inverter, source, real brake, restraint, bearings, controls, harness, mounting, shielding and thermal hardware"))


def build():
    p = json.loads(PARAMETERS.read_text())
    OUT.mkdir(exist_ok=True)
    result = dict(evidence_class="GEN6_G1_UNSELECTED_FIRST_ARTICLE_GEOMETRY_SCREEN",
                  source_sha256=sha(Path(__file__)), parameters_sha256=sha(PARAMETERS),
                  freecad_version=".".join(App.Version()[:3]), candidates={})
    for kind in ("A", "B"):
        doc = App.newDocument(f"Gen6_G1_{kind}")
        fixed, mover, spacecraft, conceptual, objects = geometry(doc, kind, p)
        report = metrics(kind, p, objects)
        native = OUT / f"Gen6_G1_{kind}_Envelope.FCStd"
        step = OUT / f"Gen6_G1_{kind}_Envelope.step"
        doc.saveAs(str(native))
        Part.export(objects, str(step))
        reimport = Part.Shape()
        reimport.read(str(step))
        original = sum(obj.Shape.Volume for obj in objects)
        if abs(reimport.Volume-original) > 1e-3:
            raise AssertionError("STEP read-back volume disagrees with FreeCAD assembly")
        report["export"] = dict(native=native.name, native_sha256=sha(native),
                                step=step.name, step_sha256=sha(step),
                                readback_total_volume_mm3=reimport.Volume,
                                original_total_volume_mm3=original)
        result["candidates"][kind] = report
        App.closeDocument(doc.Name)
    result["exclusions"] = ["A 3U inert dummy is a geometry proxy, not a qualified payload interface",
                            "Neither candidate has a selected motor, winding, source or brake hardware",
                            "Only five stroke stations and static B-rep intersections are checked",
                            "No launch loads, tolerance stack, contact dynamics, magnetic exposure or failure containment",
                            "Partial material mass is not installed mass or the P130 30 kg assumption"]
    (OUT / "Gen6_G1_Envelope_Report.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({kind: {"partial_kg": round(d["partial_material_mass"]["fixed_and_carrier_kg"], 3),
                             "carrier_kg": round(d["partial_material_mass"]["captured_carrier_kg"], 3)}
                      for kind, d in result["candidates"].items()}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    args = parser.parse_args()
    build()


if __name__ == "__main__":
    main()
