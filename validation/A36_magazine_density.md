# A36 — magazine density, the only lever left on kill criterion 1

**Bands declared 2026-08-14, before `analysis/magazine_density.py` existed.**
Verify with `git show --stat <this commit> -- analysis/magazine_density.py`, which must return
nothing.

---

## Why this run exists

[A35](A35_constraint_ledger.md) attributed every kilogram to the requirement causing it and found
that **49.23 kg — 58.2 % of dry mass — survives every deletion of every requirement in every one of
64 corners.** At twelve satellites that is **4.10 kg each, still twice kill criterion 1.**

**No architecture change closes the criterion.** The surviving mass is per *machine*, and the only
lever A35 found that reaches the threshold is the divisor: the same mass over more satellites.
That lever is outside the physics entirely, needs no new subsystem, and **has never been studied.**

This run asks whether it is real.

## What is being modelled

Dry mass is split three ways. **The split is declared here, before the script, so it cannot be
tuned to pass.** Attribution is read from `constraint_ledger.py`'s C6 tagging rather than restated,
so there is one source and not two.

| Class | Items | Scaling |
|---|---|---|
| **Per satellite** | cassette shells, followers/gates/escapements — the containment A35 tagged `C6` | **∝ N** |
| **Magazine skin** | panels/closeouts, enclosure/radiator | **∝ N^(2/3)** — surface of a growing volume |
| **Fixed** | track, stator, sled, brake, bank, PPU, battery and avionics, harness, thermal, bracket | constant |

> **The N^(2/3) exponent is an assumption with no derivation behind it**, entered because a stated
> assumption is auditable and a hidden one is not. It is the single most contestable line in this
> run. The bracket is held **fixed**, which is optimistic — it really scales with what it carries —
> and that is stated rather than absorbed.

## Geometry that may not be violated

From `cad/parameters.json` via `payload_family.py`, and established by [A24](A24_fixed_cell_manifest.md):

| | |
|---|---|
| Cassette section | **166.0 mm** — a constraint written nowhere else until A24 found it |
| Stack pitch | **104.0 mm** |
| Cell length | **340.5 mm**, in a 380.5 mm cassette less a 30 mm drive bay |

---

## Acceptance bands

**Declared before the script. Not to be edited after the run.**

| # | Band | FAIL if |
|---|---|---|
| **1** | At N = 12 the model returns kg/satellite within **1 %** of `payload_family.py`'s output, **read from the source at run time** | The model does not reproduce the machine that exists |
| **2** | Fixed + skin + N × per-satellite reproduces modelled dry mass at every N, to **0.01 kg** | Mass is invented or lost in the split |
| **3** | The **N → ∞ limit** of kg/satellite is **≤ 2.0 kg** | **Magazine density cannot close kill criterion 1 at any manifest size, and A35's only remaining lever is gone** |
| **4** | kg/satellite reaches **≤ 2.0 kg** at **N ≤ 30** | The lever works only at a manifest size that is a different machine |
| **5** | At N = 24 an arrangement exists with **track-axis length unchanged** and largest transverse dimension **≤ the track length** | Doubling the manifest makes the machine wider than it is long, or forces the track longer — which fights the stowed-envelope goal directly |
| **6** | No reported arrangement violates the 166 mm section, 104 mm pitch or 340.5 mm cell | The density is bought by ignoring geometry A24 established |
| **7** | At ADR-020's **1200 s** cadence an N = 24 campaign completes in **≤ 12 h** | The host cannot be asked to hold station for the manifest |

### Band 1 is written the way it is because of P54

A24 band 1 encoded its reference as the literal **6.375 kg**, that figure was later corrected to
7.042, and the band now fails against a snapshot rather than against a disagreement. **This band
reads `payload_family.py` at run time and holds no literal**, so a future correction upstream moves
the reference with it instead of breaking the band.

### Band 3 is the decisive one

Bands 4 to 7 are engineering. **Band 3 decides whether the project has a route to kill criterion 1
at all.** If the per-satellite containment mass alone exceeds 2 kg, no manifest size helps, A35's
saturation result stands unrelieved, and the criterion must be renegotiated rather than met.

## What this run does not do

It does not design a magazine. It does not model indexing reach, follower travel, structural
depth of a taller stack, or the ascent loads on a doubled cassette — **all of which get worse with
N and none of which is priced here.** It reports a mass and an envelope, and every one of those
omissions makes the answer optimistic.

---

## Results

*(Filled after the run. Nothing above this line changes.)*
