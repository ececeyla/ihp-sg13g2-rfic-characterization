"""Contract template for the KIT user's original GDS-to-CSXCAD/openEMS model.

Do not enter invented SG13G2 stack dimensions. Copy this file, fill from a
licensed verified PDK/flow, and pass its path to run_auto_nport_interactive.py.
"""


def build_simulation(gds_path, ports, excite_port, simdir, frequencies_hz, reference_ohm):
    """Return (new openEMS FDTD object, one properly terminated port per marker).

    Required in a real implementation:
      * Import GDS Metal1 8/0, TopMetal2 134/0 (and any relevant conductors).
      * Use verified SG13G2-nonsub process stack with metal/dielectric properties.
      * Use marker layers 201/0, 202/0, ... to place vertical/lumped ports.
      * Set PML boundary, FDTD excitation, and mesh (including port z cells).
      * Set excite=1 only for `excite_port`; all other ports excite=0.
      * Return fresh FDTD and correctly ordered port objects for each run.
    """
    raise NotImplementedError('Connect the original verified SG13G2 GDS-to-openEMS driver first')
