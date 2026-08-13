# Licensing

**The whole of this repository is licensed under the Creative Commons Attribution 4.0
International License (CC BY 4.0).** The full legal text is in [`LICENSE`](LICENSE); the
attribution form is in [`NOTICE`](NOTICE).

**A single licence, at the root, with no directory split.**

| Directory | Licence |
|---|---|
| `analysis/` | CC BY 4.0 |
| `cad/` | CC BY 4.0 |
| `docs/` | CC BY 4.0 |
| `legacy/` | CC BY 4.0 |
| `paper/` | CC BY 4.0 — **except the IEEE manuscript, see below** |
| `tools/` | CC BY 4.0 |
| `validation/` | CC BY 4.0 |
| `wiki/` | CC BY 4.0 |
| `.github/` | CC BY 4.0 |
| Root files | CC BY 4.0 |

## Why one licence rather than a code/documents split

A split placing a code licence on `analysis/` and `tools/` was considered and **rejected**.
This repository does not separate cleanly into code and documents: `validation/` holds fourteen
Python files alongside its run sheets, `cad/` holds three generator scripts including the one
that produces the geometry, and `paper/` holds three figure generators. More importantly,
`analysis/` is not incidental tooling — `motor_model.py` computes the thrust constant and the
operating point, and `sizing.py` sets the geometry. **That code is the design expressed
executably**, not machinery around it.

A carve-out would therefore have drawn a line through the middle of the same disclosure. One
licence over everything is the simpler and more defensible position.

## What this change does not do

**This is not retroactive.** Snapshots of this repository taken before this change — clones,
forks, archives, and every commit reachable before it — **remain available under the MIT
licence** they carried at the time. The previous licence text is retained at
[`LICENSE-MIT-superseded`](LICENSE-MIT-superseded) for that reason. Nothing here revokes rights
already granted.

## The IEEE manuscript

`paper/` contains two different things:

- **The reproducibility package** — `make_figures.py`, `make_animation.py`, `figures/`, and the
  build notes — is CC BY 4.0 like the rest of the repository.
- **The manuscript itself** (`paper.tex` and the compiled PDF) is CC BY 4.0 **as published here
  today**, and that position is provisional. **If the manuscript is accepted for publication, an
  IEEE copyright transfer would supersede this licence for the accepted version.** This
  repository cannot license rights it has transferred. See [`paper/README.md`](paper/README.md).

## Attribution

CC BY 4.0 requires credit, a link to the licence, and **an indication of whether changes were
made**. The last of those is the one most often skipped, and for an engineering record where
numbers have moved and are documented as having moved, it is the one that matters most.
