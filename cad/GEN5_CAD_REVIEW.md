---
title: "VOLLEY Gen5 — CAD review and interface disposition"
subtitle: "Reference assembly, FreeCAD 1.0 export, 9 October 2026"
author: "VOLLEY computational design record"
date: "9 October 2026"
header-includes:
  - \usepackage{graphicx}
---

# Executive disposition

**Status: reviewable geometry; side-fed fit failed; no manufacturing or flight release.** This package contains eight dimension-controlled Gen5 B-rep parts, eight FreeCAD-exported STEP parts, a native 20-instance FreeCAD document, two STEP assembly exports, a measured exact-solid interference, and the configuration/mass evidence needed to interpret them. The as-drawn side-fed reference placement has an **11 mm transverse shortfall before clearance** and **32,915 mm³ track/cassette intersection per side**. That is a failed geometry check, not an illustration to conceal.

The installed enclosure is 1839 × 530 × 940 mm. A quoted ESPA Grande class length of roughly 1270 mm is a *comparison only*; it is exceeded by about 44%. There is no approved host interface control document. The modeled dry mass is 126.6 kg and incorporates estimates and a historical Gen3 sled solid-volume input; it is not a measured FreeCAD assembly mass.

# Software and released CAD files

The B-rep geometry is generated with CadQuery 2.8.0/OpenCascade 7.9.3.1 from `cad/parameters.json`. FreeCAD 1.0.0 imports those eight STEP shapes into named `Part::Feature` instances, saves a native `Gen5_Review.FCStd`, exports each source part through FreeCAD to `step/freecad_gen5/`, and exports the assembly to `VOLLEY_Review_Assembly_FreeCAD_Gen5.step`. A separate CadQuery assembly STEP records the same placement. The FreeCAD document preserves part identity, placement, source-file SHA-256 and review status; the imported solids do not have editable native FreeCAD feature histories.

- [Parameter file](parameters.json): coordinate frame and dimensions; some details provisional.
- [Eight source STEP parts](step/gen5/): CadQuery B-rep solids.
- [Native FreeCAD document](native/Gen5_Review.FCStd): 20 named instances; review placement only.
- [Eight FreeCAD STEP parts](step/freecad_gen5/): shape and 0.01 mm³ volume read-back band passed.
- [FreeCAD assembly STEP](step/gen5/VOLLEY_Review_Assembly_FreeCAD_Gen5.step): valid read-back; side-fed packaging **fails**.
- [FreeCAD export report](FREECAD_EXPORT.json): software version, file hashes and exact-solid overlap.
- [Source assembly report](REVIEW_ASSEMBLY.json): placements, source hashes and width calculation.

The first view below is a **Blender render of the Gen5 geometry**. It is a visualization, not a photograph of built hardware or a solver screenshot. The section below it is generated from the CAD dimensions and exact-solid intersection report.

\begin{center}
\includegraphics[width=0.70\linewidth]{renders/gen5/hero_open.png}\\
\small Figure 1. Blender render of the Gen5 geometric model (visualization only).
\end{center}

\begin{center}
\includegraphics[height=0.43\textheight]{../figures/gen5_packaging_section.png}\\
\small Figure 2. Transverse reference placement; red regions mark the track/cassette clash.
\end{center}

# Packaging and interface check

In the declared first-cell side-fed placement, the inside width of the 530 mm enclosure after two 2 mm skins is 526 mm. The 205 mm track plus two 166 mm cassette widths requires 537 mm. Placing each cassette against an inside wall gives zero side-wall clearance and an 11 mm combined shortfall. FreeCAD and CadQuery independently evaluate the imported exact solids at this placement and both find 32,915 mm³ of track/cassette overlap per side. The FreeCAD native document retains the collision so a reviewer can inspect it. The width calculation does not prove that *every possible architecture* fails; a new feeder geometry, vertical separation, cutout or enclosure would need a new configuration and full analysis.

The cassette placement is a reference assumption, not a specified joint or feed stroke. The 12 payload shapes are envelope proxies, not any named flight CubeSats. Static overlap screening does not cover a moving payload, door opening, jam clearing, retraction or emergency safe state. No tolerance stack, thermal distortion, harness routing, end-turn volume, fastener access, provider keep-out or launch load path has been closed. The ring flange shape is a reference mounting geometry, not a provider-approved ESPA interface.

# Mass and structural boundary

The [generated BOM](BOM.md) includes enclosure skins, frames, radiator, equipment bays and brackets added by A46; older prose saying these lines are absent was corrected at this review. The 126.6 kg modeled dry total still mixes geometry-derived, modelled and assumed entries. The 9.445 kg sled is adopted from historical Gen3 STEP solid volumes. FreeCAD volumes of the current assembly are **not** a replacement mass ledger: STEP bodies include proxy materials and the 12 payload solids, while wiring, purchased components, joints and host reinforcement do not have complete flight geometry. The A4 structural check used a specific earlier chassis idealization; it is not an assembled moving-load verification for this STEP.

# Reproduction and disposition

Run `python3 cad/build_gen5.py --check`; then `python3 cad/build_review_assembly.py` and `python3 cad/plot_review_packaging.py` in the repository's declared Python environment. Run `/usr/bin/python3 cad/freecad_export_review.py` with FreeCAD 1.0 available. The source and FreeCAD SHA-256 lists are in the two JSON reports. `cad/native/Gen5_Review.FCStd` can be opened in a FreeCAD GUI for component inspection. The two assembly STEP exports and eight FreeCAD part exports can be independently imported in another STEP reader. FreeCAD read-back validates topology/volume as described; it does not qualify manufacturability or payload compatibility.

**Review decision:** retain Gen5 as the fixed *evaluated academic configuration*, report this packaging failure alongside the mass failure, and do not mark the mechanical design flight-ready. A future redesign that removes the clash is a new configuration requiring renewed mass, force, power, thermal, structural and mission calculations.
