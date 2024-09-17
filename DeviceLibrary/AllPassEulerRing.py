import klayout.db as db
import math
import numpy as np
from .BasicCurve import *
from .BasicComponents import *
from .Resonator import *


def all_pass_euler_ring(
    canvas: db.Layout,
    layer: int,
    waveguide_width: float = 0.45,
    arc_length: float = 100.0,
    straight_length: float = 10.0,
    gap: float = 0.2
) -> db.Cell:
    """
    Creates an all-pass ring consisting of a racetrack resonator and a bus waveguide.

    The racetrack resonator is coupled to the bus waveguide, and the gap controls the separation
    between them. T

    Args:
        canvas: The layout object where the all-pass ring resonator will be created.
        layer: The layer index where the waveguide should be inserted.
        waveguide_width: The width of the waveguide (default is 0.45 microns).
        arc_length: The arc length of the 180-degree Euler bend (in microns).
        straight_length: The length of the straight sections of the racetrack resonator (in microns).
        gap: The gap between the racetrack resonator and the bus waveguide (in microns).

    Returns:
        A db.Cell object containing the all-pass ring resonator.

    Example:
        .. code-block:: python

            layout = db.Layout()
            layer_index = layout.layer(1, 0)

            # Define parameters for the all-pass ring resonator
            waveguide_width = 0.45
            radius = 100.0
            straight_length = 10.0
            gap = 0.2

            # Create the all-pass ring resonator
            all_pass_ring = create_all_pass_ring(
                canvas=layout,
                layer=layer_index,
                waveguide_width=waveguide_width,
                radius=radius,
                straight_length=straight_length,
                gap=gap
            )

    """
    # Create a new cell for the all-pass ring resonator
    all_pass_ring_cell = canvas.create_cell("ALL_PASS_EULER_RING")

    # Create the racetrack resonator
    racetrack = euler_racetrack_resonator(canvas, layer, arc_length, straight_length, waveguide_width)
    s = arc_length / 2
    alpha = np.pi / (s ** 2)
    L = np.sqrt(np.pi / alpha)  # Constant ℓ

    # Compute Fresnel integrals to calculate X and Y coordinates
    fresnel_sin, fresnel_cos = fresnel(1)
    x_coords = L * fresnel_cos  # C(s/ℓ)
    # y_coords = L * fresnel_sin  # S(s/ℓ)

    # Create the bus waveguide (length is adjusted to match the racetrack)
    bus_length = straight_length + 2 *  x_coords  + waveguide_width
    bus_waveguide = straight_wg(
        canvas=canvas,
        layer=layer,
        length=bus_length,
        width=waveguide_width
    )

    # Insert the racetrack resonator into the all-pass ring cell
    all_pass_ring_cell.insert(db.DCellInstArray(racetrack.cell_index(), db.DTrans()))

    # Insert the bus waveguide into the all-pass ring cell with a vertical offset (shifted by the gap)
    offset = db.DVector(- x_coords - waveguide_width / 2, -gap - waveguide_width)
    all_pass_ring_cell.insert(db.DCellInstArray(bus_waveguide.cell_index(), db.DTrans(offset)))

    return all_pass_ring_cell
