import klayout.db as db
import math
import numpy as np
from .BasicCurve import *
from .BasicComponents import *
from .Resonator import *


def all_pass_adiabatic_euler_ring(
    canvas: db.Layout,
    layer: int,
    waveguide_width: float = 0.45,
    arc_length1: float = 100.0,
    arc_length2: float = 80.0,
    straight_length: float = 10.0,
    gap: float = 0.2
) -> db.Cell:
    """
    Creates an all-pass adiabatic euler ring consisting of a racetrack resonator and a bus waveguide.

    The racetrack resonator is coupled to the bus waveguide, and the gap controls the separation
    between them. 

    Args:
        canvas: The layout object where the all-pass ring resonator will be created.
        layer: The layer index where the waveguide should be inserted.
        waveguide_width: The width of the waveguide (default is 0.45 microns).
        arc_length1: Length of outter arc (in microns).
        arc_length2: Length of inner arc (in microns).
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
            all_pass_adiabatic_euler_ring_1 = all_pass_adiabatic_euler_ring(
            canvas=layout,
            layer=layer_index,
            waveguide_width=waveguide_width,
            arc_length1 = 100.0,
            arc_length2 = 80.0,
            straight_lengt = 10.0,
            gap=0.2

            )

    """
    # Create a new cell for the all-pass ring resonator
    top_cell = canvas.create_cell("ALL_PASS_ADIABATIC_EULER_RING")

    # Create the racetrack resonator
    racetrack = adiabatic_euler_racetrack_resonator(canvas=canvas, layer=layer,width=waveguide_width,straight_length=straight_length, num_points=2000, arc_length1=arc_length1, arc_length2=arc_length2)




    s1 = arc_length1 / 2
    alpha1 = np.pi / (s1 ** 2)
    L = np.sqrt(np.pi / alpha1)  # Constant ℓ

    # Compute Fresnel integrals to calculate X and Y coordinates
    fresnel_sin, fresnel_cos = fresnel(1)
    x_coords = L * fresnel_cos  # C(s/ℓ)
    # y_coords = L * fresnel_sin  # S(s/ℓ)

    # Create the bus waveguide (length is adjusted to match the racetrack)
    bus_length = straight_length + 2 *  x_coords
    bus_waveguide = straight_wg(
        canvas=canvas,
        layer=layer,
        length=bus_length,
        width=waveguide_width
    )

    # Insert the racetrack resonator into the all-pass ring cell
    top_cell.insert(db.DCellInstArray(racetrack.cell_index(), db.DTrans()))

    # Insert the bus waveguide into the all-pass ring cell with a vertical offset (shifted by the gap)
    # offset = db.DVector(- x_coords - waveguide_width / 2, -gap - waveguide_width)
    offset = db.DVector(- x_coords -straight_length, -gap - waveguide_width/2)
    top_cell.insert(db.DCellInstArray(bus_waveguide.cell_index(), db.DTrans(offset)))

    return top_cell