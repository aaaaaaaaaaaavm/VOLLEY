"""Create a native FreeCAD review document and export its named Gen5 STEP.

Run with /usr/bin/python3 on a FreeCAD 1.0 installation. FreeCAD opens the eight
parametric CadQuery STEP parts as B-reps and owns the assembly placements and final
STEP export. The source parts are not represented as editable FreeCAD feature
histories; this is a native review assembly, not a fabrication-ready CAD release.
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
PARAM = json.loads((ROOT / "parameters.json").read_text())
REPORT = json.loads((ROOT / "REVIEW_ASSEMBLY.json").read_text())
NATIVE = ROOT / "native/Gen5_Review.FCStd"
STEP = ROOT / "step/gen5/VOLLEY_Review_Assembly_FreeCAD_Gen5.step"
OUTPUT = ROOT / "FREECAD_EXPORT.json"
SOURCE = ROOT / "step/gen5"
PART_NATIVE_DIR = ROOT / "step/freecad_gen5"
PART_NAMES = ("Interface_ESPA", "Track", "Stator", "Sled", "Magazine_Cassette",
              "Brake", "Payload_3U", "Enclosure")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize_step(path: Path) -> None:
    contents = path.read_text(encoding="utf-8")
    contents = re.sub(r"'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}'", "'1970-01-01T00:00:00'", contents)
    contents = re.sub(r"FILE_NAME\('[^']*'", f"FILE_NAME('{path.name}'", contents)
    path.write_text(contents, encoding="utf-8")


def main() -> None:
    if App.Version()[0] != "1":
        raise RuntimeError(f"reviewed against FreeCAD 1.x; found {App.Version()}")
    NATIVE.parent.mkdir(parents=True, exist_ok=True)
    PART_NATIVE_DIR.mkdir(parents=True, exist_ok=True)
    native_part_hashes = {}
    for name in PART_NAMES:
        source = Part.read(str(SOURCE / f"VOLLEY_{name}_Gen5.step"))
        target = PART_NATIVE_DIR / f"VOLLEY_{name}_FreeCAD_Gen5.step"
        source.exportStep(str(target))
        normalize_step(target)
        roundtrip = Part.read(str(target))
        if not roundtrip.isValid() or abs(roundtrip.Volume - source.Volume) > 0.01:
            raise RuntimeError(f"FreeCAD STEP part read-back failed: {name}")
        native_part_hashes[name] = digest(target)
    doc = App.newDocument("VOLLEY_Gen5_Review")
    group = doc.addObject("App::Part", "ReferenceAssembly")
    group.Label = "Gen5 reference only — packaging clash unresolved"
    items = []
    seen = {}

    def add(instance: str, source: str, x=0.0, y=0.0, z=0.0):
        path = SOURCE / f"VOLLEY_{source}_Gen5.step"
        shape = Part.read(str(path))
        if shape.isNull() or not shape.isValid():
            raise RuntimeError(f"invalid source solid: {path}")
        feature = doc.addObject("Part::Feature", instance)
        feature.Label = instance.replace("_", " ")
        feature.Shape = shape
        feature.Placement.Base = App.Vector(float(x), float(y), float(z))
        feature.addProperty("App::PropertyString", "SourceFile", "Provenance")
        feature.SourceFile = str(path.relative_to(ROOT))
        feature.addProperty("App::PropertyString", "SourceSHA256", "Provenance")
        feature.SourceSHA256 = digest(path)
        feature.addProperty("App::PropertyString", "DesignStatus", "Provenance")
        feature.DesignStatus = "REFERENCE_ONLY_NOT_FLIGHT_APPROVED"
        group.addObject(feature)
        items.append(feature)
        seen[instance] = feature

    for name in ("Interface_ESPA", "Track", "Stator", "Sled", "Brake", "Enclosure"):
        add(name, name)
    p = REPORT["reference_placement_mm"]
    pitch = PARAM["groups"]["magazine"]["satellite_pitch_z"]
    for side, sign in (("S", -1), ("P", 1)):
        y = sign * p["cassette_center_y_abs"]
        add(f"Magazine_{side}", "Magazine_Cassette", p["cassette_x"], y, p["cassette_z_min"])
        for index in range(6):
            add(f"Payload_{side}{index+1:02d}", "Payload_3U", p["payload_x"], y,
                p["payload_first_center_z"] + index * pitch)
    doc.recompute()
    if len(items) != 20:
        raise RuntimeError("expected 20 named instances")
    overlap = {side: seen["Track"].Shape.common(seen[f"Magazine_{side}"].Shape).Volume
               for side in ("S", "P")}
    for side in ("S", "P"):
        if abs(overlap[side] - REPORT["track_cassette_overlap_mm3"][side]) > 0.1:
            raise RuntimeError(f"FreeCAD/CadQuery overlap mismatch for side {side}: {overlap[side]}")
    doc.saveAs(str(NATIVE))
    Part.export(items, str(STEP))
    normalize_step(STEP)
    imported = Part.read(str(STEP))
    if imported.isNull() or not imported.isValid():
        raise RuntimeError("FreeCAD STEP export failed read-back validity")
    result = {
        "status": "NATIVE_REVIEW_ASSEMBLY_EXPORTED_WITH_KNOWN_INTERFERENCE",
        "freecad_version": App.Version(),
        "source_method": "FreeCAD 1.0 Part B-rep imports of the eight CadQuery-generated STEP parts",
        "instance_count": len(items),
        "native_fcstd_sha256": digest(NATIVE),
        "freecad_step_sha256": digest(STEP),
        "freecad_part_step_sha256": native_part_hashes,
        "freecad_step_readback_valid": bool(imported.isValid()),
        "track_cassette_overlap_mm3": {key: round(value, 3) for key, value in overlap.items()},
        "geometry_limits": ["no native parametric feature history for imported part solids",
                            "known side-fed interference", "no fasteners/harness/tolerance stack",
                            "no provider ICD or payload qualification"],
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n")
    print(f"FreeCAD {'.'.join(App.Version()[:3])}: {len(items)} named instances, read-back valid")
    print(f"FreeCAD exact-solid overlaps S/P: {overlap['S']:.3f}/{overlap['P']:.3f} mm^3")
    print(f"FCStd {NATIVE.stat().st_size} bytes; assembly STEP {STEP.stat().st_size} bytes; eight part STEP exports")
    App.closeDocument(doc.Name)


if __name__ == "__main__":
    main()
