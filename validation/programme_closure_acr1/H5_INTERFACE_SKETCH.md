# H5 notional load-path and service interfaces

This sketch references the actual ACR1 source coordinates and solid-signature box. It does not define an approved provider ICD ormanufacturing bolt pattern. Coordinates are CAD millimetres; the intended host mounting datum is Z=−150 mm. The represented ladder occupies Z=−190..−150 mm. Final bracket/bolt/grounding/keep-out design needs provider inputs.

```mermaid
flowchart TB
  P["Two six-level banks · twelve3U
actual box 2,250×1,240×1,348.9 mm"]
  L["Selected-cell pusher → indexed lift
captive pallet capture before prior restraint opens"]
  S["Retained 13.127806 kg sled/pallet
1,300 mm powered stroke +210 mm arrest"]
  G["Asymmetric guides / connected C chassis
current structural and tolerance budgets"]
  M["Host-mount ladder
generic datum CAD Z=−150 mm"]
  H["Provider deck / adapter
bolt pattern, loads, stiffness, CG and keep-outs required"]
  P --> L --> S --> G --> M --> H
```

Payload axial reaction and LSM source reactions close through the carrier/guide/chassis supports and the host-mount ladder. Payload departure creates a net host impulse; internal sled motion creates a larger transient reaction and then returns momentum during arrest. The retained captive pallet stays onthe carrier. A payload-proxy envelope is not a load-bearing provider bracket. Launch restraint paths and external access remain tobe defined with the host.

```mermaid
flowchart LR
  B["Host DC service
24 V reference request, quality/limits unknown"] --> C["Isolated charger / source protection
efficiency and inrush acceptance required"]
  C --> E["64 cell32s2p bank
86.4 V internal initial charge"]
  E --> I["Three-phase inverter /40 kHzPWM"] --> F["LSM launch / arrest /return"]
  B --> D["Feed /lift /locks /brakes
sequencer and encoders"]
  A["Host mission authority / independent inhibits"] --> Q["Custody /home-pin /source /release interlocks"]
  Q --> D
  Q --> I
  R["Bonding /return /EMC /thermal deck interface
provider numeric limits required"] --- C
  R --- D
  R --- I
```

The home-index interface is a retracting 6 mm pin in a 6.2 mm carrier bore; the current model identifies this as external host-provided hardware, unselected. Clear retraction is required before carrier travel. Power/thermal integration must add the unlocated 7 kg source/control package and numeric services listed in H0. No unused CAD volume is automatically credited as radiator, harness clearance orspace-qualified electronics packaging.

The mission interface is an individually authorized separation vector plus finite recoil/recovery budget. Keep the generic 500 kg LEO host and the separate 300 kg-wet lunar reference distinct. A supplied provider state, ICD, attitude/thrust authority, plume/visibility constraints and independent disposal approval are required before adopting either reference.

Sources:inputs/PARAMETERS.json; inputs/RESOURCE_LEDGER.json; inputs/SIGNATURES_home.json; inputs/SIGNATURES_release.json; STUDY_RESULTS.json; HARDWARE_FLOWDOWN.json. The diagrams are notional interface sketches, not CAD orsolver screenshots.
