"""P113-S16: same-epoch two-body correction to the timing-only phase claim."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

from host_reference import MU, RE

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/results/phasing_reference.json"
FIG = ROOT / "figures/phasing_reference.svg"
SHEET = ROOT / "validation/P113_S16_phasing_correction.md"
ALTITUDE_M = 450_000.0
DELAY_S = 468.0
AFTER_S = 86_400.0
SPEEDS = (0.0, 1.0, 2.0, 10.0, 16.029)
SAMPLES = 241


def circular_state(time_s):
    radius = RE + ALTITUDE_M
    n = math.sqrt(MU / radius**3)
    theta = n * time_s
    return np.array([radius*math.cos(theta), radius*math.sin(theta),
                     -radius*n*math.sin(theta), radius*n*math.cos(theta)])


def release_state(time_s, speed):
    y = circular_state(time_s)
    tangential = y[2:] / np.linalg.norm(y[2:])
    y[2:] += speed * tangential
    return y


def propagate(initial, duration, times, tight=False):
    def rhs(_t, y):
        radius = np.linalg.norm(y[:2])
        return np.r_[y[2:], -MU*y[:2]/radius**3]
    r = solve_ivp(rhs, (0, duration), initial, method="DOP853", t_eval=times,
                  rtol=2e-13 if tight else 2e-11,
                  atol=1e-12 if tight else 1e-10, max_step=75 if tight else 300)
    if not r.success:
        raise RuntimeError(r.message)
    return r.y.T


def case(speed, tight=False):
    after = np.linspace(0, AFTER_S, SAMPLES)
    a = propagate(release_state(0, speed), DELAY_S+AFTER_S, DELAY_S+after, tight)
    b = propagate(release_state(DELAY_S, 0.0), AFTER_S, after, tight)
    theta_a = np.unwrap(np.arctan2(a[:, 1], a[:, 0]))
    theta_b = np.unwrap(np.arctan2(b[:, 1], b[:, 0]))
    # Both unwrap from near the same phase at the first common epoch.
    phase = np.degrees(theta_a-theta_b)
    delta_state = a[0]-b[0]
    return dict(speed_m_s=speed, phase_deg=phase.tolist(),
                second_release_position_gap_m=float(np.linalg.norm(delta_state[:2])),
                second_release_velocity_gap_m_s=float(np.linalg.norm(delta_state[2:])),
                endpoint_phase_deg=float(phase[-1]))


def main():
    rows = [case(speed) for speed in SPEEDS]
    tight = [case(speed, tight=True) for speed in SPEEDS]
    zero = rows[0]
    convergence = max(abs(a["endpoint_phase_deg"]-b["endpoint_phase_deg"])
                      for a, b in zip(rows, tight))
    radius = RE + ALTITUDE_M
    n0 = math.sqrt(MU/radius**3)
    speed0 = math.sqrt(MU/radius)
    # A first-order same-epoch trend: the first released 10 m/s object has
    # approximately DELAY_S more time on the altered orbit than the second.
    a10 = 1/(2/radius-(speed0+10)**2/MU)
    n10 = math.sqrt(MU/a10**3)
    trend_deg = math.degrees((n10-n0)*DELAY_S)
    # Compare the first object's phase relative to the second at the second
    # release epoch. One-day phase includes their slightly offset initial phase.
    trend_error = abs(rows[3]["phase_deg"][0]-trend_deg)
    checks = dict(zero_position_gap_m=zero["second_release_position_gap_m"] < .001,
                  zero_velocity_gap_m_s=zero["second_release_velocity_gap_m_s"] < 1e-6,
                  zero_one_day_phase_deg=abs(zero["endpoint_phase_deg"]) < 1e-4,
                  mean_motion_trend_deg=trend_error < 3,
                  integration_convergence_deg=convergence < .01)
    data = dict(study="P113-S16",status="CORRECTIVE_TWO_BODY_MODEL",
                inputs=dict(altitude_m=ALTITUDE_M,release_delay_s=DELAY_S,
                            after_second_release_s=AFTER_S,speeds_m_s=SPEEDS,
                            samples=SAMPLES,mu_m3_s2=MU,re_m=RE),
                time_after_second_release_s=np.linspace(0,AFTER_S,SAMPLES).tolist(),
                cases=rows,checks=checks,
                convergence_max_endpoint_deg=convergence,
                mean_motion_initial_trend_deg=trend_deg,
                source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                               for p in (Path(__file__),SHEET)})
    OUT.write_text(json.dumps(data,indent=2,allow_nan=False)+"\n")
    if not all(checks.values()):
        raise SystemExit(f"checks failed: {checks}")

    plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10,
                         "svg.hashsalt":"P113-S16-2026-10-09"})
    fig,ax=plt.subplots(figsize=(9,5),dpi=150)
    fig.patch.set_facecolor("white");ax.set_facecolor("#f7fafc")
    palette=["#c54f4f","#8194a2","#197e91","#a878cc","#dd9b38"]
    t=np.asarray(data["time_after_second_release_s"])/3600
    for row,color in zip(rows,palette):
        ax.plot(t,row["phase_deg"],lw=2.1,color=color,
                label=f'{row["speed_m_s"]:g} m/s relative impulse')
    ax.set(xlabel="Hours after second release (common epoch)",
           ylabel="In-track angular phase: first minus second (deg)")
    ax.grid(color="#d7e0e7",lw=.8)
    for spine in ax.spines.values():spine.set_visible(False)
    ax.legend(frameon=False,loc="lower left")
    ax.set_title("Waiting alone creates no persistent relative phase",
                 loc="left",fontweight="bold",color="#102d44",pad=13)
    fig.text(.5,.018,
             "450 km circular reference · 468 s delay · first payload receives indicated impulse; second receives zero · two-body model",
             ha="center",fontsize=8.3,color="#4f6474")
    fig.subplots_adjust(left=.10,right=.97,top=.87,bottom=.17)
    fig.savefig(FIG,metadata={"Date":"2026-10-09","Creator":"VOLLEY P113-S16"})
    fig.savefig(FIG.with_suffix(".png"),dpi=180,
                metadata={"Software":"VOLLEY P113-S16"})
    print(checks)
    print(f"zero endpoint {zero['endpoint_phase_deg']:.8g} deg; "
          f"tight change {convergence:.6g} deg")


if __name__ == "__main__":
    main()
