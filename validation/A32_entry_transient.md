# A32: the entry transient and segment handover

**The last band with a plausible chance of killing the plate drive.**

[A31](A31_plate_drive_normal_force.md) settled the steady state: the plate centres itself, the
restoring force is 0.1 % of thrust, and thrust is blind to alignment. **A31 explicitly does not
model the transient**, and its own limitations section names entry as "where a destabilising
transverse impulse would do its damage".

Two transients exist in this architecture and neither has been looked at:

1. **Establishment.** The satellite starts at rest and the stator is switched on. Eddy currents
   in the plate take time to build, so thrust is not available at t = 0 and the machine is
   pushing against a secondary that is not yet responding.
2. **Segment handover.** [ADR-022](../docs/adr/022-stator-segmented-not-block-commutated.md)
   segments the stator, and a 340 mm plate crossing a segment boundary sees the travelling field
   truncated under part of its own length.

> ## BANDS DECLARED 2026-08-13, BEFORE `analysis/entry_transient.py` EXISTS.
>
> The script is absent at this commit. Verify with
> `git show --stat <this commit> -- analysis/entry_transient.py`, which returns nothing.

## Result, 2026-08-13: entry is a non-event; the segment joint is not

`analysis/entry_transient.py`, bands committed at `0635b5c` before it existed. Results in
`analysis/results/entry_transient.json`.

| Band | Test | Result | |
|---|---|---:|---|
| 1 | transient solver within 15 % of A31's steady state | **−9.0 %** | **PASS** |
| 2 | 90 % thrust within 65 mm of travel | **0.679 mm** | **PASS** |
| 3 | transient transverse force ≤ steady state, no sign change | **2.73×, restoring** | **FAIL** |
| 4 | segment handover ripple ≤ 20 % pk-pk | **30.1 %** | **FAIL** |

### Band 1 — two different models now agree

**A time-domain thin-sheet solve and A31's frequency-domain layered solve agree to 9.0 %** —
610.6 N against 670.9 N at the same operating point. Different physics implementation, different
domain, different discretisation, same answer to within the band. **The plate drive's thrust
figure is no longer single-sourced**, which is more than can be said for most numbers in this
repository.

### Band 2 — the entry transient is a non-event

| | |
|---|---:|
| Fundamental-mode magnetic diffusion time of the plate | **3.198 ms** |
| Time to reach 90 % of steady-state thrust | 5.75 ms |
| **Distance travelled while establishing** | **0.679 mm** |
| Against the acceleration zone | **0.05 %** of it |

The satellite starts at rest, so it barely moves while the eddy currents establish. **The concern
that motivated this sheet — that entry is where a destabilising impulse does its damage — does
not survive contact with the time constant.** 3.2 ms is short against a 142 ms stroke, and at
rest it is short against nothing at all.

### Band 3 fails, and the band is what is wrong

**The transverse force peaks at 2.73× its steady-state value during establishment.** The band
required it not to exceed steady state.

**It never changes sign.** It is restoring throughout, and the overshoot is *toward* centre, not
away from it. And the absolute numbers are these: steady-state transverse force at 0.5 mm offset
is **0.824 N** against **611 N** of thrust, so a 2.73× transient peak is about **2.25 N** — a
force that would move a 4.2 kg plate 0.4 mm in a tenth of a second, on a transient lasting six
milliseconds.

**The band asked the wrong question.** What matters is whether the plate is driven across its
2 mm clearance, and that is an *excursion*, not a ratio. A band on the ratio to steady state
fails on an over-restoring transient that is entirely harmless, and would have passed a
destabilising force that happened to be smaller than its own steady state.

**The band is left exactly as declared and is not re-run.** Recorded here so the next sheet does
not repeat it: **a stability band must be on the excursion or on the absolute force, never on the
ratio to the steady state it is transiently overshooting.** Logged as **P51**. Same class as A2
band 3, which passed while measuring numerical cancellation on a symmetry axis — a band can be
well-formed, falsifiable, and still not be the question.

### Band 4 fails, and this one is in the machine

**Thrust ripple across a segment boundary is 30.1 % peak-to-peak against a 20 % band.**

**And it is not the joint gap.** Sweeping the unenergised gap at the joint, separately from the
band, which stands as declared:

| Unenergised gap at the joint | Thrust | Ripple |
|---:|---:|---:|
| 10 mm | 611.8 N | 30.1 % |
| 5 mm | 616.7 N | 31.4 % |
| 2 mm | 613.8 N | 29.5 % |
| **0 mm** | 613.3 N | **25.0 %** |

**Closing the gap entirely leaves 25 %.** The ripple is not a gap effect, it is the **longitudinal
truncation of the travelling field** at the edge of an energised section — the classic end effect
of a segmented long stator with a short secondary, and it is intrinsic to the topology rather
than to the joint design.

**The consequence is the one the band was written to catch.** With four segments over 1.30 m, the
segment-crossing frequency sweeps **0 → 61.5 Hz** across the stroke, and the track's first two
modes are at **48 Hz and 109 Hz**. A 30 % force disturbance sweeping through 48 Hz is **A17's
force-ripple chirp problem in a new place**, and **P36** already records that the track has no
dynamic design case. This does not get to be assumed clear.

**The direction, not the fix.** Energising *overlapping* segments so the field under the plate is
never truncated is the obvious candidate and it is not computed here. Longer segments lower the
crossing frequency but do not remove the truncation. Logged as **P52**.

### Three new solvers in a row, three first runs wrong, three caught by their own bands

Stated once, plainly, because it is the most useful thing in this sheet.

| | First run returned | Caught by | The fault |
|---|---|---|---|
| **A30** `edge_effect.py` | exactly 0.0000 for every geometry | band 2 | travelling wave written as a real cosine, so thrust integrated to zero |
| **A31** `plate_normal_force.py` | **705 %** of the magnetic-pressure ceiling | band 5 | a single-sided model, and flux normalised on the screened field |
| **A32** `entry_transient.py` | **+304 %** against A31 | band 1 | thrust computed as K × B_imposed instead of K × B_total |

**Every one of those would have been published as a result.** Each was caught by a band declared
before the script existed, and in every case the band that caught it was the *verification* band
— the one that exists only to check the solver against something already known, and that adds no
new physics. **That is the cheapest band to write and the one most often left out.**

---

## What is being computed

A **time-domain** solve of the thin-sheet secondary, which is a different model from A31's
frequency-domain layered solve on purpose. The sheet's induced current is carried as a stream
function ψ; including the sheet's own reaction field gives each spatial mode a magnetic diffusion
time τ_k, and it is that time constant — absent from every steady-state result so far — that the
transient turns on.

The imposed field is windowed in x, so a segment boundary is a step in the window and the plate
straddling two segments falls out of the same solve.

## Acceptance bands

### Band 1 — the transient solver reproduces the steady state

**Band: at constant velocity with the stator fully energised, thrust from this solver agrees with
A31's layered solve to within 15 %.**

Two different models — a time-domain thin sheet against a frequency-domain layered solve — so the
band is loose. **It is not loose about the sign or the order of magnitude.** A30 band 2 caught a
solver returning identically zero and A31 band 5 caught one returning 705 % of physics, both on
their first run; this band exists because that has now happened twice in one day.

### Band 2 — the machine is not waiting for its own secondary

**Quantity:** distance travelled from switch-on before thrust first reaches 90 % of its
steady-state value.

**Band: ≤ 65 mm**, which is 5 % of the 1.30 m acceleration zone.

**This band may fail.** If establishment costs a material fraction of the stroke, the exit
velocity falls and the profile the **A28** velocity loop tracks is wrong at exactly the point
where it has least authority.

### Band 3 — nothing transient pushes the plate at the wall

**Quantity:** peak transverse force on the plate at 0.5 mm offset at any instant during
establishment, against its own steady-state value at the same offset.

**Band: the transient peak does not exceed the steady-state value, and does not change sign.**

A31 found the transverse force restoring and negligible in steady state. The concern this band
tests is whether the *approach* to that state overshoots or reverses — because a plate driven
across 2 mm of clearance during the first milliseconds does not care what the steady state would
have been.

### Band 4 — the plate crosses a segment boundary without a step

**Quantity:** peak-to-peak thrust ripple as the plate traverses one segment boundary, as a
fraction of mean thrust.

**Band: ≤ 20 %.**

A 340 mm plate on a segmented 1.30 m stator spans a boundary for a substantial part of the
stroke. Above 20 % this becomes a force disturbance at a frequency set by the segment pitch and
the velocity, sweeping upward through the stroke — which is the **A17** force-ripple chirp
problem in a new place, and it would have to be shown clear of the track modes rather than
assumed clear.

## What this cannot settle

- **The sheet model is not the layered model.** It carries the secondary's own reaction field but
  treats the stators as an imposed windowed field rather than solving the gap. Band 1 is what
  bounds the disagreement.
- **Rigid plate, rigid track.** A transverse impulse is applied to a body assumed not to bend.
- **No mechanical model of retention.** How the satellite is held before the stator takes over is
  undefined in this architecture and is not modelled here.
- **Nothing is measured.** **E4** stands.
