## Adityavardhan Mishra

**Mechanical engineer. Powertrain, ECUs, CubeSat deployment. Asking spacecraft inconvenient questions.**

<p align="center">
  <img src="https://raw.githubusercontent.com/aaaaaaaaaaaavm/VOLLEY/main/cad/renders/gen5/hero_open.png" alt="VOLLEY, an electromagnetic CubeSat deployer" width="100%">
</p>

BTech Mechanical Engineering, Symbiosis Institute of Technology, Pune · 2023–2027

In 2021 I got stuck on a dumb question: why do we still deploy CubeSats with springs. I never
really got unstuck. That question is now **VOLLEY**: an electromagnetic deployer that ejects
unmodified 3U CubeSats at a programmable velocity from a spent rideshare upper stage. I've
presented it at DRDO ARDE and the India Science Festival.

Before that there was rocketry, where our payload took **2nd globally** at the SDL Payload
Challenge, IREC 2025 in Texas. Alongside it there are engines, I run Poona Motor Club, tune Royal
Enfield, KTM and Honda platforms, and when Powertronic's map files turned out to be an obfuscated
binary I reverse-engineered the format and built a dual-map editor so I could stop guessing. This
year I'm on powertrain for our Formula Student team.

Aerospace, telecom software, engines. I have a hunch they all come from the same place. Haven't
proven it yet.

---

<p align="center">
  <img src="https://raw.githubusercontent.com/aaaaaaaaaaaavm/VOLLEY/main/figures/A29_wake.png" alt="OpenFOAM solution around the sled" width="32%">
  <img src="https://raw.githubusercontent.com/aaaaaaaaaaaavm/VOLLEY/main/figures/A02_field_map.png" alt="Halbach airgap field and its depth profile" width="32%">
  <img src="https://raw.githubusercontent.com/aaaaaaaaaaaavm/VOLLEY/main/figures/A35_ledger.png" alt="Constraint ledger and the 64-corner floor" width="32%">
</p>

<p align="center"><sub>External aerodynamics in OpenFOAM, <b>581&nbsp;779 cells</b> &middot; the Halbach airgap field resolved through the array's 90&nbsp;mm depth &middot; every kilogram attributed to the requirement that causes it. <b>All three are model output. Nothing in the project has been built, fired or measured</b> &mdash; and the repository leads with that rather than hiding it.</sub></p>

### The thing I'd actually like you to look at

The idea is not really the motor. A launch vehicle's upper stage does its job in ten minutes and
then becomes debris; POEM has already flown the counter-example. **VOLLEY turns that spent stage
into a last-mile delivery vehicle** — it repositions between altitude shells on its own reaction
control and fires satellites off at individually commanded velocities at each one. **Altitude is
in; plane change is not**, at 133 m/s per degree — and **phase is not either**, which I found by
checking rather than by being told: satellites released minutes apart from the same host separate
in true anomaly for no velocity at all, so 30° costs **468 seconds of waiting**. What survives is
narrower and I think better: **a clock changes phase, and a commanded deployment impulse changes
orbital energy.** Drag and J₂ change orbits too — the point is not that nothing else can, it is
that nothing else in a deployment interface can do it *per satellite, on command*.

**[VOLLEY](https://github.com/aaaaaaaaaaaavm/VOLLEY)**, a magazine-fed ironless double-sided
Halbach linear synchronous motor that ejects unmodified CubeSats at **16.029 m/s and 10.07 g**,
drawing **2.78 kJ gross and 2.74 kJ net** per shot. TRL 2–3. Nothing built, fired or measured.

**The design target has since moved, and the reason is the best result in the project.** I
attributed every kilogram of the deployer to the requirement that causes it, then deleted every
requirement in all 64 combinations to find the lightest machine any relaxation could reach.
**88.67 kg survives all of them** — 70 % of dry mass, against a 2 kg-per-satellite criterion. There
is no version of Gen5 that meets its own mass target. So the target changed from shrinking
subsystems to deleting them: the payload accelerated directly, by cold gas, along a rail the spent
stage already provides. **The architecture that was the target the day before is kept in full**,
with the analysis that retired it at the top of it.

**Gen5 keeps every headline number, because Gen5 is what has the structural FEA, the CFD, the
designed control loop and the second CAD implementation behind it. The current direction has none
of those and does not inherit them.** Both are published side by side rather than one quietly
replacing the other.

### What it proved, and what it lost

**It proved one thing**: a commanded, per-satellite change in orbital energy, on a satellite that
is never modified mechanically or electrically. A spring gives every satellite the same push, and
its designed differential is exactly zero — that is categorical, and no amount of mass correction
touches it.

**It lost two arguments to its own analyses, and both are on the front page.** Mass parity with a
canister of springs is **withdrawn**: an acceptance band written before the comparison script
existed asked for parity within 15 %, and VOLLEY is **1.758× heavier per satellite**. So is the
constellation-phasing claim — 30° of in-track phase costs **468 seconds of waiting** at no velocity
cost, so a spring and a clock reach it and this machine is not needed for it.

**Open it for the defect record, not the numbers.** Every error I've found in my own work is
published and numbered, including the ones that damage the claims. An independent propagator
falsified a claim in my paper's own abstract; that's logged as P16 rather than quietly dropped.
The pulse-power chain does not close on a commercially realistic single supercapacitor string.
A covariance claim, an internal-momentum conclusion and the brake-fin thermal model have all
been superseded in public.

**Acceptance bands are written down *before* each analysis runs**, so a failure cannot be
rationalised afterwards. That is not a formality. Twice this month a band failed, I went looking
for the design flaw, and found the bug in **my own analysis script** instead — once a sign
convention that had quietly cost 57 km of a delivery envelope, once a limit I had computed for
one burn of a two-burn manoeuvre. A band chosen after seeing the answer would have passed both
and shipped both.

The most recent one is the flavour of the whole thing: modelling the release properly showed the
release was never the problem — the payload arrives in its cradle at **18 to 115 times** the
tip-off limit at the *start* of the stroke, which nothing had looked at.

### The sibling study that tests the opposite premise

VOLLEY refuses to touch the satellite, and that refusal is expensive — most of the energy goes into
launcher hardware, and most of the mechanism exists to stop and return it. **[BOLLEY](https://github.com/aaaaaaaaaaaavm/BOLLEY)
asks what happens if I stop refusing**: the spacecraft accepts a few hundred grams of *passive*
interface — no power, no electronics, nothing to command — and the launcher deletes the sled, the
brake and the return stroke. Same evidence standard, opposite answer to the same question, and it
records the branches that failed as carefully as the one that worked.

That habit is the actual portfolio:
**[skills, with the file that proves each one](https://github.com/aaaaaaaaaaaavm/VOLLEY/blob/main/docs/SKILLS.md)**

| | |
|---|---|
| **[VOLLEY](https://github.com/aaaaaaaaaaaavm/VOLLEY)** | The authoritative engineering record. Start at [`docs/CONCEPT.md`](https://github.com/aaaaaaaaaaaavm/VOLLEY/blob/main/docs/CONCEPT.md) |
| **[VOLLEY-paper](https://github.com/aaaaaaaaaaaavm/VOLLEY-paper)** | The manuscript — IEEE-formatted, 18 pages, written and unsubmitted — and the reproducibility package |
| **[VOLLEY-thesis](https://github.com/aaaaaaaaaaaavm/VOLLEY-thesis)** | Final-year submission |
| **[VOLLEY-lab](https://github.com/aaaaaaaaaaaavm/VOLLEY-lab)** | The vault: ideas that never became a complete thing, and why each stopped. Not citable |
| **[BOLLEY](https://github.com/aaaaaaaaaaaavm/BOLLEY)** | The sibling study. Same standard, opposite premise: the satellite carries passive hardware so the launcher can delete its own |

---

### Three smaller tools that survived the extraction

I pulled out the parts that still make sense without the spacecraft around them. Each repository
keeps its VOLLEY source commit and file hashes, and each keeps the failed or void evidence beside
the useful result.

| Repository | What it does | Boundary |
|---|---|---|
| **[Pulsed Linear Motor Design Lab](https://github.com/aaaaaaaaaaaavm/pulsed-linear-motor-design-lab)** | Screens force, stroke, moving mass, source impedance and energy | Constant-force model; no hardware validation |
| **[Engineering Evidence Toolkit](https://github.com/aaaaaaaaaaaavm/engineering-evidence-toolkit)** | Checks finite results, local links, source presence and artifact hashes | Consistency is not physics validation |
| **[Orbital Deployment Trade Study](https://github.com/aaaaaaaaaaaavm/orbital-deployment-trade-study)** | Screens tangential impulses, phase drift, recoil and internal-mass disturbance | Two-body and rigid-body only; not conjunction assessment |

---

### What I actually do

**Simulation**: scikit-fem, gmsh, GetDP, CalculiX, ngspice, GMAT, magpylib. I wrote a 2-D
magnetostatic FEM from the weak form to check my own thrust constant; it agrees to **0.03%** at
the corrected operating point, the first time that number rested on a PDE solve instead of
another superposition model.

**CAD/CAE**: Fusion 360, SolidWorks, AutoCAD, ANSYS. Three CAD generations of the deployer, all
in the repository as STEP.

**Engines**: combustion airflow, head porting, camshaft profiling, ECU calibration. 46 to ~60 bhp
on an RE Super Meteor 650, dyno-validated across the band.

**Code**: Python for numerics, traceability tools and engineering automation; MATLAB and C where
the problem needs them. At work I own systems architecture and product design for a telecom CRM
platform, which is not what I was hired to do.

<sub>Hindi and English native · Marathi, Maithili · Russian, French elementary. Friends call me AVM,
pronounced how it's spelled, *Aevium*. Recognised by the ISRO Chairman for aerospace STEM
outreach; member, Space Generation Advisory Council. <b>Both are personal, and neither implies
that any organisation endorses, approves or is involved in the engineering work above.</b></sub>

[adityavardhanmishr@gmail.com](mailto:adityavardhanmishr@gmail.com) ·
[LinkedIn](https://www.linkedin.com/in/adityavardhanmishra/) · Pune, India
