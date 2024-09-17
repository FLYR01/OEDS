import klayout.db as db
import math
import numpy as np
from .BasicCurve import *  # Import all functions from BasicCurve


def bend_wg(
        canvas: db.Layout,
        layer: int,
        curve_points: list[tuple[float, float]],
        width: float
) -> db.Cell:
    """Create a cell with a rounded bend of given list of (x, y) coordinates.

    Args:
        ly: The layout object to which the bend will be added.
        layer: The layer where the bend should be inserted.
        curve_points: A list of (x, y) coordinates representing the curve.
        width: Width of the waveguide.

    Returns:
        A db.Cell object containing the bend.

    Example:
        .. code::

            bend_cell = bend_waveguide(
                canvas=layout, layer=layer, curve_points=arc_points, width=0.45
            )
    """
    bend_cell = canvas.create_cell("BEND")

    # Create points for the bend path
    points = [db.DPoint(x, y) for x, y in curve_points]

    # Create and insert the bend path
    bend = db.DPath(points, width)
    bend_cell.shapes(layer).insert(bend)

    return bend_cell

def straight_wg(
        canvas: db.Layout,
        layer: int,
        length: float,
        width: float
) -> db.Cell:
    """Create a cell with a straight waveguide of given length and width.

    Args:
        canvas: The layout object (db.Layout) where the waveguide will be added.
        layer: The layer index (int) where the waveguide should be inserted.
        length: Length of the waveguide (in microns).
        width: Width of the waveguide (in microns).

    Returns:
        A db.Cell object containing the straight waveguide.

    Example:
        .. code::

            wg_cell = straight_waveguide(
                canvas=layout, layer=layer, length=100.0, width=0.45
            )
    """
    # Create a new cell for the straight waveguide
    wg_cell = canvas.create_cell("STRAIGHT")

    # Insert a rectangle representing the waveguide
    wg_cell.shapes(layer).insert(db.DBox(0, -width / 2, length, width / 2))

    return wg_cell

def circle_arc180_wg(
        canvas: db.Layout,
        layer: int,
        radius: float,
        width: float,
        num_points: int = 1000,
) -> db.Cell:
    """Create a cell with a 180-degree arc-shaped waveguide of given radius and width.

    This function generates a 180-degree circular arc waveguide, creates a new
    cell in the layout, and inserts the arc waveguide into the specified layer.
    It also inserts a point after the first point and before the last point
    with y-coordinate of 0.001.

    Args:
        canvas: The layout object (db.Layout) to which the waveguide will be added.
        layer: The layer index (int) where the waveguide should be inserted.
        radius: The radius of the arc (in microns).
        width: The width of the waveguide (in microns).
        num_points: Number of points to use for generating the circle bend curve (default is 1000).


    Returns:
        A db.Cell object containing the 180-degree arc waveguide.

    Example:
        .. code::

            bend_cell = circle_arc180_wg(
                canvas=layout, layer=layer, radius=100, width=0.45
            )
         -
        |  \
       o1  o2

    """
    # Create a new cell for the arc-shaped waveguide
    circle_arc180_cell = canvas.create_cell("CIRCLE_ARC180")

    # Generate the 180-degree arc points
    curve_points = circle(center_x=0.0, center_y=0.0, radius=radius, num_points=num_points, angle=180)

    # Insert a new point after the first point with the same x-coordinate but y = 0.001
    first_point = curve_points[0]
    curve_points.insert(1, (first_point[0], 0.001))

    # Insert a new point before the last point with the same x-coordinate but y = 0.001
    last_point = curve_points[-1]
    curve_points.insert(-1, (last_point[0], 0.001))

    # Create points for the bend path
    points = [db.DPoint(x, y) for x, y in curve_points]

    # Create and insert the bend path
    bend = db.DPath(points, width)
    circle_arc180_cell.shapes(layer).insert(bend)

    return circle_arc180_cell


def euler_arc180_wg(
        canvas: db.Layout,
        layer: int,
        arc_length: float,
        width: float,
        num_points: int = 1000,
) -> db.Cell:
    """
    Creates a 180-degree Euler arc-shaped waveguide in a layout cell.

    Args:
        canvas: The layout object to which the waveguide will be added.
        layer: The layer index where the waveguide should be inserted.
        arc_length: Length of the 180-degree Euler bend waveguide (in microns).
        width: Width of the waveguide (in microns).
        num_points: Number of points to use for generating the Euler curve (default is 1000).

    Returns:
        A db.Cell object containing the 180-degree arc waveguide.

    Example:
        .. code::

            bend_cell = ceuler_arc180_wg(
                canvas=layout, layer=layer, arc_length=50, width=0.45
            )

        o2 _
             \
             )
       o1 _ /
    """
    # Create a new cell for the Euler arc waveguide
    euler_arc_cell = canvas.create_cell("EULER_ARC180")

    # Calculate alpha for the Euler spiral
    s = arc_length / 2
    alpha = np.pi / (s ** 2)

    # Generate the points for the bottom curve of the Euler spiral
    bottom_curve_points = euler_spiral(s=s, alpha=alpha, num_points=num_points)

    # Calculate the y-shift to reflect the curve vertically for the top arc
    y_shift = 2 * bottom_curve_points[-1][1]

    # Generate the top curve by reflecting the bottom curve
    top_curve_points = [(x, -y + y_shift) for x, y in bottom_curve_points]

    # Combine the bottom and top curve points to form the full waveguide
    full_curve_points = bottom_curve_points + top_curve_points[::-1]

    # Insert additional points to smooth the transition at the start and end of the arc
    first_point_x, first_point_y = full_curve_points[0]
    last_point_x, last_point_y = full_curve_points[-1]
    full_curve_points.insert(1, (first_point_x + 0.001, first_point_y))
    full_curve_points.insert(-1, (last_point_x + 0.001, last_point_y))

    # Create the path of the waveguide from the generated points
    path_points = [db.DPoint(x, y) for x, y in full_curve_points]
    bend_path = db.DPath(path_points, width)

    # Insert the waveguide into the specified layer
    euler_arc_cell.shapes(layer).insert(bend_path)

    return euler_arc_cell
