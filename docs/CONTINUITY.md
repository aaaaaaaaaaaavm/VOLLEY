# Project continuity and work ownership

Updated 2026-09-15. This is the starting point when resuming work. Fetch current `main`, inspect the working tree and read the most recent task evidence before editing. The programme has two coordinated workstreams.

| Workstream | Owns | First deliverable |
|---|---|---|
| [Mission and redesign](workstreams/MISSION_AND_REDESIGN.md) | Front-page presentation, complete mission comparison, Gen6 selection and selected release-cell integration | Turn S1–S4 into architecture requirements, then run the P92 arrangement/mechanism trade |
| [Engineering closure](workstreams/ENGINEERING_CLOSURE.md) | Frozen-baseline corrections, reusable engineering evidence, BOLLEY and prototype-readiness inputs | Reconcile later results against open entries, then execute bounded closure tasks |

## Current authority

VOLLEY is a programme for provider-hosted control of spacecraft departure conditions. Gen5 is the frozen electromagnetic comparison case. The existing gas-driven Gen6 is an investigated candidate; the mechanism selection is reopened. Compact controllable release with independently retained payloads is a leading candidate, not an adopted design. No hardware has been built or tested.

Read [BASELINE](BASELINE.md) for Gen5 values, [OPEN_PROBLEMS](../OPEN_PROBLEMS.md) for unresolved evidence, [PROVENANCE](PROVENANCE.md) for evidence class, [DECISION_LOG](DECISION_LOG.md) for accepted decisions, and [PROGRAMME_EXECUTION](PROGRAMME_EXECUTION.md) for the coordinated sequence. Older concept documents preserve earlier assumptions; current comparisons must include springs with timing and host manoeuvres, charge installed host support, and leave provider compatibility unclaimed.

## Completed work that must not be restarted by mistake

PR #33 and the paper/thesis companion PRs #2 are merged. The departure screen has 210 cases; the sequential energy-target campaign has 180; the single-payload terminal-state timing screen has 300. [P113-S4](MANIFEST_TIMING.md) is also merged: 100 two-payload schedule/order/authority cases using one evolving host, with 44 accepted tested campaigns. The S4 JSON, report, SVG, tests and normal freshness gate are published, and paper/thesis companion snapshots were synchronized to the S4 source commit.

These are four different scopes. S4 is not full-manifest closure: clearing/settling intervals, release/navigation error, installed burden and the complete manifest remain outside the bounded screen. P113/E5 remain open. On the fine grid, BOLLEY, Gen5 and existing Gen6 authority screens share the same best tested 2.777987 kg ideal host-fuel result and 4.569852 m/s first release; that is a tested campaign result, not a universal optimum or hardware ranking.

Existing trim/contact failures remain. A numerical pass does not mean hardware acceptance or an architecture win. Use the live VOLLEY and BOLLEY registers for current counts rather than dated handoff numbers.

## Shared files and integration

Use a separate branch/worktree per task. Reserve overlapping paths in the task's work note before editing them. Mission requirements, new configuration decisions and selected interfaces belong to the redesign stream. Closure studies identify their existing configuration and must not silently become a competing redesign.

Registers, parameters, baseline generators, ADR indices, changelog, public summaries and companion exports are shared integration surfaces. Submit focused changes, fetch current main before integrating, and reconcile against the new evidence. If another task owns overlapping paths, complete the independent calculation/report and defer those integration edits until its commit lands. Never replace a whole shared file with an older copy.

For each completed task record: starting commit, criteria commit, configuration, changed paths, result and uncertainty, failures retained, verification commands/outcomes, published commit, register disposition, export status and next action. Distinguish local/uncommitted work from published evidence. Follow [CONTRIBUTING](CONTRIBUTING.md), including criteria-before-code and clean-source companion regeneration.

## Cross-stream and external dependencies

Closure supplies prior art, sensor/material/component evidence, atmosphere/covariance bounds, existing contact-model corrections and BOLLEY results. Redesign supplies mission requirements and selected interfaces. P117/P118 depend on P92; detailed replacement trim work must wait for the selection it implements. Existing-guide analysis can proceed with its own configuration clearly named.

Provider data, customer acceptance, funding/disclosure decisions, manufacture, measurement and independent review cannot be manufactured by documentation. Prepare the calculation, questionnaire or test package needed to obtain them. Do not close an externally dependent item because its request is ready.

## Presentation update record

2026-09-15: rebuilt the repository front page as a visual technical brochure and replaced the old single-page website with a visual project site, browser mission sandbox, interactive Gen5 CAD viewer, evolution/evidence/current-work pages and a documentation portal. Earlier concept narratives remain historical and no clean-sheet Gen6 mechanism is rendered before selection.

2026-09-15: integrated P113-S4, synchronized its bounded result into the public visual surfaces and companion snapshots, and advanced the redesign stream to architecture requirements and P92 selection. No hardware evidence changed.