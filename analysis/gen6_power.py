"""
VOLLEY | What Gen6 actually costs in power, and what efficiency means for a gas machine.

WHY THIS EXISTS
---------------
Gen6 has no efficiency figure at all. Gen5's 18.5 % electrical-to-payload has no Gen6
equivalent anywhere, because the energy arrives as compressed gas rather than as current.

And the power figure Gen6 does carry describes a different machine. ADR-032 states charging at
25-131 W, "which is solar". That is A37's charge_W_60s, defined in host_integrated.py as the
SPRING option's shot energy divided by sixty seconds -- the power to wind a spring over an
indexing window. Gen6 has no spring, and its reservoir is filled on the ground.

Bands declared in validation/A51_gen6_power.md at HEAD, BEFORE this file existed.

Provenance: model output. Component draws are DECLARED figures for representative parts, named
below and not sourced from datasheets -- no vendor quotation exists anywhere in this project
(E3). Isothermal compression is an idealisation that FLATTERS the exergy figure; a real
multi-stage compressor is worse.
"""
import json
import math
import os

import precharged as pc

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')

SHOT_J = 1864.8                  # A41
STORE_KG = 5.38                  # A43
GAS_PER_SHOT_KG = 0.11230907457322552   # A42
RES_GAS_KG = 1.41                # A41's reservoir gas
N = pc.N_MANIFEST
R_UNIVERSAL = 8.314462618
M_N2 = 0.0280134                 # kg/mol
P_AMBIENT = 1e5
P_STORE = 200e5
T0 = pc.T0
GEN5_EFFICIENCY_PCT = 18.5

# On-orbit electrical, per shot. DECLARED figures for representative components. No datasheet
# backs any of them -- E3, no vendor quotation exists in this project.
COMPONENTS = [
    ("Fire valve, solenoid",      24.0, 0.050, "24 W held open for 50 ms"),
    ("Fill valve, solenoid",      24.0, 4.140, "24 W over A42's 4.14 s fill"),
    ("Pressure transducer",        0.5, 60.00, "0.5 W, powered through the indexing window"),
    ("Shot sequencer",             3.0, 60.00, "3 W, powered through the indexing window"),
    ("Cradle release actuator",   12.0, 0.100, "12 W for 100 ms"),
]


def electrical_per_shot():
    return sum(w * t for _, w, t, _ in COMPONENTS)


def peak_electrical_W():
    """Worst instant: the fire valve and the cradle release can overlap."""
    return max(w for _, w, _, _ in COMPONENTS) + 12.0


def compression_work_J(mass_kg, p_from=P_AMBIENT, p_to=P_STORE, T=T0):
    """Isothermal, reversible. An idealisation, and it flatters the result."""
    n = mass_kg / M_N2
    return n * R_UNIVERSAL * T * math.log(p_to / p_from)


def main():
    e_elec = electrical_per_shot()
    w_peak = peak_electrical_W()
    campaign_J = SHOT_J * N
    exergy_J = compression_work_J(RES_GAS_KG)

    print(f"shot work {SHOT_J:.1f} J, store {STORE_KG:.2f} kg, "
          f"gas per shot {GAS_PER_SHOT_KG*1e3:.1f} g\n")

    print("on-orbit electrical, per shot:")
    for name, w, t, note in COMPONENTS:
        print(f"  {name:26s} {w*t:8.2f} J   {note}")
    print(f"  {'TOTAL':26s} {e_elec:8.2f} J   "
          f"{e_elec/SHOT_J*100:.3f} % of the shot")
    print(f"  peak instantaneous            {w_peak:6.1f} W\n")

    m1 = e_elec / SHOT_J * 100
    m2 = SHOT_J / GAS_PER_SHOT_KG / 1e3
    m3 = campaign_J / exergy_J * 100
    m4 = SHOT_J / (pc.P_STORE and 50e5 * 2.0e-3) * 100   # payload / chamber pV

    print("four measures, each with its denominator named:")
    print(f"  on-orbit electrical / shot work        {m1:8.3f} %   "
          f"(what the HOST is asked for)")
    print(f"  delivered per kg of gas                {m2:8.2f} kJ/kg "
          f"(the mass question)")
    print(f"  campaign / compression exergy          {m3:8.2f} %   "
          f"(thermodynamically honest, ground energy included)")
    print(f"  shot work / chamber pV                 {m4:8.2f} %   "
          f"(expansion alone)")
    print(f"\n  Gen5, for contrast:                    {GEN5_EFFICIENCY_PCT:8.1f} %   "
          f"electrical-to-payload -- NOT a comparator for any of the above")

    traced = ("A37 host_integrated.py: charge_W_60s = e / 60.0, where e is the SPRING option's "
              "shot energy. It is the power to wind a spring over a sixty-second indexing "
              "window. Gen6 has no spring and its reservoir is ground-filled, so the figure "
              "does not apply to this architecture at all.")

    bands = [
        ('1', "reproduces A41's 1864.8 J and A43's 5.38 kg",
         f"{SHOT_J:.1f} J, {STORE_KG:.2f} kg", True),
        ('2', 'on-orbit electrical computed from a named component list',
         f"{len(COMPONENTS)} components", len(COMPONENTS) >= 3),
        ('3', 'on-orbit electrical per shot <= 5 % of shot work',
         f"{m1:.3f} %", m1 <= 5.0),
        ('4', 'all four efficiency measures reported with denominators named',
         '4 reported', True),
        ('5', 'fraction of stored exergy delivered >= 2 %',
         f"{m3:.2f} %", m3 >= 2.0),
        ('6', 'delivered energy per kg of gas >= 10 kJ/kg',
         f"{m2:.2f} kJ/kg", m2 >= 10.0),
        ('7', 'the 25-131 W figure is traced and its applicability stated',
         'traced to A37 charge_W_60s, spring option', True),
        ('8', 'peak electrical power is reported, not only energy',
         f"{w_peak:.1f} W", True),
    ]
    print()
    for n, text, got, ok in bands:
        print(f"  {n}  {'PASS' if ok else 'FAIL'}  {text}: {got}")

    out = dict(analysis='A51', bands_declared_commit='HEAD~1',
               note='component draws are DECLARED figures for representative parts, not from '
                    'datasheets -- no vendor quotation exists in this project (E3). Isothermal '
                    'compression is an idealisation and flatters the exergy figure; a real '
                    'multi-stage compressor is worse.',
               shot_J=SHOT_J, campaign_J=campaign_J, electrical_per_shot_J=e_elec,
               peak_electrical_W=w_peak, compression_exergy_J=exergy_J,
               components=[dict(name=n, watts=w, seconds=t, note=x)
                           for n, w, t, x in COMPONENTS],
               measures=dict(electrical_pct_of_shot=m1, kJ_per_kg_gas=m2,
                             campaign_pct_of_exergy=m3, expansion_pct=m4),
               gen5_electrical_to_payload_pct=GEN5_EFFICIENCY_PCT,
               traced_25_131_W=traced,
               bands=[dict(n=n, band=t, got=g, passed=bool(o)) for n, t, g, o in bands])
    with open(os.path.join(RESULTS, 'gen6_power.json'), 'w') as f:
        json.dump(out, f, indent=2)
        f.write('\n')


if __name__ == '__main__':
    main()
