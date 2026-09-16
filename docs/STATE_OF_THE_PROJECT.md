# Where the project stands

Updated 2026-09-16. This page is a current-state pointer, not a substitute for the evidence register or the generation histories.

## Programme

VOLLEY investigates provider-hosted control of spacecraft departure conditions. The present programme question is not how to maximize ejection speed; it is what controllable departure authority is useful for a stated mission and what is the smallest credible machine that supplies it.

P113-S1 through S4 now provide bounded mission screens. S4 couples two payload deliveries through one evolving host state and found that, in its best tested fine-grid campaign, the BOLLEY, Gen5 and historical gas-Gen6 authority screens all used the same 4.569852 m/s first release. That is not a product requirement or global optimum. It is evidence that additional release authority did not improve that tested campaign. Clearing/settling, release/navigation uncertainty, host attitude recovery, installed burden, replenishment and complete-manifest effects remain open.

## Gen5

The [frozen baseline](BASELINE.md) is a modelled electromagnetic deployer, with no hardware validation. [GEN5_CLOSURE.md](GEN5_CLOSURE.md) records the Phase I freeze and its failed kill criteria. It does not mean all computer work is complete.

P37's retention-pin computation was answered by A22; P46's thrust correction was applied by ADR-030; A52 answered E29's missing angular-momentum budget; P95's mass correction is present in A35 and the public summaries. Qualification, host data and the failed mass criterion remain separate. Remaining Gen5 work stays configuration-specific and is completed only where a live claim or reused component needs it.

## Gen6

The current calculation reference is the [clean-sheet Gen6 reference architecture](GEN6_REFERENCE_ARCHITECTURE.md): **independent retained cells with a motor-charged mechanical accumulator, independent latch, short guided pusher and local catcher**. Spring form, latch, bearings, catcher, motor/gearbox and cell structure are deliberately unselected. P92 remains open until mission uncertainty, installed burden, release repeatability, shock/tip-off, catcher dynamics, cycle life and host accommodation can falsify or support the reference.

The approximately 8 m direct cold-gas guide is now the **historical gas-Gen6 comparator**, not the current programme authority. Its pressure-system, guide/contact, suspended-trim and campaign evidence remains valuable under that configuration. A72-A74 still show that its magnetic secondary and conducting tube cannot be treated as a solved combination. P103/P108 remain historical-guide contact/exit-state questions unless a later decision explicitly reuses that geometry.

Direct short-stroke electromechanical and compact-gas pushers remain backups. Banked and shared-magazine payload arrangements remain comparators to independent cells. BOLLEY remains a separate cooperative-payload path.

## Prototype status

No VOLLEY hardware has been built, fired, measured, qualified or flown. The [prototype-readiness programme](PROTOTYPE_READINESS.md) defines the route from the current evidence to one named buildable test article. The immediate physical-facing task is to define small discriminating release-cell coupons with acceptance bands frozen before hardware: force-displacement, preload/release sensitivity, latch repeatability/shock, pusher friction, exit velocity/tip-off and catcher load.

## How I present it

Use the Gen5 [baseline](BASELINE.md) for frozen Gen5 numbers, [PROVENANCE.md](PROVENANCE.md) for what supports claims, [GEN6_REFERENCE_ARCHITECTURE.md](GEN6_REFERENCE_ARCHITECTURE.md) for the current Gen6 reference, [PROGRAMME_EXECUTION.md](PROGRAMME_EXECUTION.md) for sequence, and the [register](../OPEN_PROBLEMS.md) for unresolved evidence. Historical generation documents preserve their own configurations rather than being rewritten as though they described the current reference.

The paper and thesis describe the Gen5 baseline; their exported analysis payload can include later programme work without making Gen6 part of the manuscript's verified scope. No universal CubeSat qualification acceleration is established here. Study acceleration ceilings are internal screens; payload-specific structural, shock and magnetic compatibility require evidence.