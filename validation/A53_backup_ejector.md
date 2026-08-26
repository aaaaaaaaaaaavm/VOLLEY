# A53, the per-cell backup ejector, designed rather than priced

**Bands declared 2026-08-16, before `analysis/backup_ejector.py` existed.**
Verify with `git show --stat <this commit> -- analysis/backup_ejector.py`, which must return nothing.

---

## Why this run exists

[A47](A47_gen6_fmea.md) found it is worth six times the entire architecture change.

| Change | Satellites delivered at *r* = 0.99 | Gain |
|---|---:|---:|
| Gen5 → Gen6, an entire architecture | 6.620 → 6.992 | **+0.37** |
| **Gen6 → Gen6 with a per-cell ejector** | 6.992 → **9.261** | **+2.27** |

Because it changes the structure rather than the count. Deleting subsystems removes shared
elements one at a time; a mechanism in every cell makes the drive satellite-forfeiting instead of
manifest-forfeiting, which is the only move that touches what E30 actually says.

A47 priced its effect and did not design it. Mass, volume, its own failure rate, and whether it
fits the cell the magazine already uses are all unknown, and P75 says so. This run answers
those.

## What it is, and what it is not

A small spring per cell, guaranteeing clearance if the drive is dead. It does not deliver
the Δv the product is sold on. It converts *"the drive failed and we lost eight satellites"* into
*"the drive failed and eight satellites deployed with no benefit"*.

---

## Acceptance bands

Declared before the script. Not to be edited after the run.

| # | Band | FAIL if |
|---|---|---|
| **1** | Ejector mass per cell at **1.5 m/s** on a 4 kg payload is **≤ 0.25 kg**, using `actuator_trade.py`'s spring energy density | Twelve of them cost more than the reliability they buy |
| **2** | Twelve ejectors add **≤ 3.0 kg**, keeping added mass per satellite **≤ 2.0 kg** | It re-crosses the numerator Gen6 currently passes, which is what A47's +2.27 was bought against |
| **3** | The ejector fits **inside the existing cell envelope** — `magazine.satellite_pitch_z` unchanged | It is not a per-cell addition, it is a magazine redesign |
| **4** | Its stored energy is **≤ 2 %** of the gas shot's | A spring big enough to matter is a second drive, which is **PII-20** and was declined |
| **5** | Re-running A47's model with the **designed** mass confirms delivery **≥ 9.0** satellites at *r* = 0.99 | The design erodes the benefit the design exists for |
| **6** | The ejector's **own failure rate is included** as a shot-scope element, not assumed perfect | The gain is an artefact of giving the new part infinite reliability |
| **7** | Exit velocity if the ejector fires alone is **≥ 1.0 m/s**, clearing the tube | It does not achieve the one thing it is for |
| **8** | The **standby problem is stated**: a spring held compressed from integration to the last shot | A39 recorded exactly this against the gas option and it applies here too |

## Predictions

1. **Band 1 passes.** 4.5 J at `actuator_trade.py`'s 300 J/kg is grams, not hundreds of grams —
   the mass will be in the latch and the guide, not the spring.
2. **Band 4 passes trivially**: 4.5 J against 1864.8 is 0.24 %.
3. **Band 6 is the one that could bite.** Twelve new mechanisms are twelve new things to fail, and
   if each is unreliable the parallel gain erodes. I expect it to survive because a shot-scope
   failure costs one satellite rather than the manifest.
4. **Band 5 passes**, landing near A47's 9.261 rather than well below it.

## Result

**RUN 2026-08-16. Seven of eight bands pass. Band 7 fails by a factor of forty, and it takes the
highest-value reliability change in the record with it.

| # | Band | Result | |
|---|---|---|---|
| 1 | ≤ 0.25 kg per cell | 0.135 kg | **PASS** |
| 2 | ≤ 3.0 kg total, ≤ 2.0 kg/sat | 1.620 kg, 1.538 | **PASS** |
| 3 | fits the 104 mm cell pitch | 60 mm | **PASS** |
| 4 | ≤ 2 % of the gas shot | 0.241 % | **PASS** |
| 5 | A47 re-run gives ≥ 9.0 satellites | 9.261 | **PASS** |
| 6 | its own failure rate included | included | **PASS** |
| 7 | **firing alone clears the tube** | **needs 181.8 J, has 4.5 J** | **FAIL** |
| 8 | standby problem stated | stated | **PASS** |

### The ejector cannot get the payload out of the tube

A spring sized for a clean 1.5 m/s departure stores 4.5 J. Pushing the payload the length of a
2.18 m sealed tube against A41's friction allowance costs 181.8 J. A shortfall of 40.4x.

A47 priced a mechanism in the abstract. In Gen6 the payload is not sitting in an open cell, it
is in a tube, with a piston behind it, and if the drive is dead something has to move both.

Sizing the spring to actually clear the tube costs the mass argument:

| | Per cell | × 12 | Added per satellite |
|---|---:|---:|---:|
| Clearance only *(cannot clear the tube)* | 0.135 kg | 1.620 kg | **1.538 kg** |
| **Clearing the tube** | **0.726 kg** | **8.713 kg** | **2.129 kg — crosses** |

So the change A47 valued at +2.27 satellites either does not work, or it re-crosses the one
kill-criterion numerator Gen6 currently passes. Recorded as P81.

### And P67 decides this too, which is now the fourth thing it decides

The 181.8 J is A41's friction *allowance* over the full stroke, the pessimistic reading, and
[P67](../OPEN_PROBLEMS.md) has never measured the real value. At a genuinely small friction the
clearing energy collapses and the light ejector works.

One bench test now governs four open decisions: this ejector, [A49](A49_design_surface.md)'s
long-stroke design point, [ADR-033](../docs/adr/033-gen6-trim-stage.md)'s trim stage, and
P77's pulse store. Nothing else in this project has that reach.

### What survives

**Bands 1 to 6 all pass**, so the *concept* is sound wherever the payload does not have to
traverse a sealed tube, a Gen5-style open cell, or a Gen6 variant that vents the tube and
disengages the piston. The failure is architectural, not conceptual, and that distinction is
the deliverable.

## What this run does not do

- The latch and guide mass is a declared guess of 0.12 kg per cell with no derivation, and it
  is the largest assumption here, the spring itself is 15 g.
- It does not design a venting or piston-disengage mechanism, which is the obvious escape and
  is unpriced.
- Spring energy density is `actuator_trade.py`'s upper end for spring steel, which flatters it.
- The standby problem stands: a spring held compressed from integration to the last shot, which
  is the same class of objection A39 recorded against the gas option.
