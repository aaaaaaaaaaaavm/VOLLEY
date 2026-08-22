"""A69 runner: the tube's centreline, contribution by contribution.

Bands declared in validation/A69_tube_centreline.md before analysis/tube_centreline.py existed.
"""
import json
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tube_centreline as t                                        # noqa: E402


def main():
    out = dict(analysis="A69", bands_declared_commit="a69-bands",
               note=("Euler-Bernoulli Hermite beam on seven rigid supports at 1.0 m. "
                     "Contributions solved separately and ranked. Manufacturing straightness is "
                     "a DECLARED tolerance, not computed here. Nothing measured -- E4."),
               section=dict(I_m4=t.I_SEC, A_m2=t.A_SEC, mass_per_m=t.MASS_PER_M,
                            mass_kg=t.MASS_PER_M * t.L, E_Pa=t.E_MOD, OD_m=t.OD, bore_m=t.BORE),
               declared=dict(support_pitch_m=t.SUPPORT_PITCH, supports=list(t.SUPPORTS),
                             support_tol_mm=t.SUPPORT_TOL_MM,
                             ascent_lateral_g=t.ASCENT_LATERAL_G,
                             thermal_dT_K=list(t.THERMAL_DT_K)))

    gK, wK, eK = t.verify_imposed_curvature()
    out["imposed_curvature_check"] = dict(got_m=gK, closed_form_m=wK, err_pct=100 * eK)
    print(f"imposed-curvature limiting case: {gK:.6e} against k*L^2/8 = {wK:.6e} "
          f"({100*eK:.4f} %)")
    got, want, err = t.verify_simple_span()
    out["simple_span"] = dict(got_m=got, closed_form_m=want, err_pct=100 * err)
    b1 = err <= 0.005
    print(f"band 1 simple span: {got:.6e} against {want:.6e}  ({100*err:.4f} %)")

    conv = []
    for n in (200, 400, 800, 1600):
        x, w, th = t.case_self_weight(1.0, n)
        conv.append(dict(n_el=n, peak_mm=float(np.abs(w).max() * 1e3)))
    out["mesh_convergence"] = conv
    b2 = abs(conv[-1]["peak_mm"] - conv[-2]["peak_mm"]) / conv[-2]["peak_mm"] < 0.005
    print("band 2 mesh:", ", ".join(f"{c['n_el']}:{c['peak_mm']:.5f}" for c in conv))

    f1 = t.free_free_first_mode()
    a59 = 1.67
    out["free_free_f1_Hz"] = f1
    b3 = abs(f1 - a59) / a59 <= 0.05
    print(f"band 3 free-free f1: {f1:.4f} Hz against A59's {a59}")

    cases = {}
    for g_level, name in ((1.0, "bench_1g"), (0.0, "orbit_0g"),
                          (t.ASCENT_LATERAL_G, "ascent_lateral")):
        x, w, th = t.case_self_weight(g_level, 800)
        cases[name] = dict(peak_mm=float(np.abs(w).max() * 1e3),
                           peak_slope=float(np.abs(th).max()),
                           rms_mm=float(np.sqrt((w ** 2).mean()) * 1e3))
    x, w, th, off, _k0 = t.orbital_centreline(dT_K=0.0)
    cases["support_placement"] = dict(peak_mm=float(np.abs(w).max() * 1e3),
                                      peak_slope=float(np.abs(th).max()),
                                      rms_mm=float(np.sqrt((w ** 2).mean()) * 1e3),
                                      offsets_mm=[float(o * 1e3) for o in off])
    # P110: the thermal case is now solved as an imposed curvature on the continuous member,
    # together with the support offsets, in ONE compatible beam solve.
    therm = []
    for dT in (0.0, 0.5, 1.0, 2.0, 5.0):
        xc, yc, thc, _o, kap = t.orbital_centreline(dT_K=dT)
        therm.append(dict(dT_K=dT, curvature_per_m=kap,
                          peak_mm=float(np.abs(yc).max() * 1e3),
                          max_slope=float(np.abs(thc).max()),
                          max_slope_jump=float(np.abs(np.diff(thc)).max()),
                          sag_40mm_um=t.sagitta_over(xc, yc, 0.040) * 1e6,
                          sag_120mm_um=t.sagitta_over(xc, yc, 0.120) * 1e6,
                          sag_200mm_um=t.sagitta_over(xc, yc, 0.200) * 1e6,
                          sag_400mm_um=t.sagitta_over(xc, yc, 0.400) * 1e6))
    cases["thermal_bow"] = dict(peak_mm=therm[-1]["peak_mm"], sweep=therm)
    sigma_h, growth = t.pressure_bore_growth()
    out["pressure"] = dict(hoop_MPa=sigma_h / 1e6, bore_growth_um=growth * 1e6,
                           pct_of_nominal_clearance=100 * growth * 1e6 / 50.0)
    out["cases"] = cases

    # Band 4, ACTUALLY TESTED. P110: this was `b4 = True`, which is not a test.
    xc, yc, thc, _o, kap1 = t.orbital_centreline(dT_K=1.0)
    d_th = np.abs(np.diff(thc))
    curv = np.abs(np.diff(thc) / np.diff(xc))
    slope_ref = float(np.abs(thc).max())
    cont = dict(
        n_points=int(len(xc)),
        displacement_finite=bool(np.isfinite(yc).all()),
        slope_finite=bool(np.isfinite(thc).all()),
        max_slope=slope_ref,
        max_slope_jump=float(d_th.max()),
        slope_jump_rel=float(d_th.max() / slope_ref),
        max_curvature_per_m=float(curv.max()),
        imposed_curvature_per_m=float(kap1),
        curvature_ratio=float(curv.max() / kap1))
    out["continuity"] = cont
    # A continuous member's slope jump between adjacent nodes must be a discretisation artefact,
    # not a structural kink: require it below 1 % of the peak slope, and the peak curvature
    # within 5x the imposed curvature.
    b4 = (cont["displacement_finite"] and cont["slope_finite"]
          and cont["slope_jump_rel"] < 0.01 and cont["curvature_ratio"] < 5.0)
    out["exported_centreline"] = dict(n_points=len(xc), x_m=[float(v) for v in xc[::40]],
                                      w_mm=[float(v * 1e3) for v in yc[::40]],
                                      slope=[float(v) for v in thc[::40]])
    print(f"band 4 continuity: slope jump {cont['max_slope_jump']:.3e} "
          f"({100*cont['slope_jump_rel']:.4f} % of peak slope), "
          f"curvature {cont['max_curvature_per_m']:.3e} against imposed {kap1:.3e}")

    b5 = cases["orbit_0g"]["peak_mm"] <= 0.1
    print(f"band 5 orbit 0 g sag: {cases['orbit_0g']['peak_mm']:.6f} mm")

    b6 = True
    print(f"band 6 pressure: hoop {sigma_h/1e6:.2f} MPa, bore growth {growth*1e6:.3f} um "
          f"({out['pressure']['pct_of_nominal_clearance']:.1f} % of the 50 um clearance)")

    # Band 7, on ACTUAL combined centrelines. P110: this added scalar peaks, which is not a
    # centreline. Each row below is one compatible solve.
    best = min(r["peak_mm"] for r in therm)
    worst = max(r["peak_mm"] for r in therm)
    out["orbital_centreline_mm"] = dict(low=best, high=worst, a67_bracket_mm=[0.1, 2.0],
                                        note="peaks of solved combined centrelines, not sums")
    b7 = worst <= 2.0
    print(f"band 7 orbital centreline: {best:.4f} to {worst:.4f} mm against A67's 0.1-2.0")

    ranked = sorted(((k, v["peak_mm"]) for k, v in cases.items()), key=lambda z: -z[1])
    out["ranked"] = [dict(case=k, peak_mm=v) for k, v in ranked]
    b8 = True
    print("band 8 ranked:", ", ".join(f"{k} {v:.4f} mm" for k, v in ranked))

    bands = [
        ("1", "simple span reproduces 5wL^4/384EI AND imposed curvature reproduces k*L^2/8, "
              "both to 0.5 %", f"{100*err:.4f} % and {100*eK:.4f} %", b1 and eK <= 0.005),
        ("2", "mesh converged, 0.5 % between N and 2N",
         f"{conv[-2]['peak_mm']:.5f} -> {conv[-1]['peak_mm']:.5f} mm", b2),
        ("3", "free-free first mode reproduces A59's 1.67 Hz to 5 %", f"{f1:.4f} Hz", b3),
        ("4", "the centreline is continuous: finite, slope jump < 1 % of peak slope, "
              "curvature within 5x the imposed",
         f"jump {100*cont['slope_jump_rel']:.4f} %, curvature ratio {cont['curvature_ratio']:.2f}",
         b4),
        ("5", "0 g support sag <= 0.1 mm", f"{cases['orbit_0g']['peak_mm']:.6f} mm", b5),
        ("6", "pressure-induced bore growth reported against the clearance",
         f"{growth*1e6:.3f} um, {out['pressure']['pct_of_nominal_clearance']:.1f} %", b6),
        ("7", "solved combined centrelines peak inside A67's swept 2.0 mm",
         f"{best:.4f} to {worst:.4f} mm over dT 0-5 K", b7),
        ("8", "contributions reported separately and ranked",
         ranked[0][0] + " dominates", b8),
    ]
    out["bands"] = [dict(band=n, name=nm, detail=d, pass_=bool(ok)) for n, nm, d, ok in bands]
    print("\nbands:")
    for n, nm, d, ok in bands:
        print(f"  band {n}: {'PASS' if ok else 'FAIL'}  {nm}\n            {d}")

    path = os.path.join(t.RESULTS, "tube_centreline.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, default=float)
        fh.write("\n")
    print(f"\nwrote {path}")


if __name__ == "__main__":
    main()
