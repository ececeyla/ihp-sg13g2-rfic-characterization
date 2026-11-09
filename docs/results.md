# Results and interpretation

The main source is the **9-page IEEE-style KIT internship report** supplied by the researcher, with original simulation screenshots and tables. These are historical **simulation results reported in the document**, not a newly executed run.

For original figures, see **[Full internship report](Ceyla_RFIC_IEEE_Two_Column_Report.pdf)**.

## 1. SiGe npn13G2 HBT circuit characterization

| Analysis | Documented observation | Meaning |
| --- | --- | --- |
| DC IC–VBE | Collector current rises sharply with base bias | Transistor turn-on and model setup |
| DC IC–VCE | Curves shift with base bias; finite slope at larger VCE | Finite output resistance and bias dependence |
| AC response | Strong low/mid-frequency response followed by roll-off | High-frequency parasitic effects |
| S21 | Around +20 dB over a broad part of the reported lower-frequency range | Forward gain despite poor matching |
| S11 / S22 | Frequency-dependent, generally poor 50 Ω matching | Matching networks required |
| NF / NFmin | Around 1.5 dB / 0.5 dB at lower frequencies | Noise mismatch vs optimum source |
| Rn / Sopt | Rn about 21 Ω at low frequency; Sopt not at 50 Ω center | Noise matching differs from power matching |
| K / determinant / MSG | K below 1 across much of sweep; MSG decreases with frequency | Unconditional stability not established |

The 1 MHz–500 GHz sweep is **not** a validated operating frequency or process performance claim.

## 2. Layout-based openEMS results

### Existing GSG reference example

The report describes validating an existing IHP-oriented GSG line workflow via KLayout → AppCSXCAD → openEMS. At **10 GHz** it reports:

- **S11 −35.00 dB**
- **S21 −0.016 dB**
- **S21 phase −5.75°**
- **Input impedance 50.29 − j1.76 Ω**

**Attribution:** This was a pre-existing reference example used to confirm the tool flow, not a newly invented GSG geometry.

### Custom Metal1–TopMetal2 transmission line

A **200 µm × 20 µm TopMetal2** signal trace above a **240 µm × 200 µm Metal1** ground plane was modeled and simulated. The report lists an approximate **S11 of −36 dB**, **S21 of −0.045 dB** and **phase of −4.8°** at **10 GHz**.

**Limitation:** Only Port 1 excitation was documented. The full two-port S-matrix (including independent S12/S22 excitation) was not demonstrated. Mesh convergence was recommended as future work.

### Three-port T-junction and automated N-port analysis

A custom three-port layout with top-metal T-shaped signal conductor and three port markers was evaluated using an adaptation of an existing generic N-port Python flow. The report documents Touchstone `.s3p` generation, nine S-parameters, passivity/reciprocity checks and around **−3.6 dB** for its transmission branches, with approximately **−9.8 dB** diagonal reflections. Values are from a specific reported example; do not treat them as measured hardware performance.

**Attribution:** The generic N-port solver originated in an existing openEMS example. The internship adaptation focused on interactive file/frequency configuration and automatic port detection.

### Single npn13G2 PCell DRC/LVS

A transistor test cell was created in KLayout, terminal labels applied and checked using SG13G2 design rules. The report shows **zero DRC violations** and a successful **LVS match** after using an LVS-compatible netlist and consistent terminal/parameter representation.

**Limitation:** These are verification results for **one transistor test cell**. They are not evidence of a full RFIC implementation or silicon tape-out.

## 3. Technical takeaway

The internship connects transistor-level RF figures of merit to physical layout and EM verification. The transistor simulation phase highlights the distinction between gain, matching, noise and stability. The EM phase shows how GDSII geometry, ports, dielectric stacks and FDTD meshes produce passive microwave S-parameters, and the DRC/LVS phase verifies a small active-device layout.

## Artifact completeness and caveats

- Original plots and screenshots are embedded in the **full report PDF**, which is tracked here.
- The source repository currently includes a standalone `.spice` HBT snapshot but **not** the original EM `.gds`, Python FDTD scripts, Touchstone outputs or full schematic `.sch` files.
- The SPICE snapshot bias values differ from those used in some report figures. Re-run each corresponding testbench before claiming numerical reproducibility.
- Some report text has transcription/formatting errors in PDF and one T-junction result has a sign inconsistency; the values above follow the accompanying explanatory narrative and figures rather than claiming a fresh numerical validation.

## Report figure files

Three original KLayout screenshots from pages 5–7 have been separately archived under `assets/report-*.jpg` and linked from the README. The numerical results are sourced from the original PDF, not those screenshots. See [figure provenance](figure-provenance.md).
