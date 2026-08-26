# ADR-028: no LaTeX in the flagship; the manuscript is authored in its own repository

Status: Accepted, Date: 2026-08-13, Phase: I, Changes: ADR-017

## Context

[ADR-017](017-four-repositories.md) made `VOLLEY-paper` and `VOLLEY-thesis` generated
companions: `tools/export_companion.py` writes them wholesale from the flagship, nothing in them
is authored, and a hand-edit is answered by deleting and regenerating rather than by reconciling.
That is still the right rule for the *reproducibility payload*, the scripts, the run sheets, the
figures and the baseline, and it is what keeps `16.388 m/s` from forking across four
repositories.

It was the wrong rule for the manuscript. A `.tex` file is not a derived artefact. It is
written, revised, submitted, reviewed and revised again, and it acquires a copyright status of
its own: an IEEE transfer on acceptance would supersede whatever licence the flagship stamps on
it, which is why `PAPER_MANIFEST` already carried a deliberate licence hold rather than the
flagship's own `LICENSE`. A file the flagship cannot license is not a file the flagship should
own.

And it made the flagship the wrong shape. This repository is an engineering record. It was
carrying a LaTeX class file, a 1.6 MB compiled PDF, an archived superseded PDF, a CV and its
generator, none of which any analysis reads, and all of which had to be rebuilt, page-counted
and re-committed on every pass.

## Decision

The flagship holds no LaTeX, no `.cls`, and no compiled PDF.

| Moves to | What |
|---|---|
| VOLLEY-paper, authored | `paper.tex`, `IEEEtran.cls`, the built PDF, `archive/`, `cv/` and `make_cv.py` |
| VOLLEY-thesis, authored | `source/paper.tex`, `IEEEtran.cls`, the built PDF |

What stays in the flagship is the figures and their generators, relocated to `figures/` with
`tools/make_figures.py` and `tools/make_animation.py`. A figure is a *result*, it is drawn from
`analysis/` and it is what `docs/FIGURE_INDEX.md` indexes, so it belongs in the engineering
record whether or not a paper ever cites it.

`export_companion.py` no longer wipes the companion. It removes and rewrites only the paths
in its own manifest. Anything else in a companion is authored and is preserved. Until this
change the tool called `shutil.rmtree(dest)`, so running it after this move would have deleted
the paper.

## Alternatives

Keep generating the manuscript from the flagship. Rejected. It forces every editorial pass
through a regeneration step, and it means the flagship stamps a licence on a document whose
rights may already have been transferred.

Move the figures out too, with the paper. Rejected. The figures are outputs of `analysis/`
and inputs to the run sheets and to `docs/FIGURE_INDEX.md`. Moving them would leave the
engineering record unable to show its own results, and would put a generator that imports
`motor_model` in a repository that only receives a copy of it.

Leave everything and just tidy the README. Rejected as the version of this decision that
changes nothing. The complaint is not aesthetic: a compiled PDF in an engineering record is an
artefact nothing here can verify, guard, or rebuild without a LaTeX install that
`tools/env-setup.sh` had to carry for that reason alone.

## Consequences

The flagship is smaller and every remaining file is checkable. No artifact in it now requires
a TeX engine, so `tools/check_artifacts.py` loses the two pairs it could only verify by page
count, and `tools/env-setup.sh`'s LaTeX dependency exists for nothing in this repository.

The companions stop being purely generated, and that has to be said plainly. `VOLLEY-paper`
is now *authored manuscript + generated payload*. The ADR-017 rule, "if a companion is ever
hand-edited, delete and regenerate it", now applies only to the manifest paths. Deleting
`VOLLEY-paper` wholesale would destroy authored work, which was not true yesterday.

Historical references are not rewritten. `CHANGELOG.md` and `OPEN_PROBLEMS.md` describe
edits made to `paper/paper.tex` on dates when that path existed. They are the audit record and
this project does not rewrite its record; the paths in them are historical facts, not links.

## Validation

How we would find out this is wrong.

- A number forks between the manuscript and the scripts. This is the failure ADR-017 existed
 to prevent, and moving the manuscript out is exactly the move that could reintroduce it. The
  guard is that the *figures and the reproducibility payload are still generated* from here, so a
  fork can only occur in body text, and `tools/make_baseline.py --check` still holds the 23
  values that text quotes.
- A regeneration deletes authored work. The per-manifest removal above is the fix; if it is
  ever reverted to a wholesale `rmtree`, the paper is lost. That is worth a test, and there is
  not one.
- The flagship stops being able to show its own results. If `figures/` ever drifts out of the
  flagship after this, the engineering record has been hollowed out and this decision went too
  far.
