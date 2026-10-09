# P117 — rated energy, kinematics and mass algebra audit

**Status:** historical-model algebraic energy ledger closes; physical source and loss validation remain open. **Evidence class:** independent calculation from the captured JSON and explicitly stated model assumptions, not a second electromagnetic solver or hardware test.

## Inputs and method

Run `python3 analysis/rated_energy_mass_audit.py`. It reads the captured [`motor_results.json`](../analysis/results/motor_results.json) and [`mass_properties.json`](../analysis/results/mass_properties.json), records their SHA-256 digests, and writes [`rated_energy_mass_audit.json`](../analysis/results/rated_energy_mass_audit.json). It does not import either production model. The equations are ordinary mass summation, $E_k=mv^2/2$, $W=Fs$, $v t/2$ for a constant-acceleration equivalent stroke, and conservation of the *reported* brake terms. Bands were set before evaluating the residuals in the script; the 1 J sled kinetic-energy band accommodates the reported 9.45 kg rounded sled mass.

| Cross-check | Result | Meaning |
|:--|--:|:--|
| Dry parts sum vs reported dry mass | 126.56 vs 126.6 kg | Rounding agrees within 0.1 kg |
| Loaded minus dry, divided by 12 | 4.000 kg per 3U | Matches the rated payload kinetic energy |
| $mv^2/2$ for payload at 16.029 m/s | 513.858 J vs 513.870 J reported | Identity agrees within 0.1 J |
| Constant-acceleration equivalent $vt/2$ | 1.30075 m vs 1.300 m powered stroke | Kinematic consistency only; not a force-history validation |
| Brake force × 39 mm | 51.787 J vs 51.798 J reported | First-order brake work identity agrees |
| Recovered energy after stated losses | 47.035 J vs 47.041 J reported | Rounded brake ledger agrees |
| Net draw | 2782.391 − 47.041 = 2735.350 J vs 2735.3 J reported | Rounding agrees |

The compact result JSON leaves **124.488 J (4.47%)** after subtracting payload and sled kinetic energies, copper heat and bank ESR. Reading the actual historical shot equations resolves that balance:

| Term in the historical model | Energy |
|:--|--:|
| 95% converter assumption applied to discrete mechanical work | 90.964 J |
| 200 W auxiliary assumption over 162.3 ms | 32.460 J |
| Forward-Euler use of updated velocity in $Fv\Delta t$ | 1.064 J |
| Remaining rounded-output difference | 0.0001 J |

The last numerical term follows $\tfrac12 m N(F\Delta t/m)^2$ with 13.445 kg moving mass, 1,623 steps and $\Delta t=10^{-4}$ s. It is an integration artifact, **not a physical energy loss**. The [energy chart](../figures/gen5_energy_accounting.svg) now shows the modelled components of gross draw. This closes only the old model's arithmetic. The 95% converter, 200 W auxiliaries, capacitor bank, winding and recovery do not have selected supplier data or independent coupled-trajectory verification. [C-05](../docs/GEN5_FREEZE_READINESS.md) therefore remains open for an installed electrical design and a force-profile rerun.
