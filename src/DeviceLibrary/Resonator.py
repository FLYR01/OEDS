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

def adiabatic_euler_racetrack_resonator(
        canvas: db.Layout,
        layer: int,
        width: float = 0.45,
        straight_length: float = 3,
        num_points: int = 2000,
        arc_length1: float = 20,
        arc_length2: float = 17,
) -> db.Cell:
    """
    Creates an adiabatic Euler racetrack resonator in a layout cell.

    Args:
        canvas: The layout object to which the adiabatic Euler racetrack resonator will be added.
        layer: The layer index where the adiabatic Euler racetrack resonator should be inserted.
        width: Width of the waveguide (in microns).
        straight_length: Length of the straight section connecting the two arcs (in microns).
        num_points: Number of points to use for generating the Euler curves.
        arc_length1: Length of outter arc (in microns).
        arc_length2: Length of inner arc (in microns).

    Returns:
        A db.Cell object containing the adiabatic Euler racetrack resonator.

    Example:
        .. code::

            ring_cell = create_adiabatic_ruler_ring(
                canvas=layout, layer=layer, width=450, straight_length=3000
            )
    """
    # Create a top-level cell for the adiabatic Euler ruler ring
    top_cell = canvas.create_cell("ADIABATIC_EULER_RING")
    arc_length1=arc_length1*1000
    arc_length2=arc_length2*1000
    width=width*1000
    straight_length=straight_length*1000



    # Define s and alpha for each arc
    s1, s2 = arc_length1 / 2, arc_length2 / 2
    alpha1, alpha2 = np.pi / (s1 ** 2), np.pi / (s2 ** 2)

    # Generate points for the two Euler arcs
    curve_points1 = euler_arc180_curve(s=s1, alpha=alpha1, num_points=num_points, x_bias=0, y_bias=0)
    curve_points2 = euler_arc180_curve(s=s2, alpha=alpha2, num_points=num_points, x_bias=0, y_bias=width)

    # Combine the two sets of curve points
    full_curve_points = np.vstack((curve_points1, curve_points2[::-1]))

    # Create polygon from combined curve points
    polygon = db.Polygon([db.Point(*pt) for pt in full_curve_points])

    # Create the region and insert the polygon
    region = db.Region()
    region.insert(polygon)

    # Duplicate and rotate the arc by 180 degrees
    transformation = db.ICplxTrans(1.0, 180, True, -straight_length, 0)  # No mirror, origin shifted by straight_length
    left_arc = region.transformed(transformation)

    # Create the waveguides connecting the arcs
    poly_bottom_waveguide = db.Polygon([
        db.Point(curve_points1[0][0], curve_points1[0][1]),
        db.Point(curve_points2[0][0], curve_points2[0][1]),
        db.Point(curve_points2[0][0] - straight_length, curve_points2[0][1]),
        db.Point(curve_points1[0][0] - straight_length, curve_points1[0][1]),
    ])

    poly_top_waveguide = db.Polygon([
        db.Point(curve_points1[-1][0], curve_points1[-1][1]),
        db.Point(curve_points2[-1][0], curve_points2[-1][1]),
        db.Point(curve_points2[-1][0] - straight_length, curve_points2[-1][1]),
        db.Point(curve_points1[-1][0] - straight_length, curve_points1[-1][1]),
    ])

    # Insert the arcs and waveguides into the top-level cell
    top_cell.shapes(layer).insert(region)
    top_cell.shapes(layer).insert(left_arc)
    top_cell.shapes(layer).insert(poly_bottom_waveguide)
    top_cell.shapes(layer).insert(poly_top_waveguide)

    return top_cell
