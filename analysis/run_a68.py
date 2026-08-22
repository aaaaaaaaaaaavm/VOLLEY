"""A68 runner: verify the contact laws, then measure how much of A67's headline is model form.

Bands declared in validation/A68_contact_law.md before analysis/contact_laws.py existed.
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import contact_laws as cl                                          # noqa: E402
import guided_contact as g                                         # noqa: E402

E_SWEEP = (0.2, 0.3, 0.5, 0.7, 0.9)
V_SWEEP = (0.05, 0.5, 2.0)
K_REF = float(g.contact_stiffness(np.array([g.NOMINAL["clearance_um"] / 2.0 / 1e6]))[0])
M = g.M_BODY


def main():
    out = dict(analysis="A68", bands_declared_commit="a68-bands",
               note=("Code verification of three compliant-contact formulations, then the same "
                     "VOLLEY case under each. Nothing measured -- E4."),
               K=K_REF, exponent=cl.N_EXP, mass_kg=M)

    print("bands 1-3: restitution recovery")
    rows, chi_id = [], {}
    for e in E_SWEEP:
        chi_id[e] = cl.chi_identified(e, K_REF, M, 0.5)
        for v in V_SWEEP:
            r = dict(e=e, v0=v,
                     LN=cl.impact(cl.chi_ln(e), K_REF, M, v),
                     HC=cl.impact(cl.chi_hc(e), K_REF, M, v),
                     ID=cl.impact(chi_id[e], K_REF, M, v))
            for k in ("LN", "HC", "ID"):
                r[k + "_err_pct"] = 100.0 * (r[k] - e) / e
            rows.append(r)
            print(f"  e={e:.1f} v0={v:.2f}  LN {r['LN_err_pct']:+7.1f}%  "
                  f"HC {r['HC_err_pct']:+7.1f}%  ID {r['ID_err_pct']:+7.2f}%")
    out["recovery"] = rows
    out["chi_identified"] = {str(k): v for k, v in chi_id.items()}

    b1 = max(abs(r["ID_err_pct"]) for r in rows) <= 0.5
    lo = [r for r in rows if r["e"] < 0.7]
    b2 = all(abs(r["HC_err_pct"]) < abs(r["LN_err_pct"]) for r in lo)
    hi = [r for r in rows if r["e"] >= 0.9]
    b3 = all(max(abs(r[a] - r[b]) / r[b] for a, b in (("LN", "ID"), ("HC", "ID"))) <= 0.02
             for r in hi)

    print("\nbands 4-5: timestep and force convergence, at the nominal restitution")
    e = 0.7
    conv = []
    for h in (4e-8, 2e-8, 1e-8):
        conv.append(dict(h=h, restitution=cl.impact(chi_id[e], K_REF, M, 0.5, h=h),
                         peak_N=cl.peak_force(chi_id[e], K_REF, M, 0.5, h=h)))
        print(f"  h={h:.1e}  e={conv[-1]['restitution']:.6f}  peak={conv[-1]['peak_N']:.2f} N")
    out["convergence"] = conv
    b4 = abs(conv[-1]["restitution"] - conv[-2]["restitution"]) / conv[-2]["restitution"] < 0.005
    b5 = abs(conv[-1]["peak_N"] - conv[-2]["peak_N"]) / conv[-2]["peak_N"] < 0.01

    print("\nband 6: the same VOLLEY case under each law")
    vol = {}
    for name, law in (("LN", "LN"), ("HC", "HC"),
                      ("ID", float(chi_id[0.7]))):
        r = g.run(law=law)
        W = g.gas_work()
        ke = 0.5 * g.M_BODY * float(r["v_exit"][0]) ** 2
        vol[name] = dict(rate_deg_s=float(r["rate_deg_s"][0]), v_exit=float(r["v_exit"][0]),
                         v_lat=float(r["v_lat"][0]), peak_N=float(r["peak_N"][0]),
                         hits=int(r["hits"][0]),
                         energy_residual_pct=100.0 * (W - ke - float(r["e_fric"][0])
                                                      - float(r["e_cont"][0])) / W)
        print(f"  {name}  rate {vol[name]['rate_deg_s']:8.4f} deg/s   "
              f"peak {vol[name]['peak_N']:7.1f} N   "
              f"energy {vol[name]['energy_residual_pct']:+.4f} %")
    out["volley_case"] = vol
    rates = [v["rate_deg_s"] for v in vol.values()]
    spread = (max(rates) - min(rates)) / min(rates) * 100.0
    out["model_form_spread_pct"] = spread
    b6 = spread <= 25.0
    b7 = all(abs(v["energy_residual_pct"]) <= 0.5 for v in vol.values())

    bands = [
        ("1", "ID recovers restitution to 0.5 %",
         f"worst {max(abs(r['ID_err_pct']) for r in rows):.3f} %", b1),
        ("2", "HC beats LN at every e below 0.7",
         f"LN worst {max(abs(r['LN_err_pct']) for r in lo):.1f} %, "
         f"HC worst {max(abs(r['HC_err_pct']) for r in lo):.1f} %", b2),
        ("3", "all three agree within 2 % as e -> 0.9",
         f"LN {hi[0]['LN']:.4f}, HC {hi[0]['HC']:.4f}, ID {hi[0]['ID']:.4f}", b3),
        ("4", "restitution converges, 0.5 % between h and h/2",
         f"{conv[-2]['restitution']:.6f} -> {conv[-1]['restitution']:.6f}", b4),
        ("5", "peak force converges, 1 % between h and h/2",
         f"{conv[-2]['peak_N']:.2f} -> {conv[-1]['peak_N']:.2f} N", b5),
        ("6", "model-form spread on the VOLLEY case <= 25 %",
         f"{spread:.1f} % ({min(rates):.3f} to {max(rates):.3f} deg/s)", b6),
        ("7", "energy closes to 0.5 % under each law",
         f"worst {max(abs(v['energy_residual_pct']) for v in vol.values()):+.4f} %", b7),
    ]
    out["bands"] = [dict(band=n, name=nm, detail=d, pass_=bool(ok)) for n, nm, d, ok in bands]
    print("\nbands:")
    for n, nm, d, ok in bands:
        print(f"  band {n}: {'PASS' if ok else 'FAIL'}  {nm}\n            {d}")

    path = os.path.join(g.RESULTS, "contact_laws.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, default=float)
        fh.write("\n")
    print(f"\nwrote {path}")


if __name__ == "__main__":
    main()
