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

---

## Result

**RUN 2026-08-19. Four of nine bands pass. P83 is confirmed and it is worse than predicted, but
the falsifier it was expected to feed turns out not to move.**

| # | Band | Result | |
|---|---|---|---|
| 1 | reproduces A44's 1.113 % within 2 % | **1.1133 %** | **PASS** |
| 2 | friction owns ≥ 80 % of the variance | **98.68 %** | **PASS** |
| **3** | 3σ at the adopted point ≤ 2.0 % | **3.9798 %** | **FAIL, 2.0×** |
| **4** | A48's 0.323 m/s covers ±3σ | **needs 1.1543 m/s** | **FAIL, 3.57×** |
| 5 | section ≤ 15 % of the stroke | **1.80 %** | **PASS** |
| **6** | resized section ≤ 1.0 kg | **1.2328 kg** | **FAIL** |
| 7 | added mass per satellite ≤ 2.0 kg | **1.3987 kg** | **PASS** |
| **8** | correction energy ≤ 5 % of the shot | **5.81 %** | **FAIL** |
| 9 | authority against friction share | 7 points, **0.373 → 3.260 m/s** | **REPORT** |

**Band 1 reproduced A44 to four decimal places** — 1.1133 % against its stored 1.11334669 %, and
the seal's variance share at **93.4 %** against A44's reported 93.4 %. *The two runs are the same
model at two points, which is what band 1 exists to establish.*

> ### Band 1 caught a bug in this script before it caught anything about the design
>
> **The first run returned 1.2353 % and failed band 1 by 11 %.** The cause was in
> `trim_authority.py`, not in A44: `gen6_dispersion.py` references the transducer's full scale to
> **a fixed 50 bar**, and this script had written **200 bar**, the storage pressure. That made the
> pressure noise four times too large.
>
> **The band was not widened. The script was fixed and the run repeated.** This is the fourth time
> in this project that a band declared beforehand has found a defect in the analysis rather than in
> the design.

### What ADR-034's stroke did to the open-loop shot

| | A44's point, 2.18 m at 50 bar | **Adopted, 8.0 m at 22.73 bar** | |
|---|---:|---:|---|
| Exit velocity | 29.008 m/s | **29.005 m/s** | held, by construction |
| **3σ dispersion** | 0.3230 m/s, **1.113 %** | **1.1543 m/s, 3.980 %** | **3.57×** |
| Friction work | 181.8 J | **667.2 J** | 3.67× |
| Friction share of shot work | 9.75 % | **28.39 %** | 2.91× |
| **Variance owned by the seal** | 93.4 % | **98.68 %** | **it now owns almost all of it** |

**The dispersion tracks the friction work almost exactly** — 3.57× against 3.67× — which is the
mechanism stated plainly: a constant Coulomb force acting over a longer stroke removes more work,
and its ±20 % uncertainty removes a proportionally larger uncertainty with it.

**Every other error term has been squeezed out.** At 98.68 %, the transducer and the payload mass
together account for 1.3 % of the variance. **There is now effectively one error source in this
machine, and it is the one that has never been measured.**

### The trim stage, resized

| | A48 as built | **A55, resized** | |
|---|---:|---:|---|
| Authority | 0.323 m/s | **1.1543 m/s** | **3.57×** |
| Section length | 39.7 mm | **144.0 mm** | 3.63× |
| As a fraction of the stroke | 1.822 % | **1.800 %** | *unchanged* |
| Correction energy | 37.7 J | **136.6 J** | 3.62× |
| As a fraction of the shot | 2.02 % | **5.81 %** | **band 8 fails** |
| **Section mass** | **0.340 kg** | **1.2328 kg** | **3.63×** |
| Added mass per satellite | 1.431 kg | **1.3987 kg** | *lower, on ADR-034's smaller base* |

**Band 7 is the one that matters and it holds.** The resized section costs 0.103 kg per satellite
against ADR-034's 1.296 kg base, so **1.3987 kg against an unmoved 2.0 kg threshold.** The design
does not re-cross the one kill-criterion numerator Gen6 passes.

> ### The falsifier this was expected to feed does not move
>
> **ADR-033 falsifier 1 is that the pulse store weighs more than the section it feeds**, and the
> ADR's own reasoning is that *"pulse hardware scales with current, not energy."*
>
> **The current does not change.** Peak power goes from **27 820 W to 28 606 W — 2.8 %** — because
> the force per metre is fixed by A2's thrust constant and A1's sheet current, and the exit
> velocity is held. **The section gets longer, not harder to drive.**
>
> **So the energy the store must deliver grows 3.6× while the peak current it must switch is
> essentially unchanged.** By ADR-033's own scaling argument, that is the cheaper of the two ways
> to grow. **P77 is not made worse by this run**, which is the opposite of what was predicted.

### The prediction, and where it was wrong

**Recorded before the run: 3σ near 3 %, authority near 0.9 m/s, about 2.8× short, band 4 failing
and band 6 passing.**

**Direction right, magnitude understated, and band 6 went the other way.** 3σ came in at 3.98 %
rather than 3 %, the authority at 1.154 m/s rather than 0.9, the shortfall at 3.57× rather than
2.8×, and **band 6 failed** — the resized section is 1.2328 kg, not under the kilogram predicted.

### Band 9 — what P67's measurement decides, read off directly

| Friction share of shot work | Force | 3σ | Authority needed | Section | Section mass |
|---:|---:|---:|---:|---:|---:|
| 9.75 % *(A44's share)* | 28.6 N | 1.146 % | 0.373 m/s | 51.5 mm | 0.441 kg |
| 15 % | 44.1 N | 1.805 % | 0.571 m/s | 76.7 mm | 0.657 kg |
| 20 % | 58.8 N | 2.528 % | 0.775 m/s | 101.5 mm | 0.869 kg |
| **28.39 %** *(A41's allowance)* | **83.4 N** | **3.980 %** | **1.154 m/s** | **144.0 mm** | **1.233 kg** |
| 35 % | 102.8 N | 5.394 % | 1.491 m/s | 178.4 mm | 1.527 kg |
| 45 % | 132.2 N | 8.190 % | 2.081 m/s | 232.2 mm | 1.987 kg |
| 60 % | 176.3 N | 15.058 % | 3.260 m/s | 320.1 mm | 2.740 kg |

**Band 6's 1.0 kg limit is crossed somewhere between a 20 % and a 28 % friction share.** A bench
measurement below about **22 %** keeps the trim stage under a kilogram; above **45 %** the section
alone exceeds the 2.0 kg per-satellite threshold.

**Note the first row.** Even at A44's own friction share, the 8.0 m stroke needs **0.373 m/s**
against A48's 0.323 — so **A48's section was marginal at the old stroke and is short at the new
one for two separate reasons**, only one of which is friction.

## Consequences

- **[ADR-033](../docs/adr/033-gen6-trim-stage.md) is amended, not reversed.** The decision stands;
  the section is **144.0 mm at x = 7856.0**, not 39.7 mm at x = 7960.3.
- **[ADR-034](../docs/adr/034-gen6-long-stroke-design-point.md) does not move.** Band 7 holds and
  no kill-criterion numerator changes. The stroke is not what needs re-selecting.
- **P83 closes as confirmed.** The stage was under-authority by 3.57×, which is what it alleged.
- **P77 stands and is not aggravated**, on the peak-current argument above.
- **P67 now sets a section length as well as a dispersion**, and band 9 is the table to read it against.

## What this run did not settle

- **It does not weigh the pulse store.** That is **A54**, and it remains ADR-033's actual falsifier.
- **There is still no velocity sensor in any file.** A loop is only as good as what it measures,
  and the 1.4 ms available to measure in has not moved.
- **The friction is still A41's allowance, not a measurement.** **P67. E4 stands.**
