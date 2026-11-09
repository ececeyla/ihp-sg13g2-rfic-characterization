#!/usr/bin/env python3
"""Parametric GDS examples based on dimensions/layers named in the KIT report.

Not original internship GDS or a complete DRC-clean silicon implementation.
Dielectric/metal thickness and SG13G2 stack must come from the real PDK.
"""
import argparse
from pathlib import Path

GROUND = (8, 0)       # Metal1 (KIT report)
SIGNAL = (134, 0)     # TopMetal2 (KIT report)
PORTS = [(201, 0), (202, 0), (203, 0)]


def rectangle(cell, gd, a, b, layer):
    import gdstk
    cell.add(gdstk.rectangle(a, b, layer=layer[0], datatype=layer[1]))


def build(out_dir):
    import gdstk
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    # gdstk's cell geometry is in micrometers: unit=1e-6 m.
    lib = gdstk.Library(unit=1e-6, precision=1e-9)
    line = lib.new_cell('METAL_2PORT_RECONSTRUCTED')
    rectangle(line, None, (-120, -100), (120, 100), GROUND)
    rectangle(line, None, (-100, -10), (100, 10), SIGNAL)
    rectangle(line, None, (-100, -10), (-90, 10), PORTS[0])
    rectangle(line, None, (90, -10), (100, 10), PORTS[1])
    lib.write_gds(str(out_dir/'metal_2port_reconstructed.gds'))
    # T-junction proportions were not specified in the PDF: illustrative only.
    lib2 = gdstk.Library(unit=1e-6, precision=1e-9)
    tj = lib2.new_cell('T_JUNCTION_ILLUSTRATIVE')
    rectangle(tj, None, (-130, -130), (130, 130), GROUND)
    rectangle(tj, None, (-100, -10), (100, 10), SIGNAL)
    rectangle(tj, None, (-10, -10), (10, 100), SIGNAL)
    rectangle(tj, None, (-100, -10), (-90, 10), PORTS[0])
    rectangle(tj, None, (90, -10), (100, 10), PORTS[1])
    rectangle(tj, None, (-10, 90), (10, 100), PORTS[2])
    lib2.write_gds(str(out_dir/'t_junction_illustrative.gds'))
    return out_dir


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out-dir', type=Path, default=Path('generated_gds'))
    args = parser.parse_args()
    print('Generated:', build(args.out_dir))


if __name__ == '__main__':
    main()
