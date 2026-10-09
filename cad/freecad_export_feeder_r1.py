"""Create native FreeCAD R1 candidate and STEP, with read-back and collision checks.

Run with /usr/bin/python3 where FreeCAD 1.0 Python modules are installed.
Imported CadQuery B-reps are named Part features, not editable feature histories.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, "/usr/lib/freecad-python3/lib")
import FreeCAD as App  # noqa: E402
import Part  # noqa: E402

ROOT = Path(__file__).resolve().parent
R1 = ROOT / "step/feeder_candidate_r1"
BASE = ROOT / "step/gen5"
NATIVE = ROOT / "native/Feeder_Candidate_R1.FCStd"
STEP = R1 / "VOLLEY_Feeder_Assembly_FreeCAD_R1.step"
RESULT = ROOT / "FREECAD_FEEDER_R1.json"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def norm(path):
    s = path.read_text()
    s = re.sub(r"'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}'", "'1970-01-01T00:00:00'", s)
    s = re.sub(r"FILE_NAME\('[^']*'", f"FILE_NAME('{path.name}'", s)
    path.write_text(s)


def main():
    if App.Version()[0] != "1":
        raise RuntimeError(f"FreeCAD 1.x required: {App.Version()}")
    expected = json.loads((ROOT / "FEEDER_CANDIDATE_R1.json").read_text())
    if not expected["all_routes_clear"]:
        raise RuntimeError("CadQuery candidate sweep failed")
    NATIVE.parent.mkdir(parents=True, exist_ok=True)
    doc = App.newDocument("VOLLEY_Feeder_R1")
    group = doc.addObject("App::Part", "CandidateAssembly")
    group.Label = "R1 unselected geometry — no retention or actuator"
    items, seen = [], {}

    def add(instance, path, x=0, y=0, z=0):
        shape = Part.read(str(path))
        if shape.isNull() or not shape.isValid():
            raise RuntimeError(f"invalid source STEP {path}")
        feature = doc.addObject("Part::Feature", instance)
        feature.Label = instance.replace("_", " ")
        feature.Shape = shape
        feature.Placement.Base = App.Vector(float(x), float(y), float(z))
        feature.addProperty("App::PropertyString", "SourceFile", "Provenance")
        feature.SourceFile = str(path.relative_to(ROOT))
        feature.addProperty("App::PropertyString", "SourceSHA256", "Provenance")
        feature.SourceSHA256 = sha(path)
        feature.addProperty("App::PropertyString", "DesignStatus", "Provenance")
        feature.DesignStatus = "R1_UNSELECTED_GEOMETRY_ONLY"
        group.addObject(feature)
        items.append(feature)
        seen[instance] = feature

    for name in ("Interface_ESPA", "Track", "Stator", "Sled", "Brake"):
        add(name, BASE / f"VOLLEY_{name}_Gen5.step")
    add("Wide_Enclosure_R1", R1 / "VOLLEY_Wide_Enclosure_R1.step")
    add("Lift_Guides_R1", R1 / "VOLLEY_Lift_Guides_R1.step")
    for side, sign in (("P",1),("S",-1)):
        add(f"Open_Cassette_{side}_R1", R1 / f"VOLLEY_Open_Cassette_{side}_R1.step",
            200, sign*190.5, 0)
        for i in range(6):
            add(f"Payload_{side}{i+1:02d}", BASE / "VOLLEY_Payload_3U_Gen5.step",
                220, sign*190.5, 76+i*104)
    doc.recompute()
    if len(items) != 21 or not all(x.Shape.isValid() for x in items):
        raise RuntimeError("FreeCAD assembly object validity failed")
    overlaps = {side: seen["Track"].Shape.common(seen[f"Open_Cassette_{side}_R1"].Shape).Volume
                for side in ("P", "S")}
    if any(v > .01 for v in overlaps.values()):
        raise RuntimeError(f"FreeCAD track/cassette clash {overlaps}")
    doc.saveAs(str(NATIVE))
    Part.export(items, str(STEP))
    norm(STEP)
    readback = Part.read(str(STEP))
    if readback.isNull() or not readback.isValid():
        raise RuntimeError("FreeCAD assembly STEP read-back invalid")
    result = dict(status="UNSELECTED_R1_NATIVE_REVIEW_NOT_FLIGHT_DESIGN",
                  freecad_version=App.Version(), named_instances=len(items),
                  native_sha256=sha(NATIVE), step_sha256=sha(STEP),
                  track_cassette_overlap_mm3=overlaps,
                  readback_valid=True,
                  limitation="B-rep imports; no native parametric feature history, actuator, retention gate, ICD or qualification")
    RESULT.write_text(json.dumps(result, indent=2) + "\n")
    print(f"FreeCAD R1: {len(items)} valid instances; overlaps {overlaps}; STEP read-back valid")
    App.closeDocument(doc.Name)


if __name__ == "__main__":
    main()
