# A19: which assumed inputs actually move the answer, and which only look like they do

**Closes:** nothing. **Ranks** the assumptions behind P29, P28, `docs/STRUCTURAL_GAP.md` and the
A18 sweep set, so that the measurement programme can be ordered by leverage rather than by
whichever number is most argued about.

> ## BANDS DECLARED 2026-08-10, BEFORE `analysis/sensitivity_ranking.py` EXISTS.
>
> Everything below the "Acceptance bands" heading is committed before the script is written.
> This is the last item in Phase I where that rule applies, and it applies here in an unusual
> form: **the bands are about rank stability, not about a pass/fail value.** A sensitivity
> ranking has no correct answer to be checked against. What it can be checked against is whether
> the ranking it produces is a property of the physics or an artefact of how the sweeps were
> drawn — and that is falsifiable.

---

## What this is, and the thing it must not be mistaken for

**It ranks assumptions. It does not make any of them less assumed.**

This project has a Monte Carlo, and it measures **dispersion** — how much `v_exit` scatters given
sensor noise, from `closed_loop_mc()`. Nothing anywhere ranks the *assumed inputs* by how much
they move the answer. Those are different questions: dispersion asks how precisely the machine
repeats, sensitivity asks which of the numbers nobody has measured would change the result if it
turned out to be wrong.

**The output is a measurement priority list.** It says what to measure first. It does not
narrow a single interval, it does not convert an assumption into a result, and it must not be
read as new precision. Every input here is unmeasured **before** this analysis and unmeasured
**after** it — E4 is unaffected, and so is every band that any of these inputs feeds.

**The honest failure mode of this analysis is that it reads as more than it is.** A ranked table
with percentages in it looks like knowledge. It is a statement about a model's derivatives with
respect to quantities whose ranges are themselves assumed, which is why band 5 and band 6 below
exist and why band 6 is allowed to void the whole thing.

---

## The inputs, their ranges, and where each range comes from

**Nine, not eight.** Magnet remanence `BR` is added to the eight this analysis was scoped
around, because it is the one input with a direct path to `v_exit` through K<sub>t</sub>, and a
ranking of what moves exit velocity that omits the magnets would be answering a different
question. It is declared here, before the run, rather than added afterwards.

| # | Input | Nominal | Range | Where the range comes from |
|---|---|---:|---|---|
| 1 | **Magnet remanence** `BR` | 1.32 T | 1.25 – 1.40 T | Grade spread and thermal drift for a sintered NdFeB class. **The CAD does not state a grade.** Assumed |
| 2 | **Brake pole field** `B_POLE` | 0.50 T | 0.30 – 0.70 T | A18's own declared sweep. **Nothing in the CAD states this field**; B-4 is the only test that would bound it |
| 3 | **Structural Q** | 20 | 10 – 30 | A18's `Q_SWEEP`. Bolted aluminium. **Never specified or measured** — `docs/STRUCTURAL_GAP.md` |
| 4 | **Fin emissivity** | 0.50 | 0.05 – 0.90 | A18's `EPS_SWEEP`: bare copper to a treated surface. Surface finish is not specified |
| 5 | **Contact conductance** | 500 W/m²K | 100 – 5000 | A18's `H_SWEEP`. Joint-dependent, two orders of magnitude wide, and unspecified |
| 6 | **Bank ESR** | 12 mΩ | 6 – 65 mΩ | Nominal has **no current source** (E17); upper bound is A10's hard ceiling. P26 records a real single string at 116–185 mΩ, i.e. past the top of this range |
| 7 | **Ballistic coefficient** | 61 kg/m² | 40 – 90 | A5's declared sweep |
| 8 | **Packing efficiency** | 0.562 | 0.40 – 0.60 | Calibrated so the 3U case returns the twelve the machine is laid out for; the 40–60 % band is the original hedge it replaced |
| 9 | **Magnet resistivity** | 1.4 µΩ·m | 1.2 – 1.6 | Sintered NdFeB class range. Grade unstated, as in #1 |

**Six of these nine ranges have no source better than "assumed" or "a previous sweep of mine".**
That is recorded here, in advance, because it is the fact band 6 tests.

## The outputs

| Output | Source | Why it is here |
|---|---|---|
| **`v_exit`** | `motor_results.shot.v_exit` | The headline number. 16.388 m/s |
| **Net efficiency** | `motor_results.eff_net_pct` | 20.99 %, net of regeneration |
| **kg per satellite** | `payload_family.kg_per_satellite` | 6.375 kg — the quantity kill criterion 1 is crossed on |

**A fourth column is reported and not ranked: the binding output.** Several of these inputs have
**no path at all** to any of the three above, and drive a kill criterion or a numbered defect
instead. Reporting a sensitivity of zero and stopping would be true and useless, so each input
also names the quantity it actually governs.

## Method

For each input *i* and output *y*, with the input at its nominal *x₀* and range [lo, hi]:

- **Swing** = (y<sub>max</sub> − y<sub>min</sub>) / y(x₀) over {lo, x₀, hi} — a **global**
  measure, and the primary ranking key.
- **Elasticity** = (∂y/y) / (∂x/x) at x₀, by central difference at ±5 % — a **local** measure,
  independent of how wide the range was drawn.

Ranking by a global measure alone confounds "this input matters" with "I drew a wide range for
this input". Ranking by a local measure alone misses saturation and thresholds. **Reporting both
is the point**, and band 1 and band 2 are the check that they agree.

---

## Acceptance bands

Declared before the script exists. Each is capable of failing.

| # | Question | Band | What a miss means |
|---|---|---|---|
| 1 | **Top-ranked input for each output**, swing versus elasticity | **the same input under both** | the ranking depends on which metric was chosen, so no single ranking can be published and the analysis reports two |
| 2 | **Top three for each output**, as a set, order free | **the same set under both** | as band 1 but weaker; a miss here and a pass on band 1 means the tail is metric-dependent and only the leader is safe to quote |
| 3 | **Inputs with no model path to an output** | **exactly 0.000, not merely small** | a non-zero result means either an undeclared coupling in the model or a bug in the sweep. **Suspect the script before believing the coupling** |
| 4 | **The largest swing on `v_exit`** | **≥ 1 %** | if nothing moves exit velocity by 1 % across every range in the table, the ranges are too narrow to inform anything and the analysis is not worth publishing |
| 5 | **Rank order with every range halved** | **unchanged, for the top three of each output** | **the band that carries the whole analysis.** If halving the ranges reorders the ranking, the ranking is an artefact of how wide I drew the intervals rather than a property of the machine, and it must be published as such or not at all |
| 6 | **Provenance of the top-ranked input's range** | **report**; VOID-able as a measurement priority | if the leader's range is itself unsourced, the ranking is partly a statement about my own guess, and saying so is mandatory rather than optional |

### Band 5 is the one to watch, and band 3 is the one most likely to catch a bug

**Band 5** is the difference between a result and a rhetorical device. Every input here is swept
across a range I chose. If the ordering survives halving every range it is telling me something
about the machine; if it does not, it is telling me about my own priors, and the correct
publication is "this cannot be ranked".

**Band 3** is a self-check, and it is written because this analysis is unusually easy to get
silently wrong. Sweeping an input the model does not read produces a clean, plausible zero;
sweeping one through the wrong module produces a clean, plausible **non**-zero. The declared-zero
entries are known in advance from the module structure — brake pole field, structural Q, fin
emissivity, contact conductance and magnet resistivity have no path to `v_exit`, and none of the
electromagnetic or thermal inputs has a path to kg per satellite, which depends only on deployer
dry mass and packing. If any of those returns non-zero, the script is wrong.

**Band 4 is capable of failing and the failure would be informative**, not embarrassing: it would
say the headline number is robust to everything on this list, which is itself the answer to
"what should I measure to protect `v_exit`".

## What happens at each outcome, fixed now

1. **Band 1 or 2 fails.** Publish both rankings side by side and state that the metric choice
   changes the answer. Do not pick the more convenient one.
2. **Band 3 fails.** Stop. The script is wrong, or the model has a coupling that is not declared
   anywhere, and either way nothing else in this sheet can be trusted until it is found.
3. **Band 4 fails.** Report the ranking as a null result for `v_exit`: nothing on this list
   threatens the headline number across its plausible range, and the measurement priority is set
   entirely by the other two outputs and by the binding-output column.
4. **Band 5 fails.** The ranking is range-dependent. It is published as an ordering *conditional
   on the declared ranges*, with the conditionality in the heading rather than in a footnote, and
   it may not be used to order the measurement programme.
5. **Band 6 returns VOID.** The leader is named, and the sentence "this ranking's top entry rests
   on a range with no source" is published with it.

**No band may be widened after the run.** A miss produces a numbered defect or a stated
limitation, not a revised target.

## Provenance

Inputs are read from the modules that own them — `motor_model` for `BR`, `R_ESR`;
`phase1_closeout` for the brake, thermal and structural sweeps; `astro` for the ballistic
coefficient; `payload_family` for packing — by import and monkey-patch of the module constant,
never by restating the value in the sweep script. Where a range comes from a previous run sheet
it is cited to that sheet rather than re-derived.

**Nothing here is measured.** This is a sensitivity analysis of a model against assumptions, and
its own inputs are the assumptions. E4 stands.
