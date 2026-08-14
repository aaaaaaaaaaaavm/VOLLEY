# Validation plan

Independent cross-checks of the claims in `analysis/`. **Nineteen of the twenty-one below have run.**
**Two of them failed**, two are partial, one returned three rows that could not be evaluated at
all, and one found a published number 37 % high.

## Why it exists

This directory was written when `PROVENANCE.md` could point at only two cross-checks — the
Halbach field (analytic vs magpylib) and orbital decay (orbit-averaged vs Cowell RK4) — both
internal, and the field one analytic-against-analytic, so not confirmation by a different
physical method (`OPEN_PROBLEMS.md` E2).

**That has changed, and not uniformly in the project's favour.** A1 put a meshed PDE solve
against K<sub>t</sub> and agreed to 0.03 % after correcting shared quadrature. A4 put CalculiX against the chassis and it passed.
A12 put two independent numerical methods against the array attraction and found the published
value **37 % high**. And **A5 failed**: an independent propagator falsified an invariance claim
that was in the paper's own abstract.

**What has still never happened is a measurement.** Every row below is one model against
another model (E4). Each analysis closes a specific named item.

| # | Analysis | Tool | Closes | Status |
|---|---|---|---|---|
| A1 | Airgap field, 2-D magnetostatic | scikit-fem + gmsh (FEMM substituted) | E1 (2-D half), E2 (partly) | **RUN 2026-07-29**, verdict **PARTIAL**: K<sub>t</sub> agrees to 0.03 % after correcting shared quadrature, two bands missed with causes (P20, P21) |
| A4 | Sled chassis structural | CalculiX ccx 2.21 | **P5, P8** | **RUN 2026-07-28**: as-drawn plate passes all three bands |
| A5 | Orbital lifetime and seeding | GMAT R2022a | E6, hardens x1.80 | **RUN**, verdict **FAIL** on invariance. See [`../docs/RESULTS.md`](../docs/RESULTS.md) |
| A9 | Decay rate against flown CubeSats (TLE history) | Space-Track + numpy | **E6, against reality rather than another model** | **NOT RUN**, blocked by network policy here and re-tested 2026-07-31. **Candidate objects now shortlisted** in the sheet, so this is an afternoon elsewhere |
| A6 | Conjunction probability | scipy 2-D Pc (CARA substituted) | P1 — **not closed** | **CORRECTED 2026-08-03**: fixed-shape claim retracted; current slab bound 4.4e-5, two of five bands, three **VOID**, P1 open |
| A7 | Separation and tip-off | Project Chrono | E7-adjacent | **still specified, not run.** **A7-R RUN 2026-08-05** instead: Chrono is unavailable and the release mechanism is undefined, so the tolerance was computed rather than the rate — the full push may act unbalanced for only **50.7 µs** before the 2 °/s band breaks |
| A8 | Pulse-power chain | ngspice / PySpice | E17 | **RERUN 2026-08-05** as A8-R2 at the corrected point: six of six bands, exit velocity agrees to 0.016 % |
| A10 | Shot against a realistic bank ESR | `motor_model.shot()` | nothing; **opened P26** | **RERUN 2026-08-03**: hard ceiling 68 mohm, five of six bands, one VOID |
| A11 | Regenerative recovery of sled energy | `motor_model.regen_brake()` | nothing; asks what R5 did not | **RERUN 2026-08-03**: 291.4 J recovered, eight of eight bands |
| A12 | Inter-array attraction, two numerical methods | magpylib + surface Maxwell stress | **P17** | **CORRECTED 2026-08-03**: extended stress plane 2680.0 N vs 2686.6 N volume force; five of five bands |
| A13 | Indexing and sled-return attitude disturbance | momentum bookkeeping | **E24** | **CORRECTED 2026-08-03**: transient-rate rows 3/4 FAIL, row 7 VOID; ideal residual rate is zero and the cadence conclusion is superseded |
| A14 | EMI scoping: payload coupling and comms | `drive_electrical` + magpylib | advances **E12**; **opened P34** | **RUN 2026-08-05**, verdict **PARTIAL**: six of eight bands, band 4 **FAIL** at 611x, band 5 VOID. The dominant term is the static magnet field, not the drive |
| A16 | Gen4 finite-stator thrust vs sled station | magpylib | **E27** | **RUN 2026-08-05**: full-overlap thrust reproduces `F_cmd` to 0.000 %; Gen4 reaches **13.390 m/s, 81.7 % of Phase I**, an upper bound |
| A17 | Ripple chirp through the track modes | scipy SDOF | **E23**; **opened P36** | **RUN 2026-08-05**, verdict **FAIL**: 8.18x amplification at the fundamental crossing of the 109 Hz mode, and Q is not the variable that saves it |
| A18 | Brake, magnet eddy, fin transient, launch restraint, standoff | numpy + Miles | **E20, E19, E26, E22**, and E10's analysis half; **opened P37** | **RUN 2026-08-06**: E19/E26/E22 pass, E20 passes only for a 0.4-0.5 T pole field, **E10 FAILS at every Q** |
| A20 | Reachable orbit envelope vs host Δv budget | numpy + `astro.py` | nothing; quantifies **ADR-024**, advances PII-6 | **RUN 2026-08-10**, verdict **band 1 FAIL**: the band named a two-burn Hohmann and its limit was computed for one burn. Band 3 caught a sign bug in the script. Host supplies 56 % of the altitude extent at 100 m/s |
| A21 | VOLLEY against springs, drag and cold gas, identical axes | numpy + `astro.py` | nothing; **replaces the headline ratio** | **RUN 2026-08-10**: seven of seven. **7.52×** the lifetime extension of the fastest spring against 6.56× on velocity; mass parity at 1.062; cold gas wins at 3U by 7.5×, declared as a loss in advance. **RE-RUN 2026-08-14** at the corrected operating point (**P53**): still seven of seven, at **7.33×**, **6.41×**, parity 1.062 and **8.3×** |
| A22 | Retention gate resize against the random-vibration case | numpy + `phase1_closeout.e10` | **P37**, E10's analysis half | **RUN 2026-08-10**: six of six. 2 × D6 → **2 × D9** takes the margin at Q = 30 from **−0.36 to +0.45** and keeps it positive across Q = 10–30, for **11 g** |
| A23 | Tip-off at release, modelled rather than bounded | numpy rigid body | advances **E7**; **opened P41** | **RUN 2026-08-10**: release is comfortable — it happens 12.2 ms into coast at zero force. **The payload arrives in its cradle at 36–231 °/s**, 18–115× the band, and nothing had modelled it |
| A24 | The payload ladder as a fixed-cell design, not a volume ratio | numpy + `payload_family.py` | ADR-025; **opened P44** | **RUN 2026-08-10**: five of six, **band 6 FAIL**. **1U no longer closes kill criterion 1** (36/load, 2.125 kg, not 40/1.913); **ThinSat and 12U do not fit at all** — the 166 mm cassette width is a constraint written nowhere else. Band 6 missed at 0.508 % against 0.5 %: 720 ChipSats need **7.19 kg of shim hardware for 3.6 kg of payload** |
| A25 | A flywheel energy store against P26 | numpy + `motor_model.py` | targets **P26**; **opened P45** | **RUN 2026-08-10**: five of six, **band 4 FAIL** by 1.1 kg. **Band 6 — the point of the exercise — passes decisively: 35 mΩ against A10's 68 mΩ ceiling, 66 kW deliverable against 32.5 required.** Needs no architecture change. Mass parity, not saving; the miss turns on one unsourced machine specific-mass figure |
| **A2** | The 3-D field, and the depth assumption inside K<sub>t</sub> | numpy + magpylib | closes **E1**'s 3-D half; **opened P46** | **RUN 2026-08-10**: four of four run, **band 4 (getdp FEM) NOT RUN so E2 stays open**. The field was never 2-D — the *thrust integral* was. Resolving depth costs **4.42 % of K<sub>t</sub>** (10.5386 → 10.5386), **v_exit 16.029 → 16.029**. **Baseline not changed**; computed and held. Band 1 caught a 57 % normalisation bug in the analysis; **band 3 was badly chosen** and measures numerical cancellation at 10⁻²⁰ T |
| A27 | Why a linear motor, and not a screw, rack or spring | numpy + `motor_model.py` | answers review item 18 | **RUN 2026-08-10**: screw **disqualified by kinematics** (49,164 rpm; DN 8.2× over, critical speed 37× under); rack fails on **vacuum contact at 16.0 m/s**; **a ~1.8 kg spring works at 21.1 g** and fails only on commandability. **The motor is chosen for commandability, not performance** |

> **Two entries above are document reviews rather than banded runs**, and are filed in `docs/`
> because they declare no band: [`ICD_COMPLIANCE.md`](../docs/ICD_COMPLIANCE.md) (the launch
> interface permits 16.029 m/s; three worse requirements found) and
> [`FMEA.md`](../docs/FMEA.md) (**nine of thirteen elements forfeit the manifest**; the design
> needs **r ≥ 0.99326** per element per cycle to beat a spring). Both came out of the external
> review recorded in [`REVIEW_RESPONSES.md`](../docs/REVIEW_RESPONSES.md).
| A19 | Sensitivity ranking of nine assumed inputs | numpy + the real pipeline | nothing; **ranks** the assumptions behind P29, P28, `STRUCTURAL_GAP` | **RUN 2026-08-10**, verdict **band 1 FAIL**: net efficiency has two different leaders depending on the metric, so both rankings are published. `v_exit` does not respond to bank ESR at all — nil, then total |

A10 and A11 are cross-checks of the model against its own physics rather than against an
external tool, which is a weaker class of check and is labelled as one. They are here because each
asks a question no external solver was going to be pointed at: whether the bank can source the
shot at all, and whether the sled's energy has to be thrown away. **A12 is stronger than both** —
its two methods share only the block model of the magnets — and **A6 is weaker than any of them**,
since both its geometry and its covariance come from inside this project.

> **This table was wrong about A1 for a day**, from 2026-07-30 to 2026-07-31: it said "specified,
> not run" while `OPEN_PROBLEMS.md` E1 and `docs/ROADMAP.md` both recorded A1 as run on
> 2026-07-29. The cause is worth keeping, because it is the reason A1 and A5 now carry their
> results inline. **Both run sheets were pure specifications**, with their outcomes living only in
> `OPEN_PROBLEMS.md`, `CHANGELOG.md` and `docs/RESULTS.md`, so a search of `validation/` for
> completed runs found A4, A8 and A10 and missed them. **A run sheet that does not record its own
> result is not a record.** A1 and A5 were written up on 2026-07-31 in the format A4, A8, A10 and
> A11 already used.

A2 (3-D field, end effects) and A3 are not specified here; A1 closes only the 2-D half of
E1, and the 3-D end effects still need a 3-D solver.

## The one rule that makes these tests rather than exercises

**The acceptance band is declared before the analysis runs.** Every run sheet in this
directory states its band up front, and each band is traceable to a current value in
`analysis/results/*.json`. A cross-check whose target is chosen after seeing the answer
proves nothing.

This is not hypothetical here. `docs/FEMM_Run_Sheet.md` was written against ⟨B⟩ ≈ 0.62 T
across the winding gap; the winding-resolved model now computes **0.552 T**, so that
sheet can no longer function as a test and is marked superseded. The replacement sheet
(`analysis/femm/FEMM_RUN_SHEET.md`) had the same problem in its stray-field targets,
they predated the P3 correction, and was fixed on 2026-07-27.

When a band is missed, the outcome is a new P-item, not a quietly widened band.

**A field band must name which field, at which plane, as which quantity.** Added 2026-08-10 from
**P20**, and it is aimed at **A2** in particular. A1's array-surface band was declared against
`analytic_B0_surface_T` = 0.7714 T, the fundamental amplitude of a **single** array's ideal wave
at its own surface. Any measurement at that plane in a **double-sided** machine includes the
opposing array, worth `B0·exp(-k·GAP)` = 0.160 T there, so the correct double-sided reference is
**0.9317 T** — and the FEM's fundamental is 0.9312 T, a ratio of 0.9994. **The row failed as
declared and the model was right.** A raw peak at that plane reads 1.4641 T and is a third
quantity again, mesh-dependent, because the plane sits on the magnet face where block-corner
harmonics dominate and the field is formally singular at the corners.

So a band at a magnet surface needs **two references named, not one**: single-sided or
double-sided, and fundamental or raw peak. A1's sheet is left exactly as written — a band is
never edited after its run — and this is where the correction lives instead, so the next sheet
meets it without having to know to search the register for it.

**And when a band cites an external document, record which document, which revision, and whether
a tighter comparator exists in the same family.** Added 2026-07-31 after **P30**: A7's tip-off
band was set at 5 °/s from the external NRCSD-E, whose publisher calls that figure provisional,
while the internal NRCSD that has actually flown specifies 2 °/s. Nobody picked the easy number
on purpose — it is what happens when a band cites one source and nobody asks what else that source
set contains. **A band may still be tightened before a run**, which is how that one was fixed; it
may never be touched after one.

## Conventions

- Inputs come from what is already committed: `cad/step/gen3/*.step` (Gen3 is current,
  see `cad/README.md`), `cad/parameters.json`,
  `analysis/femm/emocd_cross_section.dxf`. Where a check needs an orbit or a constant, it
  imports from `analysis/*.py` rather than restating the value, see `gmat/build_scripts.py`.
- Outputs land in `validation/results/<analysis>.json` alongside the solver version,
  mesh size, and boundary conditions, the same way `analysis/results/*.json` works.
- A completed run gets a `CHANGELOG.md` entry with cause, before/after, and the P/E item
  it moves.
- `analysis/*.py` stays authoritative until a run closes the relevant item. **Do not
  hand-edit a script to match an FEA result**, record the discrepancy first, decide
  second.

## Licensing

Keep these tools external. CalculiX and Code_Aster are GPL, Elmer is LGPL, and this
repository is MIT, commit input decks and result JSON, never vendored solver code.
Orekit (Apache-2.0), Project Chrono (BSD-3) and pyleecan (Apache-2.0) are permissive.
NASA's CARA tools are MATLAB under a NASA open-source agreement; parts run under Octave,
and the licence should be read before anything is redistributed.
