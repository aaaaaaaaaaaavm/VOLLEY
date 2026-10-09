"""Export a named Gen5 review assembly and its measured packaging screen.

The placements are a stated reference arrangement, not a solved feeder or flight
installation. The script deliberately reports an interference rather than cutting
away the cassette or track to make a pleasing assembly image.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import cadquery as cq

ROOT = Path(__file__).resolve().parent
PARAM_FILE = ROOT / "parameters.json"
PART_DIR = ROOT / "step/gen5"
OUT = PART_DIR / "VOLLEY_Review_Assembly_Gen5.step"
REPORT = ROOT / "REVIEW_ASSEMBLY.json"
PARTS = ("Interface_ESPA", "Track", "Stator", "Sled", "Magazine_Cassette",
         "Brake", "Payload_3U", "Enclosure")


def read_part(name: str):
    return cq.importers.importStep(str(PART_DIR / f"VOLLEY_{name}_Gen5.step"))


def main() -> None:
    params = json.loads(PARAM_FILE.read_text(encoding="utf-8"))
    g = params["groups"]
    source_hashes = {name: hashlib.sha256((PART_DIR / f"VOLLEY_{name}_Gen5.step").read_bytes()).hexdigest()
                     for name in PARTS}
    shapes = {name: read_part(name) for name in PARTS}
    assembly = cq.Assembly(name="VOLLEY_Gen5_REFERENCE_NOT_FLIGHT")
    for name in ("Interface_ESPA", "Track", "Stator", "Sled", "Brake", "Enclosure"):
        assembly.add(shapes[name], name=name)

    # The side-fed reference layout is the only placement assumed here. It keeps the
    # two cassette outer faces at the enclosure's *inner* side walls (zero clearance).
    # It is intentionally not passed off as an accepted mechanical interface.
    enclosure_inner_half_y = g["enclosure"]["y_half_width"] - g["enclosure"]["skin_thickness"]
    cassette_half_y = g["magazine"]["cassette_width_y"] / 2
    center_y = enclosure_inner_half_y - cassette_half_y
    cassette_x = 200.0  # reference feed-line placement; no feeder motion is modeled
    payload_x = cassette_x + 20.0
    cell_bottom = g["magazine"]["septum_z_min"]
    payload_h = g["payload_3u"]["height_z"]
    pitch = g["magazine"]["satellite_pitch_z"]
    cassette_collisions = {}
    for side in (-1, 1):
        label = "S" if side < 0 else "P"
        dy = side * center_y
        placed_cassette = shapes["Magazine_Cassette"].translate((cassette_x, dy, 0))
        assembly.add(placed_cassette, name=f"Magazine_{label}")
        # CAD exact-solid overlap, distinct from a broad bounding-box warning.
        cassette_collisions[label] = round(placed_cassette.intersect(shapes["Track"]).val().Volume(), 3)
        for i in range(g["magazine"]["satellites_per_cassette"]):
            zc = cell_bottom + payload_h / 2 + i * pitch
            placed_payload = shapes["Payload_3U"].translate((payload_x, dy, zc))
            assembly.add(placed_payload, name=f"Payload_{label}{i+1:02d}")

    assembly.save(str(OUT), exportType="STEP")
    contents = OUT.read_text(encoding="utf-8")
    contents = re.sub(r"'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}'", "'1970-01-01T00:00:00'", contents)
    contents = re.sub(r"FILE_NAME\('[^']*'", f"FILE_NAME('{OUT.name}'", contents)
    OUT.write_text(contents, encoding="utf-8")

    track_width = g["track"]["overall_width"]
    cassette_width = g["magazine"]["cassette_width_y"]
    available = 2 * enclosure_inner_half_y
    required = track_width + 2 * cassette_width
    report = {
        "status": "REVIEW_ONLY_INTERFERENCE_FOUND",
        "configuration": "Gen5 side-fed reference, stationary first-cell alignment",
        "not_demonstrated": ["feeder kinematics", "launch locks", "tolerances", "fasteners",
                             "electrical harness", "approved host ICD", "payload qualification"],
        "parameters_sha256": hashlib.sha256(PARAM_FILE.read_bytes()).hexdigest(),
        "part_sha256": source_hashes,
        "assembly_sha256": hashlib.sha256(OUT.read_bytes()).hexdigest(),
        "step_file": str(OUT.relative_to(ROOT)),
        "instance_count": 20,
        "reference_placement_mm": {"cassette_x": cassette_x, "cassette_center_y_abs": center_y,
                                   "payload_x": payload_x, "cassette_z_min": 0.0,
                                   "payload_first_center_z": cell_bottom + payload_h / 2},
        "side_by_side_width_screen_mm": {"enclosure_internal_width": available,
                                         "track_overall_width": track_width,
                                         "two_cassette_width": 2 * cassette_width,
                                         "required_without_clearance": required,
                                         "shortfall_without_clearance": required - available},
        "track_cassette_overlap_mm3": cassette_collisions,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"{OUT.name}: {OUT.stat().st_size} bytes, {report['instance_count']} instances")
    print(f"width shortfall {required-available:.1f} mm; exact track/cassette overlap {cassette_collisions} mm^3")


if __name__ == "__main__":
    main()
