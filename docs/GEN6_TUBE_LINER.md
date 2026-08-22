# The stator, the tube, and whether a liner deletes the question

**Scoping trade, 2026-08-22.** [P92](../OPEN_PROBLEMS.md) records that
[ADR-033](adr/033-gen6-trim-stage.md) puts the trim stator *outside* the drive tube and its magnets
*inside*, [ADR-035](adr/035-drive-tube-material.md) made that tube aluminium four days later, and
**no file computes what a conducting sleeve between a travelling-field stator and its secondary
costs.**

> ## This is not A66, and it does not close P92
>
> **A66 is the run P92 asks for**, with bands declared before the script, reporting **thrust
> attenuation, induced loss and wall temperature** against ADR-035's 473 K ceiling. **None of those
> three is computed here.**
>
> This file does one thing A66 would do first — the skin-depth comparison — and uses it to ask a
> *different* question: **is there a design that makes A66 unnecessary?** P92 names the candidates
> itself and does not choose between them. **P92 stays LIVE and A66 stays deferred behind P67.**

---

## 1. The tube is much thinner than the skin depth, which is the opposite of a shorted turn

| | |
|---|---:|
| Pole pitch, `stator.pole_pitch` | **24 mm** |
| Carriage speed, `gen6_drive.exit_velocity_m_s_zero_friction` | **34.28 m/s** |
| **Excitation frequency**, *v* / 2λ | **714.2 Hz** |
| Aluminium conductivity, `analysis/phase1_closeout.py` | **3.5 × 10⁷ S/m** |
| **Skin depth at 714 Hz** | **3.183 mm** |
| Wall, `gen6_drive.tube_wall_mm` | **1.0 mm** |
| **Wall ÷ skin depth** | **0.314** |

**A sleeve shields when it is thick against the skin depth. This one is about a third of it.** The
field penetrates the wall rather than being excluded by it, so **the attenuation is likely modest
and the "shorted turn" framing in P92 overstates the mechanism.**

> **"Likely modest" is not a number, and this file does not pretend it is one.** A thin conductor
> still carries induced current, still dissipates, and still drags. **What the ratio establishes is
> the *regime*, not the magnitude** — and P92's three questions are all magnitudes. *A66 is still
> the thing that answers them.*

**One consistency check fell out of it.** The tube mass computed from this geometry is **1.1689 kg
at the 8.2 m rail** and **1.1404 kg at 8.0 m**; `parameters.json` carries **1.1404 kg**. So the
committed tube mass is the **stroke** length, not the rail — which is right, and which
[A57](../validation/A57_stage_attitude_packaging.md) band 6 has just made worth stating out loud.

---

## 2. What a local non-conducting section costs

**The candidate is not lining the whole 8 m tube.** It is replacing the aluminium *only where the
stator sits* — A55 sized that section at **144.01 mm**, and a generous 3× span is **432 mm**, about
**5 %** of the tube.

| Material over a 432 mm section | Mass | Against the aluminium it replaces |
|---|---:|---:|
| Aluminium 6061-T6, as drawn | 0.0616 kg | — |
| **PEEK** | **0.0301 kg** | **−31.5 g** |
| **G-10 / FR4 glass-epoxy** | **0.0422 kg** | **−19.4 g** |
| Ti-6Al-4V *(conducting, listed only for scale)* | 0.1011 kg | +39.5 g |

**The liner costs negative mass.** *That is not the interesting part* — 31 g is noise against an
11.45 kg added-hardware budget. **The interesting part is that mass is not the objection**, which
is what ADR-035 chose the tube on.

### Densities used, and they are declared rather than sourced

**2700, 1320, 1850 and 4430 kg/m³.** These are handbook class figures, they are not in any results
file in this repository, and **no supplier has been asked.** They are good enough to establish that
the mass difference is tens of grams and **not good enough for anything else.**

---

## 3. What it actually costs, and neither cost is mass

**1 — A joint in a pressure tube.** The drive tube is the cylinder. A non-conducting section means
**two joints** in a component that holds 22.73 bar and guides a piston at 34 m/s, at the exact
station where the seal must not snag. [A59](../validation/A59_tube_structure.md) found the tube
needs **seven supports at 1.0 m spacing** and buckles under its own shot reaction by 45× without
them; adding discontinuities to it is a structural question A59 did not ask.

**2 — ADR-035's 473 K ceiling, and it is `NEEDS SOURCE` for every candidate here.** The ceiling
exists because [A63](../validation/A63_steam_design_point.md) found **none of 108 steam design
points reaches it**. **This file does not state a continuous service temperature for PEEK or for
G-10**, because neither is in this repository and asserting one from memory is exactly the failure
[P98](../OPEN_PROBLEMS.md) is about. *A polymer section at the stator station has to clear 473 K or
it is not a candidate, and nothing here has checked that.*

**3 — A third option P92 names and this file has not priced: a *slotted* aluminium section.** Slots
break the induced current path without changing material, joint count or thermal class. **It is
probably the cheapest answer and it is the one with no numbers here at all.**

---

## 4. What this changes

**It de-risks the branch rather than closing it.** If [P67](../OPEN_PROBLEMS.md) comes back above
**22.3 N**, the trim stator is needed and A66 becomes the next run. **This file says that branch is
not frightening**: the coupling regime is favourable, the mass cost of a fix is negative, and there
are three candidate fixes of which the cheapest has not been priced.

**It changes nothing about P67 itself**, and it is not a reason to delay B-2.

| | |
|---|---|
| **P92** | **stays LIVE.** Attenuation, induced loss and wall temperature are still uncomputed |
| **A66** | **stays deferred behind P67**, exactly as ADR-036 left it |
| **ADR-035** | unchanged. It chose aluminium on mass, and mass is still not the objection |
| **What this file adds** | the regime, the mass of a fix, and the two costs that are not mass |

---

## Provenance

Pole pitch, wall, bore and carriage speed from `cad/parameters.json`. Conductivity from
`analysis/phase1_closeout.py`. Stator section length from
[A55](../validation/A55_trim_authority.md). Skin depth and section masses computed here from those
inputs and from **declared** material densities.

**Nothing in this file is measured, and it is a scoping calculation rather than a run** — it has no
declared bands, it was not committed before its own arithmetic, and **it must not be cited as if it
were A66.**
