# Where the project stands

Updated 2026-09-06. The previous version mixed pre-ADR-030 defects with corrected numbers, including a thrust correction from a number to itself. I have replaced that stale snapshot with the current evidence routes; its earlier text remains in git history.

## Gen5

The [frozen baseline](BASELINE.md) is a modelled electromagnetic deployer, with no hardware validation. [GEN5_CLOSURE.md](GEN5_CLOSURE.md) records the Phase I freeze and its failed kill criteria. It does not mean all computer work is complete.

P37's retention-pin computation was answered by A22; P46's thrust correction was applied by ADR-030; A52 answered E29's missing angular-momentum budget; P95's mass correction is present in A35 and the public summaries. Their register dispositions now reflect that evidence. Qualification, host data and the failed mass criterion remain separate.

The remaining Gen5 calculations and decisions are listed individually in [BSX_REVIEW.md](BSX_REVIEW.md). No item is retired simply because Gen6 changes the architecture.

## Gen6

The current target is direct cold-gas payload acceleration along an approximately 8 m stage-integrated guide. The trim stage is suspended. A72-A74 show that the magnetic secondary and conducting tube cannot be treated as a solved combination. P92 requires an architecture decision; P103/P108 retain the guide-contact and exit-state work.

[COMPUTATIONAL_CLOSURE.md](COMPUTATIONAL_CLOSURE.md) records the active Gen6 calculation backlog. [BSX_REVIEW.md](BSX_REVIEW.md) supplies the generated live-item list, handoff sequence and provider questions. The older [GEN6_CLOSURE.md](GEN6_CLOSURE.md) is a historical planning document and must be read with those later results.

## How I present it

Use the Gen5 [baseline](BASELINE.md) for numbers, [PROVENANCE.md](PROVENANCE.md) for what supports them, and the [register](../OPEN_PROBLEMS.md) for limitations. The paper and thesis describe the Gen5 baseline; their exported analysis payload can include later programme work without making Gen6 part of the manuscript's verified scope.

No universal CubeSat qualification acceleration is established here. The chosen acceleration ceiling is an internal design constraint; payload-specific structural and magnetic compatibility require evidence.
