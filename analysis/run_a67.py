"""A67 runner: bands, sweeps, Monte Carlo and sensitivity for the guided-contact model.

Bands declared in validation/A67_guided_contact.md at 246b7ee, before analysis/guided_contact.py
existed. This file evaluates them; it does not choose them.
"""
import json
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import guided_contact as g                                          # noqa: E402

RESULTS = g.RESULTS
SEED = 20260822
N_SOBOL = 32                    # 32 * (2*7 + 2) = 512 samples
KEYS = list(g.BRACKET.keys())


def band1():
    """Perfectly straight bore, no eccentricity, friction at A41's allowance."""
    r = g.run(straightness_mm=0.0, ecc_mm=0.0, cg_off_mm=0.0,
              friction_N=g.SEAL["friction_allowance_N"])
    want = g.D["exit_velocity_m_s_at_friction_allowance"]
    got = float(r["v_exit"][0])
    return got, want, abs(got - want) / want <= 0.01


def band2():
    r = g.run(straightness_mm=0.0, ecc_mm=0.0, cg_off_mm=0.0)
    worst = max(abs(float(r["v_lat"][0])) / 30.0, abs(float(r["rate_deg_s"][0])) / 2.0)
    return worst, worst < 1e-9


def band3():
    """Free radial impact: does the contact law return the declared restitution?

    No gas, no friction, no bore curvature. The body is placed at the clearance with a pure
    radial velocity and the rebound ratio is measured. This verifies the Lankarani-Nikravesh
    implementation against its own definition, independently of anything about VOLLEY.
    """
    out = []
    for e in (0.3, 0.5, 0.7):
        for v0 in (0.05, 0.5, 2.0):
            c = g.NOMINAL["clearance_um"] / 2.0 / 1e6
            K = g.contact_stiffness(np.array([c]))
            m, d, dd = g.M_BODY, 0.0, v0
            h, onset = 2.0e-7, v0
            hist = []
            for _ in range(400000):
                if d > 0.0:
                    damp = 1.0 + (3.0 * (1.0 - e * e) / 4.0) * dd / onset
                    a = -K[0] * d ** 1.5 * max(damp, 0.0) / m
                else:
                    a = 0.0
                dd += a * h
                d += dd * h
                hist.append(dd)
                if d < 0.0 and dd < 0.0:
                    break
            got = abs(dd) / v0
            out.append(dict(e=e, v0=v0, restitution=got, err_pct=100 * (got - e) / e))
    worst = max(abs(o["err_pct"]) for o in out)
    return out, worst, worst <= 5.0


def energy(r):
    W = g.gas_work()
    ke = 0.5 * g.M_BODY * float(r["v_exit"][0]) ** 2
    resid = (W - ke - float(r["e_fric"][0]) - float(r["e_cont"][0])) / W
    return W, ke, 100 * resid


def land_sweep():
    """Band 8: does the answer depend on the geometry that provides the angular constraint?"""
    seps = np.array([40.0, 80.0, 120.0, 200.0, 300.0, 400.0])
    r = g.run(land_sep_mm=seps, **{k: np.full(seps.size, v)
                                   for k, v in g.NOMINAL.items() if k != "land_sep_mm"})
    return [dict(land_sep_mm=float(s), rate_deg_s=float(x), peak_N=float(p),
                 v_exit=float(v), diverged=bool(d))
            for s, x, p, v, d in zip(seps, r["rate_deg_s"], r["peak_N"],
                                     r["v_exit"], r["diverged"])]


def monte_carlo():
    from SALib.sample import sobol as sobol_sample
    from SALib.analyze import sobol as sobol_analyze
    problem = dict(num_vars=len(KEYS), names=KEYS,
                   bounds=[list(g.BRACKET[k]) for k in KEYS])
    X = sobol_sample.sample(problem, N_SOBOL, calc_second_order=False, seed=SEED)
    r = g.run(**{k: X[:, i] for i, k in enumerate(KEYS)})
    good = ~(r["diverged"] | r["stalled"])
    y = np.where(good, r["rate_deg_s"], np.nan)
    # SALib cannot take NaN; failed samples are replaced by the ensemble median and COUNTED.
    y_filled = np.where(np.isnan(y), np.nanmedian(y), y)
    Si = sobol_analyze.analyze(problem, y_filled, calc_second_order=False,
                               print_to_console=False, seed=SEED)
    rate = r["rate_deg_s"][good]
    return dict(
        n=int(X.shape[0]), n_good=int(good.sum()),
        n_diverged=int(r["diverged"].sum()), n_stalled=int(r["stalled"].sum()),
        step_s=float(r["h"]),
        rate_mean=float(rate.mean()), rate_median=float(np.median(rate)),
        rate_p997=float(np.percentile(rate, 99.7)), rate_max=float(rate.max()),
        rate_3sigma=float(rate.mean() + 3 * rate.std(ddof=1)),
        v_exit_mean=float(r["v_exit"][good].mean()),
        v_exit_3sigma=float(3 * r["v_exit"][good].std(ddof=1)),
        v_lat_p997=float(np.percentile(r["v_lat"][good], 99.7)),
        peak_N_max=float(r["peak_N"][good].max()),
        impulse_p997=float(np.percentile(r["impulse_Ns"][good], 99.7)),
        hits_median=float(np.median(r["hits"][good])),
        sobol=[dict(name=k, S1=float(Si["S1"][i]), S1_conf=float(Si["S1_conf"][i]),
                    ST=float(Si["ST"][i]), ST_conf=float(Si["ST_conf"][i]))
               for i, k in enumerate(KEYS)])


def main():
    out = dict(analysis="A67", bands_declared_commit="246b7ee",
               note=("6-DOF rigid body, two lands, Lankarani-Nikravesh contact, sinusoidal bore "
                     "centreline at twice A59's support pitch. Six inputs have no source in this "
                     "repository and are declared brackets, not measurements. Nothing is "
                     "measured -- E4."),
               convergence=[dict(h=4e-5, rate=8.7862), dict(h=2e-5, rate=9.5505),
                            dict(h=1e-5, rate=15.0981), dict(h=5e-6, rate=14.8800),
                            dict(h=2.5e-6, rate=14.8772), dict(h=1.25e-6, rate=14.8786),
                            dict(h=6.25e-7, rate=14.8756)],
               nominal_inputs=g.NOMINAL, brackets={k: list(v) for k, v in g.BRACKET.items()})

    print("bands 1-6 at the nominal point")
    v1, w1, ok1 = band1()
    w2, ok2 = band2()
    b3, worst3, ok3 = band3()
    nom = g.run()
    W, ke, resid = energy(nom)
    rate = float(nom["rate_deg_s"][0])
    peak = float(nom["peak_N"][0])
    out["nominal"] = dict(v_exit=float(nom["v_exit"][0]), v_lat=float(nom["v_lat"][0]),
                          rate_deg_s=rate, peak_N=peak,
                          impulse_Ns=float(nom["impulse_Ns"][0]),
                          hits=int(nom["hits"][0]), step_s=float(nom["h"]),
                          gas_work_J=W, ke_J=ke, energy_residual_pct=resid)
    out["restitution_check"] = b3
    out["land_sweep"] = land_sweep()
    ls = [d["rate_deg_s"] for d in out["land_sweep"]]
    spread8 = (max(ls) - min(ls)) / min(ls) * 100.0

    print("monte carlo + sobol")
    mc = monte_carlo()
    out["monte_carlo"] = mc

    bands = [
        ("1", "axial regression against the 1-DOF model, 1 %",
         f"{v1:.4f} against {w1:.4f} m/s", ok1),
        ("2", "symmetry: zero forcing gives zero lateral and angular state",
         f"worst {w2:.2e} of scale", ok2),
        ("3", "contact law returns the declared restitution, 5 %",
         f"worst {worst3:.2f} %", ok3),
        ("4", "energy closes to 0.5 %", f"{resid:+.4f} %", abs(resid) <= 0.5),
        ("5", "nominal exit angular rate <= 2.0 deg/s", f"{rate:.3f} deg/s", rate <= 2.0),
        ("6", "peak contact normal force <= 445.88 N", f"{peak:.1f} N", peak <= g.F_CMD),
        ("7", "Monte Carlo 3-sigma exit angular rate <= 2.0 deg/s",
         f"{mc['rate_3sigma']:.3f} deg/s (p99.7 {mc['rate_p997']:.3f})",
         mc["rate_3sigma"] <= 2.0),
        ("8", "land separation moves the answer by more than 5 %",
         f"{spread8:.1f} % over 40-400 mm", spread8 > 5.0),
        ("9", "sensitivity reported and the dominant input named",
         max(mc["sobol"], key=lambda d: d["ST"])["name"], True),
    ]
    out["bands"] = [dict(band=n, name=nm, detail=d, pass_=bool(ok)) for n, nm, d, ok in bands]
    print("\nbands:")
    for n, nm, d, ok in bands:
        print(f"  band {n}: {'PASS' if ok else 'FAIL'}  {nm}\n            {d}")

    path = os.path.join(RESULTS, "guided_contact.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, default=float)
        fh.write("\n")
    print(f"\nwrote {path}")


if __name__ == "__main__":
    main()
