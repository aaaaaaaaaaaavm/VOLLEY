"""
VOLLEY | Gen6 sizing: the satellite's own CDS corner rails as the motor secondary.

THE IDEA
--------
The CubeSat Design Specification has required, since 2003, four hard-anodised **aluminium
corner rails** on every CubeSat. Their stated purpose is to be pushed and guided by a
deployer. They are standardised in dimension and material class, they are structural, they
run the full length of the satellite, they are symmetric about its axis, and under the
anodising they are bare conductive aluminium.

That is, by accident, a **linear induction motor secondary that every customer already owns,
already qualifies, and already flies.** Every deployer ever built treats it as a bearing
surface. None has used it as an armature.

If the drive couples to the rails, then:
  * there is no sled -- the satellite IS the mover;
  * there is nothing to arrest, so there is no brake;
  * nothing is added to the satellite, so "unmodified" stops being a claim to defend and
    becomes a consequence of the topology.

WHAT THIS FILE IS AND IS NOT
----------------------------
**Sizing, not validation.** No acceptance band has been declared for any number here and none
is claimed. It answers one question -- is the thrust in the right order of magnitude -- and
the honest answer to "is this real" is A30, which does not exist yet.

**REJECTED 2026-08-13 BY A30 BAND 1. THIS FILE IS KEPT AS THE RECORD OF A FAILED PROPOSAL.**

`EDGE` derated the ideal sheet-secondary thrust for the transverse edge effect and assumed
**0.55**, declared here as the number most likely to be wrong and the one the whole result
scaled on. `analysis/edge_effect.py` measured it: **0.0253**, a factor of 22 out. Four rails at a
generous 0.60 T make **41.9 N** against the 413 N required. The architecture does not close, and
no pole pitch rescues it -- the edge factor wants the secondary wide against the pole pitch and
the airgap wants the pole pitch large against the gap, and an 8.5 mm conductor in a 10.5 mm gap
demands both at once.

`EDGE` below is set to the measured value, so running this file now reports the rejection rather
than the proposal. The original assumption is recorded above rather than deleted. See
`validation/A30_rail_drive.md` and **P49**.

Provenance: model output, first-principles. Nothing here is measured. E4 stands.
"""
import json
import math
import os

import motor_model as mm

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
MU0 = 4e-7 * math.pi

# CubeSat Design Specification, rev 14: corner rails, minimum 8.5 mm wide, hard-anodised,
# aluminium 7075 or 6061. Length is the satellite's long dimension.
RAIL_W = 0.0085
RAIL_LEN = 0.3405                 # m, 3U
N_RAILS = 4
A_COUPLE = N_RAILS * RAIL_W * RAIL_LEN

RHO_AL, CP_AL = 2700.0, 900.0
RAIL_KG = N_RAILS * RAIL_W * RAIL_W * RAIL_LEN * RHO_AL

# Alloy conductivity. THRUST IS ALLOY-INDEPENDENT at the operating point below -- only the
# slip loss changes -- which is a robustness property worth having, because a deployer does
# not get to choose what its customers' rails are made of.
ALLOYS = {'6061-T6': 2.5e7, '7075-T6': 1.9e7}

EDGE = 0.0253                     # MEASURED by edge_effect.py, A30 band 1.
                                  # Was assumed 0.55 -- wrong by 22x. See P49.
G_QUAL = 25.0                     # payload qualification acceleration cap
CONV_EFF = 0.90                   # converter + copper, stated


def magnetic_pressure(Bg):
    """The thrust ceiling of any induction machine: B^2/2mu0, derated for edge effect."""
    return Bg * Bg / (2 * MU0) * EDGE


def goodness(w, sigma, tau, gap):
    """LIM goodness factor. Double-sided stator straddling the rail, so the magnetic gap is
    two mechanical clearances PLUS the rail: aluminium is non-magnetic and counts as gap."""
    g_e = 2 * gap + RAIL_W
    k = math.pi / tau
    delta = math.sqrt(2 / (w * MU0 * sigma))
    t_eff = min(RAIL_W, 2 * delta)
    return MU0 * w * sigma * t_eff / (k * k * g_e), g_e, delta, t_eff


def stroke(Bg, tau, gap, sigma, m=None, L=None, dt=2e-4):
    """Integrate one shot holding G*s = 1, the machine's own thrust maximum.

    At G*s = 1 thrust sits at the magnetic pressure independently of speed, so the drive holds
    it by raising frequency and lowering slip as the satellite accelerates -- an ordinary VFD
    schedule. Energising only the section under the satellite is what ADR-022's segmented
    stator already provides.
    """
    m = mm.M_SAT if m is None else m
    L = mm.ACCEL_ZONE if L is None else L
    F = min(magnetic_pressure(Bg) * A_COUPLE, G_QUAL * 9.81 * m)
    v = x = t = E_mech = E_slip = 0.0
    f = s = G = 0.0
    while x < L:
        w = 2 * math.pi * max(v / (2 * tau), 20.0)
        for _ in range(3):                     # slip and frequency are coupled; settle them
            G, _, _, _ = goodness(w, sigma, tau, gap)
            s = 1.0 / G if G > 1 else 1.0
            v_s = v / (1 - s) if s < 1 else max(2 * v, 1.0)
            w = 2 * math.pi * v_s / (2 * tau)
        f = w / (2 * math.pi)
        v += F / m * dt
        x += v * dt
        t += dt
        E_mech += F * v * dt
        E_slip += F * (v_s - v) * dt
    E_in = (E_mech + E_slip) / CONV_EFF
    return dict(F_N=F, a_g=F / m / 9.81, v_exit=v, t_ms=t * 1e3, f_max_Hz=f,
                slip_end=s, G_end=G, E_mech_J=E_mech, E_slip_J=E_slip, E_in_J=E_in,
                eff_slip_pct=100 * E_mech / (E_mech + E_slip),
                eff_overall_pct=100 * E_mech / E_in,
                rail_dT_K=E_slip / (RAIL_KG * CP_AL))


if __name__ == '__main__':
    Kt, _ = mm.thrust_constant()
    ref = mm.shot(Kt)
    m_move_today = mm.M_SAT + mm.M_SLED

    print("Gen6 sizing: the satellite's own CDS rails as the secondary\n")
    print(f"coupling area   {A_COUPLE*1e4:.1f} cm2  ({N_RAILS} rails x {RAIL_W*1e3:.1f} mm "
          f"x {RAIL_LEN*1e3:.1f} mm)")
    print(f"rail mass       {RAIL_KG*1e3:.0f} g of aluminium the satellite already carries")
    print(f"edge derating   {EDGE}  <- the largest assumption in this file\n")
    print(f"TODAY: {ref['v_exit']:.2f} m/s at {ref['a_g']:.1f} g, {ref['E_drawn']:.0f} J drawn, "
          f"moving mass {m_move_today:.2f} kg of which {mm.M_SLED} kg is sled")
    print(f"       payload gets {ref['KE_payload']:.0f} J = "
          f"{100*ref['KE_payload']/ref['E_drawn']:.1f} % of what is drawn\n")

    print(f"{'Bg,T':>5} {'tau':>6} {'gap':>5} {'alloy':>9} {'F,N':>6} {'a/g':>5} {'v,m/s':>7} "
          f"{'t,ms':>6} {'f,Hz':>6} {'slip%':>6} {'E_in,J':>7} {'rail dT':>8}")
    rows = []
    for Bg in (0.35, 0.45, 0.60):
        for tau in (0.036, 0.048):
            for alloy, sigma in ALLOYS.items():
                r = stroke(Bg, tau, 0.002, sigma)
                r.update(Bg_T=Bg, tau_m=tau, gap_m=0.002, alloy=alloy)
                rows.append(r)
                print(f"{Bg:5.2f} {tau*1e3:5.0f}mm {2.0:4.1f}mm {alloy:>9} {r['F_N']:6.0f} "
                      f"{r['a_g']:5.1f} {r['v_exit']:7.2f} {r['t_ms']:6.1f} {r['f_max_Hz']:6.0f} "
                      f"{100*r['slip_end']:6.1f} {r['E_in_J']:7.0f} {r['rail_dT_K']:6.1f} K")

    # The design point this file argues for: modest flux, a realistic 2 mm clearance, and the
    # worse of the two alloys, so nothing rests on getting a customer's metallurgy lucky.
    pick = stroke(0.45, 0.048, 0.002, ALLOYS['7075-T6'])
    print(f"\nDESIGN POINT  Bg 0.45 T, tau 48 mm, 2.0 mm clearance, worst-case 7075 rails:")
    print(f"  {pick['F_N']:.0f} N, {pick['a_g']:.1f} g, {pick['v_exit']:.2f} m/s in "
          f"{pick['t_ms']:.0f} ms, drive to {pick['f_max_Hz']:.0f} Hz")
    print(f"  {pick['E_in_J']:.0f} J drawn against today's {ref['E_drawn']:.0f} J "
          f"({ref['E_drawn']/pick['E_in_J']:.2f}x less), rails warm {pick['rail_dT_K']:.1f} K")
    print(f"  payload gets {pick['E_mech_J']:.0f} J = {pick['eff_overall_pct']:.1f} % of drawn, "
          f"against {100*ref['KE_payload']/ref['E_drawn']:.1f} % today")
    verdict = "FASTER" if pick['v_exit'] > ref['v_exit'] else "SLOWER"
    print(f"  and it is {verdict}: {pick['v_exit']:.2f} vs {ref['v_exit']:.2f} m/s "
          f"(moving mass {mm.M_SAT} kg against {m_move_today:.2f} kg)")
    if pick['F_N'] < ref['F_cmd']:
        print(f"\n  REJECTED: {pick['F_N']:.0f} N against the {ref['F_cmd']:.0f} N Gen5 "
              f"commands. A30 band 1 measured the edge factor at {EDGE}, not the 0.55 this "
              f"file assumed.")

    os.makedirs(RESULTS, exist_ok=True)
    json.dump(dict(coupling_area_m2=A_COUPLE, rail_kg=RAIL_KG, edge_derating=EDGE,
                   g_qual_cap=G_QUAL, converter_eff=CONV_EFF,
                   today=dict(v_exit=ref['v_exit'], a_g=ref['a_g'], E_drawn_J=ref['E_drawn'],
                              KE_payload_J=ref['KE_payload'], moving_mass_kg=m_move_today,
                              sled_kg=mm.M_SLED),
                   sweep=rows, design_point=dict(Bg_T=0.45, tau_m=0.048, gap_m=0.002,
                                                 alloy='7075-T6', **pick),
                   caveat=("SIZING, NOT VALIDATION. No acceptance band has been declared for "
                           "any figure here. The edge derating is the dominant assumption.")),
              open(os.path.join(RESULTS, 'rail_drive.json'), 'w'), indent=2)
    print("\n-> results/rail_drive.json")
