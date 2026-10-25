# VOLLEY prototype design-review requirements

**25 October 2026.** VOLLEY-G5-ACR1 is the completed computational design reference. This record defines the evidence required before a named future article can receive a build/test release. Physical prototyping and flight acceptance remain subsequent stages. The [project boundary](PROJECT_BOUNDARY.md) excludes separate side-project completion dependencies.

## Evaluated and future configurations

[ACR1](../validation/acr1/README.md) evaluates twelve nominal 4 kg 3U surrogates with guided lead-screw feed, a positively restrained transfer cradle and retained launch sled. The selected FM08-R3 mixed-size feeder remains a separate subsystem study. Original Gen5 interference, mass and performance findings retain their historical configuration.

Gen6 physical development and mixed 1U/3U handling are separately versioned. They require a named test article, payload/contact envelopes, installed hardware and instrumentation tied to the intended operating cases. Existing computational selection does not provide measured reliability, actual host/provider acceptance or hardware ratings.

## Review gates

| Gate | Required evidence | Closure boundary |
|:--|:--|:--|
| Mission and requirements | Payload envelope, target states/epoch, service case, accuracy/load limits, host assumptions and matched conventional comparator | Sources and assumptions distinguished; unknown provider limits retained |
| Architecture | Equal-boundary candidate trade, installed resources and failed criteria | Mandatory safety/fit gates precede weighted scoring |
| Feed and restraint | Full selected-cell transfer/reset, independently locked storage, bridge/docking and interrupted-transfer behavior | Complete CAD/STEP, swept motion, tolerance/load/contact and fault evidence |
| Accelerator and source | Winding/drive/source selection, force map, coupled circuit and thermal histories | Actual component ratings, numerical checks and uncertainty; no inherited rating |
| Structure and materials | Launch/retained/operating/fault load paths, stiffness, thermal distortion, fits and material sources | Provisional environmental screens separated from provider qualification |
| Sled arrest and return | Capture/brake energy, peak loads, heat, reset and rebound/recontact | Same moving mass, geometry and duty as the selected article |
| Installed resources | Full BOM, mass/CG/inertia, energy, charging, volume, harness, supports, cooling and cost | Count omitted/unknown hardware explicitly |
| Controls and safety | Command/inhibit/charge/feed/release/catch states and sensor/reset/jam/power faults | Containment demonstrated; retries only under verified recovery logic |
| Host campaign | Changing mass/recoil, attitude recovery, maneuvers, settling, charging and disposal | Coupled sequential mission; no sparse-sample clearance claim |
| Manufacturing definition | Editable CAD, valid STEP, dimensioned drawings, datums, tolerances, assembly/access/inspection | Controlled source and export identity |
| Experiment definition | Smallest discriminating coupon, calibrated instrumentation and predetermined pass/rework/stop criteria | Proposed tests remain unrun until actual measurements exist |
| Independent review | Reproducible package, technical feedback and resolved or signed-open discrepancies | External acceptance cannot be supplied by a software check |

## Change control

Geometry or component changes reopen every affected load, field, thermal, motion, mass and mission result. Preserve earlier records and explicitly identify new evidence cutoffs. The report and companion paper can present a bounded negative finding; an unsuccessful design is not relabelled build ready.

Physical manufacture, repeated-release measurements, environmental tests, provider approval and flight demonstration remain later evidence stages. Presentation images and animations explain a configuration; they cannot substitute for those stages.
