# H0 numeric host demand sheet

Configuration:VOLLEY-G5-ACR1, current modeled 1–3 m/s, twelve 4 kg 3U payloads. The lunar campaign is separately named LUNAR-PCS-01; its 280 kg dry core and allocated control authority are not a selected provider.

| Interface | Numeric modeled demand | Evidence/meaning |
|---|---|---|
| Geometry |2.250×1.240×1.3489 m; 3.7634 m³ rectangular box|Eight actual native solid-signature states.7 kg unlocated hardware, harness, service and provider keep-outs additional.|
| Mass |156.556720 kg device dry; 204.556720 kg loaded; 48 kg payload removed|Source ledger includes 7 kg electrical/control allocation; its CG/inertia location is missing.|
| Motion |1.300 m powered travel; 0.210 m arrest; 355 s custody cycle|400 s zero-force loading coast; 450 s mission slot; 20 s post/5 s pre guards.|
| Pulse source |64 cells,32s2p,86.4 V internal initial bank; ≤992.126 J per represented 1–3 m/s shot|Source bank/inverter buffers pulse demand. This is not a request for an 86.4 V host bus.|
| Source recharge |≤2.756 W over 450 s at assumed 80% efficiency|Balance adds 1.1664 W. Actual charger input, efficiency, protection and startup need acceptance.|
| Feed drive |24 V reference; ≤0.719578 A peak; ≤690.79 J over 40 s|Highest accepted feed-resistance case 155 N; peak current held for full duration gives a conservative represented-drive envelope.|
| Lift drive |24 V reference; ≤0.496188 A peak; ≤3382.02 J over 284 s total|10 kg moving-mass study, zero-g, ≤100 N resistance; 22+120+120+22 s motions. Actual cradle/pallet/payload 7.573 kg is below 10 kg study mass.|
| Represented host electrical envelope |≤12.973 W average; ≤21.192 W peak, plus listed services|These are upper bounds for represented loads, not a complete installed bus rating.|
| Represented local heat envelope |≤12.936 W averaged over 450 s, plus listed services|Conservatively counts source losses, motor input, balancing and charger loss. Sink temperature, view factor, contact resistance and actual component duty remain required.|
| Current payload loads |26.8635 N source axial computational load; 100 N transverse guide sensitivity|No launch/environment/mounting-bolt allowable is inferred. Magnetic-gap and guide margins are design budgets requiring physical correlation.|
| Final recoil,3 m/s |≈11.708 N·s payload momentum|Reference initial 704.55672 kg assembly:post-arrest host kick≈0.01671 m/s; transient source recoil≈0.07293 m/s is a different state.|
| Offset attitude demand |0.1 m offset→≈1.171 N·m·s; ≥0.05854 N·m average over 20 s|Inertia and actual release-axis/CG offset must be supplied. This is not slew/pointing acceptance.|
| Pointing / navigation study |0.1°1 sigma pointing,10 m/0.01 m/s navigation sigma; 0.192240 m/s 3 sigma release-speed budget for the standalone 1 km perilune band|These are allocated investigation inputs. Full harmonic navigation/feedback and measured joint accuracy remain required; native open-loop drift exceeds those navigation inputs.|
| Disposal |Independent carrier solution with zero release credit|Existing native 20 N/220 s surrogate impact solutions require≤7.778 kg in the all-failure bounds; actual engine/site/policy external.|

Additional service terms requiring numeric provider/article inputs:controller/encoder/communications standby; lock/keeper/index/home-pin actuators and brakes; drive/harness losses; heaters and thermal control. A complete host request is **12.973 W plus these average terms**, and **21.192 W plus concurrent peak terms**. No omitted term is silently set to zero. This sheet supplies calculated demands and explicitly unresolved interfaces; P7/provider acceptance remains open.

Sources:STUDY_RESULTS.json, inputs/RESOURCE_LEDGER.json, inputs/FEEDER_SIZING.json, inputs/LIFT_SIZING.json, inputs/POWER_COMPONENT_REFERENCE.json, inputs/DESIGN_BUDGETS.json and eight SIGNATURES captures. HARDWARE_FLOWDOWN.json records the arithmetic.
