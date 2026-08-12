# FMEA: what each failure costs, and what the design has to achieve

**Answers review items 20 and 22, and converts E30 from a criticism into a requirement.**

E30 established the architecture's shape and the two numbers that decide whether the trade is
worth taking, then found that **nothing estimated per-shot reliability**. This does.

> **This is not a reliability prediction.** No element below has a measured failure rate, a
> qualification history, or a cycle-life test behind it. Per-cycle reliability is a **parameter,
> swept rather than asserted**, and the useful output is the inverse question: *given this
> architecture, what must each element achieve for the design to beat a spring at all?*
> **Anyone quoting a single p from this file is misusing it.**

## Single-failure-loses-N

| Element | Scope | Cycles | A single failure costs |
|---|---|---:|---|
| Sled chassis and rollers | **shared** | 12 | **all remaining** |
| Stator winding | **shared** | 12 | **all remaining** |
| Power converter (SiC bridge) | **shared** | 12 | **all remaining** |
| Energy store (bank or flywheel) | **shared** | 12 | **all remaining** |
| Avionics and shot sequencer | **shared** | 12 | **all remaining** |
| Position sensing / commutation | **shared** | 12 | **all remaining** |
| Eddy brake | **shared** | 12 | **all remaining** |
| Sled return | **shared** | 12 | **all remaining** |
| Launch lock release | **shared** | 1 | **all** |
| Cassette follower drive | cassette | 6 | six |
| Escapement | cassette | 6 | six |
| Retention gate (2 × D9 pins) | cassette | 6 | six |
| Individual release event | shot | 1 | one |

> **Nine of thirteen elements forfeit the remaining manifest on a single failure.**
> **A spring dispenser has zero such elements** — every failure costs exactly one satellite.
>
> **Revised 2026-08-10:** segmentation analysis moves the stator from *forfeits* to *degrades*
> for all but its breech segment, so the honest count is **eight and a fraction**, not nine. The
> table above is left as first computed; the correction is in the mitigations section.
>
> **Nine shared elements × twelve cycles is 108 chances to fail.**

**This is the answer to review item 22.** A jammed sled is not a special case to be analysed
separately; it is one of nine ways to lose the manifest, and the sled is simply the most obvious.
There is **no redundant sled, no manual release, and no recovery mode** anywhere in the design.

## What the architecture delivers

| Per-element per-cycle reliability | Effective p per shot | Expected satellites | vs a 0.99 spring (11.88) |
|---:|---:|---:|---:|
| 0.9999 | 0.9990 | **11.92** | +0.04 |
| **0.999** | 0.9895 | **11.26** | −0.62 |
| 0.995 | 0.9487 | **8.80** | −3.08 |
| 0.99 | 0.8998 | **6.62** | −5.26 |
| 0.98 | 0.8089 | 4.02 | −7.86 |
| 0.95 | 0.5836 | 1.37 | −10.51 |

**The fall-off is brutal and it is structural, not pessimistic.** Dropping per-element reliability
from 0.999 to 0.99 — a factor of ten in element quality — costs **more than four satellites**,
because the penalty compounds over 108 opportunities.

## The requirement, which is the useful output

| To match a 0.99-reliable spring | Requires, per element per cycle |
|---|---:|
| On **delivered orbital life** (7.95 satellites suffice, since each is worth 1.495×) | **r ≥ 0.99326** |
| On **satellite count** (11.88 satellites) | **r ≥ 0.99984** |

**0.99326 per element per cycle is the design requirement.** At that value each element survives
the twelve-cycle campaign with probability **0.9220** — which is a demanding but not unreasonable
target for qualified space mechanisms, and is the first quantitative reliability requirement this
project has ever had.

**0.99984 is not a realistic target** for a twelve-cycle electromechanical system with no flight
heritage. **VOLLEY should not be sold on satellite count**; on that metric a spring wins and will
keep winning.

## What this changes about the product argument

**The honest claim is not "as reliable as a spring."** It is:

> Above **r ≈ 0.9933** per element per cycle, VOLLEY delivers **fewer satellites** than a spring
> and **more total mission value**, because each satellite it delivers is worth 1.495× a
> spring-deployed one. Below that, it loses on both.

That is a narrower and more defensible claim than the repository has been making, and it is
falsifiable by test rather than by argument.

## Two mitigations that exist and are not credited

Both are real and **neither is in the numbers above**, because crediting them without analysis
would be exactly the optimism this file exists to avoid:

1. **The stator winding is segmented** (`paper.tex` §VII, and P29 closed the modelling half).
   **Analysed 2026-08-10 — `analysis/segment_redundancy.py` — and it mostly holds**, with one
   exception that matters:

   | Segments | Segment length | If a **later** segment dies | Still worth |
   |---:|---:|---:|---:|
   | 4 | 325 mm | **14.19 m/s (86.6 %)** | 1.41× a spring |
   | 8 | 162 mm | 15.33 m/s (93.6 %) | 1.45× a spring |
   | 12 | 108 mm | 15.69 m/s (95.8 %) | 1.47× a spring |

   **A dead segment is a length the sled coasts over, not a stopped machine** — provided the sled
   is already moving. **The breech segment is the exception: there is no force on a stationary
   sled, so if the first segment dies the shot never starts.**

   **So the stator is not one element, it is two.** The breech segment forfeits the manifest; every
   other segment degrades the shot. At four segments **three of four stator failures are
   survivable**; at twelve, eleven of twelve.

   **The design action this points at is cheap:** duplicate or overlap the breech segment, or
   provide any independent means of getting the sled moving. That converts the last
   manifest-forfeiting mode of the winding into a degradation.
2. **Retention gates are per-cassette**, so one gate failure forfeits six rather than twelve —
   already credited in the model's structure, but the escapement and follower share that scope
   and their cycle life is untested.

## What would close review items 20 and 22 properly

1. **Cycle-life tests** for the three cycling mechanisms — escapement, gate, sled. **This is
   metal, not computation**, and it is the only route to a defensible r.
2. **A segmentation redundancy analysis**, which is computation and could remove one of the nine.
3. **A jam recovery mode**, or an explicit accepted-risk statement with the number attached.
4. **Radiation and SEE qualification for the converter** (review item 25), which is currently one
   of the nine with no qualification path at all.

**Until 1 is done, r is unknown and the product claim above cannot be made.** That is the honest
position, and it is the same position B-1 occupies for the field model: **the analysis is done
and the measurement is not.**
