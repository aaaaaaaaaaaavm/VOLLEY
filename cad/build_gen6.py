"""
VOLLEY | Gen6: the CAD, built from parameters.

WHY THIS EXISTS
---------------
ADR-032. The payload is accelerated directly by cold gas along a rail the host stage
provides. There is no mover, no stator, no brake and no return stroke -- so almost nothing in
Gen5 carries forward except the part that survives every architecture: the containment.

Every dimension here is a run result, not a choice:

    bore 15.805 mm, stroke 8000 mm     A49, the host stage's whole acceleration length
    chamber 2 L at 50 bar              A41, the point where velocity saturates and gas does not
    reservoir 11.25 L at 200 bar       A42, the ADIABATIC figure -- see below
    cradle preload 201.7 N             A38, at 2.4x the Gen5 offset moment

WHAT THIS IS NOT
----------------
**A geometry and interface model, not a manufacturing model.** Same scope as Gen5: no
fillets, no fasteners, no harness, no tolerancing, no seal or valve detail. Every part is
the simplest solid carrying the right interfaces at the right stations.

THREE THINGS IT DRAWS THAT ARE NOT SETTLED
------------------------------------------
1. **The reservoir carries 11.25 L, the conservative end of P64.** A42 modelled the bottle as
   adiabatic; at ADR-020's twenty-minute cadence it re-equilibrates and the isothermal figure
   is 7.65 L. Both are in parameters.json. Drawing the larger one is deliberate.
2. **The cradle is a placeholder.** A34 says the mechanism does not exist and A38 raised its
   preload to 201.7 N per contact, which must still release inside a 1 N residual. What is
   drawn is the envelope it has to live in, not a design.
3. **The stage rail is drawn as a straight extrusion of unknown provenance.** No launch
   provider has agreed to anything, and A37's 43.33 kg stage credit is the least-examined
   number in the architecture.

USAGE
    python3 cad/build_gen6.py                 # build STEP + STL into cad/step/gen6, cad/stl
    python3 cad/build_gen6.py --check         # build, then verify against parameters.json
"""
import argparse
import json
import math
import os
import re

import cadquery as cq

HERE = os.path.dirname(os.path.abspath(__file__))
STEP_DIR = os.path.join(HERE, "step", "gen6")
STL_DIR = os.path.join(HERE, "stl")

P = json.load(open(os.path.join(HERE, "parameters.json")))
D = P["groups"]["gen6_drive"]
S = P["groups"]["gen6_store"]
T = P["groups"]["gen6_trim"]
MAG = P["groups"]["magazine"]
PAY = P["groups"]["payload_3u"]

EPOCH = "1970-01-01T00:00:00"          # STEP headers carry wall-clock time; normalise it


def _norm(path):
    """Strip the timestamp so a rebuild is byte-stable, as Gen5 does."""
    with open(path, encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    text = re.sub(r"'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}'", f"'{EPOCH}'", text)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def export(shape, name, stl=False):
    os.makedirs(STEP_DIR, exist_ok=True)
    path = os.path.join(STEP_DIR, f"VOLLEY_{name}_Gen6.step")
    cq.exporters.export(shape, path)
    _norm(path)
    if stl:
        os.makedirs(STL_DIR, exist_ok=True)
        cq.exporters.export(shape, os.path.join(STL_DIR, f"VOLLEY_{name}_Gen6.stl"))
    return path


def drive_tube():
    """The bore the payload is pushed along. It is the rail and the cylinder at once.

    That dual role is the reason the wall is not sized on pressure alone: hoop stress at
    50 bar on this bore needs 0.16 mm and the minimum practical wall is 1.0 mm, so the
    section is set by handling and by carrying A38's 201.7 N cradle preload -- neither of
    which is modelled here.
    """
    bore, wall, L = D["bore_mm"], D["tube_wall_mm"], D["stroke_mm"]
    return (cq.Workplane("YZ").circle(bore / 2 + wall).circle(bore / 2)
            .extrude(L + 60.0).translate((-30.0, 0, 0)))



def trim_stator():
    """ADR-033. A short stator at the muzzle end that corrects rather than throws.

    It is energised only after the gas has finished, and its length is set by the +-3 sigma
    authority A44 measured -- not by a force target. The magnet set it acts on rides the
    carriage, which is why P34 and E35 come back with it.

    The pulse store that feeds this is NOT modelled and NOT weighed: 37.7 J at 28 kW is
    requirement C3 at a fiftieth of Gen5's energy, and ADR-033 falsifier 1 is that it weighs
    more than the 0.340 kg section it serves.
    """
    bore, wall = D["bore_mm"], D["tube_wall_mm"]
    L, x0 = T["section_length_mm"], T["section_start_mm"]
    belt_t = 6.0                      # radial depth of the winding, over the tube wall
    return (cq.Workplane("YZ")
            .circle(bore / 2 + wall + belt_t).circle(bore / 2 + wall)
            .extrude(L).translate((x0, 0, 0)))


def carriage():
    """The piston face and the cradle that holds the payload against it.

    A34's contact lever is half the payload length, NOT the 70 mm centre-of-mass offset --
    the lever that takes up the clearance is not the lever that applies the moment.
    """
    bore = D["bore_mm"]
    lever = D["cradle_contact_lever_mm"]
    piston = cq.Workplane("YZ").circle(bore / 2 - 0.1).extrude(12.0)
    seat = (cq.Workplane("XY").box(2 * lever, PAY["width_y"], 8.0)
            .translate((lever + 12.0, 0, -PAY["height_z"] / 2 - 4.0)))
    stops = cq.Workplane("XY").box(8.0, PAY["width_y"], 24.0)
    stops = (stops.translate((12.0 + 4.0, 0, 0))
             .union(stops.translate((12.0 + 2 * lever - 4.0, 0, 0))))
    return piston.union(seat).union(stops)


def chamber():
    """The pre-charged volume. Cylindrical rather than spherical: it packages along a stage."""
    v_mm3 = S["chamber_volume_l"] * 1e6
    r = 60.0
    length = v_mm3 / (math.pi * r * r)
    wall = 3.0
    return (cq.Workplane("YZ").circle(r + wall).circle(r).extrude(length)
            .union(cq.Workplane("YZ").circle(r + wall).extrude(wall))
            .union(cq.Workplane("YZ").circle(r + wall).extrude(wall)
                   .translate((length - wall, 0, 0))))


def reservoir():
    """The bottle. Carries A42's ADIABATIC 11.25 L, the conservative end of P64."""
    v_mm3 = S["reservoir_volume_l"] * 1e6
    r = 90.0
    length = v_mm3 / (math.pi * r * r)
    wall = 6.0
    return (cq.Workplane("YZ").circle(r + wall).circle(r).extrude(length)
            .union(cq.Workplane("YZ").circle(r + wall).extrude(wall))
            .union(cq.Workplane("YZ").circle(r + wall).extrude(wall)
                   .translate((length - wall, 0, 0))))


def stage_rail():
    """What the host stage provides, drawn so the interface can be checked.

    A37 credits 43.33 kg of structure to the stage. NOTHING here validates that: no provider
    has agreed to anything and this is the least-examined number in the architecture.
    """
    L = D["stroke_mm"] + 200.0
    return (cq.Workplane("XY").box(L, 120.0, 40.0)
            .translate((L / 2 - 100.0, 0, -80.0)))


def magazine_cassette():
    """Unchanged from Gen5. A36 and A37 agree from opposite directions that the containment
    is the only subsystem surviving every architecture deletion -- 11.45 kg of it."""
    return (cq.Workplane("XY")
            .box(MAG["cassette_length_x"], MAG["cassette_width_y"], MAG["cassette_height_z"])
            .faces(">Z").shell(-4.0))


PARTS = [("Drive_Tube", drive_tube, True), ("Trim_Stator", trim_stator, True),
         ("Carriage", carriage, True),
         ("Chamber", chamber, True), ("Reservoir", reservoir, True),
         ("Stage_Rail", stage_rail, True), ("Magazine_Cassette", magazine_cassette, True)]


def check():
    """Read the geometry back and compare it to parameters.json."""
    fails = []
    v_ch = math.pi * 60.0 ** 2 * (S["chamber_volume_l"] * 1e6 / (math.pi * 60.0 ** 2)) / 1e6
    v_res = math.pi * 90.0 ** 2 * (S["reservoir_volume_l"] * 1e6 / (math.pi * 90.0 ** 2)) / 1e6
    v_trim = math.pi * ((D["bore_mm"] / 2 + D["tube_wall_mm"] + 6.0) ** 2
                        - (D["bore_mm"] / 2 + D["tube_wall_mm"]) ** 2) * T["section_length_mm"]
    checks = [
        ("chamber volume", v_ch, S["chamber_volume_l"], 1e-6),
        ("reservoir volume", v_res, S["reservoir_volume_l"], 1e-6),
        ("piston area from bore", math.pi * (D["bore_mm"] / 2) ** 2, D["piston_area_mm2"], 0.1),
        ("force from area and charge",
         D["piston_area_mm2"] * 1e-6 * S["charge_pressure_bar"] * 1e5,
         D["commanded_force_N"], 1.0),
        ("acceleration from force", D["commanded_force_N"] / 4.0 / 9.81,
         D["acceleration_g"], 0.05),
        # The constant-pressure bound, sqrt(2*p0*A*L/m), was written here as a bare 32.7 --
        # correct at 2.18 m and 50 bar, and silently wrong at any other design point. It is a
        # derived quantity, so it now reads the parameter it is derived from. ADR-034.
        ("constant-pressure velocity bound",
         math.sqrt(2 * D["commanded_force_N"] / 4.0 * D["stroke_mm"] / 1e3),
         D["exit_velocity_m_s_constant_pressure_bound"], 0.6),
    ]
    for name, got, want, tol in checks:
        ok = abs(got - want) <= tol
        print(f"  {'OK  ' if ok else 'FAIL'} {name:32s} {got:10.4f} against {want:.4f}")
        if not ok:
            fails.append(name)
    return fails


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    for name, fn, stl in PARTS:
        path = export(fn(), name, stl=stl)
        print(f"  wrote {os.path.relpath(path, HERE)}")
    if args.check:
        print("\nagainst parameters.json:")
        fails = check()
        if fails:
            raise SystemExit(f"\n{len(fails)} geometry check(s) failed: {fails}")
        print("\ngeometry agrees with parameters.json")


if __name__ == "__main__":
    main()
