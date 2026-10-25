# C7 hardware requirement flowdown from the lunar campaign

This flowdown completes the translation of the declared surviving lunar investigation into hardware/service requirements. It does not select orqualify a lunar carrier or change the near-term ACR1 LEO article. Each row names the source result, downstream original task IDs and the remaining physical/provider evidence needed for acceptance.

## C7-V · Post-arrest separation command and vector

Accepted modeled command 1–3 m/s; actual finite-host relative speeds in this 12-shot campaign 0.960300–2.873143 m/s.6 prograde/6 retrograde. Direction is body+X; all retargeting consumes finite slew time.

Downstream:N2, N3. Source:campaign/T5_R20_searched.json.

Acceptance:Imposed source-calibrated point-event mapping; source-rated physical pulse/contact and actual payload release accuracy remain external.

## C7-Q · Increment and 3 sigma state accuracy

Declared 1 km osculating-perilune error band: speed 3 sigma<= 0.192240 m/s at the standalone+3 m/s reference with 10 m/0.01 m/s navigation sigma and 0.1 deg pointing sigma. Quantization-only necessary increment<= 0.221980 m/s; allocate finer when other speed errors consume budget.

Downstream:N2, N5. Source:NAVIGATION_REQUIREMENTS.json.

Acceptance:Study requirements only. Independent speed/angle saturation is not a joint guarantee. Measured sensor/control covariance and perturbed campaign Monte Carlo not supplied. The harmonic native host endpoint differs from the open-loop point-gravity planner by about 1.63 km/1.49 m/s, exceeding the assumed 10 m/0.01 m/s navigation bands; full-force navigation/planning/feedback is required before combining the standalone covariance with a campaign precision claim.

## C7-A · Finite host control authority and recovery

Surviving tested reference uses 20 N main thrust, Isp 220 s,5 Nm attitude couple, >= 18.567 deg/s rate and declared inertia tensor. Cold-gas couple uses 60 s Isp and 0.5 m lever.20 s guard,400 s loading coast,5 s preguard and 450 s slots are included.

Downstream:N3, N5. Source:CAMPAIGN_RESULTS.json.

Acceptance:An operational demand, not a supplier capability.5 deg/s and double-inertia cases retain missed-slot failures; a real host must demonstrate allocated authority/plume/pointing and resources.

## C7-M · Mass properties and load path

Actual source ACR1 dry 156.556720 kg including unlocated 7 kg allowance; loaded 204.556720 kg. Eight-state geometry box 2.250 x 1.240 x 1.3489 m. Campaign uses 280 kg complete dry retained core with declared inertia, actual CAD payload coordinates and per-shot updated CG/inertia. Payload axial computational load 26.8635 N and 100 N guide sensitivity remain source budgets.

Downstream:N2, N3, N5. Source:STUDY_RESULTS.json; inputs/DESIGN_BUDGETS.json.

Acceptance:Manufactured mass/CG/inertia, external mounting bolts, launch/environment loads and provider interface approval remain external.

## C7-R · Retention duration and custody

At least 5400 s from staging campaign start through final nominal release; failed payloads remain captive through abort and independently available disposal. Launch/transfer waiting must be added: ideal Earth–Moon flight is about 5 days, not a validated retention rating.355 s source cycle inside 400 s coast; captivity/capture precedes prior restraint release.

Downstream:N2, N5. Source:campaign_inputs.json; inputs/MISSION_INPUTS.json.

Acceptance:Current native custody geometry is retained. Physical latch endurance, launch/thermal retention and failed-path clearance tests remain external; no impossible automatic fault reset is claimed.

## C7-E · Pulse and bus services

64 cells32s2p,86.4 V internal initial bank.1–3 m/s maximum captured pulse 992.126 J; known represented service upper envelope 12.973 W average/21.192 W peak plus named unallocated services.24 V is the motor/charger-interface design request.

Downstream:N3, N5. Source:H0_DEMAND_SHEET.md.

Acceptance:Host bus quality/isolation, fault current/charger efficiency, standby/brake/lock services and actual circuit/pulse/vacuum acceptance remain external.

## C7-T · Thermal, vacuum and material properties

Represented thermal upper envelope 12.936 W over 450 s plus unallocated heater/control/actuator terms. Pulse loss and copper/tolerance budgets are source linked. Eaton cell catalog operating range−40..65 degC is a reference limit, not space qualification.

Downstream:N2, N3, N5. Source:inputs/DESIGN_BUDGETS.json; inputs/POWER_COMPONENT_REFERENCE.json.

Acceptance:Required sink/interface temperatures, radiator view factors, thermal contact/conduction, cycling, outgassing, vacuum friction and contamination acceptance must be measured/agreed. No approved lunar radiator is inferred.

## C7-EMC · EMC, grounding and magnetic interface

40 kHz source PWM; 86.4 V internal bank; source-rated current/voltage/ripple design budgets retained. Separate structure/return/bonding and exclusion-zone interfaces must be allocated around the LSM and pulse wiring.

Downstream:N3, N5. Source:inputs/POWER_COMPONENT_REFERENCE.json.

Acceptance:Provider conducted/radiated/transient limits, magnetic cleanliness, shielding/harness/bonding tests and payload susceptibility are missing acceptance inputs, not fabricated compliance.

## C7-F · Release count, cadence and abort/disposal

12 command attempts at 450 s spacing; successful reference releases 12. Modeled pre-command isolated-cell fault yields 11 releases/1 retained; unresolved shared-path fault at slot 6 stops after 5 releases with 7 retained. Engine-only disposal remains independent of successful releases; surviving campaign leaves 18.233629 kg versus 8 kg reserved floor. Additional actual terminal-state disposal replays for nominal/isolated-cell/shared-path-abort cases all hit the sphere with<= 6.510957 kg additional propellant, below 8 kg, after coasting to apolune and finite attitude preparation.

Downstream:N2, N3, N5. Source:CAMPAIGN_RESULTS.json; DISPOSAL_NATIVE_RESULTS.json.

Acceptance:Sensor/interlock/abort actuation must implement those controlled states. A real impact site, engine/propellant capability and disposal authorization remain external.

The referenced N2/N3/N5 tasks retain their physical and source-rated build gates. A computational requirement table does not close material measurements, contact correlation, manufacturing release, host/customer inputs orindependent human review. Near-term ACR1 remains twelve3U,1–3 m/s modeled command range and 64 source cells.
