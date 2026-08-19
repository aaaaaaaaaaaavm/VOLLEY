"""
VOLLEY | Recoil and angular impulse at Gen6.

WHY THIS EXISTS
---------------
Two of the four NEEDS SOURCE rows in docs/KILL_CRITERIA.md, and E29, which is live: "Nothing
computes the shot's angular impulse about the host, and a reaction wheel saturates."

Gen5's recoil is 64.1 N.s per shot and KILL_CRITERIA calls it the healthiest item on the list.
Gen6 fires nearly double the impulse -- 4 kg at 29.009 m/s against 16.029 -- and has never been
computed, so a row marked healthy for Gen5 cannot be assumed healthy for Gen6.

Bands declared in validation/A52_gen6_recoil.md at HEAD, BEFORE this file existed.

Provenance: model output. Rigid host, all shots fired along one axis in one direction so
angular impulse accumulates, no attitude control during the shot, no host flexibility, no
propellant slosh. The CoM offset is a SWEEP and not a number, because no stage's mass
properties are public -- E5.
"""
import json
import os

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

M_PAY = 4.0
V_GEN5 = 16.029192806414976
V_GEN6 = 29.008                       # A44, with friction
V_TRIM = 0.3230                       # A48: the trim stage's authority
N = 12
WHEEL_N_M_S = 15.0                    # E29's stated wheel class
ISP_S = 220.0                         # hydrazine class
G0 = 9.80665
OFFSETS_M = (0.0, 0.01, 0.025, 0.05, 0.10, 0.25, 0.50, 1.0)


def linear_impulse(v, m=M_PAY):
    return m * v


def angular_impulse(v, offset_m, m=M_PAY):
    """Momentum times the moment arm from the host centre of mass."""
    return linear_impulse(v, m) * offset_m


def saturating_offset(v, n=N, wheel=WHEEL_N_M_S):
    """Offset at which n shots saturate the wheel. The interface requirement E29 asks for."""
    return wheel / (linear_impulse(v) * n)


def nulling_propellant_kg(total_impulse):
    return total_impulse / (G0 * ISP_S)


def main():
    i5, i6 = linear_impulse(V_GEN5), linear_impulse(V_GEN6)
    i_trim = linear_impulse(V_TRIM)
    camp5, camp6 = i5 * N, i6 * N

    print(f"{'':22s} {'per shot':>10s} {'campaign':>10s}")
    print(f"{'Gen5':22s} {i5:9.2f}  {camp5:9.1f}  N.s")
    print(f"{'Gen6, gas shot':22s} {i6:9.2f}  {camp6:9.1f}  N.s")
    print(f"{'Gen6, trim stage':22s} {i_trim:9.2f}  {i_trim*N:9.1f}  N.s   "
          f"({i_trim/i6*100:.2f} % of the shot)")
    print(f"{'Gen6, total':22s} {i6+i_trim:9.2f}  {(i6+i_trim)*N:9.1f}  N.s")
    print(f"\nGen6 is {i6/i5:.2f}x Gen5 per shot")

    prop6 = nulling_propellant_kg(camp6 + i_trim * N)
    prop5 = nulling_propellant_kg(camp5)
    print(f"propellant to null the campaign at Isp {ISP_S:.0f} s: "
          f"Gen5 {prop5:.3f} kg, Gen6 {prop6:.3f} kg")

    print(f"\nangular impulse about the host CoM, and wheel state after {N} shots:")
    print(f"{'offset mm':>10s} {'per shot':>12s} {'campaign':>12s} {'vs 15 N.m.s wheel':>20s}")
    rows = []
    for d in OFFSETS_M:
        a1 = angular_impulse(V_GEN6 + V_TRIM, d)
        ac = a1 * N
        rows.append(dict(offset_m=d, per_shot=a1, campaign=ac,
                         wheel_fraction=ac / WHEEL_N_M_S))
        state = "within" if ac <= WHEEL_N_M_S else f"SATURATES x{ac/WHEEL_N_M_S:.1f}"
        print(f"{d*1e3:10.0f} {a1:11.3f}  {ac:11.2f}  {state:>20s}")

    sat_off = saturating_offset(V_GEN6 + V_TRIM)
    sat_off_5 = saturating_offset(V_GEN5)
    print(f"\nthrust line must pass within {sat_off*1e3:.1f} mm of the host centre of mass "
          f"to keep a {WHEEL_N_M_S:.0f} N.m.s wheel unsaturated over {N} shots")
    print(f"  Gen5's equivalent requirement was {sat_off_5*1e3:.1f} mm")

    # band 1: does the method reproduce Gen5's published figure?
    bands = [
        ('1', "the method reproduces Gen5's 64.1 N.s within 1 %",
         f"{i5:.2f} N.s", abs(i5 - 64.1) / 64.1 <= 0.01),
        ('2', 'Gen6 per-shot and campaign linear recoil reported',
         f"{i6:.2f} N.s, {camp6:.1f} N.s campaign", True),
        ('3', 'angular impulse computed across an offset sweep',
         f"{len(rows)} offsets", len(rows) >= 5),
        ('4', f'the offset saturating a {WHEEL_N_M_S:.0f} N.m.s wheel in {N} shots is stated',
         f"{sat_off*1e3:.1f} mm", True),
        ('5', 'propellant to null the campaign <= 1.0 kg',
         f"{prop6:.3f} kg", prop6 <= 1.0),
        ('6', 'the result is stated as an alignment requirement in millimetres',
         f"{sat_off*1e3:.1f} mm", True),
        ('7', "the trim stage's contribution is included",
         f"{i_trim:.2f} N.s per shot, {i_trim/i6*100:.2f} % of the gas shot", True),
    ]
    print()
    for n, text, got, ok in bands:
        print(f"  {n}  {'PASS' if ok else 'FAIL'}  {text}: {got}")

    out = dict(analysis='A52', bands_declared_commit='HEAD~1',
               note='rigid host, all shots along one axis in one direction so angular impulse '
                    'accumulates, no attitude control during the shot, no host flexibility, no '
                    'propellant slosh. The CoM offset is a sweep, not a number, because no '
                    "stage's mass properties are public -- E5.",
               gen5_per_shot=i5, gen6_per_shot=i6, trim_per_shot=i_trim,
               gen5_campaign=camp5, gen6_campaign=camp6 + i_trim * N,
               ratio_gen6_gen5=i6 / i5,
               propellant_gen5_kg=prop5, propellant_gen6_kg=prop6,
               wheel_N_m_s=WHEEL_N_M_S, isp_s=ISP_S,
               offsets=rows, saturating_offset_mm=sat_off * 1e3,
               gen5_saturating_offset_mm=sat_off_5 * 1e3,
               bands=[dict(n=n, band=t, got=g, passed=bool(o)) for n, t, g, o in bands])
    with open(os.path.join(RESULTS, 'gen6_recoil.json'), 'w') as f:
        json.dump(out, f, indent=2)
        f.write('\n')


if __name__ == '__main__':
    main()
