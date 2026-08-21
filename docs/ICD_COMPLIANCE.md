# Launch vehicle interface compliance

**Does a published rideshare interface actually permit deployment at 16.029 m/s?**

Raised in review as the question most likely to invalidate the project independently of whether
the physics works. **It had never been checked.** Conventional dispensers release at 1–2 m/s; if a
provider's stated limit sits near that figure, VOLLEY's central number is non-compliant by 8×
regardless of everything else in this repository.

> **This is a document review, not a validation run.** No acceptance band was declared before
> reading, because there is nothing to compute — the answer is written down in somebody else's
> requirements. It is filed here rather than in `validation/` for that reason. What it does
> follow is `validation/README.md`'s external-document rule: **which document, which revision,
> and whether it was read.**

## Documents read

| Document | Revision | Read? |
|---|---|---|
| Rideshare Payload User's Guide | **Version 10, September 2024** | **Yes**, in full text |
| NRCSD-E CubeSat requirement, deployment velocity withstand | as cited in secondary sources | **No** — figure taken second-hand, flagged below |

---

## The headline: the premise survives

**§3.3.2, Rates and Velocity**, quoted exactly:

> *"Payloads must target a minimum separation velocity of 0.3 m/s and a maximum separation
> velocity of 1.0 m/s. **Containerized deployments such as CubeSats may be deployed at a velocity
> greater than 1.0 m/s.**"*

**A 1.0 m/s cap exists, and containerised CubeSat deployments are explicitly exempted from it.**
No numeric upper bound is placed on containerised deployment velocity anywhere in the document.

**VOLLEY is a containerised CubeSat deployment.** On this interface, at this revision, **16.029 m/s
is not prohibited.** The question that was expected to be lethal is not.

**What this does *not* establish.** One guide is not the market. The exemption is permissive
rather than affirmative — it says CubeSats *may* exceed 1.0 m/s, not that any velocity is
acceptable — and a provider retains approval authority over any specific payload. **An 8×
departure from convention will be scrutinised even where it is not forbidden.**

---

## Three requirements that matter more than the velocity limit

### 1. Deployments must be under active attitude control — and E29 says the host cannot hold it

**§3.3.4, Payload Maneuvers and Deployments:**

> *"All secondary deployments must be performed while under active attitude control. **Deployments
> in uncontrolled directions or during Payload tumbling are not allowed.**"*

**This couples directly to E29 and the coupling is severe.** E29 computes that the shot's angular
impulse about the host centre of mass saturates a 15 N·m·s reaction wheel at roughly **shot four**
for a 50 mm CoM offset — 3.28 N·m·s per shot, 39.3 N·m·s across a campaign.

**A host that has lost attitude authority is not merely degraded; its remaining deployments are
non-compliant.** The requirement converts an attitude-control problem into a **licensing and
approval** problem, and it does so at shot four of twelve.

**This is the strongest argument yet for the CoM-alignment lever**, which attacks the moment arm
rather than the momentum, and it is now a compliance requirement rather than an engineering
preference.

### 2. A seven-day hold before secondary deployments — against a campaign window of about a month

> *"Delay secondary deployments (e.g. a deployed object deploying a sub-Payload) until **at least
> seven days** after Payload separation from the Launch Vehicle."*

**This applies to the hosted last-mile configuration ADR-024 adopted**, where VOLLEY rides a host
that has itself separated from the launch vehicle. The CubeSats are then sub-payloads of a
deployed object.

**E28 already found campaign mission life at a real POEM altitude is about a month** — two GMAT
runs at 350 km reentered at **36 and 29 days**. **Seven days is 20–24 % of the available window,
spent before the first shot.**

It does not apply to VOLLEY mounted as a dispenser on the launch vehicle itself, which is the
dedicated configuration. **The two ConOps therefore have materially different compliance
positions, and the repository has never distinguished them on this axis.**

### 3. An exit-direction requirement the geometry must satisfy

> *"All deployed Payloads must exit through the +X<sub>PL</sub> surface of the allowable Payload
> volume. Customer must show by analysis that none of the deployed Payload Constituents contact
> other portions of the Payload before exiting the +X<sub>PL</sub> surface."*

VOLLEY fires along its own track axis. **Mounted on a radial ESPA port, that axis is not the
launch vehicle's +X.** Whether the deployer's own allowable payload volume is the relevant frame
is exactly the kind of question an interface review turns on, and **it is not answered here.**

The second clause — *show by analysis that no deployed constituent contacts other portions of the
payload* — is a requirement VOLLEY can meet and has partly met: A6 ran the conjunction screen,
A15 measured 396 m worst-case separation. **What it has not analysed is intra-cell contact**,
where A24 found cell-mates leave at identical velocity and never separate, and the proposed
mechanism failed band 6 at femtosat scale (P44).

---

## Numbers to adopt from this document

| Quantity | Value | Bears on |
|---|---|---|
| CubeSat dispenser quasi-static, axial | **10 g** | The structural case. It used to say "GEVS and the 25 g CDS cap"; **the CDS publishes no such cap and GEVS is a random-vibration standard** — 25 g is this design's chosen ceiling (**P98**) |
| CubeSat dispenser quasi-static, lateral (RSS) | **17 g** | Same. **Lateral is the larger number and the repository's structural work is axial-dominated** |
| Launch vehicle rate before separation, roll | ± 2.0 °/s | The tip-off budget, which A23 assesses against a 2 °/s band |
| Launch vehicle rate before separation, pitch/yaw | ± 1.0 °/s | Same |
| Unique deploy signal per separating payload | required | VOLLEY's sequencer commands twelve releases from one mechanism — arguably compliant, not verified |

**The 17 g lateral figure deserves attention.** A18 and A22 sized the retention gates against
random vibration through a 109 Hz mode; this is a separate quasi-static case, in the axis the
gates are least studied in.

---

## The qualification gap, which is paperwork rather than physics

A secondary source reports the **NRCSD-E** requirement that a CubeSat *"shall be capable of
withstanding a deployment velocity of 0.5 to 2.5 m/s at ejection."* **This figure was not read in
the primary document and is flagged as second-hand.**

If it holds, **customer satellites are qualified to a velocity range whose ceiling is 2.5 m/s.
VOLLEY deploys at 16.029 m/s — 6.4× that ceiling.**

**Physically this is a non-issue and the repository can show why:** a satellite is not damaged by
velocity, it is damaged by acceleration, and VOLLEY's **10.07 g against this design's own 25 g ceiling** is well
inside qualification. Velocity is a consequence of acceleration and stroke, and the stroke is the
deployer's problem, not the satellite's.

**Programmatically it is a real barrier.** A customer whose satellite is qualified "per NRCSD-E"
has **no qualification basis** for a 16.0 m/s release, even though nothing about their hardware is
actually threatened. **Paperwork barriers of this kind end space projects that physics does not**,
and closing it means either a qualification argument that translates velocity limits into
acceleration limits, or an accepted difference negotiated per customer.

---

## What is now open

Recorded as register entries rather than left in this file:

- **E31** — the two ConOps have different compliance positions and the repository has never
  distinguished them.
- **E29** gains a compliance consequence: wheel saturation at shot four makes subsequent
  deployments **not allowed**, not merely degraded.
- **The 10 g axial / 17 g lateral dispenser case** is not in any structural analysis here.

**And the survey is one document deep.** A second and third provider's guide should be read before
any claim is made about the market rather than about one interface.
