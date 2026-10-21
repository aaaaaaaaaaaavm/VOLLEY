"""CAD-based material proxy ledger and gate-pin static load sensitivities."""

from pathlib import Path
import json, math, itertools
import FreeCAD as App
import Part
from mechanism import shapes, State, REVISION

H = Path(__file__).parent
records = []
pin = []
rho = {"aluminium": 2.7e-6, "steel": 7.85e-6, "catalogue": 1.4e-6, "payload": 0}
for label, L, payload_mass in [("1U", 113.5, 1.33), ("3U", 340.5, 4.0)]:
    ss, meta = shapes(
        L, State(feed=201, gate=120, bolt=0, payload_feed=200, receiver=0)
    )
    ledger = []
    for n, sh in ss.items():
        material = meta[n][0]
        mass = sh.Volume * rho[material]
        basis = "Assumed homogeneous material density; major/thread/bearing envelopes are not true manufactured material."
        if n == "payload":
            mass = payload_mass
            basis = "Declared mission payload mass, homogeneous rail-surrogate inertia."
        if n == "motor_3242_envelope":
            mass = 0.179
            basis = "Manufacturer mass, homogeneous envelope inertia approximation."
        if n == "nut_SB3700_envelope":
            basis = "Assumed1.4g/cm3 polymer mass; supplier nut mass unverified."
        ledger.append(
            dict(
                part=n,
                material=material,
                volume_mm3=sh.Volume,
                mass_proxy_kg=mass,
                CG_mm=list(sh.Solids[0].CenterOfMass),
                basis=basis,
            )
        )
    total = sum(x["mass_proxy_kg"] for x in ledger)
    cg = [
        sum(x["mass_proxy_kg"] * x["CG_mm"][i] for x in ledger) / total
        for i in range(3)
    ]
    tensor = [[0.0] * 3 for i in range(3)]
    for row in ledger:
        sh = ss[row["part"]].Solids[0]
        m = row["mass_proxy_kg"]
        c = row["CG_mm"]
        d = [c[i] - cg[i] for i in range(3)]
        for i in range(3):
            for j in range(3):
                tensor[i][j] += (
                    m
                    / sh.Volume
                    * getattr(sh.MatrixOfInertia, "A" + str(i + 1) + str(j + 1))
                    + m * ((sum(t * t for t in d) if i == j else 0) - d[i] * d[j])
                ) * 1e-6
    bounds = App.BoundBox()
    for sh in ss.values():
        bounds.add(sh.BoundBox)
    records.append(
        dict(
            payload=label,
            state="sled_captured",
            total_with_payload_proxy_kg=total,
            without_payload_proxy_kg=total - payload_mass,
            CG_with_payload_mm=cg,
            inertia_with_payload_kg_m2=tensor,
            envelope_mm=[bounds.XLength, bounds.YLength, bounds.ZLength],
            ledger=ledger,
        )
    )
    gate_mass = ss["storage_gate"].Volume * rho["aluminium"]
    for g, actuator in itertools.product([5, 10, 25], [0, 50, 200]):
        F = gate_mass * g * 9.80665 + actuator
        d = 6.0
        a = 18.0
        b = 17.0
        span = a + b
        I = math.pi * d**4 / 64
        M = F * a * b / span
        pin.append(
            dict(
                payload=label,
                gate_material_proxy_kg=gate_mass,
                acceleration_g=g,
                additional_actuator_force_assumed_N=actuator,
                total_pin_load_N=F,
                support_span_mm=span,
                load_position_mm=a,
                diameter_mm=d,
                nominal_bending_MPa=32 * M / (math.pi * d**3),
                double_shear_average_MPa=F / (2 * math.pi * d * d / 4),
                wing_projected_bearing_MPa=F / (10 * d),
                simply_supported_deflection_mm=F
                * a
                * a
                * b
                * b
                / (3 * 200000 * I * span),
            )
        )
r = dict(
    revision=REVISION,
    configurations=records,
    pin_static_cases=pin,
    boundary="CAD material and catalogue mass proxies; no installed gearbox/brake/controller, gate actuators, fasteners, wiring, harness, launch locks or thermal hardware. Tensor uses homogeneous component approximations. Pin analysis is a simply-supported beam with assumed200GPa steel; no selected alloy allowable, hole contact, real bracket stiffness, impact, fatigue or qualification.",
)
(H / "METROLOGY.json").write_text(json.dumps(r, indent=2) + "\n")
print(
    [(x["payload"], round(x["without_payload_proxy_kg"], 3)) for x in records],
    ";",
    len(pin),
    "pin load sensitivities",
)
