# ADR-021: Freeze the defect register at Phase I close

Status: Accepted, Date: 2026-08-10, Phase: I, Governs: `OPEN_PROBLEMS.md`

## Context

The register and the discipline around it are the reason anything in this repository can be
trusted. They are also, now, the largest consumer of effort in it, and the two facts have to be
stated together or this decision reads as giving up on rigour.

What the discipline bought. Bands declared before runs and defects published rather than
quietly fixed have caught, repeatedly, things that would otherwise be sitting in a published
paper: a minimum-separation figure wrong by 5.7x, an inter-array force 37 % high, an
invariance claim in the paper's own abstract falsified by an independent propagator, and
P38, a sentence in the manuscript that the project's own validation had disproved five days
earlier. None of that surfaces without the apparatus. It is not overhead and it was not a mistake.

What it now costs. Three measurements, taken 2026-08-10:

| | |
|---|---|
| Analysis code | ~3,200 lines |
| Prose about that code | ~16,000 lines across docs, run sheets, `CHANGELOG.md` and the register |
| Tools whose only job is policing the record | five, `register_status`, `check_links`, `check_artifacts`, `make_baseline`, `export_companion` |

Three signals that it has passed its useful point:

1. The apparatus has begun generating its own defect load. Of the three entries opened on
   2026-08-10, P38 is a defect in the paper and P39 is a defect in the file-copying semantics of
   the export tool. Both are real and both were correctly fixed. Neither has any bearing on
   whether the machine works. When the record-keeping machinery produces the defects the
   record-keeping machinery then tracks, the loop has closed on itself.

2. Analyses have started confirming rather than discovering. A19's headline output was
   "measure structural Q first". [`../STRUCTURAL_GAP.md`](../STRUCTURAL_GAP.md) said exactly that
   on 2026-08-06, four days earlier, with no sweep behind it. A19's quantification is worth
   having and it changed no action.

3. The cheapest decisive act remains untaken. B-1, a Halbach pair on a gaussmeter,
   roughly ₹22,000, bill of materials and safety case already written, has never been ordered,
   while seventeen model-against-model analyses were produced around it.

The one-line version: this project can state, to four significant figures, the field 70 mm from
an array that does not exist.

There is a subtler risk too. E4, nothing built or measured, is documented so thoroughly and
so honestly that it has stopped reading as a problem to solve and started reading as a disclosed
property of the work. A permanent caveat can quietly become permission.

## Decision

`OPEN_PROBLEMS.md` is frozen. It remains authoritative and is closed to new entries except in
three cases.

A new numbered entry may be opened only for:

1. A defect in the machine, an error in the design, or in a model of it, that changes what
   the hardware would do.
2. A defect that makes a published Phase I deliverable wrong, the paper, `BASELINE.md`, the
   portfolio. This is the P38 case and it stays numbered, because a wrong published claim is the
   thing the register exists for.
3. A validation band miss. `validation/README.md`'s rule is unchanged: a missed band produces
   a numbered defect, never a widened band.

Everything else is fixed in place with a `CHANGELOG.md` line and no number. Specifically
barred from the register:

- Defects in `tools/`. The apparatus is not the product. P39 would not be numbered under this
  rule.
- Bookkeeping drift, stale cross-references, count mismatches, a document quoting a
  superseded figure. Fix it and log it.
- Observations about the register itself.
- Anything whose motivation is *better* rather than *correct*, which already belongs in
  [`../VAULT.md`](../VAULT.md) and `VOLLEY-lab`.

The headline counts stop being propagated. `OPEN_PROBLEMS.md` carries the count, derived by
`tools/register_status.py`. `KILL_CRITERIA.md`, `ROADMAP.md` and `PHASE_I_CLOSURE.md` now point at
the register instead of restating its numbers. Five places quoting one number was five chances
to drift and a recurring tax on every register change, and it bought nothing a reader could not
get by following one link.

## What this is not

Nothing is deleted, closed, or downgraded. All 67 entries stay, with their dispositions
intact. The 29 live items are still live and still carry their named next steps. A freeze is not
a purge, and a register that quietly shed its inconvenient entries would destroy the only thing
this project has instead of hardware.

It is not retroactive. P38 and P39 keep their numbers. This project does not rewrite its
record, and re-numbering yesterday's entries under today's rule is exactly that.

It does not touch the band rule, which is the load-bearing half of the discipline and is not
what became expensive. Bands are still declared before runs, still never widened after one, still
produce a numbered defect when missed.

It does not apply to Phase II. `VOLLEY-lab` has no baseline and makes no stability promise.
Its register is not frozen.

It is not permanent. The freeze is reviewed at the next baseline boundary. If Phase II opens
with hardware in it, the register that matters will be a different one anyway.

## Consequences

- The effort released goes to measurement, in the order
  [`../ROADMAP.md`](../ROADMAP.md) now carries: B-1 first, then the two owner decisions
  that block the most downstream work (P29 stator segmentation, P9 target host class),
  neither of which is waiting on analysis.
- `PHASE_I_CLOSURE.md`'s framing is unaffected, Phase I still ends with E4 open, categories D
  and E open with named owners, and that is still the defensible end state.
- The risk this accepts, stated rather than hidden: a real defect in `tools/` will now be
  fixed and logged rather than tracked, so it is possible for one to be forgotten. That is judged
  cheaper than the alternative, on the evidence that the last two apparatus defects consumed a
  working session between them while three kill criteria sat crossed and unmoved.

## Validation

None. This is a governance decision, and the thing that would falsify it is simple and worth
naming in advance: if the next machine-level defect is found late because attention moved off
the register, this ADR was wrong. The counter-test is whether B-1 gets ordered.
