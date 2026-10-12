#!/usr/bin/env python3
"""FreeCAD nominal B-rep screen of an unselected, one-cell Gen6 feeder.

Run with system Python and PYTHONPATH=/usr/lib/freecad-python3/lib.
Solids are editable Part primitives, not production sketches or rated hardware.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import FreeCAD as App
import Part

HERE = Path(__file__).resolve().parent
OUT = HERE / "release"
PARAMETERS = HERE / "parameters.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def box(doc, group, name, size, origin, role):
    obj = doc.addObject("Part::Box", name)
    obj.Label = name.replace("_", " ")
    obj.Length, obj.Width, obj.Height = size
    obj.Placement.Base = App.Vector(*origin)
    obj.addProperty("App::PropertyString", "EvidenceRole", "VOLLEY")
    obj.EvidenceRole = role
    group.addObject(obj)
    return obj


def make_state(name, state, p):
    doc = App.newDocument("Gen6_Feed_" + name)
    cassette = doc.addObject("App::Part", "FixedCassette")
    moving = doc.addObject("App::Part", "FeederMovingProxies")
    carrier = doc.addObject("App::Part", "CradleAndRail")
    surrogate = doc.addObject("App::Part", "InertSpacecraftEnvelope")
    length = p["length_mm"]
    px = p["payload_x_mm"]
    z = p["payload_z_mm"]
    advance = state["payload_advance_mm"]
    lift = p["gate_lift_mm"] if state["gate_open"] else 0
    # Spacecraft bottom touches a floor proxy at z=48; no contact force is inferred.
    payload = box(doc, surrogate, "Passive_3U_Box", (length, 100, 100),
                  (px, p["cassette_payload_y_mm"] + advance, z), "INERT_ENVELOPE_NO_APPROVED_CONTACT")
    # Fixed floor and bridge: same height, no vertical free-fall assumption.
    fixed = [
        box(doc, cassette, "Cassette_Floor", (length, 125, 10), (px, -265, 38), "FLOOR_PROXY"),
        box(doc, cassette, "Transfer_Bridge", (length, 85, 10), (px, -140, 38), "BRIDGE_PROXY"),
        box(doc, cassette, "Cassette_Back_Wall", (length, 5, 100), (px, -280, 48), "RESTRAINT_ENVELOPE_ONLY"),
        box(doc, cassette, "End_Stop_Front", (5, 225, 100), (px-10, -265, 48), "UNRATED_STOP"),
        box(doc, cassette, "End_Stop_Aft", (5, 225, 100), (px+length+5, -265, 48), "UNRATED_STOP"),
        box(doc, carrier, "Cradle_Floor", (length, 110, 10), (px, -55, 38), "CRADLE_CONTACT_PROXY"),
        box(doc, carrier, "Cradle_Right_Guide", (length, 5, 50), (px, 55, 48), "GUIDE_PROXY"),
    ]
    gate = box(doc, moving, "Cassette_Gate", (length, 5, 100),
               (px, -145, 48+lift), "UNRATED_MOVING_BARRIER")
    left_guide = box(doc, moving, "Cradle_Left_Guide", (length, 5, 50),
                     (px, -60, 48+lift), "UNRATED_MOVING_GUIDE")
    pusher_y = -260 if state["pusher_withdrawn"] else -260 + advance
    pusher = box(doc, moving, "Captured_Pusher_Face", (length, 10, 100),
                 (px, pusher_y, 48), "LEAD_SCREW_PUSHER_ENVELOPE_NO_DRIVE")
    doc.recompute()
    objects = fixed + [gate, left_guide, pusher, payload]
    if any(o.Shape.isNull() or not o.Shape.isValid() for o in objects):
        raise AssertionError(name + ": invalid solid")
    # Gate and left guide are moving obstacles, except their touch with floor.
    checks = []
    for actor in (payload, pusher):
        for obstacle in fixed + [gate, left_guide]:
            overlap = actor.Shape.common(obstacle.Shape).Volume
            checks.append({"actor": actor.Name, "obstacle": obstacle.Name,
                           "intersection_mm3": round(overlap, 6)})
            if overlap > 1e-5:
                raise AssertionError(f"{name}: {actor.Name} intersects {obstacle.Name}: {overlap}")
    # Intended zero-volume contact at the pusher face is not a force calculation.
    pusher_payload_overlap = pusher.Shape.common(payload.Shape).Volume
    if pusher_payload_overlap > 1e-5:
        raise AssertionError(name + ": pusher penetrates payload")
    sweep = None
    if name == "01_transfer_armed":
        # Sample the nominal transfer every 2.5 mm, including both endpoints.
        # This is a sampled B-rep check, not a continuous swept-volume proof.
        worst = 0.0
        worst_station = 0.0
        for station in range(81):
            offset = p["feeder_travel_mm"] * station / 80
            for source in (payload, pusher):
                shape = source.Shape.copy()
                shape.translate(App.Vector(0, offset, 0))
                for obstacle in fixed + [gate, left_guide]:
                    overlap = shape.common(obstacle.Shape).Volume
                    if overlap > worst:
                        worst, worst_station = overlap, offset
        if worst > 1e-5:
            raise AssertionError(f"nominal transfer intersects at {worst_station} mm: {worst} mm3")
        sweep = {"stations": 81, "increment_mm": 2.5,
                 "max_solid_intersection_mm3": worst,
                 "continuous_swept_volume_proven": False}
    native = OUT / f"Gen6_Feed_{name}.FCStd"
    step = OUT / f"Gen6_Feed_{name}.step"
    doc.saveAs(str(native))
    Part.export(objects, str(step))
    imported = Part.Shape()
    imported.read(str(step))
    original_volume = sum(o.Shape.Volume for o in objects)
    if abs(imported.Volume-original_volume) > 0.01:
        raise AssertionError(name + ": STEP readback volume differs")
    result = {
        "state": name,
        "payload_advance_mm": advance,
        "gate_open": state["gate_open"],
        "pusher_withdrawn": state["pusher_withdrawn"],
        "checks": checks,
        "max_payload_obstacle_intersection_mm3": max(x["intersection_mm3"] for x in checks if x["actor"] == payload.Name),
        "pusher_payload_intersection_mm3": pusher_payload_overlap,
        "sampled_transfer_sweep": sweep,
        "original_total_volume_mm3": original_volume,
        "step_readback_volume_mm3": imported.Volume,
        "native_file": native.name, "native_sha256": sha256(native),
        "step_file": step.name, "step_sha256": sha256(step),
    }
    App.closeDocument(doc.Name)
    return result


def main():
    p = json.loads(PARAMETERS.read_text())
    OUT.mkdir(exist_ok=True)
    report = {
        "evidence_class": p["evidence_class"],
        "freecad_version": ".".join(App.Version()[:3]),
        "source_sha256": sha256(Path(__file__)),
        "parameters_sha256": sha256(PARAMETERS),
        "nominal_end_stop_gap_mm": p["nominal_end_stop_gap_mm"],
        "nominal_cradle_side_gap_mm": p["nominal_cradle_side_gap_mm"],
        "states": [make_state(name, state, p) for name, state in p["states"].items()],
        "limitations": [
            "Nominal exact-solid screen only; no tolerance or continuous swept-solid result",
            "No launch-rated individual restraint or power-loss containment at mid-transfer",
            "No selected screw, actuator, bearing, gate return, latch, sensor or interlock",
            "No contact force, payload face approval, jam torque, debris or environmental test",
            "No four-cell 1U/3U architecture, installed mass or provider interface",
        ],
    }
    path = OUT / "Gen6_Feed_One_Cell_Report.json"
    path.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"states": len(report["states"]),
                      "maximum_nominal_overlap_mm3": max(s["max_payload_obstacle_intersection_mm3"] for s in report["states"])}))


if __name__ == "__main__":
    main()
