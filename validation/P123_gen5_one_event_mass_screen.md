# P123 — one-event installed mass and fuel screen

**Status:** deterministic reference calculation; source and CI check published. This is a one-release algebra screen, not a twelve-release campaign, selected motor rating, launch-mass estimate, provider quotation or hardware validation.

## Review question

Does the propellant saved by an ideal finite-force Gen5 release offset the larger installed device in the existing matched reference case? P123 follows [the matched mission definition](../docs/MATCHED_MISSION_REFERENCE.md) and propagates the five [P122 geometry scenarios](P122_gen5_finite_force_sensitivity.md) through the same ideal preburn calculation. Run `python3 analysis/gen5_one_event_mass_screen.py --check`; plain invocation prints the full numerical result as JSON. The code uses Python's standard library.

## Controlled inputs and equation

All cases carry twelve 4 kg spacecraft on a 300 kg base host at the reference epoch. The host is assigned an illustrative 220 s specific impulse, 10 kg fixed fuel and a 2 kg reserve. The inertial target increment is **+16.029 m/s**, retained as the common mission comparison target; it is **not** a validated Gen5 release speed. Spring release is an assumed 2.5 m/s with 72 kg installed dispenser mass. Gen5 uses 126.562 kg modeled dry mass and P118's 12.448437 m/s **ideal work-to-speed conversion**, not a voltage-limited achievable rating.

For device mass `D`, fuel loaded `F`, one payload mass `p`, relative release conversion `v`, and preburn `b`, let `M0 = 300 + D + 12p + F` kg and `Ve = 220 × 9.80665` m/s. The root solve enforces

```text
b + [1 - p / (M0 exp(-b/Ve))] v = 16.029 m/s
propellant_used = M0 [1 - exp(-b/Ve)]
```

The bracketed term follows the reference model's ideal recoil bookkeeping. The fixed-fuel comparison holds `F = 10 kg`. A second, hypothetical *one-event resized-fuel* calculation solves the nested identity `F = 2 kg reserve + propellant_used(D, v, F)`. This accounts for fuel mass changing the preburn mass. The resized result cannot be used to size fuel for all twelve releases or to infer a provider launch-mass saving.

## Result

| Option | Fixed 10 kg load: one-event fuel used | Hypothetical resized one-event loaded fuel | Device + resized fuel |
|:--|--:|--:|--:|
| Spring class, 2.5 m/s | 2.692639 kg | 4.659253 kg | 76.659253 kg |
| Gen5 finite ideal, 12.448437 m/s | 0.826601 kg | 2.814686 kg | 129.376686 kg |

The fixed-fuel Gen5 case saves **1.866038 kg of propellant for this single ideal event**. The Gen5 device is **54.562 kg** heavier. With the one-event fuel load resized self-consistently, its *device plus required fuel* proxy is **52.717433 kg** higher than the spring reference. On this narrow proxy, a Gen5 device would need mass at or below **73.931985 kg** for parity at the P118 ideal speed. This is a conditional design threshold, not a feasible redesign claim or full mission break-even mass.

That proxy parity requires **52.630015 kg less Gen5 device dry mass**, about **41.6%** of the current 126.562 kg model, while preserving the same ideal release conversion. The five enclosure-related entries in the existing [mass ledger](../analysis/results/mass_properties.json)—skins 32.82, frames 8.20, radiator 2.59, bay boxes 1.87 and fasteners 4.55 kg—sum to **50.03 kg**. Even the physically impossible act of removing all five would miss this narrow parity target by about **2.60 kg** before the structure, radiator, interfaces or drive are replaced. This is an arithmetic lower-bound warning, not a proposed design. A feasible mass trade must involve multiple subsystems and rerun the force, thermal, stiffness, containment and host-interface models as their masses and shapes change.

There is also a **speed-independent lower bound** for this one-event reference. Even if an ideal release made the host preburn zero, loaded fuel could not fall below the common 2 kg reserve. Spring device plus resized fuel is 76.659253 kg, so any Gen5 device would need to weigh at most **74.659253 kg** to tie that proxy. The current 126.562 kg device misses even this physically generous limit by **51.902747 kg**. More thrust or better switching alone cannot erase this specific mass gap; the architecture or the mission value must change. This bound does not apply to a different target or complete campaign.

| P122 ideal geometry case | Ideal conversion | Gen5 one-event resized fuel | Gen5 minus spring device + fuel |
|:--|--:|--:|--:|
| Nominal 12 mm gap | 12.448438 m/s | 2.814686 kg | +52.717433 kg |
| Gap 14 mm | 11.613728 m/s | 2.997865 kg | +52.900612 kg |
| Gap 16 mm | 10.840040 m/s | 3.167715 kg | +53.070463 kg |
| Depth offset 5 mm | 12.202757 m/s | 2.868594 kg | +52.771341 kg |
| Depth offset 10 mm | 11.957672 m/s | 2.922377 kg | +52.825124 kg |

The tiny difference between P118's nominal 12.448437 m/s and P122's 12.448438 m/s is their separate numerical integrations. It has no physical meaning at this precision. All table speeds are ideal energy conversions and are **not** commanded or guaranteed releases. The five cases are selected perturbations, not a probability distribution.

![P123 device and one-event resized-fuel comparison](../figures/gen5_one_event_installed_burden.svg)

## Interpretation and closure

The one-event calculation exposes the installed-mass hurdle and gives a quantitative design target. It does **not** overturn the [twelve-release reference](../docs/MATCHED_MISSION_REFERENCE.md): neither option completes that sampled campaign, and the tested Gen5 case reaches only one accepted release under its short spacing target. Mission value must therefore be re-evaluated with one named payload, host and interface, a selected and derated drive, a complete feed and brake, all twelve sequential releases, reliability and disposal, and a common cost/mass accounting boundary.

A professional next design trade can vary cassette count, installed motor mass, actual speed range and target spacing together. It should present a Pareto set for dry mass, required fuel, energy, accepted deliveries and interface volume; every point must refer to one controlled CAD and circuit revision. The present 73.932 kg threshold is useful as a *screening constraint* for that trade, not proof that the constraint can be achieved.
