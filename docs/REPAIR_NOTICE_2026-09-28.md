# September 2026 engineering record correction

VOLLEY grew quickly, and assumptions that had not been fully checked against source evidence or a matched system comparison entered the main engineering record. Over the past three weeks I have reviewed the direction of the next-generation work and repaired claims that had outrun the evidence. The independent motor-charged launcher-cell bank made the problem clear: it left fired cells installed and did not provide the single reusable, sequentially fed launch path I wanted VOLLEY to investigate.

This release withdraws that arrangement as the selected next design. It is preserved as a dated [VOLLEY-lab study](https://github.com/aaaaaaaaaaaavm/VOLLEY-lab/blob/main/VLAB-X003_independent_cell_bank.md), together with the earlier gas-guide study and the calculations that exposed their limits. The original versions remain in Git history. No new release mechanism, loader, propulsion method, or speed range is selected by this correction.

The repair also separates model output from measurement, a two-payload timing sample from a complete-manifest capability, and random-vibration Grms from static acceleration. It removes universal CubeSat load and provider-fit claims that did not have payload-specific evidence. The Gen5 electromagnetic calculation remains a comparison case; the project has not built or fired a prototype.

The work is **not complete**. Full 1/4/12-payload mission and installed-system comparisons, actual CubeSat and host interface data, feeder and jam behaviour, shot-to-shot speed control, payload contact loads, and calibrated repeated-release tests remain open. Individual validation results are retained with their original inputs and failed cases. The [current status](NEXT_GENERATION_STATUS.md), [open problems](../OPEN_PROBLEMS.md), and [provenance](PROVENANCE.md) control how they may be used.

Going forward, I will require a dated requirement, stated assumptions, a source or calculation, a failure condition, and an independent review before a configuration-specific result becomes a general VOLLEY claim. The next generation remains in development.
