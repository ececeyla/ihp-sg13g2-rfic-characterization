# Reproducibility and dependencies

## Verified file in this repository

`simulations/S1_npn13G2_RF_Biased_Testbench.spice` is a snapshot of the provided Ngspice RF-biased SiGe HBT testbench. Its topology and simulation control commands have been preserved.

## External setup required

- IHP SG13G2 OpenPDK, including the **HBT corner model** (not bundled).
- Ngspice version supporting two-port `sp` analysis and, for noise metrics, its noise option.
- Ubuntu and/or Docker; the internship workflow used **IIC-OSIC-TOOLS** and Xschem.

The netlist contains a machine-specific model directive:

```spice
.lib /foss/pdks/ihp-sg13g2/libs.tech/ngspice/models/cornerHBT.lib hbt_typ
```

Update that path for your local installation. Do not redistribute foundry/PDK libraries or third-party tool sources in this repo.

## Key differences between sources

| Setting | Supplied SPICE snapshot | Values documented for several AC/RF analyses |
| --- | --- | --- |
| Base bias V2 | 0.85 V | 0.8 V |
| Collector supply V4 | 1.2 V | 2.0 V |
| Port reference impedance | 50 Ω | 50 Ω |
| C1, C2 | 1 F each | 1 F each |
| L3, L4 | 1 H each | 1 H each |
| SP sweep | 1 MHz–500 GHz | 1 MHz–500 GHz |

DC sweeps described in the report require their own sweep controls; they are **not included** in the provided SPICE snapshot.

## Running the supplied snapshot

From a working Ngspice environment, run:

```bash
ngspice simulations/S1_npn13G2_RF_Biased_Testbench.spice
```

This is a **suggested invocation**, not evidence that the current file has been successfully rerun here. The simulation should be checked for model-loading warnings, correct port semantics, possible unsupported commands and bias conditions. Visual plot commands can require a graphical display.

## Limitations

- No frozen simulator/PDK commit hash was provided.
- The Xschem `.sch` source file was not supplied; the available `.spice` snapshot is not a substitute for a complete schematic repository.
- No automated CI simulation is configured. Do not infer numerical equivalence from a successful parsing step.
- No layout sign-off, EM result, measured test chip, or finalized RF matching is claimed.

## What would improve reproducibility

1. Record exact Ngspice, Xschem and PDK versions/commits.
2. Save each bias point and sweep as a **separate simulation configuration**.
3. Run the configurations in a documented container.
4. Export numerical results or plots, with frequency windows and input conditions specified.
5. Add validation checks for noise, S-parameters and stability across chosen practical frequency bands.
