"""
Do the Phase II items combine? Three findings, two of them supersessions.

WHY THIS EXISTS
---------------
Phase II holds eighteen deferred items, each sized on its own. Nothing had ever asked whether
they interact -- and two of them turn out to be alternatives rather than complements, which is
only visible once PII-18 puts a 0.6 kg shuttle where a 9.445 kg sled used to be.

    1. PII-1's lever IS the mover's mass. Make the mover light and it collapses.
    2. PII-15 exists to shorten the machine. Spending the unused qualification margin does
       the same thing without a cable over a sheave.
    3. The combination closes kill criterion 2, which has been crossed or unevaluable since
       the envelope was first drawn.

**SKETCH, NOT VALIDATION.** No band is declared for anything here. The mass rollup in
particular is a scaling argument over `mass_properties.py`'s own lumps, not a re-run of it.

Provenance: model output, from committed values. Nothing measured. E4 stands.
"""
import json
import math
import os

import mass_properties as mp
import motor_model as mm

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

G_CAP = 25.0                       # payload qualification acceleration cap
OVERHEAD_M = 1.839 - 1.300         # everything in the closed envelope that is not the stroke
ESPA_GRANDE_M = 1.270
BRAKE_GEN5_M = 0.240               # regen + arrest run-out today
SHUTTLE_KG = 0.60                  # PII-18 plate + pusher + latch, generous
PII1_SPRING_J = 41.8               # as sized in DESIGN_OPTIONS_exit_velocity.md


def kick(E, M, m=None):
    """Velocity a momentum-conserving spring adds, PII-1.

    Conserving momentum and adding E to the pair gives dv = sqrt(2 E M / (m (M+m))).
    **The mover's mass is the lever**, which is why this interacts with PII-18 at all.
    """
    m = mm.M_SAT if m is None else m
    return math.sqrt(2 * E * M / (m * (M + m)))


def kick_energy(dv, M, m=None):
    """Energy needed for a given kick -- the inverse, and the number that kills PII-1."""
    m = mm.M_SAT if m is None else m
    return 0.5 * m * dv * dv * (m / M + 1)


def stroke_for(v, a_g):
    """Acceleration zone needed to reach v at a given payload acceleration."""
    return v * v / (2 * a_g * 9.81)


def envelope(v, a_g, brake_m):
    """Closed envelope, holding everything that is not the stroke at its Gen5 value."""
    return stroke_for(v, a_g) + (OVERHEAD_M - BRAKE_GEN5_M + brake_m)


def brake_runout(mover_kg, v, g_arrest=200.0):
    return v * v / (2 * g_arrest * 9.81), mover_kg * g_arrest * 9.81


def mass_sketch(L_new, L_old=1.300, shuttle=SHUTTLE_KG, iron_add=3.0):
    """Scaling sketch over mass_properties' own lumps. NOT a re-run of the rollup."""
    m_tot, _, _ = mp.build()
    scale = L_new / L_old
    d = {}
    for name, m, _ in mp.parts:
        if name.startswith('Sled'):
            d[name] = -m
        elif 'brake' in name.lower():
            d[name] = -m * 0.75
        elif name.startswith(('Track longerons', 'Stator copper', 'Stator formers')):
            d[name] = -m * (1 - scale)
        elif name.startswith('Panels'):
            d[name] = -m * 0.25
        elif name.startswith('Supercapacitor'):
            d[name] = -m * 0.45
    net = sum(d.values()) + iron_add + shuttle
    return dict(lumps=d, iron_add=iron_add, shuttle=shuttle, net_kg=net,
                dry_before=m_tot, dry_after=m_tot + net)


if __name__ == '__main__':
    ref = mm.shot(mm.thrust_constant()[0])
    out = {}

    print("1. PII-1 is superseded by PII-18, and the reason is arithmetic\n")
    print(f"   {'mover':>36} {'M, kg':>7} {'dv from 41.8 J':>15} {'E for 3.83 m/s':>15}")
    p1 = []
    for name, M in (("Gen5 sled, what PII-1 was sized on", mm.M_SLED),
                    ("PII-18 shuttle + pusher + latch", SHUTTLE_KG),
                    ("PII-18 bare plate", 0.398)):
        row = dict(mover=name, M_kg=M, dv=kick(PII1_SPRING_J, M),
                   E_for_3p83=kick_energy(3.83, M))
        p1.append(row)
        print(f"   {name:>36} {M:7.3f} {row['dv']:12.2f} m/s {row['E_for_3p83']:12.0f} J")
    out['pii1'] = p1
    print("\n   PII-1 is the project's self-declared strongest idea and it buys 3.83 m/s for")
    print("   41.8 J -- but only because it is levering a 9.445 kg sled. On a 0.6 kg shuttle")
    print("   the same spring buys 1.65 m/s, and matching the original costs 225 J.")
    print("   PII-18 delivers the same exit velocity by not wasting the energy in the first")
    print("   place, and adds NO mechanism to the release path -- which is PII-1's own")
    print("   stated reason for being Phase II.\n")

    print("2. PII-15 is superseded too, by the qualification margin nobody is spending\n")
    print(f"   Gen5 runs at {ref['a_g']:.1f} g of a {G_CAP:.0f} g budget. That was never a")
    print("   choice: it is where thrust over mass landed with a 9.445 kg sled aboard.\n")
    print(f"   {'target v':>9} {'a, g':>6} {'accel zone':>11} {'vs 1.30 m':>10}")
    st = []
    for v in (ref['v_exit'], 20.0):
        for g in (ref['a_g'], 16.1, 21.6, G_CAP):
            L = stroke_for(v, g)
            st.append(dict(v=v, a_g=g, stroke_m=L))
            print(f"   {v:8.2f} {g:6.1f} {L*1e3:9.0f} mm {L/1.30:9.2f}x")
        print()
    out['stroke'] = st
    print("   PII-15's 2:1 reeving was 'the only lever found that shortens the machine")
    print("   without lengthening anything else', 1.30 m -> 0.65 m. The margin does the")
    print("   same for free, and without a cable over a sheave -- which REV-07 records")
    print("   cannot claim the exemption that screened out the rack (E21, and another")
    print("   manifest-forfeiting element for E30).\n")

    print("3. And together they close kill criterion 2\n")
    ro, F = brake_runout(SHUTTLE_KG, 20.26)
    print(f"   brake run-out falls {BRAKE_GEN5_M*1e3:.0f} -> {ro*1e3:.0f} mm because the "
          f"mover is {SHUTTLE_KG} kg, not {mm.M_SLED} ({F:.0f} N at a 200 g arrest)")
    print(f"   Gen5: 1300 mm stroke + {OVERHEAD_M*1e3:.0f} mm overhead = 1839 mm, "
          f"{100*(1.839/ESPA_GRANDE_M-1):.0f} % over ESPA-Grande\n")
    print(f"   {'configuration':>34} {'stroke':>9} {'envelope':>10}  verdict")
    env = []
    for label, v, g in (("Gen5 velocity at 16.1 g", ref['v_exit'], 16.1),
                        ("Gen5 velocity at 21.6 g", ref['v_exit'], 21.6),
                        ("20 m/s at 21.6 g", 20.0, 21.6)):
        e = envelope(v, g, ro)
        env.append(dict(label=label, v=v, a_g=g, envelope_m=e, fits=bool(e < ESPA_GRANDE_M)))
        verdict = "FITS ESPA-Grande" if e < ESPA_GRANDE_M else f"{100*(e/ESPA_GRANDE_M-1):.0f} % over"
        print(f"   {label:>34} {stroke_for(v,g)*1e3:6.0f} mm {e*1e3:7.0f} mm  {verdict}")
    out['envelope'] = env

    ms = mass_sketch(stroke_for(ref['v_exit'], 16.1))
    out['mass_sketch'] = ms
    print(f"\n4. mass, as a scaling SKETCH over mass_properties' own lumps")
    print(f"   dry {ms['dry_before']:.1f} -> {ms['dry_after']:.1f} kg  ({ms['net_kg']:+.1f})")
    print(f"   per 3U satellite {ms['dry_before']/12:.3f} -> {ms['dry_after']/12:.3f} kg "
          f"(threshold ~2 kg: still crossed, by {ms['dry_after']/12/2:.1f}x not "
          f"{ms['dry_before']/12/2:.1f}x)")
    print(f"   per PocketQube 1P at 288 per load (A24): {ms['dry_after']/288:.3f} kg -- "
          f"passes by {2/(ms['dry_after']/288):.0f}x")

    os.makedirs(RESULTS, exist_ok=True)
    out['caveat'] = ("SKETCH, NOT VALIDATION. No band is declared for anything here. The mass "
                     "figures are a scaling argument over mass_properties.py's lumps, not a "
                     "re-run of the rollup.")
    json.dump(out, open(os.path.join(RESULTS, 'architecture_synthesis.json'), 'w'), indent=2)
    print("\n-> results/architecture_synthesis.json")
