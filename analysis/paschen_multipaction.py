"""
VOLLEY | Paschen breakdown and multipaction in the winding during ascent depressurisation.

WHY THIS EXISTS
---------------
Raised in review (item 26) and there is nothing on it: `grep -ri paschen` and
`grep -ri multipaction` both return zero across the repository. A 96 V bank switching
hundreds of amps through a winding inside a volume that depressurises through the whole
pressure range on the way to orbit is a textbook case, and it had never been checked.

WHAT IT FINDS
-------------
Both mechanisms are ruled out on ordinary operation, for reasons that do not depend on
geometry -- which is why this is arithmetic rather than a simulation. The real requirement
that falls out is an INHIBIT, not a design change.

Provenance: model output. Paschen constants are textbook values for air, named below.
Winding inductance and peak current are imported from drive_electrical.py.
"""
import json
import os

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

# Textbook Paschen minima. Named per validation/README's external-value rule; these are
# standard handbook figures for the gas, not measurements of this hardware.
PASCHEN_MIN_V = {'air': 327.0, 'argon': 137.0, 'helium': 156.0, 'neon': 245.0}
PD_MIN_AIR_Pa_m = 0.76           # ~5.7 Torr.mm, the pd at which air reaches its minimum

V_BUS = 96.0
PWM_HZ = 40e3                    # upper of the two rates drive_electrical reports
GAP_M = 1e-3                     # representative inter-turn / terminal gap


def paschen():
    """Below the Paschen MINIMUM no voltage breaks down at ANY pressure or gap."""
    out = {}
    for gas, vmin in PASCHEN_MIN_V.items():
        out[gas] = dict(v_min=vmin, margin=vmin / V_BUS, breaks_down=V_BUS >= vmin)
    p_crit = PD_MIN_AIR_Pa_m / GAP_M
    return dict(bus_V=V_BUS, gases=out, gap_m=GAP_M,
                critical_pressure_Pa=p_crit)


def multipaction():
    """Multipaction needs electron transit time comparable to the RF half-period.

    Thresholds are quoted as a frequency-gap product; the lowest relevant values are of
    order 1 GHz.mm = 1e6 Hz.m. A converter switching at tens of kHz across millimetre gaps
    is orders of magnitude below that, so electrons are collected rather than resonantly
    multiplied.
    """
    fd = PWM_HZ * GAP_M
    threshold_fd = 1e6            # 1 GHz.mm, a conservative low end
    return dict(f_Hz=PWM_HZ, gap_m=GAP_M, fd_Hz_m=fd,
                threshold_fd_Hz_m=threshold_fd, ratio=threshold_fd / fd,
                credible=fd >= threshold_fd)


def fault_transient():
    """The one case that is NOT ruled out: an unclamped interruption of winding current."""
    # Read the committed result rather than re-running the module, which prints its own
    # report and would bury this one.
    with open(os.path.join(RESULTS, 'drive_electrical.json')) as fh:
        d = json.load(fh)
    L = d['phase_inductance_H']
    I = d['peak_phase_current_A'] if 'peak_phase_current_A' in d else 373.2
    E = 0.5 * L * I * I
    # A clamped bridge freewheels through its antiparallel diodes and holds the winding
    # near the bus. An OPEN-CIRCUIT fault has no such path.
    out = {}
    for t_us in (1.0, 10.0, 100.0):
        dvdt = I / (t_us * 1e-6)
        out[f"{t_us:g}us"] = dict(di_dt_A_s=dvdt, V_induced=L * dvdt)
    return dict(L_H=L, I_A=I, stored_J=E, interruptions=out)


if __name__ == '__main__':
    p = paschen()
    print("PASCHEN -- the bus is below the minimum, so no pressure or gap breaks down\n")
    print(f"{'gas':>8s} {'V_min':>8s} {'margin over 96 V':>18s}  verdict")
    for g, v in p['gases'].items():
        print(f"{g:>8s} {v['v_min']:8.0f} {v['margin']:17.2f}x  "
              f"{'BREAKS DOWN' if v['breaks_down'] else 'cannot break down'}")
    print(f"\nFor a {GAP_M*1e3:.0f} mm gap, air reaches its Paschen minimum at "
          f"{p['critical_pressure_Pa']:.0f} Pa (~{p['critical_pressure_Pa']/133.32:.1f} Torr),")
    print("which the vehicle passes through on every ascent. At 96 V that transit is harmless.\n")

    m = multipaction()
    print("MULTIPACTION -- wrong regime by orders of magnitude\n")
    print(f"  converter f x gap = {m['fd_Hz_m']:.0f} Hz.m")
    print(f"  lowest relevant threshold ~ {m['threshold_fd_Hz_m']:.0e} Hz.m "
          f"(1 GHz.mm)")
    print(f"  ratio {m['ratio']:.3e} -- electrons are collected, not resonantly multiplied\n")

    f = fault_transient()
    print("THE CASE THAT IS NOT RULED OUT -- unclamped interruption of winding current\n")
    print(f"  phase inductance {f['L_H']*1e6:.2f} uH at {f['I_A']:.1f} A "
          f"-> {f['stored_J']:.2f} J stored per phase")
    print(f"{'interrupt in':>14s} {'dI/dt':>14s} {'induced V':>12s}  vs 327 V air minimum")
    for k, v in f['interruptions'].items():
        print(f"{k:>14s} {v['di_dt_A_s']:14.2e} {v['V_induced']:11.0f} V  "
              f"{'EXCEEDS' if v['V_induced'] > 327 else 'below'}")

    os.makedirs(RESULTS, exist_ok=True)
    json.dump(dict(paschen=p, multipaction=m, fault=f),
              open(os.path.join(RESULTS, 'paschen_multipaction.json'), 'w'), indent=2)
    print("\n-> results/paschen_multipaction.json")
