# A59 — the drive tube as a beam, a column and a pressure vessel

**Bands declared 2026-08-19, before `analysis/tube_structure.py` existed.**
Verify with `git show --stat <this commit> -- analysis/tube_structure.py`, which must return nothing.

---

## Why this run exists

**[ADR-034](../docs/adr/034-gen6-long-stroke-design-point.md) took the stroke from 2.18 m to
8.0 m and nothing structural was checked.** [A49](A49_design_surface.md) costed the tube as
*"a plain cylinder at one wall thickness, no bending, no alignment tolerance, no dynamic seal
behaviour"* — its own words — and added that **every omission flatters a long tube.**

**`cad/build_gen6.py` says the same thing in its docstring**: 22.73 bar on this bore needs
0.16 mm of wall and the minimum practical wall is 1.0 mm, *"so the section is set by handling and
by carrying A38's 201.7 N cradle preload — neither of which is modelled here."*

**So the tube is drawn at a wall thickness chosen by two criteria that were never computed**, and
it is now **8.0 m long at 17.805 mm outside diameter — an aspect ratio of 449:1.**

## What is actually being asked

**The drive tube is three things at once**, and the repository has only ever checked the first:

| | |
|---|---|
| **A pressure vessel** | hoop stress at the charge pressure. This is the only one `precharged.py` sizes |
| **A beam** | it spans the stage, it sags under handling and ascent load, and it has a bending mode that must clear the launch band |
| **A column** | the shot's axial reaction, **p₀·A**, runs back through it to whatever holds it |

**And a fourth thing that is not structural but is decided by the same variable:** the piston has
to slide through it. Any residual bow is side load on the seal, which is **P67**, which A49 band 6
already showed is the term this design point is most exposed to.

**The design variable is support spacing**, and this run asks what spacing each criterion demands.

## Declared before the run

**The material is not stated anywhere in the repository, and that is itself a finding.**
[A49](A49_design_surface.md) computes `tube_kg` at **2700 kg/m³**, aluminium.
[`analysis/precharged.py`](../analysis/precharged.py) sizes the chamber at **7800 kg/m³** with a
**500 MPa** allowable and a safety factor of 2 — steel. **Nothing says which the tube is.** Both
are computed here and the difference is reported rather than resolved by preference.

| | Value | Where it comes from |
|---|---|---|
| Bore / wall / length | 15.805 mm / 1.0 mm / 8.0 m | `cad/parameters.json`, `gen6_drive` |
| Charge pressure | 22.7258 bar | `cad/parameters.json`, ADR-034 |
| Allowable stress, safety factor | 500 MPa, 2.0 | `precharged.py` |
| Aluminium | E = 69 GPa, ρ = 2700 kg/m³ | `sizing.py` E_al, A49 RHO_AL |
| Steel | E = 200 GPa, ρ = 7800 kg/m³ | ρ from `precharged.py::chamber_kg` |
| Dynamic target | first mode **> 70 Hz** | `sizing.py::track_first_mode` |
| Ascent case | **25 g** quasi-static | `sizing.py::retention_gate`, g_ascent |
| **Support model, declared here so it cannot be tuned afterwards** | a split ring clamp of 3 mm wall, 12 mm wide, plus a 40 × 12 × 3 mm standoff bracket to the rail, plus two fasteners at 2 g — all aluminium | an estimate, and stated as one |

**Mode constants and the beam formulae are the ones `sizing.py::track_first_mode` already uses**,
not restated: λ² = 9.87 pinned-pinned and 22.37 fixed-fixed.

## The prediction, recorded before the run

**Written down so it can be wrong.** I expect bands 2, 3 and 4 to fail — the unsupported tube
misses the dynamic target, buckles under its own shot reaction, and needs supports closer than
2 m. **I expect band 5 to fail too: that the supports cost more than half a kilogram** and eat
ADR-034's mass saving, which is the outcome that would send the design point back to A49's
surface.

**If band 5 passes, my planning-stage worry was wrong** and the tube's mass risk lies somewhere
else. That is worth recording either way.

---

## Acceptance bands

**Declared before the script. Not to be edited after the run.**

| # | Band | FAIL if |
|---|---|---|
| **1** | Hoop stress at 22.7258 bar is **within 500 MPa / 2.0** | The tube is a pressure problem after all, and `build_gen6.py`'s claim that 0.16 mm suffices is wrong |
| **2** | The **unsupported** 8.0 m tube's first bending mode is **≥ 70 Hz**, `sizing.py`'s own target | **The tube as drawn does not meet the dynamic target this repository set for its own structure** |
| **3** | Euler buckling load of the **unsupported** tube exceeds the shot's axial reaction **p₀·A with the declared safety factor of 2** | **The tube buckles under the reaction of its own shot**, and intermediate support is mandatory rather than good practice |
| **4** | The support spacing that satisfies bands 2, 3 and 7 simultaneously is **≥ 2.0 m** — at most three intermediate supports on an 8 m span | The tube needs a support roughly every metre, and the rail interface is a structure rather than a set of brackets |
| **5** | Total support mass at that spacing is **≤ 0.5 kg** | **The supports eat ADR-034's mass saving**, and the design point has to move back onto A49's surface |
| **6** | **Tube + supports ≤ 2.0 kg**, the limit [A49](A49_design_surface.md) band 7 declared and passed at 1.140 kg | **A49's tube mass was optimistic by more than the band allows**, and ADR-034's per-satellite figure is wrong |
| **7** | Bending stress at the **25 g** ascent case, at the selected spacing, is **within 500 MPa / 2.0** | The spacing chosen for stiffness does not survive the launch load |
| **8** | Self-weight sag at **1 g** over the selected spacing is **≤ 10 % of the bore** | The tube cannot be handled, assembled or ground-tested straight, and the piston cannot be trusted to slide in a fixture |
| **9** | **REPORT, no pass/fail.** Tube mass in aluminium against steel, and what each does to bands 2, 3 and 6 | — |

## What this run will not do

- **No FEA.** Euler–Bernoulli beam, Euler column, thin-wall hoop. No shear deformation, no local
  crushing at the clamps, no stress concentration, no weld or joint.
- **It does not model the seal.** The link to **P67** is named and left there; side load from a
  residual bow is not computed.
- **It does not design a support.** The clamp model above is a mass estimate declared in advance,
  not a bracket anyone has drawn.
- **It does not settle the material.** It reports both and records that the repository does not say.
- **Random vibration is not covered** — only a 25 g quasi-static case. The 109 Hz mode work in
  [A33](A33_track_dynamics.md) and the Q-sweep in A22 are the precedent for what a real dynamic
  case would need, and neither exists for this tube.

**Provenance: model output. E4 stands — nothing here is measured.**
