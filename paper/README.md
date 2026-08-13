# The paper

`paper.tex` is the source. `VOLLEY_IEEE_Conference.pdf` is the last compiled build.

**Rebuilt 2026-08-10 (third pass)** from the current source with pdfTeX (TeX Live 2023):
**13 pages, zero undefined references, zero missing figures, zero errors.** Source and PDF agree. The one-page CV was
regenerated from `analysis/results/*.json` and rebuilt in the same environment on 2026-08-06
and is unchanged by this build.

To rebuild: run `pdflatex paper.tex` from this directory until the cross-references settle
(three passes from a clean build), or upload `paper.tex`, `IEEEtran.cls` and `figures/` to Overleaf.

## What changed in the current build

**2026-08-10, second pass.** Three factual corrections and two additions. The retention gate now
states **two D9 pins at 41.0 kN**, margin **+0.45 at Q = 30**, after A22 resized it — the text
previously described a negative margin as an open problem. Tip-off is rewritten to A23's result:
the release is comfortable because it happens 12.2 ms into coast at zero force, and the risk is
the **36–231 °/s** cradle arrival at the *start* of the stroke. The claim that the 10–20 s versus
1200 s cadence contradiction "remains open" is removed — **ADR-020 closed it at 1200 s**.
Added: the last-mile ConOps in §VII with its envelope bounded by A20, and the **7.5×**
lifetime-extension ratio from A21 in the abstract.

## What changed in the third pass, 2026-08-10

**Five corrections and one new subsection**, all from work that landed after the second pass and
from the external review recorded in [`docs/REVIEW_RESPONSES.md`](../docs/REVIEW_RESPONSES.md).

1. **The abstract's 7.5× now carries its counterpart.** That ratio compares *gains*; on
   **delivered orbital life** it is **1.50**, which is the figure a risk-weighted comparison must
   use because a satellite the deployer fails to release delivers nothing. E30-02.
2. **The limitations section is rewritten where it had gone stale.** Three-dimensional field
   closure is no longer "open": resolving the field across the array's 90 mm depth rather than
   sampling the centre plane and multiplying **reduces K<sub>t</sub> by 4.42 %** to 10.54 and
   v_exit to 16.03 m/s. **That correction is computed and deliberately not applied** — it has not
   been checked by a method that solves a field equation in 3-D, and re-baselining onto an
   unchecked number would repeat the error it identifies (**P46**). The ESR sentence now records
   that a flywheel clears the ceiling at 35 mΩ against 68, at mass parity (**A25**).
3. **A new subsection, "Architecture reliability, and the bar it sets."** **Nine of thirteen
   elements forfeit the remaining manifest on a single failure, against zero for a spring
   dispenser.** Matching a spring on satellite count needs p = 0.9985 and is unrealistic;
   matching on delivered life needs p = 0.9347, i.e. **r ≥ 0.99326 per element per cycle** — the
   first quantitative reliability requirement the design has carried, and unmeasured. Segmentation
   is analysed as genuine redundancy **except at the breech segment**, where no force acts on a
   stationary sled.
4. **The FMEA table's sled-jam row is corrected.** It claimed the dual-cassette split bounds a jam
   to half the manifest. It does not: that bounds an *escapement or gate* fault, and **one sled
   serves all twelve cells.**
5. **The payload-family table gains a footnote.** Its counts are volumetric; the fixed-cell design
   study replaces them where a cell exists — **1U gives 36 per load at 2.125 kg, not 40 at 1.92**,
   and **ThinSat and 12U are refused outright** (**A24**).
6. **The conclusion is narrowed.** The linear motor is selected for **commandability, not
   performance** — a screw cannot reach the velocity and a ~1.8 kg spring can, failing only in
   that its velocity is built in rather than commanded (**A27**).

**2026-08-10, the payload magnetic environment (P34, P38).** Sec. VII gains the inward-facing
half of the interface, and Sec. on space environment and EMC has a falsified sentence removed:
it claimed a magnetometer-carrying customer payload "sees a field comparable to a conventional
reaction-wheel assembly at the same standoff", which A14 band 4 had already falsified at 611×
magnetometer full scale five days earlier. See `docs/PAYLOAD_ENVIRONMENT.md`.

The three groups below are from the 2026-08-06 build and still describe the rated point:

1. **The rated point moved.** The sled mass was computed as 9.445 kg from the Gen3 CAD solid volumes, against the 4.86 kg the parametric model assumed (P15). Exit velocity is now
   16.4 m/s at 10.5 g, efficiency 21.0 %, lifetime multiplier x1.62, dry mass 76.5 kg. This
   was not a judgement call after the fact: `validation/A4_sled_structural.md` fixed the
   consequence of each mass band **before** the structural analysis ran, and the ≥ 6.80 kg
   branch is the one that fired.
2. **The invariance claim is gone** (P16). GMAT falsified it, and Sec. V-B now explains why
   the sweep that supported it could never have detected a problem.
3. **Two claims the CAD contradicted are corrected** (P12): the ESPA-Grande envelope is
   stated as a requirement the geometry does not yet meet, and the "not detailed CAD"
   limitation is replaced by what the CAD actually says.

## Figures

`figures/F*.png` are regenerated by **`make_figures.py`**, which imports `analysis/`
directly. Run `python3 paper/make_figures.py` after any change to the operating point.

`D01_block.png` and `D02_layout.png` are schematics, not plots, see
`legacy/make_diagrams.py`.

## Archive

`archive/` holds superseded builds. Nothing in it should be cited; see its own README.

## Licensing, and why this directory is a separate case

The **reproducibility package** — `make_figures.py`, `make_animation.py`, `figures/` and these
build notes — is **CC BY 4.0**, like the rest of the repository. See [`../LICENSING.md`](../LICENSING.md).

**The manuscript is different.** `paper.tex` and the compiled PDF are published here under
CC BY 4.0 **today, and that position is provisional**: if the manuscript is accepted for
publication, **an IEEE copyright transfer would supersede this licence for the accepted
version**. This repository cannot license rights it has transferred, and the preprint published
here would not automatically carry the same terms as the accepted paper.

**Nothing about the analysis changes.** The scripts, the results, and the run sheets the
manuscript draws on stay CC BY 4.0 regardless of what happens to the manuscript itself, which is
the practical reason the two are separated here rather than treated as one artifact.
