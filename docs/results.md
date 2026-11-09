# Results and interpretation

The following descriptions are taken from an **internship working report dated July 2026**. They are **not results of a fresh simulation run in this repository**.

| Analysis | Reported outcome | Limitation |
| --- | --- | --- |
| DC IC–VBE | Collector current rises sharply as VBE increases | No extracted device-model fit supplied |
| DC IC–VCE | Output current depends on base bias; finite output slope | Early characterization only |
| AC gain | Large low/mid-frequency gain, with roll-off at higher frequencies | Artificially large ideal passives |
| S21 | Around +20 dB in a broad section of the documented sweep | Does not establish 50 Ω power matching |
| S11 / S22 | Poor, frequency-dependent port matching | No matching network designed |
| S12 | Low reverse transmission at lower frequencies, increasing at higher frequency | Strong dependence on operating point and model |
| NF / NFmin | Around 1.5 dB / 0.5 dB respectively in the lower-frequency region | Approximate values read from documented plots, not measurements |
| Noise resistance | Approximately 21 Ω at lower frequencies | Bias- and frequency-dependent |
| Sopt | Noise-optimum source reflection differs from a perfect 50 Ω match | No implemented noise-match circuit |
| K / determinant magnitude / MSG | K below 1 over a large portion of sweep; MSG falls with frequency | Unconditional stability **not** demonstrated |

## Main engineering takeaway

The HBT can show forward transmission even when its input/output are poorly matched. Gain, noise matching and stability are **distinct design constraints**. The next design step would be to select a practical target frequency/bias point and develop stabilization and matching networks around it.

## Artifact provenance

The only supplied netlist snapshot in this repository uses base/collector source values of **0.85 V / 1.2 V**, while the report specifies **0.8 V / 2.0 V** in its RF/AC methodology. Numerical results must not be attributed to that snapshot without restoring the appropriate conditions and checking the simulator version.

The original report also contains some uncompleted template sections and figure-caption inconsistencies. It is treated as a **working research record**, not a fully independently verified publication.
