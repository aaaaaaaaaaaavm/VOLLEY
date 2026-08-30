"""A66: what the aluminium drive tube costs the trim stator.

ADR-033 puts the trim stator outside the tube and its magnets inside. ADR-035 then made the
tube aluminium. The tube never moves, so the stator's travelling field crosses it at FULL
SLIP on every shot, whatever the carriage is doing. That is a shorted turn by construction
and this file is the first in the repository to price it.

Two independent methods, because one is not a result.

    thin sheet   the wall lumped into a surface current. Closed form, valid while the wall is
                 thin against the skin depth, and the limit the textbook sheet-rotor result
                 gives for a linear machine.
    exact slab   the field resolved THROUGH the wall thickness by matching A and dA/dy at both
                 interfaces, with the diffusion equation solved inside the metal. Makes no thin
                 wall assumption and reduces to the sheet result when the wall is thin.

They share no expression. The slab route solves a two-interface boundary-value problem; the
sheet route solves a one-unknown self-consistency. Agreement between them is band 6.

Units are SI throughout.
"""
import cmath
import json
import math
import os
import sys

MU0 = 4.0e-7 * math.pi

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RESULTS = os.path.join(HERE, 'results')

P = json.load(open(os.path.join(ROOT, 'cad', 'parameters.json')))
G = P['groups']

# --- inputs, every one from the repository -------------------------------------------------
SIGMA_AL = 3.5e7                                   # S/m, SIG_AL in analysis/phase1_closeout.py
WALL_M = G['gen6_drive']['tube_wall_mm'] / 1e3
BORE_M = G['gen6_drive']['bore_mm'] / 1e3
V_SYNC = G['gen6_drive']['exit_velocity_m_s_zero_friction']
V_ADOPTED = G['gen6_drive']['exit_velocity_m_s']
WAVELENGTH_M = G['stator']['wavelength'] / 1e3
POLE_PITCH_M = G['stator']['pole_pitch'] / 1e3
ACTIVE_W_M = G['stator']['active_width_y'] / 1e3
SECTION_M = G['gen6_trim']['section_length_mm'] / 1e3
FORCE_N = G['gen6_trim']['force_N']
AUTHORITY_MS = G['gen6_trim']['authority_m_s']
SECTION_MASS_KG = G['gen6_trim']['added_mass_kg']
T_CEILING_K = G['gen6_drive']['tube_temperature_ceiling_K']
SHOTS = 12                                         # ADR-030 manifest
STROKE_M = 8.0                                     # ADR-034
PER_SAT_BASE_KG = 1.296                            # A49, the figure trim_authority.py adds to
N_MANIFEST = 12

# aluminium 6061-T6 thermal, handbook at room temperature. E4: nothing here is measured.
RHO_AL = G['gen6_drive']['tube_material_density_kg_m3']
CP_AL = 896.0                                      # J/(kg K)
T_START_K = 293.15


def k_wave(wavelength_m=WAVELENGTH_M):
    """Spatial wavenumber of the travelling field."""
    return 2.0 * math.pi / wavelength_m


def excitation_hz(v=V_SYNC, wavelength_m=WAVELENGTH_M):
    """What the STATIONARY wall sees. The tube never moves, so the slip is the whole of the
    synchronous speed. This is the frequency P92 asks for."""
    return v / wavelength_m


def skin_depth(sigma=SIGMA_AL, f=None, mu=MU0):
    if f is None:
        f = excitation_hz()
    return math.sqrt(2.0 / (2.0 * math.pi * f * mu * sigma))


def reynolds_sheet(sigma=SIGMA_AL, d=WALL_M, v=V_SYNC, mu=MU0):
    """Magnetic Reynolds number of the wall as a thin sheet, mu*sigma*d*v/2.

    Dimensionless: mu*sigma is s/m^2, times d is s/m, times v is 1. This, and not the skin
    depth, is what decides how much field reaches the magnets. A wall can be thin against the
    skin depth and still shield hard if it is moving fast relative to the field, which is
    exactly the case here because it is not moving at all.
    """
    return mu * sigma * d * v / 2.0


def transmission_sheet(sigma=SIGMA_AL, d=WALL_M, v=V_SYNC, mu=MU0):
    """Field at the magnets over field with no wall, thin-sheet limit. Conductive part only."""
    return 1.0 / complex(1.0, reynolds_sheet(sigma, d, v, mu))


def transmission_slab(sigma=SIGMA_AL, d=WALL_M, v=V_SYNC, wavelength_m=WAVELENGTH_M, mu=MU0):
    """Field at the magnets over field with no wall, exact through the thickness.

    Region 1 air, region 2 metal of thickness d, region 3 air. A travelling wave e^j(wt-kx)
    with A decaying away from the wall on both sides. Matching A and dA/dy at y=0 and y=d and
    eliminating the internal constants gives

        T = 1 / [ cosh(gamma d) + (gamma/k + k/gamma) sinh(gamma d) / 2 ]

    with gamma = sqrt(k^2 + j w mu sigma). At sigma = 0 this returns exp(-k d), which is the
    field a wall of that thickness costs by geometry alone with no conduction, so the ratio to
    exp(-k d) isolates what the CONDUCTIVITY costs. That normalisation is what makes this
    comparable with the sheet result, which carries no geometry.
    """
    k = k_wave(wavelength_m)
    w = 2.0 * math.pi * (v / wavelength_m)
    gamma = cmath.sqrt(complex(k * k, w * mu * sigma))
    r = gamma / k
    t_total = 1.0 / (cmath.cosh(gamma * d) + (r + 1.0 / r) * cmath.sinh(gamma * d) / 2.0)
    geometric = math.exp(-k * d)
    return t_total / geometric, t_total, geometric


def band1_verification():
    """Zero conductivity, and the sheet against the slab over two decades of conductance."""
    out = {}
    t0 = transmission_slab(sigma=0.0)
    out['zero_sigma_conductive_transmission'] = abs(t0[0])
    out['zero_sigma_is_unity'] = abs(abs(t0[0]) - 1.0) < 1e-12
    out['zero_sigma_total_equals_geometric'] = abs(abs(t0[1]) - t0[2]) < 1e-12

    decades = []
    worst = 0.0
    for scale in (1e-3, 1e-2, 1e-1, 1.0):
        s = SIGMA_AL * scale
        sheet = abs(transmission_sheet(sigma=s))
        slab = abs(transmission_slab(sigma=s)[0])
        rel = abs(sheet - slab) / slab
        worst = max(worst, rel)
        decades.append({'sigma_scale': scale, 'sigma_S_m': s, 'sheet': sheet,
                        'slab': slab, 'rel_diff': rel})
    out['decades'] = decades
    out['worst_rel_diff'] = worst
    out['pass_'] = (out['zero_sigma_is_unity'] and out['zero_sigma_total_equals_geometric']
                    and worst <= 0.005)
    return out


def airgap_flux_density():
    """Back out the working flux density from the force the section is specified to make.

    F = B * K * L * W with K the stator sheet current. Every term but B is in parameters.json,
    so B follows from the design rather than from an assumption about the magnets.
    """
    k_sheet = G['gen6_trim']['sheet_current_A_per_m']
    return FORCE_N / (k_sheet * SECTION_M * ACTIVE_W_M), k_sheet


def induced_loss_W(t_conductive, sigma=SIGMA_AL, d=WALL_M, v=V_SYNC):
    """Ohmic dissipation in the wall under the stator, from the field that is actually there.

    The wall carries an induced sheet current K = sigma * d * v * B_net, where B_net is the
    field after the wall's own reaction has reduced it. Using the unshielded field here is the
    common way to get a number several times too large, so B_net carries the transmission
    factor. Power is |K|^2 / (sigma d) per unit area over the stator footprint.
    """
    b_gap, _ = airgap_flux_density()
    b_net = b_gap * abs(t_conductive)
    k_induced = sigma * d * v * b_net
    p_area = k_induced ** 2 / (sigma * d)
    area = SECTION_M * ACTIVE_W_M
    return p_area * area, b_gap, b_net, k_induced


def wall_temperature(p_loss_W):
    """Rise over a 12-shot campaign, adiabatic in the heated ring.

    Adiabatic is the correct first bound. The shot lasts about four milliseconds and nothing in
    this repository establishes a conduction path or a radiator, so any cooling credit would be
    invented. The heated volume is the tube ring under the stator, not the stator footprint:
    the induced current closes around the tube.
    """
    dwell_s = SECTION_M / V_SYNC
    e_per_shot_J = p_loss_W * dwell_s
    ring_vol = math.pi * (BORE_M + WALL_M) * WALL_M * SECTION_M
    mass_kg = ring_vol * RHO_AL
    d_t_per_shot = e_per_shot_J / (mass_kg * CP_AL)
    return {'dwell_s': dwell_s, 'energy_per_shot_J': e_per_shot_J,
            'heated_ring_mass_kg': mass_kg, 'rise_per_shot_K': d_t_per_shot,
            'rise_campaign_K': d_t_per_shot * SHOTS,
            'peak_K': T_START_K + d_t_per_shot * SHOTS,
            'ceiling_K': T_CEILING_K,
            'within_ceiling': T_START_K + d_t_per_shot * SHOTS <= T_CEILING_K}


def build():
    f = excitation_hz()
    delta = skin_depth(f=f)
    rm = reynolds_sheet()
    t_sheet = transmission_sheet()
    t_slab_c, t_slab_total, geom = transmission_slab()

    # The slab is the reported answer. It makes no thin-wall assumption.
    att = abs(t_slab_c)

    delivered = AUTHORITY_MS * att
    growth = 1.0 / att
    section_needed_m = SECTION_M * growth
    pct_stroke = 100.0 * section_needed_m / STROKE_M
    mass_needed = SECTION_MASS_KG * growth
    per_sat = PER_SAT_BASE_KG + mass_needed / N_MANIFEST

    p_loss, b_gap, b_net, k_ind = induced_loss_W(t_slab_c)
    thermal = wall_temperature(p_loss)

    b1 = band1_verification()
    bands = [
        {'band': '1', 'name': 'model verification: zero-sigma unity, sheet against slab to 0.5 %',
         'detail': f"zero-sigma {b1['zero_sigma_conductive_transmission']:.6f}, "
                   f"worst sheet-slab {b1['worst_rel_diff']*100:.4f} % over 3 decades",
         'pass_': b1['pass_']},
        {'band': '2', 'name': 'REPORT: skin depth against the wall',
         'detail': f"f {f:.1f} Hz, delta {delta*1e3:.3f} mm, wall {WALL_M*1e3:.1f} mm "
                   f"= {WALL_M/delta:.3f} delta",
         'pass_': None},
        {'band': '3', 'name': 'the section as drawn still delivers 1.1543 m/s through the wall',
         'detail': f"delivers {delivered:.4f} m/s, {att*100:.2f} % of sized",
         'pass_': delivered >= AUTHORITY_MS},
        {'band': '4', 'name': 'compensated section stays within 15 % of the 8.0 m stroke',
         'detail': f"{section_needed_m*1e3:.2f} mm = {pct_stroke:.4f} % of stroke",
         'pass_': pct_stroke <= 15.0},
        {'band': '5', 'name': 'added mass per satellite with the compensated section <= 2.0 kg',
         'detail': f"{per_sat:.4f} kg (section {mass_needed:.4f} kg)",
         'pass_': per_sat <= 2.0},
        {'band': '6', 'name': 'independent implementation agrees on transmission within 10 %',
         'detail': f"sheet {abs(t_sheet):.6f}, slab {att:.6f}, "
                   f"{abs(abs(t_sheet)-att)/att*100:.4f} %",
         'pass_': abs(abs(t_sheet) - att) / att <= 0.10},
    ]

    return {
        'analysis': 'A66',
        'bands_declared_commit': 'a66-bands',
        'note': ('Tube shielding of the Gen6 trim stator. The wall is stationary so it sees '
                 'full slip. Two independent methods. Nothing measured, E4.'),
        'inputs': {'sigma_S_m': SIGMA_AL, 'wall_m': WALL_M, 'bore_m': BORE_M,
                   'v_sync_m_s': V_SYNC, 'wavelength_m': WAVELENGTH_M,
                   'section_m': SECTION_M, 'force_N': FORCE_N,
                   'authority_m_s': AUTHORITY_MS, 'section_mass_kg': SECTION_MASS_KG},
        'excitation_hz': f, 'skin_depth_m': delta, 'wall_in_skin_depths': WALL_M / delta,
        'reynolds_sheet': rm,
        'transmission': {'sheet_abs': abs(t_sheet), 'slab_conductive_abs': att,
                         'slab_total_abs': abs(t_slab_total), 'geometric_only': geom,
                         'sheet_slab_rel_diff': abs(abs(t_sheet) - att) / att},
        'authority': {'sized_m_s': AUTHORITY_MS, 'delivered_m_s': delivered,
                      'shortfall_m_s': AUTHORITY_MS - delivered,
                      'growth_factor': growth,
                      'section_needed_mm': section_needed_m * 1e3,
                      'pct_of_stroke': pct_stroke,
                      'section_mass_needed_kg': mass_needed,
                      'per_satellite_kg': per_sat},
        'loss': {'b_gap_T': b_gap, 'b_net_T': b_net, 'induced_sheet_current_A_m': k_ind,
                 'wall_loss_W': p_loss,
                 'against_peak_mechanical_W': G['gen6_trim']['peak_mechanical_W'],
                 'loss_over_mechanical': p_loss / G['gen6_trim']['peak_mechanical_W']},
        'thermal': thermal,
        'verification': b1,
        'bands': bands,
    }


def main():
    r = build()
    print(f"A66 tube shielding, wall {WALL_M*1e3:.1f} mm aluminium at {SIGMA_AL:.1e} S/m")
    print(f"  excitation {r['excitation_hz']:.1f} Hz, skin depth {r['skin_depth_m']*1e3:.3f} mm,"
          f" wall = {r['wall_in_skin_depths']:.3f} skin depths")
    print(f"  sheet magnetic Reynolds number {r['reynolds_sheet']:.4f}")
    t = r['transmission']
    print(f"  transmission: slab {t['slab_conductive_abs']:.4f}, sheet {t['sheet_abs']:.4f}, "
          f"differ {t['sheet_slab_rel_diff']*100:.3f} %")
    a = r['authority']
    print(f"  authority {a['delivered_m_s']:.4f} of {a['sized_m_s']:.4f} m/s sized; "
          f"section must grow {a['growth_factor']:.3f}x to {a['section_needed_mm']:.2f} mm "
          f"({a['pct_of_stroke']:.3f} % of stroke)")
    print(f"  per-satellite mass {a['per_satellite_kg']:.4f} kg")
    l, th = r['loss'], r['thermal']
    print(f"  wall loss {l['wall_loss_W']/1e3:.2f} kW against {l['against_peak_mechanical_W']/1e3:.1f} kW mechanical"
          f" ({l['loss_over_mechanical']*100:.1f} %)")
    print(f"  wall {th['rise_per_shot_K']:.2f} K per shot, {th['rise_campaign_K']:.1f} K over "
          f"{SHOTS}, peak {th['peak_K']:.1f} K against {th['ceiling_K']:.0f} K ceiling")
    print("\nbands:")
    for b in r['bands']:
        v = 'REPORT' if b['pass_'] is None else ('PASS' if b['pass_'] else 'FAIL')
        print(f"  band {b['band']}: {v}  {b['name']}\n            {b['detail']}")
    os.makedirs(RESULTS, exist_ok=True)
    json.dump(r, open(os.path.join(RESULTS, 'tube_shielding.json'), 'w'), indent=2)
    print("\n-> results/tube_shielding.json")
    return 0


if __name__ == '__main__':
    sys.exit(main())
