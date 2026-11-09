# Reproducibility and dependencies

## Available artifacts

- [HBT RF testbench](../simulations/S1_npn13G2_RF_Biased_Testbench.spice): provided Ngspice snapshot.
- [Original KIT circuit-to-EM report](Ceyla_RFIC_IEEE_Two_Column_Report.pdf): includes original plots, KLayout screenshots, results tables, DRC/LVS evidence and description of the EM run scripts.
- [IIC-OSIC-TOOLS setup guide](IIC_OSIC_TOOLS_Installation_and_Localhost_Guide.pdf): 14-page installation/localhost workflow.

## Dependencies

Circuit stage: IHP SG13G2 OpenPDK (HBT model), Xschem and Ngspice. The setup used Ubuntu 24.04, Docker and IIC-OSIC-TOOLS.

Physical stage: KLayout, AppCSXCAD, openEMS and appropriate SG13G2 stack definitions. Do not copy/redistribute PDK files or upstream sample code without checking their own licenses.

## Testbench snapshot mismatch

| Parameter | Current standalone SPICE snapshot | Selected RF/AC configurations in the report |
| --- | --- | --- |
| Base supply V2 | 0.85 V | 0.8 V |
| Collector supply V4 | 1.2 V | 2.0 V |
| RF ports | 50 Ω each | 50 Ω each |
| Coupling / RF choke | C1/C2 = 1 F; L3/L4 = 1 H | Same ideal values |
| S-parameter sweep | 1 MHz–500 GHz | Same reported sweep |

These settings intentionally or historically differ across snapshots. A `.spice` file with one bias point is **not** a complete set of all documented experimental runs. The .dc controls for the transistor DC families are not in the provided RF snapshot.

The SPICE file has a local PDK library path:

```spice
.lib /foss/pdks/ihp-sg13g2/libs.tech/ngspice/models/cornerHBT.lib hbt_typ
```

Adapt this to your own environment. A suggested invocation after installing the model is:

```bash
ngspice simulations/S1_npn13G2_RF_Biased_Testbench.spice
```

This command has **not been executed as part of the GitHub import**.

## EM flow described in the report

1. Verify an existing GSG reference layout with SG13G2 materials, port markers and mesh.
2. Build custom Metal1–TopMetal2 geometry in KLayout, marking input/output port locations.
3. Run AppCSXCAD preview, then execute the openEMS FDTD solver.
4. Generate Touchstone and plot S11/S21/phase; for the N-port example, excite each detected port sequentially.
5. Verify a separate single-HBT PCell with the SG13G2 DRC/LVS flow.

**Not yet available as standalone repository files:** the original `.gds` geometries, the modified `run_auto_nport_interactive.py` and `analyze_touchstone.py` scripts, `.s2p/.s3p` outputs, full extracted S-matrices, and the original Xschem schematic source.

## Verification status

The attached documents report the completed experiments. The present repository has not independently reproduced all simulations, validated mesh convergence or tape-out performance. The EM plots shown in the report are real historical artifacts from that report, not synthetic/recreated GitHub charts.
