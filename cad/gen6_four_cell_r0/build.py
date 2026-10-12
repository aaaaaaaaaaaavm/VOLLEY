#!/usr/bin/env python3
"""Four-cell mixed-size packaging screen; FreeCAD solids, not a feeder release.

Run with PYTHONPATH=/usr/lib/freecad-python3/lib /usr/bin/python3.
The source first-article rail is reused as a geometric boundary. The four
independent cell mechanisms and host accommodation are not yet designed.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import FreeCAD as App
import Part

HERE = Path(__file__).resolve().parent
OUT = HERE / "release"
SOURCE = HERE.parent / "gen6_first_article/parameters.json"
CELLS = (
    ("A_3U", 170.0, 340.5, -1),
    ("B_3U", 550.0, 340.5, 1),
    ("C_1U", 960.0, 113.5, -1),
    ("D_1U", 1120.0, 113.5, 1),
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def box(doc, group, name, dims, pos, role):
    obj = doc.addObject("Part::Box", name)
    obj.Length, obj.Width, obj.Height = dims
    obj.Placement.Base = App.Vector(*pos)
    obj.addProperty("App::PropertyString", "EvidenceRole", "VOLLEY")
    obj.EvidenceRole = role
    group.addObject(obj)
    return obj


def add_guides(doc, fixed, movable, active):
    parts = []
    for side in (-1, 1):
        y = -65 if side < 0 else 55
        cursor = 100.0
        for name, x, length, cell_side in CELLS:
            if side != cell_side:
                continue
            if x > cursor:
                parts.append(box(doc, fixed, f"Guide_{side}_Before_{name}",
                                 (x-cursor, 10, 52), (cursor, y, 18), "GUIDE_PROXY"))
            parts.append(box(doc, movable, f"Guide_Window_{name}",
                             (length, 10, 52),
                             (x, y, 158 if name == active else 18),
                             "UNRATED_LIFTING_GUIDE"))
            cursor = x + length
        parts.append(box(doc, fixed, f"Guide_{side}_After", (1700-cursor, 10, 52),
                         (cursor, y, 18), "GUIDE_PROXY"))
    return parts


def make_state(state, active=None, advance=0):
    doc = App.newDocument("Gen6_Four_Cell_" + state)
    fixed = doc.addObject("App::Part", "FixedStructure")
    moving = doc.addObject("App::Part", "MotionProxies")
    spacecraft = doc.addObject("App::Part", "PassivePayloadEnvelopes")
    conceptual = doc.addObject("App::Part", "UnratedDriveEnvelopes")
    parts = []
    for side, y in (("Left", -80), ("Right", 60)):
        parts.append(box(doc, fixed, "Frame_"+side, (1800, 20, 18), (0, y, 0), "FRAME_PROXY"))
    for i, x in enumerate((0, 400, 800, 1200, 1600, 1780)):
        parts.append(box(doc, fixed, f"Crossmember_{i+1}", (20, 120, 18),
                         (x, -60, 0), "FRAME_PROXY"))
    parts += add_guides(doc, fixed, moving, active)
    for side, y in (("Left", -55), ("Right", 45)):
        parts.append(box(doc, fixed, "Support_Lip_"+side, (1600, 10, 8),
                         (100, y, 40), "CONTACT_SURFACE_PROXY"))
    parts.append(box(doc, conceptual, "Drive_Envelope", (1300, 80, 6),
                     (150, -40, 18), "NO_WINDING_OR_MASS_RATING"))
    parts.append(box(doc, conceptual, "Brake_Envelope", (200, 80, 6),
                     (1450, -40, 18), "NO_BRAKE_FORCE_OR_HEAT_RATING"))
    for name, x, length, side in CELLS:
        # Mirror R2's cassette around the rail centreline. A face touching
        # another face has zero intersection volume; no contact load is implied.
        floor_y = -265 if side < 0 else 140
        back_y = -280 if side < 0 else 275
        bridge_y = -140 if side < 0 else 55
        bridge_width = 85 if name == active else 75
        gate_y = -145 if side < 0 else 140
        push_y = -260 if side < 0 else 250
        payload_y = -250 if side < 0 else 150
        dy = -side * advance if name == active else 0
        parts += [
            box(doc, fixed, name+"_Floor", (length, 125, 10), (x, floor_y, 38), "FLOOR_PROXY"),
            box(doc, moving, name+"_Bridge", (length, bridge_width, 10),
                (x, bridge_y + (10 if side > 0 and name != active else 0), 38),
                "UNRATED_SUPPORT_BRIDGE"),
            box(doc, fixed, name+"_Back", (length, 5, 100), (x, back_y, 48), "RESTRAINT_ENVELOPE_ONLY"),
            box(doc, fixed, name+"_Front_Stop", (5, 125, 100), (x-10, floor_y, 48), "UNRATED_STOP"),
            box(doc, fixed, name+"_Aft_Stop", (5, 125, 100), (x+length+5, floor_y, 48), "UNRATED_STOP"),
            box(doc, moving, name+"_Gate", (length, 5, 100),
                (x, gate_y, 168 if name == active else 48), "UNRATED_MOVING_BARRIER"),
            box(doc, moving, name+"_Pusher", (length, 10, 100),
                (x, push_y + dy, 48), "PUSHER_FACE_NO_DRIVE"),
            box(doc, spacecraft, name+"_Payload", (length, 100, 100),
                (x, payload_y + dy, 48), "INERT_ENVELOPE_NO_APPROVED_CONTACT"),
        ]
    if active is not None:
        name, x, length, side = next(c for c in CELLS if c[0] == active)
        # One carrier docks at the chosen loading station. Its ability to
        # reach and lock at every station has not been established.
        parts += [
            box(doc, moving, "Carrier_Chassis", (60, 80, 18), (x-70, -40, 30), "UNRATED_DOCKING_PROXY"),
            box(doc, moving, "Carrier_Pusher", (10, 88, 90), (x-10, -44, 48), "CONTACT_FACE_PROXY"),
            box(doc, moving, "PM_Armature", (40, 80, 4), (x-60, -40, 26), "MAGNET_ENVELOPE_NOT_ARRAY_DESIGN"),
        ]
    doc.recompute()
    invalid = [p.Name for p in parts if p.Shape.isNull() or not p.Shape.isValid()]
    overlaps = []
    for i, a in enumerate(parts):
        for b in parts[i+1:]:
            if a.Shape.BoundBox.intersect(b.Shape.BoundBox):
                volume = a.Shape.common(b.Shape).Volume
                if volume > 1e-4:
                    overlaps.append([a.Name, b.Name, round(volume, 5)])
    sweep = None
    if active is not None and state.endswith("_armed"):
        actors = [p for p in parts if p.Name in (active+"_Payload", active+"_Pusher")]
        obstacles = [p for p in parts if p not in actors]
        swept_overlaps = []
        side = next(c[3] for c in CELLS if c[0] == active)
        for station in range(81):
            offset = -side * 2.5 * station
            for actor in actors:
                shape = actor.Shape.copy()
                shape.translate(App.Vector(0, offset, 0))
                for obstacle in obstacles:
                    if shape.BoundBox.intersect(obstacle.Shape.BoundBox):
                        volume = shape.common(obstacle.Shape).Volume
                        if volume > 1e-4:
                            swept_overlaps.append([station, actor.Name, obstacle.Name, round(volume, 5)])
        sweep = dict(stations=81, station_spacing_mm=2.5,
                     overlaps=swept_overlaps, continuous_or_tolerance_proof=False)
    native = OUT / (state + ".FCStd")
    step = OUT / (state + ".step")
    doc.saveAs(str(native))
    Part.export(parts, str(step))
    imported = Part.Shape()
    imported.read(str(step))
    delta = imported.Volume - sum(p.Shape.Volume for p in parts)
    result = dict(state=state, active_cell=active, advance_mm=advance,
                  parts=len(parts), invalid=invalid, overlaps=overlaps,
                  sampled_transfer_sweep=sweep,
                  step_solids=len(imported.Solids), step_valid=imported.isValid(),
                  step_volume_difference_mm3=round(delta, 6),
                  native=native.name, native_sha256=digest(native),
                  step=step.name, step_sha256=digest(step))
    App.closeDocument(doc.Name)
    return result


def main():
    OUT.mkdir(exist_ok=True)
    p = json.loads(SOURCE.read_text())
    states = [make_state("00_stowed")]
    for name, *_ in CELLS:
        for label, advance in (("armed", 0), ("mid", 100), ("seated", 200)):
            states.append(make_state(name+"_"+label, name, advance))
    failures = [s for s in states if s["invalid"] or s["overlaps"] or
                (s["sampled_transfer_sweep"] and s["sampled_transfer_sweep"]["overlaps"]) or
                not s["step_valid"] or s["parts"] != s["step_solids"] or
                abs(s["step_volume_difference_mm3"]) > .01]
    if failures:
        raise AssertionError("nominal four-cell FreeCAD/STEP failure: " +
                             json.dumps([{k: s[k] for k in ("state", "invalid", "overlaps",
                               "parts", "step_solids", "step_valid", "step_volume_difference_mm3")}
                               for s in failures]))
    cells = []
    for name, x, length, side in CELLS:
        available = p["brake_stator_start_x"] - x
        cells.append(dict(name=name, size="3U" if length > 200 else "1U",
                          side="left" if side < 0 else "right", x_mm=x,
                          length_mm=length, available_drive_travel_mm=available,
                          ideal_mean_g_for_6_m_s=round(6**2/(2*available/1000*9.80665), 3),
                          ideal_mean_g_for_3_m_s=round(3**2/(2*available/1000*9.80665), 3)))
    report = dict(status="UNSELECTED_FOUR_CELL_NOMINAL_PACKAGING_SCREEN_R0",
                  method="FreeCAD 1.0 exact-solid nominal state checks and STEP readback",
                  source_sha256=digest(Path(__file__)), source_parameters_sha256=digest(SOURCE),
                  cells=cells, lateral_outermost_y_mm=[-280, 280],
                  states=states, open=["motion between states and concurrent actuation",
                    "positive launch and mid-transfer restraint", "carrier docking at each cell",
                    "bridge, gate and guide transition", "same-boundary feeder candidates",
                    "tolerances, thermal growth, contact and load", "complete mass and host envelope",
                    "downstream reduced acceleration travel and drive/shot sequencing"])
    (OUT/"Four_Cell_R0_Report.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"states":len(states), "cells":cells,
                      "overlap_states":sum(bool(x["overlaps"]) for x in states)}))


if __name__ == "__main__":
    main()
