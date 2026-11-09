# Verification and evidence matrix

This crosswalk helps supervisors and other readers distinguish actual 2026 internship observations, preserved historical sources, newly written reproducibility aids, and unresolved limitations.

| Workstream | Historical evidence | Currently executable repository artifact | Verification boundary |
|---|---|---|---|
| HBT DC / AC / RF | Original 9-page IEEE report (pages 1–4) | Preserved `simulations/S1_npn13G2_RF_Biased_Testbench.spice` | Original snapshot bias differs from selected figure runs; no fresh model simulation claimed |
| Noise / K / MSG | Report plots & Ngspice control expressions | Preserved SPICE testbench | Device-level simulated values, not measured RF amplifier |
| GSG workflow | Report pages 4–5 | No original `.s2p` in repository | Reference geometry came from an existing example; the 8–12 GHz points are not a re-created frequency sweep |
| Custom two-port line | Report page 5, plotted S11/S21/phase | Clearly reconstructed layout in `layout_examples/` | Only Port 1 excitation historically documented; no full original S-matrix or newly verified FDTD |
| Three-port T-junction | Report page 6, S-matrix screenshot | New `scripts/run_auto_nport_interactive.py` and analyzer | Requires original stack and a real openEMS driver; illustrative T geometry is not a historical GDS |
| Single-HBT DRC/LVS | Report pages 7–8, tool logs | Screenshots archived under `assets/` | Reported 0 violations and match apply to the original one-device PCell, **not** reconstructed GDS |
| Postprocessing | Newly written in November 2026 | `scripts/analyze_touchstone.py`, `tests/test_touchstone.py` | Unit tests use fabricated fixture data; unit-test success is **not** a hardware/EM reproduction |

## Demo command

```bash
python -m pip install numpy matplotlib
python scripts/analyze_touchstone.py examples/synthetic_two_port_TEST_ONLY.s2p --freq-ghz 10 --out-dir generated_demo
python -m unittest discover -s tests -v
```

The `examples/synthetic_two_port_TEST_ONLY.s2p` file is a parser fixture containing arbitrary 8, 10, and 12 GHz S-parameter samples. It is not a measurement, not output from IHP models, and not meant to match the original report.

## Reproducibility dependencies

To reproduce the actual KIT RF/EM work one would additionally need the exact model corner, original bias/schematics, SG13G2 process stack and via-port construction, verified openEMS driver, original GDS layouts, and mesh/boundary settings. The existing full PDF remains the primary historical source.
