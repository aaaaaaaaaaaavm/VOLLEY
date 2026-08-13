"""A29: turn the CFD force into the ground-test correction, and check the declared bands.

Bands are in validation/A29_ground_test_air_drag.md, committed at 949fdf4 before this
directory existed.

The chain, stated so each link can be checked separately:
    CFD  ->  drag force at exit velocity
         ->  work done against air over the 1.30 m stroke, using the profile's own v(x)
         ->  exit-velocity deficit
         ->  that deficit compared to the design point AND to the dispersion the test measures
"""
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "analysis"))
import motor_model as mm  # noqa: E402

import forces  # noqa: E402

DISPERSION_3SIG = None      # filled from motor_results.json; never hard-coded


def force_history(case, meta, window=5):
    """Drag at the last `window` written times, so the wake's unsteadiness is visible.

    A steady solver on a massively separated bluff-body wake does not converge, it
    plateaus and oscillates. Reading one iteration reports a sample of that oscillation as
    though it were an answer, which is the reason this function exists.
    """
    path = os.path.join(HERE, case)
    times = sorted((d for d in os.listdir(path) if d.replace('.', '', 1).isdigit()),
                   key=float)[-window:]
    out = []
    for t in times:
        r = forces.analyse(path, meta["rho"], meta["U_inf"], meta["frontal_area_m2"],
                           meta["L_m"], time=t)
        out.append(dict(time=float(t), drag_N=r["drag_N"], Cd=r["Cd"],
                        Cd_pressure=r["Cd_pressure"]))
    return out


def deficit(drag_at_exit, v_exit, m, L=None):
    """Exit-velocity deficit from air over the acceleration zone.

    The profile is position-scheduled as v = v_target*sqrt(x/L), so v^2 is LINEAR in x and
    the drag force, which goes as v^2, is linear in x too. The work is therefore
    F_max*L/2, not F_max*L -- getting this wrong would double the answer.
    """
    L = mm.ACCEL_ZONE if L is None else L
    W = 0.5 * drag_at_exit * L
    v_air = math.sqrt(max(v_exit ** 2 - 2 * W / m, 0.0))
    return dict(work_J=W, v_vacuum=v_exit, v_air=v_air, deficit_m_s=v_exit - v_air,
                deficit_pct=100 * (v_exit - v_air) / v_exit)


if __name__ == "__main__":
    meta = json.load(open(os.path.join(HERE, "case_meta.json")))
    res = json.load(open(os.path.join(HERE, "..", "..", "analysis", "results",
                                      "motor_results.json")))
    DISPERSION_3SIG = float(res["closed_loop_3sigma"])
    m = mm.M_SAT + mm.M_SLED
    v = float(res["shot"]["v_exit"])

    hist = {}
    for case in [c for c in ("free", "channel", "free_fine", "channel_fine")
                 if os.path.isdir(os.path.join(HERE, c))]:
        hist[case] = force_history(case, meta[case])
        d = np.array([h["drag_N"] for h in hist[case]])
        print(f"{case:14s} drag over last {len(d)} written times: "
              f"mean {d.mean():.4f} N, spread +/-{0.5*(d.max()-d.min()):.4f} N "
              f"({100*0.5*(d.max()-d.min())/d.mean():.1f} %)")

    def mean_drag(c):
        return float(np.mean([h["drag_N"] for h in hist[c]]))

    def mean_cd(c):
        return float(np.mean([h["Cd"] for h in hist[c]]))

    out = dict(v_exit=v, moving_mass_kg=m, accel_zone_m=mm.ACCEL_ZONE,
               dispersion_3sigma=DISPERSION_3SIG, history=hist)

    free = mean_drag("free")
    dfc = deficit(free, v, m)
    out["free"] = dict(drag_N=free, Cd=mean_cd("free"), **dfc)
    print(f"\nfree stream:  Cd {mean_cd('free'):.4f}, drag {free:.4f} N at {v:.3f} m/s")
    print(f"              work over {mm.ACCEL_ZONE} m = {dfc['work_J']:.4f} J")
    print(f"              v {dfc['v_vacuum']:.4f} -> {dfc['v_air']:.4f} m/s, "
          f"deficit {dfc['deficit_m_s']*1e3:.3f} mm/s ({dfc['deficit_pct']:.4f} %)")

    bands = {}
    if "free_fine" in hist:
        cf, cc = mean_cd("free_fine"), mean_cd("free")
        e = 100 * abs(cf - cc) / cf
        bands["1"] = ("fine and coarse mesh agree within 10 %",
                      f"Cd {cc:.4f} coarse vs {cf:.4f} fine -> {e:.2f} %", bool(e <= 10.0))
    bands["2"] = ("0.7 <= Cd <= 2.5", f"{mean_cd('free'):.4f}",
                  bool(0.7 <= mean_cd("free") <= 2.5))
    bands["3"] = ("deficit below 1.0 % of v_exit",
                  f"{dfc['deficit_pct']:.4f} % ({dfc['deficit_m_s']*1e3:.2f} mm/s)",
                  bool(dfc["deficit_pct"] < 1.0))
    r4 = dfc["deficit_m_s"] / DISPERSION_3SIG
    bands["4"] = (f"deficit >= 10 % of the {DISPERSION_3SIG:.4f} m/s dispersion",
                  f"{100*r4:.1f} % of it", bool(r4 >= 0.10))
    if "channel" in hist:
        ch, fr = mean_cd("channel"), mean_cd("free")
        rise = 100 * (ch - fr) / fr
        dch = deficit(mean_drag("channel"), v, m)
        out["channel"] = dict(drag_N=mean_drag("channel"), Cd=ch, **dch)
        print(f"in channel:   Cd {ch:.4f}, drag {mean_drag('channel'):.4f} N, "
              f"deficit {dch['deficit_m_s']*1e3:.3f} mm/s")
        print(f"              confinement raises Cd by {rise:+.1f} %")
        bands["5"] = ("channel Cd exceeds free-stream Cd by >= 10 %",
                      f"{rise:+.1f} %", bool(rise >= 10.0))

    print("\nbands:")
    for k in sorted(bands):
        name, detail, ok = bands[k]
        print(f"  band {k}: {'PASS' if ok else 'FAIL'}  {name}\n            {detail}")
    out["bands"] = [dict(band=k, name=bands[k][0], detail=bands[k][1], passed=bands[k][2])
                    for k in sorted(bands)]

    # What the servo does with it, which is a different question from what the band asks.
    F_cmd = float(res["shot"]["F_cmd"])
    out["closed_loop"] = dict(
        extra_force_N=free, pct_of_commanded_force=100 * free / F_cmd,
        note=("The bands measure the OPEN-LOOP deficit, which is what a raw shot comparison "
              "sees. A servo tracking the velocity profile nulls it instead, and it appears "
              "as commanded force rather than as velocity error."))
    print(f"\nclosed loop:  the servo absorbs it as {free:.3f} N of extra command, "
          f"{100*free/F_cmd:.3f} % of the {F_cmd:.0f} N shot")

    dest = os.path.join(HERE, "..", "..", "analysis", "results", "cfd_air_drag.json")
    json.dump(out, open(dest, "w"), indent=2)
    print(f"\n-> {os.path.relpath(dest, os.path.join(HERE, '..', '..'))}")
