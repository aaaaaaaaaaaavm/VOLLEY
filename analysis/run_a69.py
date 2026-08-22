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
    (x, w, th), off = t.case_support_tolerance(800)
    cases["support_placement"] = dict(peak_mm=float(np.abs(w).max() * 1e3),
                                      peak_slope=float(np.abs(th).max()),
                                      rms_mm=float(np.sqrt((w ** 2).mean()) * 1e3),
                                      offsets_mm=[float(o * 1e3) for o in off])
    therm = []
    for dT in t.THERMAL_DT_K:
        k, sag = t.thermal_bow(dT)
        therm.append(dict(dT_K=dT, curvature_per_m=k, sagitta_per_span_mm=sag * 1e3))
    cases["thermal_bow"] = dict(peak_mm=therm[-1]["sagitta_per_span_mm"], sweep=therm)
    sigma_h, growth = t.pressure_bore_growth()
    out["pressure"] = dict(hoop_MPa=sigma_h / 1e6, bore_growth_um=growth * 1e6,
                           pct_of_nominal_clearance=100 * growth * 1e6 / 50.0)
    out["cases"] = cases

    b4 = True                                       # the centreline is exported as x, w, slope
    out["exported_centreline"] = dict(n_points=len(x), x_m=[float(v) for v in x[::40]],
                                      w_mm=[float(v * 1e3) for v in w[::40]])

    b5 = cases["orbit_0g"]["peak_mm"] <= 0.1
    print(f"band 5 orbit 0 g sag: {cases['orbit_0g']['peak_mm']:.6f} mm")

    b6 = True
    print(f"band 6 pressure: hoop {sigma_h/1e6:.2f} MPa, bore growth {growth*1e6:.3f} um "
          f"({out['pressure']['pct_of_nominal_clearance']:.1f} % of the 50 um clearance)")

    # Worst-case orbital combination: what actually fires. Self-weight is zero at 0 g, so the
    # centreline in flight is support placement plus thermal bow.
    worst = cases["support_placement"]["peak_mm"] + cases["thermal_bow"]["peak_mm"]
    best = cases["support_placement"]["peak_mm"] + therm[0]["sagitta_per_span_mm"]
    out["orbital_centreline_mm"] = dict(low=best, high=worst,
                                        a67_bracket_mm=[0.1, 2.0])
    b7 = 0.1 <= best and worst <= 2.0
    print(f"band 7 orbital centreline: {best:.4f} to {worst:.4f} mm against A67's 0.1-2.0")

    ranked = sorted(((k, v["peak_mm"]) for k, v in cases.items()), key=lambda z: -z[1])
    out["ranked"] = [dict(case=k, peak_mm=v) for k, v in ranked]
    b8 = True
    print("band 8 ranked:", ", ".join(f"{k} {v:.4f} mm" for k, v in ranked))

    bands = [
        ("1", "simple span reproduces 5wL^4/384EI to 0.5 %", f"{100*err:.4f} %", b1),
        ("2", "mesh converged, 0.5 % between N and 2N",
         f"{conv[-2]['peak_mm']:.5f} -> {conv[-1]['peak_mm']:.5f} mm", b2),
        ("3", "free-free first mode reproduces A59's 1.67 Hz to 5 %", f"{f1:.4f} Hz", b3),
        ("4", "a continuous centreline is returned and exported",
         f"{len(x)} nodes, position and slope", b4),
        ("5", "0 g support sag <= 0.1 mm", f"{cases['orbit_0g']['peak_mm']:.6f} mm", b5),
        ("6", "pressure-induced bore growth reported against the clearance",
         f"{growth*1e6:.3f} um, {out['pressure']['pct_of_nominal_clearance']:.1f} %", b6),
        ("7", "combined worst case inside A67's swept 0.1-2.0 mm",
         f"{best:.4f} to {worst:.4f} mm", b7),
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
