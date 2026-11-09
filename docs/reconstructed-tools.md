# Reconstructed analysis tools — provenance and usage

**Important:** The scripts in `scripts/` were newly written in November 2026 from the scope and layer descriptions in the historical KIT report. **They are not the original internship scripts** and must not be presented as those scripts. The provided `.spice` snapshot and original PDF are historical artifacts; source reconstruction is separate.

## What works without SG13G2 or openEMS

Install `numpy` and, for plots, `matplotlib`. Then inspect an *actual* Touchstone v1 file:

```bash
python scripts/analyze_touchstone.py path/to/your_model.s3p --freq-ghz 10 --out-dir generated_analysis
python -m unittest discover -s tests -v
```

The tool accepts `.s1p`, `.s2p`, `.s3p` and higher N-port data in Touchstone v1 S-parameter format (RI, MA, DB). It returns all `Sij` plots, magnitude/phase, passivity (largest singular value), reciprocity (`max|S-S.T|`), a JSON summary and CSV metrics. Its rows represent **output ports** and columns **excited ports**, using the Touchstone column-major ordering. It rejects Touchstone v2 keywords rather than incorrectly guessing their layout.

**Passivity interpretation:** For a power-wave S-matrix with equal real reference impedances, largest singular value <= 1 is a necessary condition for passive behavior. This numerical check does not prove that a model is physically correct. Reciprocity is expected only for reciprocal structures.

## GDS reconstruction (not the original source)

```bash
pip install gdstk
python scripts/generate_gds_examples.py --out-dir generated_gds
```

This creates `metal_2port_reconstructed.gds` with documented layer numbers Metal1 8/0 and TopMetal2 134/0, ground 240 × 200 µm, signal 200 × 20 µm, and 10 × 20 µm port markers 201/0 and 202/0. `t_junction_illustrative.gds` creates a sample 3-port layout with 201/0, 202/0 and 203/0 markers; **its exact dimensions were not reported**, so it is only illustrative.

The GDS polygons are planar layout geometry, not an EM material stack. **No DRC, LVS or EM verification was performed for these newly generated examples.** Actual RF loss, impedance and phase require an appropriate process stack, conductor/dielectric properties, mesh, port treatment and convergence test.

## Automatic N-port orchestration

```bash
python scripts/run_auto_nport_interactive.py generated_gds/metal_2port_reconstructed.gds --dry-run
python scripts/run_auto_nport_interactive.py your_verified_layout.gds \
  --driver /path/to/your_openems_model_driver.py --start-ghz 0.1 --stop-ghz 20 --points 201
```

GDS detection uses marker layers 201/0, 202/0, and so on, requiring **one polygon per port** and consecutive port numbering. `--dry-run` creates a configuration manifest without computing or claiming EM results. The real run requires an **external, verified openEMS driver** with the following callable interface:

```python
def build_simulation(gds_path, ports, excite_port, simdir, frequencies_hz, reference_ohm):
    # Return (openEMS FDTD instance, list of openEMS port objects in marker order)
    # Each run must excite only excite_port, terminate all other ports,
    # and recreate fresh simulation objects for this particular excitation.
    ...
```

For each driven port *j*, the runner executes its own FDTD simulation and calculates `Sij = uf_ref_i / uf_inc_j`. It writes `generated_em/<GDS basename>.sNp` in Touchstone v1 RI format. It cannot run without the **historical model stack / layout importer / port construction**, which was not present in the supplied PDFs. The test driver template intentionally raises an exception until those verified process values have been connected.

**Never substitute a toy dielectric thickness, PEC metal or dummy 50 Ω test network and then label the output as an IHP SG13G2 result.**

## Historical evidence vs newly generated output

The original report contains real historical plot screenshots and tables. The files `assets/report-*.jpg` come from that PDF; one should not equate them with the outputs of the newly written programs. The approximate X-band line results are transcribed into `data/reported_custom_line_xband.csv`, clearly marked as reported values rather than a new simulation or `S2_GSG_sim.s2p` file. The original `.s2p` and complete original EM driver have **not** been recovered.

## Ready-to-download example GDS files

The repository also includes `layout_examples/metal_2port_reconstructed.gds` and `layout_examples/t_junction_illustrative.gds`, created newly from the above geometric definitions using standard GDSII boundary records. These are **not the original KIT layout files**. They have been structurally checked as binary GDSII records but not verified in KLayout, nor simulated with openEMS.
