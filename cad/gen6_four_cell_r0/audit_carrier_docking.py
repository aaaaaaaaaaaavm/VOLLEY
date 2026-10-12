#!/usr/bin/env python3
"""Sample carrier travel past four stored cells before the selected transfer."""
from pathlib import Path
import argparse
import hashlib
import json

import FreeCAD as App
import Part

HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--release", type=Path, default=HERE/"release")
    out = parser.parse_args().release
    report = json.loads((out/"Four_Cell_R0_Report.json").read_text())
    source = out/"00_stowed.FCStd"
    doc = App.openDocument(str(source))
    obstacles = [o for o in doc.Objects if o.TypeId == "Part::Box"]
    max_target_x = max(c["x_mm"] for c in report["cells"])
    travel = max_target_x-170.0
    stations = int(travel/5)+1
    # Same carrier envelopes and initial station as in each active state.
    carrier = (
        ("Chassis", Part.makeBox(60,80,18,App.Vector(100,-40,30))),
        ("Pusher", Part.makeBox(10,88,90,App.Vector(160,-44,48))),
        ("Armature", Part.makeBox(40,80,4,App.Vector(110,-40,26))),
    )
    overlaps = []
    for station in range(stations):
        dx = travel*station/(stations-1) if stations > 1 else 0
        for name, original in carrier:
            shape = original.copy()
            shape.translate(App.Vector(dx,0,0))
            for obstacle in obstacles:
                if shape.BoundBox.intersect(obstacle.Shape.BoundBox):
                    volume = shape.common(obstacle.Shape).Volume
                    if volume > 1e-4:
                        overlaps.append([station,name,obstacle.Name,round(volume,5)])
    App.closeDocument(doc.Name)
    result = dict(status="NOMINAL_UNLOADED_CARRIER_DOCKING_SCREEN",
                  source=source.name, source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                  station_count=stations, travel_mm=travel, maximum_step_mm=5,
                  intersections=overlaps,
                  unverified=["loaded carrier travel", "motored positioning repeatability",
                              "brake return and homing", "hard stops and locks", "tolerances/deflection",
                              "guide/bridge transition", "safe state"])
    (out/"Carrier_Docking_Sweep.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"stations":stations,"travel_mm":travel,"intersections":len(overlaps)}))
    if overlaps:
        raise AssertionError("nominal carrier docking path intersects stored assembly")


if __name__ == "__main__":
    main()
