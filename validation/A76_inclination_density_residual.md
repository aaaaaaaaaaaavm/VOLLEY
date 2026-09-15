# A76, whether inclination through a variable atmosphere explains A75's residual

**Closes, if it passes:** the named candidate in [P79](../OPEN_PROBLEMS.md#p79)'s remaining
residual. It does not close P79.

[A75](A75_decay_density_calibration.md) inverted E28's two GMAT reentries into uniform density
scales of **1.9667** at 55.2 deg and **2.4443** at 9.6 deg, agreeing to **1.2428x**. One scalar
reproduces both, so `astro.py`'s shape in altitude was never the defect. What a scalar cannot carry
is two different values at the same altitude, and P79 records the obvious candidate in writing:
*"inclination is the obvious candidate, and that is the part a variable-density atmosphere would
explain."*

This run tests that sentence and nothing else. The two GMAT cases differ in exactly one input.
`validation/gmat/build_poem_campaign.py` sets both at 350 km, `ECC_BASE = 0.0`, RAAN 0, AOP 0,
TA 0, the same epoch, `MSISE90`, `F107 = F107A = 150.0` and `KP = 3.0`. Only `INC_DEG` differs. So
if a variable-density atmosphere explains the residual, it has to do it through inclination, and
there are two ways it can: the thermosphere's **latitude structure**, which a 9.6 deg orbit samples
differently from a 55.2 deg one, and the **J2 nodal regression rate**, which goes as cos i and so
sweeps the two orbits through the diurnal density bulge at different speeds.

> ## BANDS DECLARED 2026-09-15, BEFORE `analysis/inclination_density.py` EXISTS.
>
> Verify with `git show --stat <this commit> -- analysis/inclination_density.py`, which must
> return nothing.
>
> Bands 1 and 6 were run before declaration and that is deliberate: both check the tooling rather
> than the physics, and a tooling check nobody has run is not a check. The NRLMSISE-00 mass-density
> identity in band 1 was confirmed to 1.8e-7 over twenty scratch points, which is why its threshold
> is set at 1e-6 and not lower. **Bands 3 and 4, the two that can fail on the physics, were not
> evaluated in any form before this file was committed.** No ratio, no averaged density and no
> attribution split was computed.

## The evidence this run is tested against

Everything here is already in the repository. None of it is a measurement: GMAT is a second model
and NRLMSISE-00 is a third, so this is a structural test between models.

| | | |
|---|---|---|
| R2, 350 km, **55.2 deg** | reentered at **36 days** | E28, quoted in A50 |
| R3, 350 km, **9.6 deg** | reentered at **29 days** | E28, quoted in A50 |
| Inferred uniform density scales | **1.9667** and **2.4443** | A75 |
| The residual this run attacks | **1.2428x** | A75 |
| Run conditions | 350 km circular, RAAN/AOP/TA 0, epoch `01 Jan 2027 00:00:00.000`, F10.7 = F10.7A = 150.0, Kp = 3.0 | `validation/gmat/build_poem_campaign.py` |

Kp 3.0 converts to **ap 15** on the standard Kp-to-ap table. GMAT ran **MSISE90**; this run uses
**NRLMSISE-00**, `pymsis` 0.13.0 with `version=0`, because MSISE90 is not available here and its
successor is. That substitution is the reason band 4 is a structural test and not a reproduction of
GMAT's own numbers, and it is stated again under *What this run will not do*.

## What is held fixed, and why

Altitude is held at **350 km throughout**. This is not a decay simulation and does not integrate an
orbit down. Holding altitude fixed is what isolates inclination, which is the only input the two
GMAT cases disagree on. The primary averaging window is **29 days**, the shorter of the two
observed lifetimes, so both cases are averaged over a span both fleets actually survived; 36 days
is reported as a sensitivity rather than as a second answer.

## Acceptance bands

**Six bands. Bands 3 and 4 can fail, and band 4 is the one this run exists to ask.**

| # | Band | FAIL if |
|---|---|---|
| **1** | **Verification by identity.** At every sample point, NRLMSISE-00's returned total mass density reproduces its own species sum, `rho = 1.66e-27 * (4*He + 16*O + 28*N2 + 32*O2 + 40*Ar + 1*H + 14*N + 16*O_anomalous)` with number densities in cm^-3, to **<= 1e-6 relative** | The model's output is being read wrong, and every number below it is unfounded |
| **2** | **REPORT, no pass/fail.** Time-averaged density at each inclination, their ratio, and the same pair with the nodal regression frozen at the epoch value | The numbers belong on the record whichever way bands 3 and 4 fall |
| **3** | **Direction.** Time-averaged density at **9.6 deg exceeds** that at 55.2 deg, at the primary window and at all four quarter-year epochs | A variable atmosphere moves density the wrong way with inclination. The candidate P79 names is then wrong in sign, and its size stops mattering |
| **4** | **Magnitude.** The ratio explains at least half of A75's 1.2428x residual in log terms and overshoots by no more than the same amount: **ratio within [1.1148, 1.3855]**, being 1.2428^0.5 and 1.2428^1.5 | Inclination through a variable atmosphere is not the mechanism, or is only a minor part of one. P79's residual then needs a candidate nobody has named yet, and saying so is the result |
| **5** | **REPORT.** The attribution between latitude structure and local-time sampling, taken as the difference between the regressing-node and frozen-node ratios | Which of the two mechanisms carries the effect is the part that tells the next run what to build |
| **6** | **Guard on the nodal rate**, since band 5 rests entirely on it. The implemented secular rate must be **retrograde below 90 deg**, **prograde above**, **vanish at exactly 90 deg to <= 1e-15 deg/day**, and reach the sun-synchronous rate **360/365.2422 deg/day at an inclination inside (96, 98) deg** at 350 km circular | A sign or factor error in the one inclination-dependent term would manufacture band 5's answer out of arithmetic |

## What this run will not do

**It does not reproduce the GMAT runs and does not claim to.** NRLMSISE-00 is not MSISE90, and a
ratio agreeing with 1.2428x would be a structural explanation of the residual, not a second
derivation of the two lifetimes. The absolute level stays where A75 left it.

**It does not rebuild `astro.py`.** Nothing in `analysis/` changes behaviour as a result of this
run. If band 4 passes, the consequence is that a variable-density atmosphere is the right repair
for P79 and the residual has a named cause; building that atmosphere into the model is separate
work, and A50's failed band 1 stays failed either way.

**It does not touch E28.** Campaign mission life still needs the duration statement E28 asks for,
at whatever level the atmosphere is eventually quoted at.

**It is not hardware evidence, and there is still no measurement anywhere in this chain.**

---

## My execution, 2026-09-15

`pymsis` 0.13.0, NRLMSISE-00 through `version=0`. The run takes about one second and two runs on
this machine produce a byte-identical result, so it went into the freshness gate rather than
being excluded from it, at a declared 1e-6 because pymsis returns float32.

**Four of six bands resolve, and band 4, the one this run exists to ask, fails.**

| # | Band | Result | |
|---|---|---:|---|
| 1 | NRLMSISE-00 reproduces its own species sum | 2.860e-07 against 1e-6 | **PASS** |
| 2 | REPORT, the two averaged densities | 1.009985e-11 and 9.962054e-12 kg/m³ | REPORT |
| 3 | Direction, 9.6° denser than 55.2° | 1.0138, and 1.0408 / 1.0332 / 1.0273 at the other quarters | **PASS** |
| 4 | Magnitude inside [1.1148, 1.3855] | **1.0138** | **FAIL** |
| 5 | REPORT, attribution | latitude 1.0136, local time 1.0002× on top | REPORT |
| 6 | Nodal-rate guard | −0.144240 / +0.144240 °/day either side of 90°, 5.06e-16 at 90°, sun-synchronous at 96.8493° | **PASS** |

**The candidate P79 names is the right sign and the wrong size.** Inclination through a
variable-density atmosphere moves density the way the evidence needs, and band 3 holds at all four
quarters, so the direction is not an artefact of one epoch. But it delivers **1.0138×** where
A75's residual is **1.2428×**. In log terms that is **6.3 %** of it, short by a factor of **15.9**.

**Almost all of the little there is comes from latitude, not from local time.** Freezing the node
changes the ratio from 1.0138 to 1.0136, so the J2 nodal rate going as cos i contributes 1.0002×.
The second of the two routes this run was built to separate carries essentially nothing.

### Why the answer is this small, which is not what the point-wise numbers suggest

A post-hoc diagnostic is in the result file under `post_hoc_diagnostic_not_a_band`, added after the
bands were evaluated and depended on by none of them. At fixed UT the model's density varies
across latitude by **1.109× to 1.345×** — the right order to explain a 1.2428× residual. It does
not, because **the gradient reverses sign with local solar time**: towards the pole density rises
on the night side and falls on the day side. An orbit sampling every local time averages most of
the contrast away, and what survives is the 1.4 % that does not cancel.

So the failure is not the averaging being broken. The averaging is the mechanism.

### The sampling defect this run had first, preserved at `f65eab3`

The first execution sampled two revolutions per day, which put its step at exactly 43 200 s
against a diurnal cycle and pinned the grid to a fixed pair of local solar times. Band 5 reported
local-time sampling at 1.0004×, which is what a blind grid reports rather than what the atmosphere
does. The grid now walks every revolution contiguously — 452 revolutions over 29 days at 24 points
each — and nothing in it is commensurate with 24 h.

**The correction changed the answer by 0.0001.** 1.0137 became 1.0138, and band 4 fails either
way. The defect was real and had to be fixed before band 5 could be quoted; it was not what made
band 4 fail.

### What this leaves

P79's residual now has **no named cause**. The entry's sentence — *"inclination is the obvious
candidate, and that is the part a variable-density atmosphere would explain"* — is falsified as an
explanation of the size, and A76 is the reason to stop looking there. What is left is the
provenance flag `build_poem_campaign.py` already carries beside both cases: *"POEM-4-like —
UNVERIFIED"* and *"POEM-3-like — UNVERIFIED"*. Two GMAT runs whose reference orbits are not
traceable to this repository are a thinner foundation for a 1.2428× residual than they looked
while the residual had a physical candidate attached to it.

**A75 is untouched.** Its scales, its band and its re-quoted durations all stand; this run tests
the cause of the residual, not its size. **A50 band 1 stays failed.** **E28 stays open.**
