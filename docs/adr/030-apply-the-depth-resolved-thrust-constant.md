# ADR-030: apply the depth-resolved K<sub>t</sub>, and take the three decisions beside it

**Status:** Accepted · **Date:** 2026-08-13 · **Phase:** I · **Moves the baseline** · **Closes:** P46, P28, P10, P32

## Context

Four decisions had been open long enough that not-deciding had become the decision. Each was
deferred for a defensible reason and each was deferring an unflattering number.

**P46 — the thrust constant is a centre-plane value.** `motor_model.thrust_constant()` sampled
`B_y` on the plane z = 0 and multiplied by the full 90 mm depth as though that value held across
it. It does not; the field falls off toward the array's z-edges. **A2 measured the cost at
4.42 %** on 2026-08-10 and the correction was **computed and held** rather than applied, because
moving a frozen baseline value is not a validation's decision to take on its own.

**P28 — the arrest section is oversubscribed.** 240 mm of regenerative stator plus a 300 mm eddy
fin against a 339 mm section, both in the same airgap.

**P10 — packaging mass is absent from the rollup.** Enclosure, radiator and packaged avionics
were in no lump, so 76.5 kg was a floor rather than an estimate — and kill criterion 1 was
computed from it anyway.

**P32 — Gen4 has no corresponding operating point.** It exists only inside Fusion, has never been
exported, and releases at s = 1200 mm over a 900 mm stroke where `analysis/` assumes 1500 mm over
1.3 m.

## Decision

**All four are taken. The baseline moves.**

### 1. The thrust integral is depth-resolved

`thrust_constant()` now Gauss-Legendre averages `B_y` over z ∈ [−45, +45] mm before the Lorentz
sum. **This is a change to the physics, not a pasted factor** — ADR-015's rule. Setting `nz = 1`
reproduces the superseded centre-plane value exactly, so A2's ratio stays checkable.

| | Was | Is |
|---|---:|---:|
| K<sub>t</sub>, N per kA/m | 11.0258 | **10.5386** |
| Ratio | — | **0.9558**, exactly A2 band 2's measurement |
| Exit velocity, 3U | 16.388 m/s | **16.029 m/s** |

### 2. The regenerative section shortens to 39 mm

Three branches were priced. **Keeping both and lengthening the section** puts the envelope at
~1940 mm, worsening the one kill criterion that cannot currently be evaluated at all. **Dropping
regen entirely** costs 2 points of efficiency — which is in no kill criterion — and raises brake
duty **24 %**, which makes **E34**, fourth on the lethality ranking, worse. **Shortening regen to
fit** is adopted.

> **That recommendation was made and withdrawn inside an hour.** Dropping regen was proposed
> first and the composite showed why it was wrong: trading efficiency to worsen a top-five
> lethality item is the wrong direction, and the coupling was not checked before recommending.

### 3. Packaging enters the rollup as a labelled placeholder

**8.0 kg, with no derivation behind it, and the lump says so in its own name.** A number carrying
a caveat is auditable; a hole is not. `KILL_CRITERIA.md` already flagged a plausible 20 kg, so
8 kg is the lean end and deliberately the less flattering choice to leave un-taken.

### 4. Gen4 is retired

Gen5 is generated from `cad/parameters.json` and `build_gen5.py --check` reads 23 dimensions back
out of it. **A geometry that cannot be exported, cannot be checked, and does not match the
parameters is not a generation this project has.** The renders remain as the only visual record
and are labelled historical where they appear.

## The coupled consequence nobody had priced

**Applying P46 dropped the open-loop ceiling below the fleet setpoint.** 16.2 m/s against a new
ceiling of 16.029 is **101.07 % of it** — the exact condition [ADR-014](014-fleet-setpoint-below-ceiling.md)
exists to forbid, because a setpoint the machine cannot reach makes the dispersion figure a
measure of shortfall rather than of sensing noise.

**`V_FLEET` moves 16.2 → 15.8 m/s**, holding ADR-014's *fraction* rather than its number: 98.57 %
of the new ceiling against the 98.85 % it held before. **The rule survived contact with the
correction, which is what a rule is for.**

## What moved, and what it invalidates

| | Published | Now | |
|---|---:|---:|---:|
| K<sub>t</sub>, N per kA/m | 11.026 | 10.539 | −4.4 % |
| Exit velocity, m/s | 16.388 | **16.029** | −2.2 % |
| Fleet setpoint, m/s | 16.2 | **15.8** | −2.5 % |
| Acceleration, g | 10.53 | 10.07 | −4.4 % |
| Pulse, ms | 158.6 | 162.3 | +2.3 % |
| Peak current, A | 339 | 320 | −5.7 % |
| Energy recovered, J | 291 | **47** | −84 % |
| Electrical-to-payload, % | 21.0 | **18.8** | −10 % |
| Sled KE to the brake, J | 977 | **1162** | +19 % |
| Dry mass, kg | 76.5 | **84.5** | +10.5 % |
| kg per 3U satellite | 6.378 | **7.042** | +10.5 % |

**Every number moves the wrong way. Nothing improves.** That is what taking these decisions
costs, and it is why they were deferred.

**Validations invalidated: none, and this was checked rather than assumed.** Every run sheet in
`validation/` records the operating point it ran at, and A2's own band 2 is the measurement being
applied here. **A4 and A5 already predate the current point and say so** (P19); nothing else in
`validation/` is a function of K<sub>t</sub> in a way that changes its verdict. **A28's velocity
loop is unaffected** — the loop is feedback-linearised, so K<sub>t</sub> cancels out of the loop
transfer entirely, which is the fact P47 turned on.

**Kill criterion 1 gets worse: crossed by 3.2× → 3.5×.** Criteria 2 and 3 are unchanged and still
crossed.

## Alternatives

**Hold P46 indefinitely.** Rejected. The repository would publish a design point it has itself
computed is beaten, in a project whose entire argument is that it propagates corrections.

**Apply P46 and leave the setpoint at 16.2.** Rejected — it violates ADR-014 and makes the
dispersion figure meaningless.

**Take P46 alone and defer the other three.** Rejected as the version of this decision that
produces two baseline moves instead of one. Propagation is the expensive part; doing it once is
cheaper than doing it twice, and the four are being taken at a boundary rather than piecemeal.

## Validation

**How we would find out this is wrong.**

- **`thrust_constant(nz=1)` stops reproducing 11.0258.** Then the depth-resolved integral is not
  a clean superset of the one it replaced, and A2's 0.9558 ratio no longer means what it said.
- **A measured K<sub>t</sub> from B-2 lands nearer 11.03 than 10.54.** Then the depth correction
  is real but something else compensates, and both numbers were wrong.
- **The 8 kg placeholder is cited as though it were computed.** It is named
  `(P10 PLACEHOLDER, 8.0 kg, no derivation)` in the rollup for exactly this reason.
- **A reader finds an old number still live somewhere.** `tools/propagate_baseline.py` ran
  against a whitelist and excluded the audit record by construction; if a live document still
  says 16.388, the whitelist was wrong.
