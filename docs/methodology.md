# Methodology

This document summarizes the workflow actually described in the July 2026 working report.

## Hardware/device representation

- Process design kit: **IHP SG13G2** OpenPDK.
- Active device: **npn13G2 SiGe HBT**.
- RF-biased 50 Ω input/output testbench.
- Early characterization employed ideal **1 F coupling capacitors** and **1 H bias inductors**. These values are simulation simplifications, not an integrated RF circuit implementation.

## 1. DC characterization

**IC versus VBE**: sweep base bias from **0.55 to 0.95 V** in **5 mV** steps, keeping the collector supply at **2 V**. The observed exponential-like collector-current increase was used to check device/model setup.

**IC versus VCE**: sweep collector supply from **0 to 2 V**, stepping base bias from **0.70 to 0.90 V** in **50 mV** increments. This provides the family of output characteristic curves.

## 2. Small-signal response

For the documented AC sweep, base bias is **0.8 V**, collector supply **2 V**, input AC amplitude **1 V**, and output excitation is disabled. Compare collector-node and output voltage ratios versus frequency.

## 3. Two-port RF characterization

Use 50 Ω port references and compute **S11, S12, S21, S22**. The documented sweep was **1 MHz to 500 GHz**, but this must not be interpreted as a valid operating range. Use S11 and S22 to evaluate input/output matching, S21 for forward transmission, and S12 for reverse isolation.

Display Smith charts and available impedance/admittance vectors (Z and Y parameters) to check how port properties vary with frequency.

## 4. RF noise analysis

Enable the Ngspice noise-enabled two-port analysis (`sp ... 1`) to examine **NF**, **NFmin**, **Rn** and **Sopt**. The working report describes NF and NFmin and uses an Sopt Smith chart to examine noise-optimal source impedance.

## 5. Stability metrics

Using the complex S-parameter results,

```text
Delta = S11*S22 - S12*S21
K = (1 - |S11|² - |S22|² + |Delta|²) / (2|S12*S21|)
MSG (linear ratio) = |S21 / S12|
MSG (dB) = 10*log10(|S21 / S12|)
```

For conventional two-port unconditional stability, check **K > 1** and **|Delta| < 1**. A region with K below 1 is not guaranteed unconditionally stable, so the working report presents MSG without claiming a fully stable matched amplifier.

## Scope

The report documents device characterization and an open-source post-processing workflow, **not** a tape-out, a completed matching design, or measured silicon performance.
