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

## Result, 2026-08-10: **band 1 FAILS**, and the failure is the most useful thing here

`analysis/sensitivity_ranking.py`, bands committed at `03628da` before it existed. Results in
`analysis/results/sensitivity_ranking.json`. The harness reproduces the operating point exactly —
**v_exit 16.388 m/s, net efficiency 20.99 %, 6.375 kg per satellite** — which is the first check
that the sweep is driving the real pipeline and not a copy of it.

### Swing, over the full declared range

| Input | `v_exit` | Net efficiency | kg / satellite |
|---|---:|---:|---:|
| **Bank ESR** | 0.000 % | **23.240 %** | 0.000 % |
| **Packing efficiency** | 0.000 % | 0.000 % | **50.000 %** |
| **Magnet remanence** | **5.660 %** | 5.498 % | 0.000 % |
| Brake pole field | 0.000 % | 0.000 % | 0.000 % |
| Structural Q | 0.000 % | 0.000 % | 0.000 % |
| Fin emissivity | 0.000 % | 0.000 % | 0.000 % |
| Contact conductance | 0.000 % | 0.000 % | 0.000 % |
| Ballistic coefficient | 0.000 % | 0.000 % | 0.000 % |
| Magnet resistivity | 0.000 % | 0.000 % | 0.000 % |

### Elasticity, local, at ±5 %

| Input | `v_exit` | Net efficiency | kg / satellite |
|---|---:|---:|---:|
| Magnet remanence | **0.5028** | **0.4869** | 0.0000 |
| Packing efficiency | 0.0000 | 0.0000 | **−0.9091** |
| Bank ESR | 0.0000 | −0.0376 | 0.0000 |
| *all others* | 0.0000 | 0.0000 | 0.0000 |

### Band verdicts

| # | Band | Verdict |
|---|---|---|
| 1 | Leader agrees between swing and elasticity | **FAIL**, on net efficiency |
| 2 | Top three agree as a set | **PASS** |
| 3 | Declared no-path entries exactly zero | **PASS** — all exactly 0.000 |
| 4 | Largest `v_exit` swing ≥ 1 % | **PASS**, 5.660 % |
| 5 | Rank order unchanged with every range halved | **PASS** |
| 6 | Provenance of each leader | **REPORT** — see below |

### Band 1 failed exactly where it was written to

**Net efficiency has two different leaders depending on the metric.** Swing says **bank ESR**, at
23.24 % against magnet remanence's 5.50 %. Elasticity says **magnet remanence**, at 0.4869 against
bank ESR's −0.0376 — a factor of thirteen the other way.

Both are correct and they are measuring different things. **Bank ESR wins on swing because its
declared range is enormous** — 6 to 65 mΩ, a factor of eleven, because the nominal has no source
at all (E17) and the upper bound is A10's hard ceiling. **Magnet remanence wins on elasticity
because efficiency genuinely responds to it**, and its range is narrow only because a magnet grade
is a thing you can look up once someone specifies one.

The rule fixed in advance was: *publish both rankings side by side and state that the metric
choice changes the answer; do not pick the more convenient one.* Both tables are above.

**The engineering reading is the useful one.** Bank ESR is the top measurement priority for
efficiency **because nobody knows what it is**, not because efficiency is especially sensitive to
it. Magnet remanence is what efficiency actually responds to. Those are different reasons to
measure something and the ranking is worth more for keeping them apart than it would be for
collapsing them into one number.

### The result that was not expected: **`v_exit` does not respond to the bank at all**

Bank ESR was declared as having a path to `v_exit` — it is not in the no-path set — and its swing
is **exactly zero across the whole range to the ceiling**.

**This is real and the mechanism is clear.** `shot()` commands a sheet current, so the force is
`F_cmd = 0.9·K_t·K_RATED` and the acceleration is fixed; ESR changes how much energy the bank
gives up and how far it sags, not how hard the machine pushes. Exit velocity is
`sqrt(2·a·s)` and stays there **until the bank cannot source the demand at all**, at which point
`shot()` raises `BankLimitError` rather than degrading — which is **P27**'s fix doing its job.

So the bank's effect on exit velocity is not small. It is **nil, and then total.** A cliff, not a
slope. That is a more useful thing to know about **P26** than a sensitivity coefficient would have
been, and no amount of ranking would have shown it if the guard had still been silently
substituting a plausible current.

### Band 6: the leaders' provenance, and one of them is my own guess

| Output | Leader by swing | Range provenance | Unsourced? |
|---|---|---|---|
| `v_exit` | magnet remanence | assumed; **the CAD states no magnet grade** | **yes** |
| Net efficiency | bank ESR | nominal unsourced (E17); ceiling from A10 | **yes** |
| kg / satellite | packing efficiency | calibrated to the 3U layout | no |

**Two of the three leaders lead on ranges nobody sourced.** For `v_exit` the effect is direct:
the 5.66 % swing is a statement about a ±0.075 T interval that exists because no one has written
down which magnet this machine uses. Specifying the grade would collapse that range and could
move the leader. **This is reported, as the band required, and it qualifies the ranking rather
than voiding it** — the ordering is stable (band 5) and the zeros are real (band 3), so the
ranking stands, with its top two entries flagged as resting on intervals of my own construction.

### Two limitations, both found on the first run

**1. One-at-a-time sensitivity cannot see interactions, and there is a concrete one here.** Fin
emissivity returns **exactly zero on every output including its own binding quantity**, because
at the nominal contact conductance of 500 W/m²K the joint sinks the heat and radiation is
irrelevant. That is true at the nominal point and false as a general statement — at the bottom of
the conductance range the emissivity does matter:

| Contact conductance | Fin residual at ε = 0.05 | at ε = 0.90 |
|---:|---:|---:|
| 100 W/m²K | 0.1701 K | **0.0746 K** |
| 500 W/m²K | 0.0004 K | 0.0002 K |
| 5000 W/m²K | 0.0000 K | 0.0000 K |

**A19 sweeps one input at a time and reports zero for emissivity. A18 swept the two as a grid and
would have caught it.** The ranking above is a ranking *at the nominal point*, and where two
uncertain inputs gate each other it will understate the one that is currently masked. Recorded
here rather than left for a reader to find.

**2. Band 5 is only meaningfully tested on one output.** Rank stability under halved ranges is a
real test where the entries are non-zero: on net efficiency, bank ESR leads magnet remanence
**23.24 % to 5.50 %** at full range and **9.92 % to 2.76 %** at half, so the ordering is a
property of the physics and not of the interval width. On `v_exit` and kg per satellite only one
input is non-zero, so the second and third places are **ties among structural zeros broken by
list order**, and band 5 passing on those positions means nothing. The band passed; on two of
three outputs it passed vacuously, and saying so is the point.

### The binding outputs — what the seven "zero" inputs actually govern

Reporting a sensitivity of zero and stopping would be true and useless. Each input that has no
path to the ranked three drives something, and in two cases it drives a kill criterion.

| Input | Governs | Across its range |
|---|---|---|
| **Structural Q** | **gate margin of safety (P37)** | **+0.559 → −0.100** — passes at Q = 10, **negative at Q = 30** |
| **Brake pole field** | brake stopping distance (E20) | 0.345 m → 0.063 m, against a **0.210 m** arrest section |
| Ballistic coefficient | unboosted lifetime | 0.856 → 1.925 yr |
| Contact conductance | fin residual after 12 shots | 0.108 K → 0.000 K |
| Fin emissivity | fin residual after 12 shots | 0.000 K → 0.000 K — masked, see limitation 1 |
| Magnet resistivity | magnet eddy rise per shot | 0.003 K → 0.002 K |

**This column is where the measurement priority actually lives.** Structural Q moves a margin of
safety through zero and brake pole field moves a stopping distance across the length of the
section it has to stop in — both are pass/fail transitions inside their declared ranges, while
the three ranked outputs move by single-digit percentages. **The headline numbers are not what is
at risk from these assumptions. The design's viability is**, and a ranking that only looked at
`v_exit`, efficiency and kg per satellite would have reported six harmless zeros and missed both.

### What this says to do first

1. **Measure structural Q.** It is the only input on the list that moves a margin of safety
   through zero, and `docs/STRUCTURAL_GAP.md` already records four findings queueing behind it.
2. **Specify the magnet grade.** It is a look-up, not a measurement, and it collapses the
   interval behind the leader on `v_exit`.
3. **Source the bank ESR.** Its efficiency swing is the largest number in the whole analysis and
   it exists because the value has no provenance; and its effect on `v_exit` is a cliff, so the
   thing to establish is which side of it the hardware sits on.
4. **B-4 for the brake pole field**, which decides whether the brake fits the section at all.

**None of this is new precision.** Every input is exactly as unmeasured after this analysis as
before it. What has changed is the order to attack them in.

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
