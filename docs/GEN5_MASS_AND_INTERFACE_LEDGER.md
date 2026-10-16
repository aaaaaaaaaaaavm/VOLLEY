# Evaluated Gen5 mass and interface ledger

**Historical model reconciliation, not a weighed or installation-ready assembly.** The 23 model lines total 126.561588 kg dry, 174.561588 kg loaded, and 10.546799 kg per carried 3U. The x-only model CG is 0.457690 m from its assumed breech datum. The rounded publications remain 126.6 kg, 174.6 kg, 10.55 kg/3U and 0.46 m. No physical tensor is inferred from missing three-dimensional placements.

| # | Model line | kg | CG x m | CAD representation | Evidence basis |
|--:|:--|--:|--:|:--|:--|
| 1 | Track longerons (2x Al box section) | 6.829920 | 0.750 | Track | parametric hollow-section estimate; 1.55 m mass length versus 1.8 m CAD |
| 2 | Stator copper (1.3 m, 60% fill) | 6.289920 | 0.650 | Stator | fill-factor material estimate; not solid proxy density |
| 3 | Stator formers / potting (PEEK eq.) | 0.972972 | 0.650 | Stator | fill-factor material estimate; not solid proxy density |
| 4 | Sled Halbach magnets (2 faces) | 3.672000 | 0.150 | Sled | parametric plus historical Gen3 solid-volume reconciliation |
| 5 | Sled Ti chassis (shell equivalent) | 0.736798 | 0.150 | Sled | parametric plus historical Gen3 solid-volume reconciliation |
| 6 | Sled rollers / latch / backstop | 0.450000 | 0.150 | Sled | parametric plus historical Gen3 solid-volume reconciliation |
| 7 | Eddy brake magnets + yoke | 1.684800 | 1.420 | Brake | primitive/lump estimate; no selected brake |
| 8 | Fixed brake hardware + ring spring (moving Cu fin is in sled) | 0.856000 | 1.400 | Brake | primitive/lump estimate; no selected brake |
| 9 | Cassette shells (2x Al sheet eq.) | 8.852976 | 0.350 | Magazine_P / Magazine_S | shell/fill or lump estimate; feeder not modeled |
| 10 | Followers, gates, escapements (2x) | 2.600000 | 0.300 | Magazine_P / Magazine_S | shell/fill or lump estimate; feeder not modeled |
| 11 | Supercapacitor cells + busbars | 6.500000 | 0.100 | not individually represented | assumed lump; no selected component |
| 12 | PPU (SiC bridge, filters) | 4.000000 | 0.100 | not individually represented | assumed lump; no selected component |
| 13 | Battery + avionics + IMU | 5.500000 | 0.120 | not individually represented | assumed lump; no selected component |
| 14 | Harness | 2.500000 | 0.600 | not individually represented | assumed lump; no selected component |
| 15 | Thermal (pipes, radiator, MLI) | 6.000000 | 0.700 | not individually represented | assumed lump; no selected component |
| 16 | ESPA bracket + fasteners | 9.000000 | 0.350 | Interface_ESPA | assumed lump; provider mount not selected |
| 17 | Panels / closeouts | 5.500000 | 0.750 | Enclosure or omitted detail | skin/fill/lump estimate; allocation overlap must be resolved in any redesign |
| 18 | Enclosure skins (2 mm Al, 6.077 m2 net, A46) | 32.820000 | 0.500 | Enclosure or omitted detail | skin/fill/lump estimate; allocation overlap must be resolved in any redesign |
| 19 | Enclosure frames and ribs (A46, 25 % of skin, declared) | 8.200000 | 0.500 | Enclosure or omitted detail | skin/fill/lump estimate; allocation overlap must be resolved in any redesign |
| 20 | Radiator (1600 x 200 x 3 mm Al, A46) | 2.590000 | 0.450 | Enclosure or omitted detail | skin/fill/lump estimate; allocation overlap must be resolved in any redesign |
| 21 | Equipment-bay boxes (4 bays, 1.5 mm Al, A46) | 1.870000 | 0.300 | Enclosure or omitted detail | skin/fill/lump estimate; allocation overlap must be resolved in any redesign |
| 22 | Fasteners and brackets (A46, 10 % of structure, declared) | 4.550000 | 0.500 | Enclosure or omitted detail | skin/fill/lump estimate; allocation overlap must be resolved in any redesign |
| 23 | Sled CAD reconciliation (P15, CAD-derived 9.445 kg) | 4.586202 | 0.150 | Sled | parametric plus historical Gen3 solid-volume reconciliation |

## Bounds and omissions

- No installed BOM or vendor-checked component masses
- x-only lump centers are not measured assembly CG; lateral/vertical CG and full inertia unavailable
- Historical Gen3 sled volume is not a complete Gen5 material extraction
- CAD solid material proxies cannot replace shell/fill mass estimates
- Thermal/radiator, panel/enclosure and bracket allocations may overlap; no quantified credit taken
- Harness routing, actual feeder/locks, actuator, winding ends and provider adapter lack installed detail
- A new geometry or component selection requires a new mass/CG/inertia revision

The quoted ±15% model spread is an illustrative assumption, not a confidence interval. Even its low end is 107.577 kg, or 8.965 kg/3U; it still exceeds the 72 kg twelve-canister class assumption. This does not establish a fair current-product comparison: the 6 kg/3U benchmark is a historical class input, not a vendor-installed quote.

## Interface boundary

Gen5 uses twelve 4 kg, 340.5 × 100 × 100 mm geometric proxies, not a selected spacecraft ICD. Its adapter is an intersecting ring/hub representation, not an approved ESPA interface. The separately versioned Gen6 study uses two 1U and two 3U at 1.33/4 kg nominal. CDS Rev. 14.1 gives class study ceilings of 2/6 kg; NRCSD Rev. - has different mission-specific limits. The [public reference audit](GEN6_GO1_PUBLIC_REFERENCE_AUDIT.md) identifies SwissCube and MinXSS as form-factor precedents. Neither is the selected payload.

The generic maneuvering OTV deck, 500 km SSO and parametric adapter do not supply a real bolt pattern, allowable load, thermal, vacuum, EMC, shock or magnetic limit. The 5/10/25 g acceleration cases are provisional sensitivity inputs. Actual provider/payload documents govern compatibility.

[Machine-readable ledger](../analysis/results/gen5_mass_ledger.json) · [Geometric failure disposition](../cad/GEN5_INTERFERENCE_DISPOSITION.md).
