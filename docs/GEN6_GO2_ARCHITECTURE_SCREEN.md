# Gen6 Go 2: G1 architecture and first-article screen

**Decision record, 12 October 2026. G1 open; no build released.** [Go 1 P130](../validation/P130_gen6_matched_campaign.md) showed that a competent spring-plus-host policy can achieve the same four surrogate target states. Under its assumed hardware masses, VOLLEY does not win a device-plus-fuel comparison. Go 2 therefore asks whether a controlled 4 kg dummy article can expose the actual drive and release risks without claiming a finished service system.

## Candidate set and decision

Both layouts retain an ordinary, passive 3U spacecraft envelope. A reusable carrier pushes it along a common guide and is captured while the payload continues. A 1U adapter and four-slot feeder are **future interfaces**, not items in this first-article CAD. The first article's 3–6 m/s study band is a proposed measurement range; P130's 7 and 9 m/s mission commands remain unproven.

| Criterion | A: captured permanent-magnet carrier | B: captured conductive-plate carrier |
|:--|:--|:--|
| Reason to retain | Closest to the Gen5 permanent-magnet force-model lineage, allowing direct falsification and new short-stroke measurements. | Removes permanent magnets from the moving carrier; tests a distinct induction topology already explored historically in VOLLEY-lab PII-19. |
| Principal risk | Magnetic exposure, mover capture, finite-array handover, peak source current and installed magnet/drive mass. | Slip-dependent force, plate heating, reactive power, normal force, and historical 30.1% handover ripple in a different design. |
| Current geometric evidence | Editable FreeCAD assembly, STEP read-back, five nominal stroke stations and partial proxy mass. | The same, using a conductive-plate proxy. |
| Actual drive, contact, brake and electrical closure | **Open** | **Open** |
| G1 disposition | **Analysis lead only; not selected for construction** | **Live challenger; not rejected** |

This order reflects the user's intention to make Gen6 the first practical prototype while preserving the negative Gen5 academic result. It does not carry Gen5's 12.448 m/s ideal force screen into Gen6. It does not claim novel electromagnetic separation; comparable work is prior art.

## Findings from controlled CAD and mechanics

- [Native FreeCAD assemblies, STEP exports and STEP-derived views](../cad/gen6_first_article/README.md) show a 1.3 m powered travel, 200 mm brake-space envelope, passive 3U surrogate and 110 mm guide corridor. Five sampled nominal positions have zero exact-solid intersection. The guide's simple 5 mm side gap clears an assumed 0.5° yaw plus 1.5 mm linear stack by just 0.53 mm, and fails the 0.7° case. Contact, full swept solid, deformation and tolerance distribution are open.
- [P131](../validation/P131_gen6_go2_article_bounds.md) gives an ideal 6 m/s total moving-energy floor around 82 J and mean drive force around 63 N, before friction or electrical loss. The captured carrier needs about 10 J of stopping work and 49–51 N ideal mean force over 200 mm. Peak force, brake thermal cycling and shock are unknown.
- The CAD-derived **partial** frame/guide/carrier material proxy is 9.926 kg (A) or 9.945 kg (B). The narrow P130 device-plus-consumed-fuel parity ceiling is 19.282 kg, leaving about 9.35 kg for every unmodeled installed item. This is a necessary budget **under surrogate inputs**, not mass closure or an approved flight allocation.
- The [FreeCAD mass/CG/inertia ledger](../cad/gen6_first_article/release/Gen6_G1_Partial_Mass_CG_Inertia.json) places A's partial dry material center at x=0.864 m and its modeled pitch inertia at 2.637 kg·m². Adding the assigned 4 kg uniform dummy shifts the combined center from x=0.713 m at start to x=1.138 m at the end of the powered stroke. These are geometry-proxy properties, **not** an installed host load case; they show that moving payload position materially changes the host moment budget.
- The [P132 source and instrument screen](../validation/P132_gen6_go2_power_instrument_screen.md) converts that ideal 82 J moving-energy floor to **818 J bus energy at an assumed 10% end-to-end efficiency** for a 6 m/s shot. Its ideal 96-to-72 V capacitor floor is 0.406 F; an ideal constant-acceleration end-stroke power floor is 3.77 kW. These are sizing hypotheses, not a rated motor, bank or instrument.

## Next engineering packages, in decision order

| Package | Concrete release required | Reject or redesign if |
|:--|:--|:--|
| G1-1 Interface and contact | Payload rail/dummy dimensions and load limits, positive launch restraint, pusher compliance/contact law, release lip and tip-off budget; provider-specific constraints where available. | The guide damages or changes an ordinary passive CubeSat, or actual yaw/contact uncertainty exceeds delivered-state tolerance. |
| G1-2 Installed mass and sourcing | Numbered parts and supplier data for frame, guides, magnets/plate, primary, inverter, source, wiring, sensors, brake, restraint, fasteners, thermal and host mounting; CAD volume and measured/vendor mass reconciliation. | The complete system cannot justify its mass premium for a customer job. |
| G2-1 Drive/circuit/thermal | Independent 3-D force calculation, finite-array handover, coupled current/voltage/position, hot resistance, switch/storage ratings, force/speed envelope, numerical convergence and uncertainty. | A 4 kg payload cannot achieve the predeclared test band inside source/thermal limits. |
| G2-2 Mechanism and host loads | Captive carrier stop and failed-stop containment, repeated brake heat, structural/launch/EMI, jam, abort/reset, host recoil and field exposure. | Any credible failure ejects the carrier or exposes the payload/host beyond their limits. |
| G3 Instrumented article | Safe contained build, calibrated current/voltage/position/speed-vector/contact/temperature sensing, repeated shots and preregistered model bands. | Measurements miss the bands; stop and redesign before a mixed-size feeder. |

**Resource decision:** no prototype purchase or fabrication specification is released. The native CAD and numeric bounds make the next design work inspectable, but their missing hardware is too consequential to call either a complete Gen6 product or a passed G1 gate. The Gen5 thesis/paper PDF remains a separate computational study.
