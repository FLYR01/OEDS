import klayout.db as db
import math
import numpy as np
from .BasicCurve import *
from .BasicComponents import *


def racetrack_resonator(
        canvas: db.Layout,
        layer: int,
        radius: float,
        straight_length: float,
        width: float
) -> db.Cell:
    """
    Creates a racetrack resonator using straight waveguides and 180-degree bends.

    The racetrack resonator is formed by two straight waveguides connected by two
    180-degree circular arc bends on either end.

    Args:
        canvas: The layout object where the resonator will be added.
        layer: The layer index where the waveguide should be inserted.
        radius: The radius of the 180-degree bends (in microns).
        straight_length: The length of the straight sections (in microns).
        width: The width of the waveguide (in microns).

    Returns:
        A db.Cell object containing the racetrack resonator.
    """
    # Create a new cell for the racetrack resonator
    resonator_cell = canvas.create_cell("RACETRACK_RESONATOR")

    # Create the top and bottom straight sections of the racetrack
    straight_wg_top = straight_wg(canvas, layer, straight_length, width)
    straight_wg_bottom = straight_wg(canvas, layer, straight_length, width)

    # Create the 180-degree bends using the specified radius and width
    bend_wg = circle_arc180_wg(canvas, layer, radius=radius, width=width)

    # Insert the top and bottom straight sections
    resonator_cell.insert(
        db.DCellInstArray(straight_wg_top.cell_index(), db.DTrans(db.DVector(0, 0)))
    )
    resonator_cell.insert(
        db.DCellInstArray(straight_wg_bottom.cell_index(), db.DTrans(db.DVector(0, 2 * radius)))
    )

    # Insert the two 180-degree bends (left and right)
    resonator_cell.insert(
        db.DCellInstArray(bend_wg.cell_index(), db.DTrans(db.DTrans.R90, db.DVector(0, radius)))
    )
    resonator_cell.insert(
        db.DCellInstArray(bend_wg.cell_index(), db.DTrans(db.DTrans.R270, db.DVector(straight_length, radius)))
    )

    return resonator_cell




def euler_racetrack_resonator(
    canvas: db.Layout,
    layer: int,
    arc_length: float,
    straight_length: float,
    width: float
) -> db.Cell:
    """
    Creates an Euler racetrack resonator using straight waveguides and Euler bends.

    The resonator consists of two straight sections connected by two 180-degree
    Euler bends on either side, forming a racetrack shape.

    Args:
        canvas: The layout object where the resonator will be added.
        layer: The layer index where the waveguide should be inserted.
        arc_length: The arc length of the 180-degree Euler bend (in microns).
        straight_length: The length of the straight sections (in microns).
        width: The width of the waveguide (in microns).

    Returns:
        A db.Cell object containing the Euler racetrack resonator.

    Example:
        .. code-block:: python

    """
    # Create a new cell for the Euler racetrack resonator
    resonator_cell = canvas.create_cell("EULER_RACETRACK")

    # Compute parameters for Euler bends
    s = arc_length / 2
    alpha = np.pi / (s ** 2)
    L = np.sqrt(np.pi / alpha)  # Constant ℓ

    # Compute Fresnel integrals to calculate X and Y coordinates
    fresnel_sin, fresnel_cos = fresnel(1)
    x_coords = L * fresnel_cos  # C(s/ℓ)
    y_coords = L * fresnel_sin  # S(s/ℓ)

    # Create the top and bottom straight waveguides
    straight_wg_top = straight_wg(canvas, layer, straight_length, width)
    straight_wg_bottom = straight_wg(canvas, layer, straight_length, width)

    # Create the 180-degree Euler bend
    bend_euler = euler_arc180_wg(canvas=canvas, layer=layer, arc_length=arc_length, width=width)

    # Insert the top and bottom straight waveguides
    resonator_cell.insert(
        db.DCellInstArray(straight_wg_top.cell_index(), db.DTrans(db.DVector(0, 0)))
    )
    resonator_cell.insert(
        db.DCellInstArray(straight_wg_bottom.cell_index(), db.DTrans(db.DVector(0, 2 * y_coords)))
    )

    # Insert the two Euler bends (left and right)
    resonator_cell.insert(
        db.DCellInstArray(bend_euler.cell_index(), db.DTrans(db.DTrans.R0, db.DVector(straight_length, 0)))
    )
    resonator_cell.insert(
        db.DCellInstArray(bend_euler.cell_index(), db.DTrans(db.DTrans.R180, db.DVector(0, 2 * y_coords)))
    )

    return resonator_cell
