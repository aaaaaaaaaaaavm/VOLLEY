"""A71 runner: convergence of the guided-contact solution.

Bands declared in validation/A71_guided_contact_converged.md before
analysis/guided_contact_ivp.py existed.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import guided_contact as g                                          # noqa: E402
import guided_contact_ivp as m                                      # noqa: E402

DT = 1.0
ADMISSIBLE_LANDS = (40.0, 80.0, 120.0, 200.0)      # A70: 400 mm is inadmissible at 1 K


def main():
    out = dict(analysis="A71", bands_declared_commit="a71-bands", dT_K=DT,
               note=("Stiff adaptive implicit integration (Radau) of the 6-DOF guided-contact "
                     "problem on A69's corrected continuous centreline. The peak penalty force "
                     "is deliberately NOT reported as physical. Nothing measured -- E4."))

    r1 = m.run(straight=True, ecc_mm=0.0, cg_off_mm=0.0,
               friction_N=g.SEAL["friction_allowance_N"])
    want = g.D["exit_velocity_m_s_at_friction_allowance"]
    b1 = abs(r1["v_exit"] - want) / want <= 0.01
    out["rigid_limit"] = dict(v_exit=r1["v_exit"], want=want,
                              err_pct=100 * (r1["v_exit"] - want) / want)
    print(f"band 1 rigid limit: {r1['v_exit']:.4f} against {want} m/s "
          f"({100*(r1['v_exit']-want)/want:+.3f} %)")

    tol = []
    for rtol in (1e-7, 1e-8, 1e-9):
        r = m.run(dT_K=DT, rtol=rtol)
        tol.append(dict(rtol=rtol, **{k: r[k] for k in
                                      ("rate_deg_s", "v_exit", "impulse_Ns", "steps",
                                       "peak_penetration_frac_clearance", "energy_gap_pct")}))
        print(f"  rtol {rtol:.0e}: rate {r['rate_deg_s']:8.4f}  pen "
              f"{100*r['peak_penetration_frac_clearance']:6.2f}%  steps {r['steps']}")
    out["tolerance_sweep"] = tol
    d2 = abs(tol[-1]["rate_deg_s"] - tol[-2]["rate_deg_s"]) / tol[-2]["rate_deg_s"]
    b2 = d2 < 0.02

    stiff = []
    for ks in (1.0, 10.0, 100.0):
        r = m.run(dT_K=DT, rtol=1e-8, K_scale=ks)
        stiff.append(dict(K_scale=ks, **{k: r[k] for k in
                                         ("rate_deg_s", "v_exit", "impulse_Ns", "steps",
                                          "peak_penetration_frac_clearance")}))
        print(f"  K x{ks:5.0f}: rate {r['rate_deg_s']:8.4f}  pen "
              f"{100*r['peak_penetration_frac_clearance']:6.2f}%  steps {r['steps']}")
    out["stiffness_sweep"] = stiff
    rates = [s["rate_deg_s"] for s in stiff]
    spread3 = (max(rates) - min(rates)) / min(rates)
    pen_stiffest = min(s["peak_penetration_frac_clearance"] for s in stiff)
    b3 = spread3 < 0.05 and pen_stiffest <= 0.10

    conv = tol[-1]
    b4 = abs(conv["energy_gap_pct"]) <= 1.0

    laws = {}
    for law in ("LN", "MOD"):
        r = m.run(dT_K=DT, rtol=1e-8, law=law)
        laws[law] = dict(rate_deg_s=r["rate_deg_s"], v_exit=r["v_exit"],
                         impulse_Ns=r["impulse_Ns"])
        print(f"  law {law}: rate {r['rate_deg_s']:8.4f}")
    out["laws"] = laws
    lr = [v["rate_deg_s"] for v in laws.values()]
    b5 = (max(lr) - min(lr)) / min(lr) <= 0.25

    out["impulse_Ns"] = conv["impulse_Ns"]
    b6 = ("impulse reported; peak penalty force deliberately not quoted as physical", True)

    b7 = conv["rate_deg_s"] <= 2.0 if b2 and b3 else None

    lands = []
    for L in ADMISSIBLE_LANDS:
        r = m.run(dT_K=DT, rtol=1e-8, land_sep_mm=L)
        lands.append(dict(land_sep_mm=L, rate_deg_s=r["rate_deg_s"],
                          peak_penetration_frac_clearance=r["peak_penetration_frac_clearance"]))
        print(f"  L {L:5.0f} mm: rate {r['rate_deg_s']:8.4f}")
    out["land_sweep"] = lands
    b8 = max(d["land_sep_mm"] for d in lands) <= 200.0

    bands = [
        ("1", "rigid-limit regression to 1 %",
         f"{r1['v_exit']:.4f} against {want} m/s", b1),
        ("2", "tolerance convergence < 2 % between 1e-8 and 1e-9",
         f"{100*d2:.2f} % ({tol[-2]['rate_deg_s']:.3f} -> {tol[-1]['rate_deg_s']:.3f} deg/s)", b2),
        ("3", "stiffness insensitivity < 5 % over two decades, penetration <= 10 %",
         f"{100*spread3:.1f} % spread, penetration {100*pen_stiffest:.2f} % at the stiffest", b3),
        ("4", "energy closes to 1 %", f"{conv['energy_gap_pct']:+.3f} %", b4),
        ("5", "two formulations agree within 25 %",
         f"{min(lr):.3f} to {max(lr):.3f} deg/s", b5),
        ("6", "contact impulse reported, peak penalty force not quoted as physical",
         f"{conv['impulse_Ns']:.4f} N.s", b6[1]),
        ("7", "converged exit angular rate <= 2.0 deg/s",
         (f"{conv['rate_deg_s']:.3f} deg/s" if b7 is not None
          else "NOT EVALUABLE -- bands 2 and 3 must pass before a physical rate is quoted"), b7),
        ("8", "land sweep inside the admissible region",
         f"max {max(d['land_sep_mm'] for d in lands):.0f} mm against A70's 200 mm at 1 K", b8),
    ]
    out["bands"] = [dict(band=n, name=nm, detail=d,
                         pass_=(None if ok is None else bool(ok))) for n, nm, d, ok in bands]
    print("\nbands:")
    for n, nm, d, ok in bands:
        v = "NOT EVALUABLE" if ok is None else ("PASS" if ok else "FAIL")
        print(f"  band {n}: {v}  {nm}\n            {d}")

    path = os.path.join(m.RESULTS, "guided_contact_ivp.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, default=float)
        fh.write("\n")
    print(f"\nwrote {path}")


if __name__ == "__main__":
    main()
