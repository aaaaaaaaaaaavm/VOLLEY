# VOLLEY

### Commanded electromagnetic CubeSat deployment

VOLLEY studies controlled deployment of passive CubeSats from a maneuvering orbital-transfer host. The design combines individually restrained storage cells, a guided feeder, a reusable launch carrier and electromagnetic acceleration. Its service objective is to deliver different commanded orbital states while accounting for the host manoeuvres, installed equipment and operating resources required.

[Project website](https://aaaaaaaaaaaavm.github.io/VOLLEY/) · [Selected feeder](validation/selected_feeder/README.md) · [CAD and STEP](cad/README.md) · [Numerical evidence](docs/CURRENT_NUMERICAL_EVIDENCE.md)

## The selected feeder

![FM08-R3 guided lead-screw four-cell feeder, rendered from native CAD](validation/selected_feeder/cad/figures/FM08_assembly.png)

*Blender technical render from the FM08-R3 native geometry. Colours distinguish payloads, structural parts and restraints; the view represents the academic design.*

**FM08-R3 uses guided lead-screw transfer from separate fixed cassettes to one indexed receiver.** Each stored satellite is restrained independently. A fixed spacer adapts a 1U cell to the common leading datum and remains inside the cassette. A guided pusher moves the payload through a capped transfer channel into the receiver, whose far-side stops are closed before feeding. Seating and receiver capture must be proved before the pusher returns. The storage barrier closes before launch is enabled.

| Design parameter | Declared reference |
|:--|:--|
| Initial manifest | Two 1U and two 3U public-envelope surrogates |
| Transfer direction | Sideways across the 100 mm spacecraft width |
| Local commanded stroke | 200 mm in 30 s |
| Common receiver indexing | 900 mm in 20 s |
| Transfer drive | Guided 10×2 mm lead-screw pusher; nominal 9:1 geared motor |
| Receiver drive | Toothed-belt indexer with nominal 59:1 gearbox; actual ratio 59.4 |
| Power basis | 24 V catalog reference drives; declared study assumptions |
| Receiver and cell custody | Independent storage restraints, capped transfer channel, far stops and receiver capture |

![Selected feeder sequence, rendered from native CAD states](validation/selected_feeder/cad/figures/FM08_sequence.png)

*Prescribed nominal states show storage, transfer, receiver capture and release preparation. These views illustrate the checked geometry; they do not measure release dynamics.*

[Editable FreeCAD and STEP](validation/selected_feeder/cad/README.md) · [Trade, calculations and interlocks](validation/selected_feeder/verification/REPORT.md) · [Reproduction and acceptance record](validation/selected_feeder/README.md)

### Why lead screw?

The seven-concept trade uses safety 35%, packaging/mass 25%, positioning 20%, cycle/power 10% and manufacture 10%. The top three judgment scores are **7.30/10 lead screw**, **7.10 rack-and-pawl**, and **6.90 spring/two-gate**. The small margin and sensitivity to priorities are retained. Guided transfer, contained handoff and a direct sizing path support the chosen architecture; rack-and-pawl remains the runner-up. These scores describe design judgments and do not estimate reliability.

[Full ranking and common-input comparison](validation/selected_feeder/verification/REPORT.md) · [Alternative concepts and earlier CAD](https://github.com/aaaaaaaaaaaavm/VOLLEY-lab#readme)

## Gen5: evaluated computational baseline

Gen5 is the fixed twelve-3U electromagnetic configuration evaluated in the academic study. Gen6 contains the separately versioned feeder and capacity development.

| Gen5 quantity | Result and interpretation |
|:--|:--|
| Ideal finite-geometry release screen | 12.448 m/s under assumed phase/electrical conditions |
| Historical periodic-force model | 16.029 m/s; retained for model comparison |
| Historical modeled dry mass | 126.562 kg, or 10.547 kg per 3U slot |
| Evaluated side-fed packaging | 11 mm width shortfall in the original reference |
| Performance status | Computational results; no component-rated or measured release setting |

[Immutable Gen5 technical record](docs/GEN5_TECHNICAL_BASELINE.json) · [Computational engineering report](reports/GEN5_COMPUTATIONAL_REVIEW.pdf) · [Finite-force cross-check](validation/P121_gen5_finite_force_surface3d.md)

## Commanded orbital delivery

![Finite-force host-control schedules and resource comparison](validation/finite_burn_review/figures/force_fuel_trade.png)

The declared service reference is a generic maneuvering OTV in approximately 500 km sun-synchronous orbit. Four satellites are released within one orbital period; full position/velocity targets are compared at one common epoch 24 hours after the final release. The host-assisted spring alternative uses the same mission boundary.

The earlier finite-force twelve-release 35%/35% study gives 33.83 N peak/23.12 kg propellant for its spring input and 18.00 N/6.12 kg for its imposed VOLLEY input. Both reach the constructed targets under a 100 N/30 kg allowance, while the assumed device-mass premium exceeds the propellant saving. Those inputs do not rate a physical launcher.

[Native Orekit and finite-force evidence](validation/finite_burn_review/README.md) · [Four/twelve-payload integration and updated resource assessment](validation/system_feasibility_closure/README.md) · [Market and customer fit](MARKET_AND_CUSTOMER_FIT.md)

## Methods and evidence

The repository contains editable FreeCAD geometry, STEP exchanges, electromagnetic and structural calculations, native solver inputs/outputs, orbital propagation, source-linked figures and executable checks. The selected feeder uses nominal geometry, prescribed kinematics, analytical load/tolerance screens and a deterministic fault/interlock specification.

No physical prototype, measured release precision or flight qualification is claimed. The historical Chrono transfer model remains numerically sensitive and supplies no accepted peak-contact-load or precision rating. Catalog components are ambient reference choices; spacecraft compatibility and environmental qualification require later hardware and provider work.

[Current numerical evidence](docs/CURRENT_NUMERICAL_EVIDENCE.md) · [Literature](docs/LITERATURE.md) · [Geometry and numerical history](validation/README.md)

## Reproduce the work

Each captured study includes its source, inputs, software versions, raw results and hash manifest. Native CAD reconstruction uses FreeCAD; STEP allows neutral geometry exchange. Blender views are labeled as renders. Run `python tools/prepublish_gate.py --all` for publication consistency, then the study-specific commands for engineering reproduction.

## Project editions

[Thesis: college report and presentation](https://github.com/aaaaaaaaaaaavm/VOLLEY-thesis) · [Paper: IEEE-formatted manuscript and reproduction](https://github.com/aaaaaaaaaaaavm/VOLLEY-paper) · [Labs: alternatives and experiments](https://github.com/aaaaaaaaaaaavm/VOLLEY-lab)

Each edition includes its own relevant evidence. The manuscript is unsubmitted and its IEEE venue remains unselected. The 1 km/s-class and lunar investigations are separate feasibility studies, with their assumptions and negative findings retained.
