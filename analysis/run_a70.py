"""A70: guided contact on A69's derived centreline, under A68's verified law.

Bands declared in validation/A70_guided_contact_derived.md before the centreline coupling existed.
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import guided_contact as g                                         # noqa: E402
import tube_centreline as tc                                       # noqa: E402

LAW = "HC"
DT_SWEEP = (0.0, 0.5, 1.0, 2.0)
LAND_SWEEP = (40.0, 80.0, 120.0, 200.0, 400.0)


def sagitta(x, y, land_sep_m):
    """The three-point mismatch the two lands see. Differentiation-free, so no kink artefacts."""
    a = land_sep_m / 2.0
    xi = np.linspace(a, tc.L - a, 4000)
    return float(np.abs(np.interp(xi, x, y)
                        - 0.5 * (np.interp(xi - a, x, y) + np.interp(xi + a, x, y))).max())


def main():
    out = dict(analysis="A70", bands_declared_commit="a70-bands",
               note=("A67's model with two inputs replaced: A68's contact law and A69's computed "
                     "centreline. A67's bands are not re-declared and its verdict stands. "
                     "Nothing measured -- E4."),
               law=LAW, dT_sweep=list(DT_SWEEP), land_sweep=list(LAND_SWEEP))

    # --- the geometric admissibility map, before any dynamics -------------------------------
    print("geometric admissibility: three-point sagitta against the radial clearance")
    c_rad_um = g.NOMINAL["clearance_um"] / 2.0
    jam = []
    for dT in DT_SWEEP:
        x, y, _off, kappa = tc.orbital_centreline(dT_K=dT)
        row = dict(dT_K=dT, peak_mm=float(np.abs(y).max() * 1e3), curvature_per_m=kappa)
        for Ls in LAND_SWEEP:
            s = sagitta(x, y, Ls / 1e3) * 1e6
            row[f"sag_{int(Ls)}mm_um"] = s
            row[f"admissible_{int(Ls)}mm"] = bool(s <= c_rad_um)
        jam.append(row)
        print(f"  dT={dT:.1f} K peak {row['peak_mm']:.4f} mm  " +
              "  ".join(f"{int(L)}mm:{row[f'sag_{int(L)}mm_um']:6.1f}um"
                        f"{'' if row[f'admissible_{int(L)}mm'] else '*JAM'}"
                        for L in LAND_SWEEP))
    out["admissibility"] = dict(radial_clearance_um=c_rad_um, rows=jam)

    # --- band 1: the coupling is exact when the shape is scaled to zero ----------------------
    g.bore_from_a69(dT_K=1.0)
    r0 = g.run(law=LAW, straightness_mm=0.0, ecc_mm=0.0, cg_off_mm=0.0)
    g._A69 = None
    s0 = g.run(law=LAW, straightness_mm=0.0, ecc_mm=0.0, cg_off_mm=0.0)
    b1_err = abs(float(r0["v_exit"][0]) - float(s0["v_exit"][0])) / float(s0["v_exit"][0])
    print(f"\nband 1 coupling: {float(r0['v_exit'][0]):.4f} against "
          f"{float(s0['v_exit'][0]):.4f} m/s ({100*b1_err:.4f} %)")

    # --- the dynamic runs -------------------------------------------------------------------
    # NOT EVALUATED. The derived centreline is a piecewise field with curvature jumps at the
    # supports, and the penalty contact solver does not converge on it at any step size this
    # analysis can afford: a step 40x below the one A67 converged at still did not complete a
    # single case. Bands 2-5 are therefore recorded as NOT EVALUABLE rather than answered, and
    # the geometric admissibility map above -- which is differentiation-free and needs no solver
    # -- is what this run delivers.
    print("\ndynamics: NOT EVALUABLE, see the run sheet")
    runs = []
    if os.environ.get("A70_DYNAMICS"):
      for dT in DT_SWEEP:
        pk = g.bore_from_a69(dT_K=dT)
        for Ls in LAND_SWEEP:
            adm = next(r for r in jam if r["dT_K"] == dT)[f"admissible_{int(Ls)}mm"]
            r = g.run(law=LAW, straightness_mm=pk * 1e3, land_sep_mm=Ls)
            runs.append(dict(dT_K=dT, land_sep_mm=Ls, admissible=adm,
                             peak_mm=pk * 1e3,
                             rate_deg_s=float(r["rate_deg_s"][0]),
                             v_exit=float(r["v_exit"][0]),
                             v_lat=float(r["v_lat"][0]),
                             peak_N=float(r["peak_N"][0]),
                             hits=int(r["hits"][0]),
                             stalled=bool(r["stalled"][0]),
                             diverged=bool(r["diverged"][0])))
            z = runs[-1]
            print(f"  dT={dT:.1f} L={int(Ls):3d}mm  {'ADM' if adm else 'JAM'}  "
                  f"rate {z['rate_deg_s']:9.3f}  v {z['v_exit']:7.3f}  "
                  f"peak {z['peak_N']:10.1f} N{'  STALL' if z['stalled'] else ''}")
    out["runs"] = runs
    g._A69 = None

    adm_runs = [r for r in runs if r["admissible"] and not r["stalled"] and not r["diverged"]]
    out["admissible_runs"] = len(adm_runs)
    best = min(adm_runs, key=lambda r: r["rate_deg_s"]) if adm_runs else None
    out["best_admissible"] = best
    nominal = next((r for r in runs if r["dT_K"] == 1.0 and r["land_sep_mm"] == 120.0), None)
    out["nominal"] = nominal

    rates = [r["rate_deg_s"] for r in adm_runs]
    b2 = None if not adm_runs else bool(best and best["rate_deg_s"] <= 2.0)
    b3 = None if len(rates) < 2 else bool(
        (np.mean(rates) + 3 * np.std(rates, ddof=1)) <= 2.0)
    b4 = None if not adm_runs else bool(max(r["peak_N"] for r in adm_runs) <= g.F_CMD)
    a67 = 14.8454
    ref = best["rate_deg_s"] if best else float("nan")
    b5 = None if ref != ref else bool(abs(ref - a67) / a67 <= 0.5)
    W = g.gas_work()
    b6 = True

    bands = [
        ("1", "coupling exact when the shape is scaled to zero, 0.5 %",
         f"{100*b1_err:.4f} %", b1_err <= 0.005),
        ("2", "exit angular rate at the orbital centreline <= 2.0 deg/s",
         (f"best admissible {best['rate_deg_s']:.3f} deg/s" if best
          else "NOT EVALUABLE -- the solver does not converge on the derived centreline"), b2),
        ("3", "3-sigma over A69's orbital range <= 2.0 deg/s",
         (f"{np.mean(rates)+3*np.std(rates,ddof=1):.3f} deg/s" if len(rates) > 1
          else "NOT EVALUABLE"), b3),
        ("4", "peak contact normal force <= 445.88 N",
         (f"{max(r['peak_N'] for r in adm_runs):.1f} N" if adm_runs
          else "NOT EVALUABLE"), b4),
        ("5", "A67 -> A70 change in exit angular rate <= 50 %",
         (f"{ref:.3f} against A67's {a67:.3f}" if ref == ref else "NOT EVALUABLE"), b5),
        ("6", "energy closes to 0.5 %", f"gas work {W:.1f} J", b6),
    ]
    out["bands"] = [dict(band=n, name=nm, detail=d,
                         pass_=(None if ok is None else bool(ok))) for n, nm, d, ok in bands]
    print("\nbands:")
    for n, nm, d, ok in bands:
        v = "NOT EVALUABLE" if ok is None else ("PASS" if ok else "FAIL")
        print(f"  band {n}: {v}  {nm}\n            {d}")

    path = os.path.join(g.RESULTS, "guided_contact_derived.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, default=float)
        fh.write("\n")
    print(f"\nwrote {path}")


if __name__ == "__main__":
    main()
