# ADR-029: Phase I closes on Gen5; Gen6 is the Phase II design target

**Status:** Accepted · **Date:** 2026-08-13 · **Phase:** I · **Governs:** the Phase I/II boundary

## Context

On 2026-08-13 an architecture exploration ran from a single question — whether "unmodified
CubeSat" is worth defending — through four rejected or superseded proposals to a candidate that
survives three sittings: a **linear induction drive on a passive aluminium mover**, with no
magnets, no 9.445 kg sled, no brake worth the name, and the satellite untouched.

**On every axis that has been measured, it beats Gen5.** It is also, today, nine measured bands
against Gen5's hundred analyses.

**And the exploration itself demonstrated the failure mode [ADR-021](021-freeze-the-register.md)
froze the register to stop.** Six register entries were opened in one day:

| | A defect in the machine? |
|---|---|
| **P47** — the published velocity-loop gain was linearly unstable | **yes** |
| **P52** — 30 % segment-handover ripple through a 48 Hz track mode | **yes**, and it belongs to Gen6 |
| P48, P49, P50, P51 | **no** — all four are defects in analyses written that day |

**Two of six are about the design.** Four are the apparatus generating its own workload, which is
what ADR-021 predicted in the sentence *"when the record-keeping machinery produces the defects
the record-keeping machinery then tracks, the loop has closed on itself."*

**Meanwhile B-1 — one measurement, ₹22,000, bill of materials written 2026-07-30 — is still
unordered.** It has been the top of the roadmap since ADR-021 and it is the only available action
that changes the *category* of this project's evidence rather than its degree.

The project does not have an engineering problem. **It has a stopping problem:** no definition of
"done" exists that does not require one more analysis, so there is always one more analysis.

## Decision

**Phase I closes on Gen5. Gen6 is the Phase II design target and is not built.**

1. **Gen5 is frozen** as the Phase I design — the baseline, the CAD, the paper, the cost model
   and the mass rollup all continue to describe it, unchanged.
2. **Gen6 — the passive-mover linear induction architecture — is recorded as the Phase II design
   target**, in `PHASE_II.md` and `GEN6_ARCHITECTURE.md`, with its nine measured bands and its
   unsized remainder both stated. It is promoted at a baseline boundary or not at all.
3. **Phase I is not re-baselined onto it.** That would move K<sub>t</sub>, v_exit, the mass
   rollup, the cost model, the CAD and the manuscript — to replace an architecture with a hundred
   analyses by one with nine bands.
4. **No further architecture exploration before B-1.** Exploration does not terminate on its own;
   it terminates when it is stopped.

**P52 is not a Phase I blocker.** Gen5's winding is segmented *for fault isolation and driven as
one section* ([ADR-022](022-stator-segmented-not-block-commutated.md)), so it has no segment
handover. P52 is a property of the Gen6 drive and travels with it.

## Alternatives

**Re-baseline Phase I onto Gen6 now.** Rejected on cost and evidence. Months of propagation, and
the twin-fin geometry, the retention, the release, the 850 mm stroke and the stator iron have
**zero** bands between them. The rail proposal also looked excellent until its first band.

**Keep exploring until an architecture closes every kill criterion.** Rejected: none does. Kill
criterion 1 fails at 3U in every variant examined, and the search has no natural end.

**Drop Gen6 and stop.** Rejected. The finding is real, measured, and is the natural forward
chapter of the thesis: *a passive aluminium mover beats a permanent-magnet sled on every axis
that has been measured*. It does not need metal to be worth publishing.

## Consequences

**Phase I closes with a bounded remaining list rather than an empty register**, which is what
[`../PHASE_I_CLOSURE.md`](../PHASE_I_CLOSURE.md) §9 defined as a defensible end state on
2026-08-05: categories A, B and C closed; D, E and **E4** open with named owners.

**The paper describes Gen5 and does not mention Gen6.** A manuscript that hedges between two
architectures argues for neither.

**Gen6's own defects stay with Gen6.** P52, the twin-fin geometry and the retention question are
Phase II debt and are not counted against Phase I.

**The cost is stated plainly: Phase I closes on an architecture its own author now believes is
second-best.** That is the correct trade — a finished, honest, checkable Phase I is worth more
than an unfinished better one — but it is a real cost and pretending otherwise would be the
dishonest version of this decision.

## Validation

**How we would find out this is wrong.**

- **B-1 is still unordered in a month.** Then the stopping rule did not bind and this ADR bought
  nothing. That is the single measurable test of whether this decision worked.
- **A measured K<sub>t</sub> departs materially from 11.03 N per kA/m.** Then Gen5's design point
  moves, and so does Gen6's, because both descend from the same field model. Freezing Gen5 would
  not have been wrong; it would have been beside the point.
- **Gen6's unsized remainder turns out to contain a band 1.** The rail drive died on its first
  band and this ADR assumes Gen6 will not. If the twin-fin geometry or the retention fails
  similarly, then holding Phase I on Gen5 was worth more than it looks here.
- **The thesis is weaker for carrying two architectures.** If a reader finds the Gen6 chapter
  reads as indecision rather than as a result, the boundary was drawn in the wrong place.
