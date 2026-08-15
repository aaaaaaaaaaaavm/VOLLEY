## Adityavardhan Mishra

**Mechanical engineer. Powertrain, ECUs, CubeSat deployment. Asking spacecraft inconvenient questions.**

BTech Mechanical Engineering, Symbiosis Institute of Technology, Pune · 2023–2027

In 2021 I got stuck on a dumb question: why do we still deploy CubeSats with springs. I never
really got unstuck. That question is now **VOLLEY**: an electromagnetic deployer that ejects
unmodified 3U CubeSats at a programmable velocity from a spent rideshare upper stage. Against the
fastest published spring it is 6.6 times the velocity — but **7.5 times the orbital lifetime it
buys**, which is the number that matters and the one I had been under-quoting. I've presented it
at DRDO ARDE and the India Science Festival.

Before that there was rocketry, where our payload took **2nd globally** at the SDL Payload
Challenge, IREC 2025 in Texas. Alongside it there are engines, I run Poona Motor Club, tune Royal
Enfield, KTM and Honda platforms, and when Powertronic's map files turned out to be an obfuscated
binary I reverse-engineered the format and built a dual-map editor so I could stop guessing. This
year I'm on powertrain for our Formula Student team.

Aerospace, telecom software, engines. I have a hunch they all come from the same place. Haven't
proven it yet.

---

### The thing I'd actually like you to look at

The idea is not really the motor. A launch vehicle's upper stage does its job in ten minutes and
then becomes debris; POEM has already flown the counter-example. **VOLLEY turns that spent stage
into a last-mile delivery vehicle** — it repositions between altitude shells on its own reaction
control and fires satellites off at individually commanded velocities at each one. **Altitude is
in; plane change is not**, at 133 m/s per degree — and **phase is not either**, which I found by
checking rather than by being told: satellites released minutes apart from the same host separate
in true anomaly for no velocity at all, so 30° costs **468 seconds of waiting**. The claim that
survives is **orbit change**, which no clock can imitate.

**[VOLLEY](https://github.com/aaaaaaaaaaaavm/VOLLEY)**, a magazine-fed ironless double-sided
Halbach linear synchronous motor that ejects unmodified CubeSats at **16.029 m/s and 10.07 g**,
drawing **2.78 kJ gross and 2.74 kJ net** per shot. TRL 2–3. Nothing built, fired or measured.

**The design target has since moved.** Attributing every kilogram to the requirement that causes
it showed the reusable magnet sled is **11 % of dry mass** and the pulse-power chain is **28 %**,
so the current target deletes the second: the payload accelerated directly, by cold gas, along a
rail the spent stage provides. **The architecture that was the target the day before is kept in
full**, with the measurement that retired it at the top of it.

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

That habit is the actual portfolio:
**[skills, with the file that proves each one](https://github.com/aaaaaaaaaaaavm/VOLLEY/blob/main/docs/SKILLS.md)**

| | |
|---|---|
| **[VOLLEY](https://github.com/aaaaaaaaaaaavm/VOLLEY)** | The authoritative engineering record. Start at [`docs/CONCEPT.md`](https://github.com/aaaaaaaaaaaavm/VOLLEY/blob/main/docs/CONCEPT.md) |
| **[VOLLEY-paper](https://github.com/aaaaaaaaaaaavm/VOLLEY-paper)** | IEEE manuscript and reproducibility package |
| **[VOLLEY-thesis](https://github.com/aaaaaaaaaaaavm/VOLLEY-thesis)** | Final-year submission |
| **[VOLLEY-lab](https://github.com/aaaaaaaaaaaavm/VOLLEY-lab)** | The vault: ideas that never became a complete thing, and why each stopped. Not citable |

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
outreach; member, Space Generation Advisory Council.</sub>

[adityavardhanmishr@gmail.com](mailto:adityavardhanmishr@gmail.com) ·
[LinkedIn](https://www.linkedin.com/in/adityavardhanmishra/) · Pune, India
