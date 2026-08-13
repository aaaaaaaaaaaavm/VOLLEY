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
