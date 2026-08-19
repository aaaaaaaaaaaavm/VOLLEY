# A55 — the dispersion and the trim authority, at the stroke ADR-034 actually adopted

**Bands declared 2026-08-19, before `analysis/trim_authority.py` existed.**
Verify with `git show --stat <this commit> -- analysis/trim_authority.py`, which must return nothing.

---

## Why this run exists

**[P83](../OPEN_PROBLEMS.md).** [A48](A48_trim_stage.md) sized a 39.7 mm stator carrying
**±0.323 m/s** against [A44](A44_gen6_dispersion.md)'s dispersion of **1.113 % at 3σ**, of which
**93.4 % was seal friction**. Both were computed over a **2.18 m** stroke.

**[ADR-034](../docs/adr/034-gen6-long-stroke-design-point.md) took the stroke to 8.0 m and tripled
the friction share** — 9.75 % → **28.39 %** of shot work, [A49](A49_design_surface.md) band 6,
recorded as **P78**. Friction scales with contact length while the work saturates.

**[P84](../OPEN_PROBLEMS.md) is why nobody noticed.** `gen6_dispersion.py` computes
`w_net = w - friction_N * pc.STROKE`, and `pc.STROKE` was still 2.18 m three days after the design
point moved. **A44 and A48 have been answering a superseded question**, and no gate caught it
because nothing compared the parameter file against the scripts. *That repair is committed before
this run so the numbers below are computed at the adopted point.*

## The question

**Does 39.7 mm of stator still cover ±3σ at the stroke that was adopted?**

And the one behind it, which is what makes this HIGH rather than bookkeeping: **ADR-033's first
falsifier is that the pulse store weighs more than the 0.340 kg section it feeds.** Pulse hardware
scales with current, not energy. **If the authority has to grow, the unweighed store grows with
it**, and the project's most likely falsifier becomes more likely.

## Method

**The dispersion model is `gen6_dispersion.py`'s, imported rather than restated**, with its
Monte-Carlo seed and its three variance terms unchanged: charge-pressure setting, payload mass, and
the seal friction that owns most of it. **The only thing that changes is the stroke and the charge
pressure**, both now read from `cad/parameters.json`.

**The trim geometry is `trim_stage.py`'s**, likewise imported: energy to correct, section length
at A2's depth-resolved thrust constant and A1's sheet current, and the mass of magnets and stator
per metre from `mass_properties.py`.

**What is added** is a sweep of the friction share, so the authority requirement is reported as a
*function* of the term nobody has measured rather than at a single assumed value. **P67 is the
measurement; this run says what it decides.**

## The prediction, recorded before the run

**Dispersion scales roughly with the friction share**, so I expect 3σ near **3 %** against A44's
1.113 %, and the required authority to land near **0.9 m/s** against the 0.323 m/s A48 sized —
about **2.8× short**. I expect the section length to grow by the same factor and the mass with it,
so **band 4 fails**.

**I expect band 6 to pass**: that even the grown section stays under a kilogram, so ADR-033
survives as a decision and what changes is its cost.

---

## Acceptance bands

**Declared before the script. Not to be edited after the run.**

| # | Band | FAIL if |
|---|---|---|
| **1** | At **2.18 m and 50 bar** the model reproduces A44's **1.113 % at 3σ** within 2 % relative | The model is not A44's and nothing below is comparable to it — the A38 band 1 lesson, applied deliberately |
| **2** | At the adopted point the friction term still owns **≥ 80 %** of the variance | The dispersion has changed character, and a run that only rescales A44 is the wrong instrument |
| **3** | 3σ dispersion at the adopted point is **≤ 2.0 %** | The open-loop spread more than doubles, and the commanded-velocity claim degrades faster than the stroke buys velocity |
| **4** | **A48's 39.7 mm section still covers ±3σ** at the adopted point | **P83 is confirmed: the trim stage is under-authority against the dispersion ADR-034 creates** |
| **5** | The section length required is **≤ 15 %** of the stroke — A48's own band 3 limit, unchanged | The correction stops being a trim and becomes a second drive |
| **6** | Added mass of the resized section is **≤ 1.0 kg** | ADR-033 stops being cheap, and the trade against a per-cell ejector has to be re-run |
| **7** | Added mass per satellite, **including the resized section**, stays **≤ 2.0 kg** | **The design re-crosses the one kill-criterion numerator Gen6 currently passes** |
| **8** | The correction energy stays **≤ 5 %** of the shot | The trim stage is doing a material share of the work, not correcting it |
| **9** | **REPORT, no pass/fail.** Required authority against friction share, swept, so P67's measurement can be read off it | — |

## What this run will not do

- **It does not re-run A44 or A48 in place.** Those are dated records of what was found at the
  point that was current then, and they are annotated rather than rewritten.
- **It does not weigh the pulse store.** That is **P77** and **A54**, still open, and it is
  ADR-033's actual falsifier. This run only says how much authority the store must feed.
- **It does not model the sensor.** A loop is only as good as what it measures and Gen6 has no
  velocity sensor in any file.
- **The friction coefficient is still A41's allowance, not a measurement.** **P67. E4 stands.**
