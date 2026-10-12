#!/usr/bin/env python3
"""Build and audit an unselected one-cell Gen6 track/feed integration revision.

This script checks nominal B-rep interference. It does not define a launch-rated
restraint, transfer actuator, feeder selection, or provider interface.
Run with PYTHONPATH=/usr/lib/freecad-python3/lib /usr/bin/python3.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import FreeCAD as App
import Part

HERE = Path(__file__).resolve().parent
CAD = HERE.parent
OUT = HERE / "release"
ARTICLE = CAD / "gen6_first_article/release/Gen6_G1_A_Envelope.FCStd"
FEED = CAD / "gen6_feeder/parameters.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def add_box(doc, group, name, size, origin, role):
    obj = doc.addObject("Part::Box", name)
    obj.Length, obj.Width, obj.Height = size
    obj.Placement.Base = App.Vector(*origin)
    obj.addProperty("App::PropertyString", "EvidenceRole", "VOLLEY")
    obj.EvidenceRole = role
    group.addObject(obj)
    return obj


def make_state(state_name, advance, open_gate, p):
    original = App.openDocument(str(ARTICLE))
    doc = App.newDocument("Gen6_Integrated_R1_" + state_name)
    fixed = doc.addObject("App::Part", "FixedStructure")
    moving = doc.addObject("App::Part", "CapturedMovingProxies")
    spacecraft = doc.addObject("App::Part", "InertSpacecraft")
    envelopes = doc.addObject("App::Part", "UnratedEnvelopes")
    parts = []
    omitted = {"Guide_Left", "Passive_3U_Dummy_Envelope"}
    for old in original.Objects:
        if old.TypeId != "Part::Box" or old.Name in omitted:
            continue
        role = getattr(old, "EvidenceRole", "UNRATED_PROXY")
        if old.Name.startswith(("Carrier_", "PM_Armature")):
            group = moving
        elif old.Name.endswith("Envelope"):
            group = envelopes
        else:
            group = fixed
        xyz = old.Placement.Base
        parts.append(add_box(doc, group, old.Name,
                             (old.Length.Value, old.Width.Value, old.Height.Value),
                             (xyz.x, xyz.y, xyz.z), role))
    App.closeDocument(original.Name)
    length = p["length_mm"]
    px = p["payload_x_mm"]
    bottom = p["payload_z_mm"]
    # The left guide is split around the transfer window. Its middle segment
    # lifts 140 mm, fully above the 100 mm payload proxy during transfer.
    guide_gap_end = px + length
    parts += [
        add_box(doc, fixed, "Guide_Left_Before_Window", (px - 100, 10, 52), (100, -65, 18), "GUIDE_PROXY"),
        add_box(doc, fixed, "Guide_Left_After_Window", (1700 - guide_gap_end, 10, 52),
                (guide_gap_end, -65, 18), "GUIDE_PROXY"),
        add_box(doc, moving, "Guide_Left_Lifting_Window", (length, 10, 52),
                (px, -65, 18 + (140 if open_gate else 0)), "UNRATED_RETRACTABLE_GUIDE"),
        add_box(doc, fixed, "Cassette_Floor", (length, 125, 10), (px, -265, 38), "FLOOR_PROXY"),
        # Stop bridge at the outside of the left guide. The 10 mm open gap
        # needs a separate contact/deflection analysis before any hardware use.
        add_box(doc, fixed, "Transfer_Bridge_R1", (length, 75, 10), (px, -140, 38), "GAP_BRIDGE_PROXY"),
        add_box(doc, fixed, "Cassette_Back_Wall", (length, 5, 100), (px, -280, 48), "RESTRAINT_ENVELOPE_ONLY"),
        # Restrict end stops to the cassette region so they do not occupy the
        # carrier pusher or launch guide. Actual retention remains unresolved.
        add_box(doc, fixed, "End_Stop_Front_R1", (5, 125, 100), (px - 10, -265, 48), "UNRATED_STOP"),
        add_box(doc, fixed, "End_Stop_Aft_R1", (5, 125, 100), (px + length + 5, -265, 48), "UNRATED_STOP"),
        add_box(doc, moving, "Cassette_Gate", (length, 5, 100),
                (px, -145, 48 + (120 if open_gate else 0)), "UNRATED_MOVING_BARRIER"),
    ]
    feeder_pusher = add_box(doc, moving, "Captured_Feeder_Pusher", (length, 10, 100),
                            (px, -260 if advance == 200 else -260 + advance, 48),
                            "PUSHER_FACE_NO_DRIVE")
    parts.append(feeder_pusher)
    payload = add_box(doc, spacecraft, "Passive_3U_Box", (length, 100, 100),
                      (px, -250 + advance, bottom), "INERT_ENVELOPE_NO_APPROVED_CONTACT")
    parts.append(payload)
    doc.recompute()
    if any(x.Shape.isNull() or not x.Shape.isValid() for x in parts):
        raise AssertionError(state_name + ": invalid solid")
    overlaps = []
    for i, a in enumerate(parts):
        for b in parts[i + 1:]:
            if not a.Shape.BoundBox.intersect(b.Shape.BoundBox):
                continue
            volume = a.Shape.common(b.Shape).Volume
            if volume > 1e-4:
                overlaps.append({"part_a": a.Name, "part_b": b.Name,
                                 "intersection_mm3": round(volume, 6)})
    if overlaps:
        raise AssertionError(state_name + ": solid interference: " + json.dumps(overlaps))
    sweep = None
    if state_name == "01_transfer_armed":
        obstacles = [x for x in parts if x not in (payload, feeder_pusher)]
        maximum = 0.0
        for station in range(81):
            dy = 200 * station / 80
            for actor in (payload, feeder_pusher):
                shape = actor.Shape.copy()
                shape.translate(App.Vector(0, dy, 0))
                for obstacle in obstacles:
                    if shape.BoundBox.intersect(obstacle.Shape.BoundBox):
                        maximum = max(maximum, shape.common(obstacle.Shape).Volume)
        if maximum > 1e-4:
            raise AssertionError("sampled transfer interference " + str(maximum))
        sweep = {"stations": 81, "increment_mm": 2.5,
                 "maximum_intersection_mm3": round(maximum, 6),
                 "continuous_sweep_or_tolerance_proven": False}
    native = OUT / ("Gen6_Integrated_R1_" + state_name + ".FCStd")
    step = OUT / ("Gen6_Integrated_R1_" + state_name + ".step")
    doc.saveAs(str(native))
    Part.export(parts, str(step))
    imported = Part.Shape()
    imported.read(str(step))
    volume = sum(x.Shape.Volume for x in parts)
    if abs(imported.Volume - volume) > 0.01:
        raise AssertionError("STEP readback volume mismatch")
    result = {"state": state_name, "part_count": len(parts), "overlaps": overlaps,
              "sampled_transfer_sweep": sweep, "source_total_volume_mm3": volume,
              "step_readback_volume_mm3": imported.Volume,
              "native": native.name, "native_sha256": sha(native),
              "step": step.name, "step_sha256": sha(step)}
    App.closeDocument(doc.Name)
    return result


def main():
    OUT.mkdir(exist_ok=True)
    p = json.loads(FEED.read_text())
    states = [
        ("00_stowed", 0, False),
        ("01_transfer_armed", 0, True),
        ("02_mid_transfer", 100, True),
        ("03_seated", 200, False),
    ]
    report = {"status": "UNSELECTED_NOMINAL_ONE_CELL_INTEGRATION_SCREEN",
              "freecad_version": ".".join(App.Version()[:3]),
              "source_sha256": sha(Path(__file__)),
              "first_article_native_sha256": sha(ARTICLE),
              "feeder_parameters_sha256": sha(FEED),
              "corrections": ["split and lift 340.5 mm of left guide during transfer",
                              "end transfer bridge before guide corridor",
                              "shorten cassette end stops outside carrier path",
                              "use one payload/cradle/guide set in combined assembly"],
              "states": [make_state(*x, p) for x in states],
              "open": ["full four-cell 1U/3U layout", "mechanical launch restraints",
                       "positive mid-transfer containment", "bridge-gap contact/deflection",
                       "actuators and guide alignment", "manufacturing tolerances",
                       "continuous swept solids", "loads, thermal, wear and faults",
                       "mass/CG/inertia reconciliation", "host mounting and provider ICD"]}
    (OUT / "Gen6_Integrated_R1_Report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"states": len(report["states"]), "parts_each": report["states"][0]["part_count"]}))


if __name__ == "__main__":
    main()
