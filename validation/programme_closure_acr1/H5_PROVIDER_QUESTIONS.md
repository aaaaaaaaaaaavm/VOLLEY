# H5 provider integration questions

Prepared question sheets for an integration review; no provider was contacted and no answer or approval is implied. Each requested answer should name an ICD revision, value/limit, coordinate frame and evidence maturity. Use H0_DEMAND_SHEET.md and H5_INTERFACE_SKETCH.md as the controlled numeric request.

## Mechanical and payload integration

1. Can the candidate host accommodate the actual 2.250×1.240×1.3489 m geometry box and 204.556720 kg loaded mass, with separate service/harness/launch keep-outs and the unlocated 7 kg allocation?
2. What are the mounting plane, bolt pattern, load distribution, permitted CG/inertia, stiffness/mode, launch/quasi-static, vibration and shock limits? The current generic mounting datum is CAD Z=−150 mm; it is not an approved bolt interface.
3. What external retention, release authorization and launch restraint requirements apply? Can the host provide or accept the current 6 mm retracting home-index pin/6.2 mm bore interface, and verify clear travel before the 355 s cycle?
4. Supply the real payload rail/mass/inertia/CG, retention, venting, tip-off, shock, release-clearance and separation-state acceptance inputs. Are twelve 4 kg 3U surrogates valid for this specific mission?
5. What access is required for captive-pallet capture-before-release inspection, bank/lift servicing, discharge and safe failed-cell removal? Which unresolved shared-path faults mandate abort?

## Electrical, thermal and EMC integration

1. Supply bus voltage/quality, current and energy limits, startup, inrush, brownout, source isolation and charging inhibit requirements.24 V is the present motor-interface reference, not a known host service.
2. Confirm the represented average/peak power request in H0 plus numeric controller/lock/brake/home-pin/harness/heater allocations. Can pulse charging occur during feed/lift operation? What load-shed and fault-containment states are required?
3. Supply hot/cold mounting-interface temperatures, conductive paths/contact resistance, radiator/view-factor constraints, allowable thermal cycling and vacuum/outgassing/contamination requirements. Catalog operating temperatures do not establish vacuum acceptance.
4. Supply conducted/radiated/40 kHzPWM transient limits, ground/return/bonding/isolation policy, magnetic-cleanliness zones and payload susceptibility. Specify the required qualification/correlation evidence and instrumentation.
5. Which host commands, telemetry, timing, arming/disarming, cell/source monitoring and independent inhibit channels must the sequencer implement? How is safe local capacitor discharge confirmed after abort?

## Mission, attitude and operations integration

1. Supply actual delivered orbit/state/epoch, launch-dispersions, target departure states/times and success bands. Separate LEO delivery from launch-suppliedTLI/direct-lunar delivery; include carrier-only TLI/LOI, stationkeeping and disposal reserves.
2. Supply full host/payload mass/CG/inertia, release-axis lever arm, actuator torque/rate/momentum/thrust authority, cold-gas/chemical Isp and propellant limits. Are arbitrary body-axis directions available without plume orsolar/communications restrictions?
3. Can the host meet 355 s custody inside 400 s zero-force loading at 450 s slots, including 20 s post/5 s pre guards and finite recoil/slew recovery? The surviving lunar sensitivity case needs 5 Nm and up to 18.57 deg/s; the 5 deg/s case misses a sign-reversal slot. No existing host is asserted to meet this.
4. What navigation covariance, clock jitter, relative-speed/pointing accuracy, conjunction screening and non-recontact criterion are required? Which inputs are measured, simulated, allocated orunknown?
5. Who authorizes each release and abort? What disposal method remains valid with all 12 payloads captive, and what exact engine, reserve, site/trajectory, policy and approval evidence is required? A reference-sphere impact is a dynamics result, not a disposal authorization.

Return answers with the originalPLAN-H1/H2/H3/H6/P7 references. These prepared questions complete a question-set deliverable only; host selection and external acceptance require genuine responses.
