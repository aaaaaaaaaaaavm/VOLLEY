# A36, magazine density, the only lever left on kill criterion 1

**Bands declared 2026-08-14, before `analysis/magazine_density.py` existed.**
Verify with `git show --stat <this commit> -- analysis/magazine_density.py`, which must return
nothing.

---

## Why this run exists

[A35](A35_constraint_ledger.md) attributed every kilogram to the requirement causing it and found
that 49.23 kg, 58.2 % of dry mass, survives every deletion of every requirement in every one of
64 corners. At twelve satellites that is 4.10 kg each, still twice kill criterion 1.

No architecture change closes the criterion. The surviving mass is per *machine*, and the only
lever A35 found that reaches the threshold is the divisor: the same mass over more satellites.
That lever is outside the physics entirely, needs no new subsystem, and has never been studied.

This run asks whether it is real.

## What is being modelled

Dry mass is split three ways. The split is declared here, before the script, so it cannot be
tuned to pass. Attribution is read from `constraint_ledger.py`'s C6 tagging rather than restated,
so there is one source and not two.

| Class | Items | Scaling |
|---|---|---|
| **Per satellite** | cassette shells, followers/gates/escapements — the containment A35 tagged `C6` | **∝ N** |
| **Magazine skin** | panels/closeouts, enclosure/radiator | **∝ N^(2/3)** — surface of a growing volume |
| **Fixed** | track, stator, sled, brake, bank, PPU, battery and avionics, harness, thermal, bracket | constant |

> The N^(2/3) exponent is an assumption with no derivation behind it, entered because a stated
> assumption is auditable and a hidden one is not. It is the single most contestable line in this
> run. The bracket is held fixed, which is optimistic, it really scales with what it carries,
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

Declared before the script. Not to be edited after the run.

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
reads `payload_family.py` at run time and holds no literal, so a future correction upstream moves
the reference with it instead of breaking the band.

### Band 3 is the decisive one

Bands 4 to 7 are engineering. **Band 3 decides whether the project has a route to kill criterion 1
at all. If the per-satellite containment mass alone exceeds 2 kg, no manifest size helps, A35's
saturation result stands unrelieved, and the criterion must be renegotiated rather than met.

## What this run does not do

It does not design a magazine. It does not model indexing reach, follower travel, structural
depth of a taller stack, or the ascent loads on a doubled cassette, all of which get worse with
N and none of which is priced here. It reports a mass and an envelope, and every one of those
omissions makes the answer optimistic.

---

## Results

**RUN 2026-08-14. Six of seven bands pass. Band 4 fails, and it is the one that mattered.**

| # | Band | Result | |
|---|---|---|---|
| 1 | reproduces `payload_family` at N = 12, within 1 % | 7.044 against **7.042 kg** | **PASS** |
| 2 | split reproduces dry mass to 0.01 kg | 84.5316 against 84.5316 | **PASS** |
| 3 | N → ∞ limit ≤ 2.0 kg/satellite | **0.954 kg** | **PASS** |
| 4 | ≤ 2.0 kg/satellite at N ≤ 30 | **first at N = 116** | **FAIL** |
| 5 | N = 24 packages within the track length | 5 arrangements, best 664 mm | **PASS** |
| 6 | geometry respected | cassette length unchanged throughout | **PASS** |
| 7 | N = 24 campaign ≤ 12 h | 8.0 h | **PASS** |

### The mass split

| | |
|---|---:|
| Fixed | **59.58 kg** |
| Magazine skin, at N = 12 | 13.50 kg, growing as N^(2/3) |
| **Per satellite** | **0.954 kg** — A35's C6 containment |

### The curve

| N | dry kg | **kg/satellite** | stack z | width y | campaign |
|---:|---:|---:|---:|---:|---:|
| 12 | 84.53 | **7.044** | 416 | 498 | 4.0 h |
| 24 | 103.91 | **4.330** | 624 | 664 | 8.0 h |
| 36 | 122.02 | 3.389 | 936 | 664 | 12.0 h |
| 60 | 156.32 | 2.605 | 1040 | 996 | 20.0 h |
| 96 | 205.20 | 2.138 | 1248 | 1328 | 32.0 h |

### Band 3 passes and band 4 fails, and both are needed to read the result

The limit is 0.954 kg/satellite, so magazine density *does* reach the criterion in principle.
It first reaches 2.0 kg at N = 116, which is not a denser magazine, it is a different machine.

And N = 116 cannot be packaged at all. *Derived here from the run's own geometry:* every
factorisation of 116 puts either the stack or the width outside the 1500 mm track length,
4 x 29 gives a 3016 mm stack, 29 x 4 gives a 4814 mm width, and so on for all six. The largest
manifest that fits is N = 126 (14 slots x 9 cassettes, 1456 x 1494 mm), which reaches
1.941 kg/satellite on a 244.6 kg machine running a 42-hour campaign.

> Kill criterion 1 is reachable by manifest size, and only at the very edge of what the
> envelope permits, on a machine three times the mass of the present one.

### A correction I owe

Reporting A35 I wrote that the surviving 49.23 kg over twenty-four satellites is 2.05 kg each,
and allowed that letting the containment grow might put it "near 2.5 kg."

It is 4.330 kg. The naive division held the machine constant while the containment and skin
both grow with N, and the estimate was wrong by more than a factor of two. **Band 4 was written to
test that claim and it caught it** — which is the entire purpose of declaring a band before knowing
the answer.

### Where this leaves kill criterion 1

Three routes existed. Two are now closed by measurement:

| | |
|---|---|
| **Architecture** | **Closed by A35.** 49.23 kg survives every requirement deletion in all 64 corners |
| **Manifest size** | **Closed by A36 band 4.** Reachable only at N ≈ 116–126, outside the envelope or at its edge, on a 244.6 kg machine |
| **Smaller payloads** | **Open.** `docs/PAYLOAD_CLASSES.md` already puts PocketQube at 0.266 kg/satellite. It closes the criterion and changes the product |

The criterion is now met by exactly one route, and that route is a different market. That is a
decision for the owner, not an analysis, and it should be taken explicitly rather than absorbed.

### Limitations, and every one of them makes this optimistic

Indexing reach, follower travel over a 1248 mm stack, the structural depth a taller cassette needs,
and ascent loads on a doubled magazine are not priced. The N^(2/3) skin exponent has no
derivation. The ESPA bracket is held fixed when it really scales with what it carries. A real
magazine at N = 24 will be heavier than 103.91 kg, not lighter.
