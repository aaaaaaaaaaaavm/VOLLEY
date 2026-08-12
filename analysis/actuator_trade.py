"""
VOLLEY | Why a linear motor, and not a screw, a rack, or a spring.

WHY THIS EXISTS
---------------
Raised in review as item 18. The repository has no recorded answer: `grep -ri "lead screw"`
and `grep -ri "rack and pinion"` both return zero, and DECISION_LOG records the choice of eddy
brake and ironless stator but never the choice of LINEAR MOTOR over every other way of pushing
a satellite. A reviewer is entitled to ask why the hardest option was taken.

Criteria declared in validation/A27_actuator_trade.md at 9857b3c, BEFORE this file existed.

Provenance: model output. Component class limits (ball-screw DN, gear pitch-line velocity,
spring energy density) are published handbook ranges, named at each use, not measurements.
"""
import json
import math
import os

import motor_model as mm

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

G = 9.81
M_SLED, M_PAY = mm.M_SLED, 4.0
M_TOT = M_SLED + M_PAY
L = mm.ACCEL_ZONE
V = 16.388
G_CAP = 25.0
E_PAY = 0.5 * M_PAY * V ** 2          # 537 J to the payload
E_TOT = 0.5 * M_TOT * V ** 2          # everything the actuator must supply

# Published class limits, named per the run sheet's requirement.
DN_LIMIT = 150e3          # mm.rpm, conventional ball-screw DN ceiling
CRIT_SPEED_K = 1.2e8      # mm.rpm coefficient, fixed-fixed screw whirling
GEAR_PLV_LIMIT = 10.0     # m/s, upper end of high-speed rack practice
SPRING_ENERGY_DENSITY = 300.0   # J/kg usable, upper end for spring steel


def lsm():
    Kt, ripple = mm.thrust_constant()
    F = 0.9 * Kt * mm.K_RATED
    a = F / M_TOT
    return dict(name="Linear synchronous motor (incumbent)",
                F_N=F, a_g=a / G, v_max=V, contact=False,
                control="continuous", stored_at_rest_J=0.0,
                limit_name="sheet current and bank ESR",
                limit_value=None, limit_ok=True)


def ball_screw(lead_mm=20.0, d_mm=25.0, length_mm=1500.0):
    """Limiting quantity is rotational speed, twice over: DN and whirling."""
    rpm = V / (lead_mm / 1000.0) * 60.0
    dn = d_mm * rpm
    n_crit = CRIT_SPEED_K * d_mm / (length_mm ** 2)
    F = M_TOT * (V ** 2 / (2 * L))
    return dict(name=f"Ball screw, {lead_mm:g} mm lead, D{d_mm:g}, {length_mm:g} mm",
                rpm=rpm, DN=dn, DN_limit=DN_LIMIT, DN_over=dn / DN_LIMIT,
                n_crit_rpm=n_crit, crit_over=rpm / n_crit,
                F_N=F, a_g=(V ** 2 / (2 * L)) / G, contact=True,
                control="continuous", stored_at_rest_J=0.0,
                limit_name="DN number and whirling critical speed",
                limit_ok=(dn <= DN_LIMIT and rpm <= n_crit))


def rack_pinion(pitch_d_mm=100.0):
    rpm = V / (math.pi * pitch_d_mm / 1000.0) * 60.0
    plv = V                              # pitch-line velocity IS the linear speed
    F = M_TOT * (V ** 2 / (2 * L))
    torque = F * (pitch_d_mm / 2000.0)
    return dict(name=f"Rack and pinion, D{pitch_d_mm:g} pinion",
                rpm=rpm, pitch_line_v=plv, plv_limit=GEAR_PLV_LIMIT,
                plv_over=plv / GEAR_PLV_LIMIT, torque_Nm=torque,
                F_N=F, a_g=(V ** 2 / (2 * L)) / G, contact=True,
                control="continuous", stored_at_rest_J=0.0,
                limit_name="pitch-line velocity",
                limit_ok=plv <= GEAR_PLV_LIMIT)


def spring(stages=1):
    """A linear spring's force peaks at release and falls to zero -- peak g is what binds.

    Only the PAYLOAD needs accelerating if the spring pushes the satellite directly, which is
    the honest comparison: a spring architecture has no sled to carry.
    """
    E = 0.5 * M_PAY * V ** 2
    F_mean = E / L
    F_peak = 2.0 * F_mean                # linear spring, force falls linearly to zero
    a_peak = F_peak / M_PAY
    mass = E / SPRING_ENERGY_DENSITY
    return dict(name=f"Staged mechanical spring, {stages} stage(s)",
                E_J=E, F_mean_N=F_mean, F_peak_N=F_peak, a_g=a_peak / G,
                spring_mass_kg=mass, contact=False,
                control=("discrete, %d level(s)" % stages),
                stored_at_rest_J=E,
                limit_name="peak acceleration at release",
                limit_ok=a_peak / G <= G_CAP)


def screen(c):
    """C1..C5 exactly as declared."""
    c1 = c.get('limit_ok', True)
    c2 = c['a_g'] <= G_CAP
    ctrl = c['control']
    c3 = 'PASS' if ctrl == 'continuous' else ('PARTIAL' if 'discrete' in ctrl else 'FAIL')
    c4 = not c['contact']
    c5 = c['stored_at_rest_J'] == 0.0
    return dict(C1=c1, C2=c2, C3=c3, C4=c4, C5=c5)


if __name__ == '__main__':
    cands = [lsm(), ball_screw(), rack_pinion(), spring(1), spring(4)]
    print(f"duty: {M_TOT:.3f} kg to {V} m/s over {L} m, <= {G_CAP:g} g, "
          f"{E_TOT:.0f} J total, {E_PAY:.0f} J to the payload\n")
    print(f"{'candidate':46s} {'C1':>4s} {'C2':>4s} {'C3':>8s} {'C4':>4s} {'C5':>4s}  peak g")
    out = []
    for c in cands:
        s = screen(c)
        out.append(dict(candidate=c, screen=s))
        f = lambda b: ('ok' if b else 'FAIL')
        print(f"{c['name']:46s} {f(s['C1']):>4s} {f(s['C2']):>4s} {s['C3']:>8s} "
              f"{f(s['C4']):>4s} {f(s['C5']):>4s}  {c['a_g']:5.1f}")

    print("\nwhy each non-incumbent fails:")
    b = cands[1]
    print(f"  ball screw : {b['rpm']:.0f} rpm needed. DN = {b['DN']:.3e} against a "
          f"{DN_LIMIT:.0e} limit ({b['DN_over']:.1f}x over),")
    print(f"               and whirling critical speed is {b['n_crit_rpm']:.0f} rpm "
          f"({b['crit_over']:.0f}x over).")
    r = cands[2]
    print(f"  rack       : pitch-line velocity IS {r['pitch_line_v']:.1f} m/s against ~"
          f"{GEAR_PLV_LIMIT:.0f} m/s practice ({r['plv_over']:.2f}x),")
    print(f"               {r['torque_Nm']:.1f} N.m at {r['rpm']:.0f} rpm, and it is a "
          f"CONTACT drive at full speed in vacuum (E21).")
    s1 = cands[3]
    print(f"  spring     : {s1['E_J']:.0f} J, peak {s1['F_peak_N']:.0f} N -> "
          f"{s1['a_g']:.1f} g, about {s1['spring_mass_kg']:.1f} kg of spring steel.")
    print(f"               Kinematically FINE. It fails only on commandability, and it "
          f"stores {s1['stored_at_rest_J']:.0f} J at rest.")

    os.makedirs(RESULTS, exist_ok=True)
    json.dump(dict(duty=dict(m_total=M_TOT, v=V, L=L, g_cap=G_CAP,
                             E_total_J=E_TOT, E_payload_J=E_PAY),
                   results=out), open(os.path.join(RESULTS, 'actuator_trade.json'), 'w'),
              indent=2, default=str)
    print("\n-> results/actuator_trade.json")
