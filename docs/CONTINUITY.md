# Project continuity and work ownership

Updated 2026-09-15. This is the starting point when resuming work. Fetch current `main`, inspect the working tree and read the most recent task evidence before editing. The programme has two coordinated workstreams.

| Workstream | Owns | First deliverable |
|---|---|---|
| [Mission and redesign](workstreams/MISSION_AND_REDESIGN.md) | Front-page presentation, complete mission comparison, Gen6 selection and selected release-cell integration | Complete multi-payload terminal-state requirements and release timing |
| [Engineering closure](workstreams/ENGINEERING_CLOSURE.md) | Frozen-baseline corrections, reusable engineering evidence, BOLLEY and prototype-readiness inputs | Reconcile later results against open entries, then execute bounded closure tasks |

## Current authority

VOLLEY is a programme for provider-hosted control of spacecraft departure conditions. Gen5 is the frozen electromagnetic comparison case. The existing gas-driven Gen6 is an investigated candidate; the mechanism selection is reopened. Compact controllable release with independently retained payloads is a leading candidate, not an adopted design. No hardware has been built or tested.

Read [BASELINE](BASELINE.md) for Gen5 values, [OPEN_PROBLEMS](../OPEN_PROBLEMS.md) for unresolved evidence, [PROVENANCE](PROVENANCE.md) for evidence class, [DECISION_LOG](DECISION_LOG.md) for accepted decisions, and [PROGRAMME_EXECUTION](PROGRAMME_EXECUTION.md) for the coordinated sequence. Older concept documents preserve earlier assumptions; current comparisons must include springs with timing and host manoeuvres, charge installed host support, and leave provider compatibility unclaimed.

## Completed work that must not be restarted by mistake

PR #33 and the paper/thesis companion PRs #2 are merged. The departure screen has 210 cases; the sequential energy-target campaign has 180; the single-payload terminal-state timing screen has 300. These are three different scopes. Neither energy targets alone nor a single-payload timing search establish a complete manifest or useful constellation. [TERMINAL_TIMING](TERMINAL_TIMING.md) records the latest study limits.

The 52 live VOLLEY entries and BOLLEY's 48-entry register have not been closed by writing this handoff. Existing trim/contact failures remain. A numerical pass does not mean hardware acceptance or an architecture win.

## Shared files and integration

Use a separate branch/worktree per task. Reserve overlapping paths in the task's work note before editing them. Mission requirements, new configuration decisions and selected interfaces belong to the redesign stream. Closure studies identify their existing configuration and must not silently become a competing redesign.

Registers, parameters, baseline generators, ADR indices, changelog, public summaries and companion exports are shared integration surfaces. Submit focused changes, fetch current main before integrating, and reconcile against the new evidence. If another task owns overlapping paths, complete the independent calculation/report and defer those integration edits until its commit lands. Never replace a whole shared file with an older copy.

For each completed task record: starting commit, criteria commit, configuration, changed paths, result and uncertainty, failures retained, verification commands/outcomes, published commit, register disposition, export status and next action. Distinguish local/uncommitted work from published evidence. Follow [CONTRIBUTING](CONTRIBUTING.md), including criteria-before-code and clean-source companion regeneration.

## Cross-stream and external dependencies

Closure supplies prior art, sensor/material/component evidence, atmosphere/covariance bounds, existing contact-model corrections and BOLLEY results. Redesign supplies mission requirements and selected interfaces. P117/P118 depend on P92; detailed replacement trim work must wait for the selection it implements. Existing-guide analysis can proceed with its own configuration clearly named.

Provider data, customer acceptance, funding/disclosure decisions, manufacture, measurement and independent review cannot be manufactured by documentation. Prepare the calculation, questionnaire or test package needed to obtain them. Do not close an externally dependent item because its request is ready.

## Presentation update record

2026-09-15: replaced the front-page configuration summary with a mission-led brochure, retained frozen results and failure boundaries, and marked earlier concept narratives as historical. Added workstream ownership and a complete routing of live VOLLEY items. No analysis, register status, baseline, CAD or companion evidence changed.
