# Project continuity and work ownership

Updated 2026-09-17. This is the starting point when resuming work. Fetch current `main`, inspect the latest evidence and read the current workstream before editing. The programme has two coordinated workstreams.

**Latest restart and next-batch scope:** [17 September checkpoint](RESTART_20260917.md).
**Latest executed engineering batch:** [16 September review](REVIEW_20260916.md).
P113-S6 and P92-S2 have now run: 512 conditional error corners and 144 reference-cell
mechanical cases. They extend, but do not close, the mission/reference decision.
The previous two-workstream ownership split no longer implies separate active contributors.

| Workstream | Owns | First deliverable |
|---|---|---|
| [Mission and redesign](workstreams/MISSION_AND_REDESIGN.md) | Mission requirements, Gen6 reference falsification, configuration decision and selected release-cell integration | Add the uncertainty/settling terms omitted by S4, then quantify installed burden and failure topology |
| [Engineering closure](workstreams/ENGINEERING_CLOSURE.md) | Frozen-baseline corrections, reusable engineering evidence, BOLLEY and prototype-readiness inputs | Execute bounded closure tasks without silently redefining the current reference |

## Current authority

VOLLEY is a programme for provider-hosted control of spacecraft departure conditions. Gen5 is the frozen electromagnetic comparison case. The historical gas-driven Gen6 remains an evidence-rich comparator, not the current reference. The clean-sheet reference carried forward for the next calculations is **independent retained cells with a motor-charged mechanical accumulator, independent latch, short guided pusher and local catcher**. This is a reference architecture, not selected flight hardware. P92 and P113 remain open, and no hardware has been built or tested.

Read [BASELINE](BASELINE.md) for Gen5 values, [OPEN_PROBLEMS](../OPEN_PROBLEMS.md) for unresolved evidence, [GEN6_REFERENCE_ARCHITECTURE](GEN6_REFERENCE_ARCHITECTURE.md) for the current reference and its kill conditions, [PROVENANCE](PROVENANCE.md) for evidence class, [DECISION_LOG](DECISION_LOG.md) for accepted decisions, and [PROGRAMME_EXECUTION](PROGRAMME_EXECUTION.md) for the coordinated sequence. Older concept and gas-Gen6 documents preserve earlier assumptions; current comparisons must include springs with timing and host manoeuvres, charge installed host support, and leave provider compatibility unclaimed.

## Completed work that must not be restarted by mistake

The departure screen has 210 cases; the sequential energy-target campaign has 180; the single-payload terminal-state timing screen has 300. [P113-S4](MANIFEST_TIMING.md) is merged: 100 two-payload schedule/order/authority cases using one evolving host, with 44 accepted tested campaigns. The S4 JSON, report, SVG, tests and normal freshness gate are published, and paper/thesis companion snapshots were synchronized to the S4 source commit.

These are four different scopes. S4 is not full-manifest closure: clearing/settling intervals, release/navigation error, installed burden and the complete manifest remain outside the bounded screen. P113/E5 remain open. On the fine grid, BOLLEY, Gen5 and historical gas-Gen6 authority screens share the same best tested 2.777987 kg ideal host-fuel result and 4.569852 m/s first release; that is a tested campaign result, not a universal optimum, product requirement or hardware ranking.

The [P92 clean-sheet screen](GEN6_REFERENCE_ARCHITECTURE.md) converts that bounded mission result into a compact reference-cell problem. It does not close installed mass, repeatability, shock/tip-off, catcher dynamics, cycle life, host resources or provider accommodation. Existing gas-guide trim/contact failures remain in their historical configuration. A numerical pass does not mean hardware acceptance or an architecture win. Use the live VOLLEY and BOLLEY registers for current counts rather than dated handoff numbers.

## Main-first integration

`main` is the programme authority and the normal working branch. Do not create a persistent branch merely to separate routine tasks. Before each write, fetch current `main` and reconcile overlapping edits. A temporary branch is justified only when a change cannot safely be developed on `main`, requires an isolated review, or must preserve an intentionally unfinished experiment. Delete or retire it immediately after integration; never treat a stale branch as a second programme state.

Registers, parameters, baseline generators, ADR indices, changelog, public summaries and companion exports are shared integration surfaces. Keep changes focused and never replace a whole shared file with an older copy. Mission requirements, new configuration decisions and selected interfaces belong to the redesign stream. Closure studies identify their existing configuration and must not silently become a competing redesign.

For each completed task record: starting commit, criteria commit, configuration, changed paths, result and uncertainty, failures retained, verification commands/outcomes, published commit, register disposition, export status and next action. Distinguish work that has merely been written from evidence that has passed its declared checks. Follow [CONTRIBUTING](CONTRIBUTING.md), including criteria-before-code and clean-source companion regeneration.

## Cross-stream and external dependencies

Closure supplies prior art, sensor/material/component evidence, atmosphere/covariance bounds, historical gas-guide contact corrections and BOLLEY results. Redesign supplies mission requirements and selected interfaces. P117/P118 are historical trim-stage work and must not be restarted merely because they once depended on P92; first establish whether the current reference reuses any of that subsystem. Existing-guide analysis can proceed with its own configuration clearly named.

Provider data, customer acceptance, funding/disclosure decisions, manufacture, measurement and independent review cannot be manufactured by documentation. Prepare the calculation, questionnaire or test package needed to obtain them. Do not close an externally dependent item because its request is ready.

## Presentation and architecture update record

2026-09-15: rebuilt the repository front page as a visual technical brochure and replaced the old single-page website with a visual project site, browser mission sandbox, interactive Gen5 CAD viewer, evolution/evidence/current-work pages and a documentation portal.

2026-09-15: integrated P113-S4, synchronized its bounded result into the public visual surfaces and companion snapshots, and advanced the redesign stream from mission screening to architecture requirements.

2026-09-16: completed the clean-sheet P92 reference screen. The current reference is the independent motor-charged stored-energy release cell described above. The historical 8 m gas guide, direct electromechanical and compact-gas concepts, banked/shared-path arrangements, frozen Gen5 and BOLLEY remain comparators or backups. No hardware evidence changed, and P92/P113 remain open.
