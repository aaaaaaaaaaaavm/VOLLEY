# VOLLEY: one page

Adityavardhan Mishra, Dept. of Mechanical Engineering, Symbiosis Institute of
Technology, Symbiosis International (Deemed University), Pune.
[adityavardhanmishr@gmail.com](mailto:adityavardhanmishr@gmail.com),
[full repository](https://github.com/aaaaaaaaaaaavm/VOLLEY)

> Nothing in this project has been built, fired, measured, qualified or flown, and no result here
> has been reviewed by a third party. Every number below is a script output. Where two solvers
> agree, that is a consistency check between models and not experimental validation.
> [`docs/PROVENANCE.md`](docs/PROVENANCE.md) says what stands behind each claim.

## The mission

VOLLEY is a last-mile orbital delivery programme for rideshare spacecraft. A secondary payload
inherits the orbit its primary was going to, and VOLLEY exists to change that without putting
propulsion on the satellite.

After the primary spacecraft separates, the launch vehicle's final stage can, where host
capability and mission rules permit, continue as a temporary controlled orbital delivery platform.
The host performs the coarse orbital repositioning and VOLLEY produces the fine, individually
commanded release condition for each secondary satellite. The stage then passivates and re-enters.

The mission has been that since [ADR-002](docs/adr/002-host-is-a-spent-upper-stage.md) in 2023.
What has changed across the generations is how much of the deployment machinery VOLLEY carries
itself. Gen5 is the self-contained electromagnetic implementation; Gen6 turns the stage's own
structure and length into part of the machine. The mission is the same and the integration
differs, and [`docs/LINEAGE.md`](docs/LINEAGE.md) keeps the two apart.


---

## 1. What VOLLEY asks

A CubeSat flown as a rideshare secondary inherits the primary customer's orbit. The spring that
ejects it adds 1 to 2 m/s. That is a real change in orbital energy, and at 2.5 m/s it extends
orbital lifetime by 8.2 %, but it is sized for separation, it is two orders of magnitude short of
what commanded orbit shaping needs, and it is the same value for every satellite in the manifest.
Of more than 4,800 nanosatellites and CubeSats catalogued as of January 2026, on the order of 222
carry a propulsion system; the rest stay where they were dropped.

The question is what it costs to give each of them a commanded departure velocity without putting
anything on the satellite.

## 2. Gen5, the analysed baseline

Gen5 is a frozen computational baseline rather than a measured one. An ironless double-sided
Halbach linear synchronous motor drives a reusable permanent-magnet sled along a 1.5 m track,
twelve 3U satellites feed from two transverse cassettes, and a contactless eddy-current brake
arrests the sled. Every figure is single-sourced to a committed JSON result and re-checked against
its script on every commit ([`docs/BASELINE.md`](docs/BASELINE.md), gate-checked by
`tools/make_baseline.py`).

| | | |
|---|---|---|
| Thrust constant | 10.54 N per kA/m, +/-1.01 % ripple | 2-D FEM agrees to 0.03 %, 3-D to 0.059 % |
| Exit velocity, 3U | 16.029 m/s | at 10.07 g for 162.3 ms |
| Pulse | 162.3 ms, 320 A peak | 2782 J gross, 2735 J net |
| Regeneration | 47 J over a 39 mm section | the brake takes the other 1162 J |
| Electrical to payload | 18.8 % net of regeneration | 514 J delivered |
| Dispersion, closed loop | 0.0274 m/s (3-sigma) | +/-0.10 km of apogee placement |
| Semi-major axis change | +28.8 km | orbital lifetime 1.60x at mean activity |
| Mass, dry / loaded | 126.6 / 174.6 kg | 10.55 kg per 3U satellite |
| Track first mode | 109.0 Hz | recoil 64.1 N.s per shot |
| Recurring hardware | ₹1,345,055 | every price assumed. No vendor has quoted any line item |

The 25 g acceleration ceiling this machine is designed to is a requirement it sets on itself. It
is not a CubeSat qualification limit: no published standard fixes a universal quasi-static level,
the CubeSat Design Specification defers test levels to the launch provider, and GEVS specifies a
random-vibration spectrum whose g<sub>rms</sub> is not a quasi-static equivalent
([P98](OPEN_PROBLEMS.md)). Whether any given satellite tolerates 10.07 g is payload-specific and
has not been established.

## 3. What Gen5 demonstrated

A commanded, per-satellite change in orbital energy, on a satellite that is never modified
mechanically or electrically, from a stage that was going to be discarded. A spring's designed
differential between satellites is exactly zero, which is categorical rather than a ratio, and no
mass correction touches it. One maximum-velocity shot gives +60.2 % of orbital life against a
2.5 m/s spring's +8.2 %, because lifetime extension is superlinear in delta-v.

It also demonstrated a method. 71 run sheets cover 68 analyses across A1 to A71 (A3, A26 and A60
were numbered and never written), each with its acceptance bands committed before the script that
produces the number existed. That is checkable, because the band commit touches no script. No band
has ever been widened after a result was known.

## 4. What Gen5 lost

Two competitive arguments were made for this machine and both are withdrawn by its own analyses.

| Claim | Status |
|---|---|
| Mass parity with a canisterised dispenser | Withdrawn. [A21](validation/A21_comparators.md) band 4 asked for parity within 15 %, and the ratio is 1.758, meaning 10.55 kg per 3U satellite against a dispenser's roughly 6.0 kg. It failed on a change to this work rather than to the comparator: [A46](validation/A46_enclosure_buildup.md) replaced an 8.00 kg packaging placeholder with 50.04 kg of derived line items. [P69](OPEN_PROBLEMS.md) |
| Constellation phase spacing | Withdrawn. Satellites released 1200 s apart reach 30 degrees of in-track phase in 468 seconds at zero delta-v, and hold it at zero relative rate; a commanded split reaches 30 degrees in 1.4 days and then drifts through it at 21.75 deg/day, which a propulsion-less satellite cannot null. A spring and a clock reach it. [P56](OPEN_PROBLEMS.md) |
| Lifetime-ratio invariance | Withdrawn. Offered as the result the analysis could defend, and GMAT R2022a falsified it. [P16](OPEN_PROBLEMS.md) |
| Against a cold-gas module on the satellite | Loses by 12.4x on mass, declared as a loss before the run so it could not be framed away afterwards |
| Against a spring on maturity | Loses outright. TRL 9 and thousands deployed, against TRL 2 to 3 and nothing measured |

Kill criterion 1, mass per satellite, is crossed at 5.3x on dry mass against a 2 kg estimate
([`docs/KILL_CRITERIA.md`](docs/KILL_CRITERIA.md): seven thresholds, three crossed).

## 5. What the analyses changed

Four results moved the design rather than confirming it.

1. Exact CAD mass took the headline from 20.37 to 16.029 m/s. A parametric 4.86 kg sled became
   9.445 kg when solid volumes were computed ([P15](OPEN_PROBLEMS.md)), and resolving the field
   through the array's 90 mm depth rather than sampling the centre plane then took another 4.42 %
   ([ADR-030](docs/adr/030-apply-the-depth-resolved-thrust-constant.md)). Both consequences were
   declared in writing before the analyses ran.
2. An independent propagator falsified a claim in this project's own abstract. GMAT disagreed at
   low solar activity by 18 % against a 5 % band. The cause was the sweep rather than the
   arithmetic.
3. ngspice found a term no script carried. Energy closure failed at 97.0 % against a declared 98
 to 102 %, and the missing 86.6 J a shot was the capacitor bank's own series resistance.
4. Every kilogram was attributed to the requirement causing it, then every requirement deleted.
   Across all 64 corners, 88.67 kg survives, which is 70.06 % of dry mass and 7.39 kg per
   satellite against a 2 kg criterion ([A35](validation/A35_constraint_ledger.md)).

## 6. Why the architecture moved

Result 4 is why. No combination of requirement deletions closes kill criterion 1, so Gen5 cannot
be optimised into its own mass target. On 2026-08-14
[ADR-032](docs/adr/032-gen6-stage-integrated-gas-store.md) changed the target, to deleting the
subsystems rather than shrinking them.

## 7. Current design direction, Gen6

The payload is accelerated directly, by cold gas, along a rail a spent upper stage already
provides. There is no mover, no stator carrying the shot, no pulse-power chain, no brake and no
return stroke. 29.75 kg is deleted and 43.33 kg becomes stage structure, while 11.45 kg of
containment and a sized gas store remain. A short trim stator that would correct the velocity the
gas produces is sized at 144.01 mm and suspended by
[ADR-036](docs/adr/036-seal-specification-and-the-trim-stage.md): at the specified 17.8 N seal it
may not be needed at all, and [P67](OPEN_PROBLEMS.md) decides.

> Gen6 has not inherited Gen5's evidence, and nothing on this page transfers to it. There is no
> FEA, no circuit model, no CFD and no second CAD implementation. Its release mechanism does not
> exist, and no launch provider has been approached about lending a stage.

## 8. Evidence boundary

| | |
|---|---|
| Measured | nothing. [`docs/FIGURE_INDEX.md`](docs/FIGURE_INDEX.md)'s `measured` evidence class has zero members |
| Cross-checked by an independently implemented method | the airgap field (2-D FEM to 0.03 %, 3-D to 0.059 %), the pulse chain (ngspice), the astrodynamics (GMAT R2022a) |
| Model output, single-sourced | everything else |
| Assumed | every price. [A21](validation/A21_comparators.md) band 7 required the comparison script to emit `NOT COMPUTED`, and it does. No cost claim is made in either direction |
| Independent review | none |
| Defect register | 153 numbered entries, 59 live, including every one that damages the claims above |
| Affiliation | none claimed. No institution, agency or company endorses, approves or is integrating this work. POEM and Vikram-1 appear in the manuscript as worked host examples only |

## 9. Where to read next

| | |
|---|---|
| The whole Phase I case on one page | [`docs/GEN5_CLOSURE.md`](docs/GEN5_CLOSURE.md) |
| Why the system exists, and what service it offers | [`docs/CONCEPT.md`](docs/CONCEPT.md) |
| Current programme disposition | [`docs/STATE_OF_THE_PROJECT.md`](docs/STATE_OF_THE_PROJECT.md) |
| What is broken | [`OPEN_PROBLEMS.md`](OPEN_PROBLEMS.md), [`docs/KILL_CRITERIA.md`](docs/KILL_CRITERIA.md) |
| The manuscript | [VOLLEY-paper](https://github.com/aaaaaaaaaaaavm/VOLLEY-paper), an IEEE-formatted technical manuscript, 18 pages |
| Ideas that were tried and stopped, with the reason each stopped | [VOLLEY-lab](https://github.com/aaaaaaaaaaaavm/VOLLEY-lab) |
| The opposite premise, a satellite that does carry passive hardware | [BOLLEY](https://github.com/aaaaaaaaaaaavm/BOLLEY) |
