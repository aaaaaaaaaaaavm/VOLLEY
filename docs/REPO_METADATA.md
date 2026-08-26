# Repository descriptions and topics

The GitHub "About" text is not in any repository, so it cannot be corrected by any check here.
It is the first thing a visitor reads and it drifted for exactly that reason: on 2026-08-14 the
flagship's still advertised 16.388 m/s and 10.533 g, two corrections out of date, and read as a
specification rather than as a description of what the thing does.

This file is the source. Applying it is manual, GitHub exposes repository descriptions only
through settings or the API, and neither the propagation tools nor `check_links.py` can see them.
Same class as P62, where the published wiki drifted from its own source.

## How to apply

Repository to About (gear icon, top right) to set Description, Website and Topics.

> ## ⚠ NOT APPLIED AS OF 2026-08-22. The live text still differs on five repositories.
>
> Checked against the GitHub API on 2026-08-22. What is live now, and why it is wrong:
>
> | Repository | Live description says | Problem |
> |---|---|---|
> | BOLLEY | *"...move a few hundred grams of passive interface hardware onto the CubeSat and remove kilograms of active actuation, power electronics..."* | Materially wrong. BOLLEY *keeps* the windings, the switching, the sensing and the stored energy on the launcher. What it removes is the sled, the brake and the return stroke. The description describes a mechanically-mediated transfer that is not the architecture |
> | BOLLEY | no topics, no licence | see the entry below |
> | VOLLEY-paper | *"...Generated from the flagship; do not edit here"* | Contradicts [ADR-028](adr/028-no-latex-in-the-flagship.md): the manuscript is authored here. Only the reproducibility payload is generated |
> | VOLLEY-paper | licence shows MIT | corrected in the repository 2026-08-22; GitHub will re-read it on the next push. See that repository's `LICENSING.md` |
> | VOLLEY-lab | *"VOLLEY Phase II: research and redesign, where the frozen baseline does not apply"* | The README has been the vault framing since 2026-08-16. The description never followed |
> | VOLLEY | *"...magazine-fed electromagnetic launcher that mounts to a spent stage..."* | Not wrong, but it predates the current front page and reads as a specification |
> | aaaaaaaaaaaavm (profile) | no description | it is the target of a printed QR code |
>
> This is the one class of public surface no gate in this repository can reach, because GitHub
> keeps it outside the git tree. `tools/check_public.py` checks everything that *is* in the tree.

---

## VOLLEY

> Description
>
> Giving rideshare CubeSats an orbit their host was not going to. An electromagnetic deployer that
> launches twelve satellites at individually commanded speeds, without modifying any of them. Open
> engineering record, with every defect published.

Website: `https://aaaaaaaaaaaavm.github.io/VOLLEY/`

Topics: `cubesat` `smallsat` `space-systems` `aerospace-engineering` `linear-motor`
`orbital-mechanics` `design-study` `open-science` `reproducible-research` `engineering-record`

## VOLLEY-paper

> Description
>
> IEEE-formatted technical manuscript for VOLLEY, with every script, figure and acceptance test
> behind its numbers. Written so a reviewer can rerun the work rather than take it on trust.
> Unsubmitted; no venue selected.

Topics: `cubesat` `aerospace-engineering` `reproducible-research` `open-science` `manuscript`
`space-systems`

*The manuscript and its class file are authored here; the analysis, validation and figures are
generated from the flagship. The live description currently says the whole repository is generated
and must not be edited, which is the opposite of ADR-028.*

## VOLLEY-thesis

> Description
>
> Final-year thesis on VOLLEY: the manuscript, the analyses behind it, and the full record of what
> failed along the way. Submitted with its defects visible rather than tidied away.

Topics: `cubesat` `aerospace-engineering` `thesis` `space-systems` `reproducible-research`
`open-science`

## VOLLEY-lab

> Description
>
> The vault. Ideas from the VOLLEY programme that never became a complete thing, each kept with
> the computed result or the arithmetic that stopped it. Nothing here should be cited.

Topics: `cubesat` `aerospace-engineering` `research-notes` `design-exploration` `space-systems`

## BOLLEY

> Description
>
> The other answer to the same question: let a CubeSat carry a few hundred grams of passive
> hardware, and take kilograms of machinery off the launcher. Sibling study to VOLLEY, developed
> to the same standard.

Topics: `cubesat` `smallsat` `aerospace-engineering` `linear-induction-motor` `space-systems`
`design-study` `open-science`

Licence: none is currently declared, and that is a decision to take rather than a gap to paper
over. Every other public repository in the programme carries CC BY 4.0 (the toolkit, Apache 2.0).
BOLLEY carries no `LICENSE` file, so GitHub shows no licence and the default is "all rights
reserved". If it is meant to match the programme, copy the flagship's `LICENSE` and `NOTICE`
across; if the absence is deliberate, say so in its README so a reader is not left guessing.
*No licence has been invented for it here.*

## pulsed-linear-motor-design-lab

> Description
>
> An installable calculator for screening pulsed linear-motor stages: force, stroke, moving mass,
> source impedance and where the energy goes. Carries VOLLEY's reference calculation and the
> independent checks that qualify it.

Topics: `linear-motor` `electromagnetics` `python` `engineering-tools` `design-study`
`open-science` `reproducible-research`

## orbital-deployment-trade-study

> Description
>
> A calculator for the orbital side of deploying a satellite: the impulse it takes, how the fleet
> drifts apart afterwards, and what the push does to the vehicle that gave it. Not a conjunction
> or flight-safety tool.

Topics: `orbital-mechanics` `cubesat` `space-systems` `python` `engineering-tools`
`trade-study` `open-science`

## engineering-evidence-toolkit

> Description
>
> A command-line check that asks whether a repository's results, links and artifacts still agree
> with the sources they were computed from. Establishes consistency, never validity.

Topics: `reproducible-research` `research-software` `python` `cli` `open-science`
`engineering-tools` `continuous-integration`

## aaaaaaaaaaaavm (profile)

> Description
>
> GitHub profile repository. Not applicable, profile repositories show no About text.

---

## What these are written to avoid

The old flagship text was a specification: *"a magazine-fed ironless Halbach linear synchronous
motor that ejects unmodified 3U CubeSats at 16.388 m/s and 10.533 g."* Three problems with it.

It answered the wrong question. A description says what something is *for*. A reader who does
not already know what a Halbach array is learns nothing, and one who does still does not learn why
it exists.

It carried numbers, so it went stale. Two corrections later it advertised a velocity the
repository had withdrawn. A description should contain no quantity that any analysis can move,
that is what the README's tables are for, and they regenerate.

It buried the honesty. *"Design study, TRL 2-3; model only"* is the most important sentence in
it and it was last. The published defect record is the strongest thing about this work; it belongs
in the sentence, not the footnote.
