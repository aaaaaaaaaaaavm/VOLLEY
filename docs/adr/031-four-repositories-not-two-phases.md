# ADR-031: four repositories by role, replacing the two-phase model

Status: Accepted, Date: 2026-08-13, Supersedes: the phase model in
[`../programme/ENGINEERING_PROGRAMME.md`](../programme/ENGINEERING_PROGRAMME.md) §§2, 10 ·
Extends: [ADR-017](017-four-repositories.md)

## Context

The programme dossier defines two phases. Phase I develops three deliverables against a
frozen baseline; Phase II *"begins after Phase I and may fundamentally redesign any aspect."*
Phase I closed on 2026-08-13 ([ADR-029](029-phase-one-closes-on-gen5.md)).

The phase model did real work and it is worth saying what. The freeze is what made
`make_baseline.py --check`, the operating-point fork guard and the bands-before-scripts rule
mean anything, and the boundary is what allowed Gen6 to be developed and then *not* adopted on
the day it looked best. Without a line, the search does not terminate.

But the vocabulary costs more than it now buys. "Phase I" requires the reader to know the
dossier before anything parses. The boundary needs administering, the question *"is this Phase I
or Phase II?"* came up repeatedly through 2026-08-13 and consumed judgement each time. And the
phase model measures calendar position, while every decision that actually mattered turned on
evidence maturity: what has bands passed, what has been measured, what is stable enough to
publish.

The four repositories already encode that, and they do it without a glossary.

## Decision

The programme is described by the four repositories and their roles. The two-phase model is
retired as live vocabulary.

| Repository | Holds | Changes |
|---|---|---|
| VOLLEY-lab | Concepts that never became a complete thing, possibilities for the future, and the evidence behind them. A vault, not a graveyard | Freely. Nothing is protected |
| VOLLEY *(main)* | The authoritative engineering record. The concept, improved and optimised continuously | Freely, subject to the consistency checks below |
| VOLLEY-paper, VOLLEY-thesis | The same concept, at its most stable, reliable and proven form. Different scope, a conference contribution and a full submission, but not different designs | Improvable until presented or published. Frozen at that moment |

### The freeze is an external event, not an internal one

Paper and thesis freeze when presented or published, and not before. Until then they may be
improved, provided what enters them is stable, effective and reliable against the problem
statement.

That is deliberately a *quality* bar rather than a *calendar* bar. A submission date can slip and
a boundary can be argued with; publication cannot be argued with. It is the first hard,
external, unmovable line this programme has had.

### What replaces the phase gate

Maturity, in three tiers, each with a stated condition for crossing:

| From to to | Crossing condition |
|---|---|
| lab to main | Its acceptance bands have been declared before its script existed, and run. This is unchanged and is not negotiable |
| main to paper/thesis | Stable, effective and reliable against the problem statement. Not "interesting", not "better", *reliable* |
| paper/thesis to frozen | Presented or published |

Nothing crosses upward on enthusiasm. That was the point of the phase gate and it survives
the phase gate's retirement.

### One rule the vault needs

Every entry states why it stopped. PII-16 carries the measurement that killed it, a
transverse edge factor of 0.0253 against the 0.55 it was sized on. PII-17 carries the mass
arithmetic that declined it. That is what makes the vault evidence rather than a pile, and it
is the only rule the lab has.

## What this changes in practice, and what it does not

`docs/VAULT.md` becomes [`../VAULT.md`](../VAULT.md), the same eighteen entries, the same
entry criteria, renamed to what it is.

`docs/BASELINE.md`'s change control loses one clause and keeps the rest. The clause that goes
is *"performance improvement may not move the baseline"*, a pure freeze artefact, and main now
improves by design. Everything else stays, because none of it was about phases:

- a change must name its trigger;
- it must state which validations it invalidates, the P19 lesson;
- it must propagate in order: scripts, then figures, then paper, never the reverse;
- and it must be recorded in `CHANGELOG.md` and as an ADR.

The machinery is untouched and still means what it meant. `make_baseline.py --check` verifies
that the published values match the scripts *at every commit*; that is a consistency check, not a
freeze, and it works identically whether or not the numbers are allowed to move. The
operating-point fork guard in `sizing.py` refused eleven times during ADR-030's propagation and
would do so again tomorrow.

`PHASE_I_CLOSURE.md` keeps its name. It is the record of an event that was called that.

## Alternatives

Keep the phases. Rejected: the vocabulary requires a glossary, the gate requires an
administrator, and the thing it protects is better protected by a maturity condition.

Retire the phases and freeze nothing. Rejected. ADR-021 and ADR-029 are the two decisions
that stopped an unbounded search, and both depend on a line existing. The line moves from a
date to a publication; it does not disappear.

Cut a tag at each submission and freeze the tag instead of the repository. Considered and
declined as more machinery than the problem needs. Publication already produces a fixed artefact,
and a frozen repository is easier to explain to a reader than a tag policy.

## Consequences

A reader needs no glossary. Four repositories, four sentences, no roman numerals.

Main can improve without ceremony, which is what it does anyway and what
`GEN6_ARCHITECTURE.md` is queued for.

And the risk is named rather than hidden: main improving freely is exactly how the search
becomes unbounded again. The protection is that nothing reaches paper or thesis without being
reliable, and that the four verification tools still gate every commit. If a year from now main
carries three architectures and the paper carries none, this decision failed and ADR-029's
stopping rule should be reinstated as a date.

## Validation

How we would find out this is wrong.

- The paper stops tracking main. If what is in the manuscript and what is in `analysis/`
  diverge, the "reliable" bar is not being applied and the phase freeze was doing work this does
  not replace.
- The vault fills with entries that do not say why they stopped. Then it is a graveyard and
  the one rule was not enforced.
- `make_baseline.py --check` starts failing routinely rather than exceptionally. That would
  mean main is changing faster than it is being propagated, which is the P42 defect class at
  scale.
- Someone asks "what phase are we in?" and the answer matters. It should not.
