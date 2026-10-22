"""Native FreeCAD candidate geometry, material ledger and motion inspection.

Run: PYTHONPATH=/usr/lib/freecad-python3/lib /usr/bin/python3 build.py
Dimensions in mm. Detailed design candidates, not a manufacturing release.
Thread/gear forms, purchased actuator internals and contact compliance are unresolved.
"""

from pathlib import Path
import math, json, hashlib, itertools
import FreeCAD as App
import Part

HERE = Path(__file__).resolve().parent
OUT = HERE / "release"
OUT.mkdir(exist_ok=True)
P = json.loads((HERE / "requirements.json").read_text())
DENSITY = {
    "aluminium": 2.7e-6,
    "steel": 7.85e-6,
    "polymer": 1.41e-6,
    "payload": 0,
    "envelope": 0,
}
CACHE = {}
CANDIDATES = [
    "lead_screw",
    "spring_dual_gate",
    "rack_pawl",
    "indexed_drum",
    "pantograph",
    "telescopic",
    "belt_shuttle",
]
V = App.Vector


def block(dims, pos):
    return Part.makeBox(*dims, V(*pos))


def cyl(radius, length, pos, axis=(0, 1, 0)):
    return Part.makeCylinder(radius, length, V(*pos), V(*axis))


def link(a, b, r=3):
    a, b = V(*a), V(*b)
    v = b - a
    return Part.makeCylinder(r, v.Length, a, v)


def parts(candidate, L, u=0, phase="transfer"):
    out = []

    def add(name, shape, material="aluminium", role="fixed", contact=""):
        assert not shape.isNull() and shape.isValid(), name
        out.append(
            {
                "name": name,
                "shape": shape,
                "material": material,
                "role": role,
                "contact": contact,
            }
        )

    def box(name, dims, pos, mat="aluminium", role="fixed", contact=""):
        add(name, block(dims, pos), mat, role, contact)

    # Payload and receiving cradle share datums: X longitudinal launch, Y feed, Z normal.
    y = -200 + u
    z = 22.0
    gate_open = phase not in ["stowed", "reset"]
    docked = phase == "seated"
    box("Passive_payload", (L, 100, 100), (0, y, z), "payload", "payload")
    box("Cassette_floor", (L + 24, 110, 6), (-12, -210, 16), contact="floor joints")
    box(
        "Support_bridge",
        (L + 24, 100, 6),
        (-12, -100, 16),
        contact="coplanar floor joints",
    )
    box(
        "Receiving_sled_floor",
        (L + 24, 110, 4),
        (-12, 0, 18),
        role="receiver",
        contact="support contact only",
    )
    for x in [-6, L + 2]:
        side = block((4, 200, 108), (x, -208, 22))
        cap = block((10, 200, 4), (x - 3, -208, 124))
        add(
            "Stored_side_cap_" + str(x),
            side.fuse(cap)
            .cut(block((14, 6, 10), (x - 4, -94, 123)))
            .cut(block((14, 6, 10), (x - 4, -86, 123)))
            .removeSplitter(),
            "aluminium",
            "fixed",
            "one machined L-section; not overlapping separate pieces",
        )
    box("Cassette_rear", (L + 24, 4, 112), (-12, -212, 22), contact="floor joint")
    lift = (
        float(phase.split("_")[1])
        if phase.startswith("gate_")
        else (120 if gate_open else 0)
    )
    box("Storage_gate", (L + 2, 4, 100), (-1, -93, 22 + lift), role="gate")
    box(
        "Receiver_side_gate",
        (L + 24, 2, 108),
        (-12, -4, 142 if not docked else 22),
        role="gate",
    )
    # Independently restrained storage gate; pins do not penetrate the passive satellite.
    for x in [-16, L + 16]:
        add(
            "Storage_gate_pin_" + str(x),
            cyl(2, 20, (x, -91, 148 if gate_open else 118), (0, 0, 1)),
            "steel",
            "latch",
            "gate ear contact unresolved",
        )
    # Captive transfer fork has front AND rear barriers: no reliance on pushing friction.
    front_up = docked
    fy = -200 if docked else y
    if docked:
        u = 0
    # Overhead fork ties the barriers to the drive outside the cassette walls.
    # The front gate is a separate sliding member; its latch/joint remains unrated.
    rear = block((L - 4, 3, 109), (2, fy - 4, 30))
    pieces = [
        block((16, 12, 6), (-38, fy - 26, 62)),
        block((L + 22, 3, 5), (-11, fy - 4, 134)),
        block((4, 110, 5), (-11, fy - 5, 134)),
        block((4, 110, 5), (L + 7, fy - 5, 134)),
        block((21, 25, 5), (-28, fy - 26, 134)),
        block((6, 12, 72), (-28, fy - 26, 62)),
        block((42, 12, 6), (-75, fy - 26, 62)),
    ]
    for bx in [-34, -62]:
        pieces.append(
            block((26, 18, 24), (bx - 13, fy - 29, 40))
            .cut(cyl(8, 18, (bx, fy - 29, 52)))
            .cut(block((10, 5, 10), (-61, fy - 21, 34)))
        )
    if candidate == "lead_screw":
        pieces.extend(
            [
                block((6, 12, 22), (-38, fy - 28, 62)),
                block((8, 12, 8), (-40, fy - 28, 76)),
            ]
        )
    frame = rear.multiFuse(pieces).removeSplitter()
    assert len(frame.Solids) == 1, "Disconnected fork load path"
    add(
        "Driven_fork_frame",
        frame,
        "aluminium",
        "moving",
        "One connected fork and bearing housings; bearing fits, gate and nut attachment ratings remain unverified",
    )
    box(
        "Fork_front_barrier",
        (L, 3, 35),
        (0, fy + 101, 145 if front_up else 60),
        role="moving",
    )
    # Side arms and crosshead are part of the single connected fork solid above.
    # Rail clamp shoes close before the fork front barrier opens at the receiving datum.
    for x in [5, L - 13]:
        for yy in [-1, 100]:
            box(
                "Receiver_clamp_" + str(x) + "_" + str(yy),
                (8, 1, 8),
                (
                    x,
                    yy if docked else yy + (-8 if yy < 0 else 8),
                    26 if docked else 132,
                ),
                "steel",
                "clamp",
            )
    # Twin linear guides and load-carrying shuttle outside spacecraft keep-out.
    for x in [-34, -62]:
        add("Guide_shaft_" + str(x), cyl(4, 450, (x, -440, 52)), "steel", "fixed")
        bearing = cyl(8, 18, (x, -229 + u, 52)).cut(cyl(4.25, 18, (x, -229 + u, 52)))
        add("Guide_bearing_" + str(x), bearing, "polymer", "moving")
    # Crosshead is fused into Driven_fork_frame; no disconnected proxy link.
    # Positive arrest rack: tooth/pawl contact is represented, not qualified.
    if "capture_rack" not in CACHE:
        base = block((8, 450, 5), (-60, -440, 26))
        teeth = [block((8, 1, 3), (-60, -440 + j, 31)) for j in range(0, 450, 2)]
        CACHE["capture_rack"] = base.multiFuse(teeth).removeSplitter()
    rack = CACHE["capture_rack"]
    add("Power_off_capture_rack", rack, "steel", "fixed")
    box(
        "Spring_applied_pawl",
        (8, 3, 8),
        (-60, -220 + u, 35),
        "steel",
        "moving",
        "engagement/contact proof pending",
    )
    # Actuator/sensor packages remain explicit uncatalogued envelopes; no invented mass.
    box(
        "Drive_motor_envelope",
        (35, 45, 35),
        (-95, -445, 85),
        "envelope",
        "unselected_actuator",
    )
    for yy in [-203, -3]:
        box(
            "Position_sensor_" + str(yy),
            (12, 12, 12),
            (L + 30, yy, 135),
            "envelope",
            "unselected_sensor",
        )
    if candidate == "lead_screw":
        add(
            "Tr8x2_screw_blank",
            cyl(4, 450, (-48, -440, 84)),
            "steel",
            "drive",
            "thread form represented by nominal blank",
        )
        nut = block((16, 16, 16), (-56, -228 + u, 76)).cut(
            cyl(4.25, 16, (-48, -228 + u, 84))
        )
        add("Tr8_nut_blank", nut, "polymer", "drive", "thread engagement not resolved")
        for yy in [-440, -10]:
            add(
                "Screw_end_bearing_" + str(yy),
                cyl(9, 10, (-48, yy, 84)).cut(cyl(4.25, 10, (-48, yy, 84))),
                "steel",
                "drive",
            )
    elif candidate == "spring_dual_gate":
        # Helical centreline and circular section, actual wire volume available.
        h = 180 + u
        turns = P["spring_active_turns"]
        helix = Part.makeHelix(h / turns, h, 10)
        profile = Part.Wire([Part.makeCircle(0.6, V(10, 0, 0), V(0, 1, 0))])
        wire = Part.Wire(helix.Edges)
        spring = wire.makePipeShell([profile], True, True)
        spring.rotate(V(0, 0, 0), V(1, 0, 0), -90)
        spring.translate(V(-48, -410, 84))
        add("Captured_spring_wire", spring, "steel", "drive")
        box(
            "Second_escapement_gate",
            (L + 2, 3, 100),
            (-1, -85, 142 if gate_open else 22),
            role="gate",
        )
        box(
            "Governor_brake_envelope",
            (30, 30, 30),
            (-95, -350, 85),
            "envelope",
            "unselected_actuator",
        )
    elif candidate == "rack_pawl":
        if "driven_rack" not in CACHE:
            base = block((10, 240, 8), (-49, -425, 78))
            teeth = [block((10, 2, 3), (-49, -425 + j, 86)) for j in range(0, 240, 4)]
            CACHE["driven_rack"] = base.multiFuse(teeth).removeSplitter()
        rack = CACHE["driven_rack"].copy()
        rack.translate(V(0, u, 0))
        add("Driven_rack", rack, "steel", "drive", "tooth form schematic")
        add(
            "Index_pinion_blank",
            cyl(12, 10, (-53, -205, 102), (1, 0, 0)),
            "steel",
            "drive",
            "involute tooth profile unmodeled",
        )
        box(
            "Independent_index_pawl",
            (12, 1.6, 3),
            (-58, -206.8, 86 if phase in ["stowed", "seated"] else 126),
            "steel",
            "drive",
            "Nominal tooth-gap fit; pivot, actual tooth contact and load validation remain open",
        )
    elif candidate == "indexed_drum":
        # Axis along X; four separately retained cells. Mixed storage length is explicit.
        center = V(0, -150, 350)
        span = 340.5
        for i in range(1, 4):
            angle = i * 90.0
            ll = (
                (113.5 if i in [1, 3] else 340.5)
                if L > 200
                else (340.5 if i in [1, 3] else 113.5)
            )
            module = parts("lead_screw", ll, 0, "stowed")
            for q in module:
                if q["name"].startswith(
                    ("Passive_payload", "Cassette_", "Stored_side_cap", "Storage_gate")
                ):
                    shape = q["shape"].copy()
                    shape.rotate(center, V(1, 0, 0), angle)
                    add(
                        "Other_cell_" + str(i) + "_" + q["name"],
                        shape,
                        q["material"],
                        "other_payload" if q["material"] == "payload" else "drive",
                    )
        add(
            "Drum_axle",
            cyl(12, span + 240, (-140, -150, 350), (1, 0, 0)),
            "steel",
            "drive",
        )
        for xx in [-120, span + 20]:
            ring = cyl(298, 6, (xx, -150, 350), (1, 0, 0)).cut(
                cyl(273, 6, (xx, -150, 350), (1, 0, 0))
            )
            hub = cyl(25, 6, (xx, -150, 350), (1, 0, 0)).cut(
                cyl(13, 6, (xx, -150, 350), (1, 0, 0))
            )
            pieces = [hub]
            for j in range(4):
                ang = j * math.pi / 2
                pieces.append(
                    link(
                        (xx + 3, -150 + 20 * math.sin(ang), 350 - 20 * math.cos(ang)),
                        (xx + 3, -150 + 283 * math.sin(ang), 350 - 283 * math.cos(ang)),
                        5,
                    )
                )
            add(
                "Drum_rotor_" + str(xx),
                ring.multiFuse(pieces).removeSplitter(),
                "aluminium",
                "drive",
                "machined or welded rotor; weld/load verification absent",
            )
    elif candidate == "pantograph":
        n = 3
        th0 = math.radians(10)
        th1 = math.radians(70)
        a = 200 / (2 * n * (math.sin(th1) - math.sin(th0)))
        theta = math.asin(math.sin(th0) + u / (2 * n * a))
        base = -220 - 2 * n * a * math.sin(th0)
        for xx in [-110]:
            for i in range(n):
                ya = base + 2 * i * a * math.sin(theta)
                yb = ya + 2 * a * math.sin(theta)
                za = 84 - a * math.cos(theta)
                zb = 84 + a * math.cos(theta)
                add(
                    "Scissor_" + str(xx) + "_" + str(i) + "A",
                    link((xx + 3, ya, za), (xx + 3, yb, zb), 2.5),
                    "steel",
                    "drive",
                    "pinned joints nominal",
                )
                add(
                    "Scissor_" + str(xx) + "_" + str(i) + "B",
                    link((xx - 3, ya, zb), (xx - 3, yb, za), 2.5),
                    "steel",
                    "drive",
                    "pinned joints nominal",
                )
        box(
            "Scissor_input_actuator",
            (25, 35, 70),
            (-95, base - 25, 49),
            "envelope",
            "unselected_actuator",
        )
    elif candidate == "telescopic":
        for i in range(3):
            a = 22 - 5 * i
            length = 120
            origin = (-48 - a / 2, -320 + i * u / 3, 84 - a / 2)
            tube = block((a, length, a), origin).cut(
                block(
                    (a - 3, length, a - 3),
                    (origin[0] + 1.5, origin[1], origin[2] + 1.5),
                )
            )
            add(
                "Nested_stage_" + str(i),
                tube,
                "aluminium",
                "drive",
                "stage stop and bearing fit require detailed review",
            )
    elif candidate == "belt_shuttle":
        for yy in [-430, -10]:
            add(
                "Drive_pulley_" + str(yy),
                cyl(12, 8, (-52, yy, 84), (1, 0, 0)),
                "aluminium",
                "drive",
            )
        for zz in [70.5, 96]:
            box(
                "Belt_span_" + str(zz),
                (8, 420, 1.5),
                (-52, -430, zz),
                "polymer",
                "drive",
            )
        clamp = block((16, 18, 10), (-56, -226 + u, 92)).cut(
            block((10, 20, 2), (-53, -227 + u, 95.75))
        )
        add(
            "Belt_carriage_clamp",
            clamp,
            "aluminium",
            "drive",
            "belt tension/contact and clamping screws unverified",
        )
        for yy in [-430, -10]:
            ring = cyl(13.5, 8, (-52, yy, 84), (1, 0, 0)).cut(
                cyl(12, 8, (-52, yy, 84), (1, 0, 0))
            )
            half = block((10, 13.5, 30), (-53, yy - 13.5 if yy < -100 else yy, 69))
            add("Belt_return_" + str(yy), ring.common(half), "polymer", "drive")
    return out


def audit(items):
    collisions = []
    minimum_payload_gap = None
    for a, b in itertools.combinations(items, 2):
        if not a["shape"].BoundBox.intersect(b["shape"].BoundBox):
            continue
        volume = a["shape"].common(b["shape"]).Volume
        if volume > 1e-4:
            collisions.append(
                {
                    "a": a["name"],
                    "b": b["name"],
                    "volume_mm3": round(volume, 6),
                    "payload_involved": a["role"] in ["payload", "other_payload"]
                    or b["role"] in ["payload", "other_payload"],
                    "disposition": "UNRESOLVED; not automatically accepted as intended contact",
                }
            )
    return collisions


def export(candidate, L, payload_class):
    items = parts(candidate, L, 0, "stowed")
    doc = App.newDocument(candidate + "_" + payload_class)
    rows = []
    objects = []
    for part in items:
        obj = doc.addObject(
            "Part::Feature", part["name"].replace("-", "m").replace(".", "_")
        )
        obj.Shape = part["shape"]
        obj.addProperty("App::PropertyString", "MaterialBasis")
        obj.MaterialBasis = part["material"]
        obj.addProperty("App::PropertyString", "EvidenceBoundary")
        obj.EvidenceBoundary = part["contact"] or part["role"]
        objects.append(obj)
        rows.append(
            {
                "part": part["name"],
                "material": part["material"],
                "role": part["role"],
                "volume_mm3": part["shape"].Volume,
                "modeled_mass_kg": part["shape"].Volume * DENSITY[part["material"]],
            }
        )
    doc.recompute()
    stem = candidate + "_" + payload_class
    doc.saveAs(str(OUT / (stem + ".FCStd")))
    Part.export(objects, str(OUT / (stem + ".step")))
    exported = Part.Shape()
    exported.read(str(OUT / (stem + ".step")))
    assert exported.isValid() and len(exported.Solids) >= len(items), (
        stem,
        len(exported.Solids),
        len(items),
    )
    # Exact mid-transfer and seated STEP snapshots are generated from the same parameters.
    if payload_class == "3U":
        for phase, u in [("mid_transfer", 100), ("seated", 200)]:
            ss = [
                p["shape"]
                for p in parts(candidate, L, u, "seated" if u == 200 else "transfer")
            ]
            compound = Part.Compound(ss)
            compound.exportStep(str(OUT / (stem + "_" + phase + ".step")))
    sweep = block((L, 300, 100), (0, -200, 22))
    swept = []
    for part in parts(candidate, L, 0, "transfer"):
        if part["role"] in ["payload", "moving"]:
            continue
        vol = sweep.common(part["shape"]).Volume
        if vol > 1e-4:
            swept.append({"part": part["name"], "volume_mm3": vol})
    collisions = []
    poses = (
        [
            (u, "seated" if u == 200 else "transfer")
            for u in [0, 25, 50, 75, 100, 125, 150, 175, 200]
        ]
        + [(0, "stowed")]
        + [(0, "gate_" + str(lift)) for lift in [0, 30, 60, 90, 120]]
    )
    for u, phase in poses:
        pp = parts(candidate, L, u, phase)
        cc = audit(pp)
        collisions.append(
            {
                "advance_mm": u,
                "phase": phase,
                "intersections": cc,
                "unresolved_payload_intersections": sum(
                    c["payload_involved"] for c in cc
                ),
            }
        )
    report = {
        "candidate": candidate,
        "payload_class": payload_class,
        "source_revision": P["revision"],
        "modeled_material_kg": sum(r["modeled_mass_kg"] for r in rows),
        "parts": rows,
        "valid_export_solids": len(exported.Solids),
        "motion_stations": collisions,
        "continuous_translational_payload_sweep": {
            "method": "Exact B-rep union of the straight-translating rectangular payload envelope against fixed feed-state geometry",
            "unresolved_penetrations": swept,
            "not_proven": "Nonlinear drive/index motion, contacts, arbitrary attitude or tolerance clearance",
        },
        "limitations": [
            "Discrete nominal B-rep stations, not continuous clearance or contact verification",
            "Actuator/sensor envelopes excluded from material mass; no installed mass claim",
            "No approved satellite interface, hardware reliability or manufacturing release",
            "Every positive-volume intersection retained; no default intended-contact waiver",
        ],
    }
    (OUT / (stem + "_report.json")).write_text(json.dumps(report, indent=2) + "\n")
    App.closeDocument(doc.Name)
    print(
        stem,
        "parts",
        len(rows),
        "modeled material kg",
        round(report["modeled_material_kg"], 3),
        "payload overlaps",
        sum(s["unresolved_payload_intersections"] for s in collisions),
        flush=True,
    )
    return report


if __name__ == "__main__":
    results = []
    for c in CANDIDATES:
        for spec in P["payloads"]:
            results.append(export(c, spec["length_mm"], spec["class"]))
    files = {
        f.name: hashlib.sha256(f.read_bytes()).hexdigest()
        for f in OUT.iterdir()
        if f.suffix in [".FCStd", ".step"] or f.name.endswith("_report.json")
    }
    (OUT / "CAD_REPORT.json").write_text(
        json.dumps(
            {"revision": P["revision"], "reports": results, "artifact_sha256": files},
            indent=2,
        )
        + "\n"
    )
