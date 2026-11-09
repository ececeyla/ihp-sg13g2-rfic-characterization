# Figures, origins and attribution

All image files under `assets/report-*.jpg` were extracted without modification from `docs/Ceyla_RFIC_IEEE_Two_Column_Report.pdf`. The source PDF is the historical July 2026 KIT/IHE internship document.

| File | Source | What it represents |
| --- | --- | --- |
| `report-custom-line-klayout.jpg` | PDF p. 5, Fig. 11 | KLayout view of the custom two-port layout with signal, ground and port markers |
| `report-tjunction-klayout.jpg` | PDF p. 6, Fig. 13 | KLayout view of the three-port T layout |
| `report-hbt-layout.jpg` | PDF p. 7, Fig. 17 | Single npn13G2 test-cell layout (not complete IC) |

These are layout **screenshots** and should not be presented as newly generated solver results. For actual RF simulation plots, matrix outputs and DRC/LVS screenshot evidence, consult the source PDF.

The newly reconstructed code and generated layouts added subsequently to this repository must be labelled separately from the original historical artifacts. No numerical data or measurements are reconstructed from these screenshots.

## Additional original plotted evidence

The following screenshots were also taken directly from the historical PDF, and JPEG-encoded from its embedded images (no new simulation). Source figure images: page 5, custom-line S11/S21/phase; page 6, T-junction S-parameter sweep and matrix printout; page 7, DRC and LVS log figures.

- `report-line-s11.jpg`, `report-line-s21.jpg`, `report-line-phase.jpg`: custom-line plots from p. 5
- `report-tjunction-sparams.jpg`, `report-tjunction-matrix.jpg`: three-port plots/terminal output from p. 6
- `report-drc-log.jpg`, `report-lvs-log.jpg`: original single-HBT layout checks from p. 7

The original plots remain embedded in the complete report PDF. Image re-encoding does not amount to independent re-running of any simulation.
