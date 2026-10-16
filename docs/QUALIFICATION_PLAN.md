# Qualification and environmental test plan

**Status: proposed physical validation; every test below is unrun.** No VOLLEY
hardware has been built. The plan describes the evidence a later article would
need; it is not a qualification result or an approved test specification.

Provider and spacecraft interface documents must establish applicable environments,
limits, margins, notching and acceptance procedures. GEVS and the CubeSat Design
Specification provide context; neither establishes a universal 25 g payload limit.
The 5/10/25 g cases are provisional sensitivity inputs. Random-vibration RMS levels
cannot be substituted for quasi-static strength or inflicted release-load limits.

---

## 0. What the deployer must survive, and what it must not inflict

Two directions, and they are easy to conflate:

| | The deployer as payload | The deployer as source |
|---|---|---|
| Sees | Launch loads from the vehicle | |
| Inflicts | | Ejection loads and stray field on the CubeSats it carries |
| Governing | Vehicle user guide, GEVS protoflight | CubeSat Design Specification interface, this design's chosen 25 g acceleration ceiling (not a CDS figure, P98), magnetic keep-out |

The second column is the unusual one. A spring deployer imparts 1-2 m/s and is magnetically
inert; VOLLEY carries a Halbach array centimetres from satellites it has not built, and fires
a 330 A pulse next to them. T-6 and T-7 address this electromagnetic configuration. Conventional dispensers also require mission-specific compatibility and release-environment verification.

---

## T-1: Random vibration, protoflight

| | |
|---|---|
| Level | GEVS protoflight, 14.1 g<sub>rms</sub>, 20-2000 Hz, 3 axes |
| Duration | 60 s per axis |
| Article | Full deployer, loaded with 12 mass simulators |
| Closes | E4, and the launch-restraint half of E10 |

Pass criteria. No change in first mode > 5 % between pre- and post-test signature sweeps
(a shift means something loosened). Retention gates hold the six-satellite stack preload,
the analysis said 5.9 kN through two D6 A-286 pins at margin 1.2, superseded 2026-08-10: the sizing case was quasi-static and the governing one is random vibration, so the gate is now two D9 pins at 41.0 kN, margin +0.45 at Q = 30 (A22). Margin 1.2 was thin
enough that this test is the one that matters. Launch locks hold the sled. No mass simulator
moves in its cassette.

> This is now a predicted failure, not a ranked risk (2026-08-06). A18 band 9 gives
> 11.7-20.2 kN through retention pins sized for 5.9 kN. P37.

What this is really testing. `sizing.py` gives the track a first mode of 48 Hz
pinned-pinned and 109 Hz fixed-fixed against a 70-100 Hz secondary-structure convention. The
design *specifies* end-fixed mounting to clear it. If the as-built joint is anywhere between
pinned and fixed (which is what A4 had to bracket for the chassis plate) the real mode may
sit inside the primary band. This is the single most likely qualification failure.

## T-2: Sine sweep and low-frequency

> Promoted to pass/fail 2026-08-06, and it must now report Q. A17 found the force ripple
> amplifies 8.18x at the 109 Hz mode and that no plausible damping rescues it (P36),
> and A18 found the retention load scales as sqrt(Q) with the margin going negative by Q = 30
> (P37). A signature comparison cannot answer either. T-2 must measure the damping at
> each mode, and it is a qualification item rather than a before-and-after check. See
> [`STRUCTURAL_GAP.md`](STRUCTURAL_GAP.md).

Vehicle-specific, typically 5-100 Hz at 1.25x flight limit. Pre- and post-signature sweeps
either side of every other test in this plan; they are how you detect damage that a visual
inspection misses.

## T-3: Shock

Pyroshock or equivalent at the separation-system level, per the vehicle ICD. The concern is
not the deployer surviving it but the magnets: shock is the credible path to cracking a
sintered NdFeB block or breaking a magnet bond. `sizing.py` gives the bond 0.118 MPa against
10 MPa allowable at a margin of 84, which is comfortable, but that figure is quasi-static and
shock is not.

Pass criteria. No change in airgap field measured before and after (a cracked or partly
demagnetised block shows up as a field change before it shows up as anything else).

## T-4: Thermal vacuum

| | |
|---|---|
| Level | 8 cycles, −40 °C to +60 °C, <= 1x10⁻⁵ torr, dwell to stabilisation |
| Article | Full deployer, powered, firing into the brake at temperature |
| Closes | E11, part of E4, and the operational half of E21 |

Pass criteria. A full 12-shot campaign at both temperature extremes with exit velocity
within the declared dispersion band. Bakeout mass loss per ASTM E595: TML <= 1.0 %, CVCM
<= 0.1 %, the materials rule (B16) already specifies E595-compliant selection, and this is
where that gets tested rather than asserted.

Why this one is load-bearing. Three open items converge here and nowhere else.
`sizing.py` puts the N45SH remanence temperature coefficient at −0.11 %/K over ±40 K, moving
the thrust constant ∓4.4 %, so velocity dispersion across the thermal range is a claim this
test either supports or destroys. E19 (eddy heating inside the magnet blocks, not
modelled anywhere) can only be observed in vacuum, where there is no convection to hide it.
And E21 (vacuum tribology of rollers reused twelve times, at 1.48 kN per pair) has no
analysis behind it at all, this is the first time the roller interface would run in its real
environment.

## T-5: Thermal cycling and brake soak

The eddy brake absorbs 1.29 kJ per shot into a 0.86 kg copper fin: a 3.9 K adiabatic rise per
shot, 47 K over a twelve-shot campaign if it never radiated. Fire twelve shots at the
minimum inter-shot cadence and instrument the fin. This is the direct test of a number the
paper quotes, and it is cheap once T-4 hardware exists.

## T-6: EMC and magnetic cleanliness

| | |
|---|---|
| Level | MIL-STD-461 RE102/CE102 class, tailored to the vehicle ICD |
| Closes | E12, and validates the keep-out behind P3 |

Radiated emissions during a 330 A pulse, and, the part with no spring-deployer precedent,
static field at the payload envelope. `verify_field.py` gives 22.7 / 4.3 / 0.4 mT at
10 / 20 / 50 mm behind the array. Pass criteria: measured field at the cassette payload
envelope within 20 % of that model, and inside the magnetometer limit of whatever satellite
is manifested. A customer flying a magnetometer or a magnetorquer needs this number measured,
not modelled, and the far-field values are the least trustworthy row in the whole field model.

## T-7: Payload-specific inflicted release environment

An instrumented inert 3U surrogate would record axial/lateral acceleration, shock,
angular rate, restraint unloading and contact across the actual release stroke.
The historical periodic-force model predicts 10.068 g, but its release-speed claim
is challenged. The 5/10/25 g sensitivity cases are not payload allowables.

Pass bands must come from the selected spacecraft and host interface documents.
The checked NRCSD IDD Rev. - gives 0.5–2.0 m/s deployment and up to 5°/s per axis
for its ISS interface. Those values do not approve a VOLLEY release. The CDS does
not supply a universal quasi-static or rotational qualification limit.

## T-8: Life and reuse

A provisional endurance study could use 200 shots with inspections of rollers,
rails, magnet bonds, retention, brake and reset behavior between blocks. That is
16 complete twelve-shot campaigns plus eight shots, not ten campaigns.
The actual required count, duty cycle, environments, wear limits and statistical
reliability demonstration must be defined from a service requirement before testing.
No endurance run has occurred, and a proposed shot count closes no reuse criterion.

---

## Sequence, and what gates what

```mermaid
flowchart TD
    B["Benchtop sub-scale<br/>docs/BENCHTOP_TESTS.md"] --> EM["Engineering model<br/>full-scale, ambient"]
    EM --> T7["T-7 ejection environment<br/>the 25 g and tip-off claims"]
    EM --> T8["T-8 life and reuse<br/>200 shots"]
    T7 --> QM["Qualification model"]
    QM --> T2["T-2 signature sweep"]
    T2 --> T1["T-1 random vibration"]
    T1 --> T3["T-3 shock"]
    T3 --> T4["T-4 thermal vacuum"]
    T4 --> T5["T-5 brake soak"]
    T5 --> T6["T-6 EMC and magnetics"]
    T6 --> T2b["T-2 signature sweep, post"]
```

Signature sweeps bracket the environmental block because that is how damage is detected. T-7
and T-8 come first, on an engineering model, because they test claims the design rests on
and if the 25 g or tip-off numbers fail there, the qualification model should not be built
to that design.

## What this plan costs, honestly

Nothing here is affordable on a student budget. A protoflight vibration and TVAC campaign at
an Indian test house is a five-to-six-figure rupee proposition per article before the article
itself exists, and `analysis/cost.py` puts recurring hardware alone above ₹1.3 M with every
price assumed.

That is the argument for `docs/BENCHTOP_TESTS.md`. Four of the claims above can be tested
at sub-scale for the price of the magnets, and doing so would give this project its first
measured number, which it does not currently have at any scale (E4).
