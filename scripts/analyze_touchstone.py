#!/usr/bin/env python3
"""Inspect Touchstone v1 .sNp data and check passive N-port S-matrices.

This is a new reconstruction, NOT the author's original internship script.
Requires numpy; matplotlib is optional unless plots are requested.
"""
import argparse
import csv
import json
import re
from pathlib import Path

import numpy as np

UNITS = {'HZ': 1., 'KHZ': 1e3, 'MHZ': 1e6, 'GHZ': 1e9}


def read_touchstone(path):
    path = Path(path)
    match = re.search(r'\.s(\d+)p$', path.name, flags=re.I)
    if not match:
        raise ValueError('Expected a .sNp file, for example data.s2p or data.s3p')
    n = int(match.group(1))
    if n < 1:
        raise ValueError('Port count must be positive')
    unit, form, z0 = 'GHZ', 'MA', 50.0  # Touchstone v1 defaults
    numeric = []
    with path.open(encoding='utf-8-sig') as handle:
        for line in handle:
            line = line.split('!', 1)[0].strip()
            if not line:
                continue
            if line.startswith('['):
                raise ValueError('Touchstone v2 keywords are not supported; export a v1 .sNp file')
            if line.startswith('#'):
                words = line[1:].upper().split()
                if not words or words[0] not in UNITS or 'S' not in words:
                    raise ValueError('Only Touchstone S-parameter data with a supported frequency unit is accepted')
                unit = words[0]
                form = next((a for a in words if a in ('RI', 'MA', 'DB')), None)
                if form is None:
                    raise ValueError('Missing RI, MA or DB format in option line')
                if 'R' in words:
                    j = words.index('R')
                    if j + 1 >= len(words):
                        raise ValueError('Missing reference impedance after R')
                    z0 = float(words[j + 1])
                if not np.isfinite(z0) or z0 <= 0:
                    raise ValueError('Reference impedance must be finite and positive')
                continue
            numeric.extend(float(v.replace('D', 'E').replace('d', 'e')) for v in line.split())
    width = 1 + 2 * n * n
    if not numeric or len(numeric) % width:
        raise ValueError(f'Incomplete data: expected {width} numbers per frequency record')
    records = np.asarray(numeric).reshape(-1, width)
    frequency = records[:, 0] * UNITS[unit]
    if np.any(~np.isfinite(frequency)) or np.any(frequency < 0) or np.any(np.diff(frequency) <= 0):
        raise ValueError('Frequencies must be finite, nonnegative and strictly increasing')
    pairs = records[:, 1:].reshape(-1, n * n, 2)
    first, second = pairs[:, :, 0], pairs[:, :, 1]
    if form == 'RI':
        values = first + 1j * second
    elif form == 'MA':
        values = first * np.exp(1j * np.deg2rad(second))
    else:
        values = 10 ** (first / 20) * np.exp(1j * np.deg2rad(second))
    # Touchstone 1.0 is column-major: S11,S21,S12,S22 for 2 ports.
    return frequency, values.reshape(-1, n, n).transpose(0, 2, 1), z0


def checks(smatrix):
    if not np.all(np.isfinite(smatrix)):
        raise ValueError('Nonfinite S-parameter values')
    max_sv = np.linalg.svd(smatrix, compute_uv=False)[:, 0]
    asym = np.max(np.abs(smatrix - smatrix.swapaxes(1, 2)), axis=(1, 2))
    return max_sv, asym


def analyze(path, target_ghz=10.0, out_dir=None, make_plots=True, tol=1e-3):
    freq, s, z0 = read_touchstone(path)
    n = s.shape[1]
    max_sv, asym = checks(s)
    idx = int(np.argmin(np.abs(freq - target_ghz * 1e9)))
    db = 20 * np.log10(np.maximum(np.abs(s), 1e-15))
    phase = np.angle(s, deg=True)
    print(f'{n}-port Touchstone: {path} | {len(freq)} points | Z0={z0:g} ohm')
    print(f'Nearest point to {target_ghz:g} GHz: {freq[idx]/1e9:.6g} GHz')
    print('Rows = observed/output ports; columns = excited/input ports')
    for row in db[idx]:
        print('  ' + '  '.join(f'{x:8.3f}' for x in row) + ' dB')
    print(f'Max singular value: {max_sv[idx]:.6g} (<=1+{tol:g}: {max_sv[idx] <= 1 + tol})')
    print(f'Max reciprocity error: {asym[idx]:.6g} (<= {tol:g}: {asym[idx] <= tol})')
    output = Path(out_dir) if out_dir else Path(path).with_suffix('')
    output.mkdir(parents=True, exist_ok=True)
    summary = {'source': str(path), 'nports': n, 'points': len(freq), 'z0_ohm': z0,
               'target_ghz': target_ghz, 'sample_ghz': float(freq[idx]/1e9),
               's_db_rows_output_columns_input': db[idx].tolist(),
               'largest_singular_value': float(max_sv[idx]),
               'reciprocity_max_abs_error': float(asym[idx]),
               'passivity_at_sample': bool(max_sv[idx] <= 1 + tol),
               'reciprocity_at_sample': bool(asym[idx] <= tol)}
    (output/'summary.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    with (output/'checks.csv').open('w', newline='', encoding='utf-8') as handle:
        writer = csv.writer(handle)
        writer.writerow(['frequency_hz','max_singular_value','max_reciprocity_error'])
        writer.writerows(zip(freq, max_sv, asym))
    if make_plots:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        for matrix, ylabel, filename in ((db, 'Magnitude (dB)', 'sparameters_db.png'),
                                          (phase, 'Phase (degrees)', 'sparameters_phase.png')):
            fig, ax = plt.subplots(figsize=(9, 5))
            for i in range(n):
                for j in range(n):
                    ax.plot(freq/1e9, matrix[:, i, j], label=f'S{i+1}{j+1}')
            ax.set(xlabel='Frequency (GHz)', ylabel=ylabel)
            ax.grid(True, alpha=.3)
            ax.legend(ncol=min(4, n), fontsize=8)
            fig.tight_layout()
            fig.savefig(output/filename, dpi=160)
            plt.close(fig)
        fig, ax = plt.subplots(figsize=(9, 4.5))
        ax.plot(freq/1e9, max_sv, label='Largest singular value')
        ax.axhline(1, linestyle='--', label='Passivity threshold')
        ax.plot(freq/1e9, asym, label='Max |S - S.T|')
        ax.set(xlabel='Frequency (GHz)', ylabel='Dimensionless metric')
        ax.legend(); ax.grid(True, alpha=.3); fig.tight_layout()
        fig.savefig(output/'passivity_reciprocity.png', dpi=160)
        plt.close(fig)
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', type=Path, help='.sNp file generated from simulation')
    parser.add_argument('--freq-ghz', type=float, default=10.0)
    parser.add_argument('--out-dir', type=Path)
    parser.add_argument('--no-plots', action='store_true')
    parser.add_argument('--tolerance', type=float, default=1e-3)
    args = parser.parse_args()
    analyze(args.file, args.freq_ghz, args.out_dir, not args.no_plots, args.tolerance)


if __name__ == '__main__':
    main()
