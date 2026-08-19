# A53 — the per-cell backup ejector, designed rather than priced

**Bands declared 2026-08-16, before `analysis/backup_ejector.py` existed.**
Verify with `git show --stat <this commit> -- analysis/backup_ejector.py`, which must return nothing.

---

## Why this run exists

**[A47](A47_gen6_fmea.md) found it is worth six times the entire architecture change.**

| Change | Satellites delivered at *r* = 0.99 | Gain |
|---|---:|---:|
| Gen5 → Gen6, an entire architecture | 6.620 → 6.992 | **+0.37** |
| **Gen6 → Gen6 with a per-cell ejector** | 6.992 → **9.261** | **+2.27** |

**Because it changes the structure rather than the count.** Deleting subsystems removes shared
elements one at a time; **a mechanism in every cell makes the drive satellite-forfeiting instead of
manifest-forfeiting**, which is the only move that touches what **E30** actually says.

**A47 priced its effect and did not design it.** Mass, volume, its own failure rate, and whether it
fits the cell the magazine already uses are all unknown — and **P75** says so. This run answers
those.

## What it is, and what it is not

**A small spring per cell, guaranteeing clearance if the drive is dead.** It does **not** deliver
the Δv the product is sold on. It converts *"the drive failed and we lost eight satellites"* into
*"the drive failed and eight satellites deployed with no benefit"*.

---

## Acceptance bands

**Declared before the script. Not to be edited after the run.**

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

*Not yet run.*
