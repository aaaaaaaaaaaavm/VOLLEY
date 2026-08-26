# A52, recoil and angular impulse at Gen6

**Bands declared 2026-08-16, before `analysis/gen6_recoil.py` existed.**
Verify with `git show --stat <this commit> -- analysis/gen6_recoil.py`, which must return nothing.

---

## Why this run exists

Two of the four `NEEDS SOURCE` rows in [`KILL_CRITERIA.md`](../docs/KILL_CRITERIA.md), and
[E29](../OPEN_PROBLEMS.md), which is live:

> *"Nothing computes the shot's angular impulse about the host, and a reaction wheel saturates."*

Gen5's recoil is 64.1 N·s per shot and is called *"the healthiest item on the list"*. Gen6
has never been computed, and it fires a heavier impulse: 4 kg at 29.009 m/s against 4 kg at
16.029. Recoil scales with the impulse and the impulse has nearly doubled, so a row marked
*healthy* for Gen5 cannot be assumed healthy for Gen6.

And the geometry changed underneath it. Gen5 fired along the axis of a machine bolted to a
host. Gen6 fires along a rail that *is* the stage, so the thrust line's offset from the host centre
of mass is a different quantity, and it is the quantity E29 says nobody has computed.

## Method

Linear recoil is the payload's momentum, as in `astro.py`. What is added is the angular part:
the moment about the host centre of mass at a stated offset, integrated over the shot, and the
reaction-wheel momentum it demands across a twelve-shot campaign.

The CoM offset is a declared sweep, not a number, because no stage's mass properties are
public, that is E5, and it is why the Gen5 recoil table is parametric.

---

## Acceptance bands

Declared before the script. Not to be edited after the run.

| # | Band | FAIL if |
|---|---|---|
| **1** | Applying the method at Gen5's operating point reproduces **64.1 N·s** within 1 % | The method is not the one `astro.py` used and the comparison is meaningless |
| **2** | Gen6 linear recoil per shot is reported, and the **campaign total** with it | A per-shot figure alone understates what the host is asked to absorb |
| **3** | **Angular impulse about the host CoM is computed** across an offset sweep | E29 stays open and this run did not do its job |
| **4** | The offset at which a **15 N·m·s** wheel saturates within twelve shots is stated | The result is not actionable as an interface requirement |
| **5** | Propellant to null the campaign's linear recoil is **≤ 1.0 kg** at a stated I<sub>sp</sub> | Recoil stops being *"a customer decision rather than an engineering one"* |
| **6** | The result is stated as an **interface requirement on thrust-line alignment**, in millimetres | E29's actual complaint — that no such requirement exists — is not answered |
| **7** | Both the **trim stage's** contribution and the gas shot's are included | ADR-033 added a second force on the same axis and it is not in any budget |

## Predictions

1. **Band 2: about 116 N·s per shot**, 4 kg at 29.009 m/s, and **≈ 1393 N·s** over twelve — against
   Gen5's 64.1 and 769.
2. **Band 5 passes.** At a hydrazine-class I<sub>sp</sub> the campaign is under a kilogram.
3. **Band 4 is the useful output**, and I expect the saturating offset to be small enough that
   an alignment requirement is unavoidable, which is exactly what E29 says is missing.
4. **Band 7 contributes almost nothing numerically** — the trim stage is 37.7 J against 1864.8 —
   **but omitting it would be the same error A48 band 5 made**, so it is in.

## Result

**RUN 2026-08-16. Seven of seven bands pass, and E29 has the requirement it said was missing.**

| | Per shot | Campaign |
|---|---:|---:|
| Gen5 | 64.12 N·s | 769.4 N·s |
| **Gen6, gas shot** | **116.03 N·s** | **1392.4 N·s** |
| Gen6, trim stage | 1.29 N·s | 15.5 N·s |
| **Gen6, total** | **117.32 N·s** | **1407.9 N·s** |

Gen6 recoils 1.81x harder than Gen5 per shot. Nulling the campaign costs 0.653 kg at a
hydrazine-class I<sub>sp</sub>, against Gen5's 0.357, still under a kilogram, so
`KILL_CRITERIA.md`'s judgement that recoil is *"a customer decision rather than an engineering
one"* survives the architecture change.

### The angular half, which is what E29 actually asked for

| CoM offset | Per shot | Over 12 shots | vs a 15 N·m·s wheel |
|---:|---:|---:|---|
| 10 mm | 1.173 N·m·s | 14.08 | within |
| **25 mm** | 2.933 | 35.20 | **saturates ×2.3** |
| 100 mm | 11.732 | 140.79 | saturates ×9.4 |
| 500 mm | 58.662 | 703.94 | saturates ×46.9 |

> ### The interface requirement, stated in the units an integrator needs
>
> The thrust line must pass within 10.7 mm of the host centre of mass to keep a 15 N·m·s wheel
> unsaturated across a twelve-shot campaign.
>
> Gen5's equivalent was 19.5 mm. Gen6 tightens it by 1.8x, in exact proportion to the impulse.

E29's complaint was that no such requirement existed. It exists now, and it is demanding: 10.7
mm of alignment to the centre of mass of a spent stage whose mass properties are not public,
which is E5, and which is why this is a sweep rather than a number.

Momentum management is not optional at Gen6. Either the alignment requirement is met, or the
host dumps momentum between shots, and the 1200 s cadence of ADR-020 is enough time to do it.

## What this run does not do

- All shots along one axis in one direction, so angular impulse accumulates. Alternating the
  firing direction would cancel much of it and the magazine does not currently allow that.
- Rigid host, no flexibility, no propellant slosh, no attitude control during the shot.
- It does not size a wheel or a thruster, only states what they must absorb.
