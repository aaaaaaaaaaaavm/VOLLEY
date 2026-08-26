# Gen6 Fusion build package

Written 2026-08-22, for the person building the authoritative Fusion assembly.
Everything here traces to `cad/parameters.json`, `cad/build_gen6.py` or a numbered run.
Nothing in this file is a new engineering dimension. Where a dimension does not exist, it says
so and names what owns it.

> What `cad/build_gen6.py` is. A geometry and interface model: the simplest solid carrying
> the right interface at the right station. No fillets, no fasteners, no harness, no tolerancing,
> no seal or valve detail. It is a check that the parts do not collide and that the volumes are
> real, it is *not* a design, and §9 lists every place that distinction matters.
>
> Units: millimetres. Angles: degrees. Fusion document units mm.

---

## 1. Assembly tree

`H` host-provided reference, `V` VOLLEY hardware, `O` optional, `P` placeholder envelope only

```
VOLLEY_Gen6                                    (root, no bodies)
├── 00_REFERENCE
│   ├── Stage_Rail_REFERENCE            H P    host structure, drawn to check the interface
│   └── Host_Mount_Datum_REFERENCE      H      construction geometry only, no body
├── 10_PRESSURE
│   ├── Reservoir                       V P    200 bar bottle, 3.46 L
│   ├── Reservoir_Mounts                V —    DOES NOT EXIST
│   ├── Pressure_Chamber                V P    2.0 L at 22.7258 bar
│   ├── Chamber_Mounts                  V —    DOES NOT EXIST
│   ├── Valve_Manifold                  V —    DOES NOT EXIST (fill + fire)
│   ├── Plumbing                        V —    DOES NOT EXIST
│   └── Relief_Safety                   V —    DOES NOT EXIST
├── 20_DRIVE
│   ├── Drive_Tube                      V      the bore AND the rail; the one authoritative solid
│   ├── Support_1 … Support_7           V —    stations known, hardware DOES NOT EXIST
│   └── Trim_Stator                     O P    SUSPENDED by ADR-036; build last or not at all
├── 30_CARRIAGE                                ← everything here is P108-dependent
│   ├── Free_Piston                     V P    12 mm disc in build_gen6; NOT a piston design
│   ├── Front_Land                      V —    DOES NOT EXIST as geometry
│   ├── Rear_Land                       V —    DOES NOT EXIST as geometry
│   ├── Seal_Gland                      V —    DOES NOT EXIST
│   ├── Seal                            V —    class named, geometry DOES NOT EXIST
│   └── Payload_Cradle                  V P    seat + two stops; envelope only
├── 40_MAGAZINE
│   ├── Magazine_Cassette               V P    carried across from Gen5
│   ├── Magazine_Interface              V —    cassette→bore transition DOES NOT EXIST
│   └── Release_Retention               V —    DOES NOT EXIST
├── 50_SENSING                          V —    all DOES NOT EXIST
│   ├── Pressure_Transducer, Temp_Sensor, Velocity_Sensor
└── 60_ELECTRICAL                       V —    DOES NOT EXIST
```

Build 00, 10, 20 and 40 now. Leave 30 fully parametric. 50/60 are envelopes only when they
exist.

---

## 2. Coordinate system and datums

Global X = firing direction = bore axis. Z up (payload sits below the tube axis in
`build_gen6`). Y completes right-handed. Origin at `x = 0`.

| Datum | x (mm) | Status | Defined by |
|---|---:|---|---|
| CHAMBER_FACE / x = 0 | 0.000 | FIXED | `build_gen6` origin: the piston pressure face at rest |
| Tube rear end | −30.000 | FIXED | tube extruded `L + 60` translated `−30` |
| BORE_START | 0.000 | AMBIGUOUS, see below | not separately defined anywhere |
| BORE_END / MUZZLE | 8000.000 | FIXED | `stroke_mm` |
| Tube front end | 8030.000 | FIXED | same extrusion |
| PISTON_FACE (t=0) | 0.000 | FIXED | coincident with CHAMBER_FACE |
| Piston rear (as drawn) | 12.000 | PLACEHOLDER | 12 mm disc, `build_gen6.carriage()` |
| FRONT_LAND datum | UNRESOLVED | P108_DEPENDENT | no land geometry exists |
| REAR_LAND datum | UNRESOLVED | P108_DEPENDENT | no land geometry exists |
| BODY_REF / CG datum | UNRESOLVED | P108_DEPENDENT | A71 places it midway between lands |
| Cradle seat start | 12.000 | PLACEHOLDER | `carriage()` |
| Cradle seat end | 352.500 | PLACEHOLDER | `12 + 2 × 170.25` |
| Cradle stop 1 / stop 2 | 16.000 / 348.500 | PLACEHOLDER | `carriage()` |
| PAYLOAD datum | seat top face, z = −(payload_height/2) − 4 | PLACEHOLDER | `carriage()` |
| TRIM_START | 7855.990 | COMPUTED_CURRENT | `gen6_trim.section_start_mm`, A55 |
| TRIM_END | 8000.000 | COMPUTED_CURRENT | start + 144.01 |
| SUPPORT_1 ... 7 | 1000 ... 7000, 1000 pitch | COMPUTED_CURRENT | A59; A69 models them here |
| HOST_MOUNT datum | rail top face z = −60.000 | HOST_DEPENDENT | `stage_rail()`, unvalidated |
| Magazine interface | UNRESOLVED |, | no transition geometry exists |

> ### The axial-datum ambiguity A71 exposed, read before sketching the carriage
>
> `x = 0` is used for three different things and they are not the same point.
>
> 1. the piston pressure face at rest, which is where the gas acts;
> 2. the start of the usable bore, which is where guiding begins;
> 3. the body reference the dynamics integrate, which A71 places midway between the two
>    lands, so at `t = 0` A71 starts the body at `x = land_separation / 2`, precisely so that
>    the rear land is not outside the tube.
>
> `cad/parameters.json` contains no dimension separating them. The 8000 mm stroke is measured
> from `x = 0`; whether the piston *face* or the *rear land* is at `x = 0` at rest changes the
> usable stroke by the piston's own length. Do not resolve this by assumption. Create the three
> planes below and drive everything from them; the offsets between them become real when P108
> fixes the land geometry.
>
> Create in Fusion, in the root component:
> `PL_CHAMBER_FACE` at x=0, `PL_BORE_START` at `x = 0 + BoreStartOffset` (parameter, default 0)
>, `PL_BODY_REF` at `x = LandSeparation/2`, `PL_MUZZLE` at `x = Stroke`.

---

## 3. Master parameter table

Create all of these as Fusion user parameters before any sketch. Status key:
`FIXED` will not move, `COMPUTED_CURRENT` current result, may move on re-run ·
`OPTIMISABLE` a free design variable, `P108_DEPENDENT` blocked on guided-contact ·
`P67_DEPENDENT` blocked on the seal measurement, `HOST_DEPENDENT` blocked on a launch provider ·
`HARDWARE_MEASURED` needs metal, `PLACEHOLDER` a drawing convenience, not a design

| Fusion name | Value | Unit | Source | Analysis / ADR | Status |
|---|---:|---|---|---|---|
| `Bore` | 15.805 | mm | `gen6_drive.bore_mm` | A41/A49 | FIXED |
| `TubeWall` | 1.0 | mm | `gen6_drive.tube_wall_mm` | A59 band 1, 13.9x margin | FIXED |
| `TubeOD` | 17.805 | mm | `Bore + 2*TubeWall` | derived | FIXED |
| `Stroke` | 8000.0 | mm | `gen6_drive.stroke_mm` | ADR-034 | FIXED |
| `PistonArea` | 196.2 | mm² | `gen6_drive.piston_area_mm2` | π·Bore²/4 | FIXED |
| `ChargePressure` | 22.7258 | bar | `gen6_store.charge_pressure_bar` | ADR-034 | FIXED |
| `CommandedForce` | 445.88 | N | `gen6_drive.commanded_force_N` | `PistonArea × ChargePressure` | FIXED |
| `ChamberVolume` | 2.0 | L | `gen6_store.chamber_volume_l` | A41 | COMPUTED_CURRENT |
| `ChamberRadius` | 60.0 | mm | `build_gen6.chamber()` | none, drawing choice | PLACEHOLDER |
| `ChamberWall` | 3.0 | mm | `build_gen6.chamber()` | none, not a vessel calc | PLACEHOLDER |
| `ChamberLength` | 176.839 | mm | derived from volume and radius |, | PLACEHOLDER |
| `ReservoirVolume` | 3.46 | L | `gen6_store.reservoir_volume_l` | A56, sized | COMPUTED_CURRENT |
| `ReservoirPressure` | 200.0 | bar | `gen6_store.storage_pressure_bar` | A42 | COMPUTED_CURRENT |
| `ReservoirRadius` | 90.0 | mm | `build_gen6.reservoir()` | none, drawing choice | PLACEHOLDER |
| `ReservoirWall` | 6.0 | mm | `build_gen6.reservoir()` | none | PLACEHOLDER |
| `ReservoirLength` | 135.969 | mm | derived |, | PLACEHOLDER |
| `FillOrifice` | 1.0 | mm | `gen6_store.fill_orifice_mm` | A42, 4.14 s first fill | COMPUTED_CURRENT |
| `SupportPitch` | 1000.0 | mm | A59 | seven supports | COMPUTED_CURRENT |
| `SupportStation_n` | 1000·n, n=1...7 | mm | A59 / A69 |, | COMPUTED_CURRENT |
| `SupportPlacementTol` | ±0.05 | mm | A69 declared | A69 | OPTIMISABLE |
| `DiametralClearance` | 0.050 | mm | A67 declared bracket 0.020-0.200 | no repository source | P108_DEPENDENT / OPTIMISABLE |
| `LandSeparation` | 120.0 | mm | A67 declared, swept 40-400 | no repository source | P108_DEPENDENT |
| `LandLength` | UNRESOLVED | mm |, | does not exist anywhere | P108_DEPENDENT |
| `PistonLength` | 12.0 | mm | `build_gen6.carriage()` | drawing convenience only | PLACEHOLDER / P108_DEPENDENT |
| `TubeMaterial` | 6061-T6, hard anodised |, | `gen6_drive.tube_material` | ADR-035 | FIXED |
| `PistonMaterial` | 6061-T6, matched |, | `gen6_drive.piston_material` | ADR-035, A58 band 6 | FIXED |
| `TubeTempCeiling` | 473 | K | `gen6_drive.tube_temperature_ceiling_K` | ADR-035 | FIXED |
| `SealFriction` | 17.8 | N | `gen6_seal.friction_max_N` | A61, 4.00 % of p₀A | P67_DEPENDENT |
| `SealFrictionAllowance` | 83.404 | N | `gen6_seal.friction_allowance_N` | A41 ceiling | P67_DEPENDENT |
| `SealGlandGeometry` | UNRESOLVED |, |, | class only: filled-PTFE glide ring | P67_DEPENDENT |
| `SealMass` | 0.002 | kg | `gen6_seal.seal_mass_kg` | A58 band 5 | PLACEHOLDER |
| `TrimSectionLength` | 144.01 | mm | `gen6_trim.section_length_mm` | A55 | SUSPENDED (ADR-036) |
| `TrimSectionStart` | 7855.99 | mm | `gen6_trim.section_start_mm` | A55 | SUSPENDED |
| `TrimBeltDepth` | 6.0 | mm | `build_gen6.trim_stator()` | none, drawing choice | PLACEHOLDER |
| `CradleLever` | 170.25 | mm | `gen6_drive.cradle_contact_lever_mm` | A34: half the payload length | COMPUTED_CURRENT |
| `CradlePreload` | 201.7 | N | `gen6_drive.cradle_preload_N_per_contact` | A38 at the 25 g cap; P102 keeps it as the conservative figure, design point needs 91.7 | COMPUTED_CURRENT |
| `CellLengthX / SectionY / SectionZ` | 340.5 / 100.0 / 100.0 | mm | `payload_cell` | ADR-025 | FIXED |
| `CellPitchZ` | 104.0 | mm | `payload_cell.cell_pitch_z` | ADR-025 | FIXED |
| `CellsTotal` | 12 |, | `payload_cell.cells_total` | ADR-025 | FIXED |
| `CassetteLX/WY/HZ` | 380.5 / 166 / 690 | mm | `magazine` | Gen5 | COMPUTED_CURRENT |
| `RailWidth / RailHeight` | 120 / 40 | mm | `build_gen6.stage_rail()` | none, invented to draw an interface | HOST_DEPENDENT / PLACEHOLDER |
| `RailTopZ` | −60.0 | mm | derived |, | HOST_DEPENDENT |

---

## 4. SAFE TO MODEL NOW

These do not move when P108 or A72 lands. Build them natively.

### 4.1 `Drive_Tube`, the one authoritative solid

| | |
|---|---|
| Sketch plane | `YZ` at `x = −30` |
| Sketch | two concentric circles, ⌀`TubeOD` and ⌀`Bore` |
| Feature | Extrude +X, distance `Stroke + 60` |
| Result | spans x = −30 ... 8030, wall 1.0 mm |
| Material | Aluminium 6061-T6; add a surface finish note: hard anodised bore |
| Interfaces | supports at 1000·n; trim belt OD at 7855.99...8000; bore is the guiding surface |
| Joints | Rigid to root at origin. It is the assembly's spine, everything else joints to it |

> Do not put a fillet, chamfer or lead-in on either bore end. The muzzle exit geometry is
> P108-dependent (§5).

### 4.2 `Support_1 … Support_7`, stations only

Create seven construction planes offset from `PL_CHAMBER_FACE` at `SupportStation_n`. Do not
model support hardware: none exists. A59 gives spacing and a 99.7 g total mass allowance for
all seven; A69 models them as rigid transverse constraints with ±0.05 mm placement.

### 4.3 `Pressure_Chamber`, envelope, correctly labelled

Revolve/extrude on `YZ` at `x = −ChamberLength` (aft of the piston face): OD `2·(ChamberRadius +
ChamberWall)` = 126 mm, ID 120 mm, length 176.839 mm, with 3 mm end caps both ends.
Name the component `Pressure_Chamber_ENVELOPE`. Radius, wall and cap thickness are drawing
choices, see §9.

### 4.4 `Reservoir`, envelope, correctly labelled

Same construction: OD 192 mm, ID 180 mm, length 135.969 mm, 6 mm caps.
Name it `Reservoir_ENVELOPE`. Position is free, it is not on the bore axis in any file.
Joint it as-built to the rail reference, not to the tube.

### 4.5 `Magazine_Cassette`

Box 380.5 x 166 x 690, shelled −4 mm from the +Z face. Pattern the payload cell at
`CellPitchZ` = 104 mm, six per cassette, two cassettes. Cell 340.5 x 100 x 100.

### 4.6 `Stage_Rail_REFERENCE`

Box 8200 x 120 x 40, top face at z = −60, spanning x = −100 ... 8100.
Suppress it in any mass rollup and name it `_REFERENCE`. No provider has agreed to anything
(E5).

### 4.7 Datum planes (create first, before any body)

`PL_CHAMBER_FACE` (x=0), `PL_BORE_START` (x = `BoreStartOffset`, default 0) ·
`PL_BODY_REF` (x = `LandSeparation`/2), `PL_MUZZLE` (x = `Stroke`) ·
`PL_TRIM_START` (x = `TrimSectionStart`), `PL_SUPPORT_1…7`.

---

## 5. DO NOT FREEZE BEFORE P108

Everything in `30_CARRIAGE`. A71 did not converge; the exit-state model that would size these
is unresolved, and A70 additionally found that land separation has a thermal-admissibility
ceiling (400 mm is inadmissible at a 1 K across-diameter gradient, 200 mm at 5 K).

| Dimension | Why it may move | Parameterise as |
|---|---|---|
| `LandSeparation` | A67 band 8: longer lands lower tip-off; A70: longer lands jam sooner. Two-sided, with an optimum nobody has found | User parameter. Drive land positions from `PL_BODY_REF` ± `LandSeparation/2` |
| `LandLength` | Does not exist. Sets contact area, hence pressure and friction | User parameter, default 10 mm, marked UNRESOLVED |
| `DiametralClearance` | A67's dominant geometric input; A69 shows pressure alone opens the bore 3.44 µm (6.9 %) | User parameter. Never model the land at nominal ⌀; always `Bore − DiametralClearance` |
| `PistonLength` | 12 mm is a drawing convenience | User parameter |
| Rigid vs compliant land | A71's three named routes include making the piston compliant so contact stiffness is physical. That is an architecture change, not a dimension | Model the carriage as a separate component with the lands as child components. A compliant land becomes a swap, not a rebuild |
| Muzzle / guide exit geometry | Where guiding stops sets the last contact and the release pose | No lead-in, no chamfer. Leave the bore prismatic to `PL_MUZZLE` |
| Support layout | Sagitta ∝ span²; halving the pitch quarters it | Keep the seven planes driven by `SupportPitch`, not hard-numbered |

Fusion technique so these can change later without a rebuild:
1. All seven values as user parameters, never typed into a sketch.
2. Land bodies in their own components, jointed to `PL_BODY_REF` by Slider joints with
   offsets `±LandSeparation/2`, changing the parameter slides them, it does not re-solve a sketch.
3. Sketch the land radially from the tube axis using `Bore − DiametralClearance`, never an
   absolute diameter.
4. No assembly-level dimension between a land and the cradle. Drive both from `PL_BODY_REF`.

---

## 6. Current STEP file map, `cad/step/gen6/`

| File | Represents | Import directly? | Status | Action |
|---|---|---|---|---|
| `VOLLEY_Drive_Tube_Gen6.step` | 8060 mm tube, ⌀17.805/15.805 | Yes | Authoritative | Remodel natively, it is 4 dimensions and you want the parametric version |
| `VOLLEY_Chamber_Gen6.step` | 126/120 ⌀ x 176.839, 3 mm caps | Yes | Provisional envelope | Import as reference body, then remodel when a vessel calc exists |
| `VOLLEY_Reservoir_Gen6.step` | 192/180 ⌀ x 135.969, 6 mm caps | Yes | Provisional envelope | Reference body |
| `VOLLEY_Carriage_Gen6.step` | 12 mm disc + seat + 2 stops | Yes | PLACEHOLDER | Do not import. §5 |
| `VOLLEY_Magazine_Cassette_Gen6.step` | 380.5x166x690 shelled | Yes | Provisional | Remodel natively, you will pattern cells into it |
| `VOLLEY_Stage_Rail_Gen6.step` | 8200x120x40 box | Yes | Host reference, invented | Reference body, suppressed from mass |
| `VOLLEY_Trim_Stator_Gen6.step` | ⌀29.805/17.805 x 144.01 belt | Yes | SUSPENDED | Leave out; build last if P67 requires it |

---

## 7. Missing hardware

`C` computable now, `VS` vendor selection from public data, `HW` needs metal, `HO` needs a host

| Component | Status | Owned by |
|---|---|---|
| Seal + gland geometry | P67 / HW | P67, P89; class named, geometry absent |
| Fill valve, fire valve | VS | E3, select from public data |
| Regulator |, | Deleted by A41 (P63 closed by removing the component) |
| Fittings, plumbing, line volumes | VS / C | E3; line volume feeds the gas model |
| Pressure transducer | VS | E3 |
| Temperature sensors | VS | E3 |
| Velocity sensor | VS | E7, 1.4 ms loop, single pass, no window |
| Reservoir mounts, chamber mounts | C | not started |
| Tube supports (7) | C | A59 gives 99.7 g total and no hardware |
| Structural brackets, fasteners | C | not started |
| Release / retention mechanism | C | A34: 201.7 N per contact releasing inside <=1 N; does not exist in any file |
| Cassette to bore transition | C | not started |
| Electrical connectors, harness | VS | not started |
| Trim electronics + pulse store | P67 / VS | ADR-036 suspended; A64 prices the store at ~70 g |
| Pressure relief / safe state | C | E32, ascent inhibit and fault logic |
| Host mechanical interface | HO | E5, P94, P68 |

---

## 8. Fusion build order

```
STEP 1   New design, units mm. Create ALL §3 user parameters first. Do not sketch yet.
STEP 2   Root component VOLLEY_Gen6. Create the §4.7 datum planes.
STEP 3   00_REFERENCE: import Stage_Rail STEP as a reference body, suppress from mass.
STEP 4   20_DRIVE / Drive_Tube: model natively per §4.1. Rigid-joint to root at origin.
STEP 5   Support planes 1..7 from SupportPitch. No hardware.
STEP 6   10_PRESSURE: Pressure_Chamber_ENVELOPE and Reservoir_ENVELOPE per §4.3/§4.4.
STEP 7   40_MAGAZINE: cassette natively, pattern 6 cells at CellPitchZ, mirror for 12.
STEP 8   30_CARRIAGE: create the COMPONENT and its child components Front_Land, Rear_Land,
         Seal_Gland, Free_Piston, Payload_Cradle — EMPTY. Add Slider joints to PL_BODY_REF at
         ±LandSeparation/2. Do not sketch a land profile yet.
STEP 9   Sanity: section view along X. Confirm the bore is prismatic 0..8000 and nothing
         intrudes into it.
STEP 10  STOP. Everything after this is P108-dependent or vendor selection.
```

---

## 9. Existing CAD defects and placeholders, do not mistake these for design

| In `build_gen6.py` | What it actually is |
|---|---|
| `chamber()` | `r = 60`, `wall = 3` are hard-coded drawing choices. No pressure-vessel calculation sets either. MAWP, proof, burst, fracture mode and cycle count are all unanalysed |
| `reservoir()` | `r = 90`, `wall = 6`, same. A 200 bar vessel whose wall was chosen to look right |
| `carriage()` | A 12 mm disc, a flat seat and two 8 mm stops. There is no piston, no land, no gland and no seal. The `−0.1 mm` on the piston radius is not a clearance specification |
| `stage_rail()` | A 120 x 40 box invented to have something to check against. No provider has agreed to anything |
| `magazine_cassette()` | A shelled box carried across from Gen5. No cells, gates, followers or escapement |
| `trim_stator()` | A 6 mm annular belt. ADR-036 suspended the subsystem; the winding, iron, magnets and pulse store are all absent |
| Supports | Not drawn at all. Seven stations, no hardware |
| All parts | No fillets, no fasteners, no harness, no tolerances |

---

## START HERE IN FUSION

Checklist for the Fusion assistant.

1. Import as reference only: `VOLLEY_Stage_Rail_Gen6.step`, `VOLLEY_Chamber_Gen6.step`,
   `VOLLEY_Reservoir_Gen6.step`. Mark all three reference / excluded from mass.
2. Do not import `VOLLEY_Carriage_Gen6.step`. It is a placeholder.
3. Create every parameter in §3 before the first sketch. Values and names exactly as given.
4. Build immediately, natively: `Drive_Tube` (§4.1), support planes (§4.2),
   `Magazine_Cassette` + cell pattern (§4.5), the four datum planes (§4.7).
5. Create but leave empty: `Front_Land`, `Rear_Land`, `Seal_Gland`, `Free_Piston`,
   `Payload_Cradle`, jointed to `PL_BODY_REF`, no profiles.
6. Never type a number into a sketch for: land separation, land length, clearance, piston
   length, muzzle lead-in.
7. Do not invent: land length, gland cross-section, seal squeeze, valve envelopes, support
   bracket geometry, cassette to bore transition, the offset between `PL_CHAMBER_FACE` and
   `PL_BORE_START`, or any wall thickness for the chamber or reservoir.
8. Materials: tube and piston 6061-T6, bore hard anodised. Chamber and reservoir
   material is unassigned, no vessel calculation exists.
9. If a dimension is needed and not in §3, it does not exist. Name it and stop.
