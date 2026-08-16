"""
VOLLEY | Parametric solid mass properties.

Builds the dry-mass rollup from primitive solids and material densities rather
than from top-down estimates. Supersedes the earlier ~105 kg hand estimate
(legacy/c6_c10.py), chiefly because the ironless stator is far lighter than the
iron-core figure first assumed.

Reproduces (paper Sec. V-D):
    dry mass        76.5 kg
    loaded (12x3U)  124.5 kg
    CG              0.44 m from breech
    sled assembly   9.45 kg   <- CAD solid-volume result (P15); feeds motor_model.py

The first three moved when the D6 -> D9 gate resize and the sled CAD reconciliation
landed; this header had kept the pre-reconciliation 72.3 / 120.3 / 0.46 until 2026-08-10.
A docstring is the first thing anyone reads about a script, so it is worth as much as the
code under it.

LIMITATION: these are parametric primitives with shell/fill factors, NOT CAD.
Treat as estimates with perhaps +/-15 % spread until real geometry exists.
Inertia tensor is NOT computed here (only mass and CG along the track axis).

Provenance: model output, not independently re-derived.
No component mass has been checked against a vendor datasheet.
"""
import json
import os

# Outputs go next to this script, not next to whoever ran it. Every script here used to
# write to a cwd-relative "results/", so running one from the repository root created a
# SECOND, silently stale copy of its JSON at the root -- which is exactly what happened on
# 2026-07-30 and left a results/sizing.json carrying a superseded inter-array force. A
# duplicate that nothing regenerates is the defect class this repository logs twice
# already (P16, P19).
RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

# densities, kg/m^3
AL, TI, CU, PEEK, NDFEB, STEEL = 2700, 4430, 8960, 1320, 7500, 7800

parts = []  # (name, mass_kg, cg_x_m_from_breech)

# Measured from the Gen3 STEP solids (P15), superseding the parametric sled estimate
# below as the value motor_model.M_SLED uses. As-drawn and unpocketed.
SLED_CAD_MASS = 9.445


def box(name, L, W, H, rho, cg, wall=None, n=1, fill=1.0):
    if wall:
        V = (L * W * H - L * (W - 2 * wall) * (H - 2 * wall)) * n
    else:
        V = L * W * H * n
    m = V * rho * fill
    parts.append((name, m, cg))
    return m


def lump(name, m, cg):
    parts.append((name, m, cg))
    return m


def build():
    parts.clear()
    box('Track longerons (2x Al box section)', 1.55, 0.045, 0.065, AL, 0.75, wall=0.004, n=2)
    box('Stator copper (1.3 m, 60% fill)', 1.30, 0.090, 0.010, CU, 0.65, fill=0.60)
    box('Stator formers / potting (PEEK eq.)', 1.30, 0.090, 0.014, PEEK, 0.65, fill=0.45)
    box('Sled Halbach magnets (2 faces)', 0.34, 0.090, 0.008, NDFEB, 0.15, n=2)
    box('Sled Ti chassis (shell equivalent)', 0.36, 0.110, 0.012, TI, 0.15, fill=0.35)
    lump('Sled rollers / latch / backstop', 0.45, 0.15)
    box('Eddy brake magnets + yoke', 0.10, 0.09, 0.030, STEEL, 1.42, fill=0.80)
    lump('Fixed brake hardware + ring spring (moving Cu fin is in sled)', 0.856, 1.40)
    box('Cassette shells (2x Al sheet eq.)', 0.66, 0.115, 0.36, AL, 0.35, n=2, fill=0.06)
    lump('Followers, gates, escapements (2x)', 2.60, 0.30)
    lump('Supercapacitor cells + busbars', 6.50, 0.10)
    lump('PPU (SiC bridge, filters)', 4.00, 0.10)
    lump('Battery + avionics + IMU', 5.50, 0.12)
    lump('Harness', 2.50, 0.60)
    lump('Thermal (pipes, radiator, MLI)', 6.00, 0.70)
    lump('ESPA bracket + fasteners', 9.00, 0.35)
    lump('Panels / closeouts', 5.50, 0.75)
    # P10, CLOSED 2026-08-16 by A46. What stood here until today was an 8.0 kg PLACEHOLDER
    # with no derivation, entered on 2026-08-13 because a number carrying a caveat is
    # auditable and a hole is not, and chosen as the lean end of a range KILL_CRITERIA.md
    # had already put at a plausible 20 kg. A46 built the enclosure up from the geometry in
    # cad/parameters.json -- 6.077 m2 of skin after three apertures -- and the five lines
    # below replace it. THE PLACEHOLDER WAS LOW BY 6.3x.
    #
    # These are the MONOLITHIC 2 mm aluminium skins that cad/parameters.json specifies. A
    # honeycomb sandwich at 3.0 kg/m2 gives 29.98 kg for the same five lines; adopting one
    # is a DESIGN DECISION this project has not taken, and it is not taken here.
    # validation/A46_enclosure_buildup.md.
    lump('Enclosure skins (2 mm Al, 6.077 m2 net, A46)', 32.82, 0.50)
    lump('Enclosure frames and ribs (A46, 25 % of skin, declared)', 8.20, 0.50)
    lump('Radiator (1600 x 200 x 3 mm Al, A46)', 2.59, 0.45)
    lump('Equipment-bay boxes (4 bays, 1.5 mm Al, A46)', 1.87, 0.30)
    lump('Fasteners and brackets (A46, 10 % of structure, declared)', 4.55, 0.50)

    # The three 'Sled ...' lines above are the parametric estimate, kept visible for
    # the audit trail. Exact OCC solid volumes from cad/step/gen3/EMOCD_Sled_Gen3.step
    # give 9.445 kg (P15) -- the plates are drawn solid, with no pocketing. The rollup
    # therefore understated system dry mass by the same difference, so the delta is
    # carried as its own line rather than by editing the parametric parts.
    sled_parametric = sum(p[1] for p in parts if p[0].startswith('Sled'))
    lump('Sled CAD reconciliation (P15, CAD-derived 9.445 kg)',
         SLED_CAD_MASS - sled_parametric, 0.15)

    m_tot = sum(p[1] for p in parts)
    cg = sum(p[1] * p[2] for p in parts) / m_tot
    sled = sum(p[1] for p in parts if p[0].startswith('Sled'))
    return m_tot, cg, sled


if __name__ == '__main__':
    m_tot, cg, sled = build()
    print(f"{'part':40s} {'kg':>7s} {'cg_x m':>8s}")
    for n, m, c in parts:
        print(f"{n:40s} {m:7.2f} {c:8.2f}")
    print(f"\nDRY TOTAL       {m_tot:6.1f} kg")
    print(f"LOADED (12x4kg) {m_tot + 48:6.1f} kg")
    print(f"CG from breech  {cg:6.2f} m")
    sled_parametric = sum(m for n, m, _ in parts
                          if n.startswith('Sled') and 'reconciliation' not in n)
    print(f"Sled assembly   {sled:6.2f} kg  (CAD-derived, P15; feeds motor_model.M_SLED)")
    print(f"  parametric    {sled_parametric:6.2f} kg  (superseded, kept for the record)")

    res = dict(dry_kg=round(m_tot, 1), loaded_kg=round(m_tot + 48, 1),
               cg_m=round(cg, 2), sled_kg=round(sled, 2),
               sled_parametric_kg=round(sled_parametric, 2),
               parts=[[n, round(m, 2), c] for n, m, c in parts])
    os.makedirs(RESULTS, exist_ok=True)
    json.dump(res, open(os.path.join(RESULTS, 'mass_properties.json'), 'w'), indent=2)
    print("\n-> results/mass_properties.json")
