#!/usr/bin/env python3
"""Detect GDS port-marker layers and orchestrate complete openEMS N-port sweeps.

Requires a project-specific openEMS driver implementing build_simulation(...).
The SG13G2 stack / GDS-to-CSX mapping was not included in the archived PDF,
so the driver must be supplied rather than silently substituting fake stack data.
This file is a new reconstruction, NOT the original internship code.
"""
import argparse
import importlib.util
import json
from pathlib import Path

import numpy as np


def discover_ports(gds_path):
    import gdstk
    library = gdstk.read_gds(str(gds_path))
    tops = library.top_level()
    if len(tops) != 1:
        raise ValueError('GDS must have exactly one top-level cell; select/flatten a cell first')
    cell = tops[0]
    ports = []
    for number in range(1, 100):
        polys = cell.get_polygons(layer=200 + number, datatype=0)
        if not polys:
            if number == 1:
                raise ValueError('No marker found on layer 201/0')
            break
        if len(polys) != 1:
            raise ValueError(f'Expected one polygon for port {number}; found {len(polys)}')
        polygon = polys[0]
        points = np.asarray(polygon.points)
        ports.append({'number': number, 'layer': 200 + number,
                      'center_um': np.mean(points, axis=0).tolist(),
                      'bbox_um': [points.min(axis=0).tolist(), points.max(axis=0).tolist()]})
    if len(ports) < 2:
        raise ValueError('At least two port markers are needed')
    return ports


def load_driver(path):
    spec = importlib.util.spec_from_file_location('nport_model_driver', path)
    if spec is None or spec.loader is None:
        raise ValueError('Cannot load the supplied openEMS driver')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if not callable(getattr(mod, 'build_simulation', None)):
        raise ValueError('Driver must define build_simulation(gds_path, ports, excite_port, simdir, frequencies_hz, reference_ohm)')
    return mod.build_simulation


def save_touchstone(path, freqs, smatrix, z0):
    n = smatrix.shape[1]
    with Path(path).open('w', encoding='ascii') as f:
        f.write(f'! Reconstructed N-port runner; {n} ports, one excitation per column\n')
        f.write(f'# Hz S RI R {z0:g}\n')
        for k, freq in enumerate(freqs):
            values = [f'{freq:.12g}']
            for col in range(n):
                for row in range(n):
                    v = smatrix[k, row, col]
                    values += [f'{v.real:.12g}', f'{v.imag:.12g}']
            f.write(' '.join(values) + '\n')


def run(gds_path, driver_path, out_dir, f_start_ghz, f_stop_ghz, points, z0, dry_run):
    gds_path, driver_path, out_dir = Path(gds_path), Path(driver_path), Path(out_dir)
    if not gds_path.is_file():
        raise FileNotFoundError(gds_path)
    if not 0 < f_start_ghz < f_stop_ghz or points < 2 or z0 <= 0:
        raise ValueError('Require 0 < start < stop, >= 2 points and positive Z0')
    ports = discover_ports(gds_path)
    freqs = np.linspace(f_start_ghz * 1e9, f_stop_ghz * 1e9, points)
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = {'source_gds': str(gds_path), 'port_markers': ports,
                'start_ghz': f_start_ghz, 'stop_ghz': f_stop_ghz,
                'points': points, 'reference_ohm': z0,
                'status': 'dry-run' if dry_run else 'simulation-requested'}
    (out_dir/'run_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(f'Detected {len(ports)} GDS ports: ' + ', '.join(f"{p['number']} ({p['layer']}/0)" for p in ports))
    if dry_run:
        return
    if not driver_path.is_file():
        raise FileNotFoundError('Driver is required for real FDTD: ' + str(driver_path))
    build = load_driver(driver_path)
    matrix = np.empty((points, len(ports), len(ports)), dtype=complex)
    for column in range(len(ports)):
        simdir = out_dir/f'excite_port_{column + 1}'
        simdir.mkdir(parents=True, exist_ok=True)
        fdtd, port_objects = build(gds_path=gds_path, ports=ports,
                                   excite_port=column + 1, simdir=simdir,
                                   frequencies_hz=freqs, reference_ohm=z0)
        if len(port_objects) != len(ports):
            raise ValueError('Driver must return one port object per detected port')
        fdtd.Run(str(simdir), cleanup=True)
        for p in port_objects:
            p.CalcPort(str(simdir), freqs, ref_impedance=z0)
        inc = np.asarray(port_objects[column].uf_inc)
        if inc.shape != (points,) or np.any(np.abs(inc) < 1e-12):
            raise ValueError(f'Zero/invalid incident wave for driven port {column+1}')
        for row, p in enumerate(port_objects):
            wave = np.asarray(p.uf_ref)
            if wave.shape != (points,):
                raise ValueError(f'Invalid wave vector shape at port {row+1}')
            matrix[:, row, column] = wave/inc
    output = out_dir/f'{gds_path.stem}.s{len(ports)}p'
    save_touchstone(output, freqs, matrix, z0)
    print(f'Wrote {output} (all {len(ports)} independent port excitations)')


def main():
    pa = argparse.ArgumentParser(description=__doc__)
    pa.add_argument('gds', type=Path, nargs='?')
    pa.add_argument('--driver', type=Path, default=Path('openems_model_driver.py'))
    pa.add_argument('--out-dir', type=Path, default=Path('generated_em'))
    pa.add_argument('--start-ghz', type=float, default=0.1)
    pa.add_argument('--stop-ghz', type=float, default=20.)
    pa.add_argument('--points', type=int, default=201)
    pa.add_argument('--z0', type=float, default=50.)
    pa.add_argument('--dry-run', action='store_true')
    args = pa.parse_args()
    gds = args.gds or Path(input('GDS filename: ').strip())
    run(gds, args.driver, args.out_dir, args.start_ghz, args.stop_ghz,
        args.points, args.z0, args.dry_run)


if __name__ == '__main__':
    main()
