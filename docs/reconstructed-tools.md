# Analysis tools and examples

The `scripts/` directory contains supplementary utilities written after the KIT internship, based on the analysis workflow and layout dimensions documented in the [report](Ceyla_RFIC_IEEE_Two_Column_Report.pdf). They provide convenient ways to inspect Touchstone data and experiment with GDS geometry; they are **not the original internship source files**.

## Touchstone analysis

```bash
python -m pip install numpy matplotlib
python scripts/analyze_touchstone.py path/to/data.s3p --freq-ghz 10 --out-dir results
```

The parser accepts Touchstone v1 `.sNp` files in RI, MA or DB format. It plots magnitude and phase, calculates passivity and reciprocity metrics, and exports a CSV/JSON summary.

For a passive network with real, equal reference impedances, the largest singular value of the S-matrix should not exceed one. This numerical check is useful, but does not establish physical accuracy or correct material modeling.

The `examples/synthetic_two_port_TEST_ONLY.s2p` file contains three arbitrary data points for checking the parser; it is not an IHP simulation.

## Example GDS layouts

```bash
python -m pip install gdstk
python scripts/generate_gds_examples.py --out-dir generated_gds
```

The two-port example uses the dimensions reported for the custom Metal1–TopMetal2 line: 240 × 200 µm ground, 200 × 20 µm signal and 10 × 20 µm markers. The T-junction example uses the reported marker-layer approach, but illustrative arm dimensions.

These are **geometry examples only**. They have not been verified with the SG13G2 PDK or simulated in openEMS.

## N-port runner

```bash
python scripts/run_auto_nport_interactive.py generated_gds/metal_2port_reconstructed.gds --dry-run
```

Port markers are expected on GDS layers 201/0, 202/0, 203/0, etc., with one marker per port. The dry run records the detected markers.

For an actual EM analysis, the runner needs an external openEMS driver that sets up the verified IHP layer stack, ports, mesh and simulation boundary conditions:

```python
def build_simulation(gds_path, ports, excite_port, simdir, frequencies_hz, reference_ohm):
    # Return the configured FDTD simulation and its ports.
    ...
```

Each port must be driven in a separate simulation to obtain a full N-port S-matrix. The driver template does not invent missing SG13G2 material parameters and therefore cannot run standalone.

## Source of the reported values

Original plotted data and reported RF/EM results are in the [internship report](Ceyla_RFIC_IEEE_Two_Column_Report.pdf). The values in `data/reported_custom_line_xband.csv` are transcribed from the report. Files in `layout_examples/` are later geometry examples, not archived original layouts.
