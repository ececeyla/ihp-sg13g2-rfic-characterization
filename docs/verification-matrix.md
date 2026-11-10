# Internship results and repository files

This table maps the reported KIT work to the files available in the repository.

| Work | Report evidence | Files in this repository | Notes |
| --- | --- | --- | --- |
| HBT DC, AC, RF | Internship report, pages 1–4 | `simulations/S1_npn13G2_RF_Biased_Testbench.spice` | The netlist is one saved configuration, not every report run |
| Noise and stability | NF/NFmin, K and gain plots | Netlist and original report | Simulated HBT behavior, not a fabricated amplifier |
| Reference GSG line | Report, pages 4–5 | Report images | Geometry was an existing example |
| Custom two-port line | Report, page 5 | `data/reported_custom_line_xband.csv`, `layout_examples/metal_2port_reconstructed.gds` | Original GDS and complete two-port dataset are unavailable |
| T-junction | Report, page 6 | `scripts/run_auto_nport_interactive.py` and example layout | The example geometry is not the original GDS |
| HBT DRC/LVS | Report, pages 7–8 | Captured figures in `assets/` | Applies to the original one-device PCell test layout |
| Post-processing | Supplementary to the report | `scripts/analyze_touchstone.py`, `tests/test_touchstone.py` | Uses synthetic fixture data for tests |

The tests check program behavior, not the correctness of the original FDTD mesh, transistor model or physical layout. Reproducing the report requires the original model setup, bias conditions, material stack and simulation scripts.
