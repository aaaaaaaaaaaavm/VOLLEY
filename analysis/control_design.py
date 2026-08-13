"""
VOLLEY | The velocity loop: plant, margins, bandwidth, latency, and what the loop really gives.

WHY THIS EXISTS
---------------
docs/BASELINE.md publishes a 3-sigma closed-loop dispersion. That figure comes from
motor_model.closed_loop_mc(), which used proportional velocity feedback at a gain of 3500 --
asserted, never derived. There is no plant model, no transfer function, no gain or phase
margin, no controller sample rate, no sensor dynamics, and no check that the loop bandwidth
stays clear of the track's structural modes.

A headline number produced by an undesigned loop is an assumption wearing a result's clothes.

Bands declared in validation/A28_control_stability.md at 3ae36ad, BEFORE this file existed.

Provenance: model output. Sensor latency and rate are STATED ASSUMPTIONS (E7: no sensor has
been selected or characterised) and are swept rather than asserted.
"""
import json
import math
import os

import numpy as np

import motor_model as mm
import sizing

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

M = mm.M_SAT + mm.M_SLED                 # moving mass, kg
KP_PUBLISHED = 3500.0                    # the gain closed_loop_mc carried when these bands
                                         # were declared; A28's finding replaced it (P47)
F_MODE_HZ = 109.0                        # track first mode, sizing.py (fixed-fixed)
F_MODE2_HZ = 48.0                        # the second mode A17's chirp also sweeps
T_STROKE = 0.1586                        # s

# Stated assumptions, not measurements. E7 stands.
F_SAMPLE_HZ = 5000.0                     # controller rate
LATENCY_S = 0.0006                       # sensor + computation transport delay


_KT_CACHE = []


def kt():
    """motor_model's thrust constant, computed once. It is a magpylib field integral."""
    if not _KT_CACHE:
        _KT_CACHE.append(mm.thrust_constant()[0])
    return _KT_CACHE[0]


def plant_gain(Kt=None):
    """Velocity-loop plant: commanded sheet current K -> velocity. P(s) = Kt/(M s).

    A pure integrator: force is proportional to command and velocity is its integral over
    the moving mass. Damping is negligible over the stroke (no friction model exists), which
    is stated rather than assumed away.
    """
    return (kt() if Kt is None else Kt) / M   # (m/s^2) per (A/m) of sheet current


def total_lag(latency, hold=True):
    """Every source of pure phase lag in the loop, in seconds.

    Transport delay plus the zero-order hold's half-sample. Both are pure delays, so they
    add; nothing else in this loop contributes phase beyond the integrator's fixed -90 deg.
    """
    return latency + (0.5 / F_SAMPLE_HZ if hold else 0.0)


def loop_gain_per_s(Kp, kt_ratio=1.0, m_ratio=1.0):
    """Open-loop gain of the velocity error loop, in rad/s.

    THIS IS THE POINT THE ANALYSIS TURNS ON. motor_model's control law is

        Kc = (m_hat * a_ff + Kp * (v_plan - v) * m_hat) / Kt_hat

    which divides the commanded sheet current by the modelled thrust constant and multiplies
    by the modelled mass. Substituting into the plant a = Kt*Kc/m, the Kt/m of the machine
    cancels the Kt_hat/m_hat of the controller and the acceleration becomes

        a = a_ff + Kp * (v_plan - v) * (Kt/Kt_hat) * (m_hat/m)

    So Kp is not a current gain. It is a feedback-linearised acceleration-per-unit-velocity-
    error, with units of s^-1, and the loop transfer is L(s) = Kp/s * exp(-s*tau) -- the
    plant's Kt/M appears nowhere. **The crossover frequency is therefore Kp itself.**

    The cancellation is exact only if the controller's Kt_hat and m_hat are right. The two
    ratios carry the mismatch; motor_model's own Monte Carlo disperses Kt by 0.8 % and mass
    by 0.67 %, so the residual loop-gain error is under 1.5 % and moves no margin materially.
    That is worth stating rather than assuming: a feedback-linearising controller that is
    wrong about the machine is a controller with an unmodelled gain error.
    """
    return Kp * kt_ratio / m_ratio


def open_loop(w, Kp, Kt=None, latency=0.0, hold=True):
    """L(jw) for the published velocity loop: L(s) = Kp/s * exp(-s*tau).

    `Kt` is accepted and ignored for the loop transfer -- see loop_gain_per_s for why it
    cancels -- and is kept in the signature because plant_gain() below is the same machine
    seen without the linearising controller.
    """
    L = loop_gain_per_s(Kp) / (1j * w)
    tau = total_lag(latency, hold)
    if tau:
        L = L * np.exp(-1j * w * tau)
    return L


def margins(Kp, Kt=None, latency=LATENCY_S, hold=True):
    """Gain and phase margin, and the crossover, in closed form.

    For L(jw) = Kp/(jw) * exp(-jw*tau) the magnitude is Kp/w and the phase is -90 deg - w*tau,
    both monotonic, so the two crossings are exact rather than scanned:

        gain crossover   |L| = 1        ->  wc   = Kp
        phase crossover  arg L = -180   ->  w180 = pi/(2*tau)

    verify_margins() checks these against a brute-force scan of the same expression.
    """
    g = loop_gain_per_s(Kp)
    tau = total_lag(latency, hold)
    wc = g
    pm = 90.0 - math.degrees(wc * tau)
    if tau > 0:
        w180 = math.pi / (2 * tau)
        gm_db = -20 * math.log10(g / w180)
    else:
        w180, gm_db = float('inf'), float('inf')   # no phase crossover without delay
    return dict(Kp=Kp, wc_rad_s=float(wc), f_c_Hz=float(wc / (2 * math.pi)),
                phase_margin_deg=float(pm), gain_margin_dB=float(gm_db),
                w_180_rad_s=float(w180))


def verify_margins(Kp, Kt=None, latency=LATENCY_S, n=400000):
    """Brute-force scan of the same L(jw), to check the closed forms above."""
    w = np.logspace(0, 6, n)
    L = open_loop(w, Kp, Kt, latency)
    mag, ph = np.abs(L), np.unwrap(np.angle(L))
    i = int(np.argmin(np.abs(mag - 1.0)))
    j = int(np.argmin(np.abs(ph + np.pi)))
    return dict(f_c_Hz=float(w[i] / (2 * np.pi)),
                phase_margin_deg=float(180 + np.degrees(ph[i])),
                gain_margin_dB=float(-20 * np.log10(mag[j])))


def closed_bandwidth(Kp, Kt=None, latency=LATENCY_S, hold=True):
    """-3 dB bandwidth of T = L/(1+L), in Hz.

    With a = w/Kp and tau the total lag, |1 + 1/L|^2 = 1 - 2 a sin(w tau) + a^2, so the
    -3 dB point is the smallest positive root of that minus 10^(3/10). Bracketed on a coarse
    grid, then bisected -- no fine global scan.

    An unstable loop has no meaningful -3 dB bandwidth; the caller checks the margins.
    """
    g = loop_gain_per_s(Kp)
    tau = total_lag(latency, hold)
    target = 10 ** (3 / 10.0)

    def f(w):
        a = w / g
        return 1.0 - 2 * a * math.sin(w * tau) + a * a - target

    grid = np.logspace(-2, 7, 4000)
    vals = np.array([f(x) for x in grid])
    sign = np.where(np.diff(np.sign(vals)) != 0)[0]
    if len(sign) == 0:
        return float('inf')
    lo, hi = grid[sign[0]], grid[sign[0] + 1]
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if f(lo) * f(mid) <= 0:
            hi = mid
        else:
            lo = mid
    return float(0.5 * (lo + hi) / (2 * math.pi))


def design_gain(target_pm_deg=50.0, latency=LATENCY_S, Kt=None):
    """Largest proportional gain meeting a phase-margin target AND band 3's bandwidth cap."""
    lo, hi = 1.0, 1e6
    cap = F_MODE_HZ / 3.0
    best = lo
    for _ in range(120):
        mid = math.sqrt(lo * hi)
        m = margins(mid, Kt, latency)
        bw = closed_bandwidth(mid, Kt, latency)
        if m['phase_margin_deg'] >= target_pm_deg and bw <= cap:
            best, lo = mid, mid
        else:
            hi = mid
    return best


def mc_with_gain(Kp, n=800, v_target=mm.V_FLEET, latency=LATENCY_S, seed0=0):
    """motor_model's own Monte Carlo, with the gain and a transport delay made explicit."""
    Kt, _ = mm.thrust_constant()
    out, sat, stalled = [], [], []
    lag = max(1, int(round(latency / 2e-4)))
    for s in range(seed0, seed0 + n):
        r = np.random.default_rng(s)
        Ktf = Kt * (1 + r.normal(0, 0.008))
        mf = M * (1 + r.normal(0, 0.0067))
        x = v = 0.0
        dt = 2e-4
        hist, nsat, nstep = [], 0, 0
        # An unstable loop does not terminate: v oscillates about the profile and x can
        # stall or reverse. Cap the run at 20x the nominal stroke time and report it,
        # rather than hanging or silently reporting the last value before a hang.
        max_steps = int(20 * T_STROKE / dt)
        while x < mm.ACCEL_ZONE and nstep < max_steps:
            v_plan = v_target * math.sqrt(max(x, 1e-6) / mm.ACCEL_ZONE)
            v_fb = hist[-lag] if len(hist) >= lag else 0.0      # delayed measurement
            Kc_raw = (mf * v_target ** 2 / (2 * mm.ACCEL_ZONE)
                      + Kp * (v_plan - v_fb) * mf) / Ktf
            Kc = min(max(Kc_raw, 0), mm.K_RATED)
            if Kc_raw > mm.K_RATED:
                nsat += 1
            nstep += 1
            v += Ktf * Kc * (1 + r.normal(0, 0.005)) / mf * dt
            x += v * dt
            hist.append(v)
        ran_out = nstep >= max_steps
        v_meas = v + r.normal(0, 0.008)
        v += min(max(v_target - v_meas, -0.3), 0.3) + r.normal(0, 0.004)
        out.append(v)
        sat.append(nsat / max(nstep, 1))
        stalled.append(ran_out)
    a = np.array(out)
    return dict(mean=float(a.mean()), sigma3=float(3 * a.std()),
                sat_frac=float(np.mean(sat)),
                stalled_frac=float(np.mean(stalled)),
                v_min=float(a.min()), v_max=float(a.max()))


def gain_sweep(gains, latency=LATENCY_S):
    rows = []
    for g in gains:
        m = margins(g, latency=latency)
        rows.append(dict(Kp=g, f_c_Hz=m['f_c_Hz'], pm=m['phase_margin_deg'],
                         gm=m['gain_margin_dB'], bw_Hz=closed_bandwidth(g, latency=latency)))
    return rows


if __name__ == '__main__':
    Kt = kt()
    tau = total_lag(LATENCY_S)
    print(f"moving mass        {M:.3f} kg   (M_SAT {mm.M_SAT} + M_SLED {mm.M_SLED})")
    print(f"thrust constant    {Kt*1e3:.4f} N per kA/m")
    print(f"physical plant     Kt/M = {plant_gain():.6f} (m/s^2) per (A/m)")
    print(f"loop transfer      L(s) = Kp/s * exp(-s*tau),  tau = {tau*1e3:.3f} ms")
    print(f"                   ({LATENCY_S*1e3:.1f} ms transport + "
          f"{0.5/F_SAMPLE_HZ*1e3:.2f} ms zero-order hold at {F_SAMPLE_HZ:.0f} Hz)")
    print(f"track modes        {F_MODE2_HZ:.0f} Hz and {F_MODE_HZ:.0f} Hz\n")

    # ---- Band 1: the plant reproduces the machine, feedback off. -----------------------
    a_ol = Kt * 0.9 * mm.K_RATED / M
    v_ol = math.sqrt(2 * a_ol * mm.ACCEL_ZONE)
    v_ref = mm.shot(Kt)['v_exit']
    e1 = 100 * abs(v_ol - v_ref) / v_ref
    print(f"BAND 1  open-loop plant {v_ol:.4f} m/s vs motor_model.shot {v_ref:.4f} m/s"
          f"  ->  {e1:.4f} %")

    # ---- Bands 2 and 3: the published gain. -------------------------------------------
    m_pub = margins(KP_PUBLISHED)
    bw_pub = closed_bandwidth(KP_PUBLISHED)
    v_pub = verify_margins(KP_PUBLISHED)
    print(f"\nBAND 2  Kp = {KP_PUBLISHED:.0f} s^-1, as published")
    print(f"        gain crossover  {m_pub['f_c_Hz']:9.1f} Hz")
    print(f"        phase margin    {m_pub['phase_margin_deg']:9.1f} deg   "
          f"(band >= 45)   [scan check {v_pub['phase_margin_deg']:.1f}]")
    print(f"        gain margin     {m_pub['gain_margin_dB']:9.2f} dB    "
          f"(band >= 6)    [scan check {v_pub['gain_margin_dB']:.2f}]")
    print(f"\nBAND 3  closed-loop bandwidth {bw_pub:9.1f} Hz  "
          f"(band <= {F_MODE_HZ/3:.1f} Hz)")

    # ---- Band 5: the latency sweep. ---------------------------------------------------
    print(f"\nBAND 5  phase margin against transport delay, at Kp = {KP_PUBLISHED:.0f}:")
    lat_rows = []
    for lat in (0.0, 0.0001, 0.0002, 0.0004, 0.0006, 0.001, 0.002):
        mi = margins(KP_PUBLISHED, latency=lat)
        lat_rows.append(dict(latency_s=lat, phase_margin_deg=mi['phase_margin_deg'],
                             gain_margin_dB=mi['gain_margin_dB']))
        print(f"        {lat*1e3:5.2f} ms -> PM {mi['phase_margin_deg']:8.1f} deg, "
              f"GM {mi['gain_margin_dB']:7.2f} dB")
    # the delay at which the published gain reaches marginal stability
    tau_crit = (math.pi / 2) / KP_PUBLISHED
    print(f"        marginal stability at total lag {tau_crit*1e6:.0f} us "
          f"= transport {max(tau_crit - 0.5/F_SAMPLE_HZ, 0)*1e6:.0f} us "
          f"once the {0.5/F_SAMPLE_HZ*1e6:.0f} us hold is paid")

    # ---- The designed gain. -----------------------------------------------------------
    Kp_des = design_gain()
    m_des = margins(Kp_des)
    bw_des = closed_bandwidth(Kp_des)
    print(f"\nDESIGNED Kp = {Kp_des:.1f} s^-1: crossover {m_des['f_c_Hz']:.1f} Hz, "
          f"PM {m_des['phase_margin_deg']:.1f} deg, GM {m_des['gain_margin_dB']:.1f} dB, "
          f"BW {bw_des:.1f} Hz")
    print(f"         largest gain meeting PM >= 50 deg AND bandwidth <= "
          f"{F_MODE_HZ/3:.1f} Hz at {LATENCY_S*1e3:.1f} ms latency")

    sweep = gain_sweep([50, 100, 195.2, 250, 500, 1000, 2000, 3500, 5000])
    print("\n  gain sweep")
    print(f"  {'Kp, 1/s':>9s} {'f_c, Hz':>9s} {'PM, deg':>9s} {'GM, dB':>8s} {'BW, Hz':>9s}")
    for r in sweep:
        print(f"  {r['Kp']:9.1f} {r['f_c_Hz']:9.1f} {r['pm']:9.1f} {r['gm']:8.2f} "
              f"{r['bw_Hz']:9.1f}")

    # ---- Bands 4 and 6: Monte Carlo. --------------------------------------------------
    print("\nBANDS 4/6  Monte Carlo, 800 samples each, "
          f"with the {LATENCY_S*1e3:.1f} ms measurement delay carried in the loop:")
    rows = {}
    for tag, kp in (("published 3500", KP_PUBLISHED), (f"designed {Kp_des:.0f}", Kp_des)):
        r = mc_with_gain(kp)
        rows[tag] = r
        print(f"  {tag:18s} mean {r['mean']:.4f} m/s   3sigma {r['sigma3']:.4f} m/s   "
              f"command over rating {100*r['sat_frac']:.1f} % of stroke")

    pub_tag, des_tag = "published 3500", f"designed {Kp_des:.0f}"
    b = {
        '1': ('plant reproduces motor_model.shot within 1 %', f"{e1:.4f} %", bool(e1 <= 1.0)),
        '2': ('published gain: PM >= 45 deg and GM >= 6 dB',
              f"PM {m_pub['phase_margin_deg']:.1f} deg, GM {m_pub['gain_margin_dB']:.2f} dB",
              bool(m_pub['phase_margin_deg'] >= 45 and m_pub['gain_margin_dB'] >= 6)),
        '3': (f'closed-loop bandwidth <= {F_MODE_HZ/3:.1f} Hz', f"{bw_pub:.1f} Hz",
              bool(bw_pub <= F_MODE_HZ / 3)),
        '4': ('command at or below K_RATED for >= 95 % of stroke',
              f"{100*(1-rows[pub_tag]['sat_frac']):.1f} %",
              bool(rows[pub_tag]['sat_frac'] <= 0.05)),
        '5': (f'PM >= 30 deg at {LATENCY_S*1e3:.1f} ms latency',
              f"{m_pub['phase_margin_deg']:.1f} deg",
              bool(m_pub['phase_margin_deg'] >= 30)),
        '6': ('designed-controller 3sigma within 2x of 0.027 m/s',
              f"{rows[des_tag]['sigma3']:.4f} m/s",
              bool(0.0135 <= rows[des_tag]['sigma3'] <= 0.054)),
    }
    print("\nbands:")
    npass = 0
    for k in sorted(b):
        name, detail, ok = b[k]
        npass += ok
        print(f"  band {k}: {'PASS' if ok else 'FAIL'}  {name}\n            {detail}")
    print(f"\n{npass} of {len(b)} bands pass.")

    os.makedirs(RESULTS, exist_ok=True)
    json.dump(dict(M_kg=M, Kt_N_per_kA=Kt * 1e3,
                   plant='physical Kt/(M s); loop after feedback linearisation Kp/s',
                   plant_gain_per_A_per_m=plant_gain(),
                   f_sample_Hz=F_SAMPLE_HZ, latency_s=LATENCY_S, total_lag_s=tau,
                   tau_marginal_s=tau_crit,
                   track_modes_Hz=[F_MODE2_HZ, F_MODE_HZ],
                   band1_open_loop_v=v_ol, band1_reference_v=v_ref, band1_error_pct=e1,
                   published=dict(**m_pub, bandwidth_Hz=bw_pub, scan_check=v_pub),
                   designed=dict(**m_des, bandwidth_Hz=bw_des),
                   gain_sweep=sweep, latency_sweep=lat_rows, monte_carlo=rows,
                   bands=[dict(band=k, name=b[k][0], detail=b[k][1], passed=b[k][2])
                          for k in sorted(b)]),
              open(os.path.join(RESULTS, 'control_design.json'), 'w'), indent=2)
    print("-> results/control_design.json")
