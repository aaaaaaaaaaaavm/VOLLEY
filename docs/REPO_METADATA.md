# Repository descriptions and topics

**The GitHub "About" text is not in any repository, so it cannot be corrected by any check here.**
It is the first thing a visitor reads and it drifted for exactly that reason: on 2026-08-14 the
flagship's still advertised **16.388 m/s and 10.533 g**, two corrections out of date, and read as a
specification rather than as a description of what the thing does.

**This file is the source. Applying it is manual** — GitHub exposes repository descriptions only
through settings or the API, and neither the propagation tools nor `check_links.py` can see them.
Same class as **P62**, where the published wiki drifted from its own source.

## How to apply

Repository → **About** (gear icon, top right) → set **Description**, **Website** and **Topics**.

---

## VOLLEY

> **Description**
>
> Giving rideshare CubeSats an orbit their host was not going to. An electromagnetic deployer that
> launches twelve satellites at individually commanded speeds, without modifying any of them. Open
> engineering record, with every defect published.

**Website:** `https://aaaaaaaaaaaavm.github.io/VOLLEY/`

**Topics:** `cubesat` `smallsat` `space-systems` `aerospace-engineering` `linear-motor`
`orbital-mechanics` `design-study` `open-science` `reproducible-research` `engineering-record`

## VOLLEY-paper

> **Description**
>
> Conference manuscript for VOLLEY, with every script, figure and acceptance test behind its
> numbers. Written so a reviewer can rerun the work rather than take it on trust.

**Topics:** `cubesat` `aerospace-engineering` `reproducible-research` `open-science` `manuscript`
`space-systems`

## VOLLEY-thesis

> **Description**
>
> Final-year thesis on VOLLEY: the manuscript, the analyses behind it, and the full record of what
> failed along the way. Submitted with its defects visible rather than tidied away.

**Topics:** `cubesat` `aerospace-engineering` `thesis` `space-systems` `reproducible-research`
`open-science`

## VOLLEY-lab

> **Description**
>
> The vault. Ideas from the VOLLEY programme that never became a complete thing, each kept with
> the measurement or the arithmetic that stopped it. Nothing here should be cited.

**Topics:** `cubesat` `aerospace-engineering` `research-notes` `design-exploration` `space-systems`

## BOLLEY

> **Description**
>
> The other answer to the same question: let a CubeSat carry a few hundred grams of passive
> hardware, and take kilograms of machinery off the launcher. Sibling study to VOLLEY, developed
> to the same standard.

**Topics:** `cubesat` `smallsat` `aerospace-engineering` `linear-induction-motor` `space-systems`
`design-study` `open-science`

## pulsed-linear-motor-design-lab

> **Description**
>
> An installable calculator for screening pulsed linear-motor stages: force, stroke, moving mass,
> source impedance and where the energy goes. Carries VOLLEY's reference calculation and the
> independent checks that qualify it.

**Topics:** `linear-motor` `electromagnetics` `python` `engineering-tools` `design-study`
`open-science` `reproducible-research`

## orbital-deployment-trade-study

> **Description**
>
> A calculator for the orbital side of deploying a satellite: the impulse it takes, how the fleet
> drifts apart afterwards, and what the push does to the vehicle that gave it. Not a conjunction
> or flight-safety tool.

**Topics:** `orbital-mechanics` `cubesat` `space-systems` `python` `engineering-tools`
`trade-study` `open-science`

## engineering-evidence-toolkit

> **Description**
>
> A command-line check that asks whether a repository's results, links and artifacts still agree
> with the sources they were computed from. Establishes consistency, never validity.

**Topics:** `reproducible-research` `research-software` `python` `cli` `open-science`
`engineering-tools` `continuous-integration`

## aaaaaaaaaaaavm (profile)

> **Description**
>
> GitHub profile repository. Not applicable — profile repositories show no About text.

---

## What these are written to avoid

**The old flagship text was a specification**: *"a magazine-fed ironless Halbach linear synchronous
motor that ejects unmodified 3U CubeSats at 16.388 m/s and 10.533 g."* Three problems with it.

**It answered the wrong question.** A description says what something is *for*. A reader who does
not already know what a Halbach array is learns nothing, and one who does still does not learn why
it exists.

**It carried numbers, so it went stale.** Two corrections later it advertised a velocity the
repository had withdrawn. **A description should contain no quantity that any analysis can move** —
that is what the README's tables are for, and they regenerate.

**It buried the honesty.** *"Design study, TRL 2-3; model only"* is the most important sentence in
it and it was last. The published defect record is the strongest thing about this work; it belongs
in the sentence, not the footnote.
