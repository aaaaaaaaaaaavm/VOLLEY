# Do the Phase II items combine?

**Written 2026-08-13.** `analysis/architecture_synthesis.py`,
`analysis/results/architecture_synthesis.json`. **Sketch, not validation** — no band is declared
for anything here, and the mass figures are a scaling argument over `mass_properties.py`'s own
lumps rather than a re-run of the rollup.

[`VAULT.md`](VAULT.md) holds eighteen deferred items, each sized on its own. **Nothing had
ever asked whether they interact.** Two of them turn out to be *alternatives* rather than
complements — and that is only visible once **PII-18** puts a 0.6 kg shuttle where a 9.445 kg
sled used to be.

---

## 1. PII-1 is superseded, and the reason is arithmetic

**PII-1 is the project's self-declared strongest idea**: a momentum-conserving spring at release
recovers the whole velocity shortfall for **41.8 J against a 2881 J shot**.

Conserving momentum and adding energy *E* between mover *M* and satellite *m*:

$$\Delta v = \sqrt{\frac{2EM}{m(M+m)}}$$

**The mover's mass is the lever.**

| Mover | M | Δv from 41.8 J | Energy for the original 3.83 m/s |
|---|---:|---:|---:|
| Gen5 sled — what PII-1 was sized on | 9.445 kg | **3.83 m/s** | 42 J |
| PII-18 shuttle + pusher + latch | 0.600 kg | **1.65 m/s** | **225 J** |
| PII-18 bare plate | 0.398 kg | 1.38 m/s | 324 J |

**On a light shuttle the lever collapses.** Matching the original kick costs five times the
energy, for a cocked spring that must reset twelve times and be safed through the three-inhibit
chain.

**And it is not needed.** PII-18 reaches 20.26 m/s at 0.60 T by *not putting the energy into a
sled in the first place*. Two routes to the same exit velocity: one adds a mechanism to the
release path, the other adds nothing. **PII-1's own entry says its reason for being deferred is
that "it adds a mechanism to the release path, the one place ADR-008 deliberately removed
complexity."** That objection never goes away; the alternative removed the need for it.

---

## 2. PII-15 is superseded by qualification margin nobody is spending

**Gen5 runs at 10.1 g of a 25 g payload budget.** That was never a choice. It is where thrust
over mass landed with a 9.445 kg sled aboard.

| Target | a | Acceleration zone | vs 1.30 m |
|---:|---:|---:|---:|
| 16.39 m/s | 10.1 g | 1300 mm | 1.00× |
| 16.39 m/s | **16.1 g** | **850 mm** | **0.65×** |
| 16.39 m/s | 21.6 g | 634 mm | 0.49× |
| 20.00 m/s | 21.6 g | 944 mm | 0.73× |

**PII-15's 2:1 reeving was recorded as "the only lever found that shortens the machine without
lengthening anything else", 1.30 m → 0.65 m.** The margin does the same thing, for free, and
**without a cable over a sheave** — which `REV-07` records cannot claim the exemption that
screened out the rack: fretting, cold welding, lubricant with no outgassing budget, sheave
bearing life, and a single tension load path that becomes another manifest-forfeiting element
for **E30**.

**Cheaper, and it removes a failure mode instead of adding one.**

---

## 3. Together they close kill criterion 2

The brake run-out falls **240 → 105 mm**, because arresting 0.6 kg at 200 g needs 1177 N over a
tenth of a metre where arresting 9.445 kg needed the whole downstream section.

| Configuration | Stroke | **Closed envelope** | |
|---|---:|---:|---|
| Gen5 today | 1300 mm | **1839 mm** | **45 % over ESPA-Grande** |
| Gen5 velocity at 16.1 g | 850 mm | **1254 mm** | **FITS** |
| Gen5 velocity at 21.6 g | 634 mm | **1037 mm** | **FITS** |
| 20 m/s at 21.6 g | 944 mm | 1347 mm | 6 % over |

**Kill criterion 2 has been crossed or unevaluable since the envelope was first drawn.** It was
44 % over against ESPA-Grande; [ADR-023](adr/023-target-host-class.md) re-scoped the target host
rather than fix it, and `KILL_CRITERIA.md` records that honestly as *"a worse epistemic position
than a clean fail against a published number"* — a measured failure converted into an
unmeasurable unknown.

**At 1254 mm it fits, at Gen5's own exit velocity, with 3.9 g of qualification margin still
unspent.** That would let ADR-023's re-scope be reversed on evidence rather than defended.

**The conservative row is the one to design to.** 21.6 g leaves only 14 % of the payload
qualification budget, and `PAYLOAD_ENVIRONMENT.md` does not promise every payload is qualified to
25 g. 16.1 g fits the envelope and keeps 36 % in hand.

---

## 4. What it does to mass — a sketch, and labelled as one

Scaling `mass_properties.py`'s own lumps to an 850 mm machine with a 0.6 kg shuttle: sled gone,
brake down 75 %, track/stator/formers scaled with length, bank down 45 % on halved shot energy,
**plus 3 kg of iron the LIM stator needs and 0.6 kg of shuttle**.

| | |
|---|---:|
| Net | **−16.9 kg** |
| Dry mass | 76.5 → **59.6 kg** |
| Per 3U satellite | 6.378 → **4.967 kg** |
| Against the ~2 kg threshold | **still crossed**, by 2.5× instead of 3.2× |
| **Per PocketQube 1P**, 288 per load (A24) | **0.207 kg — passes by 10×** |

**Kill criterion 1 does not close at 3U and no version of this architecture makes it.** What
changes is that it closes *more comfortably* at the small classes — and those are reachable now,
because **PII-18 leaves the satellite unmodified**, so a PocketQube rides a carrier that *is* the
shuttle rather than needing a plate of its own.

---

## What the combination actually is

| | |
|---|---|
| **Drive** | Linear induction, iron-cored segmented stator, passive aluminium secondary |
| **Mover** | **PII-18** — twin aluminium fins straddling the satellite, ~0.6 kg, reusable, arrested and returned |
| **Satellite** | **Unmodified.** No plate, no consumable, no interface to publish, no magnets anywhere near it |
| **Stroke** | 850 mm at 16.1 g — spending margin Gen5 leaves idle |
| **Envelope** | ~1254 mm, **inside ESPA-Grande** |
| **Arrest** | 82–123 J, 105 mm, against Gen5's 1938 J and 18.5 kN |
| **Energy** | roughly half Gen5's per shot, so **PII-7** eases and **A25**'s flywheel gets easier |
| **Superseded** | **PII-1** (lever collapses), **PII-15** (margin does it cheaper), **PII-13** (the shoe *is* the shuttle) |
| **Reinforced** | **PII-3** two-layer stator, which is how the 0.60–0.75 T A31 needs gets produced |

**Register items this would dissolve rather than solve:** E34 (no 18.5 kN arrest), E33 and E35
(no permanent magnets), P28 (no oversubscribed arrest section), most of E24 (the return stroke is
1/24 the mass), and **decision D2** (every payload class works, because nothing is asked of the
satellite).

**What it does not touch:** **E4** — nothing measured. **P52** — the 30 % segment-handover ripple
through a 48 Hz track mode is topology-level and applies to every variant on this page. **P36** —
the track still has no dynamic design case, and a shorter, stiffer track changes its modes, so
that analysis has to be redone rather than inherited.

---

## What this page is not

**It is not a promotion.** [`VAULT.md`](VAULT.md)'s gate is explicit: items are reviewed
only at baseline boundaries, and *"an item may not be promoted by finding it interesting. It is
promoted by meeting the criterion it was given."* PII-1 and PII-15 are recorded here as
**superseded if PII-18 is promoted** — which is a finding about their interaction, not a decision
about their status.

**It is not sized.** Nine measured bands stand behind PII-18's plate (A30 band 4/5, A31 bands
1–4, A32 bands 1–2). **Zero stand behind the twin-fin geometry, the retention, the release, the
850 mm stroke or the 3 kg of stator iron.** Every number on this page above the band line is
arithmetic over committed values; every number below it is a sketch.
