# Where the project stands

> **Architecture disposition, 2026-09-28:** The separate motor-charged spring-cell bank is withdrawn as VOLLEY's next architecture. It is retained here only as a dated study. Any selection or current-reference wording below describes the former decision and is superseded. A reusable shared launch path with sequential loading is the open design objective; no speed envelope is validated. See [current status](NEXT_GENERATION_STATUS.md).


Updated 2026-09-16. This page is a current-state pointer, not a substitute for the evidence register or the generation histories.

## Programme

VOLLEY investigates provider-hosted control of spacecraft departure conditions. The present programme question is not how to maximize ejection speed; it is what controllable departure authority is useful for a stated mission and what is the smallest credible machine that supplies it.

P113-S1 through S4 now provide bounded mission screens. S4 couples two payload deliveries through one evolving host state and found that, in its best tested fine-grid campaign, the BOLLEY, Gen5 and historical gas-guide study authority screens all used the same 4.569852 m/s first release. That is not a product requirement or global optimum. It is evidence that additional release authority did not improve that tested campaign. Clearing/settling, release/navigation uncertainty, host attitude recovery, installed burden, replenishment and complete-manifest effects remain open.

[S5](OPERATIONAL_UNCERTAINTY.md) adds local sensitivities. [S6](COMBINED_RELEASE_ERRORS.md)
now combines six errors in 512 conditional event corners. Its illustrative base box passes both
events, while doubling the widths fails 20 of 64 first-event corners. Each event still begins at
its nominal host state. [P92-S2](REFERENCE_CELL_MECHANICS.md) adds the 144-case mechanical screen,
with 48 feasible analytical cases and no selected hardware. The [review and restart record](REVIEW_20260916.md)
lists completed work, exact remaining tasks and reproduction commands.

## Gen5

The [frozen baseline](BASELINE.md) is a modelled electromagnetic deployer, with no hardware validation. [GEN5_CLOSURE.md](GEN5_CLOSURE.md) records the Phase I freeze and its failed kill criteria. It does not mean all computer work is complete.

P37's retention-pin computation was answered by A22; P46's thrust correction was applied by ADR-030; A52 answered E29's missing angular-momentum budget; P95's mass correction is present in A35 and the public summaries. Qualification, host data and the failed mass criterion remain separate. Remaining Gen5 work stays configuration-specific and is completed only where a live claim or reused component needs it.

## historical study

The [independent spring-cell study](LEGACY_STUDY_REFERENCE_ARCHITECTURE.md) is withdrawn as the current reference. Its spring, latch, guide and catcher model remains a low-speed comparator; it does not establish a shared reload path or broad commanded speed. The next architecture must be selected against complete-manifest mission value, installed burden, payload loads, reliability and host accommodation. P92 remains open.

The approximately 8 m direct cold-gas guide is now the **historical gas-guide study comparator**, not the current programme authority. Its pressure-system, guide/contact, suspended-trim and campaign evidence remains valuable under that configuration. A72-A74 still show that its magnetic secondary and conducting tube cannot be treated as a solved combination. P103/P108 remain historical-guide contact/exit-state questions unless a later decision explicitly reuses that geometry.

Electromagnetic, electromechanical, gas, banked and shared-path layouts remain trade cases. A competent conventional dispenser is the baseline. BOLLEY remains a separate cooperative-payload path.

## Prototype status

No VOLLEY hardware has been built, fired, measured, qualified or flown. The [prototype-readiness programme](PROTOTYPE_READINESS.md) defines the route from the current evidence to one named buildable test article. The immediate physical-facing task is to define small discriminating release-cell coupons with acceptance bands frozen before hardware: force-displacement, preload/release sensitivity, latch repeatability/shock, pusher friction, exit velocity/tip-off and catcher load.

## How I present it

Use [current status](NEXT_GENERATION_STATUS.md) for the open architecture, the Gen5 [baseline](BASELINE.md) for its frozen model numbers, [PROVENANCE.md](PROVENANCE.md) for evidence classes, the [withdrawn spring-cell study](LEGACY_STUDY_REFERENCE_ARCHITECTURE.md) for its historical result, [PROGRAMME_EXECUTION.md](PROGRAMME_EXECUTION.md) for the next comparison, and the [register](../OPEN_PROBLEMS.md) for unresolved evidence. Historical generation documents preserve their own configurations.

The paper and thesis describe the Gen5 baseline; their exported analysis payload can include later programme work without making historical study part of the manuscript's verified scope. No universal CubeSat qualification acceleration is established here. Study acceleration ceilings are internal screens; payload-specific structural, shock and magnetic compatibility require evidence.
