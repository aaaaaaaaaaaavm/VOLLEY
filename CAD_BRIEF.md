# CAD brief

**A brief written to be read before modelling, by a person or an agent, from a link to this
repository alone.** It answers the questions a modeller has to answer before the first sketch,
and it resolves — explicitly — every place where two files in this repository disagree.

Everything here is derived from [`cad/parameters.json`](cad/parameters.json). Where this brief
and that file differ, **`parameters.json` wins and this brief is wrong**; report it.

---

## Object

**VOLLEY** is a magazine-fed electromagnetic CubeSat deployer, roughly 1.8 m long and 76 kg dry,
which mounts to a host spacecraft or spent upper stage on an ESPA ring flange and ejects twelve
unmodified 3U CubeSats one at a time along a single axis.

**Function.** An ironless double-sided Halbach linear synchronous motor accelerates a *reusable
magnetic sled* along a track. The sled carries a CubeSat, releases it at exit velocity, and is
then arrested by an eddy brake and returned for the next shot. The satellite is never modified
and carries no magnets — **the magnets ride the sled, not the payload.** Satellites feed
transversely from two six-slot cassettes into the breech.

**Design intent, in one line:** replace a ~2 m/s spring with a **16.388 m/s** commanded,
programmable push, without asking the customer to change their satellite.

---

## Coordinate frame

> **x** = firing axis, positive **toward the muzzle**. Origin **x = 0 at the ESPA flange aft
> mating face**.
> **y** = lateral. P = +y port, S = −y starboard.
> **z** = vertical. **z = 0 at the stator mid-plane.**

The payload travels in **+x** and leaves through the muzzle at x ≈ 1805 mm. It does **not** leave
through the flange at x = 0. Two superseded renders showed exactly that error and it is logged as
**P43** — if a model has the satellite exiting anywhere near x = 0, it is wrong.

---

## Parts, and the order they assemble in

Nine Fusion documents. The names below are the ones used in `parameters.json`,
`cad/step/gen3/`, the render filenames and `cad/DIMENSIONS.md` — they are consistent across all
four, and new work should keep them consistent. (The `EMOCD_` prefix is the project's former
name; it is retained in filenames so history stays traceable.)

| # | Document | What it is | Attaches to |
|---:|---|---|---|
| 1 | `EMOCD_Interface_ESPA` | Ring flange, hub plate, 4 gussets | **The base.** Everything else references it |
| 2 | `EMOCD_Track` | 2 longerons, roller channels, guide rails, launch locks | ESPA hub, runs +x |
| 3 | `EMOCD_Stator` | 162-conductor three-phase belt winding, two belts | Track, z = ±5 mm about the mid-plane |
| 4 | `EMOCD_Sled` | Halbach arrays, Ti chassis, webs, backstop, 4 rollers, brake fin | Rides the track on its rollers |
| 5 | `EMOCD_Magazine_Cassette` | Shell, follower drive, escapement, retention gate + pins, septa | Track, transverse. **Two instances** |
| 6 | `EMOCD_Brake` | 2 tapered pole plates, ring-spring stop | Track, x = 1530–1740 mm |
| 7 | `EMOCD_Payload_3U` | 3U CubeSat with CDS corner rails | **Twelve instances**, six per cassette |
| 8 | `EMOCD_Enclosure` | Skins, muzzle panel, aft flange cutout, radiator, equipment bays | Wraps everything |
| 9 | `EMOCD_Assembly` | Inserts all eight above | Carries the joints |

**Joints.** `sled_slider_X` — the sled is a slider on x only. `payload_on_sled_rigid` — the
payload is rigid to the sled from breech to release, then free.

**The second cassette is a 180° rotation about z through x = 210.25 mm, not a mirror.** Fusion
rejects mirror transforms on external references, and a mirrored cassette would also invert the
escapement handedness. Rotate it.

---

## Critical dimensions — these are the ones that cannot move

Changing any of these invalidates analysis that is already run and published. They are not
styling choices.

| Dimension | Value | Why it is fixed |
|---|---:|---|
| Magnetic **air gap per side** | **1.0 mm** | Sets the thrust constant Kt = 11.0258 N/kA·m. Everything downstream is a function of it |
| Sled gap shim **tolerance** | **±0.05 mm** | The 6 mm chassis exists to hold this against the inter-array attraction |
| **Pole pitch / wavelength** | **24 / 48 mm** | Fixes the winding and the Halbach period together. They must stay in a 1:2 ratio |
| Halbach array **length** | **340 mm** | With a finite stator this sets where end effects begin |
| Halbach magnet **thickness** | **8 mm** | Field amplitude |
| Stator **active depth** (y) | **90 mm** | Force per metre scales with it |
| **Acceleration zone end** | **1300 mm** | The 1.3 m over which work is done |
| **Release point** | **1500 mm** | Where the payload separates. Exit velocity is quoted here |
| ESPA **bolt circle / holes** | **Ø400 mm, 24 × Ø9** | Host interface. Not ours to choose |
| Payload **envelope** | **340.5 × 100 × 100 mm** | CubeSat Design Specification. Not ours to choose |
| Payload **corner rails** | **8.5 mm** | Same |
| Gate **pin diameter** | **D9, A-286, 2 per cassette** | Resized from D6 by A22 against random vibration at Q = 30. **Do not revert to D6** — it gives a negative margin |

## Soft dimensions — adjust these for fit

Chassis web positions and thicknesses, roller diameter and spacing, gusset geometry, radiator
placement, equipment-bay positions within their envelopes, skin thickness away from the muzzle
panel, and all fillets, chamfers and fastener detail. **None of these are modelled in the current
CAD at all**, which is a real limitation rather than a decision.

## Tolerances that matter

Only three, and the rest are unspecified because they have not been engineered yet:

1. **Air gap 1.0 mm per side, ±0.05 mm.** The sled chassis is stiffness-driven to hold this.
2. **Roller channel to roller.** Clearance unspecified; the channels are drawn at 67–90 mm
   against 30 mm rollers at y = 70–86 mm.
3. **Muzzle aperture 160 × 160 mm** against a 100 × 100 mm payload — 30 mm of radial clearance,
   which is the tip-off allowance, not a fit tolerance.

---

## Conflicts in this repository, and which side to build

**Read this section before anything else.** This repository deliberately keeps its unresolved
problems visible rather than deleting them, so a reader cross-referencing files *will* find
contradictions. Every one below is real and known. The right-hand column is what to model.

| # | The conflict | Build this |
|---:|---|---|
| 1 | **Gen4 renders vs `parameters.json`.** The published renders come from a Fusion Gen4 configuration that stows the sled at s = 300 mm and releases at **s = 1200 mm over a 900 mm stroke**. `parameters.json` says acceleration ends at 1300 and release is at **1500 mm**. | **`parameters.json`.** Gen4 is a provisional, unexported configuration whose performance is explicitly not claimed (`cad/CHANGELOG_CAD.md`, ADR-019, P39). Every published number rests on the 1.5 m stroke |
| 2 | **The renders are not dimensional references.** They are Gen4, and no committed STEP matches them. | Use the renders **only** for arrangement, proportion and the direction of departure. **Take no dimension off an image** |
| 3 | **Cassette shell: closed panels or open frame?** `parameters.json` draws closed **4 mm** panels; `mass_properties.py` assumes a **6 % fill open frame**. The ~4.8 kg gap is a genuinely unmade decision, not an error | **Closed 4 mm panels.** They are the upper bound and they are the mounting surface the 1 mm silicon-steel septa need. Flag it as open |
| 4 | **Stator single-layer or two-layer?** Unmade electromagnetic decision | **Single layer**, as drawn |
| 5 | **Envelope 1839 mm vs ESPA Grande's ~1270 mm class.** Over by ~44 % | **Build 1839 mm.** Do not quietly shrink it to fit. P9 is open and the geometry exists to state the problem |
| 6 | **Stator end turns are not modelled.** Correct for computing field and force; **wrong for packaging** — real racetrack ends wrap beyond the 90 mm active depth | **Model them** in any new generation, and expect the envelope to grow in y. This is a known gap, not an omission to copy |
| 7 | **Sled mass.** Gen3 solids give **9.445 kg** as drawn — unpocketed plates. The parametric estimate was 4.86 kg | **Model as drawn, solid.** Pocketing the sled changes exit velocity: re-run `mass_properties.py` then `motor_model.py` before quoting anything. P5, P8, P15 |
| 8 | **Brake pole plates at 15 mm** were lightened from solid blocks on structural reasoning alone; **no magnetic sizing has been done** | Model at 15 mm and treat the result as provisional |
| 9 | **Fusion-computed masses are wrong on purpose.** The model uses solid copper for the stator, solid aluminium for CubeSats and steel standing in for NdFeB | **Never quote a mass from the CAD.** `analysis/mass_properties.py` is authoritative for mass; Fusion is authoritative for geometry and fit only |

---

## Constraints the geometry has to satisfy

- **The payload leaves in +x, through the muzzle, away from the host.** Non-negotiable, and the
  single thing most worth checking in a finished model.
- **The magnets never leave the machine.** If a magnet is on the departing satellite, the design
  has been misread.
- **The muzzle aperture must be genuinely open** on the satellite exit line, and solid above it.
  The current model verifies this by point-containment probe.
- **Equipment bays must stay clear of the track.** Verified in the current model.
- **The aft flange cutout is a horseshoe by design** — the flange OD extends below the belly
  line, so the cutout breaches the panel's lower edge. That is not a modelling error to fix.
- **Retention gates hold against launch vibration, not against the shot.** They are sized by
  random vibration through a 109 Hz mode at Q = 30, with a 5900 N ascent preload.
- **200 g arrest cap on the brake.** The tapered pole entry is what limits deceleration and
  protects the brittle sintered NdFeB bonding. The taper is functional, not cosmetic.

---

## Reference images

In [`cad/renders/`](cad/renders/). All are **Gen4** except `exploded_view.png`. Each carries a
drawn arrow showing which way the payload leaves.

| File | View | Use it for |
|---|---|---|
| `hero_open.png` | ISO, enclosure open, payload departing | Overall arrangement; how sled, track, stator and cassette sit together |
| `espa_interface.png` | ISO from the aft flange | The host interface, and that the payload departs **away** from it |
| `track_stator.png` | Side elevation | Proportion of track length to cassette height |
| `envelope_closed.png` | Side elevation, closed | The installed envelope and how little of it is machine |
| `sled_detail.png` | ISO, sled prominent | Sled proportions relative to the track |
| `magazine_feed.png` | Axial, looking down the bore | Cassette-to-breech transverse feed; the departure axis head-on |
| `exploded_view.png` | ISO, exploded (**Gen3**) | Part relationships and assembly order |

Also useful: `cad/step/gen3/` holds STEP exports of each document plus a monolithic
`EMOCD_Gen3.step` with all nine sub-systems (395 solids), and `cad/stl/` holds derived meshes
that GitHub renders in-browser. **`cad/step/gen3/` is the master geometry** of the last exported
generation; STL is derived from it.

---

## Where everything lives

| File | What it holds |
|---|---|
| [`cad/parameters.json`](cad/parameters.json) | **Single source of truth.** Every dimension, per document, with status and provenance per group |
| [`cad/DIMENSIONS.md`](cad/DIMENSIONS.md) | The same values as flat tables — **generated** from the above, never hand-edited |
| [`cad/BOM.md`](cad/BOM.md) | Parts, quantities, materials, masses — **generated** from `analysis/mass_properties.py` |
| [`cad/CHANGELOG_CAD.md`](cad/CHANGELOG_CAD.md) | Generation history, per-file inventories, defect IDs, cross-generation comparison |
| [`docs/GEN4_STATUS.md`](docs/GEN4_STATUS.md) | Why Gen4 exists, and why its export gate is closed |
| [`OPEN_PROBLEMS.md`](OPEN_PROBLEMS.md) | Every known defect, live and corrected. The CAD-relevant ones are P5, P8, P9, P10, P12, P37, P39, P43 |
| [`analysis/`](analysis/) | Authoritative for **mass and performance**. CAD is authoritative for **geometry and fit** |

**Do not edit dimensions inside Fusion.** User parameters there are document-scoped and will
silently drift across the nine documents. Change `parameters.json`, then regenerate.

---

## What a good model would add that the current one does not have

Stated plainly, because the gaps are the useful part of a brief:

1. **Stator end turns**, and the envelope growth in y that follows (conflict 6 above).
2. **Fillets, fasteners, harness routing and tolerancing.** None exist. The current CAD is a
   geometry and interface model, not a manufacturing model.
3. **Roller channel clearances**, currently implied by two dimension pairs rather than specified.
4. **A pocketed sled** — but only together with a re-run of `mass_properties.py` and
   `motor_model.py`, because the sled mass sets the exit velocity (conflict 7).
5. **Cassette classes other than 3U.** No cassette, cradle or gate exists for any other class;
   see [`docs/PAYLOAD_CLASSES.md`](docs/PAYLOAD_CLASSES.md).
