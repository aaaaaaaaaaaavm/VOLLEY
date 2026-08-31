"""A73: the Gen6 trim secondary, derived for the annulus it is actually drawn as.

P117. `analysis/trim_stage.py` sets the section's force as `KT * SHEET_A_PER_M / 1e3`, and A2
defines that thrust constant over `motor_model.SLED_ACTIVE_LEN` -- 0.34 m of flat, DOUBLE-sided
Halbach 0.09 m deep. A55 applied it to 0.14401 m of SINGLE-sided annulus around a 15.805 mm bore
without rescaling for length, for area, for the missing second array or for curvature.

Bands declared in validation/A73_trim_secondary.md before this file existed.

HOW THE CONVENTION RISK IS REMOVED
----------------------------------
The force is not recomputed from `F = B K A`. That expression hides a factor of two -- a
time-averaged force from peak-amplitude phasors is half of it -- and A66's first run lost exactly
that factor somewhere else. Instead the SAME Lorentz integral `motor_model.thrust_constant()`
performs is generalised to take the field and the cross-section as arguments, and band 1(a)
requires it to reproduce that function's own 10.5386 N per kA/m to 1e-6 when handed Gen5's flat
field and Gen5's geometry. Every convention -- the phase search, the 45 kA/m normalisation, the
Gauss weights, the wavelengths-per-array scaling -- is then inherited rather than re-decided.

Units are SI unless a magpylib call needs millimetres, which is noted where it happens.
"""
import json
import math
import os
import sys

import numpy as np
import magpylib as magpy

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RESULTS = os.path.join(HERE, 'results')
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import motor_model as mm                              # noqa: E402  the integral's source of truth

P = json.load(open(os.path.join(ROOT, 'cad', 'parameters.json')))
G = P['groups']

LAM = mm.LAM                                          # 0.048 m
NBLK = mm.NBLK                                        # 4 blocks per wavelength
BR = mm.BR                                            # 1.32 T
WIND_THICK_GEN5 = mm.WIND_THICK                       # 0.010 m
DEPTH_GEN5 = mm.DEPTH                                 # 0.090 m
ACTIVE_GEN5 = mm.SLED_ACTIVE_LEN                      # 0.340 m
K_NORM = 45e3                                         # motor_model's own normalising sheet current

BORE_M = G['gen6_drive']['bore_mm'] / 1e3
WALL_M = G['gen6_drive']['tube_wall_mm'] / 1e3
SECTION_M = G['gen6_trim']['section_length_mm'] / 1e3
FORCE_N = G['gen6_trim']['force_N']
K_SHEET = G['gen6_trim']['sheet_current_A_per_m']
BELT_T_GEN6 = 6.0e-3                                  # cad/build_gen6.py trim_stator(), belt_t
WIND_R_IN = BORE_M / 2.0 + WALL_M                     # same file: the winding starts at the wall
PISTON_R_M = BORE_M / 2.0 - 0.1e-3                    # cad/build_gen6.py carriage(), circle()
PISTON_L_M = 12.0e-3                                  # same, .extrude(12.0)
RHO_MAGNET = 7500.0                                   # kg/m3, NdFeB handbook. E4: not measured
PER_SAT_BASE_KG = 1.296                               # A49, the figure trim_authority.py adds to
SECTION_MASS_KG = G['gen6_trim']['added_mass_kg']
N_MANIFEST = 12

BELT_SEQ = [(0, +1), (2, -1), (1, +1), (0, -1), (2, +1), (1, -1)]


# --- the integral, generalised once and verified against its source ------------------------

def lorentz_kt(sample, lo, hi, depth_of, active_len, wind_thick, nx=240, ny=9,
               n_phase=144, phase_stride=10, mean_stride=5):
    """motor_model.thrust_constant()'s integral with the field and the section as arguments.

    `sample(xs, ys)` returns the field component that couples to the winding current, shape
    (ny, nx), already averaged over the third direction. `depth_of(y)` is the extent of the
    winding in that third direction at coordinate y -- a constant DEPTH for the flat machine and
    the circumference 2*pi*r for the annulus, which is the whole of what curvature changes in
    the integral itself.
    """
    xs = np.linspace(0.0, LAM, nx, endpoint=False)
    y_nodes, y_weights = np.polynomial.legendre.leggauss(ny)
    ys = lo + (hi - lo) * (y_nodes + 1.0) / 2.0
    half_span = (hi - lo) / 2.0
    field = sample(xs, ys)                                     # (ny, nx)
    depth = np.array([depth_of(y) for y in ys])                # (ny,)

    belt = LAM / 6.0
    ph = np.array([BELT_SEQ[int((x % LAM) // belt)][0] for x in xs])
    sg = np.array([BELT_SEQ[int((x % LAM) // belt)][1] for x in xs])
    dx = LAM / nx

    def thrust(shift, phi, k):
        fx = np.roll(field, +shift, axis=1)
        te = 2.0 * math.pi * (shift * dx) / LAM - phi
        i = np.array([math.cos(te), math.cos(te - 2.0 * math.pi / 3.0),
                      math.cos(te + 2.0 * math.pi / 3.0)])
        j = k * i[ph] * sg / wind_thick
        return float(((y_weights * depth)[:, None] * j[None, :] * fx).sum()
                     * dx * half_span)

    phis = np.linspace(0.0, 2.0 * math.pi, n_phase, endpoint=False)
    means = [np.mean([thrust(s, p, K_NORM) for s in range(0, nx, phase_stride)]) for p in phis]
    phi_best = phis[int(np.argmax(means))]
    fs = np.array([thrust(s, phi_best, K_NORM) for s in range(0, nx, mean_stride)])
    f_mean = fs.mean()
    ripple = (fs.max() - fs.min()) / 2.0 / f_mean * 100.0
    return f_mean * (active_len / LAM) / K_NORM, ripple


# --- the two fields ------------------------------------------------------------------------

def flat_sampler(nz=9, double_sided=True, depth=DEPTH_GEN5, gap=mm.GAP, th=mm.TH,
                 n_wave=7, br=BR):
    """Gen5's own field through motor_model.build_field(), or one array of it."""
    if double_sided:
        field = mm.build_field(n_wave=n_wave)
    else:
        w = LAM / NBLK
        mags = []
        for i in range(n_wave * NBLK):
            x = (i - n_wave * NBLK / 2 + 0.5) * w
            ang = (90 - i * 90) % 360
            pol = [br * np.cos(np.radians(ang)), br * np.sin(np.radians(ang)), 0]
            mags.append(magpy.magnet.Cuboid(polarization=pol, dimension=(w, th, depth),
                                            position=(x, -gap / 2 - th / 2, 0)))
        field = magpy.Collection(mags)

    def sample(xs, ys):
        z_nodes, z_weights = np.polynomial.legendre.leggauss(nz)
        zs = z_nodes * depth / 2.0
        X, Y, Z = np.meshgrid(xs, ys, zs, indexing='xy')
        by3 = field.getB(np.stack([X.ravel(), Y.ravel(), Z.ravel()], 1))[:, 1].reshape(X.shape)
        return (by3 * (z_weights / 2.0)[None, None, :]).sum(axis=2)

    return sample


def annular_array(r_i, r_o, n_lam=5, n_sect=36, br=BR):
    """A Halbach travelling axially along a cylinder, built from angular sectors.

    magpylib polarisation is a Cartesian vector, so a radially magnetised ring cannot be one
    source. It is `n_sect` sectors, each magnetised along its own radius. Band 1(b) tests that
    the discretisation has converged; band 1(c) tests the whole construction against a flat
    array in the large-radius limit, which is the only check that can catch a wrong geometry
    rather than a coarse one.
    """
    src = []
    dz = LAM / NBLK
    dphi = 360.0 / n_sect
    for m in range(n_lam * NBLK):
        z0 = m * dz
        phase = m % NBLK
        for s in range(n_sect):
            phi = math.radians((s + 0.5) * dphi)
            if phase == 0:
                pol = (math.cos(phi), math.sin(phi), 0.0)
            elif phase == 1:
                pol = (0.0, 0.0, 1.0)
            elif phase == 2:
                pol = (-math.cos(phi), -math.sin(phi), 0.0)
            else:
                pol = (0.0, 0.0, -1.0)
            src.append(magpy.magnet.CylinderSegment(
                polarization=tuple(br * p for p in pol),
                dimension=(r_i * 1e3, r_o * 1e3, dz * 1e3, s * dphi, (s + 1) * dphi),
                position=(0.0, 0.0, (z0 + dz / 2.0) * 1e3)))
    return magpy.Collection(*src), n_lam * LAM


def annular_sampler(r_i, r_o, n_lam=5, n_sect=36, n_theta=3, br=BR):
    """Radial field on an (r, axial) grid, averaged over one angular sector.

    Sampled about the array's mid-length, so the ends are outside the window -- the same
    omission motor_model.build_field() makes with `end_turns_modelled: false`, and it makes
    every force here an upper bound.
    """
    coll, total_len = annular_array(r_i, r_o, n_lam, n_sect, br)
    z_mid = total_len / 2.0
    dphi = 2.0 * math.pi / n_sect

    def sample(xs, ys):
        thetas = (np.arange(n_theta) + 0.5) / n_theta * dphi
        out = np.zeros((len(ys), len(xs)))
        for th in thetas:
            for iy, r in enumerate(ys):
                px = np.full_like(xs, r * math.cos(th)) * 1e3
                py = np.full_like(xs, r * math.sin(th)) * 1e3
                pz = (z_mid + xs - LAM / 2.0) * 1e3
                b = coll.getB(np.stack([px, py, pz], 1))
                out[iy] += b[:, 0] * math.cos(th) + b[:, 1] * math.sin(th)
        return out / n_theta

    return sample, coll


def peak_radial(r_i, r_o, r_probe, n_sect=36, n_lam=5, npts=160):
    """Peak radial field at a probe radius, for the convergence and limit checks."""
    sample, _ = annular_sampler(r_i, r_o, n_lam=n_lam, n_sect=n_sect, n_theta=1)
    xs = np.linspace(0.0, LAM, npts, endpoint=False)
    return float(np.abs(sample(xs, np.array([r_probe]))).max())


def peak_flat(depth_h, standoff, n_wave=5, npts=160):
    """Peak field above a single flat Halbach array, same depth and standoff."""
    sample = flat_sampler(nz=1, double_sided=False, depth=1.0, gap=0.0, th=depth_h,
                          n_wave=n_wave)
    xs = np.linspace(0.0, LAM, npts, endpoint=False)
    return float(np.abs(sample(xs, np.array([standoff]))).max())


# --- the run -------------------------------------------------------------------------------

DEPTHS_MM = [1.5, 3.0, 4.5, 6.0, 7.5]
N_SECT = 36
N_LAM = 5
NX, NY, N_THETA = 120, 5, 2


def annular_kt(depth_m, r_o=PISTON_R_M, active_len=SECTION_M, n_sect=N_SECT):
    sample, _ = annular_sampler(r_o - depth_m, r_o, n_lam=N_LAM, n_sect=n_sect,
                                n_theta=N_THETA)
    return lorentz_kt(sample, WIND_R_IN, WIND_R_IN + BELT_T_GEN6,
                      lambda r: 2.0 * math.pi * r, active_len, BELT_T_GEN6, nx=NX, ny=NY)


def array_mass_kg(depth_m, length_m, r_o=PISTON_R_M, rho=RHO_MAGNET):
    return math.pi * (r_o ** 2 - (r_o - depth_m) ** 2) * length_m * rho


def per_satellite_kg(array_kg, section_kg=SECTION_MASS_KG):
    """The stator section is on the machine and is shared; the array is on the carriage.

    ADR-035: the carriage is not recovered and each of the twelve satellites has its own. So the
    array is added ONCE PER SATELLITE, undivided, which is not what trim_authority.py does with
    the section it shares across the manifest.
    """
    return PER_SAT_BASE_KG + section_kg / N_MANIFEST + array_kg


def band1_verification():
    kt_flat, ripple_flat = lorentz_kt(flat_sampler(), -WIND_THICK_GEN5 / 2.0,
                                      WIND_THICK_GEN5 / 2.0, lambda y: DEPTH_GEN5,
                                      ACTIVE_GEN5, WIND_THICK_GEN5)
    kt_mm, ripple_mm = mm.thrust_constant()
    identity = abs(kt_flat - kt_mm) / kt_mm

    h_probe, r_o = 5.0e-3, PISTON_R_M
    r_probe = BORE_M / 2.0 + WALL_M / 2.0
    conv = {n: peak_radial(r_o - h_probe, r_o, r_probe, n_sect=n) for n in (18, 36, 72)}
    converged = abs(conv[72] - conv[36]) / conv[72]

    big_r, standoff = 20.0 * LAM, 1.0e-3
    curved = peak_radial(big_r - h_probe, big_r, big_r + standoff, n_sect=36)
    flat = peak_flat(h_probe, standoff)
    limit = abs(curved - flat) / flat

    out = {'kt_flat_N_per_kA_m': kt_flat * 1e3, 'kt_motor_model_N_per_kA_m': kt_mm * 1e3,
           'identity_rel': identity, 'ripple_flat_pct': ripple_flat,
           'sector_peaks_T': {str(k): v for k, v in conv.items()},
           'sector_convergence_rel': converged,
           'large_radius_annular_T': curved, 'flat_single_sided_T': flat,
           'large_radius_rel': limit}
    out['pass_'] = identity <= 1e-6 and converged <= 0.01 and limit <= 0.05
    return out


def build():
    b1 = band1_verification()

    rows = []
    for d_mm in DEPTHS_MM:
        d = d_mm / 1e3
        kt, ripple = annular_kt(d)
        force = kt * K_SHEET
        m_arr = array_mass_kg(d, SECTION_M)
        rows.append({'depth_mm': d_mm, 'kt_N_per_kA_m': kt * 1e3, 'ripple_pct': ripple,
                     'force_at_90kA_m_N': force, 'force_ratio_to_spec': force / FORCE_N,
                     'peak_Br_at_wall_T': peak_radial(PISTON_R_M - d, PISTON_R_M,
                                                      BORE_M / 2.0 + WALL_M / 2.0),
                     'array_mass_at_section_kg': m_arr,
                     'per_satellite_at_section_kg': per_satellite_kg(m_arr)})

    best = max(rows, key=lambda r: r['force_at_90kA_m_N'])
    shortfall = FORCE_N / best['force_at_90kA_m_N']
    len_needed = SECTION_M * shortfall
    mass_needed = array_mass_kg(best['depth_mm'] / 1e3, len_needed)
    per_sat_needed = per_satellite_kg(mass_needed, SECTION_MASS_KG * shortfall)

    fits_radius = PISTON_R_M >= PISTON_R_M                       # by construction, stated anyway
    fits_length = len_needed <= PISTON_L_M

    flat_closed = peak_flat(best['depth_mm'] / 1e3, WALL_M / 2.0)
    curvature_ratio = best['peak_Br_at_wall_T'] / flat_closed

    bands = [
        {'band': '1', 'name': 'verification: the integral against motor_model, the sectors '
                              'against themselves, the curvature against the flat limit',
         'detail': f"identity {b1['identity_rel']:.1e} against 1e-6; sectors "
                   f"{b1['sector_convergence_rel']*100:.4f} % against 1 %; large-radius limit "
                   f"{b1['large_radius_rel']*100:.3f} % against 5 %",
         'pass_': b1['pass_']},
        {'band': '2', 'name': 'REPORT: thrust constant and force against magnet depth',
         'detail': '; '.join(f"{r['depth_mm']:.1f} mm {r['kt_N_per_kA_m']:.4f} N per kA/m, "
                             f"{r['force_at_90kA_m_N']:.2f} N" for r in rows),
         'pass_': None},
        {'band': '3', 'name': 'the section as drawn reaches its specified 948.0 N',
         'detail': f"best {best['force_at_90kA_m_N']:.2f} N at {best['depth_mm']:.1f} mm depth, "
                   f"{best['force_ratio_to_spec']*100:.2f} % of specified, short by "
                   f"{shortfall:.1f}x",
         'pass_': best['force_at_90kA_m_N'] >= FORCE_N},
        {'band': '4', 'name': 'the array that reaches 948.0 N fits the carriage as drawn, '
                              '7.8025 mm radius and 12.0 mm long',
         'detail': f"needs {len_needed*1e3:.1f} mm of array against a 12.0 mm piston, "
                   f"{len_needed/PISTON_L_M:.1f}x",
         'pass_': bool(fits_radius and fits_length)},
        {'band': '5', 'name': 'per-satellite added mass <= 2.0 kg with the array counted once '
                              'per carriage',
         'detail': f"as drawn {best['per_satellite_at_section_kg']:.4f} kg; at the length 948.0 N "
                   f"needs {per_sat_needed:.2f} kg",
         'pass_': per_sat_needed <= 2.0},
        {'band': '6', 'name': 'REPORT: the annular field against a flat array of the same depth '
                              'and standoff',
         'detail': f"annulus {best['peak_Br_at_wall_T']:.6f} T, flat {flat_closed:.6f} T, "
                   f"ratio {curvature_ratio:.4f}",
         'pass_': None},
    ]

    return {
        'analysis': 'A73',
        'bands_declared_commit': '79eff67, before this file existed',
        'note': ('The Gen6 trim secondary derived for the single-sided annulus cad/build_gen6.py '
                 'draws, by motor_model own Lorentz integral. Closes P117. E4: nothing measured.'),
        'inputs': {'bore_m': BORE_M, 'wall_m': WALL_M, 'piston_radius_m': PISTON_R_M,
                   'piston_length_m': PISTON_L_M, 'winding_inner_radius_m': WIND_R_IN,
                   'winding_thickness_m': BELT_T_GEN6, 'section_m': SECTION_M,
                   'specified_force_N': FORCE_N, 'sheet_current_A_m': K_SHEET,
                   'gen5_kt_N_per_kA_m': ACTIVE_GEN5 and b1['kt_motor_model_N_per_kA_m'],
                   'magnet_density_kg_m3': RHO_MAGNET, 'remanence_T': BR,
                   'nx': NX, 'ny': NY, 'n_theta': N_THETA, 'n_sectors': N_SECT,
                   'n_wavelengths': N_LAM},
        'verification': b1,
        'depth_sweep': rows,
        'best': best,
        'to_reach_specified_force': {'shortfall_factor': shortfall,
                                     'array_length_m': len_needed,
                                     'array_mass_kg': mass_needed,
                                     'per_satellite_kg': per_sat_needed,
                                     'piston_length_m': PISTON_L_M,
                                     'lengths_of_piston': len_needed / PISTON_L_M},
        'curvature_report': {'annular_T': best['peak_Br_at_wall_T'], 'flat_T': flat_closed,
                             'ratio': curvature_ratio},
        'bands': bands,
    }


def main():
    r = build()
    b1 = r['verification']
    print(f"A73 trim secondary, annular, bore {BORE_M*1e3:.3f} mm, winding from "
          f"{WIND_R_IN*1e3:.4f} mm over {BELT_T_GEN6*1e3:.1f} mm")
    print(f"  verification: integral identity {b1['identity_rel']:.1e}, sector convergence "
          f"{b1['sector_convergence_rel']*100:.4f} %, large-radius limit "
          f"{b1['large_radius_rel']*100:.3f} %")
    print("\n  depth    Kt          force at 90 kA/m     of 948.0 N    peak Br at wall   per sat")
    for row in r['depth_sweep']:
        print(f"  {row['depth_mm']:4.1f} mm  {row['kt_N_per_kA_m']:7.4f}   "
              f"{row['force_at_90kA_m_N']:9.2f} N      {row['force_ratio_to_spec']*100:6.2f} %"
              f"      {row['peak_Br_at_wall_T']:.4f} T     "
              f"{row['per_satellite_at_section_kg']:.4f} kg")
    n = r['to_reach_specified_force']
    print(f"\n  to reach 948.0 N: {n['shortfall_factor']:.1f}x more array, "
          f"{n['array_length_m']*1e3:.0f} mm of it against a 12.0 mm piston "
          f"({n['lengths_of_piston']:.0f}x), {n['array_mass_kg']:.2f} kg per carriage, "
          f"{n['per_satellite_kg']:.2f} kg per satellite")
    print("\nbands:")
    for b in r['bands']:
        v = 'REPORT' if b['pass_'] is None else ('PASS' if b['pass_'] else 'FAIL')
        print(f"  band {b['band']}: {v}  {b['name']}\n            {b['detail']}")
    os.makedirs(RESULTS, exist_ok=True)
    json.dump(r, open(os.path.join(RESULTS, 'trim_secondary.json'), 'w'), indent=2)
    print("\n-> results/trim_secondary.json")
    return 0


if __name__ == '__main__':
    sys.exit(main())
