# A2: the three-dimensional field, and the depth assumption inside K<sub>t</sub>

**Closes:** the 3-D half of **E1**, and the last "different physical method" gap in **E2**.
**Bears on:** **P21** (the 2-D model overestimates far field because it has infinite depth).

> ## BANDS DECLARED 2026-08-10, BEFORE `analysis/field_3d.py` EXISTS.
>
> Everything below is committed before the script is written, and the script is absent at this
> commit. Verify with `git show --stat <this commit> -- analysis/field_3d.py`, which returns
> nothing.

## Result, 2026-08-10: the depth assumption costs 4.42 % of K<sub>t</sub>

`analysis/field_3d.py`, bands committed at `964af2c` before it existed. Results in
`analysis/results/field_3d.json`.

### Band 2 — the finding

| | K<sub>t</sub>, N per kA·m |
|---|---:|
| Centre-plane only — reproduces `motor_model.thrust_constant()` to **0.000 %** | **11.0258** |
| **Depth-resolved**, `B_y` Gauss-Legendre averaged over z ∈ [−45, +45] mm | **10.5386** |
| **Ratio** | **0.9558** |

**The band was ≥ 0.95 and the result is 0.9558. It passes — by 0.008.**

**The published K<sub>t</sub> is a centre-plane value and overstates thrust by 4.42 %.** Nothing
about the field was wrong; magpylib has always modelled the blocks with their real 90 mm depth.
What was wrong is the integral treating that centre-plane value as though it held uniformly
across the full depth. It falls off toward the array's z-edges, and 4.42 % is what that costs.

**Propagated through `motor_model.shot()`, unchanged in every other respect:**

| | Published | Depth-resolved |
|---|---:|---:|
| K<sub>t</sub> | 11.0258 N/kA·m | **10.5386** (−4.42 %) |
| **v_exit** | **16.388 m/s** | **16.029 m/s** (−2.19 %) |
| Acceleration | 10.53 g | 10.07 g |
| Peak current | 339 A | 320 A |
| Stroke time | 158.6 ms | 162.3 ms |

> **The baseline has NOT been changed.** `docs/BASELINE.md` still reads 11.0258 and 16.388, and
> every downstream number still descends from them. Moving a frozen baseline value is not a
> validation's decision to take on its own, and this one is recorded as **P46** with the
> correction computed and held rather than applied.

### Band 1 caught a bug in this analysis, which is the reason it exists

The first run reported the centre-plane K<sub>t</sub> as **17.2954** against `motor_model`'s
11.0258 — **a 56.9 % reproduction error.** `kt_depth_resolved()` normalised the one-wavelength
force by `45e3 * DEPTH` where `motor_model` scales it by `SLED_ACTIVE_LEN / LAM`.

**Had band 1 not been declared, the 0.9558 would have been reported off a broken integral and
happened to look plausible.** The ratio is unchanged by the fix — both sides carried the same
error — but that is luck, not method. Reproduction now exact at **0.000 %**.

This is the third time in this project a declared band has caught a bug in the analysis rather
than a problem in the design (A19, A20, and now A2).

### Band 3 — PASSES, and is uninformative. The band was badly chosen

| | \|B\| at 500 mm along +z |
|---|---:|
| Real 90 mm depth | 1.101 × 10⁻²⁰ T |
| Infinite-depth proxy, 900 mm | 2.982 × 10⁻¹⁹ T |
| Ratio | **0.0369** — passes the ≤ 0.60 band |

**Both figures are physically meaningless.** 10⁻²⁰ T is fourteen orders of magnitude below
Earth's field and below float64's ability to resolve the cancellation producing it. The probe
point sits on the array's **symmetry axis**, where the net dipole moment cancels, so the band
measures numerical cancellation rather than field.

**The band is left exactly as declared and is not re-run** — a band is never edited after its
run. Recorded here so the next sheet does not repeat it: **a far-field band must probe off the
symmetry axis**, and P21's mechanism should be tested where the field is actually large enough to
matter, which is the standoff A14 already uses.

### Bands 4 and 5

| Band | Test | Result | |
|---|---|---|---|
| 5 | 7-wavelength array within 2 % of 21 at its centre | **0.99990** | **PASS** |
| 4 | `getdp` 3-D FEM within 5 % of magpylib | **NOT RUN** | — |

**Band 5 passing at 0.9999 settles a background assumption** the model makes everywhere and had
never stated: seven wavelengths is enough for the array centre to be effectively infinite.

**Band 4 was not run and E2's "different physical method" gap therefore stays open.** `gmsh`
4.15.2 and `getdp` 3.2.0 are now installed and working in this environment, so the obstacle is
work rather than tooling. **Stating this as not-run rather than quietly dropping it**: the
depth-resolved result above is still magpylib, which is analytic superposition — exactly the
*"neither solving a field equation"* that E2 objects to. **A2 closes E1's 3-D half. It does not
close E2.**

---

## What is actually being tested, which is narrower and sharper than "3-D"

`motor_model.build_field()` already builds the array from **magpylib `Cuboid` sources with the
real 90 mm depth**, so the *field* has always been three-dimensional and exact — superposition of
closed-form solutions for uniformly magnetised blocks is exact in free space, and the machine is
ironless.

**The two-dimensional assumption is not in the field. It is in the thrust integral.**

```python
By = field.getB(np.stack([X.ravel(), Y.ravel(), np.zeros(X.size)], 1))[:, 1]
...
return float((...).sum() * dx * (WIND_THICK / 2) * DEPTH)
```

`thrust_constant()` samples `B_y` **only on the centre plane z = 0**, then multiplies by the full
`DEPTH = 0.09 m` as though that centre-plane value held uniformly across the whole 90 mm. It does
not: the field falls off toward the array's z-edges, so **the true depth-averaged `B_y` is lower
than the centre-plane value, and K<sub>t</sub> is therefore overstated by some factor.**

That factor has never been computed. **This is what A2 computes.**

> **If this moves K<sub>t</sub>, it moves the baseline.** `docs/BASELINE.md` fixes
> **K<sub>t</sub> = 11.0258 N/kA·m** and **v_exit = 16.388 m/s**, and every downstream number
> descends from them. A2 is therefore the highest-stakes validation since A1, and the protocol is
> **stop and report**, not silently re-baseline. A missed band becomes a numbered defect.

## Acceptance bands

**Per `validation/README.md`'s rule added from P20, every field band below names the plane and the
quantity, and where a magnet surface is involved, both references.**

### Band 1 — the depth-resolved integral is implemented correctly

With `DEPTH` set to **900 mm (10× the real depth)** and everything else unchanged, the
depth-resolved K<sub>t</sub> agrees with the centre-plane K<sub>t</sub> to within **1 %**.

A very deep array is locally two-dimensional at its mid-plane, so the two integrals must
converge. **If this fails, the new integral is wrong and no other band means anything.**
**FAIL above 1 %.**

### Band 2 — the depth end-effect factor at the real 90 mm depth

**Quantity:** K<sub>t</sub> in N per kA/m, from `motor_model`'s own Lorentz integral, differing
**only** in whether `B_y` is taken on the plane z = 0 or Gauss-Legendre averaged over
z ∈ [−45 mm, +45 mm]. Same winding, same currents, same quadrature in x and y.

**Band: the ratio K<sub>t</sub>(depth-resolved) / K<sub>t</sub>(centre-plane) is ≥ 0.95.**

That is: the 2-D depth assumption overstates thrust by **no more than 5 %**.

**This band may fail, and it is the one that matters.** If the ratio comes in below 0.95, the
published K<sub>t</sub> = 11.0258 N/kA·m is overstated by more than 5 %, `v_exit` falls, and the
correct response is a numbered defect and a propagation pass — **not** an edited band and **not**
a quiet re-baseline.

### Band 3 — the far-field overestimate P21 named

**Quantity:** |**B**| in tesla, at a point **500 mm from the array centre along +z** (the depth
axis, the direction the 2-D model has no information about), outside the machine.

**Band: |B|(3-D, real 90 mm depth) ≤ 0.60 × |B|(the same field with DEPTH = 900 mm).**

P21 records that an infinite-depth model overestimates far field. This tests that the real array's
far field is *materially* lower, not merely lower — a ratio near 1.0 would mean P21's stated
mechanism is not the one operating.

### Band 4 — a different physical method

**Quantity:** peak |B_y| at **midgap (y = 0), on the plane z = 0**, over one 48 mm wavelength,
taken as the **double-sided fundamental amplitude** — *not* the single-sided reference, and *not*
the raw peak. Both alternatives are named here because A1's row failed for exactly this ambiguity
and P20 exists to stop it recurring.

**Band: a `getdp` 3-D magnetostatic solve on a `gmsh` mesh agrees with magpylib to within 5 %.**

magpylib and the wave model are both analytic superposition — *"neither solving a field
equation"*, as E2 puts it. A meshed PDE solve is a genuinely different method, and it is the last
one this project's electromagnetic model has never been checked against. **This band may fail on
mesh quality rather than on physics**, and if it does, that is what gets written.

### Band 5 — longitudinal end effect on the array's own finiteness

**Quantity:** fundamental amplitude of `B_y` at midgap, z = 0, over the **central** wavelength.

**Band: a 7-wavelength (336 mm) finite array is within 2 % of a 21-wavelength array** at its
centre.

The array is 340 mm and `build_field` uses `n_wave=7`. This tests that seven wavelengths is
enough for the centre to be effectively infinite — an assumption the model makes everywhere and
has never stated. Distinct from **A16**, which is about the array leaving the *stator*, not about
the array's own ends.

## What this cannot settle

- **Nothing here is measured.** magpylib, the wave model and getdp are three calculations. **B-1
  remains the only thing that changes the category of evidence** and it is still unordered.
- **The winding's own 3-D geometry is not modelled.** End turns are explicitly absent from
  `parameters.json` (`end_turns_modelled: false`), and they are outside the 90 mm active depth.
  A2 resolves the *field* in depth, not the *conductor* in depth.
- **No temperature dependence.** Br is taken at its nominal 1.32 T throughout.
