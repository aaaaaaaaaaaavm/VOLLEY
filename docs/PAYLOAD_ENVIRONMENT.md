# Payload magnetic environment: what this deployer does to the satellite inside it

Written 2026-08-10. Every other magnetic figure this project publishes points *outward*, the
keep-out radius in `paper/paper.tex` §VII and the four-item interface in
[`adr/010-host-agnostic-interface.md`](adr/010-host-agnostic-interface.md) both say what VOLLEY
asks of a host. This file is the inward-facing half, and until now it did not exist.

> "The satellite is never modified" is the central claim of this project. This is the
> constraint that qualifies it.
>
> The claim is about mechanical and electrical modification, and in that sense it holds: no
> bolted armature, no sabot, no harness, no separation system on the customer's side. But a
> payload that must be *magnetically* screened, or whose soft-magnetic parts come back
> magnetised, has been modified in a way the phrase does not cover. A customer is entitled to
> read the claim as broader than it is, so the qualification belongs next to the claim rather
> than in an appendix.

Source: `analysis/payload_environment.py` to `analysis/results/payload_environment.json`.
These are model outputs. Nothing here has been measured ([`PROVENANCE.md`](PROVENANCE.md), E4).

---

## 1. The specification

Field strength across the 3U payload envelope, referenced to the sled's own Halbach arrays.
`z` is measured from the stator mid-plane; the array back face is at z = 14 mm and the payload
envelope spans z = 20 to 120 mm.

| z (mm) | Peak field | x Earth's field | x magnetometer full scale | Gradient dB/dz |
|---:|---:|---:|---:|---:|
| 20, near face | 61.081 mT | 1357x | 611x | −17.14 mT/mm |
| 30 | 7.827 mT | 174x | 78x | −1.19 mT/mm |
| 40 | 2.227 mT | 50x | 22x | −0.241 mT/mm |
| 50 | 0.887 mT | 20x | 8.9x | −0.064 mT/mm |
| 60 | 0.538 mT | 12x | 5.4x | −0.016 mT/mm |
| 70, payload CoM | 0.463 mT | 10x | 4.6x | −0.004 mT/mm |
| 80 | 0.435 mT | 9.7x | 4.4x | −0.002 mT/mm |
| 90 | 0.414 mT | 9.2x | 4.1x | −0.002 mT/mm |
| 100 | 0.392 mT | 8.7x | 3.9x | −0.002 mT/mm |
| 110 | 0.367 mT | 8.2x | 3.7x | −0.003 mT/mm |
| 120, far face | 0.341 mT | 7.6x | 3.4x | −0.003 mT/mm |

Peak over one wavelength, not mean: a payload does not get to average over the pole pitch, it
sits at whatever phase it sits at.

| Comparator | Value | Crosses below it at |
|---|---|---:|
| Attitude-magnetometer full scale | 100 µT *(class figure, not a datasheet)* | z = 251 mm |
| Earth's field in LEO | 45 µT | z = 332 mm |

The envelope ends at 120 mm and the first crossing is at 251 mm. Every part of the payload sits
above magnetometer full scale, and above Earth's own field, at all times. This is not a
near-face problem with a safe interior.

### The profile has two regimes, and they fail differently

The near face sits in a steep exponential. 61 mT at z = 20 mm falls to 7.8 mT by z = 30 mm,
a factor of eight in one centimetre, with a gradient of −17 mT/mm. Force on a soft-magnetic
part goes as ∇(B²), so the near face sees not only the largest field but essentially all of the
magnetic force. 10 mm of standoff is worth a factor of eight here, which is the single most
useful number in this table for anyone laying out a payload.

Everything beyond about 60 mm sits in a nearly uniform tail. From 0.538 mT at 60 mm to
0.341 mT at 120 mm, with a gradient two to four orders of magnitude smaller. The far two-thirds
of the payload is in a weak, almost gradient-free field that is still 4 to 10x Earth's. That
regime does not pull on anything appreciably; it saturates instruments and it magnetises.

This split is why one mitigation does not cover both. Standoff fixes the near face and does
nothing for the tail. The tail is a whole-volume condition.

---

## 2. Exposure duration, and why the static field is the one that matters

| Term | Duration | Notes |
|---|---|---|
| Drive transient | 162.3 ms per shot | One shot per satellite. A14 found this is not the dominant term |
| Static Halbach field | continuous while cradled | The array is a permanent magnet. It does not switch off between shots, or on the ground |

A14's finding was that the dominant term is the static magnet field, not the drive, and the
exposure profile is why that matters more than the field ratio alone. A 162.3 ms transient is a
transient. A permanent magnet is a permanent magnet: it is at full strength during integration,
through launch, throughout the coast, and for the whole campaign.

Cradle dwell is not specified anywhere in this repository, so the bound is stated as a bound:

- Lower bound: one cadence interval, 1200 s (ADR-020), if a satellite is indexed onto the
  sled immediately before firing.
- Upper bound: the full campaign, 4.0 h, if it is cradled throughout, plus all ground
  handling and launch, if the magazine is loaded before flight, which it is.

The honest reading is that exposure is measured in weeks to months, not milliseconds, and the
uncertainty is about the concept of operations rather than about the physics. Fixing that bound
is a ConOps decision nobody has made.

> ### What this file does not establish
>
> The field a satellite sees while stowed in a cassette, as opposed to cradled on the sled.
> Every number above is referenced to the sled's Halbach arrays. The cassette sits off the thrust
> line and its standoff is not in `cad/parameters.json` in a form the field model can consume.
> The sled case is the worst case and the one that matters, but it is not the whole duty cycle,
> and eleven of the twelve satellites are in a cassette for most of the campaign.

---

## 3. The distinction that decides whether this is a caveat or a defect

A saturated magnetometer recovers. Remanent magnetisation of soft-magnetic parts does not.

This is the question P34 flags as the one worth answering, and the two halves have genuinely
different consequences:

| | Recovers | Consequence |
|---|---|---|
| Magnetometer saturation | Yes, on leaving the field | An operational constraint: attitude determination is unavailable inside the deployer and for as long as it takes to recover. Sequencing, not hardware |
| Magnetorquer operation | Yes | Cannot be commanded meaningfully against a 611x bias. Same class as above |
| Remanent magnetisation of soft-magnetic structure, screws, shielding cans, motor laminations | No | The satellite leaves permanently altered. A residual dipole perturbs attitude control for the rest of the mission |

Only the third is a modification. The first two are constraints a customer can design a
sequence around. The third changes the satellite's magnetic properties for the life of the
mission, and it is the one that touches "never modified".

### This cannot be closed without a materials list, and that is P34 step 2

A threshold for permanently magnetising a payload's soft-magnetic parts needs to know what those
parts are made of. This project does not have that list and will not invent one, A14's
band 5 was declared VOID-able in advance on exactly this ground, and it is the reason the row
above says "no" rather than giving a number.

What can be said now is that the deployer's own load path contains soft-magnetic material:

| Part | Material | Source |
|---|---|---|
| Magazine septum, 1.0 mm, between satellites | silicon steel | `cad/parameters.json` `groups.magazine.septum_material` |
| Gate pins | A-286 | `groups.magazine.gate_pin_material` |

Silicon steel is chosen for its permeability. A 1 mm septum between adjacent satellites will both
shunt flux, which helps, and itself magnetise, which changes the field a neighbouring
satellite sees in a way nothing here has modelled. That is a second reason the in-cassette field
is not simply the sled field at greater distance.

This is the deployer's materials list, not the payload's. It does not substitute for step 2.

---

## 4. What a customer has to be told, and what would change it

Stated as a compatibility constraint, not as a solved problem:

1. A payload carrying an attitude magnetometer cannot use it inside this deployer. 611x full
   scale at the near face, 3.4x at the far face. It will read saturated everywhere in the
   envelope and recover after ejection.
2. A magnetorquer cannot be commanded meaningfully inside the deployer, for the same reason.
3. A payload with soft-magnetic structure may leave permanently magnetised. Whether it does
   depends on materials this project has not been told, and the honest answer today is that it is
   unquantified, not negligible.
4. Exposure is continuous, not per-shot. Assume weeks to months at the ground-handling end.
5. 10 mm of standoff at the near face is worth a factor of eight, and is the cheapest
   mitigation available to a payload designer.

Shielding the payload is the option that should be resisted. It adds mass to the customer's
satellite, which is precisely the modification this architecture exists to avoid. Recording it
here as available and unattractive rather than leaving a customer to discover it.

### What would close this

| Step | Status |
|---|---|
| 1. State the exposure with a trustworthy far field | DONE, this file. P3 and P21 are resolved, so the block on it is gone |
| 2. A payload materials list, and the magnetisation threshold that follows | OPEN. Needs a customer or a stated reference payload |
| 3. T-6 measures it | OPEN. Only measurement closes it |

P34 does not close on this file. It narrows, from "the extent of the affected volume is not
established" to "the extent is established and the materials are not". See
[`../OPEN_PROBLEMS.md`](../OPEN_PROBLEMS.md) P34.

---

## Provenance

Field values from `analysis/payload_environment.py`, which uses magpylib's `Cuboid`, an exact
analytic solution for a uniformly magnetised block, so the finite-array field is fully
three-dimensional with no mesh. P3 and P21, which previously blocked any far-field claim, are
both resolved: `analysis/far_field_sensitivity.py` showed the 7-wavelength default converged to
0.64 % at 10 mm and 4.4 % at 20 mm against a 15-wavelength array.

The magnetometer full-scale figure is a class figure, not a datasheet, COTS CubeSat
magnetometers typically saturate between ±60 and ±100 µT, and should be replaced with a specific
part before it is cited externally. Earth's field is taken at 45 µT against a 25-65 µT range.

Nothing here has been measured. Every number is a model output, and T-6 is the test that
would change that.
