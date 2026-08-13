"""
A32: the entry transient and segment handover of the plate drive.

Bands declared in validation/A32_entry_transient.md at HEAD~0, BEFORE this file existed.

THE MODEL, AND WHY IT IS A DIFFERENT ONE
----------------------------------------
A31 solved the steady state in the frequency domain with a layered-media model. This solves the
transient in the time domain with a thin-sheet model, on purpose: two models that agree are
worth more than one model run twice, and band 1 is the comparison.

The secondary carries a stream function psi with K = curl(psi z_hat). Including the sheet's own
reaction field gives each spatial mode k its own magnetic diffusion time

    tau_k = mu0 * sigma_s / (2k) * coth(k * g_e / 2)

-- the coth is the effect of the iron either side, which returns the flux and raises the
inductance. **That time constant is what the transient turns on and it is absent from every
steady-state result in this project.** In Fourier space each mode obeys

    dpsi_k/dt + psi_k / tau_k = -(2 / (mu0 k)) * (1/tau_k) * Bext_k

so a step in the imposed field decays into steady state with tau_k, and a travelling wave at
slip frequency reproduces the frequency-domain answer. Both are checked.

The imposed field is WINDOWED in x, so an energised segment has edges, and a plate straddling a
segment boundary falls out of the same solve as the entry transient.

Provenance: model output. Nothing measured. E4 stands.
"""
import json
import math
import os

import numpy as np

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
MU0 = 4e-7 * math.pi

PLATE_W, PLATE_LEN, PLATE_T = 0.090, 0.3405, 0.003
SIGMA = 2.5e7
TAU = 0.048
GAP_MECH = 0.002
G_EFF = 2 * GAP_MECH + PLATE_T
SIGMA_S = SIGMA * PLATE_T
SEG_LEN = 0.325                 # 1.30 m acceleration zone in four segments
BG = 0.60                       # the flux density A31's sweep designs to


def tau_mode(k, g_e=G_EFF, sigma_s=SIGMA_S):
    """Magnetic diffusion time of one spatial mode of the sheet, with iron either side."""
    if k == 0:
        return np.inf
    return MU0 * sigma_s / (2 * k) / math.tanh(k * g_e / 2)


def run(v, slip_freq, duration, window=None, Bg=BG, tau=TAU, nx=1024, dt=2e-6,
        L_domain=None):
    """Time-march the sheet under a windowed travelling field. Returns thrust history.

    `window(x_lab)` returns 1 where the stator is energised. The plate occupies the middle
    PLATE_LEN of the domain and moves at `v`, so the window is evaluated in lab coordinates
    that slide past it.
    """
    L = L_domain or (4 * PLATE_LEN)
    x = np.linspace(0, L, nx, endpoint=False)
    dx = x[1] - x[0]
    k_all = 2 * np.pi * np.fft.rfftfreq(nx, dx)
    taus = np.array([tau_mode(kk) if kk > 0 else np.inf for kk in k_all])
    decay = np.where(np.isfinite(taus), np.exp(-dt / np.maximum(taus, 1e-12)), 1.0)

    kw = math.pi / tau
    w_slip = 2 * math.pi * slip_freq

    # The plate occupies a fixed band of the domain; the field pattern and the window slide.
    x0 = (L - PLATE_LEN) / 2
    on_plate = (x >= x0) & (x < x0 + PLATE_LEN)

    psi = np.zeros(nx)
    t = 0.0
    hist_t, hist_F, hist_amp = [], [], []
    n = int(round(duration / dt))
    for _ in range(n):
        x_lab = x + v * t
        Bext = Bg * np.cos(kw * x + w_slip * t)
        if window is not None:
            Bext = Bext * window(x_lab)
        Bext = Bext * on_plate

        Bk = np.fft.rfft(Bext)
        # Perfect-screening asymptote for this instant, then relax toward it with each mode's
        # own diffusion time. C = coth(k g/2) is the iron either side raising the inductance.
        with np.errstate(divide='ignore', invalid='ignore'):
            C = np.where(k_all > 0, 1.0 / np.tanh(np.maximum(k_all, 1e-12) * G_EFF / 2), 1.0)
            psi_ss_k = np.where(k_all > 0,
                                -2.0 * Bk / (MU0 * np.maximum(k_all, 1e-12) * C), 0.0)
        psi_k = np.fft.rfft(psi)
        psi_k = psi_ss_k + (psi_k - psi_ss_k) * decay
        psi = np.fft.irfft(psi_k, n=nx)

        # THRUST IS K x B_TOTAL, NOT K x B_IMPOSED. The sheet's own reaction field cancels
        # much of the imposed one -- that is what screening means -- so using the imposed
        # field overstates thrust by whatever the screening factor is. The first run of this
        # file did exactly that and came out 4x above A31; band 1 caught it.
        B_self_k = -(MU0 * k_all * C / 2.0) * psi_k
        B_total = np.fft.irfft(Bk + B_self_k, n=nx)

        Ky = -np.gradient(psi, dx)
        Fx = float(np.mean(Ky[on_plate] * B_total[on_plate]) * PLATE_LEN * PLATE_W)
        hist_t.append(t)
        hist_F.append(Fx)
        hist_amp.append(float(np.abs(Ky[on_plate]).max()))
        t += dt
    return np.array(hist_t), np.array(hist_F), np.array(hist_amp)


if __name__ == '__main__':
    import plate_normal_force as pn
    import edge_effect

    EDGE = edge_effect.edge_factor(PLATE_W, TAU)
    A = PLATE_W * PLATE_LEN

    # A31's steady state at the same operating point, for band 1.
    fs = np.logspace(0, 3, 120)
    th = [pn.at_flux(BG, slip_freq=f, g=G_EFF, t=PLATE_T, tau=TAU)['thrust_Pa'] for f in fs]
    i = int(np.argmax(th))
    f_opt = float(fs[i])
    F_a31 = float(th[i]) * A * EDGE

    print("A32: the entry transient and segment handover\n")
    print(f"plate {PLATE_W*1e3:.0f} x {PLATE_LEN*1e3:.1f} x {PLATE_T*1e3:.0f} mm, "
          f"Bg {BG} T, pole pitch {TAU*1e3:.0f} mm, segments {SEG_LEN*1e3:.0f} mm")
    k0 = math.pi / TAU
    print(f"fundamental mode diffusion time tau_k = {tau_mode(k0)*1e3:.3f} ms "
          f"(this is the quantity the whole transient turns on)")
    print(f"A31 steady state at {f_opt:.0f} Hz slip: {F_a31:.1f} N\n")

    # ---- Bands 1 and 2: switch-on with the satellite at rest, then accelerating. ----
    t_h, F_h, amp_h = run(v=0.0, slip_freq=f_opt, duration=0.030)
    F_h = F_h * EDGE
    F_ss = float(np.mean(F_h[int(0.6 * len(F_h)):]))
    err1 = 100 * (F_ss - F_a31) / F_a31
    print(f"BAND 1  transient solver steady state {F_ss:.1f} N vs A31 {F_a31:.1f} N "
          f"-> {err1:+.1f} %   (band within 15 %)")

    target = 0.9 * F_ss
    idx = np.argmax(F_h >= target) if (F_h >= target).any() else len(F_h) - 1
    t_90 = float(t_h[idx])
    # Distance travelled while establishing, integrating the machine's own acceleration from
    # rest under the thrust actually available -- not at an assumed constant speed.
    m = 4.0 + A * PLATE_T * 2700
    v_i = x_i = 0.0
    for j in range(idx + 1):
        v_i += F_h[j] / m * (t_h[1] - t_h[0])
        x_i += v_i * (t_h[1] - t_h[0])
    print(f"BAND 2  thrust reaches 90 % after {t_90*1e3:.3f} ms = {x_i*1e3:.3f} mm "
          f"of travel   (band <= 65 mm)")

    # ---- Band 3: transverse force during establishment. ----
    # A31 gives the steady-state transverse force at 0.5 mm offset. The transverse force scales
    # with the square of the induced current, so the transient ratio is (amp/amp_ss)^2 and the
    # sign cannot reverse -- eddy forces on a non-magnetic sheet are repulsive throughout.
    amp_ss = float(np.mean(amp_h[int(0.6 * len(amp_h)):]))
    ratio_peak = float((amp_h.max() / amp_ss) ** 2)
    r_off = pn.at_flux(BG, offset=0.5e-3, slip_freq=f_opt, g=G_EFF, t=PLATE_T, tau=TAU)
    Fy_ss = r_off['normal_Pa'] * A * EDGE
    print(f"BAND 3  peak induced current during the transient is "
          f"{amp_h.max()/amp_ss:.4f}x steady state, so transverse force peaks at "
          f"{ratio_peak:.4f}x")
    print(f"        steady-state transverse force at 0.5 mm: {Fy_ss:.3f} N "
          f"({'restoring' if Fy_ss < 0 else 'DESTABILISING'})")

    # ---- Band 4: segment handover. ----
    v_seg = 12.0                        # mid-stroke speed
    def win(x_lab):
        return ((x_lab // SEG_LEN).astype(int) % 2 == 0).astype(float) * 0 + 1.0 * \
               (np.mod(x_lab, 2 * SEG_LEN) < SEG_LEN) + \
               1.0 * (np.mod(x_lab, 2 * SEG_LEN) >= SEG_LEN)
    def win_gap(x_lab, dead=0.010):
        """Adjacent segments energised, with a short unenergised gap at each joint."""
        return (np.mod(x_lab, SEG_LEN) > dead).astype(float)
    t_s, F_s, _ = run(v=v_seg, slip_freq=f_opt, duration=SEG_LEN / v_seg * 1.2,
                      window=win_gap)
    F_s = F_s * EDGE
    tail = F_s[int(0.15 * len(F_s)):]
    ripple = 100 * (tail.max() - tail.min()) / abs(tail.mean())
    print(f"BAND 4  segment handover with a 10 mm unenergised joint at {v_seg} m/s: "
          f"thrust {tail.mean():.1f} N, ripple {ripple:.1f} % pk-pk   (band <= 20 %)")

    # Band 4's failure has a direction, so it is swept -- SEPARATELY from the band, which
    # stands as declared at the 10 mm joint it was run on.
    print("\nDESIGN SWEEP on the segment joint -- separate from band 4, which stands")
    print(f"  {'dead zone':>10} {'thrust N':>9} {'ripple %':>9}")
    joint = []
    for dead in (0.010, 0.005, 0.002, 0.0):
        _, F_j, _ = run(v=v_seg, slip_freq=f_opt, duration=SEG_LEN / v_seg * 1.2,
                        window=(lambda d: (lambda xl: (np.mod(xl, SEG_LEN) > d).astype(float)))(dead))
        F_j = F_j * EDGE
        tl = F_j[int(0.15 * len(F_j)):]
        rp = 100 * (tl.max() - tl.min()) / abs(tl.mean())
        joint.append(dict(dead_mm=dead * 1e3, thrust_N=float(tl.mean()), ripple_pct=rp))
        print(f"  {dead*1e3:8.1f}mm {tl.mean():9.1f} {rp:9.1f}")
    seg_hz = [v_seg / SEG_LEN, 20.0 / SEG_LEN]
    print(f"  segment-crossing frequency sweeps 0 -> {seg_hz[1]:.1f} Hz across the stroke; "
          f"track modes are at 48 and 109 Hz")

    b = {
        '1': ('transient solver within 15 % of A31 steady state', f"{err1:+.1f} %",
              bool(abs(err1) <= 15.0)),
        '2': ('90 % thrust within 65 mm of travel', f"{x_i*1e3:.3f} mm", bool(x_i <= 0.065)),
        '3': ('transient transverse force does not exceed steady state or change sign',
              f"{ratio_peak:.4f}x, {'restoring' if Fy_ss < 0 else 'destabilising'}",
              bool(ratio_peak <= 1.0 + 1e-6 and Fy_ss < 0)),
        '4': ('segment handover ripple <= 20 % pk-pk', f"{ripple:.1f} %",
              bool(ripple <= 20.0)),
    }
    print("\nbands:")
    for kk in sorted(b):
        name, detail, ok = b[kk]
        print(f"  band {kk}: {'PASS' if ok else 'FAIL'}  {name}\n            {detail}")

    os.makedirs(RESULTS, exist_ok=True)
    json.dump(dict(Bg=BG, tau=TAU, g_eff=G_EFF, sigma_s=SIGMA_S, seg_len=SEG_LEN,
                   edge_factor=EDGE, f_opt_Hz=f_opt, tau_mode_ms=tau_mode(k0) * 1e3,
                   F_a31_N=F_a31, F_transient_ss_N=F_ss, band1_err_pct=err1,
                   t90_ms=t_90 * 1e3, x90_mm=x_i * 1e3,
                   transient_force_ratio=ratio_peak, Fy_05mm_N=Fy_ss,
                   handover_ripple_pct=ripple, joint_sweep=joint,
                   segment_crossing_Hz_at_20ms=20.0 / SEG_LEN,
                   bands=[dict(band=kk, name=b[kk][0], detail=b[kk][1], passed=b[kk][2])
                          for kk in sorted(b)]),
              open(os.path.join(RESULTS, 'entry_transient.json'), 'w'), indent=2)
    print("-> results/entry_transient.json")
