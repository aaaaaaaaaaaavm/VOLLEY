# A4: Sled chassis structural (CalculiX or Code_Aster)

> ## RUN 2026-07-28, CalculiX ccx 2.21, structural leg complete
>
> | Band (declared below, before the run) | Result | |
> |---|---|---|
> | Airgap closure <= 0.025 mm per plate | 0.0194 mm (pinned) / 0.0160 (clamped) | pass, 78 % of budget |
> | Von Mises <= 587 MPa | 33.7 MPa | pass, 17x margin |
> | First mode > 200 Hz | 3408 Hz | pass, 17x |
>
> The plate as drawn meets every constraint. It is not strength-driven and only
> moderately stiffness-driven. Full record, mesh, idealisations and caveats:
> [`../validation/results/A4_sled_structural.json`](../validation/results/A4_sled_structural.json);
> decks and logs in [`../validation/fea/`](../validation/fea/).
>
> This does not close the mass question. The run answers "does the drawn chassis meet
> the constraint" (yes) rather than "what is the lightest chassis that does". Uniform
> thinning is nearly worthless, deflection goes as 1/t³, so the budget is spent at ~5.5 mm
> for a 0.30 kg saving. Real reduction needs a rib-stiffened redesign, which nothing has
> evaluated. The decision rule's >= 6.80 kg branch therefore stands: 16.53 m/s.

Closes: `OPEN_PROBLEMS.md` P5 (sled mass 4.86 vs 7.50 kg) and P8 (exit
velocity 20.37 vs provisional 17.88 m/s).

This is the highest-leverage analysis in the repository. Everything headline,
velocity, efficiency, recoil, lifetime multiplier, hangs off the sled mass, and that
mass currently has two irreconcilable estimates, neither of them FEA'd.

## The question, stated so it can be answered

Not "what does the sled weigh" but: what is the lightest chassis that holds the airgap
open to ±0.05 mm under load? Mass is the output of that constraint, not an input.

## Inputs (all committed)

- Geometry: `cad/step/gen3/EMOCD_Sled_Gen3.step`, Gen3, not an earlier generation.
  Gen3 is the dimensionally corrected sled: 488x 140 mm chassis, where Gen2 was 360x 110.
  Meshing the Gen2 sled would size a chassis that no longer exists
- Dimensions and material: `cad/parameters.json`, sled group (6 mm Ti-6Al-4V chassis,
  flagged `PROVISIONAL_PENDING_FEA`)
- Loads, from `analysis/results/sizing.json`:
  - Inter-array attraction 3.68 kN (`inter_array.force_kN`), the sizing case
    > Superseded 2026-07-31 by A12: the real force is 2.69 kN and this run was 37 % heavy.
    > A4's results are conservative and its verdict stands. It is not re-run, repeating a
    > passing structural analysis at a lighter load replaces a real result with a weaker one.
    > The bands below are left exactly as declared.
  - Axial acceleration 16.3 g at the script operating point (12.5 g if the CAD sled
    mass holds, run both)
  - Arrest 9.54 kN axial (`arrest.axial_kN`), a separate load case
- Material allowable: Ti-6Al-4V yield 880 MPa (`inter_array.Ti_yield_MPa`)

## Acceptance band (declared 2026-07-27, before running)

| Quantity | Constraint |
|---|---|
| Airgap closure under 3.68 kN | ≤ 0.05 mm total, both sides combined |
| Von Mises peak, any load case | ≤ 880 MPa / 1.5 = 587 MPa |
| First mode, chassis | > 200 Hz (an order clear of the 128 ms shot pulse) |

The decision rule for the resulting mass m, fixed now:

- m <= 5.35 kg (4.86 + 10 %) to the parametric model stands. Close P5 and P8, delete
  the provisional 17.88 m/s note from `README.md`.
- 5.35 < m < 6.80 kg to neither estimate is right. Update `mass_properties.py` to the
  FEA mass, re-run `motor_model.py`, then correct the paper. Log the whole chain.
- m >= 6.80 kg to the CAD estimate is substantially right. 17.88 m/s becomes the
  headline number, `README.md` and `paper/paper.tex` both change, and P8 escalates to
  a paper correction on the scale of P1, P4.

Deciding this in advance is the point. After the run, the temptation will be to pick the
threshold that keeps 20.37 m/s.

## If the chassis fails the stiffness constraint

Then the 6 mm plate is not the design, and the mass question is open in the other
direction, a stiffer chassis is heavier still, pushing further into the third branch
above. Report the mass at the constraint, not the mass of a chassis that does not meet it.

## Output

`validation/results/A4_sled_structural.json`, chassis mass at the stiffness constraint,
peak deflection per load case, von Mises peak, first mode, plus `solver`, `version`,
`element_type`, `element_count`, `contact_treatment`.

---

## Reproduction record, 2026-09-15

[P39](../OPEN_PROBLEMS.md#p39) left one question open: whether the CalculiX input decks belong in
the flagship. Answering it required establishing that the committed generator is the deck's
provenance, so that was measured rather than assumed. This is also the first run sheet to carry
the reproduction fields [`docs/PROTOTYPE_READINESS.md`](../docs/PROTOTYPE_READINESS.md) requires
of a controlling simulation.

| Field | Value |
|---|---|
| Source revision | `10bf06e` |
| Generator | `validation/fea/build_deck.py`, tracked; reads `cad/step/gen3/EMOCD_Sled_Gen3.step`, `cad/parameters.json` and `analysis/results/sizing.json` |
| Mesher | gmsh API 4.15.2 |
| Solver | CalculiX `ccx` 2.21-1 |
| Commands | `python3 validation/fea/build_deck.py` · `ccx plate_pinned` · `ccx plate_clamped` |
| Mesh | 29 312 nodes reported per case; 4054 loaded nodes, 2425 web nodes |
| `plate_pinned.inp` | sha256 `a3a4f94cdbf4cbee4cb463779f2751140a5779cd70bbea0d7ceae553b53bc8d9`, 2 252 204 bytes |
| `plate_clamped.inp` | sha256 `5eccc7a81d1f548284ed0403b5539ebb5f3f077175d175ed9b7f03074208274d`, 2 252 205 bytes |

**Determinism.** The generator was run twice in the same environment and both decks hashed
identically. The hashes above are therefore a property of this gmsh version, not of the run.

**Reproduced result.** Peak out-of-plane displacement, extracted from the `.dat` files:

| Case | Reproduced | Published in this run sheet |
|---|---:|---:|
| pinned | **0.01945 mm** | 0.0194 mm |
| clamped | **0.01600 mm** | 0.0160 mm |

Both bracket values reproduce. The band and the verdict are unchanged; nothing here re-opens A4.

**What is not pinned.** gmsh's mesh is not guaranteed stable across versions, so a future run on a
different gmsh may produce different deck hashes. That is why the version is recorded beside the
hash: a mismatch is then a visible discrepancy to investigate rather than a silent difference. The
displacement result is the quantity A4 is accountable for, and it is a bracket, not a single
number, precisely because the support condition is uncertain.
