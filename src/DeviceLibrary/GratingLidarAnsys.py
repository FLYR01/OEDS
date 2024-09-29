import klayout.db as db
import math
import numpy as np
from .BasicCurve import *
from .BasicComponents import *
from .Resonator import *
from .BasicOperator import *


def grating_ansys_lidar(
    canvas: db.Layout,
    layer_full_etch: int,
    layer_partial_etch: int = None,
    width1: float = 0.33,
    width2: float = 0.33,
    height1: float = 0.45,
    height2: float = 0.8,
    num_pairs: int = 20,
) -> db.Cell:
    """Creates a grating structure for an Ansys LIDAR simulation.

    Args:
        canvas: The layout canvas where the cell will be created.
        layer_full_etch: The layer index for the full etch pattern.
        layer_partial_etch: Optional; The layer index for the partial etch pattern.
        width1: The width of the first rectangle in each pair. Defaults to 0.33.
        width2: The width of the second rectangle in each pair. Defaults to 0.33.
        height1: The height of the first rectangle in each pair. Defaults to 0.45.
        height2: The height of the second rectangle in each pair. Defaults to 0.8.
        num_pairs: The number of pairs of rectangles. Defaults to 20.

    Returns:
        A cell containing the grating structure.
    """
    # Create the top cell for the grating structure
    top_cell = canvas.create_cell("GRATING_ANSYS")

    # Iterate over the number of pairs to create the grating
    for pair_index in range(num_pairs):
        # Calculate the horizontal offset for each pair of rectangles
        offset_x = pair_index * (width1 + width2)

        # Calculate the vertical center based on the maximum height
        center_y = max(height1, height2) / 2

        # Create and insert the first rectangle (width1 x height1)
        rect1 = db.DBox(
            offset_x,
            center_y - height1 / 2,
            offset_x + width1,
            center_y + height1 / 2,
        )
        top_cell.shapes(layer_full_etch).insert(db.DPolygon(rect1))

        # Create and insert the second rectangle (width2 x height2)
        rect2 = db.DBox(
            offset_x + width1,
            center_y - height2 / 2,
            offset_x + width1 + width2,
            center_y + height2 / 2,
        )
        top_cell.shapes(layer_full_etch).insert(db.DPolygon(rect2))

        # If layer_partial_etch is provided, you can add corresponding logic here
        if layer_partial_etch is not None:
            # Example: Do something with layer_partial_etch if needed
            pass  # Replace with actual logic if necessary

    return top_cell
